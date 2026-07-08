## Requirements

- Input the data
- Reshape the Orders table so that we have 3 columns:
  - Guest name
  - Dish
  - Selections (containing 🗸 or null)
- Extract the course name from the Dish field
  - Group these so that Starter and Starters are treated the same, for example
- Fill down the course name for each Guest
  - It may help to bring in the Recipe ID from the Lookup Table
  - Where the Dish contains the Course name, it may be helpful to replace the Recipe ID in the following way:
    - Starters = 1
    - Mains = 2
    - Dessert = 3
- Filter out where the Dish = Course
- Filter out Dishes which have not been selected
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Guest
    - Course
    - Recipe ID
    - Dish
