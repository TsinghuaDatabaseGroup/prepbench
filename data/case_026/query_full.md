## Context
This challenge is to build an ingredient-level view of a cocktail list using Prep Builder’s native functionality only (i.e., do not use typed calculations and do not “cheat” by copying/pasting formulas). The goal is to split each cocktail’s ingredient list into individual rows, derive each ingredient’s position within its cocktail, and compute the average cocktail price for each ingredient across all cocktails where it appears.

## Requirements
- Input the data from `input_01.csv`.
- Rename the input columns so they are:
  - `Cocktails`
  - `Ingredients`
  - `Cocktail Price`
- Ensure `Cocktail Price` is treated as a numeric field.
- Separate the ingredients so that each cocktail is expanded to one row per ingredient:
  - Split `Ingredients` into a list using a comma (`,`) as the delimiter.
  - Explode/expand the list so each ingredient becomes its own row.
- Work out the position of the ingredients within the list of ingredients in each cocktail:
  - Create `Ingredient Position` as a 1-based index representing the ingredient’s order within that cocktail’s original ingredient list (first ingredient = 1, second = 2, etc.).
- Work out the “average price of the cocktails that ingredient is used in”:
  - For each distinct ingredient, compute the mean of `Cocktail Price` across all rows where that ingredient appears.
  - Store this value as `Avg Ingredient Price` on every row for that ingredient.
  - Round `Avg Ingredient Price` to 9 decimal places.
- Add the original cocktail price back in by keeping `Cocktail Price` alongside the exploded ingredient rows.
- Set the output row ordering deterministically:
  - Sort by `Ingredient Position` ascending.
  - Within each `Ingredient Position`, preserve the original cocktail order from the input file (top to bottom).
- Rename the exploded ingredient column to `Ingredients Split`.
- Output the data exactly with the required fields.

## Output

- output_01.csv
  - 5 fields:
    - Ingredient Position
    - Ingredients Split
    - Cocktail Price
    - Cocktails
    - Avg Ingredient Price