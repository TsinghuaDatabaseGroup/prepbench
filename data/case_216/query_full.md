## Context
You are preparing a simplified trading dataset that supports a rolling (moving) average calculation over sequential trades within each Sector. Because moving calculations are not assumed to be available natively in the preparation tool, the goal is to build the logic into the prepared output so end users can work with a clean, analysis-ready table.

## Requirements
- Input the data.
  - Read and append (union) all monthly trade files provided as `input_*.csv` into a single dataset.
  - Treat the numeric portion of each file name (e.g., `input_01`, `input_02`, …) as the chronological month order of the file.

- Create a **Trade Order** field that shows the sequence number of each trade within each **Sector**.
  - First establish the global trade sequence by sorting all rows by:
    1) monthly file order (from the file name), then
    2) `id` ascending within each file.
  - Then, within each `Sector`, assign `Trade Order` as a 1-based running count following that global sequence (i.e., the first observed trade in a sector is 1, the next is 2, etc.).

- Remove all data fields except:
  - Trade Order
  - Sector
  - Purchase Price

- Create a Parameter to allow the user to select the rolling number of trades to be incorporated into the moving average.
  - Use a rolling window size of **3 trades** for the produced output (i.e., consistent with the stated default of 3).

- Create a data set that records the previous 2 trades (where applicable) as well as that Trade Order record.
  - Implement this by computing a rolling calculation per `Sector` that, for each trade, incorporates the current trade and up to the two immediately preceding trades in that sector’s `Trade Order` sequence.

- Workout the **Rolling Average Purchase Price** for each **Trade Order** in each **Sector**.
  - For each `Sector`, compute the rolling mean of `Purchase Price` over the last 3 trades including the current trade.
  - For the first and second trades in a sector, compute the mean over the available trades so far (window grows up to 3).
  - Round the resulting rolling average to **2 decimal places**.

- Filter the data for the last 100 trades for each Sector.
  - Only include sectors that have **at least 100 total trades**.
  - For each included sector, keep only the **most recent 100 trades** by `Trade Order` (i.e., the highest `Trade Order` values).

- Create the **Previous Trades** field to show the oldest trade (1) through to the latest trade (100).
  - Within each sector’s retained last-100 subset, order trades by `Trade Order` ascending and assign `Previous Trades` as a 1-based sequence:
    - `Previous Trades = 1` is the oldest trade within the retained subset
    - `Previous Trades = 100` is the most recent trade within the retained subset

- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Previous Trades
    - Trade Order
    - Sector
    - Rolling Avg. Purchase Price