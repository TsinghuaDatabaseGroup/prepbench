## Context
Data Source Bank want some quick and dirty analysis. They know where their customers are, they know where their branches are. But they don't know which customers are closest to which branches. Which customers should they be prioritising based on proximity to their branches? Now Tableau Prep doesn't natively contain spatial functions so we'll need to use some fancy Maths! Namely we'll be making use of the Haversine formula. There are 2 steps we'll need to use:
1. Transform the latitude and longitudes from decimal degrees to radians by dividing them by 180/pi (it was Pi Day yesterday after all ;))
2. The distance (in miles) can then be calculated as: 3963 * acos((sin(lat1) * sin(lat2)) + cos(lat1) * cos(lat2) * cos(long2 – long1))

## Requirements

- Input the data
- Append the Branch information to the Customer information
- Transform the latitude and longitude into radians
- Find the closest Branch for each Customer
  - Make sure Distance is rounded to 2 decimal places
- For each Branch, assign a Customer Priority rating, the closest customer having a rating of 1
- Output the data

## Output

- output_01.csv
  - 8 fields:
    - Branch
    - Branch Long
    - Branch Lat
    - Distance
    - Customer Priority
    - Customer
    - Address Long
    - Address Lat
