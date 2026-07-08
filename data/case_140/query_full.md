## Context

You are preparing a season-by-season performance table for a football club across multiple historical league systems. The goal is to standardize fields, flag seasons affected by special circumstances (including wartime gaps), and derive a season “Outcome” indicating promotion/relegation status relative to the next recorded competitive season.

## Requirements

- Input the data.
  - Read `input_01.csv` as a whitespace-delimited file (fields are separated by runs of spaces, not a single fixed delimiter).
  - Treat the input as one row per season in chronological order as it appears in the file.

- Standardize field names and ensure the points column is named correctly.
  - Rename `SEASON` to `Season` and `LEAGUE` to `League`.
  - The input contains two “P” measures (played and points). Rename the *penultimate* “P” (the points column; in Prep it appears as `P 1`) to `Pts`, keeping the other `P` as matches played.

- Exclude null rows.
  - Remove rows that are completely empty (i.e., rows with no populated fields).

- Create a `Special Circumstances` field with the following categories, and apply them deterministically:
  - `Abandoned due to WW2` for season `1939-40`.
  - `Incomplete` for the most recent season row (the season `2021-22`) and, more generally, for any season row where all match/stat fields (`P`, `W`, `D`, `L`, `F`, `A`, `Pts`) are missing.
  - `N/A` for all other fully completed competitive seasons.
  - For newly inserted wartime placeholder seasons (see below), set `Special Circumstances` to `WW1` or `WW2` as applicable.

- Ensure the `POS` field only has values for full seasons.
  - Set `POS` to null for any row where `Special Circumstances` is not `N/A` (including `Incomplete`, `Abandoned due to WW2`, `WW1`, and `WW2` placeholder rows).

- Extract numeric values from the leagues to support outcome logic.
  - Map leagues to a numeric “level” used only for comparisons between consecutive seasons:
    - `FL-CH` → 0
    - `FL-1` and `EFL-1` → 1
    - `FL-2` and `EFL-2` → 2
    - `FL-3` and `FL-3S` → 3
    - `FL-4` → 4
    - `SOUTH-1` → 2
    - `SOUTH-2` → 3
    - `NAT-P` → 5

- Create an `Outcome` field with 3 potential values, based on the next season in the original data order (ignoring any inserted wartime placeholder rows for the purpose of the comparison).
  - Compare the current season’s league level to the following season’s league level (using the mapping above):
    - `Promoted` if the next season’s level is numerically lower than the current season’s level.
    - `Relegated` if the next season’s level is numerically higher than the current season’s level.
    - `Same League` if the next season’s level is equal to the current season’s level.
  - Set `Outcome` to `N/A` when:
    - The season is the last competitive season in the original input (no following season to compare).
    - The current season is `Incomplete`.
    - Either the current or following season’s league cannot be mapped to a level.
  - For inserted wartime placeholder rows, set `Outcome` to `N/A`.

- Create new rows for seasons that were missed due to WW1 and WW2, and update fields with relevant values for these new rows.
  - Insert the following WW1 placeholder seasons immediately before the row for season `1914-15`, in this order:
    - `1918-19`, `1917-18`, `1916-17`, `1915-16`
  - Insert the following WW2 placeholder seasons immediately before the row for season `1939-40`, in this order:
    - `1945-46`, `1944-45`, `1943-44`, `1942-43`, `1941-42`, `1940-41`
  - For each inserted placeholder row:
    - Populate `Season` with the inserted season.
    - Set `Special Circumstances` to `WW1` (for the WW1 block) or `WW2` (for the WW2 block).
    - Set `Outcome` to `N/A`.
    - Set `League`, `P`, `W`, `D`, `L`, `F`, `A`, `Pts`, and `POS` to null.

- Output the data.

## Output

- output_01.csv
  - 12 fields:
    - Season
    - Outcome
    - Special Circumstances
    - League
    - P
    - W
    - D
    - L
    - F
    - A
    - Pts
    - POS