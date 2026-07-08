## Context
You have three input datasets:
1) A cocktail list with each cocktail’s selling price and a recipe expressed as ingredient measurements.
2) Ingredient sourcing information that gives the purchase price per bottle, the bottle size (in ml), and the currency of that price.
3) Currency conversion rates that define how to convert each sourcing currency into GBP.

The goal is to calculate, for each cocktail, the total ingredient cost in GBP and the resulting profit margin (selling price minus cost).

## Requirements
- Input the data from the three CSV files:
  - `input_01.csv` (cocktails), containing at least: `Cocktail`, `Price (£)`, and `Recipe (ml)`.
  - `input_02.csv` (sourcing), containing at least: `Ingredient`, `Price`, `ml per Bottle`, and `Currency`.
  - `input_03.csv` (conversion rates), containing at least: `Currency` and `Conversion Rate £`.

- Interpret the conversion rate as: **(Conversion Rate £) units of the source currency equal 1 GBP**.  
  - Convert an ingredient bottle price to GBP as:  
    `price_gbp_per_bottle = Price / (Conversion Rate £)`
  - Then compute a GBP unit cost per ml as:  
    `price_gbp_per_ml = price_gbp_per_bottle / (ml per Bottle)`

- Split out the cocktail recipes into ingredient-level rows (a “long” format):
  - Treat each cocktail’s `Recipe (ml)` as a semicolon-separated list of parts.
  - Each part must contain a single ingredient and quantity in the form `Ingredient: <number>ml`.
  - For each valid part, create one row with:
    - the cocktail name,
    - the cocktail selling price (from `Price (£)`),
    - the ingredient name,
    - the numeric ml quantity required for that ingredient.
  - Ignore recipe parts that are empty, do not contain the `:` separator, or do not yield a numeric ml quantity after removing the `ml` unit.

- Calculate the price in pounds for the required measurement of each ingredient:
  - Left-join the long recipe rows to the sourcing-derived `price_gbp_per_ml` on `Ingredient`.
  - For each long row, compute the ingredient cost contribution:  
    `cost_component = price_gbp_per_ml * ml_needed`

- Find the total cost of each cocktail:
  - Group by `Cocktail` and the cocktail `Price` and sum `cost_component` to produce `Cost`.
  - Each output row represents one `(Cocktail, Price)` combination with a computed total ingredient cost derived from the parsed recipe rows. (Cocktails with no parsed recipe items will not produce an output row.)

- Include a calculated field for the profit margin:
  - `Margin = Price - Cost`

- Round all numeric fields in the final output (`Margin`, `Cost`, `Price`) to 2 decimal places.

- Output the data exactly as specified below.

## Output

- output_01.csv
  - 4 fields:
    - Margin
    - Cost
    - Cocktail
    - Price