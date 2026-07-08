## Context

Chin & Beard Suds Co management team have heard there is unrest in a few of their Northern stores and asked their HR data manager to pull together some supporting files. Sadly for us, those files are going to take some data prep to ensure we can conduct the analysis we want to. The rumours we've heard are: 1. We are paying people more than our Corporate Pay Ranges that we have agreed 2. Bonuses account for very little (less than 10%) of someone's salary We want your help to answer these questions for us. There are some contractual pay conditions you should consider: - Bonus will be paid as long as you are still an employee for at least the 1st day of the final month of the quarter. - Consider only employees who received salary during 2019 - Anyone paid above the salary range will receive no bonus (we pay them enough already) - Assume today's date for the analysis is 1st October 2019

## Requirements

- Input the data
- Use all sheets of the Input Data source here
- Only look at staff who have been employed during 2019 (if they may have started in 2017/18 but have at least been paid by C&BS Co during 2019)
- Find the outliers and form an output data set on this:
  - Find who's pay sits outside of the pay bands
  - Find out who is in the incorrect pay bandby checking actual roles against expected roles (based on assumption on pay bands and our three possible roles)
- Form a dataset based on the sales data to assess whether each store has met their quarterly sales targets
  - If so, determine how much each staff member should have been paid in 2019 (full year), bonuses paid for 2019 and what % the bonuses are of basic salary per person.
- ignore the field '% above target for bonus', we didn't end up using this field
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - % Bonus of Salary
    - Bonus amount
    - Store
    - Name
    - Total Salary

- output_02.csv
  - 14 fields:
    - Correct Salary for Role?
    - Assumed Position based on Salary Range
    - Pay Status
    - End Date
    - Salary Range Minimum
    - Salary Range Maximum
    - Bonus amount
    - Range
    - % above target for bonus
    - Role
    - Start Date
    - Salary
    - Store
    - Name
