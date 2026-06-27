## Context
Chin & Beard Suds Co wants a repeatable way to assess whether its website pages are being viewed across the right mix of devices, operating systems, browsers, and user origins. The goal is to standardize the preparation of monthly vs. all-time pageview summaries so the same analysis can be rerun whenever new extracts are available.

## Requirements
- Input the data.
  - Use six input CSV files representing three dimensions (Browser, Operating System, Origin), each with an “all time” extract and a “this month” extract:
    - Browser: all time (input_01.csv) and this month (input_02.csv)
    - Origin: this month (input_03.csv) and all time (input_04.csv)
    - Operating System: all time (input_05.csv) and this month (input_06.csv)
  - Each input contains an `Entry` field (the dimension member name) and a `Pageviews` field.

- Create a single table for each of Origin, Operating System and Browser.
  - For each dimension, produce one output table that combines “this month” and “all time” metrics into the same row per dimension member.
  - Join logic (all three dimensions):
    - Perform a full outer join between the “this month” and “all time” tables using the dimension member name as the key (`Browser`, `Operating System`, or `Origin`).
    - Keep members that appear in only one of the two periods; their missing period fields remain null.

- Clean up values and percentages.
  - For Browser and Operating System inputs, interpret `Pageviews` as containing both:
    - a numeric pageview count, and
    - a percent of total in parentheses.
  - Convert any `< 1%` values to `0.5` for the percent-of-total.
  - Split the combined `Pageviews` field into:
    - a numeric “Value” (pageview count), and
    - a numeric “Percent” (percent of total, with `<1%` mapped to `0.5`).

- If percent of total fields don't exist in any files, create these and make them an integer.
  - For Origin inputs, treat `Pageviews` as numeric counts only and compute an integer percent-of-total field.
  - Percent calculation rule for Origin (applied separately to “this month” and “all time”):
    - Compute each member’s share as `(member_value / total_value) * 100`.
    - Take the floor of each share to get a base integer percent.
    - If the sum of floored percents is less than `94`, allocate +1 to as many rows as needed (until the percent sum reaches exactly `94`), choosing rows in descending order of fractional remainder; break ties by preserving original input order.
    - The resulting `Percent` must be an integer for every Origin row.

- Derive the change metrics.
  - Browser: `Change in % this month = (This Month Pageviews %) - (All Time Pageviews %)`
  - Operating System: `Change in % this month = (This Month Pageviews %) - (All Time Pageviews %)`
  - Origin: `Change in % pageviews = (This Month Pageviews %) - (All Time Views %)`

- Preserve a deterministic row order in each output table.
  - Primary ordering: keep the original “this month” input order first.
  - Secondary ordering: for rows not present in “this month”, place them after those rows and order them by the original “all time” input order.

- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Change in % this month
    - Browser
    - This Month Pageviews Value
    - This Month Pageviews %
    - All Time Pageviews Value
    - All Time Pageviews %

- output_02.csv
  - 6 fields:
    - Change in % this month
    - Operating System
    - This Month Pageviews Value
    - This Month Pageviews %
    - All Time Pageviews Value
    - All Time Pageviews %

- output_03.csv
  - 6 fields:
    - Change in % pageviews
    - This Month Pageviews %
    - All Time Views %
    - Origin
    - All Time Pageviews
    - This Month Pageviews