## Context
Chin & Beard Suds Co. wants to estimate how much each team member sells per day, even though sales are only captured at the store/day level. Using store-level daily sales and daily staffing records, estimate each team member’s average daily sales contribution and rank team members within each store so the top sellers can be identified.

## Requirements
- Input the data from:
  - `input_01.csv`: store-level sales by date, where `Date` identifies the day and each other column represents a store’s sales for that date.
  - `input_02.csv`: team member attendance by day, including at minimum `Date`, `Store`, and `Team Member` for each team member who worked that day.
- Reshape the store sales data to a long format so that each row represents one `(Date, Store)` with a single numeric `Store Sales` value.
- Determine how many staff work in each store each day:
  - Group the team-member attendance records by `(Date, Store)` and compute the staff count for that store on that date.
- Join Store Sales and Team Member Days:
  - Join the long-format store sales to the daily staff counts on `(Date, Store)` using an inner join (retain only `(Date, Store)` combinations present in both sources).
- Estimate the Staff Sales per Day:
  - For each `(Date, Store)`, compute the estimated sales per staff member for that day as:  
    `Est per Staff per Day = Store Sales / Staff Count`.
- Attribute the daily estimated per-staff sales to each team member day:
  - Join the team-member attendance records to the per-day estimate on `(Date, Store)` using an inner join so each team-member-day row receives the corresponding `Est per Staff per Day`.
- Estimate each team member’s overall sales level:
  - Aggregate to one row per `(Store, Team Member)` by taking the mean of `Est per Staff per Day` across all days that team member worked in that store.
  - Round the resulting estimate to 2 decimal places to produce `Estimate Sales per Staff Member`.
- Determine the team member's rank within their store:
  - Rank team members within each `Store` by `Estimate Sales per Staff Member` in descending order (highest value gets rank 1).
  - Use dense ranking so ties share the same rank and the next rank increments by 1 (e.g., 1, 2, 2, 3).
- Output the data:
  - Produce the required fields only.
  - Order rows for a stable output by sorting by `Store` (ascending), then `Rank` (ascending), then `Team Member` (ascending).

## Output

- output_01.csv
  - 4 fields:
    - Estimate Sales per Staff Member
    - Store
    - Team Member
    - Rank