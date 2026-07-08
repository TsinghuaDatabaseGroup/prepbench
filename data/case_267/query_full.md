## Context
Graduates are on a UK Plan 2 student loan. Repayments are calculated as 9% of earnings above a repayment threshold of £27,295, and the loan balance accrues interest at 7.7% per year compounded monthly. During the course, borrowing occurs once per academic year on 1 September. Repayments begin in the April following graduation, and this task produces a snapshot as of April 2024.

## Requirements
- Input the data.
- Use two inputs:
  - A loan plan / repayment parameters table (from `input_01.csv`) containing, at minimum, `Loan`, `Interest`, `Repayment Threshold`, and `% Repayment over Threshold`.
  - An undergraduate loans table (from `input_02.csv`) containing, at minimum, `Amount per year`, `Course Start`, and `Course Length (years)`.
- From the plan table, select the single row corresponding to the Undergraduate plan and extract:
  - Annual interest rate (`r`) from `Interest`.
  - Repayment threshold from `Repayment Threshold`.
  - Repayment percentage from `% Repayment over Threshold`.
  - Convert the annual interest rate to a monthly rate as: `monthly_rate = annual_interest / 12`.
- In the Undergraduate Loans table, create a row for every year of the course, representing an annual borrowing event:
  - For each course record, generate exactly `Course Length (years)` rows.
  - The borrowing (“payment”) date for each generated row is 1 September of each course year, starting in the course start year and incrementing by 1 year for each subsequent row.
  - The principal for each generated row is `Amount per year`.
- Calculate the number of whole months between each borrowing date (1 September of the relevant year) and April 2024 using a month-difference calculation:
  - `months = (2024 - pay_year) * 12 + (4 - 9)`, where `pay_year` is the year of the borrowing date (September is month 9; April is month 4).
- Join with the repayment details (the Undergraduate plan parameters) so that each generated borrowing row has the plan’s `monthly_rate`, threshold, and repayment percentage available. Treat the plan parameters as a single record applied to all borrowing rows (i.e., a cross-join style attachment).
- For each generated borrowing row, calculate the value of the borrowed amount grown with compound interest up to April 2024 using monthly compounding:
  - Use compound interest in the form:
    \[
    A = P\left(1+\frac{r}{n}\right)^{nt}
    \]
    and implement it here as:
    - `amount_with_interest = amount * (1 + monthly_rate) ** months`
    - where `amount` is the annual principal (`Amount per year`), and `months` is the number of months from the borrowing date to April 2024.
- Total these values together so only 1 row remains:
  - `Total Borrowed` = sum of all annual principals across all generated rows.
  - `Total With Interest` (intermediate) = sum of all `amount_with_interest` across all generated rows.
- Introduce a Salary parameter with values: £30,000, £35,000, £40,000, and use the £35,000 salary value to compute repayments in this output.
- Work out the monthly repayment based on salary and the plan parameters:
  - `annual_repayment = max(0, salary - threshold) * (repayment_percent / 100)`
  - `Monthly Repayment = annual_repayment / 12`
- Apply the first monthly repayment immediately to the April 2024 total-with-interest balance to get the post-repayment balance:
  - `Total Borrowed + Interest = max(0, Total With Interest - Monthly Repayment)`
- Also work out how much interest will be applied in the following month after repayment:
  - `Interest to be added next month = (Total Borrowed + Interest) * monthly_rate`
- Rounding requirements:
  - Round `Monthly Repayment` to 2 decimal places.
  - Round `Total Borrowed` to 0 decimal places.
  - Round `Total Borrowed + Interest` to 2 decimal places.
  - Round `Interest to be added next month` to 2 decimal places.
- Output the data as a single-row table with exactly the required fields.

## Output

- output_01.csv
  - 4 fields:
    - Monthly Repayment
    - Total Borrowed
    - Total Borrowed + Interest
    - Interest to be added next month