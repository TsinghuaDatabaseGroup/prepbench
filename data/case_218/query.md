## Context
Continuing a curiosity: Why is there so much variation in when Easter Sunday falls?
"The simple standard definition of Easter is that it is the first Sunday after the full Moon that occurs on or after the spring equinox. If the full Moon falls on a Sunday then Easter is the next Sunday."
Let's compare our computed Easter dates with the Full Moon dates to see if this is true.
Note: the Historical Full Moon dates only goes back to 1900 rather than 1700. Our analysis for this challenge will be between 1900 and 2023.

## Requirements

- Input the data
- Rename the Full Moon fields
- From the Time field, parse out the interesting info the full moons
  - Blue moon (second full moon within one calendar month)
  - A partial lunar eclipse takes place
  - A total lunar eclipse takes place
- Join with Easter Sunday Dates
  - Make sure we only include the Full Moon just before Easter Sunday
- Calculate the number of days between then Full Moon and Easter Sunday
- Aggregate the data so we can see how many times there has a certain number of days between the Full Moon & Easter Sunday
  - Include fields for the most interesting info related to that number of days between (use Total Lunar Eclipse, then Partial Lunar Eclipse, then Blue moon as the priority order)
  - Include fields for the first and last years for that number of occurrences
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Days Between Full Moon & Easter Sunday
    - Number of Occurrences
    - Most Interesting event
    - Min Year
    - Max Year
