## Context

Prepare a combined dataset to analyze the touring histories of two featured UK singer-songwriters, using (1) gig history records and (2) a lookup of geographic coordinates for each gig’s location, and (3) a lookup of each featured artist’s home location. The prepared output should support analysis of gig locations and “fellow artists” who appeared on the same bill.

## Requirements

- Input the data from the provided files:
  - A gigs table (“Gigs Data”) containing at least: Artist, Concert Date, Concert, Venue, Location.
  - A location-to-coordinates table containing at least: Location and a single text field holding both coordinates (named `LongLats`).
  - A home-locations table containing at least: Artist, Hometown, Longitude, Latitude (to be renamed as specified below).

- Prepare the coordinates lookup:
  - Split the `LongLats` field into two numeric fields using the comma delimiter:
    - The first value is `Latitude`.
    - The second value is `Longitude`.
  - Remove the original `LongLats` field after splitting.
  - If multiple coordinate rows exist for the same `Location`, keep only one row per `Location` (keep the first occurrence).

- Create "Fellow Artists" rows from the `Concert` field:
  - Parse `Concert` by splitting on the `/` character.
  - If `Concert` does not contain a `/`, then produce exactly one output row for that gig with `Fellow Artists` blank.
  - If `Concert` contains a `/`:
    - Create one output row per split segment.
    - Additionally, if all split segments are non-blank, also create one extra output row for that gig with `Fellow Artists` blank.
    - For each produced row, if the split segment equals the gig's `Artist` (using exact string matching, case-sensitive), set `Fellow Artists` to blank (so the artist is not listed as their own fellow artist).
  - Ensure the result is one row per gig-record per fellow-artist entry (including blank entries created by the rules above).
  - **Important**: Artist names are matched using exact string comparison. Do not perform any spelling correction, normalization, or variant handling. If the same artist appears with different spellings (e.g., "Saint Raymond" vs "Saint Rayman"), treat them as different artists.

- Join the datasets together:
  - Join the expanded gigs data to the coordinates lookup on `Location` using a left join (retain all gig rows even when coordinates are missing at this stage).
    - The join must use exact string matching on the `Location` field (case-sensitive, whitespace-sensitive, punctuation-sensitive).
    - If a gig's `Location` does not have an exact match in the coordinates lookup table, the `Longitude` and `Latitude` fields will be missing/null for that row at this stage.
  - Add in the home locations for each featured artist by joining to the home-locations table on `Artist` using an inner join:
    - Rename the home-locations fields `Longitude` → `Home Longitude` and `Latitude` → `Home Latitude` before output.
    - The join must use exact string matching on the `Artist` field (case-sensitive).

- Validate required geography for the final output:
  - Convert `Longitude` and `Latitude` (gig coordinates) to numeric.
  - Exclude rows where either gig `Longitude` or gig `Latitude` is missing after conversion (i.e., only output rows with valid gig coordinates).

- Standardize date representation:
  - Parse `Concert Date` as a date where possible and output it formatted as `DD/MM/YYYY`.
  - If a date cannot be parsed, output `Concert Date` as a blank string.

- Remove obvious duplicate records:
  - After all joins, formatting, and filtering, remove duplicates across the full set of output fields.
  - Additionally, when multiple rows are identical across all output fields except `Concert`, and the differing `Concert` values are the same when compared case-insensitively, keep only one row using a fixed, deterministic preference order for selecting which `Concert` label to retain; if no preference applies, keep the first encountered.
  - **Important**: The duplicate detection only considers case-insensitive string comparison. It does not handle spelling variants or typos. If two `Concert` values differ in spelling (even if they appear to be the same artist or event), they are considered different and both rows are retained unless all other fields are identical.

- Output the data.

## Output

- output_01.csv
  - 11 fields:
    - Longitude
    - Latitude
    - Fellow Artists
    - Artist
    - Concert Date
    - Concert
    - Venue
    - Location
    - Hometown
    - Home Longitude
    - Home Latitude