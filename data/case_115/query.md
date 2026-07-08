## Context

If you are a fan of football or have been following any of the latest news then you would have probably heard about the proposed new 'Super League' that was planned with a selection of European clubs. This would have involved a group of 12 teams playing in a competition each year without having to qualify or be relegated. The lack of fair competition between other clubs has caused an uproar among fans, players, media outlets, football associations, and even the UK government! The 'big 6' English teams to propose the Super League were Arsenal, Chelsea, Liverpool, Manchester United, Manchester City, and Tottenham Hotspur. One of the ideas to try and discourage the clubs from proceeding with the new league, was to threaten the English teams with being expelled from the English Premier League. The challenge this week is to try and understand how the current league table would change if these clubs were to be 'kicked out'.

## Requirements

- Input the data
- Calculate the Total Points for each team. The points are as follows:
  - Win -3 Points
  - Draw -1 Point
  - Lose -0 Points
- Calculate the goal difference for each team. Goal difference is the difference between goals scored and goals conceded.
- Calculate the current rank/position of each team. This is based on Total Points (high to low) and in a case of a tie then Goal Difference (high to low).
- The current league table is our first output.
- Assuming that the 'Big 6' didn't play any games this season, recalculate the league table.
- After removing the 6 clubs, how has the position changed for the remaining clubs?
- The updated league table is the second output.
- Bonus - Think about features in Tableau Prep to make this repeatable process easier!
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Position
    - Team
    - Total Games Played
    - Total Points
    - Goal Difference

- output_02.csv
  - 6 fields:
    - Position Change
    - Position 
    - Team
    - Total Games Played
    - Total Points
    - Goal Difference
