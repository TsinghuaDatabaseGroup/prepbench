## Context
You are analyzing Liverpool FC match lineup information to understand (a) how goals scored and conceded vary by Liverpool formation and opposition formation, and (b) how often and how long each player was used in specific positions, including whether they were used outside their preferred position type.

There are three input sources:
1. **Position List (`input_01.csv`)**: Defines, for each formation, how lineup position numbers map to a position name and a position type.
2. **Player List (`input_02.csv`)**: A roster-style list where each entry embeds the player name and a preferred position-type code.
3. **Lineup Data (`input_03.csv`)**: Match-by-match lineups including formations, match results, and substitution information.

## Requirements
### Inputs and basic handling
- Input the three CSV files: `input_01.csv`, `input_02.csv`, and `input_03.csv`.
- When reading `input_03.csv`, do not assume the first row is the header. Identify the header row as the first row where the first column value is exactly `No.`; use that row as the column names and treat all subsequent rows as data rows.

### Output 1: Goals scored/conceded by formation matchup
Produce an aggregated table at the grain **(Liverpool Formation, Opposition Formation)**:
1. For each match row in `input_03.csv`, derive:
   - **Liverpool Goals** and **Opposition Goals** from the `Result` field (formatted like `X-Y`) and the `Location` field:
     - If `Location` is `H` (home), then Liverpool Goals = `X` and Opposition Goals = `Y`.
     - Otherwise (away/other), Liverpool Goals = `Y` and Opposition Goals = `X`.
   - If `Result` is missing or not parseable as `X-Y`, treat both Liverpool Goals and Opposition Goals as 0 for that match.
2. Group matches by `Formation` and `Oppo Form.` and compute:
   - **Games Played** = count of matches in the group (count rows using the match identifier column `No.`).
   - **Liverpool Goals** = sum of Liverpool Goals across matches in the group.
   - **Opposition Goals** = sum of Opposition Goals across matches in the group.
   - **Avg Goals Scored** = Liverpool Goals / Games Played.
   - **Avg Goals Conceded** = Opposition Goals / Games Played.
3. Ensure the output columns appear in the exact order specified. Also, the first column header must be exactly ` Formation` (with a single leading space before the word “Formation”).

### Output 2: Player position usage, minutes, and out-of-position counts
Create player-position statistics by combining all three inputs, treating substitutions as direct replacements in the same position (i.e., the formation does not change and the substituted-on player inherits the substituted-off player’s position).

#### Step 1 — Clean the Player List into player name + preferred position type
- From `input_02.csv`, use the `Player Name` field to extract:
  - **Player Name** (the human-readable name portion).
  - **Preferred Position Type**, derived from the embedded single-letter code:
    - `G` = Goalkeeper
    - `D` = Defender
    - `M` = Midfielder
    - `A` = Attacker
- Keep only rows where both the player name and the preferred position type can be extracted; ignore non-conforming rows.
- This cleaned table is used only to (a) standardize player names and (b) provide each player’s preferred position type for out-of-position calculations.

#### Step 2 — Build a formation-position mapping
- From `input_01.csv`, build a mapping keyed by:
  - (`Formation Name`, `Player Position`)
- The mapping returns:
  - `Position Name`
  - `Position Type`

#### Step 3 — Interpret each match lineup (starters + substitutions) into minutes by player and position
For each match in `input_03.csv`:
1. Assume match length is **90 minutes**.
2. **Starters (positions 1–11):**
   - For each position number `p` from 1 to 11, read the value from the column named exactly as the number (e.g., `"1"`, `"2"`, …, `"11"`).
   - If a player name is present and the formation-position mapping contains (`Formation`, `p`), assign that player a playing segment from minute 0 to minute 90 for the mapped `Position Name` and `Position Type`.
3. **Name standardization for lineup player strings:**
   - If the lineup string exactly matches a cleaned player name, use that name.
   - Otherwise, if it matches as a case-insensitive substring of a cleaned player name, use the first such cleaned player name encountered.
   - If no match is found, keep the original lineup string as the player name.
4. **Substitutions (`sub1`, `sub2`, `sub3`):**
   - Locate columns named `sub1`, `sub2`, and `sub3` (if present). For each such `subX` column, interpret the substitution information using column adjacency:
     - The value in `subX` is `off_pos` (the position number being replaced).
     - The next column (`subX` + 1) contains `on_no` (a number that points to the column name holding the substitute player’s name in the lineup row).
     - The next column (`subX` + 2) contains `minute` (the substitution minute).
   - Only process a substitution if `off_pos`, `on_no`, and `minute` are all present and numeric.
   - Apply the “direct replacement” rule:
     - The substituted-off player’s active segment in that position ends at `min(minute, 90)` (update only the segment that currently ends at 90).
     - The substituted-on player starts a segment in the *same mapped position* at `minute` and ends at 90.
5. Convert playing segments into per-match records with one row per **(Match, Player Name, Position Name, Position Type)**:
   - **Mins Played** = sum over all that player’s segments for that position in the match, computed as `(end - start)` per segment, bounded below by 0.
   - Round total minutes to the nearest integer and output as an integer.

#### Step 4 — Aggregate to final Output 2 statistics
1. Left-join the per-match records to the cleaned player list on `Player Name` to attach `Preferred Position Type` (may be missing).
2. Aggregate to the grain **(Player Name, Position Type, Position Name)**:
   - **No Times Played** = count of match records in the group (count `Match No` rows).
   - **Mins Played** = sum of `Mins Played` in the group.
3. Compute **Games OoP** (out of position) as a *player-level* value:
   - A match counts as “out of position” for a player if, in that match record, `Position Type` ≠ `Preferred Position Type`.
   - For each player, compute the number of distinct matches where they were out of position at least once.
   - Assign this same per-player total to **Games OoP** for every row of that player in the final output.
4. Formatting requirement: append a single trailing space character to every `Player Name` value in `output_02.csv`.
5. Ensure columns appear exactly in the order specified in the Output section.

## Output

- output_01.csv
  - 7 fields:
    - Formation
    - Oppo Form.
    - Games Played
    - Liverpool Goals
    - Avg Goals Scored
    - Opposition Goals
    - Avg Goals Conceded

- output_02.csv
  - 6 fields:
    - Player Name
    - Position Type
    - Position Name
    - No Times Played
    - Mins Played
    - Games OoP