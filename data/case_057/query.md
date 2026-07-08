## Context

This week at C&B Suds Co we're looking to improve and streamline our soap packaging and delivery process. We want to figure out how we can minimise wasted box space and minimise the number of separate boxes per order - a variant of the knapsack problem! At C&B Suds Co we now use three different sizes of box for our soap orders: A bulk order box which can hold 120 soaps. A large box that can hold 24 soaps. A small box that can hold 6 soaps. For all of our orders we want to minimise the number of boxes we use per order. At the same time, we also want to try and minimise unused space in boxes. We want two outputs: an overview for each order of the number of each box size used; and one that gives the details for each individual box being shipped out.

## Requirements

- Input the data
- For each order, figure out how many boxes of each size will be required.
- Arrange this information so there is a single row per order with different fields for each box size.
- Output the above.
- For each box, figure out how many bars of soap will be in that box.
- Assign each box in each order a unique ID, starting from 1 each in each order.
- The box ID should be ascending from the box with the most soap to the box with the least.
- Output the above as well.
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Order Number
    - Order Size
    - Boxes of 120
    - Boxes of 24
    - Boxes of 6

- output_02.csv
  - 6 fields:
    - Order Number
    - Order Size
    - Box Number
    - Box Size
    - Soaps in Box
    - Last Box Per Box Size
