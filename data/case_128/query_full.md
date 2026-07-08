## Context
You are preparing a unified, analysis-ready calendar of Tokyo 2020 Olympic events sourced from the Olympics website. One input provides the event schedule (dates, times, sports, venues, and an event list), and a second input provides venue details (including venue coordinates). The goal is to produce a single table where each individual event item is a separate row, enriched with venue latitude/longitude, a sport grouping, and a flag for medal-related events.

## Data Cleaning and Ambiguity Resolution

This section clarifies how ambiguities in the input data are resolved:

- **Sport name variations**: The schedule table may contain sport names with inconsistent capitalization (e.g., `rugby` vs `Rugby`, `football` vs `Football`, `volleyball` vs `Volleyball`, `diving` vs `Diving`). The resolution logic is:
  - If the schedule's original `Sport` value begins with a lowercase letter, it is preserved as-is (with basic normalization) in the output `Sport` field.
  - If the schedule's original `Sport` value begins with an uppercase letter, the venue table's `Sport` value (if a match is found) is preferred as the canonical form; otherwise, the schedule value is used.
  - The `Sport Group` field applies specific mapping rules (see the "Group similar sports" section) that handle these variations consistently.

- **Text matching for joins**: When joining schedule and venue tables, text normalization is applied to handle formatting differences:
  - Periods are removed, non-breaking spaces are converted to regular spaces, multiple spaces are collapsed to single spaces, and text is converted to lowercase.
  - This ensures that variations like "Rugby." vs "rugby" or "Volleyball " vs "volleyball" can be matched correctly.


## Requirements
- Input the data.
  - Read the event schedule from `input_01.csv`.
  - Read the venue details from `input_02.csv`.

- Create a correctly formatted DateTime field.
  - Treat the schedule `Date` and `Time` as the source date/time components.
  - Parse `Date` into a true date using the pattern “day month year”, allowing for:
    - underscores in place of spaces, and
    - ordinal suffixes on the day number (e.g., “st”, “nd”, “rd”, “th”).
  - Create `UK Date Time` as a text field in the format:
    - `"<excel_serial> days HH:MM:00"`,
    - where `<excel_serial>` is the number of days between the parsed date (at day precision) and `1899-12-30` (Excel 1900 date system),
    - and `HH`/`MM` come from the schedule `Time` (zero-padded to 2 digits). If `Time` is not parseable into hour/minute, use `00:00`.

- Parse the event list so each event is on a separate row.
  - Split the schedule `Events` field into a list using comma as the delimiter.
  - Trim surrounding whitespace around each split item.
  - If `Events` is missing/blank, produce a single split item as an empty string.
  - If `Events` is exactly `-`, keep it as a single split item `-`.
  - Explode the schedule so the output grain is: **one row per original schedule row per split event item**.
  - Store the split value in `Events Split`.

- Group similar sports into a Sport Type field.
  - Create `Sport Group` from the final output `Sport` value using these rules (apply in order, first match wins):
    - `Baseball/Softball` → `Baseball`
    - `Artistic Gymnastics` or `Trampoline Gymnastics` → `Gymnastics`
    - `Rhythmic Gymnastics` → `Rhythmic Gymnastics`
    - `Artistic Swimming`, `Swimming`, or `Marathon Swimming` → `Swimming`
    - `Diving` → `Diving`
    - `Water Polo` → `Water Polo`
    - `Canoe Sprint` or `Canoe Slalom` → `Canoeing`
    - `Judo`, `Karate`, or `Taekwondo` → `Martial Arts`
    - `Wrestling` → `Wrestling`
    - `Boxing` → `Boxing`
    - Any sport name containing `Cycling` → `Cycling`
    - `3x3 Basketball` or `Basketball` → `Basketball`
    - `Beach Volleyball` or `Volleyball` → `Volleyball`
    - `Table Tennis` or `Tennis` → `Tennis`
    - Any sport name containing `Ceremony` → `Ceremony`
    - For lowercase sport names, apply these specific mappings:
      - `rugby` → `Rugby` (capitalize first letter)
      - `diving` → `Diving` (capitalize first letter)
      - `football` → `Football` (capitalize first letter)
      - `volleyball` → `Volleyball` (capitalize first letter)
    - Otherwise, set `Sport Group` equal to `Sport`.

- Combine the Venue table.
  - From the venue details input, derive numeric `Latitude` and `Longitude` by splitting the venue `Location` field into two values separated by a comma.
  - Join venue coordinates onto the exploded schedule using a **left join** so all schedule rows are retained.
  - Use `Sport` and `Venue` as the join keys, matching them in a normalized text form so that superficial formatting differences (such as capitalization, punctuation, or repeated spaces) do not prevent a match.
    - **Text normalization for join keys**: For both `Sport` and `Venue` fields, normalize by:
      1. Remove all period characters (`.`).
      2. Replace non-breaking spaces (`\u00A0`) with regular spaces.
      3. Split on whitespace, then join with single spaces (this collapses multiple consecutive spaces into one).
      4. Trim leading and trailing whitespace.
      5. Convert to lowercase.
    - Apply this normalization to both the schedule table's `Sport`/`Venue` fields and the venue table's `Sport`/`Venue` fields before matching.
  - Enforce a many-to-one relationship from schedule rows to venue rows (i.e., each schedule row should match at most one venue row).
  - Populate `Latitude` and `Longitude` from the venue table; if no venue match is found, leave them null.
  - Keep the schedule's `Venue` text as the output `Venue` field (do not replace it with the venue table's venue name).

- Calculate whether the event is a 'Victory Ceremony' or 'Gold Medal' event.
  - Create `Medal Ceremony?` as a boolean.
  - Set it to `True` if `Events Split` contains (case-insensitive) either the phrase `victory ceremony` or `gold medal`; otherwise `False`.

- Finalize `Sport` for output and then compute grouping.
  - Determine whether the schedule's original `Sport` value (before any normalization) begins with a lowercase letter:
    - If it does, output `Sport` based on the schedule value with basic punctuation/spacing normalization:
      - Remove trailing periods (`.`).
      - Replace non-breaking spaces (`\u00A0`) with regular spaces.
      - Collapse multiple consecutive spaces into single spaces.
      - Trim leading and trailing whitespace.
    - Otherwise, if the joined venue table provides a canonical sport name for the matched venue (i.e., the venue table's `Sport` field value), prefer that; if no venue match was found or the venue table's `Sport` is null, use the schedule value with the same basic punctuation/spacing normalization as above.
  - Compute `Sport Group` from this final output `Sport`.

- Create `Date`.
  - Output `Date` as the parsed date at day granularity (no time component).

- Output the data.
  - Select exactly the nine required fields in the required order.
  - Sort the output stably by: `UK Date Time`, then `Sport`, then `Venue`, then `Events Split` (all ascending).

## Output

- output_01.csv
  - 9 fields:
    - Latitude
    - Longitude
    - Medal Ceremony?
    - Sport Group
    - Events Split
    - UK Date Time
    - Date
    - Sport
    - Venue