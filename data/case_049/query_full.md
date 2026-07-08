## Context

Using game results from the 2019/20 NBA season recorded up to a fixed cutoff timestamp, produce two conference-specific league tables (Western and Eastern). A separate team reference list provides each team’s conference assignment, while multiple game-result files provide the schedule and outcomes to date (with some future/unplayed games present but incomplete).

## Requirements

- Input the data.
  - Read the team reference file (`input_01.csv`) containing at least `Team` and `Conference`.
  - Read and combine the four game result files (`input_02.csv` through `input_05.csv`) into a single set of games.

- Identify which games count toward the standings.
  - Use games that have both `Date` and `Start (ET)` values to determine the game start time.
  - Construct a game start timestamp by combining `Date` and `Start (ET)` as an Eastern Time datetime, convert that timestamp to UTC, and include only games with a UTC start time strictly earlier than **2020-01-06 11:00:00 UTC**.
  - Include only completed games that have final scores recorded (future games that have not yet been played should not be counted).

- Determine outcomes and create a per-team game log (the basis for all aggregations).
  - For each counted game, determine the winner by comparing scores:
    - The home team wins if `PTS.1 > PTS`; otherwise the visitor team wins.
  - Expand each game into two records (one per participating team), with:
    - `Team` (the team name),
    - `Date` (the game start time in UTC, used for ordering),
    - `Win` (1 for a win, 0 for a loss),
    - `is_home` (1 if the team is the home team for that game, else 0),
    - `is_conf` (1 if both teams are in the same conference, else 0), determined by joining each game’s home and visitor teams to the team list to retrieve conferences.

- For each team, calculate the required standings fields (one output row per team).
  - **W**: total wins = sum of `Win`.
  - **L**: total losses = total games played − wins.
  - **Pct**: win percentage = `W / (W + L)`, rounded to **3 decimal places**.
  - **Home**: home record as a string `"W-L"` computed using only games where `is_home = 1`.
  - **Away**: away record as a string `"W-L"` computed using only games where `is_home = 0`.
  - **Conf**: conference record as a string `"W-L"` computed using only games where `is_conf = 1`.
  - **L10**: record over the most recently played up to 10 games as a string `"W-L"`, where “most recently played” is defined by the UTC game datetime ordering; if a team has fewer than 10 games, use all available games.
  - **Strk**: current streak based on the most recent games in chronological order:
    - If the team’s most recent game is a win, return `"Wn"`; if it is a loss, return `"Ln"`,
    - where `n` is the count of consecutive wins or losses ending at the most recent game.
  - If any of the split records (**Home**, **Away**, **Conf**, **L10**) are missing for a team because the team has no games in that subset, set the corresponding value to `"0-0"`.

- Rank teams within each conference and split into two conference outputs.
  - Join each team’s aggregated results to the team list to get its `Conference`.
  - Within each conference separately, compute **Rank** based on **Pct** in descending order, using a tie rule where teams with equal `Pct` receive the **maximum** rank position within their tied group (equivalently, Rank = the number of teams in the same conference with `Pct` greater than or equal to the team’s `Pct`).
  - Sort each conference table by `Rank` ascending.
  - Produce two outputs:
    - `output_01.csv`: Western Conference teams.
    - `output_02.csv`: Eastern Conference teams.
  - The **GB** (games behind) field is not required and must not be produced.

- Output the data.

## Output

- output_01.csv
  - 10 fields:
    - Rank
    - Team
    - W
    - L
    - Pct
    - Conf
    - Home
    - Away
    - L10
    - Strk

- output_02.csv
  - 10 fields:
    - Rank
    - Team
    - W
    - L
    - Pct
    - Conf
    - Home
    - Away
    - L10
    - Strk