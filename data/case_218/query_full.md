## Context
Easter Sunday is commonly defined as the first Sunday after the full Moon that occurs on or after the spring equinox; if the full Moon itself falls on a Sunday, Easter is the following Sunday. To assess this relationship empirically, compare each year’s Easter Sunday date to the most recent full Moon on or before that Easter date, then summarize the distribution of day gaps between those two dates. Because the historical full Moon data is only available from 1900 onward, restrict the analysis to years 1900 through 2023 (inclusive).

## Requirements
- Input the data from:
  - `input_01.csv`: Easter Sunday dates (uses the `Easter Sunday` field).
  - `input_02.csv`: full Moon dates and annotations (uses the `Date` and `Time` fields).
- Restrict both Easter and full Moon records to the year range 1900–2023 inclusive, where "year" is derived from the parsed date.
  - Parse `Easter Sunday` as a date using the day/month/year format. If a date cannot be parsed, exclude that row from the analysis.
  - Parse the full moon `Date` as a date using the "day month year" format (e.g., day number, full month name, year). Exclude full moon rows whose date cannot be parsed.
- Rename / standardize the full Moon fields so you can reference:
  - A parsed full Moon date field (named `Full Moon Date`).
  - The `Time` field for event parsing (named `Time`).
- From the full Moon `Time` field, derive an `Interesting Event` classification based on the presence of markers:
  - The markers appear as text annotations in the `Time` field:
    - `[+]` indicates a blue moon
    - `[*]` indicates a partial lunar eclipse
    - `[**]` indicates a total lunar eclipse
  - Classification rules (checked in this order, stopping at the first match):
    - If `[+]` is present in the `Time` field, classify as `Blue moon`.
    - Else if `[*]` is present and `[**]` is not present, classify as `Partial Lunar Eclipse`.
    - Else if `[**]` is present, classify as `Total Lunar Eclipse`.
    - Otherwise leave the event empty/blank.
  - Note: If multiple markers are present in the same `Time` field, the classification is determined by the first matching rule above. For example, if both `[**]` and `[+]` are present, it will be classified as `Blue moon` because `[+]` is checked first.
- Join full moon data with Easter Sunday dates in order to associate each Easter with **only the single full Moon immediately preceding (or on) Easter Sunday**:
  - For each Easter Sunday date, consider full Moon candidates whose `Full Moon Date` is:
    - On or before that Easter Sunday date (inclusive), and
    - On or after January 1 of the previous calendar year (inclusive).
  - Note: "previous calendar year" means the year before the Easter year. For example, for Easter in year 1900, the previous calendar year is 1899, so candidates must be on or after January 1, 1899.
  - From those candidates, select the one with the smallest non-negative day difference to Easter Sunday (i.e., the most recent full Moon on or before Easter). If no candidate exists for an Easter date, exclude that Easter year from downstream calculations.
- Calculate the number of days between the selected full Moon and Easter Sunday as:
  - `Days Between = (Easter Sunday date - Full Moon Date)`, measured in whole days.
- Aggregate results to summarize how often each day-gap value occurs:
  - Group by `Days Between`.
  - For each group, compute:
    - `Number of Occurrences`: count of years in the group.
    - `Min Year`: earliest Easter year in the group.
    - `Max Year`: latest Easter year in the group.
    - `Most Interesting event`: within the group, select a single event label using this priority order (most interesting to least interesting): `Total Lunar Eclipse`, then `Partial Lunar Eclipse`, then `Blue moon`. If a group contains multiple different event types, select the one with the highest priority according to this order. If none exist in the group, leave blank.
- Ensure the final output:
  - Uses integer types for the day-gap and year/count fields.
  - Is sorted in ascending order by `Days Between Full Moon & Easter Sunday`.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Days Between Full Moon & Easter Sunday
    - Number of Occurrences
    - Most Interesting event
    - Min Year
    - Max Year