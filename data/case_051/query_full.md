## Context

You are analysing England’s match results from the Six Nations dataset to understand at which venues England have been most dominant. Dominance is measured by the match points differential (`Diff`, i.e., margin of victory/defeat), and venues are summarised using a “Standard Competition” ranking approach (the same style as Tableau Desktop’s default rank where ties share a rank and subsequent ranks are skipped).

## Requirements

- Input the data from `input_01.csv`.
- Remove games that have missing (null) scores at halftime. Specifically, exclude any match where either halftime “for” (`HTf`) or halftime “against” (`HTa`) is null.
- Ensure `Diff` is treated as a numeric field for ranking purposes.
- Determine the **Standard Competition** rank for each remaining game based on `Diff`, where a larger `Diff` is better:
  - Rank all games together (not separately within each venue).
  - The highest `Diff` receives rank 1.
  - If multiple games tie on `Diff`, they all receive the same rank equal to the smallest rank in that tied block (i.e., ties share the “best” rank), and the next rank value is skipped accordingly (standard competition ranking).
- Using that per-game rank, produce venue-level statistics (one output row per `Venue`):
  - **Number of Games**: count of games played at that venue after the halftime-null filter.
  - **Best Rank (Standard Competition)**: minimum (best) rank among games at that venue.
  - **Worst Rank (Standard Competition)**: maximum (worst) rank among games at that venue.
  - **Avg. Rank (Standard Competition)**: arithmetic mean of ranks among games at that venue, rounded to 9 decimal places.
- Format requirements:
  - Output `Best Rank (Standard Competition)` and `Worst Rank (Standard Competition)` as integers.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Venue
    - Number of Games
    - Best Rank (Standard Competition)
    - Worst Rank (Standard Competition)
    - Avg. Rank (Standard Competition)