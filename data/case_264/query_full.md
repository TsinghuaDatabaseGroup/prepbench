## Context

You are preparing an “air capacity over time” dataset that combines customer booking actions with flight capacity information. The goal is to (1) exclude customers who cancelled a given flight, (2) retain only each customer’s latest action per flight, (3) compute a cumulative seat count over time per flight and class using a deterministic ordering, and (4) merge in flight details so capacity utilization can be calculated, including explicit zero-booking rows for flight/class combinations with no bookings.

## Requirements

- Input the data.
  - Use the customer actions file as the source for customer events (including Flight Number, Class, Customer ID, Action, Date, Row, Seat).
  - Use the flight details file as the source for Flight Date and Capacity by Flight Number and Class.

- If the customer has cancelled their flight, make sure all rows are filtered out for that flight.
  - Apply this at the level of `(Flight Number, Customer ID)`: if any record for that customer on that flight has `Action = "Cancelled"`, remove **all** records for that `(Flight Number, Customer ID)` combination.

- For each customer on a flight, filter the dataset to their most recent action.
  - Determine the most recent action date per `(Flight Number, Customer ID)` using the `Date` field.
  - Keep only rows whose `Date` equals that most recent date for the corresponding `(Flight Number, Customer ID)` (if multiple rows share the most recent date, keep them).

- Based on the Date field, create a field which shows how many seats in total have been booked as of that date for each flight and class (Hint: Running Sum could be useful here!)
  - After applying the cancellation filter and “most recent action” filter, compute `Total Seats booked over time` as a running total within each `(Flight Number, Class)` group, treating each remaining row as 1 booked seat.
  - **Sorting Rule for Running Sum**: When calculating the running sum, sort records by Date (ascending). For records on the same date within the same Flight Number and Class, sort by: (1) Row (ascending), (2) Seat (ascending), (3) Customer ID (ascending). This provides a stable, deterministic ordering that can be reproduced consistently.

- Bring in information about the Flight Details.
  - Join flight details to the action-based results on `(Flight Number, Class)` so every flight/class combination from the flight details is present in the final output.
  - Carry through `Flight Date` and `Capacity` from flight details.

- Calculate the Capacity %: of the available seats on the flight for each class, what percentage have been booked so far
  - Compute `Capacity %` as:  
    `Capacity % = (Total Seats booked over time) / Capacity`
  - For classes which are yet to be booked for a flight, ensure the Capacity % shows as 0% for these rows.
    - For flight/class combinations with no matching action rows, set `Total Seats booked over time` to `0`, which results in `Capacity % = 0`.
  - The Date for these rows should be today's date (28/02/2024).
    - For flight/class combinations with no matching action rows, set `Date` to `28/02/2024`.
  - Format both `Flight Date` and `Date` as `DD/MM/YYYY` in the output.

- Output the data.

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