## Context

Build a single, analysis-ready dataset of monthly call center agent performance metrics for 2021 by combining (a) agent/leader/location reference data, (b) a calendar of month-start dates, (c) monthly performance extracts, and (d) goal thresholds expressed as additional columns. The final dataset must support reporting at the agent-by-month level, including goal attainment flags.

## Requirements

- Input the data
  - Read the agent/people file, leader file, location file, goals file, and dates file.
  - Read the 12 monthly metric files and treat each as the metrics for a specific month in 2021.
    - Map files to months by file name order: `input_01.csv` corresponds to January 2021, `input_02.csv` to February 2021, and so on through `input_12.csv` corresponding to December 2021.

- People, Location, Leader, and Dates:
  - Join the People, Location, and Leader data sets together:
    - Join People to Location using the location identifier (left join so every person is retained even if location details are missing).
    - Join the result to Leaders using People’s `Leader 1` to Leaders’ leader identifier (left join).
  - Remove the location id fields and the secondary leader id field from the working dataset (do not carry them into the final output).
  - Create last name, first name fields for the agent and the leader:
    - Create `Agent Name` as `"last_name, first_name"` from the People name fields.
    - Create `Leader Name` as `"last_name, first_name"` from the matched leader name fields.
  - Limit the dates to just 2021 and join those to the People, Location, Leader step:
    - Filter the Dates table to rows whose `Month Start Date` falls in calendar year 2021.
    - Format `Month Start Date` as exact text in `DD/MM/YYYY`.
    - Create the full agent-month frame by performing a cross join between the People/Location/Leader dataset and the filtered 2021 month-start dates so that every agent appears once for every month in 2021.
  - Keep the id, agent name, leader 1, leader name, month start date, join, and location field:
    - Retain only: `id`, `Agent Name`, `Leader 1`, `Leader Name`, `Month Start Date`, `Location` in the agent-month frame before adding metrics.

- Monthly Data
  - union the worksheets in the input step:
    - Vertically concatenate the 12 monthly metric inputs into a single metrics table (do not deduplicate).
  - merge the mismatched fields:
    - Standardize metric column naming so all months align to the same set of metric fields used in the final output (including ensuring a `Transfers` field exists for all months; months without transfer data must have `Transfers` as blank).
    - Apply the following field name mappings to unify column names across all monthly files:
      - `AgentID` → `id`
      - `Offered` → `Calls Offered`
      - `Not Answered` → `Calls Not Answered`
      - `Answered` → `Calls Answered`
      - Keep `Total Duration`, `Sentiment`, and `Transfers` as-is (if present).
    - Standardize the agent identifier field name to `id` for joining.
  - create a month start date:
    - For each monthly file, set `Month Start Date` to the first day of that month in 2021 and format it as `DD/MM/YYYY` (e.g., `01/01/2021` through `01/12/2021`).
  - remove the table names and file paths field:
    - Drop any source/lineage metadata fields (such as file name, table name, or file path) so they do not appear downstream.
  - join the data with the people - remember we need to show every agent for every month:
    - Left join the unioned monthly metrics onto the agent-month frame using keys `id` and `Month Start Date`, preserving all agent-month rows even when no metrics exist for that agent-month.
    - Missing-value handling for numeric metrics:
      - If an agent-month has no metrics at all (i.e., all core metric fields are missing), leave the metric fields blank for that row.
      - Otherwise (the agent-month has at least one metric present), fill missing values for the core metric fields with 0. Keep `Transfers` blank where it is not provided for a month.

- Goals
  - add the goals input to the flow:
    - Incorporate the goals concept into the final dataset as additional columns (one row remains one agent-month).
  - clean the goal data to have the goal name & numeric value:
    - Parse each goal string to extract the numeric threshold value:
      - For goals with format "X < Y" or "X <= Y", extract Y as the threshold value.
      - For goals with format "X >= Y" or "X > Y", extract Y as the threshold value.
      - For goals with format "X = Y" or "X == Y", extract Y as the threshold value.
      - Extract only the numeric portion, ignoring any percentage signs or other non-numeric characters unless they are part of a decimal number.
    - Specifically, extract from "Not Answered Percent < 5" the value 5, and from "Sentiment Score >= 0" the value 0.
    - Express the goal thresholds as numeric values in dedicated columns.
  - add the goals to the combined people & data step:
    - Add the following goal threshold columns (constants for all rows):
      - `Not Answered Percent < 5` = 5
      - `Sentiment Score >= 0` = 0
  - be sure that you aren't increasing the row count - the goals should be additional columns:
    - Do not create additional rows when adding goals; goals must be appended as columns to each existing agent-month row.

- Metrics & Met Goal Flags
  - create a calculation for the percent of offered that weren't answered (for each agent, each month):
    - `Not Answered Rate` = `Calls Not Answered` / `Calls Offered`.
    - Round `Not Answered Rate` to 3 decimal places using half-up rounding.
    - If the inputs needed for the rate are missing for an agent-month, keep `Not Answered Rate` blank for that row.
  - create a calculation for the average duration by agent (for each agent, each month):
    - `Agent Avg Duration` = `Total Duration` / `Calls Answered`.
    - If `Calls Answered` is missing, keep `Agent Avg Duration` blank.
    - If `Calls Answered` equals 0 (and is not missing), set `Agent Avg Duration` to 0.
    - Otherwise, round to the nearest whole number using half-up rounding.
  - create a calculation that determines if the sentiment score met the goal:
    - `Met Sentiment Goal` is `True` when `Sentiment` >= 0 and blank when `Sentiment` is blank; output as exact text (`True`/`False`).
  - create a calculation that determines if the not answered percent met the goal:
    - `Met Not Answered Rate` is `True` when `Not Answered Rate` < 0.05 and blank when `Not Answered Rate` is blank; output as exact text (`True`/`False`).

- Output the data
  - Produce a single CSV with exactly the required fields and names.
  - Ensure the output is sorted by `id` ascending and then `Month Start Date` descending (latest month first within each agent).

## Output

- output_01.csv
  - 18 fields:
    - id
    - Agent Name
    - Leader 1
    - Leader Name
    - Month Start Date
    - Location
    - Calls Answered
    - Calls Not Answered
    - Not Answered Rate
    - Met Not Answered Rate
    - Not Answered Percent < 5
    - Calls Offered
    - Total Duration
    - Agent Avg Duration
    - Transfers
    - Sentiment
    - Sentiment Score >= 0
    - Met Sentiment Goal
