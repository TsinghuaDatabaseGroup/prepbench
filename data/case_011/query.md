## Requirements

- Input the data
- Break up the JSON_Name field
- Exclude 'meta' and '' records in the same column to just leave 'indicators' and 'timestamp'
- For the column containing our metrics, if this is blank, take the value from the 'indicators' / 'timestamp' column. Rename this field as 'Data Type'
- There is a column that will contain just numbers (up to 502). If this column is blank then take the value from the other column that contains similar values up to 502. Rename this field to 'Row'
- Rename 'JSON_ValueString' to 'Value'
- Only leave fields in your data set that have been renamed as per the instruction above.
- Pivot fields to form final table structure
- Turn Unix Epoch time in to a real date
- Output the data

## Output

- output_01.csv
  - 8 fields:
    - Date
    - volume
    - high
    - low
    - adjclose
    - close
    - open
    - Row
