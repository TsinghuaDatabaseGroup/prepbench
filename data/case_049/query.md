## Context

This week’s challenge is a simple concept that’s tricky to execute: we want to take the current results from the 2019/20 NBA season (as of Jan 6th, 2020 at 11:00AM GMT+0) and produce two league tables: one for the Eastern Conference and one for the Western Conference. The input has one file with 5 sheets: Team List, October, November, December, January. Team List contains the details of the conference and division for each team, whilst the other sheets contain the results of all the games so far. January's sheet has some empty results as those games have not yet been played.

## Requirements

- Input the data
- For each team we're looking to discover the following information:
  - **Rank**: Rank for each team within their conference.
  - **W**: Wins for each team.
  - **L**: Losses for each team.
  - **Pct**: Win percentage for each team.
  - **Conf**: The wins and losses for each team against teams within the same conference only.
  - **Home**: The wins and losses for home games for each team.
  - **Away**: The wins and losses for away games for each team.
  - **L10**: The wins and losses for the last (most recently played) 10 games for each team.
  - **Strk**: The current winning or losing streak that each team is on.
- The only column not required for this challenge is the **GB** (games behind).
- After producing these pieces of information, split the teams into two separate outputs - one for each conference.
- Output the data

## Output

- output_01.csv
  - 10 fields:
    - Rank
    - Team
    - W
    - L
    - Pct
    - Conf
    - Home
    - Away
    - L10
    - Strk

- output_02.csv
  - 10 fields:
    - Rank
    - Team
    - W
    - L
    - Pct
    - Conf
    - Home
    - Away
    - L10
    - Strk
