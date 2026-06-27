## Context
After Veganuary, you want to review a set of supermarket products and determine which ones are vegan based on their ingredients/allergens text. For this analysis, treat bee by-products (e.g., honey, beeswax) as non-vegan.

## Requirements
- Input the data.
  - Use `input_01.csv` as the product list (one row per product), including at minimum: `Product`, `Description`, and `Ingredients/Allergens`.
  - Use `input_02.csv` as the keyword configuration source, providing:
    - a comma-separated list of animal-derived ingredient terms under `Animal Ingredients`
    - a comma-separated list of E-number codes (numbers only) under `E Numbers`

- Prepare the keyword data.
  - From `Animal Ingredients`, build a list of animal-derived ingredient keywords to search for (treat the terms case-insensitively when matching).
  - From `E Numbers`, add an `"E"` prefix to each E-number code for matching purposes (i.e., treat the configured codes as E-numbers).
  - Conceptually combine (“stack”) animal-ingredient terms and E-number terms into a single keyword set used to evaluate products; however, keep track of whether a match came from an animal-ingredient term versus an E-number term because they are handled differently in the final “Contains” output.
  - Ensure each keyword is treated as an individual item for matching (i.e., not as a single comma-separated string).

- Append the keywords onto the product list.
  - For each product row, evaluate its `Ingredients/Allergens` text against the prepared keywords (this is a logical append: each product is assessed against the same keyword lists).

- Check whether each product contains any non-vegan ingredients.
  - A product is **non-vegan** if either of the following is true:
    - its `Ingredients/Allergens` text contains at least one animal-ingredient keyword, matched case-insensitively as a standalone word/term (avoid matching the keyword as part of a larger word), or
    - its `Ingredients/Allergens` text contains at least one configured E-number, matched case-insensitively, allowing the code to appear with or without the leading `"E"` and allowing optional whitespace between `"E"` and the number.
  - When generating the list of matched animal-ingredient keywords for a product:
    - If either `gelatin` or `gelatine` is found, include **both** `gelatin` and `gelatine` in the matched list.
    - Order the matched animal-ingredient keywords according to this priority sequence (include only those that are matched):  
      `milk`, `whey`, `lactose`, `egg`, `honey`, `gelatin`, `gelatine`, `collagen`, `elastin`, `keratin`, `pepsin`, `isinglass`, `shellac`, `lard`, `aspic`, `beeswax`.

- Prepare a final shopping list of vegan products.
  - Aggregate the products into vegan and non-vegan based on the non-vegan check above (one output row per product).
  - Filter out the non-vegan products so only vegan products remain for the vegan shopping list output.

- Prepare a list explaining why the other products aren't vegan.
  - Keep only non-vegan products.
  - Populate a `Contains` field as a single comma-separated list of the matched **animal-ingredient keywords only** (in the priority order defined above).
    - Note: E-number matches should still cause a product to be classified as non-vegan, but they should **not** be included in the `Contains` list.
  - The final result should be one row per non-vegan product with `Contains` containing the concatenated keyword list (comma-separated).

- Output the data.

## Output

- output_01.csv
  - 2 fields:
    - Product
    - Description

- output_02.csv
  - 3 fields:
    - Product
    - Description
    - Contains