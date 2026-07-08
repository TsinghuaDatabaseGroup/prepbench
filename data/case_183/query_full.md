## Context

You are producing a month-by-month mortgage capital repayment schedule for each store, starting from a fixed “today” date of 10 August 2022. For each store’s mortgage, you will calculate the portion of the monthly payment that goes toward capital, determine how many whole months are required to fully repay the remaining capital, and then expand the data to one row per month (per store) until payoff. Each monthly row must also include the total capital still outstanding across all stores for that month.

## Requirements

- Input the data from `inputs/input_01.csv`.
  - Treat each input row as one store's mortgage.
  - The input must include, at minimum, the fields:
    - `Store`
    - `Capital Repayment Remaining`
    - `Monthly Payment`
    - `% of Monthly Repayment going to Capital` (a percentage value, e.g., 25 means 25%).
- Create a field for today, fixed as 10th August 2022.
- Create a data field to show how much capital is paid off each month:
  - `Monthly Capital Payment = Monthly Payment * (% of Monthly Repayment going to Capital / 100)`.
- Create a data field to show how many months are needed to pay off the entire debt (whole months only):
  - `Months to Payoff = ceil(Capital Repayment Remaining / Monthly Capital Payment)`.
- Generate monthly payment dates for each store:
  - The first payment is made on 10 August 2022. August 2022 is the first payment month, and the schedule includes this initial payment.
  - Generate monthly payment dates starting on 10/08/2022 (the 10th day of the month) and repeating monthly for the number of months in `Months to Payoff` per store.
  - Each store's schedule includes exactly `Months to Payoff` payment dates, starting from 10/08/2022.
- Create a row per month for each store showing the repayment status:
  - Include exactly one row for each payment date generated for each store (i.e., one row per month per store for `Months to Payoff` months).
  - Include the final payment month even if `Remaining Capital to Repay` becomes exactly 0 or negative in that month (i.e., the month where the debt reaches zero).
  - Exclude any months after a store's debt is fully paid off (i.e., do not include months beyond the `Months to Payoff` count for that store).
  - Rename the date field to `Monthly Payment Date`.
    - The schedule starts at 10 August 2022 and advances by whole months.
    - Format `Monthly Payment Date` as `DD/MM/YYYY` (e.g., 10/08/2022, 10/09/2022, ...).
  - For each store and month, compute the remaining capital after that month's payment is applied:
    - The `Remaining Capital to Repay` value for each `Monthly Payment Date` represents the capital remaining **after** the payment for that date has been applied.
    - Calculate `Remaining Capital to Repay = Capital Repayment Remaining - (month_number * Monthly Capital Payment)`,
    - where `month_number` is 1 for the first scheduled payment month (August 2022, date 10/08/2022), 2 for the next month (September 2022, date 10/09/2022), etc.
    - Example: On 10/08/2022 (month_number = 1), the remaining capital = initial `Capital Repayment Remaining` - 1 × `Monthly Capital Payment`, meaning the payment on 10/08/2022 has already been deducted from the remaining capital shown for that date.
  - For each `Monthly Payment Date`, compute the total remaining capital across all stores that have a row for that date:
    - `Capital Outstanding Total` is the sum of `Remaining Capital to Repay` across all stores that have an output row for that same `Monthly Payment Date`.
    - A store has a row on a given `Monthly Payment Date` if that date is within the store's payment schedule (i.e., the date is one of the `Months to Payoff` payment dates for that store, starting from 10/08/2022).
    - Include all stores that have a row for the date in the sum, regardless of whether their `Remaining Capital to Repay` is positive, zero, or negative for that date.
- Output the data exactly with the required columns.

## Output

- output_01.csv
  - 4 fields:
    - Monthly Payment Date
    - Store
    - Capital Outstanding Total
    - Remaining Capital to Repay