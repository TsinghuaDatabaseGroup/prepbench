## Context
The Talent Acquisition team would like to understand if we are attracting qualified candidates to apply for open roles. They are able to extract a report from the applicant tracking system, but it needs some preparation before they can complete their analysis. All of the data is in one long text string.

## Requirements

- Input the data
- Remove the header rows (row1 and year headers)
- Parse five fields from each row:
  - Application Month
  - Work Experience
  - Number Supervised
  - Industry Experience
  - Candidate Count
- Remove blank columns and the original data column
- Convert the application month to the month-ending date
- For each month, calculate the % of applicants who meet the preferred qualifications.
  - Preferred qualifications are:
    - Work Experience: at least4 years
    - Number Supervised: more than10
    - Industry Experience: Yes
  - Flag the rows that meet all of the preferred calculations
  - For each month, sum the total number of applicants and the number meeting the preferred qualifications
  - Calculate the % who met the preferred qualifications. Output the % with one decimal place
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Application Month
    - Total Candidates
    - Candidates with Preferred Qualifications
    - % of Candidates