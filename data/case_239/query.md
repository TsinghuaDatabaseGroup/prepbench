## Context

This challenge is inspired by a recent dataset from a Data School client project. It has been reimagined with the fake company Chin & Beard Suds Co.

As you know, C&BSCo has branches all over London. They like to get together every other Sunday for a 5-a-side football tournament. Every time a player plays in a match, their Total Matches number is overwritten and increased by 1. This has caused some issues for the football data nerds who want to do some analysis to see if players who have played more games will score more goals. So we'll need to help them retroactively work out how many matches a player would have played in before the start of each tournament.

## Requirements

- Input the data
- To work out the Experience each player has going into the tournament, we need to know how many matches they played after that match and minus this number from the Total Matches. This will require a running total
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Team
    - Player ID
    - Total Matches
    - Tournament Date
    - Experience at beginning of Tournament
    - Matches Played in Tournament
