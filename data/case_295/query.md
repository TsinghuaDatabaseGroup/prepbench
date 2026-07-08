## Context
- Each vehicle listed is classed as a different registration number.

## Requirements
- Input the data
- Break the Users data set into individual records (you should have 365 rows)
- The User data is formed from:
  - 1st 7 characters is the User ID
  - The last letter signifies whether the user is a private individual ('P') or Dealership (D)
  - The 3 characters after the User ID for Dealerships is the Dealership ID
- With the Ads data, remove any unsold vehicles
- Join the data sets together
- Find when an advert is first posted
- Only keep the records where advert was first posted
- Find the time between when a vehicle is first advertised on the site to when the vehicle was sold
- Find the average days for each sale a dealership has listed (group up to the nearest whole day)
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Dealership ID
    - Dealership Avg Days to Sell
