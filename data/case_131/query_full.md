## Context

You need to reproduce Excel-style conditional aggregations (SUMIFS and AVERAGEIFS) for flight ticket sales. The goal is to create per-flight, per-class totals and average daily sales, split into two time windows based on how many days before departure the sale occurred.

## Requirements

- Input the data from `input_01.csv`.
- Ensure the fields used for date arithmetic are treated as dates:
  - Parse `Date` and `Date of Flight` as day/month/year dates so that day differences are computed correctly.
- Form the flight identifier:
  - Create `Flight` as `Departure + " to " + Destination`.
- Work out how many days between the sale and the flight departing:
  - Compute `days_until = (Date of Flight - Date)` measured in whole days.
- Classify each record’s ticket sales into one of two buckets based on `days_until`:
  - “Less than 7 days before departure” when `days_until < 7`
  - “7 or more days before departure” when `days_until >= 7`
- Mimic SUMIFS and AVERAGEIFS by aggregating `Ticket Sales` within each `(Flight, Class)` for each bucket:
  - For each `(Flight, Class, bucket)`, compute:
    - Total sales = sum of `Ticket Sales`
    - Average daily sales = mean of `Ticket Sales`
  - Reshape the results so the final output has one row per `(Flight, Class)` and separate columns for the two buckets.
  - If a `(Flight, Class)` has no records in a given bucket, the corresponding sum and average outputs for that bucket must be `0` (so all required output columns exist for every row).
- Round all output measure fields to zero decimal places and output them as whole numbers.
- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Flight
    - Class
    - Avg. daily sales 7 days or more until the flight
    - Avg. daily sales less than 7 days until the flight
    - Sales less than 7 days until the flight
    - Sales 7 days or more until the flight