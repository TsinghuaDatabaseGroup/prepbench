## Context
We want to analyze Premier League players’ open-play goal scoring across the 2015–2020 period. Build a dataset that calculates each player’s open-play goals (goals excluding penalties and free kicks), derives open-play goals per appearance, and then ranks players overall and within each position.

## Requirements
- Input the data from all provided input files and combine them into a single dataset (append/union rows; do not deduplicate).
- Keep only the fields needed for the outputs and calculations:
  - Name
  - Position
  - Appearances
  - Goals
  - Headed goals
  - Goals with right foot
  - Goals with left foot
  - Penalties scored
  - Freekicks scored
- Remove all goalkeepers from the dataset (exclude rows where Position indicates Goalkeeper).
- Remove all records where Appearances equals 0 (after interpreting Appearances as a numeric field; treat missing/invalid Appearances as not greater than 0 for this filter).
- In this challenge we are interested in goals scored from open play:
  - Rename the original Goals field to **Total Goals** (this is the total goals scored metric used in outputs).
  - Create a new **Open Play Goals** field defined as:
    - **Open Play Goals = Total Goals − Penalties scored − Freekicks scored**
  - Note: penalties and free kicks may also be represented within “Goals with left foot” / “Goals with right foot”; do not adjust those footed-goal fields—only compute open play goals using the formula above.
  - Be careful how null fields are handled: for the purpose of the Open Play Goals calculation and subsequent summations, treat missing values in the goal-related metric fields (Total Goals, Headed goals, Goals with right foot, Goals with left foot, Penalties scored, Freekicks scored) as 0.
- Calculate totals across the whole time period for each player at the **(Name, Position)** level:
  - Sum Appearances, Total Goals, Headed goals, Goals with right foot, Goals with left foot, Penalties scored, and Freekicks scored across all input records for the same Name and Position.
  - Then compute Open Play Goals from these aggregated totals (using the same formula above).
- Create **Open Play Goals/Game** across the whole time period for each (Name, Position) as:
  - **Open Play Goals/Game = Open Play Goals ÷ Appearances**
  - Appearances will be > 0 due to filtering; round Open Play Goals/Game to 9 decimal places.
- Rank and filter for Output 1 (overall ranking):
  - Create **Rank** by ranking all (Name, Position) rows by Open Play Goals in descending order.
  - Use competition-style ranking where tied Open Play Goals share the same rank and the next rank number is skipped (i.e., “min” rank method).
  - Keep only rows with Rank ≤ 20; this automatically includes all ties at rank 20.
- Rank and filter for Output 2 (ranking within position):
  - Create **Rank by Position** by ranking (Name, Position) rows within each Position by Open Play Goals in descending order.
  - Use the same competition-style tie handling (“min” rank method).
  - Keep only rows with Rank by Position ≤ 20 within each Position; this automatically includes all ties at rank 20 for that position.
- Output the data to the two required CSV files with exactly the specified fields.

## Output

- output_01.csv
  - 10 fields:
    - Open Play Goals
    - Goals with right foot
    - Goals with left foot
    - Position
    - Appearances
    - Rank
    - Total Goals
    - Open Play Goals/Game
    - Headed goals
    - Name

- output_02.csv
  - 10 fields:
    - Rank by Position
    - Open Play Goals
    - Goals with right foot
    - Goals with left foot
    - Position
    - Appearances
    - Total Goals
    - Open Play Goals/Game
    - Headed goals
    - Name