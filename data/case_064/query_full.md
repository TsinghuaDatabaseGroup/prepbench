## Context

You are given a structured spreadsheet of Liverpool match line-ups and substitution events. Each match record contains (a) match details, (b) the 18-player matchday squad split into Starting XI and named substitutes, and (c) up to three substitutions with the “player off position”, “player on position”, and the minute of the substitution. The goal is to calculate, for each player across all matches in the file, how often they were in the squad, how many appearances they made, and how many total minutes they played, then derive minutes per appearance.

## Requirements

- Input the data.
  - Read `inputs/input_01.csv` as a raw grid (no pre-supplied header row). Treat each match as one row in this grid.
  - Process only rows that represent actual matches.
  - **Exclude** rows where the first cell contains "Match Details" or "No.".
  - Identify valid match rows as those where the first cell is present (non-empty) and does not match the excluded headers. Ignore any other rows.

- Update/standardize headers conceptually for the three main sections so the data can be addressed consistently (this should be done programmatically, not by manually renaming each individual column):
  - Match Details block (not used in calculations other than to identify valid match rows).
  - Starting XI block: 11 player-name cells representing positions 1–11 for Liverpool’s starters.
  - Substitution Information block: up to 3 substitutions, each represented by three fields following the pattern described in the prompt:
    - `SubX` = Substitute Off (the position number of the player who leaves the field)
    - `SubX 1` = Substitute On (the position number of the player who enters the field)
    - `SubX 2` = Time of Substitute (the minute in the match when the substitution occurred)
  - Substitutes bench block: 7 player-name cells representing positions 12–18 for Liverpool’s named substitutes.

- For each match, derive who was substituted on/off, which substitution number it was (1/2/3), and the substitution minute, and use those events to compute minutes played and appearances per player for that match, using these rules:
  - “In squad”:
    - Every player listed in the Starting XI or the Substitutes bench for a match counts as being “in the squad” for that match (add 1 to their squad count).
  - “Appearances”:
    - Every Starting XI player is counted as having made 1 appearance for that match.
    - A named substitute is counted as having made 1 appearance only if they are recorded as coming on in a substitution event; otherwise 0 for that match.
  - “Minutes played” (per match):
    - Assume a 90-minute match and do not account for stoppage/additional time.
    - Starting XI players:
      - Default minutes played is 90.
      - If a starter is substituted off, set their minutes played to the substitution minute (i.e., they play from minute 0 up to the stated minute).
    - Named substitutes:
      - Default minutes played is 0.
      - If a substitute is substituted on at minute `t`, set their minutes played to `max(0, 90 - t)`.
      - If a player is substituted on in the 90th minute, count this as 1 appearance but 0 minutes played.
  - If multiple substitutions occur, process them as follows:
    - **Processing order**: Sort all substitution events by their substitution minute (ascending). Process substitutions in chronological order, regardless of whether they are labeled as sub1, sub2, or sub3 in the input data.
    - **Position matching rules**: For each substitution event:
      - The "off" player is always determined from the Starting XI position numbers (1–11) at the start of the match. Only players who started in the Starting XI can be substituted off. Once a substitute enters the field, they cannot be substituted off in a later substitution event.
      - The "on" player is always determined from the Substitutes bench position numbers (12–18) at the start of the match.
    - **Tie-breaking for same-minute substitutions**: If multiple substitutions occur at the exact same minute:
      - Process them in the order they appear in the input data (sub1, then sub2, then sub3).
      - For each substitution at minute `t`, the player coming off plays until minute `t` (inclusive), and the player coming on plays from minute `t` to minute 90 (i.e., `max(0, 90 - t)` minutes).
    - Use the substitution minute associated with each event for the calculations above.

- After processing all matches, aggregate to the player level (one output row per player):
  - `In Squad` = total number of matches where the player appeared in either Starting XI or Substitutes bench.
  - `Appearances` = total appearances across all matches (starters always count; substitutes only count when they came on).
  - `Mins Played` = total minutes played across all matches (sum of per-match minutes as defined above).
  - `Mins per Game` = `Mins Played / Appearances` for players with at least one appearance; otherwise 0.

- Output the data:
  - Produce a single CSV with one row per player.
  - Sort the final output by `In Squad` descending, then by `Player Name` ascending.

## Output

- output_01.csv
  - 5 fields:
    - In Squad
    - Player Name
    - Mins Played
    - Appearances
    - Mins per Game