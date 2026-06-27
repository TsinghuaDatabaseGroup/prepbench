## Requirements

- Input the data
- Input each of the 12 monthly files
- Create a 'file date' using the month found in the file name
  - The Null value should be replaced as 1
- Clean the Market Cap value to ensure it is the true value as 'Market Capitalisation'
  - Remove any rows with 'n/a'
- Categorise the Purchase Price into groupings
  - 0 to 24,999.99 as 'Small'
  - 25,000 to 49,999.99 as 'Medium'
  - 50,000 to 74,999.99 as 'Large'
  - 75,000 and above as 'Very Large'
- Categorise the Market Cap into groupings
  - Below $100M as 'Small'
  - Between $100M and below $1B as 'Medium'
  - Between $1B and below $100B as 'Large'
  - $100B and above as 'Huge'
- Rank the highest5 purchases per combination of: file date, Purchase Price Categorisation and Market Capitalisation Categorisation.
- Output only records with a rank of1 to5
- Output the data

## Output

- output_01.csv
  - 10 fields:
    - Market Capitalisation Categorisation
    - Purchase Price Categorisation
    - File Date
    - Ticker
    - Sector
    - Market
    - Stock Name
    - Market Capitalisation
    - Purchase Price
    - Rank
