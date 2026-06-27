## Context

You have two input datasets: one listing individual films (including their position within a series and a grouping field), and one listing named trilogies with an associated trilogy ranking. The goal is to produce a film-level output that, for each trilogy, identifies the three films that make up that trilogy, calculates the trilogy’s average rating across those three films, and outputs the trilogy ranking, trilogy name, and film details together.

## Requirements

- Input the data from:
  - `input_01.csv` (films dataset), which includes at minimum: *Number in Series*, *Title*, *Rating*, and *Trilogy Grouping*.
  - `input_02.csv` (trilogies dataset), which includes at minimum: *Trilogy* and *Trilogy Ranking*.

- Split out the *Number in Series* field into *Film Order* and *Total Films in Series*:
  - Treat *Number in Series* as a two-part value separated by `/`.
  - Set *Film Order* to the first part and *Total Films in Series* to the second part, both as integers.

- Ensure *Rating* is numeric so it can be aggregated.

- Remove the word *trilogy* from the *Trilogy* field:
  - Create a cleaned trilogy name by removing a trailing `"trilogy"` (and surrounding whitespace) from the trilogy label.
  - Use this cleaned value as the trilogy name going forward.

- Identify the three films belonging to each trilogy (one trilogy at a time), using the films dataset:
  - **Trilogy-specific title-matching rule definition:**
    - For each trilogy, first obtain the cleaned trilogy name (after removing the trailing "trilogy" word and surrounding whitespace).
    - A film title is considered to match a trilogy if the film's *Title* contains the cleaned trilogy name (or its significant keywords) as a substring, using case-insensitive matching.
    - **Title matching pattern derivation:**
      - For each cleaned trilogy name, derive one or more matching patterns (regular expressions) that identify relevant film titles. The patterns are case-insensitive and use substring matching.
      - When the cleaned trilogy name contains common articles or prepositions (such as "The", "A", "An"), extract the core keywords for matching. The article "The" at the beginning of a trilogy name should be treated as optional in matching (e.g., "The Godfather" matches titles containing "Godfather").
      - Handle spelling variants explicitly (e.g., "Three Colours" should match both "Three Color" and "Three Colour").
      - For trilogy names that correspond to series with alternative titles or naming conventions, include patterns that match those alternatives (e.g., "Dollars" trilogy should match titles containing "Dollars" or "Good, the Bad and the Ugly").
      - For trilogy names that are part of larger franchises, use patterns that distinguish the specific trilogy (e.g., "Star Wars" should match only the original trilogy episodes IV-VI, while "Prequel" should match episodes I-III).
      - If no specific pattern derivation rules apply to a trilogy name, use the cleaned trilogy name itself (with special regex characters escaped) as the matching pattern.
      - Examples of pattern derivations:
        - "Lord of the Rings" → matches titles containing "Lord of the Rings"
        - "The Godfather" → matches titles containing "Godfather"
        - "The Dark Knight" → matches titles containing "Dark Knight" or "Batman Begins"
        - "Dollars" → matches titles containing "Dollars" or "Good, the Bad and the Ugly"
        - "Three Colours" → matches titles containing "Three Colou?rs?:? (Blue|White|Red)" (handling spelling variants and color names)
        - "Star Wars" → matches titles containing "Star Wars: (Return of the Jedi|Episode IV|Episode V)"
        - "Prequel" → matches titles containing "Star Wars: Episode (I|II|III)"
    - The matching is substring-based and case-insensitive, so partial matches within longer titles are acceptable (e.g., "The Lord of the Rings: The Two Towers" matches "Lord of the Rings").
  - **Grouping selection process:**
    - For each trilogy, determine which *Trilogy Grouping* in the films dataset most strongly corresponds to that trilogy:
      - Apply the title-matching patterns (as defined above) to all film titles within each grouping.
      - Count how many film titles in each grouping match at least one of the patterns.
      - Use the *Trilogy Grouping* with the highest count of matching titles as the "best" grouping for that trilogy.
      - If multiple groupings have the same highest count, select the first one encountered when iterating through groupings.
    - **Fallback when no matches found in any grouping:**
      - If no titles match in any grouping for that trilogy (i.e., no film titles contain the trilogy's keywords when applying the title-matching patterns within any grouping), the matching process falls back as follows:
        - First, attempt to match titles across the full films dataset (i.e., without restricting to a single grouping) using the same title-matching patterns. If matches are found, use those matched films directly (skip grouping selection).
        - If still no titles match via the title-matching patterns across the entire dataset, use the cleaned trilogy name itself (with special regex characters escaped) as a fallback pattern and attempt matching again across the full films dataset. If matches are found, use those matched films directly.
        - If no matches are found even with the fallback pattern, this indicates that the trilogy cannot be matched to any films using title-based rules. In this case, the process should still attempt to identify films by selecting a grouping, but since no grouping can be determined by title matching, select the grouping that contains the most films (or if multiple groupings have the same maximum count, select the first one encountered). All films in the selected grouping are then considered for selection without title-matching prioritization.
  - **Film selection from the best grouping:**
    - From the selected "best" grouping (or from the matched films if fallback matching was used), choose up to three films to represent the trilogy:
      - **If the grouping was selected via title matching (normal case):**
        - First, identify all films in the grouping whose titles match at least one of the trilogy's title-matching patterns.
        - If there are 3 or more matching films:
          - Sort the matching films by ascending *Film Order*, then by *Title* (alphabetical).
          - Select the first three films after sorting.
        - If there are fewer than 3 matching films:
          - Sort all films in the grouping by: (1) whether the title matches the patterns (matched films first), (2) ascending *Film Order*, (3) *Title* (alphabetical).
          - Select the first three films after sorting.
      - **If films were matched via fallback (no grouping was selected):**
        - Sort the matched films by ascending *Film Order*, then by *Title* (alphabetical).
        - Select the first three films after sorting.
      - **If no grouping could be determined and no films were matched (extreme fallback case):**
        - From the grouping selected by film count (as described in the fallback section above), sort all films by ascending *Film Order*, then by *Title* (alphabetical).
        - Select the first three films after sorting.
    - The resulting grain should be one row per selected film, with up to three rows per trilogy.

- Work out the average rating for each trilogy:
  - Compute the mean of *Rating* across the three selected films for that trilogy.
  - Round the trilogy average to 1 decimal place for the final output field *Trilogy Average*.
  - Do not round ratings prior to calculating the average.

- Trilogy ranking:
  - Use the *Trilogy Ranking* provided in the trilogies dataset as the trilogy’s ranking value in the output.
  - Attach this *Trilogy Ranking* to each of the three selected film rows for the corresponding trilogy.

- Bring the two datasets together:
  - Combine trilogy metadata (cleaned *Trilogy* name and *Trilogy Ranking*) with the selected film rows for that trilogy, and attach the computed *Trilogy Average* to each selected film row.

- Output formatting:
  - Output exactly the fields listed below.
  - Sort the final output by *Trilogy Ranking* (ascending), then *Film Order* (ascending), then *Title* (ascending), to produce a stable row order.

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