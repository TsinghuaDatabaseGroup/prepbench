## Requirements

- Input the data
- For the Prime Ministers data:
  - Group together Sir Winston Churchill and Winston Churchill
  - Split the dates to create Start Date PM and End Date PM
  - For the null End Date PM, replace with today's date
  - Create a row for every day the Prime Minister was in office
- For the Chelsea Manager data:
  - Remove unnecessary fields and rename remaining fields
  - Clean the Chelsea Managers field
  - For the null End Date CM, replace with today's date
  - Create a row for every day the Chelsea Manager was in place
- For the Chelsea Matches data:
  - Filter to only include the main competitive matches:
    - League
    - League Cup
    - F.A. Cup
    - Europe
  - Make sure the Date is a Date Data Type
  - Pivot the data so we know how many matches were won, drawn or lost on each day
  - Create a Matches field, so we know the number of matches played each day
- Bring the 3 datasets together
- Aggregate so that we are able to count the number of Chelsea Managers for each Prime Minister, as well as how many Matches were played during their time in office and the breakdown of their outcome
- Calculate the Win % for each Prime Minister
  - i.e. Matches Won / Total Matches
  - Rounded to 2 d.p.
- Output the data

## Output

- output_01.csv
  - 9 fields:
    - Prime Ministers
    - Start Date PM
    - End Date PM
    - Chelsea Managers
    - Matches
    - Matches Won
    - Matches Drawn
    - Matches Lost
    - Win %
