## Context
Data Source Bank captures new customers each month in separate tables, which makes cross-month comparison difficult. The goal is to consolidate all monthly customer records into a single dataset and restructure the demographic information so each customer has one row with separate fields for each demographic attribute.

## Requirements

- Input the data.
  - Treat each monthly table as a separate input (e.g., separate workbook tabs exported as separate input files).
  - The monthly inputs may be provided as multiple files; if some expected monthly inputs are not present, proceed with the available ones.

- Stack (union) all monthly tables on top of one another because they share the same logical fields.
  - You may do this either by explicitly unioning each table or by using a wildcard union at input time.
  - Align fields by name when unioning; fields that do not exist in a given month should be left null for that month’s rows.

- Create **Joining Date** using:
  - **Joining Day** as the day-of-month,
  - the source table name (i.e., which monthly table/file the row came from) as the month-of-year,
  - and the fixed year **2023**.
  - Format **Joining Date** as `DD/MM/YYYY` text.
  - Use the following month assignment for each input source:
    - `input_01.csv` = April (04)
    - `input_02.csv` = August (08)
    - `input_03.csv` = December (12)
    - `input_04.csv` = February (02)
    - `input_05.csv` = January (01)
    - `input_06.csv` = July (07)
    - `input_07.csv` = June (06)
    - `input_08.csv` = March (03)
    - `input_09.csv` = May (05)
    - `input_10.csv` = November (11)
    - `input_11.csv` = October (10)
    - `input_12.csv` = September (09)

- Reshape the data so each customer has a single row with one field per demographic.
  - Input data is in a “long” format where demographics are stored as rows (with a demographic name and a corresponding value).
  - Pivot to a “wide” format so that, for each customer and joining date, you produce separate columns for:
    - **Account Type**
    - **Date of Birth**
    - **Ethnicity**
  - When pivoting, if multiple rows exist for the same customer/joining date/demographic, take the first available value for that demographic.

- Ensure all data types are correct for each field.
  - Ensure **ID** is treated as text.
  - Ensure **Date of Birth** is formatted as `DD/MM/YYYY` text (coercing invalid/unparseable dates to null rather than failing).

- Remove duplicates across months:
  - If the same **ID** appears multiple times, keep only one record for that customer.
  - Select the record with the earliest **Joining Date** (using date ordering, not string ordering).
  - If there is a tie on earliest joining date, keep a single deterministic record (e.g., by stable ordering on **ID**).

- Output the data.
  - Output should contain exactly one row per unique customer **ID** (after de-duplication), with the required fields below.
  - Produce a deterministic output ordering by sorting by **ID** ascending before writing.

## Output

- output_01.csv
  - 5 fields:
    - ID
    - Joining Date
    - Account Type
    - Date of Birth
    - Ethnicity