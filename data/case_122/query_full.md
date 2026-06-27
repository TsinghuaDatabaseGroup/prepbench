## Context
Prep Air wants to evaluate its Net Promoter Score (NPS) in the context of other airlines’ customer feedback. NPS is based on customers’ likelihood to recommend an airline on a 0–10 scale, and is calculated as the percentage of promoters minus the percentage of detractors (yielding a score between -100 and +100). To understand whether Prep Air’s NPS is above or below the broader market, compute a Z-Score that standardises each airline’s NPS against the overall distribution.

## Requirements
- Input the data.
- Combine the Prep Air responses with the other airlines’ responses into a single dataset (append/union the two inputs so all response rows are included).
- Exclude any airlines that have fewer than 50 customer responses in the combined dataset (use the total count of response rows per Airline).
- Classify each customer response to the recommendation question into exactly one category based on the 0–10 score:
  - 0–6 (inclusive) = Detractors
  - 7–8 (inclusive) = Passive
  - 9–10 (inclusive) = Promoters
- Calculate NPS per airline, where each airline’s NPS is computed from its own responses:
  - Compute % Promoters = (Promoter responses / total responses) * 100.
  - Compute % Detractors = (Detractor responses / total responses) * 100.
  - Round both percentages down to the nearest whole number (i.e., take the floor of each percentage).
  - NPS = floor(% Promoters) − floor(% Detractors).
- Using the set of NPS values across all remaining airlines (after the 50-response exclusion), calculate:
  - The mean (average) NPS.
  - The standard deviation of NPS using the sample standard deviation (ddof = 1).
- For each airline, compute its Z-Score as:
  - Z-Score = (NPS − mean NPS) / (sample standard deviation of NPS)
  - Round Z-Score to 2 decimal places.
- Filter the results to only the airline named exactly “Prep Air”, keeping its NPS and Z-Score.
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Airline
    - NPS
    - Z-Score