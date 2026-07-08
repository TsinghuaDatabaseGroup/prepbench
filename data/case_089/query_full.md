## Context
You are preparing a clean, analysis-ready dataset of the most popular baby names in England and Wales for 2019. The source is provided as two separate inputs: one for boys’ names and one for girls’ names. In each input, the data for each month appears in a horizontally arranged block (months laid out side-by-side), and the task is to transform these blocks into a single, consistent month-level dataset and then produce an annual Top 10 summary by gender.

## Requirements
- Input the data.
  - Use `input_01.csv` for boys and `input_02.csv` for girls (both have no header row and should be treated as raw, positional tables).

- Restructure each input (boys first, then girls) into a single long-form monthly table with the fields:
  - `Month`, `Rank`, `Name`, `Count`, `Gender`.

- Month/block identification and reshaping logic (applies to both inputs):
  - Treat the presence of a month name (January through December) within a row as the start of a month section.
  - For each month section:
    - The row containing the month name(s) is followed by one header row.
    - The actual data rows for that section begin after those two rows and continue until the next month section begins (or the end of the file).
  - Within each section, extract repeated 3-column groups corresponding to each month present in that section, in the order:
    - `Rank`, `Name`, `Count`.
  - Pivot/stack these 3-column month groups so that each output row represents one name at one month and one rank, with:
    - `Month` coming from the month label,
    - `Rank`, `Name`, and `Count` coming from the corresponding columns in that month’s 3-column group.

- Filtering during parsing:
  - Remove any rows that represent totals (i.e., rows containing "Total").

- Add a `Gender` field:
  - Set `Gender = "Boys"` for all rows derived from `input_01.csv`.
  - Set `Gender = "Girls"` for all rows derived from `input_02.csv`.

- Combine boys and girls:
  - Append the two cleaned monthly datasets into a single monthly dataset (same schema).

- Output the monthly rankings as a single datasource:
  - Ensure the monthly output contains exactly the fields `Rank`, `Count`, `Name`, `Month`, `Gender`.
  - Sort the monthly output by `Month` in calendar order (January to December), then by `Gender`, then by `Rank` (ascending).

- Aggregate to a year level and calculate new rankings:
  - Group the combined monthly dataset by `Name` and `Gender`.
  - Sum `Count` across all months to produce an annual `Count` per `Name`/`Gender`.
  - For each `Gender`, rank names by annual `Count` in descending order and keep only the top 10 names per gender.
  - Create `2019 Rank` within each gender as 1 through 10 in that sorted order.
  - Sort the final annual output by `Gender`, then `2019 Rank` (ascending).

- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - 2019 Rank
    - Count
    - Name
    - Gender

- output_02.csv
  - 5 fields:
    - Rank
    - Count
    - Name
    - Month
    - Gender