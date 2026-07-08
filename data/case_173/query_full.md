## Context

You are preparing dialogue timing data to support a Gantt-style visualization of who is speaking over time within each episode. The core task is to compute how long each line of dialogue lasts by looking ahead to the next (distinct) timestamp, using the episode runtime as the endpoint for the final line, then expand any comma-separated speaker names so the final dataset has one row per character-speaking segment. The final output must be limited to the “Gameplay” section.

## Requirements

- Input the data.
  - Use the dialogue-level input (input_03.csv) and the episode-level details input (input_04.csv).

- Compute dialogue segment end times per episode by looking ahead to the next timestamp.
  - Treat each record’s start time as `time_in_secs`.
  - For each `Episode`, determine the next *distinct* `time_in_secs` after the current row’s `time_in_secs` (i.e., if multiple rows share the same timestamp, they should all map to the same next distinct timestamp for duration purposes).
  - For rows where there is no later distinct timestamp in that episode, use the episode end time from the episode details as the segment end time.
    - Use `runtime_in_secs` from the episode details as the episode end time, matched by `Episode`.

- (As described in the original approach) create a timestamp rank per episode ordered by earliest timestamp.
  - Use a dense ranking over `time_in_secs` within each `Episode` so identical timestamps share the same rank and do not create artificial zero-length gaps.
  - The “next line” concept should be implemented so that duration is based on the next *rank/time* after the current one (i.e., the next distinct timestamp), with the final rank using the episode runtime as the endpoint.

- Join logic to apply the “next timestamp” mapping back onto the dialogue rows.
  - Build a mapping at the grain of (`Episode`, `time_in_secs`) that provides the corresponding next distinct timestamp (or null if none).
  - Join this mapping back to the full dialogue rows on (`Episode`, `time_in_secs`) so every dialogue row can calculate a duration.
  - Then join episode end time by `Episode` so missing “next timestamp” values can be replaced with the episode runtime.

- Calculate dialogue durations.
  - For each dialogue row, compute:
    - `start_time` = `time_in_secs` cast to an integer number of seconds.
    - `Duration` = (next distinct timestamp if present, otherwise episode runtime) − `time_in_secs`.
  - Remove rows where `Duration` is not strictly positive (i.e., `Duration` must be `> 0`).
  - Ensure `Duration` is an integer number of seconds in the output.

- Some character names are comma separated; split these names out and trim any trailing whitespace.
  - If a `name` contains commas, split into multiple names.
  - Trim whitespace around each resulting name.
  - It’s ok to leave `"ALL"` as `"ALL"` (i.e., do not split it further).
  - After splitting/exploding, drop any resulting rows where `name` is missing or empty.

- Reshape the data so there is a row per character.
  - After name splitting and exploding, each output row must represent one character’s participation in one dialogue segment: one `Episode` + one `name` + one `start_time`.

- Filter the data for just Gameplay sections.
  - Keep only rows where `section` equals `"Gameplay"`.
  - Apply this filter before splitting/exploding names so only Gameplay dialogue contributes to character rows.

- Ensure no duplication of rows has occurred.
  - De-duplicate the final dataset using the full output row identity (all output columns), keeping the first occurrence when duplicates exist.

- Output the data.
  - The final dataset must contain exactly the required fields, with the same field names and casing as specified.
  - Preserve the dialogue text as a string; if a dialogue value is numeric-like, represent it consistently as a decimal string rounded to 6 decimal places with trailing zeros removed (and normalize "-0" to "0") so the output is stable.
  - **Dialogue value formatting rules:**
    - A dialogue value is considered "numeric-like" if it can be successfully parsed as a decimal number (including integers and decimal numbers, but excluding values that contain non-numeric characters beyond a leading minus sign and decimal point).
    - For numeric-like values:
      - Parse the value as a decimal number.
      - Round to 6 decimal places (using standard rounding rules).
      - Remove trailing zeros after the decimal point (e.g., "34.000000" becomes "34", "12.500000" becomes "12.5").
      - Normalize "-0" to "0".
      - Examples: "34" → "34", "34.5" → "34.5", "34.123456789" → "34.123457", "34.000000" → "34", "-0" → "0".
    - For non-numeric-like values (values that cannot be parsed as a decimal number, or contain non-numeric characters), preserve the original string value as-is.

## Output

- output_01.csv
  - 7 fields:
    - Episode
    - name
    - start_time
    - Duration
    - youtube_timestamp
    - dialogue
    - section