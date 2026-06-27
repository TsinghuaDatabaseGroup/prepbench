## Context

Due to the social distancing and isolation caused by Covid-19, all football games have been postponed across the majority of the world. Therefore to help fill the void, this week’s challenge is all about analysing football team line-ups and in-particular the Premier League games for Liverpool.
We start with a nicely formatted spreadsheet that includes the following:
- Match Details - Including dates, teams, location and formation
- Match Day Squad - 18 players broken down into Starting XI & Substitutes
  - Starting XI - the 11 players who started the game for Liverpool
  - Substitutes - the 7 players who started as a substitute for Liverpool
- Substitution Information - Includes the Player On/Off and the Time
From this we want to answer some questions about the playing time of each of the players.

## Requirements

- Input the data
- Update the headers for Match Details, Starting XI, Substitutes. Ideally this will be done without just renaming each individual header separately. Note, for substitutes the headers follow this pattern, where X is the substitute number:
  - SubX = Substitute Off, the player number who has left the field
  - SubX 1 = Substitute On, the player number who is entering the field
  - SubX 2 = Time of Substitute, the time in the match when the substitution occurred
- Calculate whether or not the player was substituted on/off, what number substitute it was (1/2/3), and at what time in the match it happened.
- If a player was substituted in the 90th minute, then we count this as 1 appearance but 0 mins played, as we don't have information about additional time played in the match.
- Answer the following questions:
  - How many times has each player been in the squad?
  - How many appearances has each player made?
  - What is their minute per games ratio?
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - In Squad
    - Player Name
    - Mins Played
    - Appearances
    - Mins per Game
