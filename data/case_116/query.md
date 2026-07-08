# query_r.md

## Requirements

- Input the data
- Remove any rows that contained a total in the Project field
- Transform the structure of the table, and move all of the dates into a single column by using a Columns to Rows pivot (use the 'Wildcard Pivot' on a '/' to automatically bring in all of the date fields)
- Split the Name, Age, Area of Work field into separate columns; exclude 'Annual Leave' from the Hours field and then change the data type to a decimal number
- Calculate the total number of hours for each area, date, and employee by using an aggregation step
- Calculate the number of days and hours each person has worked using an aggregation tool; calculate the avg hours each person worked per day: Hours/Date
- Remove the 'Chats' rows from the Area field
- Calculate the total hours per person and area using an aggregation tool
- Create a new branch with an aggregation tool to calculate the total hours across all projects (group by person and sum hours); join both of these totals together using the Name field
- Calculate the % of total hours for each area: ROUND((Hours/Total Hours)*100)
- Keep Only the 'Client' rows from the Area field; join this step with the Avg Hours step using the Name field; complete final tidying
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Name
    - Area of Work
    - % of Total
    - Avg Number of Hours worked per day
