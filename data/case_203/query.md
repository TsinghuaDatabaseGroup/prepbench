## Context
The HRIS (HR information system) keeps track of an employee’s department, but sometimes it is helpful to know the sub-department for reporting and analytics.

## Requirements

- Input the data
- From the employee data, calculate each person’s hierarchy_level
  - The employee_id_hierarchy field contains a person’s supervisory hierarchy flattened into a string (e.g. | CEO’s ID | Vice President’s ID | Director’s ID | Manager’s ID | Employee’s ID |)
  - To calculate the hierarchy level, count the number of pipes (|) in the employee_id_hierarchy and subtract 1
- Identify the sub-department heads
  - Exclude any employees in the “Executives” department
  - Exclude any employees with “Administrator” in their title
  - Find the person with the 2nd-lowest hierarchy_level within each department – those people are the sub-department heads
- Parse out the dependent_team_ids for the sub-department heads –> those are the sub-department team IDs. Rename the field subdept_team_id.
- Join the sub-departments back to the main employee data
  - An employee is in the sub-department if
    - The employee’s team hierarchy string contains the subdept_team_id
    - OR, the employee’s dependent_team_ids contains the subdept_team_id
- Join the subdept_team_id to the team lookup list, to get the sub-department name. Rename the column subdept_name.
- Make sure that all employees are included in the output, even if they do not have a sub-department (e.g. the CEO). If an employee doesn’t have a sub-department, the sub-department fields should be null.
- Output the data

## Output

- output_01.csv
  - 14 fields:
    - position_id
    - employee_id
    - title
    - department
    - supervisor_id
    - team_id
    - direct_reports
    - team_name
    - team_hierarchy
    - employee_id_hierarchy
    - dependent_team_ids
    - hierarchy_level
    - subdept_team_id
    - subdept_name
