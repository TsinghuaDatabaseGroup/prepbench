## Context
Prep Air wants to understand on-board purchasing patterns across a set of flights, using passenger purchases, assigned seats, flight departure timing, and which rows are designated as Business Class (where purchases are free to the passenger). The goal is to combine the provided sources and produce ranked summaries that quantify purchasing by departure time period, by seat position, and the implied cost of free Business Class purchases.

## Requirements
- Input the data.

- Use the following inputs and fields (at minimum) to build a passenger-level dataset:
  - **Passenger List** (`input_01.csv`): `passenger_number`, `flight_number`, `purchase_amount` (names may be present but are not required for the outputs).
  - **Seat List** (`input_02.csv`): `Row` and seat letters `A`–`F`, where each seat-letter column contains the `passenger_number` assigned to that seat for a given row.
  - **Flight Details** (`input_03.csv`): a line-based, bracketed and pipe-delimited format that must be parsed into separate fields including `FlightID`, `DepDate`, and `DepTime` (and any other provided fields).
  - **Plane Details** (`input_04.csv`): flight identifier (column `FlightNo.`) and `Business Class` row range.

- Validate key identifiers needed for joins and aggregation:
  - `passenger_number` and `flight_number` must be numeric and present for a passenger record to be retained.
  - `purchase_amount` must be numeric; treat missing/invalid values as `0`.
  - In the seat mapping, retain only seat assignments with a valid numeric `passenger_number`.

- Assign a label for where each seat is located (derive a field named **Seat Position** from seat letter):
  - A & F → `Window`
  - B & E → `Middle`
  - C & D → `Aisle`

- Reshape the **Seat List** from wide to long so that each record represents one seat assignment with:
  - `Row`
  - `SeatLetter` (A–F)
  - `passenger_number`
  - derived `Seat Position`

- Combine the **Seat List** and **Passenger List** tables:
  - Join on `passenger_number` using a left join from Passenger List to Seat List (retain all valid passengers even if a seat assignment is not found).

- Parse the **Flight Details** so that they are in separate fields:
  - Parse the bracketed, pipe-delimited rows into columns (using the first parsed bracketed row as the header definition).
  - Convert `FlightID` to numeric for joining.
  - Create a departure datetime from `DepDate` + `DepTime` to support time-of-day logic.

- Calculate the time of day for each flight (create **Depart Time of Day** from the departure hour):
  - Morning - Before 12:00 (hour < 12)
  - Afternoon - Between 12:00 - 18:00 (12 ≤ hour ≤ 18)
  - Evening - After 18:00 (hour > 18)

- Join the Flight Details & Plane Details to the Passenger & Seat tables so you can identify what rows are Business or Economy Class for each flight:
  - Join Passenger+Seat to Flight Details on `flight_number` = `FlightID` (left join) to bring in `Depart Time of Day`.
  - In Plane Details, treat `FlightNo.` as the flight identifier; rename it to `FlightID` for consistency and join on `FlightID` (left join).
  - Parse `Business Class` as a row range:
    - If provided as `start-end`, interpret as inclusive bounds.
    - If provided as a single row number, treat start and end as the same row.
  - Create a passenger-level field named **Business Class** with values:
    - `Business Class` if the passenger’s `Row` is within the inclusive range `[bc_start, bc_end]` for that flight.
    - Otherwise `Economy`.

- Answer the following questions by producing the three required ranked outputs:
  1) **What time of day were the most purchases made?**
     - Consider **Economy passengers only**.
     - First compute total Economy `purchase_amount` per flight (`flight_number`).
     - Then compute the mean of these per-flight totals within each `Depart Time of Day`.
     - Round the resulting average to 2 decimal places.
     - Rank results with Rank = 1 for the highest average; break ties by `Depart Time of Day` ascending.

  2) **What seat position had the highest purchase amount?**
     - Consider **Economy passengers only**.
     - Sum `purchase_amount` across all Economy passengers grouped by `Seat Position`.
     - Round totals to 2 decimal places.
     - Rank results with Rank = 1 for the highest total; break ties by `Seat Position` ascending.

  3) **As Business Class purchases are free, how much is this costing us?**
     - Use all passengers (Business Class and Economy).
     - Sum `purchase_amount` grouped by the derived `Business Class` field.
     - Round totals to 2 decimal places.
     - Rank results with Rank = 1 for the highest total; break ties by `Business Class` ascending.
     - Interpret the `Business Class` row’s total as the cost of free purchases.

- Bonus: If you have Tableau Prep 2021.1 or later, you can now output to Excel files. Can you combine all of the outputs into a single Excel workbook, with a different sheet for each output?

- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Rank
    - Depart Time of Day
    - Avg per Flight

- output_02.csv
  - 3 fields:
    - Rank
    - Seat Position
    - Purchase Amount

- output_03.csv
  - 3 fields:
    - Rank
    - Business Class
    - Purchase Amount