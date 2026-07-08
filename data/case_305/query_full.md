## Context

You are given a web-scraped dataset of *Strictly Come Dancing* performances and scores by series and couple. The goal is to measure how each finalist’s scoring changed from their first scored dance of the series to their performances in the final, and to output one summary row per finalist couple with their finalist placing and percentage change in average judge score.

## Requirements

- Input the data from `input_01.csv`.

- Remove repeated table header rows introduced by imperfect webscraping. Treat a row as a repeated header and exclude it if either:
  - `Couple` equals the literal string `Couple`, or
  - `Scores` equals the literal string `Scores`.

- Ensure the Week field is numeric for week-based selection:
  - Derive a numeric week number from `Week` by extracting the integer from the pattern “Week <number>”.
  - Store this numeric value for subsequent “first dance” logic.

- Process the `Scores` field (composed of a total score and per-judge scores) to create score metrics:
  - Create `Total Score` by extracting the leading numeric total from `Scores`.
  - Count the number of judges as the count of numeric entries inside the parentheses in `Scores`.
  - Create `Avg Judge's Score` = `Total Score` ÷ `Number of Judges`.
  - Exclude rows where an average judge score cannot be computed (i.e., total score and/or judge count is missing or not parseable), so that only scored dances remain.

- Identify final-week rows:
  - A row is considered part of the final if `Week` contains the standalone word “Final”.
  - Exclude weeks that are explicitly “Semi-final/Semifinal” or “Quarter-final/Quarterfinal” from being treated as the final.

- Derive each couple’s “first dance” score within a series:
  - Work at the grain of `Series` + `Couple`.
  - Among scored rows with a numeric week number, find the minimum (earliest) week number per `Series` + `Couple`.
  - If the couple has multiple scored dances in that earliest week, define their first-dance score as the mean of `Avg Judge's Score` across those dances.

- Derive each couple’s final score within a series (finalists only):
  - Consider only scored rows identified as final-week rows.
  - For each `Series` + `Couple`, compute the couple’s final average judge score across all their final dances using a judge-count-weighted approach:
    - Final Avg Judge’s Score = (sum of `Total Score` across the couple’s final dances) ÷ (sum of `Number of Judges` across the couple’s final dances).
  - Determine the couple’s finalist placing from `Result` (based on whether it indicates winner, runner-up, or third place), and keep only couples with a determined finalist placing. This implicitly restricts the output to couples who made it to the final.

- Combine first-dance and final metrics:
  - Keep one row per `Series` + `Couple` for finalist couples.
  - Compute percentage change as:
    - `% Change` = (Final Avg Judge’s Score − First-dance Avg Judge’s Score) ÷ (First-dance Avg Judge’s Score).

- Apply a series inclusion rule:
  - Ensure `Series` is numeric and retain only rows where `Series` is between 1 and 21 inclusive.

- Output the data as specified.

## Output

- output_01.csv
  - 5 fields:
    - Series
    - Couple
    - Finalist Positions
    - Avg Judge's Score
    - % Change