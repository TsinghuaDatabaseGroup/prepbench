## Context
The analysis focuses on goal timing patterns in major international men’s tournaments where goal-scorer records are available (World Cup and continental championships). The objective is to identify which 15-minute segment tends to be the most “exciting” (highest scoring rate), compare this pattern across competitions, and assess how it has shifted over decades.

## Requirements
- Input the data.
- Use the Results table as the backbone match list, and exclude matches whose tournament indicates a qualification round. Also exclude non-FIFA competitions listed in the tournament text (CONIFA and Viva World Cup).
- Derive two categorical fields from the Results table’s `tournament` text:
  - `Football Association` (e.g., FIFA, UEFA, CONMEBOL, CAF, AFC, OFC, CONCACAF)
  - `Competition` (e.g., World Cup, Euro, Copa América, Africa Cup of Nations, Asian Cup, Oceania Nations Cup, Gold Cup)
  The intent is to map each match to one of the supported competitions; not all tournaments will successfully map.
- Ensure the CONCACAF competition mapping treats “CONCACAF Championship” (and Gold Cup variants) as `Football Association = CONCACAF` and `Competition = Gold Cup`.
- Join/filter the Results-derived competitions to the International Competitions table so that only competitions defined in that reference list are retained.
- Parse match dates to obtain `Year` and compute `Decade` as the decade start year:  
  `Decade = floor(Year / 10) * 10`.
- Filter the match set to `Year >= 1950` (1950s onwards, inclusive).
- Create a `Match ID` field so each match has a unique identifier, constructed as:  
  `YYYY-MM-DD|home_team|away_team` (using the match date and the two team fields).
- Calculate the number of distinct matches per `Competition` and `Decade` as `Matches in a Decade per Competition` (count distinct `Match ID`).
- Join goal events from the Goal Scorers table to the filtered Results match set using an inner join on the match identity fields: `date`, `home_team`, and `away_team`. Keep goal rows regardless of whether the scorer name is null; the required validity check is that the goal can be assigned to a time segment.
- Assign each goal to a 15-minute `Segment` based on its `minute` value:
  - Convert `minute` to an integer; if it cannot be converted or is negative, the goal should be excluded from segment-based calculations.
  - Use these segment rules (left-closed, right-open for regulation time boundaries):
    - `0-15` for 0–14
    - `15-30` for 15–29
    - `30-45` for 30–44
    - `45-60` for 45–59
    - `60-75` for 60–74
    - `75-90` for 75–89
    - `90+` for 90 and above
- Count `Total Goals` for each combination of `Competition`, `Decade`, and `Segment` (each goal event counts as 1).
- Combine the goal counts with `Matches in a Decade per Competition` (join on `Competition` and `Decade`) and compute `Expected number of Goals` as:
  - `Total Goals / Matches in a Decade per Competition`
  - If the match count is 0, set the expected value to 0.0.
  - Round to 2 decimals using half-up rounding.
- Output the data at the grain of one row per (`Competition`, `Decade`, `Segment`).

## Output

- output_01.csv
  - 6 fields:
    - Competition
    - Decade
    - Segment
    - Total Goals
    - Matches in a Decade per Competition
    - Expected number of Goals