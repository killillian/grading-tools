# ====================================
#   Code to analyze weekly MLC hours
# ====================================


import pandas as pd
import numpy as np



# =====================
#   Read in raw files
# =====================

# Get input file names
#  Uncomment to get user input instead of hard-coding file names:
#infile_roster = input("Enter name of Webcourses roster file:  ")
#infile_mlc = input("Enter name of MLC hours file:  ")
#  Comment out if using user input instead:
wk_roster = 4
wk_mlc = 2
infile_roster = "wk" + str(wk_roster).zfill(2) + "-roster.csv"
infile_mlc = "wk" + str(wk_mlc).zfill(2) + "-mlc-raw.csv"

# Read in files as dataframes
roster = pd.read_csv(infile_roster, skiprows=[1])
mlc = pd.read_csv(infile_mlc)

# Drop last row of roster, which contains info for a fake test student
roster = roster.drop(roster.tail(1).index)



# ======================================
#   Count total hours for each student
# ======================================

# Make dictionary to map unique Student IDs to student names
student_col = "Student"
id_col = "SIS User ID"
students = pd.Series(roster[id_col].values, \
    index=roster[student_col]).to_dict()
ids_mlc = pd.Series(mlc["Student Name"].values, \
    index=mlc["Student ID"]).to_dict()

# Add up hours for each Student ID
hours_col = "Checked In Duration (In Min)"
hours = mlc.groupby("Student ID")[hours_col].sum()

# Reshape into dictionary
hours = hours.to_dict()



# ==================================================
#   Structure output as dataframe and write to csv
# ==================================================

# Make dataframe base
df = pd.DataFrame(students.items(), \
    columns=["Student Name", "UCF ID"])
total_col = "Total MLC Time (in Min) for Week " + str(wk_mlc)
df[total_col] = 0

# Make and apply function to fill in MLC hours for each student
def insert_hours(row):
    if row["UCF ID"] in hours.keys():
        return hours[row["UCF ID"]]
    return 0
df[total_col] = df.apply(insert_hours, axis=1)

# Make list of students who did hours but are not in ML
non_intersection = set(df[df[total_col] > 0]["UCF ID"]) ^ \
    set(hours.keys())
non_ml = []
for id in non_intersection:
    non_ml.append(ids_mlc[id])
non_ml.sort()

# Uncomment to see list of students who did hours but are not in ML:
#print(non_ml)

# Write output dataframe to csv
outfile = "wk" + str(wk_mlc).zfill(2) + "-mlc-total.csv"
df.to_csv(outfile, index=False)
