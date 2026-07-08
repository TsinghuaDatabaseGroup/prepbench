## Context

You are preparing a cleaned, analysis-ready dataset for a single NBA team’s game schedule (the San Antonio Spurs), sourced from ESPN-style schedule exports. Each game record includes three “Hi-” statistics:

- Hi Points: the single player who scored the most points in that game (and how many)
- Hi Rebounds: the single player with the most rebounds in that game (and how many)
- Hi Assists: the single player with the most assists in that game (and how many)

The goal is to reshape these fields into separate player and numeric value columns, derive game attributes (home/away and win/loss), and compute the running season record (“W-L”) over time so the output can be used to answer profiling questions about player frequency in wins/losses and combinations of leaders.

## Requirements

- Input the data from `input_01.csv`. Each row represents one Spurs game.
- Fix some date issues by ensuring the `DATE` field is parsed as a true date/datetime value that can be chronologically ordered.
- Split the three “Hi-” categories into separate player and value fields:
  - For each of `HI POINTS`, `HI REBOUNDS`, and `HI ASSISTS`, split the text into:
    - `... - Player`: everything before the final space
    - `... - Value`: the token after the final space, converted to an integer
- Determine whether each game was played by the Spurs: Home or Away:
  - Use the `OPPONENT` field: if it begins with the prefix `vs` then set `Home or Away` = `Home`; otherwise set it to `Away`.
- Create a cleaned opponent name:
  - Create `Opponent (clean)` by removing any leading `vs` or `@` prefix (and any immediately following spaces) from `OPPONENT`, leaving only the opponent name.
- Determine whether the Spurs won or lost each game:
  - Derive `Win or Loss` from the first character of `RESULT` (e.g., `W` or `L`).
- Compute the cumulative running record `W-L`:
  - Order games by the true chronological `DATE` (ascending).
  - Compute cumulative wins as the running total of games where `Win or Loss` = `W`.
  - Compute cumulative losses as the running total of games where `Win or Loss` = `L`.
  - Format `W-L` as `<cumulative_wins>-<cumulative_losses>` for each game.
- Create `True Date` as a formatted date string from `DATE` using `dd/mm/YYYY` (day/month/four-digit-year).
- Get rid of unrequired columns by keeping exactly the 13 fields listed in the Output section (and no others).
- Output the data to `output_01.csv`:
  - Ensure the final dataset is sorted in ascending order by `True Date`.

## Output

- output_01.csv
  - 13 fields:
    - Opponent (clean)
    - HI ASSISTS - Player
    - HI ASSISTS - Value
    - HI REBOUNDS - Player
    - HI REBOUNDS - Value
    - HI POINTS - Player
    - HI POINTS - Value
    - Win or Loss
    - Home or Away
    - True Date
    - OPPONENT
    - RESULT
    - W-L