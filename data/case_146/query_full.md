## Context

You are preparing a player-metrics dataset for a Pizza Plot / Coxcomb chart. The goal is to attach player names to poker event records, compute per-player career and performance statistics, and then produce a long-form output that contains (a) the raw metric values and (b) a scaled (rank-based) value per metric suitable for charting.

## Requirements

- Input the data.
  - Read `input_01.csv` as the players table (must include `player_id`, `name`, and `all_time_money_usd`).
  - Read `input_02.csv` as the events table (must include `player_id`, `event_date`, `player_place`, `prize_usd`, and `event_country`).

- Add the player names to their poker events / player-level results.
  - Treat `player_id` as the key that links events to players.
  - Player-level metrics must ultimately be associated with the player `name`.

- Create a column to count when the player finished 1st in an event.
  - Create `win` on the events table: `win = 1` when `player_place` indicates a 1st-place finish, otherwise `0`.
  - **Ambiguity resolution for `player_place`**: The `player_place` field contains ordinal strings (e.g., "1st", "2nd", "3rd", "22nd", "211th"). To determine a 1st-place finish, check if `player_place` equals the string `"1st"` (case-sensitive). If `player_place == "1st"`, then `win = 1`; otherwise `win = 0`.

- Replace any nulls in `prize_usd` with zero.
  - Ensure `prize_usd` is numeric; if missing or non-numeric, treat it as `0`.

- Find the dates of the players first and last events.
  - Parse `event_date` as a date/datetime.
  - For each player, compute:
    - `min_date` = earliest non-null `event_date`
    - `max_date` = latest non-null `event_date`

- Use these dates to calculate the length of poker career in years (with decimals).
  - For each player:  
    `career_length = (max_date - min_date) in days / 365.25`
  - If either date is missing (or the player has no valid event dates), set `career_length = 0.0`.

- Create an aggregated view to find the following player stats (per `player_id`):
  - Number of events they’ve taken part in: `number_of_events` = count of that player’s event rows.
  - Total prize money:
    - Use the players table value `all_time_money_usd` as the authoritative total, and rename it to `total_prize_money` in the player stats output.
    - (You may also compute the sum of `prize_usd` across events internally, but the required “Total prize money” metric used for output must be `all_time_money_usd`.)
  - Their biggest win: `biggest_win` = maximum `prize_usd` across that player’s events (0.0 if no events).
  - The percentage of events they’ve won: `percent_won` = (sum of `win`) / `number_of_events` (0.0 if `number_of_events` is 0).
  - The distinct count of the country played in: `countries_visited` = distinct count of `event_country` (excluding nulls).
  - Their length of career: `career_length` as defined above.

- Ensure all players from the players table are retained in the final player stats (even if they have zero events).
  - Join the aggregated event metrics to the players table using a right join on `player_id` (i.e., keep every player in `input_01.csv`).
  - For players with no matching events, fill the event-derived metrics with zeros:
    - `number_of_events = 0`
    - `biggest_win = 0.0`
    - `percent_won = 0.0`
    - `countries_visited = 0`
    - `career_length = 0.0`

- Reduce the data to the required metric set for visualization.
  - Work with exactly these metrics (and this metric naming) for the visualization layer:
    - `number_of_events`
    - `total_prize_money`
    - `biggest_win`
    - `percent_won`
    - `countries_visited`
    - `career_length`

**Creating a Pizza Plot / Coxcomb chart output:**
- Using the player stats to create two pivot tables (conceptually):
  - a pivot of the raw values
  - a pivot of the values ranked from 1-100, with 100 representing the highest value
  - Note: we're using a ranking method that averages ties, pay particular attention to countries visited!
- Implement the above by producing a long-form dataset with one row per `(name, metric)` containing:
  - `raw_value`: the metric’s raw value for that player.
  - `scaled_value`: the within-metric rank across all players, using average ranking for ties and ascending order (higher raw values receive higher ranks).
  - Special rule for `percent_won`: if a player’s `raw_value` is missing for this metric, treat it as receiving the maximum (highest) rank for `scaled_value`.
    - **Clarification on when `percent_won` is considered missing**: If a player has event records (N > 0 events) but never finished 1st (sum of `win` is 0), their `percent_won` should be set to `NaN` (missing), not `0.0`. The formula `0/N = 0.0` is mathematically correct, but semantically this case should be treated as "no meaningful win percentage data" rather than "zero win rate". This ensures such players receive the maximum rank per the special rule above.
- Join the pivots together.
  - The final output must include both `raw_value` and `scaled_value` for each `(name, metric)`.
- Output the data.
  - Output grain: one row per player name per metric.
  - Order the result by `name` ascending, and within each `name` order metrics as:
    1) `number_of_events`
    2) `total_prize_money`
    3) `biggest_win`
    4) `percent_won`
    5) `countries_visited`
    6) `career_length`

## Output

- output_01.csv
  - 4 fields:
    - name
    - metric
    - raw_value
    - scaled_value