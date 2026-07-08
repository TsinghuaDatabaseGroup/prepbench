## Context

Whilst reading through some great Tableau blogs over the Holidays, the bosses at Chin & Beard Suds Co. (our fake soap company that might have the worst data in history) stumbled across Ryan Sleeper's post on Financial Statements and decided they needed a nice Profit statement for their board meetings from here on. Sadly our data isn't structured like we would ideally like so your challenge this week is to automate the production of the profit statement.

## Requirements

- Input the data
- Find the profit totals for X items
- Find the profit sub-totals for X.X items
- Add the relevant values to the relevant items by replacing the nulls
- Add the leading spaces:
  - 5 spaces for X.X items
  - 10 spaces for X.X.X items
  - Do not manually rename these there is a function that will help!
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Item
    - Profit
