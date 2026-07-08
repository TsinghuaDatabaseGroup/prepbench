## Context
Chin & Beard Suds Co. records total weekly sales in GBP, but the business sells in both the UK and the US. For each calendar week, the company also records the percentage of sales attributable to the US (with the remainder attributable to the UK). Executives want to estimate a weekly range for US revenue in USD by applying the week’s best-case and worst-case GBP→USD exchange rates to the US portion of weekly sales.

## Requirements
- Input the data.
- Use the exchange-rate input to calculate weekly GBP→USD conversion rates:
  - Parse the numeric USD rate from the provided “British Pound to US Dollar” text field.
  - Use the exchange-rate date to assign each record to a calendar week defined as a Sunday-start week number (week numbering consistent with `%U`), and also retain the corresponding year.
  - For each (Year, Week), compute:
    - **Best rate** = maximum rate observed in that week
    - **Worst rate** = minimum rate observed in that week
- Take the sales data and determine the UK / US split:
  - Interpret `US Stock sold (%)` as the US share of sales for that row (as a fraction of 1 after dividing by 100).
  - Compute UK share as `1 - US share`.
- Apply the UK / US sales split to the value sold in GBP:
  - `US_Sales_GBP = Sales Value * US share`
  - `UK_Sales_GBP = Sales Value * UK share`
- Align sales weeks to exchange-rate weeks and join:
  - Treat the sales data’s `Week` as the reporting week label, but match it to exchange rates from the prior Sunday-start week by defining `Week_U = Week - 1`.
  - Join sales to weekly exchange rates using an **inner join** on:
    - Sales `Year` = Rates `Year`
    - Sales `Week_U` = Rates `Week`
  - If a sales week has no matching weekly exchange rate, exclude it from the output (due to the inner join).
- For each joined sales week, compute US sales in USD:
  - **US Sales (USD) Best Case** = `US_Sales_GBP * Best rate`
  - **US Sales (USD) Worst Case** = `US_Sales_GBP * Worst rate`
  - **US Sales Potential Variance** = `Best Case - Worst Case`
- Format and round outputs:
  - Round all monetary output fields to **2 decimal places**.
  - Output `Week` as a string in the form: `wk {Week} {Year}`, using the sales data’s `Week` and `Year` values.
  - Sort the final output by sales `Year` ascending, then sales `Week` ascending.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Week
    - UK Sales Value (GBP)
    - US Sales (USD) Best Case
    - US Sales (USD) Worst Case
    - US Sales Potential Variance