## Context
There are a couple of techniques that I use when Preppin' my Data that aren't quite native in Tableau Prep yet. So I'm curious to set a challenge which requires them and see the different work arounds that people come up with!
1. Splitting up a string into individual characters, sometimes referred to as tokenising. Currently you need to have a specific delimiter when splitting a field - what if I wanted to specify the length of each chunk that I want the string to be split into?
2. Concatenating strings when aggregating. Currently you can only count the values or return the min or the max, but sometimes I'd rather concatenate the multiple values!
To play with these techniques, we're looking at ciphers for this week's challenge. You've received an encrypted message and need to decode it using the provided cipher!

## Requirements

- Input the data
- Find a way to split each character of the encrypted message onto a separate line.
  - Make sure you retain the original order of the message!
- Use the cipher to decode the message.
- Concatenate the individual decoded characters back into a single string.
  - Make sure those spaces haven't become nulls!
- Output the data

## Output

- output_01.csv
  - 1 fields:
    - Decoded Message
