## Context
This Preppin' Data Challenge requires you to process student grades. The Prep School records this information in one excel sheet, with a sheet for each term the report comes from. The reports are in a fairly consistent format with 4 fields for the grades in each subject, but different date formats have been used. The school would like you to prepare two outputs:
1. A table with a student's average grade (GPA) across subjects for each term and then a calculated 3 term moving average of GPA to help identify struggling students.
2. A table with just the students who were awarded a prize, the date the award was issued, the 3 term rolling average of GPA that merited the award.

## Requirements

- Input the data
- Bring together the term data into 1 table
- Parse the different date time formats as we will need this for Output 2
- All terms report on the 16th day of the month
- Calculate each student's GPA for each term i.e. their average grade across subjects
- Calculate a 3 term moving average of each student's GPA, rounded to 2 decimal places
- Use the student lookup table to bring in names for the students and use calculated fields to get the full name of each student
- For Output 1:
- Finally create a variable that orders the table by Student Name Descending and Time Ascending so that the Prep School has an ordered table that they can look through alphabetically and see how the moving average of GPA changes over time
- For Output 2:
- In a separate flow after full name is calculated, filter to keep only terms 3 and 6, then create percentiles for each term based on the moving average of GPA
- Filter to students in the top 2%
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - Rank
    - id
    - Student Name
    - Term
    - Term Date
    - GPA
    - 3 Term GPA Moving Average

- output_02.csv
  - 6 fields:
    - id
    - Student Name
    - Term
    - Term Date
    - GPA
    - 3 Term GPA Moving Average
