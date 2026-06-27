## Context
Chin & Beard Suds Co. records theft incidents in its stores, including the date of the theft and (when applicable) the date and quantity of the corresponding inventory adjustment. Build a single, analysis-ready dataset that consolidates thefts and stock adjustments per incident so the business can evaluate which products are most stolen, what has not yet been adjusted, which stores lag or lead in adjustments, and where adjustments do not match the stolen quantities.

## Requirements
- Input the data.
- Input data from both sheets/files:
  - `input_01.csv`: transactional records containing (at minimum) Store ID, Crime Ref Number, Action, Quantity, Date, and Type.
  - `input_02.csv`: a Store ID to Store/Branch Name mapping.
- Update Store IDs to use the Store Names:
  - Build a mapping from `input_02.csv` such that each Store ID maps to a corresponding Branch/Store Name.
  - Add a `Branch Name` field to the transactional records by left-mapping on `Store ID` (retain theft records even when a store name is missing).
- Clean up the Product Type to just return two products types: Bar and Liquid:
  - Derive `Type` as **Bar** if the original Type value indicates “bar” (case-insensitive containment); otherwise set it to **Liquid**.
- Create an incident-level dataset at the grain of **one row per `Crime Ref Number`** by combining theft and stock adjustment information:
  - Split the transactional records into:
    - Theft records where `Action` equals **Theft**
    - Adjustment records where `Action` equals **Stock Adjusted**
  - For each `Crime Ref Number`, compute theft-side metrics from Theft records:
    - `Stolen volume` = sum of `Quantity`
    - `Theft` = earliest (minimum) `Date`
    - `Number of Records` = count of Theft records for that `Crime Ref Number`
    - `Type` and `Branch Name` carried through consistently for the incident (use the first available values from the theft-side aggregation).
  - For each `Crime Ref Number`, compute adjustment-side metrics from Stock Adjusted records:
    - `Stock Adjusted` = earliest (minimum) `Date`
    - Total adjusted quantity = sum of `Quantity` (use this value only for downstream calculations; it is not directly output as a standalone field).
  - Join adjustment-side metrics onto the theft-side incident table using a **left join on `Crime Ref Number`** so theft incidents remain present even if no adjustment exists.
- Measure the difference in days between when the theft occurred and when the stock was updated:
  - `Days to complete adjustment` = (`Stock Adjusted` date − `Theft` date) in whole days.
  - If there is no stock adjustment date for an incident, the resulting days value should be missing/null.
- Measure the variance in stolen stock and inventory adjustment:
  - `Stock Variance` = `Stolen volume` − abs(total adjusted quantity), treating missing adjusted quantity as 0.
- Format and ordering rules that affect the output:
  - Parse `Date` values as dates before aggregating.
  - Output `Theft` and `Stock Adjusted` as text formatted `DD/MM/YYYY`.
  - Sort the final output by `Stock Adjusted` ascending with missing values first, then by `Theft` ascending, then by `Crime Ref Number` ascending.
- Output the data exactly with the specified fields and file name.

## Output

- output_01.csv
  - 9 fields:
    - Branch Name
    - Crime Ref Number
    - Days to complete adjustment
    - Number of Records
    - Stock Adjusted
    - Stock Variance
    - Stolen volume
    - Theft
    - Type