## Context

You have two input datasets: one listing individual films and an anonymous `Trilogy Grouping`, and one listing trilogy names with a `Trilogy Ranking`. The goal is to compute the ranking fields from the films dataset, join those rankings to the trilogy-name dataset, and output the film rows with the trilogy metadata.

## Requirements

- Input the data from:
  - `input_01.csv` (films dataset), which includes at minimum: *Number in Series*, *Title*, *Rating*, and *Trilogy Grouping*.
  - `input_02.csv` (trilogies dataset), which includes at minimum: *Trilogy* and *Trilogy Ranking*.

- Split out the *Number in Series* field into *Film Order* and *Total Films in Series*:
  - Treat *Number in Series* as a two-part value separated by `/`.
  - Set *Film Order* to the first part and *Total Films in Series* to the second part, both as integers.

- Ensure *Rating* is numeric so it can be aggregated.

- Work out the average rating for each trilogy grouping:
  - Group the films by `Trilogy Grouping`.
  - Compute the mean `Rating` for each group without rounding before ranking.
  - Round the final output field *Trilogy Average* to 1 decimal place.

- Work out the highest ranking metric for each trilogy grouping:
  - For each `Trilogy Grouping`, compute the highest single-film `Rating` in that group.

- Rank the trilogy groupings:
  - Sort groupings by unrounded average rating descending.
  - Break ties by highest single-film rating descending.
  - If there is still a tie, sort by `Trilogy Grouping` ascending for deterministic output.
  - Assign `Trilogy Ranking` as a 1-based row number after this sort.

- Remove the word *trilogy* from the *Trilogy* field:
  - In `input_02.csv`, remove a trailing `"trilogy"` word and surrounding whitespace from the `Trilogy` value.

- Bring the two datasets together by the ranking fields:
  - Join the ranked film groups to the cleaned trilogy-name dataset on `Trilogy Ranking`.
  - Keep the film-level rows from the matched groups.

- Output formatting:
  - Output exactly the fields listed below.
  - Sort the final output by *Trilogy Ranking* ascending, then *Film Order* ascending, then *Title* ascending.

- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Trilogy Ranking
    - Trilogy
    - Trilogy Average
    - Film Order
    - Title
    - Rating
    - Total Films in Series
