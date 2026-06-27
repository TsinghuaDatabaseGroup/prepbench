## Context
You are given Our World in Data life expectancy time series and a separate country-to-continent lookup. The goal is to compare each country’s life expectancy to its continent-level life expectancy over time, compute summary metrics for 1950–2020, and report the top three countries per continent by percentage increase in life expectancy from 1950 to 2020.

## Requirements
- Input the data from two tables:
  - A life expectancy table containing at least `Entity`, `Year`, and one life expectancy measure (use the provided “life expectancy at birth” measure).
  - A country-to-continent mapping table containing `Country` and `Continent`.
- Standardize the life expectancy data to the fields:
  - `Entity` (name of country or continent as represented in the life expectancy table)
  - `Year`
  - `LE` (life expectancy at birth measure)
- Attach continents to country life expectancy series:
  - Perform an **inner join** between the mapping table and the life expectancy table where `Country` (mapping) equals `Entity` (life expectancy).
  - Keep `Country`, `Continent`, `Year`, and the country life expectancy value; name this country value `Country: Life expectancy at birth`.
- Obtain the continent life expectancy series (do not compute an average across countries):
  - Identify the set of continent names present in the mapping table (`Continent` values).
  - Filter the life expectancy table to rows whose `Entity` is one of those continent names.
  - Rename `Entity` to `Continent`, and rename `LE` to `Continent: Life expectancy at birth`.
- Align country rows to their continent’s life expectancy for the same year:
  - **Left join** the country-level dataset to the continent-level dataset on `Continent` and `Year`.
  - Retain the continent life expectancy as `Continent: Life expectancy at birth` (it may be missing for some country-years due to no matching continent-year).
- Filter the aligned dataset to include only years **from 1950 to 2020 inclusive**.
- For each country-year row in the filtered dataset, compute an indicator:
  - `Above Continent Avg? = 1` if `Country: Life expectancy at birth` is strictly greater than `Continent: Life expectancy at birth`, otherwise `0`.
- Compute “% Years Above Continent Avg” for each `(Continent, Country)`:
  - Numerator: sum of `Above Continent Avg?` across all available rows for that country between 1950 and 2020 (inclusive).
  - Denominator: count of available year rows for that country between 1950 and 2020 (inclusive).
  - Percentage formula: `100 * numerator / denominator`.
  - Round to the nearest **one decimal place**.
- Compute “% Change” in life expectancy for each `(Continent, Country)` between 1950 and 2020:
  - Extract the country life expectancy value in year 1950 (`LE_1950`) and in year 2020 (`LE_2020`) from the filtered dataset.
  - Keep only countries that have **both** a 1950 and a 2020 value (i.e., compute % change only when both endpoints exist).
  - Percentage change formula: `((LE_2020 - LE_1950) * 100 / LE_1950)`.
  - Round to the nearest **one decimal place**.
- Combine the two metrics for each `(Continent, Country)`:
  - Left join the % change results to the "% Years Above Continent Avg" results on `Continent` and `Country`.
- Select the top three countries in each continent by “% Change”:
  - Within each continent, sort by `% Change` descending; break ties by `Country` ascending.
  - Assign `Rank` within each continent starting at 1 in this sorted order.
  - Keep only ranks 1–3 per continent.
- Output the final table with exactly the required columns and types:
  - `Rank` must be an integer.
  - All percentages must be rounded to one decimal place as specified.
- Output the data.

## Output

- output_01.csv
  - 5 fields:
    - Continent
    - Rank
    - Country
    - % Years Above Continent Avg
    - % Change