## Context

A prep school is hosting a disco for Year 5 and Year 6. Each student submitted a song choice, but the DJ will only play songs that receive at least 5 votes. The task is to determine which songs meet the vote threshold, broken out by year group.

## Requirements

- Input the data.
- Combine student contact details with song choices separately for each year group:
  - Join the Year 5 contact details dataset to the Year 5 song choices dataset using **Full Name** as the join key, keeping **all** students from the contact details (left join).
  - Join the Year 6 contact details dataset to the Year 6 song choices dataset using **Full Name** as the join key, keeping **all** students from the contact details (left join).
- Append (union) the joined Year 5 and joined Year 6 results into a single table so votes can be counted across both year groups together.
- Standardize the chosen-song information into a single song field:
  - If both **Song Recommendation** and **Song Choice** exist, use **Song Recommendation** when it is present; otherwise use **Song Choice**.
  - If only one of these columns exists, use the available one as the song value.
  - Carry this standardized value forward as the song field to be counted (it will be output as **Song Recommendation**).
- Count votes at the following grain:
  - One row per **Year Group × Song** combination.
  - Compute the vote count as the **count of Full Name** within each group (including a group for missing/blank song values, if present).
- Using a clean step, rename the resulting vote-count field to **Number of Votes** (i.e., the aggregation result based on counting Full Name should be named Number of Votes).
- Filter to keep only songs with **Number of Votes >= 5**.
- Output only the required fields, and order the results deterministically by:
  1) Year Group (ascending),
  2) Number of Votes (descending),
  3) Song Recommendation (ascending).
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Number of Votes
    - Year Group
    - Song Recommendation