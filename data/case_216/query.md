## Context
The final challenge of Advanced Month involves working out moving calculations. At the time of writing this challenge they are not natively available in Tableau Prep so am intrigued by the solutions you might come up with. Trying to conduct complex analysis can be a challenge but simplifying the data set can make life much easier for end users. This is the logic we're trying to apply this week.

## Requirements

- Input the data
- Create a Trade Order field showing the order each trade has happened in for each Sector from the File Name and ID as the order of each trade within each monthly file
- Remove all data fields except:
  - Trade Order
  - Sector
  - Purchase Price
- Create a Parameter to allow the user to select the rolling number of trades to be incorporated into the moving average.
  - I've set a default of 3 trades in my moving average/
- Create a data set that records the previous 2 trades (where applicable) as well as that Trade Order record.
- Workout the Rolling Average Purchase Price for each Trade Order in each Sector
- Filter the data for the last 100 trades for each Sector
- Create the Previous Trades field to show the oldest trade (1) through to the latest trade (100).
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Previous Trades
    - Trade Order
    - Sector
    - Rolling Avg. Purchase Price
