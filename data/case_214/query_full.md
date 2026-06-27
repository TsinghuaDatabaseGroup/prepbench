## Context
Data Source Bank wants an analysis that links each customer to the closest bank branch based on geographic coordinates. Because the workflow must be done without native spatial functions, compute great-circle distance in miles using the trigonometric (acos) form of the Haversine-style formula, after converting latitude/longitude from decimal degrees to radians. The result will identify the nearest branch for every customer and then prioritise customers for each branch based on proximity.

## Requirements
- Input the data from:
  - `input_01.csv`: branch locations, including `Branch`, `Branch Long`, `Branch Lat`.
  - `input_02.csv`: customer locations, including `Customer`, `Address Long`, `Address Lat`.
- Append the Branch information to the Customer information by generating all Customer–Branch combinations (i.e., evaluate each customer against every branch) so distances can be computed for every pair.
- Transform the latitude and longitude values from decimal degrees to radians for both customers and branches using:
  - `radians = degrees * π / 180`
- For each Customer–Branch pair, calculate the distance in miles using:
  - `DistanceRaw = 3963 * acos((sin(lat1) * sin(lat2)) + cos(lat1) * cos(lat2) * cos(long2 – long1))`
  - where `(lat1, long1)` are the customer coordinates in radians and `(lat2, long2)` are the branch coordinates in radians.
  - Ensure the argument passed to `acos` is constrained to the range `[-1, 1]` to avoid invalid values from floating-point effects.
- Find the closest Branch for each Customer:
  - Select the branch with the smallest `DistanceRaw` for that customer.
  - If there is an exact tie on `DistanceRaw`, choose the tied branch that appears first in the branch input’s order after the Customer–Branch combinations are generated.
  - Create `Distance` as `DistanceRaw` rounded to 2 decimal places.
- For each Branch, assign a Customer Priority rating:
  - Within each branch, order customers by ascending `Distance`.
  - Break ties by ascending `Customer`.
  - Assign `Customer Priority` as a 1-based rank in that ordered list (closest customer = 1).
- Output the data as a single table with one row per customer (mapped to their nearest branch), and sort the final output by:
  - `Branch Long` ascending, then
  - `Customer Priority` ascending.

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