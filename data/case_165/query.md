## Context
As I've mentioned before in a previous challenge, I'm a big fan of a quiz show called Richard Osman's House of Games. However, I've often found the way that they decide the overall winner of the week a little troubling. Each day the player who has scored the most, will receive 4 points, 2nd place will receive 3 points, 3rd place will receive 2 points and last place will receive one point. These points will be added up across the week to determine the overall winner, but with a twist! Each Friday double points are awarded so 1st place receives 8 points and so on. This leads me to wondering:
- Would there be a different winner if there was no double points Friday?
- What about if participants weren't ranked at the end of each day and they had a running total score across the week instead, would that lead to a different winner?
- What about doubling the scores on the Friday, instead of the points awarded?

## Requirements

- Input the data
- Only keep relevant fields and rename certain fields to remove duplication
  - Ser. becomes Series
  - Wk. becomes Week
  - T becomes Tu
  - T 1 becomes Th
  - Total becomes Score
  - Week becomes Points
  - Week 1 becomes Rank
- Filter the data to remove Series that have a null value, or are preceded by an 'N'
- Calculate the Points without double points Friday
  - Rank the players based on this new field
  - Create a field to determine if there has been a change in winner for that particular Series and Week
- Rank the players based on their Score instead
  - Create a field to determine if there has been a change in winner for that particular Series and Week
- Calculate the Score if the score on Friday was doubled (instead of the Points)
  - Rank the players based on this new field
  - Create a field to determine if there has been a change in winner for that particular Series and Week
- Remove unnecessary fields
- Output the data

## Output

- output_01.csv
  - 14 fields:
    - Series
    - Week
    - Player
    - Original Rank
    - Rank without double points Friday
    - Change in winner with no double points Friday?
    - Rank based on Score
    - Change in winner based on Score?
    - Rank if Double Score Friday
    - Change in winner if Double Score Friday?
    - Score
    - Points
    - Score if double Friday
    - Points without double points Friday
