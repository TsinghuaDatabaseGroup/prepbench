## Context

You are preparing hospital-stay costing outputs for a set of customers (patients). The goal is to construct a complete day-by-day view of each patient’s stay (including every inpatient day), apply a tiered daily pricing model, and then produce two aggregated views: one summarised per person and one summarised per calendar date.

## Requirements

- Input the data.
  - Use `input_01.csv` as the patient-level table. It must include at least:
    - `Name` (patient identifier),
    - `First Visit` (the start date of the stay; treat as a date),
    - `Length of Stay` (number of inpatient days).
  - Use `input_02.csv` as the day “scaffold” table. It must include a numeric column `Value` representing candidate day indices.

- Use the various input sheets/files to build a view of individual cost per day per patient by expanding each patient into one row per day of stay.
  - Build the scaffold by taking rows from `input_02.csv` where `Value >= 1`, and treat `Value` as `DayIndex` (day number within the stay, starting at 1).
  - Create a full daily dataset by cross joining every patient from `input_01.csv` to every scaffold `DayIndex`, then keep only rows where `DayIndex <= Length of Stay`.
  - Define the daily calendar date for each expanded row as:
    - `Date = First Visit + (DayIndex - 1)` days.

- To determine cost, apply the tiered pricing per inpatient day based on `DayIndex`:
  - If `DayIndex` is 1–3 (inclusive): daily cost is £100.
  - If `DayIndex` is 4–7 (inclusive): daily cost is £80.
  - If `DayIndex` is 8 or greater: daily cost is £75.
  - Store this as `Cost per Day` on the daily dataset.

- Aggregate the expanded daily dataset to form a view of total cost and average cost.
  - Per-date aggregation (for `output_02.csv`):
    - Group by `Date`.
    - `Cost per Day` = sum of daily costs across all patients on that date.
    - `Number of Patients` = count of distinct `Name` values present on that date.
    - `Avg Cost per Day` = `Cost per Day / Number of Patients`, rounded to 2 decimal places.
    - Format `Date` as a string in `dd/mm/YYYY`.
  - Per-person aggregation (for `output_01.csv`):
    - Group by `Name`.
    - `Cost` = sum of `Cost per Day` across all days in that person’s stay.
    - `Days` = maximum `DayIndex` for that person (i.e., the total number of days included for them after expansion).
    - `Avg Cost per Day per person` = `Cost / Days`, rounded to 2 decimal places.

- Output the data as two CSV files with exactly the required fields and field names.

## Output

- output_01.csv
  - 3 fields:
    - Cost
    - Name
    - Avg Cost per Day per person

- output_02.csv
  - 4 fields:
    - Avg Cost per Day
    - Date
    - Cost per Day
    - Number of Patients