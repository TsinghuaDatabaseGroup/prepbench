## Context
Have you ever been given a datasource to work with which has already been lovingly "cleaned" and turned into a pivot table? Whilst that's very kind of the provider, it's not exactly ideal for Tableau Desktop! Let's work to un-pivot such a table from a stakeholder at AllChains!

## Requirements

- Input the data
- Dynamically rename the fields so that there is a common separator between the Bike Type, Date and Measure Name
- Pivot the data
- Split out the Bike Type, Date and Measure Name
- Create a field for Sales and Profit
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Bike Type
    - Region
    - Month
    - Sales
    - Profit
