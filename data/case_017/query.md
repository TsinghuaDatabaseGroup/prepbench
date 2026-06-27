## Context
This week’s challenge comes courtesy of Jenny Martin from DS14 of The Data School and her experience in writing a dissertation on how to rig elections different voting systems: We’ve had a lot of votes in recent years and I’m sure everyone’s just about had enough by now. Naively, I used to believe that the process you use to determine the “winner” of a vote was irrelevant, surely they’re all roughly the same? Then I got to university and discovered this depressing theorem: Arrows Impossibility Theorem For elections with 3 or more candidates, there is no voting system that satisfies the following conditions:
- Not a dictatorship
- If everyone ranks A above B, the population should rank A above B
- If C withdraws from the election, the ranking of A and B should not change.

I thought it would be fun to prove this disconcerting truth in Tableau Prep with some common voting systems! There are 3 I would like you all to consider:

1. First Past the Post (the one we currently use in the UK)
   - Everyone picks their favourite candidate.
   - The most commonly picked candidate wins.

2. AV (Alternative Vote)
   - Everyone ranks the candidates in order of preference.
   - If the candidate mostly commonly ranked first is ranked first in more than 50% of the votes, they win.
   - If this is not the case, then the candidate least commonly ranked first is deleted from all the votes and there is a recount.
   - This process of counting and deleting continues until a candidate holds over 50% of the popular vote.

3. Borda Count
   - Everyone ranks the candidates in order of preference.
   - The better the rank, the more points the candidate receives.
     - E.g. if there are 3 candidates, the candidate ranked first gets 3 points and the candidate ranked last gets 1 point.
   - The candidate with the most points wins.

In order to demonstrate the seriousness of the situation, our votes relate to preferences in chocolate:
- A = Aero
- B = Bounty
- C = Crunchie

A vote of “ABC” means A is ranked 1st, B is 2nd, and C is 3rd. Which is ludicrous as obviously Bounty can’t compete with Aeros and Crunchies.

## Requirements
- Input the data
- Download the data.
- Calculate the winner if we used a FPTP voting system.
- Calculate the winner if we used a AV voting system.
- Calculate the winner if we used a Borda voting system.
#### Notes:
- This week we're expecting to see lots of different methods so please do share them with us on Twitter using the #PreppinData hashtag!
- You should always count votes and points using the tools in Prep, but to filter down to just the winner you can just sort the fields and manually filter the data.
- Bonus Points: design a flow that dynamically filters down to the winner in each voting system. It's a good exercise but our solution won't cover it.
- As there's no way to program loops in Tableau Prep, to discover the AV winner you’ll need to repeat the vote count and candidate deletion steps until a candidate meets the >50% of the vote requirement.
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Voting System
    - Winner
