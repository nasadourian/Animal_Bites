def main():
    import csv
    import pandas as pd
    import matplotlib.pyplot as plt
    dt = pd.read_csv("animalBites.csv", header=0, parse_dates=True)
    
    bites = dt[["BreedIDDesc","WhereBittenIDDesc"]] 
    bites = bites[bites["BreedIDDesc"].notna()]
    bites = bites[bites["WhereBittenIDDesc"].notna()]

    head_bites = bites.loc[bites["WhereBittenIDDesc"] == "HEAD", "BreedIDDesc"]
    body_bites = bites.loc[bites["WhereBittenIDDesc"] == "BODY", "BreedIDDesc"]

    head_bites_count = head_bites.value_counts()
    body_bites_count = body_bites.value_counts()
    
    both_bites = pd.DataFrame({"Body Bites":body_bites_count, "Head Bites":head_bites_count})
    body_bites_count = both_bites["Body Bites"].fillna(0)
    head_bites_count = both_bites["Head Bites"].fillna(0)

    bites_count = head_bites_count + body_bites_count
    bites_count = bites_count.sort_values(ascending=False)
    all_bites = pd.DataFrame({"Body Bites":body_bites_count, "Head Bites":head_bites_count, "Total Bites": bites_count})
    
    all_bites = all_bites.sort_values(by=["Total Bites"], ascending=False)
    # print(all_bites)

    all_bites[["Body Bites", "Head Bites"]].head(20).plot.bar(stacked=True)
    plt.show()

main()