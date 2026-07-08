## Context
Build a workflow that checks, for each row of a provided word pair, whether the two words are anagrams of each other (inspired by an Alteryx Weekly Challenge and using words related to Tableau Prep / Preppin Data).

## Requirements
- Input the data.
  - Read `inputs/input_01.csv`, where each row contains two text fields: `Word 1` and `Word 2`.
  - The output grain must remain one row per input row (each original word pair is evaluated independently).

- Determine whether the words are anagrams, following these rules:
  - Anagrams are formed by re-arranging the letters of the other word on the same row.
  - Each word is treated as a single word (i.e., evaluate the letters within each provided string).
  - No letter can be used more than once, and all letters must be used; therefore the two words must have the same length to be anagrams.
  - Evaluate anagram status case-insensitively and ignoring leading/trailing whitespace:
    - Normalize `Word 1` and `Word 2` by converting to lowercase and trimming leading/trailing spaces.
    - If the normalized words have different lengths, the result is not an anagram.
    - Otherwise, sort the characters of each normalized word and compare the sorted character sequences; if they match, the words are anagrams.
  - Create the field `Anagram?` with:
    - `Yes` if the two words are anagrams under the rules above
    - `No` otherwise

- Output the data.
  - Write a single output file containing only the required fields.

## Output

- output_01.csv
  - 3 fields:
    - Word 1
    - Word 2
    - Anagram?