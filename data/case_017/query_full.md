## Context
The goal is to determine the winning candidate under three different voting systems using a set of ballots where each ballot ranks all candidates in order of preference (e.g., a preference string like “ABC” indicates the voter’s 1st, 2nd, and 3rd choices). You will compute the winner under:
1) First Past the Post (FPTP),
2) Alternative Vote (AV / instant-runoff), and
3) Borda Count.

## Requirements
- Input the data.
- Download the data.
- Use the input field **Voting Preferences** as the ranked ballot for each voter, where each character represents a candidate and the leftmost character is the first preference.
- Treat the set of candidates as the distinct candidate letters that appear across all preference strings; let **N** be the number of candidates.

- Calculate the winner if we used a **FPTP** voting system:
  - For each ballot, take the first-preference candidate (the first character of the Voting Preferences string).
  - Count first-preference votes per candidate across all ballots.
  - The FPTP winner is the candidate with the highest first-preference vote count.

- Calculate the winner if we used an **AV (Alternative Vote)** voting system (instant-runoff):
  - Start with all candidates “remaining”.
  - In each round:
    - For every ballot, identify that ballot’s highest-ranked candidate who is still remaining (i.e., the first candidate in the preference order that has not been eliminated).
    - Count these current first-choice votes for each remaining candidate.
    - If any candidate has **strictly more than 50%** of the total number of ballots (using the original total ballot count), that candidate is the winner and the process stops.
    - Otherwise, eliminate the candidate with the fewest current first-choice votes and repeat the round using the updated remaining set.
    - If there is a tie for fewest votes when deciding who to eliminate, eliminate the tied candidate that is earliest in alphabetical/lexicographic order.
  - If the process reaches a single remaining candidate, that candidate is the winner.
  - Note: As there's no way to program loops in Tableau Prep, to discover the AV winner you’ll need to repeat the vote count and candidate deletion steps until a candidate meets the >50% of the vote requirement.

- Calculate the winner if we used a **Borda** voting system:
  - For each ballot, assign points by rank using **N** candidates:
    - Rank 1 receives **N** points, rank 2 receives **N−1** points, …, and rank N receives **1** point.
  - Sum points per candidate across all ballots.
  - The Borda winner is the candidate with the highest total points.
- Output label requirements:
  - In the **Voting System** field, use exactly these values: **FPTP**, **AV**, **Borda**.

#### Notes:
- This week we're expecting to see lots of different methods so please do share them with us on Twitter using the #PreppinData hashtag!
- You should always count votes and points using the tools in Prep, but to filter down to just the winner you can just sort the fields and manually filter the data.
- Bonus Points: design a flow that dynamically filters down to the winner in each voting system. It's a good exercise but our solution won't cover it.
- Output the data.

## Output

- output_01.csv
  - 2 fields:
    - Voting System
    - Winner
