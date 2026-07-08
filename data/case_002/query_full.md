## Context

You are choosing between London and Edinburgh based purely on weather. Prepare a tidy, analysis-ready dataset from the provided input files so the two cities can be compared consistently across four weather metrics. Use Tableau Prep version 2019.1 or later.

## Requirements

- **Input the data**
  - Load all provided input CSV files and combine them into a single dataset (append/union all rows).
  - Ensure the combined dataset contains the fields **City**, **Metric**, **Measure**, **Value**, and **Date**. If any of these fields are absent in an input file, create them as blank for those rows before proceeding.

- **Get rid of those nicely formatted titles**
  - Remove non-data rows by excluding rows that do not provide usable records (e.g., rows where all fields are blank).
  - Validate required fields for downstream steps: keep only rows where **City**, **Metric**, **Measure** are present (non-blank) and **Date** and **Value** can be parsed to valid date and numeric types, respectively.

- **Make sure you get all the data in the Excel sheet loaded in to Prep**
  - Treat the union of all input files as the full source for the transformation; do not sample or limit rows prior to reshaping.

- **Clean up the City names to create two cities in one column (London and Edinburgh)**
  - Use the existing **City** field as the city identifier and restrict the dataset to the two target cities only:
    - Keep rows where **City** is exactly **London** or **Edinburgh**.
    - Exclude all other cities.

- **Pivot the data to give a measure per column for the four metrics in the data set**
  - Create a metric label field by concatenating **Metric** and **Measure** as:  
    **Metric_clean = Metric + " - " + Measure**
  - Keep only rows where **Metric_clean** is one of the following four metrics:
    - Wind Speed - mph
    - Max Temperature - Celsius
    - Min Temperature - Celsius
    - Precipitation - mm
  - If there are multiple records for the same **City**, **Date**, and **Metric_clean**, keep a single value by taking the first available record after combining inputs.
  - Pivot the dataset to wide format so that:
    - Each output row represents a unique **City** and **Date**.
    - The four metrics become four separate columns, populated from **Value**.
    - If any of the four metric columns are missing after pivoting, add them as empty (null) columns.
  - Filter the resulting wide dataset to the inclusive date window **2019-02-16 through 2019-02-22** (based on the parsed date).
  - Format **Date** as a string in **dd/mm/YYYY**.
  - Ensure the four metric columns are integers in the output.

- **Output the data**
  - Output a single CSV with exactly the required six fields.

## Output

- output_01.csv
  - 6 fields:
    - City
    - Date
    - Wind Speed - mph
    - Max Temperature - Celsius
    - Min Temperature - Celsius
    - Precipitation - mm