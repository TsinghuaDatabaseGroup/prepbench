## Context

You have two case-management extracts (Business Unit A and Business Unit B) plus a lookup table that translates a numeric risk level into a textual risk rating. The goal is to combine both business units into a single view and, for each risk rating, report counts of cases across quarter-based classifications and status-based outcomes relative to the start of the quarter on 01/10/21 (1 Oct 2021). You will also compute how many cases are expected to carry over into the next quarter.

## Requirements

- Input the data.
  - Use **Business Unit A** from `input_01.csv`.
  - Use **Business Unit B** from `input_02.csv`.
  - Use the **risk lookup** from `input_03.csv`, which maps **Risk level** (numeric) to **Risk rating** (text).

- From the *Business Unit A* Input, create a **Date Lodged** field.
  - Construct **Date Lodged** as a date from the existing Year, Month, and Date components in the Business Unit A input.
  - Combine the three components in the format **YYYY-MM-DD** (e.g., Year=2021, Month=4, Date=17 becomes 2021-04-17).

- Parse the **Date Lodged** field from *Business Unit B* Input.
  - The **Date lodged** field in Business Unit B is in **d/m/y** format (day/month/year).
  - Parse dates accordingly (e.g., "1/10/2021" represents 1 October 2021, not 10 January 2021).

- Use the lookup table to update the risk rating (Business Unit A only).
  - Treat Business Unit A’s existing **Rating** as the numeric risk level and map it to the textual **Risk rating** using the lookup table (`Risk level` → `Risk rating`).
  - The resulting mapped text value must be stored in a unified **Rating** field used for subsequent grouping.

- Bring Business Unit A & B together.
  - Standardize both inputs to the same core fields before combining: **Ticket ID**, **Business Unit**, **Date Lodged**, **Status**, **Rating**.
  - Combine the two business units by appending rows (i.e., stacking/unioning), producing one consolidated case table at the grain of **one row per case (Ticket ID record)**.

- Classify each case in relation to the beginning of the quarter (01/10/21).
  - Define the quarter start as **1 Oct 2021**.
  - **Opening cases**: cases with **Date Lodged** strictly **before** 1 Oct 2021.
  - **New cases**: cases with **Date Lodged** **on or after** 1 Oct 2021 (the boundary date counts as “New cases”).

- In order to count cases closed/deferred within the quarter, call out cases with a completed or deferred status.
  - **Completed**: cases whose **Status** is `Completed` (count regardless of Date Lodged).
  - **Deferred**: cases whose **Status** is `Deferred` (count regardless of Date Lodged).

- For each **Rating**, count how many cases fall into each of the following five classifications:
  - `Completed`
  - `Deferred`
  - `New cases`
  - `Opening cases`
  - `Continuing`

- Create a field for cases which will carry over into the next quarter.
  - Compute **Continuing** per Rating as:
    - **Continuing = Opening cases + New cases − Completed − Deferred**
  - Ensure missing classification counts for a given Rating are treated as zero when calculating Continuing.

- Reshape the data to match the final output.
  - Produce a long (tidy) output with one row per **(Rating, Status)** combination and a numeric **Cases** count.
  - Status labels must match exactly: `Completed`, `Deferred`, `New cases`, `Opening cases`, `Continuing`.
  - Output ordering must be deterministic:
    - Order **Rating** as: `Medium`, `Low`, `High`, then any other Rating values after these.
    - Within each Rating, order **Status** as: `Completed`, `Deferred`, `New cases`, `Opening cases`, `Continuing`.

- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Status
    - Cases
    - Rating