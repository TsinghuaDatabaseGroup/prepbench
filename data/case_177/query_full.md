## Context

You have a listening-history extract that includes a timestamp, an artist name, and the number of milliseconds played per listen. The goal is to convert play time into minutes, compute artist rankings by total listening time overall and by year, and then reshape the results into a single wide table that shows how each top artist’s rank changes from year to year.

## Requirements

- Input the data from `input_01.csv`.
- Create a minutes-played measure from milliseconds:
  - Compute `Mins Played = round(ms_played / (1000 * 60), 2)` (i.e., convert milliseconds to minutes and round to 2 decimal places).
- Extract `Year` from the timestamp field `ts` as the calendar year (e.g., using standard datetime parsing).
- Compute the overall artist ranking:
  - Aggregate to artist level by summing `Mins Played` across all records for each `Artist Name`.
  - Compute `Overall Rank` by ranking artists in descending order of total minutes, using competition ranking with the minimum rank for ties (`rank(method="min", ascending=False)`), and store it as an integer.
  - Keep only `Artist Name` and `Overall Rank` for the overall ranking table.
- Compute yearly artist rankings:
  - Aggregate to artist-year level by summing `Mins Played` for each combination of `Artist Name` and `Year`.
  - Within each `Year`, rank artists in descending order of yearly total minutes using competition ranking with the minimum rank for ties (`rank(method="min", ascending=False)`), and store this integer result as `Ranking`.
  - After `Ranking` is created, keep only `Artist Name`, `Year`, and `Ranking` for the reshape step.
- Reshape to compare how artist position changes year to year:
  - Pivot the yearly rankings wider so each artist has one row and each year 2015–2022 becomes a separate column containing that artist’s `Ranking` for the year.
  - Ensure the year columns exist in the final output for all years 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022 (values should be missing/NULL where an artist has no ranking for that year).
  - Store each year column as a nullable integer type (so missing values are allowed).
- Combine overall and yearly results:
  - Left-join the wide yearly table to the overall ranking table on `Artist Name` so every artist with an overall rank is retained.
- Filter to the overall top 100 artists:
  - Keep only artists where `Overall Rank <= 100`.
  - Sort the final result by `Overall Rank` ascending.
- Output the data with columns ordered exactly as specified.

## Output

- output_01.csv
  - 10 fields:
    - Overall Rank
    - Artist Name
    - 2015
    - 2016
    - 2017
    - 2018
    - 2019
    - 2020
    - 2021
    - 2022
