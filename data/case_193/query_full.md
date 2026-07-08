## Context

You are working with sports player training sessions where athletes do not necessarily complete the same session type every day. To avoid misleading day-to-day averages caused by gaps, you need to scaffold the data so that every (non-weekend) day is represented for each player and session type, carrying forward the most recent session score until the next session occurs.

## Requirements

- Input the data.
- Treat each record as an observed training session for a given `Player` and `Session` on a specific `Date`, with an associated `Score`.
- For each `Player` and `Session` combination, determine the date of the *next* session by ordering that player/session’s sessions by `Date` and, for each session, identifying the subsequent session date within the same player/session.
  - This “next session date” is used to define the range of days for which the current session’s score should apply.
- For the most recent training session *within a given player/session*, set its “next session date” to the **maximum `Date` found anywhere in the dataset** (the global maximum date across all players/sessions).
- Scaffold (expand) the data so the final dataset has one row per **Player × Session × calendar day** over the following ranges:
  - For a non-final session: generate daily rows from the session’s `Date` **through the day before** the next session date (inclusive of the session date; exclusive of the next session date).
  - For the final session (per player/session): generate daily rows from the session’s `Date` **through the global maximum date** (inclusive of both endpoints).
  - Ensure the scaffold does not create duplicate rows for the same Player/Session/Day; each output row must uniquely represent one player, one session type, and one date.
- Create a `Flag` field indicating whether the score comes from:
  - `Actual` when the row’s date equals the date of the underlying session providing the score, or
  - `Carried over` when the row’s date is after that session date and the score is being carried forward.
- Exclude all weekends from the final dataset:
  - Remove any rows where the date is a Saturday or Sunday (including dates that would otherwise be flagged as `Actual`).
- Format `Session Date` as `DD/MM/YYYY`.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Flag
    - Player
    - Session
    - Score
    - Session Date