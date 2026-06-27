## Context
To explore which films pass the Bechdel Test, produce a structured table of movies with their Bechdel categorisation, a numeric ranking of that categorisation, and an overall Pass/Fail flag.

## Ambiguity Resolution

This section explicitly addresses potential ambiguities in the data processing requirements to ensure deterministic behavior:

1. **Closest Preceding Image Tag Selection** (see extraction step below):
   - When multiple image tags with matching `title` attributes exist before a movie anchor, "closest preceding" means the last (most recent) such image tag when scanning the text from the beginning to the anchor position.

2. **Ranking Rule Priority** (see ranking step below):
   - If a categorisation text matches multiple ranking conditions, check conditions in order: Ranking 5 → 4 → 3 → 2 → 1.
   - Assign the ranking of the first matching condition (worse rankings take precedence).

3. **Deduplication with Tied Rankings** (see deduplication step below):
   - When multiple categorisations share the same maximum `Ranking` for a `(Movie, Year)` pair, sort by `Movie` (ascending), then `Year` (ascending), then `Categorisation` (ascending), and keep the first row.

## Requirements
- Input the data.
  - Use `input_01.csv` as the source of film-year records. It must contain at least:
    - `Year`
    - `DownloadData` (an HTML-like text field containing the movie entries and Bechdel categorisation information)
  - Use `input_02.csv` as the reference table for decoding HTML entities in movie titles. It must contain at least:
    - `Char` (the decoded character; if missing, treat it as a single space character)
    - `Numeric` (a numeric HTML entity form, such as `&#...;`)
    - `Named` (a named HTML entity form, such as `&...;`)
- Parse out the data in the `DownloadData` field so that each extracted record contains:
  - the Movie title, and
  - the Bechdel Test categorisation text that explains whether/how it passes or fails.
- Before decoding other HTML entities, replace every occurrence of `&amp;` with `&` in `DownloadData`.
  - Example: `"Toki wo kakeru sh&#333;jo (The Girl Who Leapt Through Time)"`
- Extract movie entries and their categorisations from `DownloadData` as follows:
  - Identify each movie title as the inner text of anchor tags of the form `<a id="movie-...">MOVIE TITLE</a>`.
  - For each such movie anchor, assign its `Categorisation` by finding the closest preceding image tag (before that anchor in the text) whose `title` attribute is formatted like `title="[CATEGORISATION]"`, and extracting the text inside the brackets.
    - **Ambiguity resolution**: "Closest preceding" means the last (most recent) image tag with a matching `title` attribute that appears before the movie anchor in the text. If multiple image tags exist before the anchor, select the one that appears closest to the anchor (i.e., the last match when scanning backwards from the anchor position).
  - Output grain at this stage is one row per extracted (Movie, Year, Categorisation) occurrence.
- Decode HTML entities in the extracted Movie titles.
  - HTML entities to decode are substrings that start with `&` and end with `;` (the maximum number of such codes in a Movie title is 5).
  - Replace each entity using the mapping derived from `input_02.csv`:
    - Map both `Numeric` and `Named` codes to `Char`.
    - If the mapped `Char` is missing, replace with a single space (not a null).
  - If an entity is not present in the mapping, decode it using standard HTML entity decoding.
- Rank the Bechdel Test categorisations from 1 to 5 (1 = best, 5 = worst) using the following rules based on the categorisation text (case-insensitive matching):
  - Ranking 5: categorisation contains "fewer than two women"
  - Ranking 4: categorisation contains "don't talk to each other"
  - Ranking 3: categorisation contains "only talk to each other about a man"
  - Ranking 2: categorisation contains "although dubious"
  - Ranking 1: categorisation contains "talk to each other about something other than a man"
  - If none of the above conditions match, assign Ranking 5.
  - **Ambiguity resolution**: If a categorisation text matches multiple ranking conditions, check the conditions in the order listed above (Ranking 5, then 4, then 3, then 2, then 1). Assign the ranking corresponding to the first matching condition. This means if multiple conditions match, the worse (higher numeric) ranking takes precedence.
- Derive `Pass/Fail` from `Ranking`:
  - `Pass` if `Ranking` is 1 or 2
  - `Fail` if `Ranking` is 3, 4, or 5
- Where a film has multiple categorisations for the same Movie and Year, keep only the worse ranking.
  - Define "worse" as the highest numeric `Ranking`.
  - Deduplicate on `(Movie, Year)` by keeping the row with the maximum `Ranking` (and keep its associated `Categorisation`).
  - **Ambiguity resolution**: If multiple rows have the same maximum `Ranking` for a given `(Movie, Year)` pair, sort all rows with that maximum ranking by `Movie`, then `Year`, then `Categorisation` (all ascending), and keep the first row after sorting. This ensures deterministic selection when rankings are tied.
  - Recompute/confirm `Pass/Fail` from the retained `Ranking` after this step.
- Ensure `Year` and `Ranking` are output as integers.
- Output the final dataset sorted by `Movie` then `Year`, ascending.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Movie
    - Year
    - Pass/Fail
    - Ranking
    - Categorisation