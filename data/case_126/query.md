## Context

This challenge simulates the NBA Draft Lottery, a process that determines the top draft picks for teams that did not make the playoffs. The lottery gives teams with poorer records a better chance at securing a top pick.

You are provided with three datasets to perform this simulation:
- **Lottery Odds:** A table detailing the percentage chance for each team (seeds 1–14) to win each of the first four picks. Columns `1`, `2`, `3`, `4` contain the odds per pick.
- **Lottery Combinations:** A scaffold of 1,000 numbers (1–1000), representing the possible outcomes of a lottery draw.
- **Team Seeding:** A list of the 14 participating teams and their original seeds.

## Requirements

- Input the data.
- Model the lottery probabilities for each of the first four picks independently:
  - For pick `1`, use column `1` to create a mapping from the 1,000 combinations to teams based on cumulative probability (e.g., 14% → 140 numbers).
  - For pick `2`, use column `2` to build its own mapping; for pick `3`, use column `3`; for pick `4`, use column `4`.
  - Note: Teams are not removed between picks 1–4; each pick is evaluated independently against its own column of odds.
- Use the following predefined winning numbers to determine the lottery winners:
  - Pick 1 → winning number: `282`
  - Pick 2 → winning number: `95`
  - Pick 3 → winning number: `378`
  - Pick 4 → winning number: `48`
- Allocate the remaining picks (5–14) by original seed order (1 through 14), regardless of whether a team appeared in picks 1–4.
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Actual Pick
    - Original
    - Team
