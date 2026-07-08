## Context
Prep Air want to do some analysis of flight delays to and from its key destinations. After many discussions with the airport, they finally agreed to share this data. However, it's not in the best structure, so we'll definitely need to do some prep before our analysis can begin. We have 2 inputs this week: Information on the delayed flights, separated across multiple lines; Aggregated view of flights which were not delayed.

## Requirements

- Input the data
- Aggregate the data so that you have 1 row per flight delay, instead of the current 3 rows
- Make sure all Airport codes are valid. Group those which are not.
- Calculate the total delay and number of delayed flights for each Airport, for each journey type
- Combine with information on flights which were not delayed
- Calculate the average delay and % of flights which were delayed for each Airport, for each journey type
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Airport
    - Type
    - % Flights Delayed
    - Avg Delay (mins)
