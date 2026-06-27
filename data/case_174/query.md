## Requirements

- Input the data
- For the Opportunity table:
  - Pivot the CreatedDate & CloseDate fields so that we have a row for when each opportunity Opened and a row for the ExpectedCloseDate of each opportunity
  - Rename the Pivot 1 Values field to Date
  - Rename the Pivot 1 Names field to Stage and update the values
  - Update the Stage field so that if the opportunity has closed (see the StageName field) the ExpectedCloseDate is updated with the StageName
  - Remove unnecessary fields
    - Hint: look at the fields in common with the Opportunity History table
- Bring in the additional information from the Opportunity History table about when each opportunity moved between each stage
- Ensure each row has a SortOrder associated with it
  - Opened rows should have a SortOrder of 0
  - ExpectedCloseDate rows should have a SortOrder of 11
- Remove unnecessary fields
- Remove duplicate rows that may have occurred when brining together the two tables
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - OppID
    - Date
    - Stage
    - SortOrder
