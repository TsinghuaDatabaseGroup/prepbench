## Context
Marketing wants to reward the highest-spending customers by emailing them discount codes. To do this, produce a ranked list of customers based on their total sales from orders placed in the last 6 months, where “last 6 months” is measured relative to 24/05/2019 (not today). The deliverable is the email addresses for customers who fall into the top 8% by this 6‑month total, along with their rank and total sales amount.

## Requirements
- Input the data.
- Download the **"Data for Processing"** folder containing all input files.

- Import and combine the sales data from the files while ensuring that any non-sales files accidentally included are not deleted or otherwise modified.
  - Treat the input as a folder of CSV files.
  - For the sales extraction, only use files that contain the three required fields: **Email**, **Order Total**, and **Order Date**.
  - From each qualifying file, read only these three fields and append (union) the rows across all qualifying files into one combined sales dataset.

- Restrict the combined sales rows to orders placed in the last 6 months calculated from **24/05/2019**.
  - Use an inclusive date window from **24/11/2018** through **24/05/2019**, inclusive of both endpoints.
  - Parse **Order Date** as a date using the expected day-month-year style shown in the files (e.g., `dd-Mon-YYYY`); rows with an invalid/unparseable date must not be included in the date-filtered set.

- Compute each customer’s total sales over that 6‑month window.
  - The customer key is **Email**.
  - Convert **Order Total** to a numeric value; non-numeric values should be treated as missing.
  - Aggregate to one row per **Email** by summing **Order Total** over all that customer’s filtered orders (summing while ignoring missing values).

- Rank customers by their 6‑month total sales.
  - Sort customers by **Order Total** descending (with **Email** ascending as a deterministic tie-breaker for ordering).
  - Compute **Last 6 Months Rank** as a "competition" rank based on **Order Total** descending (i.e., ties share the same rank, and the next rank after a tie skips ahead accordingly).
  - **Important**: The ranking must be computed based on the **original unrounded Order Total values**. Customers with identical unrounded **Order Total** values share the same rank. When comparing values for ranking purposes, use the full precision of the original **Order Total** values, not the rounded values. The rounding to 1 decimal place (specified in the output formatting step) is only applied for display purposes and does not affect the ranking calculation.

- Identify the “top 8%” customers to receive discount codes.
  - Let **N** be the number of customers (distinct emails) after aggregation.
  - Compute the cutoff count as `floor(N * 0.08)`, with a minimum of **1** customer when `N > 0`.
  - Keep customers whose **Last 6 Months Rank** is less than or equal to this cutoff rank threshold (this may include more than the cutoff count if ties occur at the boundary).

- Format the final output.
  - Include exactly the three output fields: **Last 6 Months Rank**, **Email**, **Order Total**.
  - Round **Order Total** to **1 decimal place**.
  - Sort the output by **Last 6 Months Rank** ascending, then **Email** ascending, then **Order Total** ascending.

- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Last 6 Months Rank
    - Email
    - Order Total