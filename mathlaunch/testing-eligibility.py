# ====================================
#   Code to analyze weekly MLC hours
# ====================================


import pandas as pd
import re



# =====================
#   Read in raw files
# =====================

# Get input file name
#  Uncomment to get user input instead of hard-coding file names:
#infile = input("Enter name of ALEKS gradebook file:  ")
#  Comment out if using user input instead:
infile = "aleks-gradebook_2023-02-27.xlsx"

# Read in file as dataframes
grades = pd.read_excel(infile, skiprows=[1])



# ================================================
#   Preprocess dataframe for easier manipulation
# ================================================

# Rewrite column names without assignment date included
new_col = []
for col in grades.columns:
    # Cut off date at end of string
    temp = col.split(" - ")[0]
    # Replace problem characters
    temp = temp.replace(" ", "_")
    temp = re.sub(r"[()%]", "", temp)
    new_col.append(temp)
grades.columns = new_col

# Create variables to hold column names that will be used often
name = "Student_Name"
#  ALEKS Modules
mods = [col for col in grades.columns \
    if "Module" in col]
mods.sort()
#  Assigned Knowledge Checks
akcs = [col for col in grades.columns \
    if "Assigned_Knowledge_Check" in col]
akcs.sort()
#  Practice Tests
pracs = [col for col in grades.columns \
    if "Practice_Test" in col]
pracs.sort()
#  Comprehensive Tests
comps = [col for col in grades.columns \
    if "Comprehensive_Test" in col]
comps.sort()

# Sort dataframe by student name
grades = grades.sort_values(by=[name])

# Replace strings in assignment columns with NaN,
#  then change NaN to 0
all_assign = mods + akcs + pracs + comps
grades[all_assign] = grades[all_assign].apply(\
    pd.to_numeric, errors="coerce")
grades = grades.fillna(0)



# ======================================================
#   Compile lists of students meeting certain criteria
# ======================================================

# Make strings for query conditions
mods_completed = "( " + \
    " & ".join(\
    [m + " >= 0.9" for m in mods]) + \
    " )"
akcs_completed = "( " + \
    akcs[-1] + " >= 0.7 | ( " + \
    " & ".join([a + " > 0" for a in akcs]) + " )" + \
    " )"
prac_taken = "( " + \
    " | ".join(\
    [p + " > 0" for p in pracs]) + \
    " )"
comp_passed = "( " + \
    " | ".join(\
    [c + " >= 0.7" for c in comps]) + \
    " )"
comp_failed = "( " + \
    " | ".join(\
    ["( " + c + " > 0 & " + c + " < 0.7 )" for c in comps]) + \
    " )"

# Use query conditions to make eligibility lists
#  Students eligible to take Practice Test
ready_for_prac = grades.query(\
    akcs_completed + \
    " & ~" + comp_passed + " & ~" + comp_failed)\
    [name].tolist()
#  Students who only need Modules to be eligible for Comprehensive Test
needs_mods = grades.query(\
    prac_taken + " & ~" + mods_completed + \
    " & ~" + comp_passed + " & ~" + comp_failed)\
    [name].tolist()
#  Students who only need Practice Test to be eligible for Comprehensive Test
needs_prac = grades.query(\
    akcs_completed + " & " + mods_completed + " & ~" + prac_taken + \
    " & ~" + comp_passed + " & ~" + comp_failed)\
    [name].tolist()
#  Students eligible to take Comprehensive Test
ready_for_comp = grades.query(\
    prac_taken + " & " + mods_completed + \
    " & ~" + comp_passed + " & ~" + comp_failed)\
    [name].tolist()
#  Students who passed Comprehensive Test
passed = grades.query(\
    comp_passed)\
    [name].tolist()
#  Students who need to retake Comprehensive Test
failed_comp = grades.query(\
    comp_failed + " & ~" + comp_passed)\
    [name].tolist()



# =========================
#   Print lists to stdout
# =========================

print("\nStudents eligible to take Practice Test:")
for student in ready_for_prac:
    print(student)

print("\nStudents who just need Modules:")
for student in needs_mods:
    print(student)

print("\nStudents who just need Practice Test:")
for student in needs_prac:
    print(student)

print("\nStudents eligible to take Comprehensive Test:")
for student in ready_for_comp:
    print(student)

print("\nStudents who need to retake Comprehensive:")
for student in failed_comp:
    print(student)

print("\nStudents who passed Comprehensive:")
for student in passed:
    print(student)
