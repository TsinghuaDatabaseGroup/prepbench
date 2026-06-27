## Context
You have been hired to create a dataset for the Prep School that will allow them to analyse the correlation between attendance and test scores.

## Requirements

- Input the data
- First we must join the test score data set and the additional class attendance data set
- Clean Data: there’s a few spelling mistakes in the data set, use the data tool of your choice to correct these mistakes before we proceed. These mistakes are in the “Subject” Column
- Use a calculated field to clean up the test score column, so each number is a rounded to the nearest whole number
- Split the student name column so we can see the first name and surname in two separate columns, named appropriately
- If any student has an attendance percentage less than 70%, flag it as "Low Attendance" in a new column "attendance flag". Conversely, if above 90%, flag as “high attendance”. And anything else as “Medium”.
- Output the data

## Output

- output_01.csv
  - 8 fields:
    - Attendance Flag
    - First Name
    - Surname
    - Attendance_Percentage
    - Student_ID
    - Subject
    - Test_score
    - TestScoreInteger
