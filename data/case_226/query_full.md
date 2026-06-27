## Context
Prep School leadership wants to better understand student performance in the subjects assessed. You have identified that classes 9A and 9B are of particular concern, and you need to classify each student’s subject results into percentile-range bands (quartiles), then flag and report only those students in 9A/9B who are consistently in the lowest band across multiple subjects.

## Requirements
- Input the data.
- Treat `input_02.csv` as one row per student, with `Student ID` plus one numeric grade column per subject. The subjects to process are the subject columns present in this file (and the final report must include English, Economics, and Psychology).
- For each subject independently, split all students’ grades into 4 groups using the following deterministic quartile-style rules:
  - Let `n` be the number of non-missing grades for that subject, and let `n_low = floor(n / 4)`.
  - If `n == 0`, assign the subject’s label as “Interquartile range” for all rows.
  - Otherwise, sort the subject’s grades ascending and define:
    - `bottom_threshold` as the value at position `n_low` in the sorted list (i.e., the `n_low`-th smallest value; when `n_low == 0`, treat `bottom_threshold` as negative infinity).
    - `top_threshold` as the smallest value in the top quartile, i.e., the value at position `n - n_low + 1` in 1-based terms (equivalently, the `n_low`-th largest boundary; when `n_low == 0`, treat `top_threshold` as positive infinity).
    - `median` as the standard median of the full set of grades for that subject (middle value for odd `n`, average of the two middle values for even `n`).
  - Assign each student a tile number per subject:
    - Tile 4 if `grade <= bottom_threshold` (bottom group).
    - Tile 1 if `grade > top_threshold` (top group).
    - Otherwise, tile 2 if `grade <= median`, else tile 3.
- Replace each tile number with the corresponding textual range label by joining to `input_03.csv` (Tiles) on tile number:
  - Use the Tiles mapping from `Number` → `Range`.
  - After replacement, each subject column must contain the tile’s `Range` label (not the numeric tile).
- Join the labeled subject results to the Student Information in `input_01.csv` using a left join on `Student ID` so every student from Student Information is retained (even if subject labels are missing).
- Trim the `Class` field in the Student Information before evaluating class-based logic:
  - Remove leading and trailing whitespace from the `Class` field.
  - If a student's trimmed `Class` is an empty string or missing, that student is not considered to be in class `9A` or `9B`.
- Create a `Flag` column as follows:
  - Set `Flag` to "Yes" only for students whose trimmed `Class` is either `9A` or `9B` **and** who have the label "25th percentile" in **at least 2** of the three reported subjects (English, Economics, Psychology).
  - When counting subjects with "25th percentile" label for the "at least 2" condition:
    - Only count subjects where the student has a valid grade and the resulting label is exactly "25th percentile".
    - Do not count subjects where the student's grade is missing or where the subject label is "Interquartile range" or any other label.
    - If a subject has no valid grades for any student (n == 0), all students receive "Interquartile range" for that subject, and this does not count toward the "at least 2" condition.
  - Otherwise set `Flag` to "No".
- Filter to just the students flagged in the previous step (i.e., keep only rows where `Flag == "Yes"`).
- Output the data, selecting and ordering columns exactly as specified, and sort the final rows by `Class` descending (so 9B before 9A) and then `Full name` ascending.

## Output

- output_01.csv
  - 6 fields:
    - Full name
    - Flag
    - Class
    - English
    - Economics
    - Psychology