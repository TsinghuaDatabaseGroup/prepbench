## Context

Ho ho ho, Merry Christmas everyone. Well not for some people! Some people have ended up on Santa's Naughty list but Santa needs to understand how much time he has allocated of his Elves to building presents that will ultimately not be delivered. Can you help Santa match who is on the Nice and Naughty List so he can deliver the correct presents to those who deserve them?

## Requirements

- Input the data
- Input all three tables in the Spreadsheet
- Pull together the Naughty and Nice list but make sure you understand who should be on each
- Parse the address to match Santa's list to the Naughty/Nice list
- Only return one row per recipient in Santa List (both Naughty and Nice)
  - Who's missing off both lists?
- Also, aggregate the nice and naughty list to understand how many hours have been allocated to building both types of presents
  - Santa only does his time planning on whole hours so make sure you round up
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - List
    - Name
    - Item
    - Family Role
    - Elves Build Time (min)
    - Address-1
    - Reason

- output_02.csv
  - 2 fields:
    - Total Hours Build Time
    - List
