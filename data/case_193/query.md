## Context

Recently, my colleague Joe Stokes brought me an interesting challenge that I knew needed to be turned into a Preppin' Data! He was working with sports player training data. Since the athletes wouldn't take part in the same training sessions every single day, this was leading to a lot of gaps in the data. As there was a metric which calculated the average across all sessions for each day, this could lead to some misleading conclusions, with a lot of variation over time. Instead, what we want is to take the value from the previous session, even if the player didn't partake in the session on that day. This helps to keep the average a bit more stable. It also means we have data for every day, even if the player were off sick that day.

## Requirements

- Input the data
- For each player and each session, we want to know what the date is of the next session
  - E.g. for Player1 who had an Agility session on 4th Jan, their next Agility session was 6th Jan - so we have missing data on 5th Jan
- For the most recent training session in the dataset, assign the next session as the maximum date in the dataset
- Scaffold the data so we have a row for each player and each session
  - Careful of duplicates!
- Create a flag to indicate whether the score comes from an actual session, or is carried over from the previous session
- Exclude all weekends (Saturdays & Sundays) from the dataset
  - Players need time off too!
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Flag
    - Player
    - Session
    - Score
    - Session Date
