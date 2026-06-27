## Context
Prep Air needs three related outputs for 2024 that rely on joins and calculated fields:
1) Customer details for flights that have been booked (including each flight’s origin and destination).
2) Flights in 2024 that have not yet been booked, with a fixed “as of” date.
3) Customers who have not booked any flight in 2024, including a “days since last flown” metric and a customer-category banding.

The datasets are large, so the workflow should only join tables when required for each output.

## Requirements
- Input the data.
- Treat “today” / the comparison date as a fixed date of **31/01/2024** for all calculations and datestamps in this task.
- Parse the relevant date fields as dates so that year-based filtering and date arithmetic can be performed.

### Common 2024 filtering
- Restrict flights to those with a flight **Date in calendar year 2024**.
- Restrict bookings to those with a booking **Date in calendar year 2024**.

### Output 1 — Customer details for booked 2024 flights (with route)
- Build a dataset at the grain of **one row per booking in 2024**.
- Join the **2024 bookings** to **customers** using an **inner join on `Customer ID`** so that only bookings with a matching customer are kept.
- Join the result to the **2024 flights** using an **inner join on (`Date`, `Flight Number`)** so that only bookings with a matching flight (in 2024) are kept and the flight route can be included.
- Select exactly the fields listed for `output_01.csv` in the Output section.
- Output the data (this corresponds to writing to a new sheet in a single workbook in the original business request; for this task, write the specified CSV output).

### Output 2 — 2024 flights not yet booked (as of 31/01/2024)
- Build a dataset at the grain of **one row per flight (Date + Flight Number) in 2024 that has zero bookings in 2024**.
- Identify the set of booked flight keys in 2024 using the combination **(`Date`, `Flight Number`)** (deduplicate bookings to keys before comparing).
- From the **2024 flights** list, keep only those flights whose (`Date`, `Flight Number`) do **not** appear among the booked keys for 2024 (i.e., a left-anti join or equivalent “not matched” filter).
- Add a datestamp field named **`Flights unbooked as of`** with the value **`2024-01-31`**.
- Select exactly the fields listed for `output_02.csv` in the Output section.
- Output the data (the “Append to Table” note applies to the original Excel-workbook framing; for this task, write the specified CSV output).

### Output 3 — Customers who have not booked in 2024, with recency banding
- Build a dataset at the grain of **one row per customer**.
- Identify customers who have **not** booked any flight in 2024 by excluding any customer whose `Customer ID` appears in the **2024 bookings** table.
- Compute **`Days Since Last Flown`** as the number of days between **2024-01-31** and the customer’s `Last Date Flown`:
  - `Days Since Last Flown = (2024-01-31 - Last Date Flown) in days`
  - If `Last Date Flown` is missing/invalid such that the day difference cannot be computed, set `Days Since Last Flown` to **-1**.
- Categorize each remaining customer into `Customer Category` using `Days Since Last Flown` with these exact thresholds:
  - If `Days Since Last Flown` is **greater than 270**: `Lapsed (over 9 months since last flight)`
  - Else if **greater than 180**: `Been away a while (6-9 months since last flight)`
  - Else if **greater than 90**: `Taking a break (3-6 months since last flight)`
  - Else (including -1): `Recent Fliers (less than 3 months since last flight)`
- Select exactly the fields listed for `output_03.csv` in the Output section.
- Output the data.

### Output formatting and determinism
- Output date fields as `YYYY-MM-DD` text in the final extracts where applicable (e.g., `Date`, `Last Date Flown`, and the datestamp field). Treat these as exact text outputs in the final files.
- Ensure each output is produced in a consistent, deterministic row order:
  - `output_01.csv`: sort by `Date`, then `Customer ID`, then `Flight Number`, then `Ticket Price` (ascending).
  - `output_02.csv`: sort by `Date`, then `Flight Number`, then `From`, then `To` (ascending).
  - `output_03.csv`: sort by `Customer ID`, then `Last Date Flown` (ascending).

## Output

- output_01.csv
  - 11 fields:
    - Date
    - From
    - To
    - Flight Number
    - Customer ID
    - Last Date Flown
    - first_name
    - last_name
    - email
    - gender
    - Ticket Price

- output_02.csv
  - 5 fields:
    - Flights unbooked as of
    - Date
    - Flight Number
    - From
    - To

- output_03.csv
  - 8 fields:
    - Customer ID
    - Customer Category
    - Days Since Last Flown
    - Last Date Flown
    - first_name
    - last_name
    - email
    - gender
