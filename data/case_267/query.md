## Context
- Graduates are on Plan 2 student loans: repay 9% of earnings over £27,295
- Interest is 7.7% applied monthly (compound)
- Loan payments are made on 1st September each year of the course
- Repayments start in April after graduation

## Requirements
- Input the data
- In the Undergraduate Loans table, create a row for every year of the course (payment date: 1st September)
- Calculate the number of months between the payment date and April 2024
- Join with the Repayment details table
- Calculate the Amount Borrowed + the Interest applied (use compound interest)
    - Compound interest is calculated as:
    $$A=P\left(1+\cfrac{r}{n}\right)^{nt}$$
    where:
        * $A$ is the final amount
        * $P$ is the original principal sum
        * $r$ is the nominal annual interest rate
        * $n$ is the compounding frequency
        * $t$ is the overall length of time the interest is applied (expressed using the same time units as $r$, usually years)
- Total these values together so only 1 row remains (total borrowed and total with interest)
- Introduce a Salary parameter with values: £30,000, £35,000, £40,000
- Workout what their monthly repayment will be
- Also work out how much interest will be applied in the following month after repayment
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Monthly Repayment
    - Total Borrowed
    - Total Borrowed + Interest
    - Interest to be added next month
