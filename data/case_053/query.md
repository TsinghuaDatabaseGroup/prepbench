## Context
This week one of our supporters, Bona, and I have collaborated on an idea for a challenge around a common issue when processing data - counting something that no longer exists in the dataset. With GDPR and other consumer focused legislation becoming more prominent, customer records are disappearing rapidly once a customer leaves a business (for good reason). However, as an analyst, this makes certain tasks more challenging, like counting how many 'x' there were in a business at anyone time. For this challenge we are looking at employees who have left the business over time as well as understanding who still remain.

## Requirements

- Input the data
- Create a full list of employees
- Create an end date for current employees that are yet to leave (use 1st March 2020) to help with calculations
- Create a scaffold month that can have the Employee data joined on to it
- Form your measures for analysis:
  - Count number of employees in employment by the company that month.
  - If the employee leaves in that month, remove them from the reporting within the month of leaving.
  - Avg Salary per employee per month
  - Total Salary paid by the company per month
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Total Monthly Salary
    - Month
    - Current Employees
    - Avg Salary per Current Employee
