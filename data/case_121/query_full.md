## Context
You are given four input CSV files that together describe a set of “Answer Smash” strings (a name and an answer merged together), a list of possible names, a list of possible category/answer pairs, and the question text for each question number. The goal is to resolve each “Answer Smash” back into its corresponding **Name** and **Answer**, attach the relevant **Question** text, and output a streamlined table.

## Requirements
- Input the data from the following files:
  - `input_01.csv`: contains at least `Q No` and `Answer Smash` (one row per answer-smash instance to resolve).
  - `input_02.csv`: contains a column `Name` (the list of candidate names).
  - `input_03.csv`: contains at least `Q No` and `Question` (question text lookup by question number).
  - `input_04.csv`: a category dataset that needs to be parsed into separate `Category` and `Answer` fields.

- The category dataset requires some cleaning so that Category and Answer are 2 separate fields:
  - Treat `input_04.csv` as a single-column raw text list (no header).
  - For each row, split the raw text on the **first** colon (`:`) into:
    - `Category` = text before the first colon
    - `Answer` = text after the first colon
  - Use the resulting `Answer` values as the candidate answer list for matching (the `Category` field does not need to appear in the final output).

- Join the datasets together, making sure to keep an eye on row counts:
  - The output must have the same number of rows as `input_01.csv` (one output row per `input_01.csv` row).
  - Bring in `Question` from `input_03.csv` by matching on `Q No`. If multiple rows exist for a given `Q No`, use the first matching `Question`.

- Filter the data so that each answer smash is matched with the corresponding name and answer:
  - For each row in `input_01.csv`, attempt to find a matching `(Name, Answer)` pair such that combining them reproduces the `Answer Smash`.
  - Generate candidate “smashed” strings from all combinations of:
    - each `Name` from `input_02.csv`, and
    - each `Answer` parsed from `input_04.csv`.
  - The primary “smash” construction must account for possible overlap between the end of `Name` and the start of `Answer`:
    - Find the largest overlap length `k` (possibly 0) such that the suffix of `Name` of length `k` equals the prefix of `Answer` of length `k` when compared case-insensitively.
    - Construct the candidate smashed string as: `Name + Answer[k:]`.
  - Compare the constructed candidate smashed string to the given `Answer Smash` case-insensitively to determine a match.
  - If no match is found using the overlap-aware construction, perform a fallback match attempt using direct concatenation `Name + Answer` (case-insensitive comparison).
  - If multiple matches are possible, select the first match encountered when iterating names in their input order and answers in their input order.
  - If no match is found after both attempts, leave `Name` and `Answer` as empty strings for that row.

- Remove unnecessary columns:
  - The final dataset must contain only the required output fields listed below.

- Output the data:
  - Sort the final output by `Q No` in ascending order.
  - Write the result to the required output file.

## Output

- output_01.csv
  - 5 fields:
    - Q No
    - Question
    - Answer
    - Name
    - Answer Smash