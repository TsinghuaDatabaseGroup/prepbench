## Context

Occasionally, employees may want to transfer from one distribution center to another (for example, if the employee wants to move to a different city). The company doesn't have a consistent policy or process for that. The HR manager has asked us to figure out how often it happens, so the HR team knows if they should prioritize working on that policy.

Our HR recording system has a few issues, so we'll need to make some assumptions for this analysis.

## Requirements

- Input the data
- Flag when transfers occurred:
  - A transfer occurs when the employee's dc_nbr changes from month to month, and the difference in months is <= 2.
  - Our HR system doesn't differentiate between an employee transferring from one DC to another vs. the employee quitting and then being rehired at another DC later, so we are going to make the assumption that if the gap is no more than two months, it was a transfer
  - For example, if an employee worked at DC #1 in May, did not work in June, then worked at DC2 #2 in July, that would count as a transfer
  - Make sure to flag the transfer in the month that the employee left the old DC (NOT the month the employee started working at the new DC)
- For each DC, calculate:
  - The count of unique employee_ids present for all history. Name this ee_count
  - The total number of transfers. Name this xfer_count
  - The percentage of employees who transferred. Name this xfer_pct and format with two decimal places (e.g. 33.35% = 35.35)
  - The average tenure (in months) for employees that transferred. Name this avg_tenure_months and format with two decimal places
- Include a total row, with the totals across all DCs
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - dc_nbr
    - ee_count
    - xfer_count
    - xfer_pct
    - avg_tenure_months
