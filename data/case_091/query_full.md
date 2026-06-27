## Context

Prep Air is a new airline that wants to estimate what full-year revenue and target performance would have looked like using only the first quarter’s actuals, adjusted for seasonal demand patterns that vary by destination country. Seasonal projection factors are provided per destination country and must be applied to Q1 performance to estimate Q2–Q4, then rolled up into a full-year view by route.

## Requirements

- Input the data.
- Treat the base period as Q1 and calculate Q1 totals at the route level:
  - Define a “route” as the pair of airport codes: `Origin` and `Destination`.
  - From the sales dataset, compute **Q1 Sales Value** per route as the sum of `Value` grouped by (`Origin`, `Destination`).
  - From the targets dataset, compute **Q1 Target Value** per route as the sum of `Value` grouped by (`Origin`, `Destination`).
  - Combine Q1 Sales and Q1 Target using an inner join on (`Origin`, `Destination`) so only routes present in both are retained.
- Make the “Quarterly Projections for Destinations” dataset usable by converting percentage-change text into numeric quarterly multipliers per destination country:
  - For each destination `Country`, create quarterly projection multipliers:
    - Q1 multiplier = 1.0
    - Q2 multiplier = 1 + (Q1–Q2 change % / 100)
    - Q3 multiplier = 1 + (Q1–Q3 change % / 100)
    - Q4 multiplier = 1 + (Q1–Q4 change % / 100)
  - Interpret each change as a signed percentage (positive increases, negative decreases). If a change value is missing, treat it as 0% (multiplier 1.0).
  - Reshape the projections so there is one row per (`Destination Country`, `Quarter`) with a single field `Projection` containing the multiplier.
- Attach country information to each route using the airports reference:
  - Join the airports table to the route data twice:
    - Map `Origin` to `Origin Country` by joining `Origin` to `Airport Code` (left join; retain all routes).
    - Map `Destination` to `Destination Country` by joining `Destination` to `Airport Code` (left join; retain all routes).
- Apply the destination-country projections to Q1 Sales Value and Q1 Target Value:
  - Join the route-level Q1 data to the long projections on `Destination Country` using an inner join (routes without a matching destination-country projection are excluded).
  - For each resulting (`Origin`, `Destination`, `Quarter`) row compute:
    - `Projected Value` = `Q1 Value` × `Projection`
    - `Projected Target` = `Q1 Target` × `Projection`
- Produce a full-year (Q1–Q4) total by route factoring in the projections:
  - Sum `Projected Value` and `Projected Target` across all four quarters for each route grouped by:
    - `Origin`, `Origin Country`, `Destination`, `Destination Country`
  - Rename the full-year totals to:
    - `Value` (full-year projected sales)
    - `Target Value` (full-year projected target)
  - Compute `Variance to Target` = `Value` − `Target Value`.
  - Round `Value`, `Target Value`, and `Variance to Target` to 2 decimal places.
- Output the data exactly as specified.

## Output

- output_01.csv
  - 7 fields:
    - Origin
    - Origin Country
    - Destination
    - Destination Country
    - Value
    - Target Value
    - Variance to Target