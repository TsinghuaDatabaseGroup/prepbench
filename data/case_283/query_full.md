## Context

You are given historical championship-winner tables for a tournament, split across Singles, Doubles, and Mixed Doubles. The goal is to build a champion-level summary that (1) counts how many titles each person has won in each tournament category, (2) identifies each champion’s most recent winning year, and (3) ranks champions by total titles—restricted to champions who have won at least one Singles title and at least one Doubles title.

## Requirements

- Input the data from the three provided files:
  - `input_03.csv` (Singles): includes a `year` column plus winner fields for men and women.
  - `input_01.csv` (Doubles): includes a `year` column plus winner fields for men and women.
  - `input_02.csv` (Mixed Doubles): includes a `Year` column and a `Champions` field.

- Filter out the years where the championship did not take place:
  - Exclude any rows that explicitly indicate the event was not held / no competition (per the text in the input row).
  - Also exclude rows where the year cannot be interpreted as a valid year.

- Ensure the Year field is numeric:
  - Produce an integer year for each remaining record:
    - Use the `year` field from Singles and Doubles.
    - Use the `Year` field from Mixed Doubles.

- Reshape the data so there is a row for each Champion, for each Year, even where there are 2 winners in the Doubles:
  - Convert each source into a consistent long format with the grain: **one row per (Year, Champion, Tournament)**.
  - If a winner cell contains multiple champions (e.g., a doubles pair listed together), split it into separate champion rows so each person is counted individually for that title-year.

- Make sure it's clear which tournament they were the Champion of: Either Men's Singles, Women's Singles, Men's Doubles, Women's Doubles or Mixed Doubles:
  - Assign the `Tournament` label as follows:
    - Singles `men` → `Men's Singles`
    - Singles `women` → `Women's Singles`
    - Doubles `men` → `Men's Doubles`
    - Doubles `women` → `Women's Doubles`
    - Mixed `Champions` → `Mixed Doubles`

- Create a field to indicate the Gender of each Champion:
  - Derive gender from participation in gendered tournaments:
    - Champions appearing in men’s tournaments are labeled `Man`.
    - Champions appearing in women’s tournaments are labeled `Woman`.
  - Mixed Doubles does not directly imply gender; if a champion only appeared in Mixed Doubles, gender would be unknown. (Champions retained after later filtering should have a gender from Singles and/or gendered Doubles.)

- Bring the data together so it's clear for each Champion how many of each tournament they've won:
  - For each Champion (and their derived Gender), compute the count of titles in each of the five tournament categories by summing occurrences in the long table.
  - Missing tournament categories for a champion must be treated as 0.

- For each Champion, calculate the most recent win across tournaments:
  - Compute `Most Recent Win` as the maximum Year across all tournaments for that Champion (using the long table).

- Filter the data to only include Champions who have won both Singles and Doubles tournaments:
  - Define Singles wins as: `Women's Singles` + `Men's Singles`.
  - Define Doubles wins as: `Women's Doubles` + `Men's Doubles` + `Mixed Doubles`.
  - Keep only champions where Singles wins > 0 **and** Doubles wins > 0.

- Create a calculation for the Total Championships each Champion has won:
  - `Total Championships` = `Women's Singles` + `Men's Singles` + `Women's Doubles` + `Mixed Doubles` + `Men's Doubles`.

- Rank the Champions in descending order of their Total Championships:
  - Sort champions by:
    1) `Total Championships` descending, then
    2) `Most Recent Win` descending.
  - Compute `Rank` using competition ranking on `Total Championships` (ties receive the same rank equal to the minimum rank in the tied group).

- Output the data:
  - Produce `output_01.csv` with exactly the required fields in the required order.
  - Ensure all numeric outputs (including `Rank` and `Most Recent Win`) are stored as integers.

## Output

- output_01.csv
  - 10 fields:
    - Rank
    - Champion
    - Gender
    - Total Championships
    - Women's Singles
    - Men's Singles
    - Women's Doubles
    - Mixed Doubles
    - Men's Doubles
    - Most Recent Win