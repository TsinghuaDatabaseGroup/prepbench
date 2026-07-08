## Context
You have Zoom chat/comment logs from three regional runs of the same conference session (APAC, EMEA, and AM). The goal is to (1) summarize how many questions vs. answers occurred in each session and (2) produce a participant-level table derived from each person’s initial “intro” comment, with all timestamps standardized to GMT.

## Requirements
- Input the data.
  - Treat the three sessions as separate inputs (one per region): APAC, EMEA, and AM (the Americas).
  - Add a field that identifies which session each record belongs to (Location = APAC / EMEA / AM).

- Make a date time field to represent local time.
  - The session date is 7 October 2020.
  - Each record has a time-of-day value; construct a “Local DateTime” by combining **2020-10-07 14:00:00** with the record’s time offset (i.e., interpret the provided time as an elapsed time added to 2:00 PM on that date).

- Work out the times to make them all equal Greenwich Mean Time (GMT).
  - Create `Date (GMT)` from `Local DateTime` using the session-specific offsets:
    - APAC is 11 hours before GMT ⇒ `Date (GMT) = Local DateTime - 11 hours`
    - EMEA is 1 hour before GMT ⇒ `Date (GMT) = Local DateTime - 1 hour`
    - AM is 5 hours after GMT ⇒ `Date (GMT) = Local DateTime + 5 hours`

- Split the comments into two categories based on each person’s sequence of comments within each session.
  - Within each `Location` and `Who`, order comments by `Date (GMT)` ascending to determine sequence.
  - Everyone’s first comment (except Carl Allchin’s) is treated as the “intro” comment that contains where they are from and whether it’s their first session.
  - Carl Allchin’s first comment in each session is an opening statement and must be excluded from question/answer counting and from the “intro” extraction output.
  - Every subsequent comment (and Carl Allchin’s non-opening comments) must be classified as either a question or an answer.

- Derive location attributes from the intro comment (first comment per person per session, excluding Carl Allchin).
  - From the intro comment text, derive:
    - `First Time Indicator`: set to 1 if the intro comment indicates “first time”; otherwise 0.
    - `City` and `Country`:
      - EMEA and APAC intros provide city and country.
      - AM intros provide city and country unless the person is in the US, where they provide city and state; in that case set `Country` to **United States** (rather than keeping the state as the country).
  - Clean up any rogue values at a high level so that city/country values can be validated (do not invent missing geography).
  - Apply a geographic validation equivalent to assigning a City and Country data role, and ONLY keep records with valid City/Country results. If the City/Country cannot be validated, exclude the record from the participant-level output.
  - **Participants to exclude due to invalid City/Country validation:** Arsene Xie, Leona Lai, Jenny Martin, Rosario Gauna

- Classify non-intro comments as “Question” or “Answer” (for counting).
  - Exclude all intro comments (as defined above) from question/answer classification and counts.
  - Exclude Carl Allchin’s first comment in each session from question/answer classification and counts.
  - For remaining comments:
    - If `Who` is Carl Allchin, classify as `Answer`.
    - Else if the comment contains an “@”, classify as `Answer`.
    - Else if the comment contains a “?”, classify as `Question`.
    - Otherwise classify as `Answer`.

- Count the number of questions and answers at each session excluding everyone’s first comment.
  - Aggregate counts by `Location` and `Question or Answer`, counting the number of classified comments (Instances).

- Output two data sets.
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Instances
    - Question or Answer
    - Location

- output_02.csv
  - 6 fields:
    - Date (GMT)
    - Location
    - City
    - First Time Indicator
    - Country
    - Who