## Context

Our input is very wide this week, with 136 fields and only 28 rows. It covers tourism in the Maldives from 2010 to 2020.

## Requirements

- Input the data
- Pivot all of the month fields into a single column
- Rename the fields and ensure that each field has the correct data type
- Filter out the nulls
- Filter our dataset so our Values are referring to Number of Tourists
- Our goal now is to remove all totals and subtotals from our dataset so that only the lowest level of granularity remains. Currently we have Total > Continents > Countries, but we don't have data for all countries in a continent, so it's not as simple as just filtering out the totals and subtotals. Plus in our Continents level of detail, we also have The Middle East and UN passport holders as categories. If you feel confident in your prep skills, this (plus the output) should be enough information to go on, but otherwise read on for a breakdown of the steps we need to take:
  - Filter out Total tourist arrivals
  - Split our workflow into 2 streams: Continents and Countries
    - Hint: the hierarchy field will be useful here
  - Split out the Continent and Country names from the relevant fields
  - Aggregate our Country stream to the Continent level
  - Join the two streams together and work out how many tourists arrivals there are that we don't know the country of
  - Add in a Country field with the value "Unknown"
  - Union this back to here we had our Country breakdown
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Breakdown
    - Number of Tourists
    - Month
    - Country
  - Month must be output as exact text in DD/MM/YYYY format.
