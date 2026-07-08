## Context
For this challenge, we're going to take a look at7 letter words which could be potentially high scoring in Scrabble and work out the likelihood of drawing the tiles needed to create this word. Are we going to make our lives easier by assuming that each tile drawn is an independent event and that the order tiles are drawn is irrelevant? Yes, but equally, if you have the statistical brain to calculate the probabilities as dependent events, considering all the possible orderings then we'd love to see that solution!

## Requirements

- Input the data
- Parse out the information in the Scrabble Scores Input so that there are3 fields:
  - Tile
  - Frequency
  - Points
- Calculate the % Chance of drawing a particular tile and round to2 decimal places
  - Frequency / Total number of tiles
- Split each of the7 letter words into individual letters and count the number of occurrences of each letter
- Join each letter to its scrabble tile
- Update the % chance of drawing a tile based on the number of occurrences in that word
  - If the word contains more occurrences of that letter than the frequency of the tile, set the probability to0 - it is impossible to make this word in Scrabble
  - Remember for independent events, you multiple together probabilities i.e. if a letter appears more than once in a word, you will need to multiple the % chance by itself that many times
- Calculate the total points each word would score
- Calculate the total % chance of drawing all the tiles necessary to create each word
- Filter out words with a0% chance
- Rank the words by their % chance (dense rank)
- Rank the words by their total points (dense rank)
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Points Rank
    - Likelihood Rank
    - 7 letter word
    - % Chance
    - Total Points
