## Requirements

- Input the data
- If the customer has cancelled their flight, make sure all rows are filtered out for that flight
- For each customer on a flight, filter the dataset to their most recent action
- Based on the Date field, create a field which shows how many seats in total have been booked as of that date for each flight and class (Hint: Running Sum could be useful here!)
  - **Sorting Rule for Running Sum**: When calculating the running sum, sort records by Date (ascending). For records on the same date within the same Flight Number and Class, sort by: (1) Row (ascending), (2) Seat (ascending), (3) Customer ID (ascending). This provides a stable, deterministic ordering that can be reproduced consistently.
- Bring in information about the Flight Details
- Calculate the Capacity %: of the available seats on the flight for each class, what percentage have been booked so far
  - For classes which are yet to be booked for a flight, ensure the Capacity % shows as 0% for these rows
  - The Date for these rows should be today's date (28/02/2024)
- Output the data

## Output

- output_01.csv
  - 11 fields:
    - Flight Number
    - Flight Date
    - Class
    - Total Seats booked over time
    - Capacity
    - Capacity %
    - Customer ID
    - Action
    - Date
    - Row
    - Seat
