## Context
Data Source Bank (DSB) has quarterly target totals for transaction values split by channel (online vs in-person). Your task is to summarize DSB transactions by quarter and channel, align those actuals to the corresponding quarterly targets, and compute the variance versus target.

## Requirements
- Input the data.

- Use **inputs/input_01.csv** as the transactions dataset and **inputs/input_02.csv** as the targets dataset.

- For the transactions data:
  - Filter to DSB transactions only: keep rows where **Transaction Code** contains the string **"DSB"**.
  - Recode **Online or In-Person** from numeric codes to labels:
    - `1` → `Online`
    - `2` → `In-Person`
  - Convert **Transaction Date** into a numeric **Quarter** (1–4) based on the calendar quarter of the transaction date.
  - Aggregate to one row per **Online or In-Person** and **Quarter** by summing **Value** within each group. This aggregated sum is the actual **Value** for that quarter/channel.

- For the targets data:
  - Reshape (pivot) the quarterly target columns into a longer format so there is one row per **Online or In-Person** and **Quarter**, with the target amount in **Quarterly Targets**.
    - Treat the quarter columns as `Q1`, `Q2`, `Q3`, `Q4`.
  - Remove the leading `'Q'` from the quarter label and convert **Quarter** to a numeric field (1–4).
  - Keep only the fields needed to join and report: **Online or In-Person**, **Quarter**, and **Quarterly Targets**.

- Join the aggregated transactions to the reshaped targets:
  - Join on **Online or In-Person** and **Quarter**.
  - Use an inner join so the output contains only quarter/channel combinations present in both datasets.

- Remove unnecessary fields so the final dataset contains only the required output columns.

- Calculate **Variance to Target** for each output row as:
  - **Variance to Target = Value − Quarterly Targets**

- Ensure the output is at the grain of **one row per Online or In-Person per Quarter**, and sort the final results by:
  - **Online or In-Person** descending, then **Quarter** ascending.

- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Online or In-Person
    - Quarter
    - Value
    - Quarterly Targets
    - Variance to Target