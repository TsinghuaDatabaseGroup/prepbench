## Context

Employees sometimes move from one distribution center (DC) to another (for example, due to relocation). The company does not currently have a consistent policy or process for these moves, and HR wants to understand how often they occur so they can decide whether to prioritize formalizing a policy. Because the HR recording system does not explicitly distinguish transfers from separations followed by rehires, this analysis applies a specific operational definition of a “transfer.”

## Requirements

- Input the data.
  - Use `inputs/input_01.csv` as the source.
  - The analysis relies on, at minimum, the fields `employee_id`, `dc_nbr`, `month_end_date`, and `tenure_months`.
  - Treat `month_end_date` (and any other date fields used) as calendar dates parsed from day-first strings (DD/MM/YYYY). The transfer logic is based on the year and month components (i.e., month-to-month spacing), not day-level differences.
  - Ensure `tenure_months` is numeric so it can be averaged; if it is missing/invalid for a given record, it should not contribute to the mean tenure calculation.

- Flag when transfers occurred (event detection).
  - Evaluate each employee’s history independently.
  - For each `employee_id`, order their records by `month_end_date` ascending.
  - Compare each record to that employee’s next chronological record and compute the month gap as the difference in calendar months:  
    `months_to_next = (next_year - current_year) * 12 + (next_month - current_month)`.
  - A transfer event occurs when all of the following are true between a record and the employee’s next record:
    - `dc_nbr` changes (current `dc_nbr` ≠ next `dc_nbr`), and
    - the month gap is between 1 and 2 months inclusive (`months_to_next >= 1` and `months_to_next <= 2`).
  - This definition operationalizes the assumption that a DC change with a gap of no more than two months represents a transfer rather than a quit-and-rehire. This includes cases where an employee is absent for one month between DC assignments.
  - Flag the transfer on the record for the month the employee left the old DC (the earlier record in the pair), not on the month they appear at the new DC. The “from DC” for counting is the `dc_nbr` on the flagged (earlier) record.
  - If an employee has multiple qualifying DC changes over time, each qualifying change is counted as a separate transfer event.

- For each DC, calculate the following metrics at the DC level (one output row per `dc_nbr`), using all available history:
  - `ee_count`: the count of unique `employee_id` values that ever appear in that DC across all months in the input (distinct employees by DC).
  - `xfer_count`: the total number of transfer events originating from that DC (i.e., number of flagged records whose “from DC” equals that DC).
  - `xfer_pct`: the percentage of employees who transferred, computed as:  
    (number of unique `employee_id` values who have at least one transfer event originating from that DC) ÷ `ee_count` × 100.  
    Round to two decimal places.
  - `avg_tenure_months`: the average of `tenure_months` taken from the flagged transfer records for that DC (i.e., tenure at the time of leaving the DC). Round to two decimal places.
  - For DCs with no transfer events, set `xfer_count` to 0, `xfer_pct` to 0, and `avg_tenure_months` to 0 (after rounding rules).

- Include a total row with totals across all DCs.
  - Label this row’s `dc_nbr` as `Total`.
  - Compute totals as follows (do not sum DC-level distinct counts when a global distinct is required):
    - Total `ee_count`: distinct `employee_id` across the entire dataset (all DCs and all months).
    - Total `xfer_count`: total number of transfer events across all DCs (sum of all event counts).
    - Total `xfer_pct`: (distinct `employee_id` with at least one transfer event anywhere) ÷ (total distinct employees) × 100, rounded to two decimals.
    - Total `avg_tenure_months`: mean `tenure_months` across all transfer events (all flagged records), rounded to two decimals.

- Output the data.
  - Output exactly the five fields listed below.
  - Order rows by `dc_nbr` ascending (numerically for DCs), and place the `Total` row last.

## Output

- output_01.csv
  - 5 fields:
    - dc_nbr
    - ee_count
    - xfer_count
    - xfer_pct
    - avg_tenure_months