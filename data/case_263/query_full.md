## Context
Prep Air want a What-If analysis to compare two loyalty reward systems (different flight-count tier bucket sizes) and understand their impact on total estimated annual program cost and how many customers would benefit at each tier.

## Requirements
- Input the data.
- Treat a customer as eligible for the loyalty scheme only if they have flown in the last year, defined as having **Last Date Flown on or after 21st February 2023** (inclusive). Exclude customers outside this rule from all downstream calculations.
- Produce results for **two tier-bucketing scenarios**:
  - bucket size **5** flights (to be reported in `output_01.csv`)
  - bucket size **10** flights (to be reported in `output_02.csv`)
- For each scenario, create a customer tier field named **Tier** based on flight count:
  - Compute the customer’s tier index as:  
    **Tier = floor(Number of Flights / bucket_size)**  
    (i.e., integer division).
- Estimate the average number of flights a customer takes per year:
  - Compute **YearsSpan = (year(Last Date Flown) − year(First Flight)) + 1**, with a minimum of 1 year.
  - Compute **AvgFlightsPerYear = Number of Flights / YearsSpan**.
- Filter the loyalty-tier rules dataset to the relevant scenario:
  - Keep only rows where **Tier Grouping** equals the scenario bucket size (5 or 10).
  - Derive a numeric tier level from the tier label by extracting its integer tier number (this defines the rule tier level used for benefit assignment).
- Expand benefits so that each benefit appears on its own row:
  - Split the **Benefits** field into individual benefit entries and create one row per (rule tier level, benefit).
  - Exclude empty benefits.
  - Deduplicate identical (rule tier level, benefit) pairs.
- Assign benefits to customers such that higher-tier customers inherit all lower-tier benefits:
  - For each customer, pair them with every rule tier level **less than or equal to** their customer Tier (i.e., customer Tier ≥ rule tier level).
  - Join these pairs to the benefit rows on the rule tier level so each customer receives all benefits from all qualifying tiers.
- Join to the costing dataset to attach a cost to each benefit:
  - Join on the **Benefit** name.
  - If a benefit has no matching cost record, exclude it from cost calculations (inner join behavior).
- Calculate the **Year Cost** contributed by each customer-benefit row:
  - If the benefit cost is specified **per flight**, compute:  
    **Year Cost = cost_per_flight × AvgFlightsPerYear**
  - Otherwise treat the cost as **yearly**, and compute:  
    **Year Cost = yearly_cost**
- Aggregate results at the customer-tier level (per scenario):
  - Group by **Tier** (the customer tier index).
  - **Number of Customers** = distinct count of customers in that Tier who have at least one costed benefit row included in the calculation.
  - **Year Cost** = sum of Year Cost across all included benefit rows for all customers in that Tier.
- Output the data for each scenario, with Tier sorted ascending.

## Output

- output_01.csv
  - 3 fields:
    - Tier
    - Year Cost
    - Number of Customers

- output_02.csv
  - 3 fields:
    - Tier
    - Year Cost
    - Number of Customers