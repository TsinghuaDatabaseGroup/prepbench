## Context
At Chin & Beard Suds Co (our Preppin' Data fake company), one of our non-executive directors has asked about the effects of Valentine's Day on our store sales. Sadly, the non-exec director isn't very good with Table Calculations in Tableau Desktop so we have promised a data set to allow them to build their own views with all of the calculations pre-computed.

## Requirements
- Input the data from `input_01.csv`.
- Treat each input row as a single store’s sales for a specific date (i.e., the output remains at the same grain as the input: Store + Date).
- Parse `Date` as a true date value (expected in `YYYY-MM-DD` format).
- Determine if the sales date is pre- or post- Valentine's day using **2019-02-14** as Valentine’s Day:
  - If `Date` is on or before **2019-02-14**, label `Pre / Post Valentines Day` as `Pre`.
  - If `Date` is after **2019-02-14**, label `Pre / Post Valentines Day` as `Post`.
- Set `Daily Store Sales` equal to the numeric sales value for that row (from the input `Value` field), as a number.
- Work out the running total of sales for each store, restarting after Valentine's day to allow comparison of the pre vs post periods:
  - Sort records by `Store`, then `Pre / Post Valentines Day`, then `Date` (ascending).
  - Within each partition defined by (`Store`, `Pre / Post Valentines Day`), compute `Running Total Sales` as the cumulative sum of `Daily Store Sales` in date order.
- Format the output `Date` as text in `DD/MM/YYYY`.
- Output the data to the required file with the required fields and names.

## Output

- output_01.csv
  - 5 fields:
    - Pre / Post Valentines Day
    - Store
    - Date
    - Running Total Sales
    - Daily Store Sales