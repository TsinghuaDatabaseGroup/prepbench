## Requirements

- Input the data
- Create the Loyalty Points:
  - For every £50 spent they get 1 loyalty point
  - Round Loyalty Points to 1 decimal place
- Create a new field to categorise the Loyalty Points:
  - Points that are greater than or equal to 7 categorise them as "MegaByte"
  - Points that are greater than or equal to 5 (but less than 7) categorise as "Byte"
  - Categorise the remaining as "No Byte"
- Find the sum of customers that qualify for each type of byte category (for females and males separately)
- Pivot so that females and males have their own field
- Calculate the percentage of females and males in each category (round the percentages to 1 decimal place)
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Category
    - Female
    - Male
