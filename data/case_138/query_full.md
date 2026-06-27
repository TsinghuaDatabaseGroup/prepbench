## Context
Engineers monitor the factory painting process for each bike batch through a stream of indicator updates. The source only records a new row when an indicator value changes, so the dataset represents discrete updates over time rather than continuous sampling. The objective is to restructure these updates into a tidy, long-form table where each row captures a single parameter update, labeled with the batch’s process step at the time of the update and enriched with the batch’s Bike Type and Batch Status.

## Requirements
- Input the data from `input_01.csv`.

- Create a Datetime field:
  - Combine the existing `Date` and `Time` fields into a single datetime value using day-first interpretation.
  - Use this combined datetime for all within-batch ordering steps.
  - Format the final output `Datetime` as text in `DD/MM/YYYY HH:MM:SS`.

- Parse the Bike Type and Batch Status for each batch:
  - Identify rows where `Data Type` equals `Result Data`.
  - Within each `Batch No.`, determine `Bike Type` as the last observed `Data Value` among result-data rows whose `Data Parameter` is `Bike Type`, ordered by `Datetime`.
  - Within each `Batch No.`, determine `Batch Status` as the last observed `Data Value` among result-data rows whose `Data Parameter` is `Batch Status`, ordered by `Datetime`.
  - Attach these batch-level values to every output row for the same `Batch No.` (left-join behavior: keep process updates even if Bike Type or Batch Status is missing).

- Preserve and label the stage where the update occurred:
  - Restrict process updates to rows where `Data Type` equals `Process Data`.
  - Within each `Batch No.`, sort rows by `Datetime`.
  - Treat rows with `Data Parameter` equal to `Name of Process Stage` as stage-definition events; the stage name is taken from their `Data Value`.
  - Create `Name of Process Step` for each process-data row by forward-filling the most recent stage-definition value within the same `Batch No.`.
  - Exclude the stage-definition rows themselves from the final long-form updates; only keep the parameter-update rows that occur during stages.

- Split out the value field into two fields: Target and Actual:
  - For each remaining process-data row, interpret `Data Parameter` as having a prefix of either `Target ` or `Actual ` followed by the underlying parameter name.
  - Extract:
    - the kind (`Target` vs `Actual`) from the prefix, and
    - the cleaned underlying parameter name as the output `Data Parameter`.

- Ensure the Data Parameter is one of: Current, Voltage, Gas Flow, Temperature, Pressure:
  - After extracting the cleaned parameter name, keep only rows whose cleaned `Data Parameter` is exactly one of:
    - `Current`, `Voltage`, `Gas Flow`, `Temperature`, `Pressure`.

- Keep one record per update per parameter (long format), preserving the stage where the update occurred:
  - Output grain: one row per qualifying process-data update event (i.e., one input process-data row after removing stage-definition rows and filtering to the five allowed parameters).
  - Populate:
    - `Target` with the row’s `Data Value` only when the kind is `Target`; otherwise leave `Target` blank/null.
    - `Actual` with the row’s `Data Value` only when the kind is `Actual`; otherwise leave `Actual` blank/null.
  - Convert `Target` and `Actual` to numeric where possible; non-numeric values should become nulls.

- Output the cleaned data with the required fields and names. (A stable sort by `Batch No.`, then `Datetime`, then `Name of Process Step`, then `Data Parameter` may be applied to make row order deterministic.)

## Output

- output_01.csv
  - 8 fields:
    - Batch No.
    - Name of Process Step
    - Bike Type
    - Batch Status
    - Datetime
    - Data Parameter
    - Target
    - Actual