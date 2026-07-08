## Context
You are given a single input file describing consecutive elevator trips. Each record specifies the floor where passengers enter the lift (“From”) and the floor where they exit (“To”). Assume the lift completes one trip before starting the next (i.e., no intermediate pickups). The goal is to compare (a) how far the lift currently needs to reposition between consecutive trips versus (b) how far it would need to reposition if it always started each trip from a single “default” starting floor.

## Data Cleaning
Before processing, apply the following data cleaning steps to handle ambiguities:
- **Missing values**: Treat empty strings, "NA", "N/A", "-", "null" (case-insensitive) as missing values. If `From` or `To` is missing, exclude that row from processing.
- **String normalization**: Trim leading and trailing whitespace from all string fields. Collapse multiple consecutive spaces into a single space.
- **Case normalization**: Convert floor labels to uppercase before processing (e.g., "b" → "B", "g" → "G").
- **Floor label validation**: Only accept floor labels that are either "B", "G", or numeric strings that can be parsed as integers. Reject any other formats (e.g., "Basement", "Ground", "1st", etc.).

## Requirements
- Input the data from `input_01.csv`. The logic below assumes at minimum two fields exist for each trip: `From` and `To`, containing floor labels. Apply the data cleaning steps above before processing.
- Create a `TripID` representing the trip sequence through the day:
  - Assume all trips took place on 12th July 2021.
  - Treat the input row order as the chronological time-of-day order, and assign `TripID = 1, 2, 3, ...` in that order (do not reorder the input).
- Convert floor labels to an ordered numeric scale consistent with the required floor order **B, G, 1, 2, 3, ...**:
  - Map `B` to `-1`, `G` to `0`, and all other floors to their integer value.
- Calculate how many floors the lift travels **between trips** under the current sequence:
  - When multiple rows share the same `(Hour, Minute)`, collapse them to a single representative trip by keeping the **last** row in that minute (preserve the original file order when determining "last").
  - Compute between-trip distances on this collapsed sequence. For each trip *i > 1*, compute reposition distance as the absolute difference between the current trip’s start floor and the previous trip’s end floor:  
    `Travel_between_trips_i = |From_numeric_i - To_numeric_(i-1)|`.
  - The first trip in the collapsed sequence has no prior trip; exclude it from the between-trips average.
  - Compute `Avg Travel between trips currently` as the mean of `Travel_between_trips_i` over *i = 2..N* in the collapsed sequence.
- Calculate which floor the majority of trips begin at (the **Default Position**):
  - Determine the most frequent value of `From` (after data cleaning).
  - If there is a tie for most frequent, select the floor label with the smallest numeric value after conversion (i.e., compare the numeric values: B=-1, G=0, and numeric floors by their integer value). For example, if both "B" and "G" have the same frequency, select "B" because -1 < 0. If both "1" and "2" have the same frequency, select "1" because 1 < 2.
- Calculate how many floors the lift would need to travel to begin each journey if it always started from the Default Position:
  - For each trip, compute `Travel_from_default_i = |From_numeric_i - DefaultPosition_numeric|`.
  - Compute `Avg travel from default position` as the mean of `Travel_from_default_i` over all trips (do not collapse by minute for this metric).
- Compare the two strategies:
  - Compute `Difference = (Avg travel from default position) - (Avg Travel between trips currently)`.
  - Round the two averages and the difference to 2 decimal places for reporting.
- Output the data as a single-row summary.

## Output

- output_01.csv
  - 4 fields:
    - Default Position
    - Avg travel from default position
    - Avg Travel between trips currently
    - Difference
