## Context

You have monthly sales and profit data for multiple product categories and scents across two stores, along with a separate table of staff days worked by store and month. The goal is to reshape the sales/profit data into a tidy, date-based structure, then attach the corresponding staff days worked for the same store and month, and finally output a single consolidated dataset with only the required fields.

## Requirements

- Input the data:
  - Read `input_01.csv` and `input_02.csv` as the two store sales/profit inputs.
    - Treat all rows from `input_01.csv` as `Store = "Lewisham"`.
    - Treat all rows from `input_02.csv` as `Store = "Camden"`.
  - Read `input_03.csv` as the staff days worked input.

- Create Sales and Profit columns (one for each measure):
  - In the combined sales/profit data (Lewisham + Camden), the measures are provided in a wide format with separate columns for each month, prefixed with `Sales ` and `Profit `.
  - Reshape (unpivot) the wide monthly measure columns so that the output has exactly one `Sales` value and one `Profit` value per `(Store, Category, Scent, Date)`.
  - Pair sales and profit by the same month based on the date portion of the column name (i.e., the part after the first space in `Sales <date>` / `Profit <date>`), so that both measures correspond to the same `Date` row.

- Create a date field:
  - For the sales/profit output rows, set `Date` to the date string extracted from the monthly Sales/Profit column names (the substring after the first space).
  - For the staff table, parse `Month` as a date and format it as `DD/MM/YYYY` into a `Date` field to align with the sales/profit `Date` strings.

- Add on the number of days worked by staff in each store:
  - Convert the staff input from wide to long so it yields rows at the grain `(Store, Date)` with a single `Staff days worked` value.
    - Use the store columns present in the staff file for `Lewisham`, `Camden`, and `Dulwich` when reshaping.
  - Join staff days worked onto the sales/profit dataset using a left join on `(Store, Date)`, keeping all sales/profit rows.
  - Only add staff numbers where store sales and profits exist:
    - Do not create standalone staff-only rows; staff values should appear only when there is a corresponding sales/profit row for the same `Store` and `Date`.

- Remove excess fields:
  - The final dataset must contain only the seven required fields in the specified order: `Store`, `Category`, `Scent`, `Date`, `Sales`, `Profit`, `Staff days worked`.

- Output the data:
  - Produce a single CSV output.
  - Sort rows for consistent output by `Store`, then `Category`, then `Scent` in the custom order `Mint`, `Lemon`, `Raspberry`, and then by `Date` ascending.

## Output

- output_01.csv
  - 7 fields:
    - Store
    - Category
    - Scent
    - Date
    - Sales
    - Profit
    - Staff days worked