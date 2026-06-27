## Context

You are preparing a country-by-SDG long-format table from the “Overview” data, where each Sustainable Development Goal (SDG) has two adjacent pieces of information per country: a colour status indicator and an arrow-based trend indicator. The goal is to reshape the wide overview layout into a tidy structure with one row per Country × SDG, while translating the colour and arrow symbols into clear text labels.

## Requirements

- Input the data.
- Input the Overview sheet (provided as `inputs/input_04.csv`).

- Treat the following columns as the country-level identifier (base) fields and carry them through to every output row:
  - `Country`
  - `2023 SDG Index Score`
  - `2023 SDG Index Rank`
  - `Regions used for the SDR`

- Exclude rows where `Country` is missing.

- Handle the SDG headings that are effectively merged across two columns (one for the colour indicator and one for the arrow indicator):
  - Interpret the SDG-related columns (everything other than the base fields) as an ordered sequence of pairs: for each SDG, the first column in the pair is the colour indicator and the second column in the pair is the arrow/trend indicator.
  - Ensure the arrow/trend fields remain clearly associated with the correct SDG by pairing each trend column with the SDG name taken from its corresponding colour-indicator column.
  - If the number of SDG-related columns is not even (i.e., cannot be partitioned into value/trend pairs), stop with an error rather than producing an output.

- Reshape the data to long format:
  - Output grain: one row per `Country` per SDG.
  - For each SDG pair:
    - Set `SDG Name` to the SDG name represented by the colour-indicator column header.
      - Extract the SDG name from the column header: if the header contains a colon (e.g., "SDG1: No Poverty"), use the full header text as the SDG name; if the header format is inconsistent or does not contain an SDG identifier, use the header text as-is.
    - Rename the colour indicator field to `SDG Value`.
    - Rename the arrow field to `SDG Trend`.
  - Preserve the original row order of countries as they appear in the input, and within each country preserve SDG order as the SDG pairs appear from left to right in the input.

- Update/standardize the SDG status labels in `SDG Value`:
  - Green - Goal Achieved
  - Yellow - Challenges Remaining
  - Orange - Significant Challenges
  - Red - Major Challenges
  - Grey - Insufficient
  - If `SDG Value` is already one of the target labels above, keep it unchanged; otherwise apply the mapping where it matches.
  - If `SDG Value` is missing (empty string, null, or whitespace-only), set it to null in the output.
  - If `SDG Value` does not match any of the source values in the mapping table above and is not already a target label, keep the original value unchanged in the output.

- Update/standardize the trend labels in `SDG Trend`:
  - ↑ - On Track
  - ➚ - Moderately Increasing
  - → - Stagnating
  - ↓ - Decreasing
  - If `SDG Trend` is already one of the target labels above, keep it unchanged; otherwise apply the mapping where it matches.
  - If `SDG Trend` is missing (empty string, null, or whitespace-only), set it to null in the output.
  - If `SDG Trend` does not match any of the source values in the mapping table above and is not already a target label, keep the original value unchanged in the output.

- Format numeric fields:
  - Convert `2023 SDG Index Score` to numeric where possible and round to 9 decimal places.
  - Convert `2023 SDG Index Rank` to an integer type where possible, leaving missing/unparseable values as null.

- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Country
    - 2023 SDG Index Score
    - 2023 SDG Index Rank
    - Regions used for the SDR
    - SDG Name
    - SDG Value
    - SDG Trend