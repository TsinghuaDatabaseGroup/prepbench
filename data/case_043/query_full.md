## Context

You have monthly sales figures by store and quarterly target values by store/region. The goal is to roll monthly sales up to quarterly totals, compare each store’s quarterly sales to its quarterly target, and attach a standardized performance label and action description based on the percent-to-target result.

## Requirements

- Input the data:
  - Read monthly store sales from `input_01.csv`.
  - Read quarterly store targets (with region) from `input_02.csv`.
  - Read the actions mapping file from `input_03.csv` (note: the action assignment is rule-based as specified below, not a lookup from this file).
- Remove any non-store sales data:
  - Exclude rows in the sales input where `Store` equals `Total`.
- Form a date to help with your quarterly calculations:
  - Reshape the sales data from wide monthly columns into a long format with fields `Store`, `Month_Year`, and `Sales`.
  - Derive `Month` by extracting the month number from `Month_Year` (e.g., the “Month N …” portion) and converting it to an integer.
  - Derive `Quarter` as: `Quarter = ((Month - 1) // 3) + 1`, producing quarters 1–4.
- Determine Store Quarterly Sales:
  - Aggregate to one row per `Store` and `Quarter`, summing `Sales` across the months in that quarter.
- Join on Store Quarterly Targets:
  - Reshape the targets data from wide quarter columns into a long format with fields `Store`, `Region`, `Quarter`, and `Target Value`, where:
    - `Store` comes from the `Location` column renamed to `Store`.
    - `Quarter` is converted from values like `Q1`–`Q4` into integers `1`–`4`.
  - Join quarterly sales to quarterly targets using an inner join on `Store` and `Quarter` (keep only store-quarter combinations present in both sources).
- Determine Store variance to Target - actual as well as percentage difference:
  - Compute `Variance to Target = Sales - Target Value`.
  - Compute `Variance to Target % = int((Sales / Target Value) * 100)`, where `int(...)` truncates to an integer.
- Match Action Description to Variance %:
  - Create `Target` and `Actions` from `Variance to Target %` using these rules (evaluated top-down):
    - If `Variance to Target %` > 150:
      - `Target` = `Above`
      - `Actions` = `Smashing it. Share with all other stores what you are doing. Can you mentor the underachieving stores?`
    - Else if `Variance to Target %` > 125:
      - `Target` = `Above`
      - `Actions` = `Brilliant work. Share ideas with other stores. Are you ready for next year?`
    - Else if `Variance to Target %` > 100:
      - `Target` = `Above`
      - `Actions` = `Doing well. Try to share ideas with other stores but try to learn from others to stay ahead`
    - Else if `Variance to Target %` == 100:
      - `Target` = `Meets`
      - `Actions` = `Nice work. Thank you for your hard work. What can you do to exceed you target? Talk to 3 high performing stores`
    - Else if `Variance to Target %` >= 75:
      - `Target` = `Below`
      - `Actions` = `Close but not quite there. Please create an assessment on blockers to hitting your target and learn from those that did.`
    - Else if `Variance to Target %` >= 50:
      - `Target` = `Below`
      - `Actions` = `This might have been poor targetting by Head Office. Please create an assessment on blockers as we will be in touch.`
    - Else:
      - `Target` = `Below`
      - `Actions` = `What went wrong? Create a detailed assessment on the blockers and we will schedule time to discuss in early January`
- Output the data:
  - Produce one output row per `Store` and `Quarter` after the join and calculations.
  - Ensure the output contains exactly the fields listed below, with these names.

## Output

- output_01.csv
  - 9 fields:
    - Variance to Target
    - Variance to Target %
    - Target Value
    - Sales
    - Store
    - Quarter
    - Region
    - Target
    - Actions