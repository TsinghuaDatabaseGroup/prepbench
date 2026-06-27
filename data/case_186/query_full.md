## Context
The CEO now wants a year-over-year summary of overall Spin Class performance (beyond individual rides). Because the cycling equipment does not capture speed, estimate distance using a configurable average riding speed (in KPH) and summarize key metrics for 2021 and 2022.

## Requirements
- Input the data.
- Interpret the ride-duration field as minutes:
  - Convert the numeric value field to a numeric type and use it as `Minutes` (i.e., treat the provided values as minutes for each ride).
  - **Data filtering for Units field**: Only process rows where the `Units` field equals `min`. Exclude any rows where `Units` has a different value (e.g., `km`, `hr`, etc.) from all calculations. This ensures that only spin class rides with duration measured in minutes are included in the analysis.
- Split the unnamed metadata column (the rightmost column in the input) into three fields using the delimiter ` - `:
  - `Coach`
  - `Calories`
  - `Music Type`
  - Treat `Calories` as an integer.
- Convert the `Date` field to `Year` (4-digit year).
- Restrict all calculations to rides in years **2021** and **2022** only.
- Exclude rides with non-positive minutes from calculations that use minutes or “per minute” logic (so that per-minute measures are well-defined). The yearly totals and averages should be computed on the same filtered set of rides.
- Create a speed input (average riding speed in KPH) used to estimate distance:
  - Use **30 KPH** as the speed value for the produced output.
  - Total distance must be computed using this speed, and values may change if a different speed is chosen.
- Compute the following measures **separately for each year (2021 and 2022)**, where one input row represents one ride:
  - **Total Mins**: sum of `Minutes`.
  - **Total Rides**: count of rides (rows).
  - **Avg. Calories per Ride**: average of `Calories` across rides.
  - **Total Distance**: `(Total Mins / 60) * Speed`.
  - **Avg. Calories per Minute**: for each ride compute `Calories per Minute = Calories / Minutes`, then take the average of this per-ride value (do not compute as total calories divided by total minutes).
  - **Total Mins per Coach**: for each coach, sum `Minutes` across rides in the year; select the coach with the maximum summed minutes. If there is a tie, choose the coach whose name sorts alphabetically first. Format the value as `Coach (minutes)` where `minutes` is an integer.
  - **Calories per Minute per Coach**: for each coach, compute the average of per-ride `Calories per Minute` within the year; select the coach with the maximum coach-average value. If there is a tie, choose the coach whose name sorts alphabetically first. Format the value as `Coach (value)` where `value` is rounded to 1 decimal place and displayed without unnecessary trailing zeros.
- Combine all measures into a single output table structured as:
  - One row per measure (using the exact measure names listed above).
  - Separate columns for 2022 and 2021 values.
  - If a measure is unavailable for a year, leave the corresponding cell blank.
- Format output values as strings:
  - `Total Mins` and `Total Rides` as whole numbers (no decimals).
  - All other numeric measures rounded to 1 decimal place, then display without unnecessary trailing zeros and without a trailing decimal point (e.g., display `420.3` not `420.30` or `420.30000000001`, and display `1140` not `1140.0`).
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Measure
    - 2022
    - 2021