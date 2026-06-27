## Context
We are preparing karaoke activity data into discrete 60-minute sessions, recognizing that customers may not perform entire songs. A session is inferred from gaps between songs, and customers are associated to sessions based on how close their entry time is to the session start, assuming customers arrive no more than 10 minutes before their session begins.

## Requirements
- Input the data:
  - Load the songs log from `input_01.csv`, including at minimum the fields `Date`, `Artist`, and `Song`.
  - Load the customer entry log from `input_02.csv`, including at minimum the fields `Customer ID` and `Entry Time`.
  - Parse `Date` and `Entry Time` as datetimes.

- Calculate the time between songs:
  - Sort all song records by `Date` ascending.
  - For each song, compute the elapsed time in minutes from the immediately previous song in this sorted order.

- If the time between songs is greater than (or equal to) 59 minutes, flag this as being a new session:
  - Treat the first song in the sorted list as the start of a new session.
  - For all other songs, flag as a new session when the minutes gap from the prior song is `>= 59`.

- Create a session number field:
  - Create `Session #` as a sequential integer assigned in time order by cumulatively counting the new-session flags (starting at 1 for the first session).

- Number the songs in order for each session:
  - Within each `Session #`, assign `Song Order` as 1 for the first song in that session, 2 for the second, etc., based on the song time order.

- Match the customers to the correct session, based on their entry time:
  - Define each session’s start time as the earliest `Date` among songs in that session.
  - For each session, find the customer entry that is closest to (but not later than) the session start time, subject to the constraint that the entry time must be within 10 minutes before the session start (inclusive).
    - If multiple customer entries satisfy this rule, select the one with the latest `Entry Time` (i.e., the nearest entry before the session start).
  - Attach the matched `Customer ID` to every song row in that session.
  - The Customer ID field should be null if there were no customers who arrived 10 minutes (or less) before the start of the session.

- Output formatting required for correctness:
  - In the final output, represent an unmatched `Customer ID` as an empty value.
  - Format `Customer ID` as follows:
    - If it is entirely numeric and has at least 7 digits, output it in scientific notation with two decimals and an uppercase exponent (e.g., `1.23E+07`-style formatting).
    - Otherwise, output it as its string value.
  - Format `Date` by rounding to the nearest minute, then outputting as `DD/MM/YYYY HH:MM:SS`.
  - Output rows sorted by `Session #` ascending, then `Song Order` ascending.

- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Session #
    - Customer ID
    - Song Order
    - Date
    - Artist
    - Song