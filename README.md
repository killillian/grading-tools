# grading-tools

Repository to hold scripts, codes, etc. used to automate grading processes for classes taught at UCF

---

## mathlaunch

Directory for grading tools used with UCF Math Launch (ML) Program:

- `mlc-hours.py`:  Takes in Webcourses gradebook roster and itemized Math Launch Center (MLC) report. Adds up total weekly hours for students who are in the roster, writes these results to a new csv file, and prints out names of students who logged time in the MLC but are not enrolled in the ML course.

- `testing-eligibility.py`:  Takes in ALEKS gradebook as an Excel file and prints list of students to stdout according to eligibility criteria ("Ready for Practice Test," "Needs Practice Test only," "Needs Modules only," "Ready for Comprehensive Test," "Passed Comprehensive Test," "Failed Comprehensive Test")
