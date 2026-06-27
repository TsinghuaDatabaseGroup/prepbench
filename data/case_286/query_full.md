## Context
You are preparing an analysis-ready table from the Women’s Heptathlon results at the 2023 World Athletics Championship to support comparisons between athletes who perform strongly in a few events versus those who are more balanced across all events. The goal is to convert the raw, wide-format results with multiple “breakdown” rows into a standardized, event-level dataset enriched with event metadata.

## Requirements
- Input the data from two CSV files:
  - `input_02.csv`: the results table containing athlete-level fields (position, athlete name, nationality, total points), a `Breakdown` field that indicates the type of row (e.g., score vs performance vs rolling total), and one column per event.
  - `input_01.csv`: the Event Lookup Table keyed by an event code, providing event metadata (event name, event type, and event order number).
- In the results table (`input_02.csv`):
  - Rename fields as follows: POS → Position, ATHLETE → Athlete, NAT → Nationality, POINTS → Total Points.
  - Remove the duplicate field for the 800m Run event: if multiple columns exist for the 800m Run event (e.g., `800` and `800.1`), keep only the column with the standard event code name (e.g., `800`) and drop any columns with non-standard names or suffixes (e.g., `800.1`).
  - Fill down (forward-fill) values in the first four fields—Position, Athlete, Nationality, Total Points—so that rows created for event breakdowns inherit the athlete-level identifiers and total points.
  - Remove letters from the Total Points field by extracting the first contiguous digit sequence and converting it to a numeric value (leave as null if no digits are present).
- Pivot/reshape the results so the output is at the grain of **one row per athlete per event**:
  - Unpivot the event columns into a long format with:
    - an `Event` identifier (the original event column name/code), and
    - a corresponding `Value`.
  - Use the `Breakdown` field to create three aligned measures for each athlete-event:
    - Event Points (from rows where Breakdown is “Event Score”),
    - Event Time/Distance (from rows where Breakdown is “Event Time/Distance”),
    - Rolling Total (from rows where Breakdown is “Rolling Total”).
  - Combine these three measures into a single athlete-event row by joining them on the keys: Position, Athlete, Nationality, Total Points, and Event. Use inner joins so that only athlete-event combinations present in all three breakdown types are retained.
- Join with the Event Lookup Table (`input_01.csv`) on the `Event` key:
  - Use a left join so every athlete-event row remains even if lookup metadata is missing.
  - Add the lookup fields: Event Name, Event Type, and Event No.
- Split position information contained in parentheses from two fields:
  - For `Event Time/Distance`: if the value ends with a parenthetical integer like `(10)`, split it into:
    - `Event Time/Distance`: the value with the parenthetical removed (trim whitespace),
    - `Event Position`: the extracted integer as a numeric value.
    - Additionally, if `Event Time/Distance` equals `NM` (case-insensitive, allowing surrounding whitespace), output it as an empty string in `Event Time/Distance` after splitting.
  - For `Rolling Total`: if the value ends with a parenthetical integer like `(10)`, split it into:
    - `Rolling Total Points`: the non-parenthetical portion converted to a numeric value,
    - `Position After Event`: the extracted integer as a numeric value.
- Ensure numeric casting for output correctness:
  - Convert Event Points to numeric (null if non-numeric),
  - Convert Position and Event No. to numeric (null if non-numeric).
- Sort rows by Position ascending and then by Event No. ascending (stable sorting), and then add a `Sort` field as a 1-based sequence number reflecting this final row order.
- Output the data exactly with the required fields and file name.

## Output

- output_01.csv
  - 13 fields:
    - Sort
    - Position
    - Athlete
    - Nationality
    - Total Points
    - Event Name
    - Event Type
    - Event No.
    - Event Time/Distance
    - Event Points
    - Event Position
    - Rolling Total Points
    - Position After Event