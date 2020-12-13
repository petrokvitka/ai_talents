import pandas as pd
import matplotlib.pyplot as plt

csv_converted_splitted = pd.read_csv("csv_converted_splitted.csv")
print("raw shape", csv_converted_splitted.shape)
print("raw columns", csv_converted_splitted.columns)

# delete plates (reduce the size from 6477 to 6167)
cups_glasses = csv_converted_splitted[csv_converted_splitted["class"] != "plate]

print("we still have nans", cups_glasses["class"].unique()
cups_glasses = cups_glasses.dropna()
print("only cups and glasses", cups_glasses.shape)
# size reduced from 6167 to 6117

acceptable_fills = ["0", "30", "100"]
cups_glasses_reduced = cups_glasses[cups_glasses["fill"].isin(acceptable_fills)]
print("only allowed fills", cups_glasses_reduced.shape)
# size reduced from 6117 to 5993

# write to a csv
cups_glasses_reduced.to_csv("reduced_cups_glasses.csv")


#print(cups_glasses_reduced.groupby("fill").nunique())

"""
		cup	glass
fill 0		365	793
fill 30	600	3637
fill 100	140	458
		1105	4888
"""

# now create a balanced dataset
# the smallest subset is "cups with fill level 100", so we will take this as a starting point

subset_number = 140

# add cups first
dataset = cups_glasses_reduced[(cups_glasses_reduced["fill"] == "0") & (cups_glasses_reduced["class"] == "cup")].sample(n=subset_number)

dataset = dataset.append(cups_glasses_reduced[(cups_glasses_reduced["fill"] == "30") & (cups_glasses_reduced["class"] == "cup")].sample(n=subset_number))

dataset = dataset.append(cups_glasses_reduced[(cups_glasses_reduced["fill"] == "100") & (cups_glasses_reduced["class"] == "cup")].sample(n=subset_number))

# now add glasses
dataset = dataset.append(cups_glasses_reduced[(cups_glasses_reduced["fill"] == "0") & (cups_glasses_reduced["class"] == "glass")].sample(n=subset_number))

dataset = dataset.append(cups_glasses_reduced[(cups_glasses_reduced["fill"] == "30") & (cups_glasses_reduced["class"] == "glass")].sample(n=subset_number))

dataset = dataset.append(cups_glasses_reduced[(cups_glasses_reduced["fill"] == "100") & (cups_glasses_reduced["class"] == "glass")].sample(n=subset_number))

# save to csv
dataset.to_csv("balanced_dataset.csv")
