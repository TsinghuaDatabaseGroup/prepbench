## Context

You are preparing a genre-by-format summary of anime performance. The goal is to report, for each combination of genre and content type (TV vs Movie), the typical rating and viewership, the best rating achieved, and a representative “prime example” title.

## Requirements

- Input the data from `input_01.csv`.

- Scope and validity filters:
  - Consider only records where `type` is exactly **TV** or **Movie**.
  - Exclude any record with a missing `rating`.
  - Exclude any record with a missing `genre`.
  - Exclude any record with `members` (viewers) less than **10000**.

- Genre handling:
  - Treat `genre` as a comma-separated list of genres.
  - Split `genre` on commas and explode so that each (anime, single-genre) pairing becomes its own row for downstream grouping. (An anime with multiple genres contributes to multiple genre groups.)

- Aggregation grain:
  - Produce one output row per **(Genre, Type)** combination after the genre split.

- For each (Genre, Type) combination, compute:
  - **Avg Rating**: the mean of `rating` across all rows in the group, rounded to **2** decimal places using **round-half-up** rounding.
  - **Max Rating**: the maximum of `rating` in the group, rounded to **2** decimal places using **round-half-up** rounding.
  - **Avg Viewers**: the mean of `members` across all rows in the group, rounded to **0** decimal places using **round-half-up** rounding, then stored as an integer.

- Prime Example selection:
  - For each (Genre, Type) group, choose a single title name (`name`) as **Prime Example** by sorting within the group using:
    1) `rating` descending  
    2) `members` descending  
    3) `name` ascending  
  - Select the first record after applying this ordering; its `name` becomes **Prime Example** for that (Genre, Type).
  - Attach **Prime Example** to the aggregated (Genre, Type) results via a left join on (Genre, Type) so every aggregated row retains its metrics even if the prime example lookup were to be missing.

- Output the data with these column names exactly:
  - `Genre` (from the exploded genre value)
  - `Type`
  - `Avg Rating`
  - `Max Rating`
  - `Avg Viewers`
  - `Prime Example`

## Output

- output_01.csv
  - 6 fields:
    - Genre
    - Type
    - Avg Rating
    - Max Rating
    - Avg Viewers
    - Prime Example
