## Context
You are preparing two analysis outputs from a Netflix lockdown survey using Tableau Prep under a “click-only” constraint (i.e., do not use typed calculations). The goal is to (1) summarize what devices people used to watch Netflix and (2) produce a ranked list of shows based on average ratings, while validating free-text show entries against an official UK Netflix content list.

## Requirements
- Input the data.
  - Use the survey responses file, a UK Netflix content list file (single-column list of titles), and a device-types reference file.

- Remove duplicate survey submissions.
  - Treat submissions as duplicates when all survey fields match except the timestamp; keep only one record per duplicate group.

- Output 1: Count how many people are watching on each device.
  - Start from the survey question that captures devices used to watch Netflix (a free-text field).
  - Because responses may contain multiple devices, split each response into multiple device tokens (support tokens separated by commas, new lines, “&”, and “/”).
  - Compare each token to the device types provided in the Devices input:
    - If a token matches a provided device type, map it to that canonical device label.
    - Ignore explicit “etc.”/“etc” tokens and blanks (i.e., they should not produce a device record).
    - If a response contains no recognized device tokens but is not blank and not only “etc.”, label it as `Other`.
  - If the same respondent lists the same device multiple times in their response, count that device only once for that respondent.
  - Aggregate to one row per device with a count of resulting device records.

- Output 2: Rank each show by its average rating.
  - Prepare a canonical list of valid shows from the UK Netflix content list:
    - Remove any trailing bracketed year (or other trailing parenthetical text) at the end of each title.
    - Standardize titles to a single canonical form for matching (case-insensitive matching), and de-duplicate the resulting show list.
  - Build a “watched shows” table from the survey:
    - From the “binging during lockdown” free-text field, split the response into show tokens using commas and semicolons only.
    - For each token, remove any trailing bracketed year/parenthetical text, standardize to the canonical form, drop blanks, and de-duplicate per respondent and show.
    - Keep only shows that exist in the canonical UK Netflix content list (inner match).
  - Prepare ratings from the predefined rating questions (i.e., all “How would you rate …” columns except the “Other” rating column):
    - Reshape these columns into a long format with one row per respondent per rated show.
    - Derive the show name from the rating question text by removing the question prefix/punctuation and standardizing to the same canonical show-name form used above.
    - Keep only ratings where the respondent is confirmed (from the watched-shows table) to have watched that show (inner match on respondent and show).
  - Validate and map “Other” ratings:
    - For respondents who provided a value for the “Other” rating question, attempt to map that rating to a single specific show from their watched-shows list.
    - Only accept an “Other” rating if the respondent has exactly one watched show that:
      - is in the canonical UK Netflix content list, and
      - is not one of the predefined shows that already have dedicated rating questions.
    - If the respondent has zero or multiple such candidate shows, exclude that “Other” rating entirely.
  - Combine the validated predefined ratings and the validated mapped “Other” ratings into a single ratings table with fields: show and numeric rating (exclude non-numeric ratings).
  - Compute the average rating per show.
  - Create a dense rank over shows by average rating in descending order (highest average rating gets rank 1; ties share the same rank, and the next rank increments by 1).
  - For deterministic output, order the final ranked results by Rank ascending, then Show ascending.

- Output the data.

## Output

- output_01.csv
  - 2 fields:
    - Device
    - Count

- output_02.csv
  - 3 fields:
    - Rank
    - Show
    - Rating