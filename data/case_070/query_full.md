## Context

A website catalogs many battles fought on British soil, and a subset of that information has been web-scraped into a raw, semi-structured extract. The goal is to convert this raw scrape into a tidy table with consistent fields and standardized dates and names, while removing any incomplete records.

## Requirements

- Input the data.
  - Read from `inputs/input_01.csv` as raw text lines.
  - Skip the first line (it is not part of the battle records).

- Find a natural way to split the data into different fields.
  - Each remaining line contains:
    - a battle name fragment at the start of the line, and
    - an HTML-like fragment containing the remaining details.
  - Parse each line into two components: the initial battle name fragment and the HTML fragment.
  - From the HTML fragment, split the content into segments using the `<br />` break marker.
  - For field extraction, treat each segment both as:
    - its original HTML segment, and
    - a plain-text version with HTML tags removed.

- Create exactly five output fields per record: `Date`, `Battle`, `War`, `Victors`, `Description`.
  - **Battle**
    - Prefer the battle title embedded in the HTML (the bolded title segment when present, identified by checking if the segment contains `font-weight:bold`).
    - Otherwise, fall back to the first non-empty plain-text segment that contains the word "Battle" (case-insensitive).
    - Otherwise, fall back to the initial battle name fragment from the start of the line.
    - Clean battle names by standardizing whitespace (collapse runs of whitespace to single spaces and trim leading/trailing whitespace).
  - **Date**
    - Extract the date as the first non-empty plain-text segment that appears after the battle title segment, excluding any segment that contains the word "Victors" (case-insensitive).
    - Clean the dates:
      - If the date is a date range, keep only the start date (the first day in the range) and discard the end day.
      - If the date is provided as a year only (including “AD” year forms), interpret it as `01/01/YYYY`.
      - Otherwise parse the date from common “day month year” / “month day year” formats.
      - Output all dates in `DD/MM/YYYY` format.
      - If a date cannot be parsed into a valid `DD/MM/YYYY`, treat the row as incomplete (and remove it).
  - **War**
    - After identifying the date segment, take the first non-empty plain-text segment that follows it, stopping before any segment that contains the word "Victors" (case-insensitive).
    - If no such segment exists (i.e., the date segment is immediately followed by a victors segment), treat the row as incomplete (and remove it).
    - Clean war text by standardizing whitespace (collapse runs of whitespace to single spaces and trim).
  - **Victors**
    - Prefer a segment explicitly labeled with `Victors:` (case-insensitive) and extract the victors value from it (the text after "Victors:").
    - If no explicit `Victors:` segment exists, use the first non-empty plain-text segment that follows the war segment.
    - Clean victors text by standardizing whitespace (collapse runs of whitespace to single spaces and trim).
  - **Description**
    - Use all remaining non-empty plain-text segments after the victors segment.
    - Concatenate them into a single description string separated by single spaces.
    - For description, trim leading/trailing whitespace (do not otherwise reflow internal spacing beyond the concatenation step).

- Handle ambiguity in field extraction.
  - **Battle field ambiguity**: When HTML contains no bolded title, use the first plain-text segment containing "Battle" as the battle title. This resolves ambiguity about which segment represents the battle title.
  - **Date field ambiguity**: When extracting the date, exclude any segment containing "Victors" (case-insensitive) to avoid misidentifying victors content as dates.
  - **War field ambiguity**: When extracting War, stop at any segment containing "Victors" (case-insensitive). If no segment exists between the date and victors segments, the record is incomplete.
  - **Victors field ambiguity**: When no explicit "Victors:" label exists, use the first non-empty segment after the war segment. This assumes the segment order is consistent: Battle → Date → War → Victors → Description.
  - **Date format ambiguity**: When parsing dates, try formats in the specified priority order (`%d %B, %Y` first, then `%B %d, %Y`, etc.). This resolves ambiguity between "day month year" and "month day year" formats.

- Remove rows which are incomplete.
  - Drop any record where any of the five required fields (`Date`, `Battle`, `War`, `Victors`, `Description`) is missing or empty after extraction and parsing.
  - Also drop records whose extracted date cannot be normalized to `DD/MM/YYYY` under the rules above.

- Clean battle names.
  - Ensure each record has a single, cleaned battle name field derived from the extracted title/name, with standardized whitespace.
  - Do not re-order the dataset; preserve the input record order after filtering.

- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Date
    - Battle
    - War
    - Victors
    - Description