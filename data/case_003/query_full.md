## Context
You work for a mobile/cell phone company and need to prepare a monthly revenue schedule for the current set of customer contracts. Each contract generates revenue once per month while it is live, starting on the contract’s start date and continuing for the number of months specified by the contract length. The goal is to produce a Tableau-ready dataset that supports recreating a monthly revenue visualization in Tableau Desktop after doing the data preparation in Tableau Prep Builder.

## Requirements
- Input the data.
- Import the file(s) and ensure **both sheets/files** are used as inputs:
  - A contracts table containing, at minimum: `Name`, `Monthly Cost`, `Contract Length (months)`, and `Start Date`.
  - A lengths table containing a single column `Length` representing month numbers to use for expansion (e.g., 1, 2, 3, …).
- Ensure data types are correctly interpreted for calculations:
  - `Contract Length (months)` and `Monthly Cost` must be treated as integers.
  - `Start Date` must be treated as a true date (interpreted from an ISO-style `YYYY-MM-DD` date string).
- Use the lengths table to expand each contract into **one row per month the contract is live**:
  - Create a cartesian-style expansion between contracts and the lengths table (i.e., pair each contract with all candidate `Length` values), then filter to keep only rows where `Length <= Contract Length (months)`.
  - Define a zero-based month offset `idx = Length - 1`.
  - Compute `Payment Date` for each expanded row as:  
    `Payment Date = Start Date + idx months`  
    (i.e., month 1 uses the start date; month 2 is start date plus 1 month; etc.).
- Keep only the required output fields and remove all other intermediate/helper fields (including any join keys, `Length`, `idx`, or ordering helpers).
- Prepare the dataset for use within Tableau Desktop and recreate the intended visualization using the monthly schedule output.
- Ensure the output row order is deterministic:
  - Sort primarily by month offset (`idx`) ascending (earliest payment month first).
  - Within each month offset, sort contracts by a round-robin order derived from the original contracts input order: assign names an order equal to their position in the **reversed** original appearance order, and sort by that order ascending.
- Format output fields as required:
  - `Payment Date` and `Start Date` must be written as text in `DD/MM/YYYY` format.
  - `Monthly Cost` and `Contract Length (months)` must be written as integers.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Payment Date
    - Name
    - Monthly Cost
    - Contract Length (months)
    - Start Date