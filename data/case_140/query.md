## Requirements

- Input the data
- Rename the penultimate column from *P 1* (as it appears in Prep) to *Pts*
- Exclude null rows
- Create a *Special Circumstances* field with the following categories
  - Incomplete (for the most recent season)
  - Abandoned due to WW2 (for the 1939 season)
  - N/A for full seasons
- Ensure the *POS* field only has values for full seasons
- Extract the numeric values from the leagues
  - FL-CH should be assigned a value of 0
  - NAT-P should be assigned a value of 5
- Create an *Outcome* field with 3 potential values. (Note: this should apply to all seasons in the data order regardless of any gaps. The current season will have a null value)
  - Promoted, where they are in a league higher than their current league in the following season
  - Relegated, where they are in a league lower than their current league in the following season
  - Same League, where they do not change leagues between seasons
- Create new rows for seasons that were missed due to WW1 and WW2
- Update the fields with relevant values for these new rows
  - e.g. change their *Special Circumstances* value to WW1/WW2
- Output the data

## Output

- output_01.csv
  - 12 fields:
    - Season
    - Outcome
    - Special Circumstances
    - League
    - P
    - W
    - D
    - L
    - F
    - A
    - Pts
    - POS
