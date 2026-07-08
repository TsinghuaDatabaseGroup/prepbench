## Context

You have three input tables: (1) a master list of surf sites with their attributes (directions, reliability, board suitability, skill levels, rating, etc.), (2) a table that provides each site’s surf season, and (3) a table of people (“preppers”) with their surfing requirements. The goal is to determine, for each person, the single best-matching surf site based on fit to their requirements and then ranking by site quality.

## Requirements

- Input the data
- Input Data
- Find a way to join all three tables together
  - Use `input_01.csv` as the primary surf-site attributes table.
  - Use `input_02.csv` as the source for each site’s `Surf Season`.
    - Create/derive a join key named `Surf Site` from `input_02.csv`’s `Site` field by removing the literal suffix ` - South Devon`.
    - Join `input_01.csv` to `input_02.csv` with a **left join** on `Surf Site`, bringing `Surf Season` onto the surf-site records (sites without a matching season remain included with a missing `Surf Season`).
  - Use `input_03.csv` as the people requirements table.
  - Combine people with sites by pairing each person with every site (cross join) and then filtering to only the suitable person–site matches (defined below).
- Identify which locations would be suitable for each person
  - A surf site is suitable for a person only if **all** of the following are true:
    - **Skill match:** the person’s `Skill` value is included in the site’s `Skill Level` list. Treat `Skill Level` as a comma+space separated list (split on `", "`).
    - **Season match:** the person’s `Season` and the site’s `Surf Season` share at least one season in common. Treat each field as a comma-separated list (split on `","`, trimming surrounding spaces per item) and require a non-empty intersection.
    - **Board match:** the person’s `Board Type` and the site’s `Boards` share at least one board type in common. Treat each field as a comma-separated list (split on `","`, trimming surrounding spaces per item) and require a non-empty intersection.
- Watch out for any duplicated person & site combinations
  - After generating suitable matches, remove duplicate rows based on the pair (`Name`, `Surf Site`), keeping a single record per person–site pair.
- Rank the top sites in terms of rating for each person. If there is a tie, then use the reliability metric where:
  - Rarely Breaks (Worst)
  - Inconsistent
  - Fairly Inconsistent
  - Fairly Consistent
  - Very Consistent (Best)
  - For each person (`Name`), rank candidate sites by:
    1) `Rating` descending (higher is better)
    2) `Reliability` descending using the ordered scale above (Very Consistent best → Rarely Breaks worst)
  - Select the **single top-ranked** surf site per person after applying the ranking and tie-break rules.
- Output the data
  - The output must have **one row per person** (one best site per `Name`) and contain exactly the specified fields.

## Output

- output_01.csv
  - 10 fields:
    - Name
    - Surf Site
    - Swell Direction
    - Reliability
    - Wind Direction
    - Type
    - Boards
    - Skill Level
    - Surf Season
    - Rating