## Context

Rank in Tableau Prep still isn't as easy as it could be. The Prep Development team have been hard at work and will come up with a solution soon so it's the final chance to try to solve how to do a Standard Competition rank in Prep. This form of Rank is actually the default rank within Tableau Desktop so to be able to mimic it is important. Let's look at the differences where the values are 10, 9, 9, 8. Standard Competition: 1, 2, 2, 4; Modified Competition: 1, 3, 3, 4. This week's challenge leads up to one of my favourite sporting tournaments of the year - the Six Nations. For those who don't know, this tournament is where England, France, Wales, Scotland, Ireland and Italy play each other at Rugby. You'll need no Rugby knowledge for this challenge. Just know the winner of the game is the team that scores more points (For) than the opposition (Aga - short for against). At which venues are England the most dominant team? Let's find their best victory (rank based on largest margin), their worst result and average rank based on the margin of victory / defeat.

## Requirements

- Input the data
- Remove the games that have null scores at halftime
- Determine the Standard Competition rank based on Diff (ie margin of victory - the larger the better)
- Using that rank give three statistics per rank:
  - Best game Rank per Venue
  - Worst game Rank per Venue
  - Average Rank per Venue
  - Number of Games played at that venue
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Venue
    - Number of Games
    - Best Rank (Standard Competition)
    - Worst Rank (Standard Competition)
    - Avg. Rank (Standard Competition)
