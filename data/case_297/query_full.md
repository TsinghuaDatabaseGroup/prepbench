## Context

You are preparing a structured, analysis-ready dataset of Strictly Come Dancing performances from a single raw input table. The goal is to standardize time fields (Series/Year/Week), normalize week/stage/theme information, split composite fields (scores and music) into atomic components, and handle group dances consistently so the final output is one row per performed song within a dance entry.

## Requirements

- Input the data from `inputs/input_01.csv` as text so that parsing and splitting rules can be applied deterministically.

- Add a `Year` field derived from `Series` using this rule:
  - If `Series` is 1 or 2, `Year = 2004`.
  - If `Series` is 3 or greater, `Year = 2002 + Series`.
  - Treat `Series` as an integer for this calculation.

- Remove repeated table headers from the dataset by filtering out rows where `Couple` equals the literal header value `"Couple"`.

- Split and standardize the `Week` field:
  - Extract the numeric week number from patterns of the form `Week <number>` and store it in `Week` as an integer.
  - If the original `Week` value contains a colon (`:`), treat the text after the first colon as week theme text and initially store it in `Theme`; otherwise set `Theme` to null.

- Derive a `Stage` field from the week theme text and clean `Theme` accordingly:
  - If the theme text indicates a quarter-final, set `Stage = "Quarter Final"` **except** when the original `Week` string uses a “Theme Week (Quarter-final)” style (i.e., contains the pattern ` Week (`); in that case, leave `Stage` null.
  - If the theme text indicates a semi-final, set `Stage = "Semi Final"`.
  - If the theme text indicates a final (and it is not a quarter-final or semi-final), set `Stage = "Final"`.
  - Remove any stage wording (quarter-final, semi-final, final) from the `Theme` text so `Theme` represents only the theme name.

- Further standardize `Theme`:
  - Remove trailing occurrences of the word “Week” and remove “Night”.
  - Remove punctuation characters.
  - Map the theme value `"Hollywood"` to `"Movie"`.
  - If the resulting theme text is empty after these transformations, set `Theme` to null.

- Split the `Scores` field into `Total Score` and `Judges Scores`:
  - When `Scores` is in the form `<total> (<judge1, judge2, ...>)`, set:
    - `Total Score` to the numeric total (integer).
    - `Judges Scores` to the text inside parentheses (as a single string).
  - If `Scores` is missing or equals `"No scoresreceived"`, set both `Total Score` and `Judges Scores` to null.
  - Drop the original `Scores` field after splitting.

- Handle group dances (identified when `Dance` contains `"Group"` or `"Marathon"`):
  - Set `Couple` to `"Group"`.
  - Set `Total Score` to null for these rows.
  - Collapse group dances before music expansion: two group-dance rows are considered the "same group-dance entry" if they have identical values for `Week` (after extraction of the numeric week number), `Dance`, and `Music` (the original `Music` field value before splitting). When collapsing multiple rows representing the same group-dance entry into a single row, keep all field values from the first occurrence (with `Couple` set to `"Group"` and `Total Score` set to null as specified above). After music expansion (splitting `Music` into `Song` and `Artist`), the same group-dance entry may produce multiple output rows (one per distinct song), but these rows should not be merged again as they represent different songs within the same group performance.

- Clean the `Couple` field by removing digits from the value (after applying the group-dance rule above).

- Split the `Music` field so each distinct song becomes its own row:
  - Treat the `Music` cell as potentially containing multiple songs separated by a delimiter; normalize the string so it can be split into a list of songs and then expand (explode) into one output row per song.
  - For each expanded song entry, split into:
    - `Song`: the song title.
    - `Artist`: the artist text when present.
  - Split song vs. artist using an em dash separator (`—`) when available; if no artist is present, leave `Artist` null.
  - Remove quote characters from `Song`.
  - If `Music` is missing or yields no songs, still keep one row for that performance with `Song` and `Artist` as null.
  - Drop the original `Music` field after creating `Song` and `Artist`.

- Combine per-week theme detail fields into a single `Theme Detail` field:
  - Create `Theme Detail` by concatenating (in this order) any non-empty values from: `Film`, `Broadway musical`, `Musical`, `Country`, `CelebratingBBC`, separated by spaces.
  - If none of these fields have values for a row, set `Theme Detail` to null.
  - Drop the source fields used to construct `Theme Detail`.

- Remove unnecessary fields so the remaining columns match the required output schema exactly.

- Deduplicate final rows:
  - After all transformations (including music expansion and group-dance collapsing), remove exact duplicate rows based on the full set of output fields, keeping the first occurrence.

- Ensure output data types where applicable:
  - `Year`, `Series`, and `Week` must be integers.
  - `Total Score` must be a nullable integer.
  - `Judges Scores` should be null when empty or represented as an explicit null-like placeholder.

- Output the data exactly as specified below.

## Output

- output_01.csv
  - 13 fields:
    - Year
    - Series
    - Week
    - Stage
    - Theme
    - Theme Detail
    - Couple
    - Total Score
    - Judges Scores
    - Dance
    - Song
    - Artist
    - Result