## Context

Welcome to week four and in my opinion, I'm three weeks too late for using basketball data. Both Jonathan and I are basketball fans but we have some questions that need solving. Therefore, this week is about using Prep to answer questions using the profile pane (of course you can build a viz if you want to). This is the Profile Pane: [image removed]. The input data comes from ESPN and the way they capture the three major stats on each team's schedule. Hi Points = Most points scored by a single player during the game; Hi Rebounds = Most times a player has recovered possession after a missed shot; Hi Assists = Most times a player has passed the ball to another player who then scored. This data copies in to Excel really badly... We have given you data just about Carl's favourite team, the San Antonio Spurs. You will obviously need to clean-up the data, but can then use some other functions in Prep Builder to help you answer the following questions: 1. In games won by the Spurs, which player most often scores the most points? 2. In games lost by the Spurs, which player most often scores the most points? 3. What combination of players scores the most points, rebounds and assists the most frequently? 4. Which player is the second most frequent at gaining the most assists in a game? 5. With the answer to Q4, where do all these games happen: Home or Away? 6. Which player scored the most points in games in October 2018 the most frequently?

## Requirements

- Input the data
- Fix some date issues!
- Split the "Hi-" categories up so player and value is separate
- Determine whether each game was played by the Spurs: Home or Away
- Determine whether the Spurs won or lost each game
- Get rid of unrequired columns
- Output the data

## Output

- output_01.csv
  - 13 fields:
    - Opponent (clean)
    - HI ASSISTS - Player
    - HI ASSISTS - Value
    - HI REBOUNDS - Player
    - HI REBOUNDS - Value
    - HI POINTS - Player
    - HI POINTS - Value
    - Win or Loss
    - Home or Away
    - True Date
    - OPPONENT
    - RESULT
    - W-L
