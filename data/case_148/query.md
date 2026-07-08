## Context
This data set is about Chin & Beard Suds Co. dedicated sales team. They have helped establish some of our wholesale clients so we want to understand more about their tenure with us and the actual cost we have spent on them (salary plus bonus).

## Requirements

- Input the data
- Create the Employment Range field which captures the employees full tenure at the company in the *MMM yyyy to MMM yyyy* format.
- Work out for each year employed per person:
  - Number of months they worked
  - Their salary they will have received
  - Their sales total for the year
- For each *Reporting Year* (the individual year someone worked for us), calculate their cumulative months (called Tenure)
- Determine the bonus payments the person will have received each year
  - It's 5% of their sales total
- Round Salary Paid and Yearly Bonus to two decimal places
- Add Salary Paid and Yearly Bonus together to form *Total Paid*
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - Name
    - Employment Range
    - Reporting Year
    - Tenure by End of Reporting Year
    - Salary Paid
    - Yearly Bonus
    - Total Paid
