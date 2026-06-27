## Context
You are scoring a multi-round multiple-choice quiz. Each participant submits their answers for five rounds, and a separate table provides the correct answers for each round. The goal is to compare each participant’s submitted answers to the correct answers, compute per-round and total scores, and assign a leaderboard position based on total score.

## Requirements
- Input the data.
  - Read `input_01.csv` as the participant answer table with one row per participant, containing `Name` and the five round answer fields `Round1`–`Round5`.
  - Read `input_02.csv` as the correct answer table, containing one row per round with fields `Round` (e.g., `Round1`–`Round5`) and `Answers`.

- Identify the participants and the correct answer for each question.
  - For each round, interpret both the participant’s round field and the correct `Answers` field as an ordered list of answers separated by commas.
  - Question alignment is by position in these lists (first item = question 1, second item = question 2, etc.).

- Combine the two input tables.
  - For each participant, associate the correct-answer list for each of the five rounds (`Round1`–`Round5`) from the correct answer table (i.e., a per-round lookup keyed by `Round`), so each participant can be scored against the correct answers for all rounds.

- Calculate how many correct answers per round and in total for each participant.
  - For each round `Round1`–`Round5`, compute the round score as the count of positions where the participant’s answer equals the correct answer for the same position.
  - Only compare answers where both the participant answer and a corresponding correct answer exist at that position (i.e., do not award points beyond the length of the correct answer list).
  - Compute `Total Score` as the sum of the five round scores.

- Assign leaderboard position.
  - Sort participants by `Total Score` in descending order.
  - Create `Position` using dense ranking on `Total Score` (participants with the same total score receive the same position; the next distinct score gets the next consecutive position).

- Output the data.

## Output

- output_01.csv
  - 8 fields:
    - Round1
    - Round2
    - Round3
    - Round4
    - Round5
    - Total Score
    - Position
    - Name