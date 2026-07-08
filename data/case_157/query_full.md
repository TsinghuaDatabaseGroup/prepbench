## Context
You are analyzing 7-letter Scrabble words to identify potentially high-scoring plays and to estimate how likely it is to draw the exact tiles needed to form each word. The likelihood calculation should assume independent draws (i.e., treat each tile draw as an independent event and ignore draw order), then combine per-letter probabilities to get a word-level likelihood.

## Requirements
- Input the data.
  - Read `input_01.csv` as the list of candidate words (field: `7 letter word`).
  - Read `input_02.csv` as a scaffold of integer positions (field: `Scaffold`).
  - Read `input_03.csv` containing a text field `Scrabble` that encodes Scrabble tile distributions and point values.

- Parse out the information in the Scrabble Scores Input so that there are 3 fields:
  - Tile
  - Frequency
  - Points  
  Specifically, from each `Scrabble` text entry:
  - Extract the point value for that row.
  - Extract each tile letter and its frequency associated with that point value.
  - Produce one row per (Tile, Frequency, Points).

- Calculate the % Chance of drawing a particular tile and round to 2 decimal places
  - Frequency / Total number of tiles  
  Use the total frequency across all parsed tiles as the denominator. Store this rounded per-tile value as `% Chance` and use this rounded value in all subsequent calculations.

- Split each of the 7 letter words into individual letters and count the number of occurrences of each letter.
  - Use the scaffold to generate positions 1 through 7 (filter `Scaffold <= 7`).
  - For each word and each scaffold position, take the character at that 1-based position (skip positions beyond the word length, if any) and treat it as the letter for that position.
  - Convert extracted letters to uppercase.
  - Aggregate to the grain: one row per (`7 letter word`, `Letter`) with `Number of Occurrences` = count of that letter in the word.

- Join each letter to its scrabble tile.
  - Join the letter-count table to the parsed tile table using `Letter = Tile`.
  - Use an inner join; letters that do not match a tile row will not be carried forward to scoring/likelihood calculations (and thus such words will not appear in the final results).

- Update the % chance of drawing a tile based on the number of occurrences in that word.
  - If the word contains more occurrences of that letter than the frequency of the tile, set that letter’s contribution to probability to 0 (i.e., impossible to form).
  - Otherwise, for independent events, compute the per-letter contribution as:  
    `Letter % Chance = (% Chance)^(Number of Occurrences)`  
    (i.e., if a letter appears multiple times, multiply its rounded `% Chance` by itself that many times).

- Calculate the total points each word would score.
  - For each letter row, compute `Points Contribution = Points * Number of Occurrences`.
  - For each `7 letter word`, compute `Total Points = SUM(Points Contribution)`.

- Calculate the total % chance of drawing all the tiles necessary to create each word.
  - For each `7 letter word`, compute `% Chance = PRODUCT(Letter % Chance)` across all letters in the word.

- Filter out words with a 0% chance.
  - Keep only rows where the word-level `% Chance` is strictly greater than 0.

- Rank the words by their % chance (dense rank).
  - Compute `Likelihood Rank` as a dense rank with higher `% Chance` receiving rank 1 (descending order).

- Rank the words by their total points (dense rank).
  - Compute `Points Rank` as a dense rank with higher `Total Points` receiving rank 1 (descending order).

- Output the data.
  - Output exactly the five required fields.
  - Sort the final output by `Points Rank` ascending, then `Likelihood Rank` ascending, then `7 letter word` ascending.

## Output

- output_01.csv
  - 5 fields:
    - Points Rank
    - Likelihood Rank
    - 7 letter word
    - % Chance
    - Total Points