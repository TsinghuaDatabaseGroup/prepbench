## Context
Chin & Beard Suds Co store performance data is arranged in an unconventional layout: for each Store there are three consecutive rows representing Sales, Target, and the Difference between them, with separate columns for each month. The goal is to transform this structure into a standard, analysis-ready table (suitable for Tableau Desktop) with one row per Store per Month and separate numeric columns for Sales, Target, and Difference.

## Requirements
- Input the data from the provided file.
- Ensure Store names are correctly populated for all rows by filling the Store value down within the table wherever it is missing.
- Remove null/empty rows that do not contain a Store name and do not contain any monthly values.
- Use the Row ID (the first column in the input) to classify each of the three rows per Store:
  - Within each Store, order rows by Row ID ascending.
  - Assign the first row to **Sales**, the second row to **Target**, and the third row to **Difference**.
  - Exclude any rows that cannot be assigned one of these three types.
- Pivot the monthly columns into a single Month column (i.e., reshape from wide months to long months) so each record represents one Store + one row type + one month.
  - Keep only records with a non-null value after pivoting.
- Convert the Month field to a Date data type, with all months belonging to year 2020.
  - Derive the month from the month column name (limited to Jan–Jul) and map it to the first day of that month in 2020.
- Reshape the data back to a wide format so that each output row represents exactly **one Store for one Month**, with three separate measure columns:
  - Sales
  - Target
  - Difference
- Output the final dataset.

## Output

- output_01.csv
  - 5 fields:
    - Store
    - Month
    - Sales
    - Target
    - Difference