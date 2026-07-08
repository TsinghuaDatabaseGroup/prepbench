## Context

You have multiple yearly employer pay-gap report extracts stored as separate CSV files. The goal is to combine these files into a single, consistent dataset, harmonise employer naming across years, and add a plain-English “Pay Gap” statement derived from the reported median hourly pay difference.

## Requirements

- Input the data.
  - Read up to five CSV files from the inputs directory: `input_01.csv` through `input_05.csv`.
  - Each file represents a distinct reporting period; tag every row with a `Report` label based on the source file:
    - `input_01.csv` → `2017 to 2018`
    - `input_02.csv` → `2018 to 2019`
    - `input_03.csv` → `2019 to 2020`
    - `input_04.csv` → `2020 to 2021`
    - `input_05.csv` → `2021 to 2022`

- Combine the files.
  - Union (append) all available tagged inputs into one dataset (do not deduplicate at union time).

- Keep only relevant fields.
  - Ensure the working dataset contains the fields needed to produce the required output: `EmployerName`, `EmployerId`, `EmployerSize`, `DiffMedianHourlyPercent`, plus the derived fields `Report`, `Year`, and `Pay Gap`.
  - Validate key numeric fields:
    - Parse `EmployerId` as an integer. Drop rows where `EmployerId` is missing/invalid after parsing.
    - Parse `DiffMedianHourlyPercent` as a numeric value (leave missing as missing if it cannot be parsed).

- Extract the Report years from the file paths.
  - Use the source file identity to determine the correct `Report` label (as listed above).

- Create a Year field based on the the first year in the Report name.
  - Create `Year` as an integer equal to the first four-digit year at the start of `Report` (e.g., `2017` from `2017 to 2018`).

- Some companies have changed names over the years. For each EmployerId, find the most recent report they submitted and apply this EmployerName across all reports they've submitted.
  - For each `EmployerId`, identify the most recent reporting year as the maximum `Year` for that employer.
  - From rows in that most recent year, collect the distinct `EmployerName` values for the employer.
  - Apply the most-recent-year employer name(s) to all rows for that `EmployerId` by replacing the original `EmployerName` with these latest name value(s).
    - If an employer has more than one distinct `EmployerName` in its most recent year, replicate the employer’s rows so that each latest-name value is represented (one output row per latest-name value per original row), and proceed to the final deduplication step described below.

- Create a Pay Gap field to explain the pay gap in plain English.
  - Use `DiffMedianHourlyPercent` to generate `Pay Gap`, respecting the dataset’s sign convention (below) and the required phrasing.

- You may encounter floating point inaccuracies. Find out more about how to resolve them.
  - When inserting the percentage value into the `Pay Gap` sentence (for non-zero, non-missing values), format the absolute value as follows:
    - Take the absolute value of `DiffMedianHourlyPercent`.
    - Round to 1 decimal place, then apply ceiling at 2 decimal precision to ensure the displayed value is never less than the rounded value (e.g., if rounded = 2.39, ceiling may produce 2.39 or 2.4 depending on precision).
    - Format as a string, removing trailing zeros only if the result is a whole number (e.g., `5.0` becomes `5`, but `2.39` stays `2.39`).
    - Truncate to appropriate length based on magnitude (3 significant characters for values < 10, 4 for values < 100).

- In this dataset, a positive DiffMedianHourlyPercent means the women's pay is lower than the men's pay, whilst a negative value indicates the other way around.
  - If `DiffMedianHourlyPercent` > 0, use “lower”.
  - If `DiffMedianHourlyPercent` < 0, use “higher”.
  - If `DiffMedianHourlyPercent` is 0 or missing, treat the median hourly pay as equal.

- The phrasing should be as follows:
  - In this organisation, women's median hourly pay is X% higher/lower than men's.
  - In this organisation, men's and women's median hourly pay is equal.

- Output the data，deduplicate records to avoid duplicate rows affecting evaluation
  - After all transformations, drop duplicate rows considering all output fields.
  - For deterministic output, sort the final dataset by `Year`, then `Report`, then `EmployerId` (ascending) before writing.

## Output

- output_01.csv
  - 7 fields:
    - Year
    - Report
    - EmployerName
    - EmployerId
    - EmployerSize
    - DiffMedianHourlyPercent
    - Pay Gap