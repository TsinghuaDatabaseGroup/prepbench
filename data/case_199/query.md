## Context
In this week's Preppin' Data we're collaborating with #GamesNightViz once more! We're looking at the Major Tiddlywinks Championship results. Before you ask, yes it is a serious game! Here's some terminology you may need to understand part of the challenge: pot-out or potout • the achievement of having all winks of a color in the pot.

## Requirements

- Input the data
- Extract the Event id from the Event field
- Parse the competitor field into Competitor and Association
- For the first Games Output:
  - Reshape the data so we have a row per Game for each Event id and Competitor
  - Potouts are denoted by a * in the Score field. Add a boolean field to indicate whether there has been a Potout
  - Clean the Score field so that fractions are translated to decimals
    - e.g. 2½ should be 2.5
- For the second Results Output:
  - Remove the Games fields
  - Clean the Points field so that fractions are translated to decimals
    - e.g. 2½ should be 2.5
  - Extract the Event Start Date from the description and translate it to a date data type
  - Ensure the field names are easy to understand
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Event id
    - Game Order
    - Competitor Name
    - Score
    - Potout
    - note

- output_02.csv
  - 10 fields:
    - Event id
    - Competitor Name
    - Event
    - Event Start Date
    - Event Description
    - Association
    - Points
    - Wins
    - Losses
    - Ties
