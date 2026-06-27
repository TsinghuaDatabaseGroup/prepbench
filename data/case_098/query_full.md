## Context
Prepare USGA Women’s U.S. Open winner scoring data for a Tableau visualization that uses polygons (squares) to represent each round in each year. The goal is to (1) generate polygon vertex coordinates for four round-based squares per year, sized so that lower scores produce smaller squares, and (2) compute decade-level minimum and maximum scores for reference lines or scaling in the viz.

## Requirements
- Input the data.
  - Use **input_01.csv** as the year-level lookup for tournament details (at minimum: Year, Country, Venue, Location).
  - Use **input_02.csv** as the scoring table (at minimum: Year, Player, Total, Round 1–Round 4, and a “to par” field).
- Join both data tables.
  - Join on **Year** using a **left join** from the scoring table (input_02) to the tournament-details table (input_01), so every scoring record is retained even if tournament details are missing.
  - The join is expected to be one-to-one by Year.
- Calculate par values for each year.
  - Convert Year to an integer.
  - Convert Total and round scores (Round 1–Round 4) to numeric.
  - Convert the “to par” field to a numeric value (“to-par number”):
    - Treat “E” / “Even” as **0**.
    - Otherwise, extract the signed integer value (e.g., -3, +2) if present; if no numeric value is available, the to-par number is null.
  - Compute **Round Par** (par for a single round) as:  
    **Round Par = round( (Total − to-par number) / 4 )**  
    and store it as an integer.
  - (Implied by the above) **Total par** for the tournament year is **4 × Round Par**.
- Reshape to one record per year and round, then compute round-level metrics.
  - Pivot the four round score columns into a long format with:
    - **Round Num** ∈ {“Round 1”, “Round 2”, “Round 3”, “Round 4”}
    - **Round Score** = the corresponding round's score (integer)
  - Compute **Round to Par** as:  
    **Round to Par = Round Score − Round Par**
- Create fields used to place years into a decade grid.
  - Compute **Decade** as: **Decade = floor(Year / 10) × 10**.
  - Compute **Row** to stack decades vertically, indexed from 1 based on the earliest decade present:  
    **Row = ((Decade − min(Decade)) / 10) + 1**
  - Compute **Column** to position years within a decade from 1 to 10:  
    **Column = Year − Decade + 1**
- Create a square (polygon) for each round for each year.
  - Extract **Round Number** as the integer 1–4 from Round Num.
  - Create **Round Colors** from Round Number using the mapping:
    - 1 → “A”, 2 → “B”, 3 → “C”, 4 → “D”
  - For each (Year, Round Num) record, generate **four polygon vertices** labeled **Point1–Point4**, producing 4 rows per round and 16 rows per year.
  - Size squares based on the round score using **sqrt(Round Score)** as the scale factor.
  - For each vertex Point ∈ {Point1, Point2, Point3, Point4}, compute coordinates as:  
    **Y Coordinate Polygon = round( sqrt(Round Score) × y_multiplier, 9 )**  
    **X Coordinate Polygon = round( sqrt(Round Score) × x_multiplier, 9 )**
  - Use the following (y_multiplier, x_multiplier) by **Round Number** and **Point**:

    - **Round 1**
      - Point1: (0, 1)
      - Point2: (0, 0)
      - Point3: (1, 0)
      - Point4: (1, 1)

    - **Round 2**
      - Point1: (-1, 1)
      - Point2: (-1, 0)
      - Point3: (0, 0)
      - Point4: (0, 1)

    - **Round 3**
      - Point1: (-1, 0)
      - Point2: (-1, -1)
      - Point3: (0, -1)
      - Point4: (0, 0)

    - **Round 4**
      - Point1: (0, 0)
      - Point2: (0, -1)
      - Point3: (1, -1)
      - Point4: (1, 0)

  - Ensure output ordering is deterministic by sorting records by:
    1) Point in the order Point1, Point2, Point3, Point4  
    2) Round Num in the order Round 1, Round 2, Round 3, Round 4  
    3) Year descending
- For each Decade, find the highest and lowest total score and round score.
  - **Min/Max Total Score**: group by Decade at the year level (using Total from the joined year record) and compute min(Total) and max(Total).
  - **Min/Max Round Score**: group by Decade at the round level (long/pivoted data) and compute min(Round Score) and max(Round Score).
  - Combine these decade summaries into a single decade-level output, sorted by Decade ascending.
- Output the data.

## Output

- output_01.csv
  - 17 fields:
    - Column
    - Row
    - Decade
    - Round to Par
    - Y Coordinate Polygon
    - X Coordinate Polygon
    - Round Colors
    - Point
    - Round Score
    - Round Num
    - Player
    - Country
    - Venue
    - Location
    - Round Par
    - Total
    - Year

- output_02.csv
  - 5 fields:
    - Decade
    - Min Round Score
    - Max Round Score
    - Min Total Score
    - Max Total Score