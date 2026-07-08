## Context
You are given a single CSV extract from the 2019 PGA (men) and LPGA (women) golf tours containing the top players and their total prize money and events played. The goal is to compute a small set of comparable tour-level summary measures and present them side-by-side for PGA vs LPGA, including an explicit “LPGA minus PGA” difference for each measure.

## Requirements
- Input the data from `input_01.csv`.

- Assume each input row represents one player and includes, at minimum, these fields:
  - `PLAYER NAME`
  - `TOUR` (contains the tour identifier, expected to include PGA and LPGA)
  - `MONEY` (total prize money for that player)
  - `EVENTS` (number of events that player participated in)

- Compute the following player-level derived fields (used for later tour-level summaries):
  - **Money per event (per player)** = `MONEY / EVENTS`.
  - **Within-tour rank by prize money** (`tour_rank`): for each `TOUR`, rank players by `MONEY` descending using dense ranking (highest money = rank 1).
  - **Overall rank by prize money** (`overall_rank`): rank all players across both tours together by `MONEY` descending using dense ranking (highest money = rank 1).
  - **Ranking difference** (`rank_diff`) = `overall_rank - tour_rank`.
    - Note: This definition yields positive values when a player’s overall rank number is larger (i.e., worse) than their within-tour rank number after combining tours.

- Aggregate to the tour level (group by `TOUR`) to answer these questions:
  1. **Total Prize Money**: sum of `MONEY`.
  2. **Number of Players**: count of players (row count).
  3. **Number of Events**: sum of `EVENTS` across players.
  4. **Avg Money per Event**: mean of the per-player `MONEY / EVENTS` values (i.e., average of player-level money-per-event, not total money divided by total events).
  5. **Avg Difference in Ranking**: mean of `rank_diff`.

- Combine the answers into one dataset in a pivoted (wide) format:
  - One row per measure listed above.
  - Separate columns for the PGA and LPGA values.

- Create a final column **Difference between tours** defined as:
  - `LPGA - PGA` for each measure.
  - This is expected to be negative for measures where LPGA values are typically smaller than PGA values.

- Formatting rules for output values:
  - `Total Prize Money`, `Number of Players`, and `Number of Events` must be integers.
  - `Avg Money per Event` must be rounded to 0 decimals and output as an integer.
  - `Avg Difference in Ranking` must be rounded to 2 decimal places for both tour values, and the “Difference between tours” for this measure must also be rounded to 2 decimal places.

- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Measure
    - PGA
    - LPGA
    - Difference between tours