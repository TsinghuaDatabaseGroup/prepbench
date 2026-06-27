## Context
Convert a Roman numeral into its integer value, taking into account that character ordering affects whether a symbol is added or subtracted.

## Requirements
- Input the data.
- Use `input_01.csv` as the source of the Roman numeral to convert:
  - Read the value from the `Number` field and treat it as a single Roman-numeral string to translate (i.e., produce one final numeric result for that input value).
- Find a way to split the Roman numeral into individual characters:
  - Create one row per character in the Roman-numeral string, preserving left-to-right order.
  - Use `input_03.csv` as a scaffold to generate the needed number of rows: take the first *N* scaffold rows, where *N* is the length of the Roman-numeral string.
  - Derive a 0-based `Position` for each character as `Scaffold - 1`, and assign the character at that position from the Roman-numeral string.
- Join the information relating to Roman Numeral values:
  - Use `input_02.csv` as the mapping table from `Roman Numeral` (single-character symbol) to `Numeric Equivalent`.
  - Left-join the per-character rows to the mapping on `Character = Roman Numeral` so each character row has its `Numeric Equivalent` when available.
- Depending on the ordering of characters in the Roman Numeral, some of these values will need a negative multiplier:
  - For each character row, look up the numeric value of the *next* character in sequence (use 0 for the last character’s “next” value).
  - If the current character’s `Numeric Equivalent` is strictly less than the next character’s `Numeric Equivalent`, multiply the current value by `-1`; otherwise keep it positive.
  - If a character has no mapped numeric value, it should contribute no value to the final sum.
- Aggregate the values to complete the translation from Roman Numeral to number:
  - Sum the adjusted per-character values across the entire string to produce the final `Numeric Equivalent`.
  - Ensure the final `Numeric Equivalent` is an integer.
- Output the data.

## Output

- output_01.csv
  - 2 fields:
    - Number
    - Numeric Equivalent