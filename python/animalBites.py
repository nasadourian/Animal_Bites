import argparse
import pandas as pd
import matplotlib.pyplot as plt

def animalSpecies(dataframe):
    
    species_bites = animalSpeciesDataframe(dataframe, False)
    # plots the chart
    species_bites.plot.bar(title="Animal Bites by Species")
    plt.show()

def animalSpeciesDataframe(dataframe, printFrame):

    #stores specific data regarding Species and their respective counts
    bite_count = dataframe["SpeciesIDDesc"].value_counts()
    # print(species, bite_count)

    # stores species counts as a DataFrame
    df = pd.DataFrame({"Count of Bites":bite_count})
    if printFrame:
        print(df)
    return df

def coatColor(dataframe):
    coat = coatColorDataframe(dataframe, False)
    # plots the chart
    coat.plot(
        kind = "pie", 
        y='color_count',
        autopct = '%1.0f%%', 
        legend = True, 
        title = "Dog Bites by Coat Colors",
        ylabel = "Coat Colors").legend(bbox_to_anchor=(1, 1))
    # plt.legend(loc='upper right')
    plt.show()

def coatColorDataframe(dataframe, printFrame):

    # grabs the data
    dataframe = dataframe[["SpeciesIDDesc", "main_color","GenderIDDesc"]]

    # filters data with NaN
    filt = dataframe["main_color"].notna()
    dataframe = dataframe.loc[filt]
    
    # grabs counts of coat color
    dfcolor = pd.DataFrame({"color_count" : dataframe["main_color"].value_counts()})

    # Creates filter for smaller values than 100 and sets it to OTHER Row
    small_filt = dfcolor["color_count"] < 100
    other_col = dfcolor.loc[small_filt].sum().to_frame().T
    other_col.loc[0, 'index'] = "OTHER"
    other_col.set_index("index", inplace=True) 

    # Creates an other category in the database of bites 
    df = pd.concat([other_col, dfcolor.loc[~small_filt]])
    df.sort_values(by="color_count", ascending=False, inplace=True)

    if printFrame:
        print(df)
    return df

def dogBreed(dataframe):

    all_bites = dogBreedDataframe(dataframe, False)
    
    #plots only Body and Head Bites by breed sorted by Total Bites
    all_bites[["BODY", "HEAD"]].head(20).plot.bar(stacked=True, title="Dog Bites by Breed and Location")
    plt.show()

def dogBreedDataframe(dataframe, printFrame):

    df = dataframe[["BreedIDDesc", "WhereBittenIDDesc"]]

    #filters data by bite location
    filt = (df["WhereBittenIDDesc"] == "HEAD") | (df["WhereBittenIDDesc"] == "BODY")
    filt2 = df["BreedIDDesc"].notna()
    df = df.loc[filt]
    df = df.loc[filt2]

    # Organizes data using group by to sort bite location counts by breed
    df = df.groupby(["BreedIDDesc"]).value_counts().unstack()
    df = df.fillna(0)
    # Creates Total Column to help sort values by most reported bites 
    df["TOTAL"] = df["BODY"] + df["HEAD"]
    df.sort_values(by="TOTAL", ascending=False, inplace=True)

    if printFrame:
        print(df)
    return df

def timeSeries(dataframe, start, end):
    timely = timeSeriesDataframe(dataframe, False)

    # filter the years wanted for Time Series 
    timely.reset_index(inplace=True)
    filt = (timely["years"] >= start) & (timely["years"] <= end)
    timely = timely.loc[filt]
    timely.set_index("years", inplace=True)  
    
    # Organizes data using group by to sort bite location counts by breed
    timely.plot(title="Time Series by Species")
    plt.show()

def timeSeriesDataframe(dataframe, printFrame):
    df = dataframe
    # Convert to datetime format and rid of NaN
    df["bite_date"] = pd.to_datetime(df["bite_date"], dayfirst=True, format='%m/%d/%Y %H:%M', errors='coerce')
    df = df[dataframe["bite_date"].notna()]
    df = df[df["SpeciesIDDesc"].notna()]

    # Grabs only the year of date
    df["bite_year"] = df["bite_date"].dt.year

    # filters out incorrect dates
    filt = (df["bite_year"] > 2025) | (df["bite_year"] < 1985)
    df = df.loc[~filt]

    # creates the needed DataFrame and groups by year
    animalTime = pd.DataFrame({"years": df["bite_year"], "animal_type": df["SpeciesIDDesc"]})
    timeline = animalTime.groupby(["years"]).value_counts().unstack().fillna(0)

    if printFrame:
        print(timeline)
    return timeline

def main():
    startDate = 1985
    endDate = 2021

    data = pd.read_csv("animalBites.csv", header=0, parse_dates=True)
    pd.set_option("display.max_rows", len(data))

    parser = argparse.ArgumentParser(
                    description='''Please select which analysis you would like to view. 
                    There are 4 options:
                    1. Dog Bites per Dog Breed
                    2. Animal Bites per Species 
                    3. Animal Bites by Primary Coat Color 
                    4. Animal Bites Time Series by Year''')
    # no - so required argument
    parser.add_argument("plotName", 
                        help="provide name of plot to display",
                        choices=["dog_breeds", "animal_types", "coat_colors", "time_series"])
    parser.add_argument("-d", "--data", 
                        action="store_true",
                        help="show the dataframe used for the analysis")
    parser.add_argument("-f", "--filter", action="store", nargs=2, type=int,
                    help="filters dates by year for time series -- plot only")
    # added "-" short and long version so it's optional
    args = parser.parse_args()

    if (args.filter != None):
        startDate = args.filter[0]
        endDate = args.filter[1]  
    
    if args.plotName == "dog_breeds":
        if args.data:
            dogBreedDataframe(data, args.data)
        else:
            dogBreed(data)

    elif args.plotName == "animal_types":
        if args.data:
            animalSpeciesDataframe(data, args.data)
        else:
            animalSpecies(data)

    elif args.plotName == "coat_colors":
        if args.data:
            coatColorDataframe(data, args.data)
        else:
            coatColor(data)

    elif args.plotName == "time_series":
        if args.data:
            if (args.filter != None): 
                print("You have entered a year filter from", str(startDate), "to", str(endDate), end=".\n")
                print("The database will not take this filter into account.", end="\n""\n")
            timeSeriesDataframe(data, args.data)
        else:
            timeSeries(data, startDate, endDate)
main()