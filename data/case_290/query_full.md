## Context

You are given a raw CSV export where each physical row can contain up to two Premier League match text blocks (one per column), along with intermittent “Matchday … of 38” announcer text. The goal is to convert these semi-structured text blocks into a clean, match-level dataset with one row per match, including the match date, teams, scores, the matchday number, and a “source row number” that reflects the original row position for reuse in a later step.

## Requirements

- Input the data from `input_01.csv`. Treat it as a two-column file with no header row; both columns contain text.
- Add a “Source Row Number” that reflects the physical row position in the source data:
  - Maintain a counter that increments once per physical source row and is assigned to any match records parsed from that row (both columns share the same source row number).
  - If the very first physical row contains no match information (i.e., neither column includes match results text), do not increment the counter for that first row; otherwise, count it as row 1. All subsequent physical rows increment the counter by 1.
- Create a "Matchday" column indicating which matchday (gameweek) each match occurred in:
  - Detect matchday announcer text in either input column in the form "Matchday X of 38".
    - Format matching: The pattern should match "Matchday" followed by a number, followed by "of 38". Trailing punctuation (such as commas) should be ignored when matching this pattern. For example, both "Matchday 1 of 38" and "Matchday 1 of 38," should be recognized as valid matchday announcements.
    - Extract the number `X` from the matched pattern and use it as the matchday value.
  - Update the current matchday to `X` when such an announcer is encountered; this matchday then applies to subsequent match blocks until updated again.
  - Do not output a record for announcer-only text; only apply it as context for following matches.
- Remove any rows/cells that do not contain game information by only emitting output records when a match block can be parsed into all required fields (date, teams, scores) and a matchday has been established.
- It is acceptable (and often easier) to combine the two input columns’ match text into a single standardized representation for parsing, but the final output must be match-level (one row per match), not row-level.
- Replace the new row character (`\n`) with a different character(s) (I use two pipe characters: `||`).
  - `\n` is recognised as `char(10)` by Prep Builder
  - This is an intermediate transformation to make parsing predictable; it should not change the final output fields or formats.
- For each match text block (each cell in either input column), parse and output the following fields:
  - **Date**: Identify the first line/token within the block that can be parsed as a date; output it formatted as `DD/MM/YYYY`.
    - Date format: The input date format is "DD MMM YY" (e.g., "11 Aug 23"). Parse this format and convert to "DD/MM/YYYY" (e.g., "11/08/2023"). If other date formats are encountered, they should be parsed according to standard date parsing rules, but the primary format in the data is "DD MMM YY".
  - **Home Score / Away Score**: After the date, identify the first integer token as Home Score and the next integer token as Away Score.
    - Integer token identification: When searching for score integers after the date, skip any integers that are part of:
      - Date components (e.g., the "23" in "11 Aug 23" should not be considered as a score)
      - Time stamps or duration strings (e.g., numbers in "3:09" or "2 minutes and 9 seconds")
      - Other non-score numeric patterns
    - The first standalone integer token encountered after the date line (excluding date components and time-related numbers) should be treated as Home Score, and the next standalone integer token as Away Score.
  - **Home Team / Away Team**: After Home Score, take the next token as Home Team; after Away Score, take the next token as Away Team. If a team name immediately repeats on the following token, skip the duplicate.
  - Ignore non-match noise lines within a cell (e.g., standalone "FT", recap/highlights lines, or arrow/bullet-like lines) so they do not interfere with parsing.
- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Away Score
    - Away Team
    - Home Score
    - Home Team
    - Matchday
    - Source Row Number
    - Date