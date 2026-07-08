## Context
To determine whether each person is on the naughty or nice list, follow these rules:
- If a name is only on the nice or naughty list, then that's what list they are part of.
- If a name is on both the naughty and nice list, the number of times they feature on each list will determine whether they are naughty or nice (whichever list has the most mentions determines the end result).
- If there is an even split between naughty and nice mentions, the latest mention will determine which list the person will end up on.

## Requirements
- Input the data
- Split the File Paths to determine which list each record is on
- Create an Index field combining the File Path number and id (id 7 from Naughty 1 file should create an id of 1007)
- Create a count of how many naughty listings and nice listings each name has
- Determine what list each person should be on
  - If the listings are tied, find the latest listing for those people as that will determine which listing they are on
- Remove any unnecessary fields and create one row per person (leaves Name and 'Naughty or Nice' field)
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Naughty or Nice
    - Name
