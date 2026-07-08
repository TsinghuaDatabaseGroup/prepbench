## Requirements

- Input the data
- Extract the information for which toys belong to which list
- Update the Quota to represent the number of toys needed
  - e.g. Barbie's dream house Quota should be 40% of 200M
- Match the Elves' Initials to their Names
  - e.g. CA = Blinky Sparkles
- It's the Production Manager who is responsible for the number of toys produced so we only need to keep information about them, so Santa knows who to share the dashboard with
- Reshape the data so we have a Date field
  - Make sure the data type matches
- For the first output, Santa wants to find out in which week certain toys exceed their Quota. You'll need to create a Running Sum of Toys Produced, as well as a field highlighting whether a toy is Over or Under Quota
- Output this dataset
- For the second output, wants to see some top level figures for the year. How will the Quotas need to be adjusted for the Over/Under Production?
  - Aggregate the data to the Toy level of detail
  - Calculate how much each Toy is Over or Under its Quota
  - Check at the list level whether there are enough Toys for the Number of Children on that list
  - So that Santa doesn't take too many Toys on his sleigh, the Toys with the most overproduction for each list should be the ones translated into spares (if there are more toys than children on the list)
- Output the data

## Output

- output_01.csv
  - 9 fields:
    - List
    - Number of Children
    - Toy
    - Production Manager
    - Quota
    - Week
    - Toys Produced
    - Running Sum of Toys Produced
    - Over or Under Quota?

- output_02.csv
  - 7 fields:
    - List
    - Toy
    - Quota
    - Toys Produced
    - Toys Ready to be Gifts
    - Spare Toys
    - Toys Over/Under Quota
