## Context

The HRIS tracks employee departments, but sub-department information is needed for reporting. Sub-departments are inferred from the organizational hierarchy based on identifying sub-department heads.

## Requirements

- Input employee data from `input_01.csv` and team lookup data from `input_02.csv`.
- Calculate each employee's `hierarchy_level`:
  - Count the number of pipe characters (`|`) in `employee_id_hierarchy` and subtract 1.
- Identify sub-department heads:
  - Exclude employees in the "Executives" department.
  - Exclude employees with "Administrator" in their title.
  - Among remaining employees in each department, find those at the 2nd-lowest hierarchy level (using dense ranking).
- Extract `subdept_team_id` from sub-department heads:
  - Parse `dependent_team_ids` and take the second pipe-delimited segment (index 1).
- Assign employees to sub-departments:
  - An employee belongs to a sub-department if their `team_hierarchy` string contains the `subdept_team_id`, OR their `dependent_team_ids` string contains the `subdept_team_id`.
  - When checking multiple sub-department IDs for a department, assign the first matching one.
- Join with the team lookup table on `subdept_team_id = team_id` to get `subdept_name`.
- All employees must appear in the output; employees without a sub-department have null values for sub-department fields.
- Output 14 columns: `position_id`, `employee_id`, `title`, `department`, `supervisor_id`, `team_id`, `direct_reports`, `team_name`, `team_hierarchy`, `employee_id_hierarchy`, `dependent_team_ids`, `hierarchy_level`, `subdept_team_id`, `subdept_name`.

## Output

- output_01.csv
  - 14 fields:
    - Field1
    - Field2
    - Field3
    - Field4
    - Field5
    - Field6
    - Field7
    - Field8
    - Field9
    - Field10
    - Field11
    - Field12
    - Field13
    - Field14
