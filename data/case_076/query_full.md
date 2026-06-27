## Context

Please enter your name and which challenge you have completed. The task itself is to standardize two weather-forecast extracts (hourly and daily) into one unified table with consistent fields.

## Requirements

- Input the data
  - Read `inputs/input_02.csv` (the “Next 5 Hours” forecast) and `inputs/input_03.csv` (the “Next 5 Days” forecast).
  - In both inputs, use the `Data` column as the sole source for parsing; each row contains a multi-line text block representing one forecast entry.
  - Treat each non-empty `Data` cell as one output row.
- Parse and standardize the hourly forecast (`input_02.csv`)
  - For each valid `Data` cell:
    - Set `Forecast Type` to `Next 5 Hours`.
    - Set `Date or Time` to the first line of the `Data` cell (the label for the time slot).
    - Set `Temperature` to the integer temperature extracted from the temperature line (capture the signed digits; store as an integer). If no temperature can be extracted, leave it null.
    - Set `Precipitation Chance` to the integer percentage extracted from the text pattern “Chance of Rain{N}%” if present; otherwise leave it null.
    - Set `Max Temp` and `Min Temp` to null (not applicable to hourly rows).
- Parse and standardize the daily forecast (`input_03.csv`)
  - For each valid `Data` cell:
    - Set `Forecast Type` to `Next 5 Days`.
    - Set `Date or Time` to the first line of the `Data` cell (the day label).
    - Set `Precipitation Chance` to the integer percentage extracted from the text pattern “Chance of Rain{N}%” if present; otherwise leave it null.
    - Set `Temperature` to null (not populated for daily rows).
    - Extract temperature values (signed integers) from the remaining lines:
      - If `Date or Time` equals `Today`, populate only `Min Temp` with the first extracted temperature value (if available) and leave `Max Temp` null.
      - Otherwise, populate `Max Temp` with the first extracted temperature value (if available) and `Min Temp` with the second extracted temperature value (if available). If only one temperature value is available, populate `Max Temp` with that value and leave `Min Temp` null.
- Combine outputs
  - Union the standardized hourly and daily rows into a single table (do not deduplicate).
  - Ensure the final column set and order exactly matches the required output schema.
  - Use nullable integer types for numeric fields so missing values remain null (not zero).
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Forecast Type
    - Date or Time
    - Temperature
    - Max Temp
    - Min Temp
    - Precipitation Chance