## Context
This challenge aims to identify seats not chosen by customers on planes. The input includes seat allocation data (split into Flow Card and Non-Flow Card holders) and a seating plan for the planes. The goal is to return seats that have not been booked.

## Requirements

- Input the data
- Union the Flow Card and Non-Flow card data sets together
- Create a data field to show whether the seat was booked by someone with the Flow Card or not (call this field 'Flow Card?')
- Aggregate the Seat Bookings to count how many bookings there are for:
  - Each Seat
  - In each Row
  - In each Class
  - For Flow and Non-Flow Card holders
- Join on the Seating Plan data to ensure you have a data set for every seat on the plane, even if it hasn't been booked (Only return the records for the seats that haven't been booked)
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Class
    - Seat
    - Row
