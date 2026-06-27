## Context
You are working with two public datasets (population and country land area) to quantify how population density has changed over the last 21 years. The objective is to identify (a) the countries with the highest population density in 2021 and (b) the countries with the largest percentage increase in population density between 2000 and 2021.

## Requirements
- Input the data.

- Population data (population by country across multiple years):
  - Read the population file in a way that ensures the true column headers are treated as headers (i.e., ignore any leading metadata rows so that the header row is correctly interpreted).
  - Keep only the country identifier and the year columns needed to produce a long (row-wise) time series; remove other descriptive/code fields.
  - Trim leading and trailing spaces from country names.
  - **Exclude aggregate/regional records**: Remove rows where the country name represents a region or aggregate rather than an individual country. Specifically exclude:
    - "Africa Eastern and Southern"
    - "Africa Western and Central"
    - "Arab World"
    - Any other entries that are clearly regional aggregates (not individual countries).
  - **Country-name standardisation**: Apply standardisation to ensure consistent naming for joining. The standardisation should handle common variations:
    - Remove annotations in square brackets (e.g., "[Note 1]" → remove)
    - Remove annotations in parentheses that are not part of the country name (e.g., "(British Crown Dependency)" → remove, but keep "(Denmark)" when it's part of the name like "Greenland (Denmark)")
    - Apply the following specific country name mappings:
      - "Virgin Islands (U.S.)" → "Virgin Islands"
      - "São Tomé and Príncipe" → "Sao Tome and Principe"
      - "Curacao" → "Curaçao"
      - "Jan Mayen" and "Svalbard" → "Svalbard" (group these together)
    - The goal is to ensure that the same country appears with the same name in both datasets after standardisation, enabling successful joins
  - Reshape the wide year columns into a long format with exactly these logical fields:
    - Country name
    - Year (as a numeric year)
    - Population (as numeric)

- Country size data (land area by country):
  - From the field containing land area in both km² and mi², extract only the land area value in km² and convert it to a numeric field.
  - Remove unnecessary fields so that only country name and land area (km²) remain.
  - Clean country names and trim any trailing spaces.
  - **Exclude aggregate/regional records**: Remove rows where the country name represents a region or aggregate rather than an individual country. Specifically exclude:
    - "World"
    - "Antarctica"
    - "Danish Realm Kingdom of Denmark" (this is an aggregate)
    - Any other entries that are clearly regional aggregates (not individual countries).
  - **Country-name standardisation**: Apply the same country-name standardisation approach used for the population dataset so that naming is consistent for joining:
    - Remove annotations in square brackets (e.g., "[Note 1]" → remove)
    - Remove annotations in parentheses that are not part of the country name (e.g., "(British Crown Dependency)" → remove, but keep "(Denmark)" when it's part of the name like "Greenland (Denmark)")
    - Standardise common country name variations to match the canonical form used in the population dataset. Use the same canonical form for each country across both datasets.
  - **Country grouping and merging**: Apply the following specific merging rules (and only these rules):
    - Group "Jersey (British Crown Dependency)" and "Guernsey (British Crown Dependency)" together to make "Channel Islands"
    - If multiple rows map to the same resulting country name after standardisation, aggregate land area by summing land area (km²) to produce one land-area value per country.
    - **No other merging rules apply**: Do not merge other territories with their parent countries (e.g., do not merge "Greenland (Denmark)" with "Denmark", keep them as separate entities if both appear in the data).

- Combine the datasets:
  - Join the population-long dataset to the country-size dataset using an inner join on the standardised country name so that only countries present in both sources are retained (i.e., exclude countries/regions that do not match in both datasets).
  - Note: The exclusion of aggregate records (World, regional aggregates, etc.) should have been handled in the previous steps. If any aggregate records remain, they should be excluded at this stage as well.

- Calculate population density:
  - For each country-year row after the join, compute:
    - **Population Density = Population / Land area (km²)**
  - Round the computed population density to 12 decimal places for downstream calculations.

- Year comparison parameters and filtering:
  - Create two parameters to allow choosing which years to compare:
    - One parameter for the more recent year (include a small set of example selectable values, including 2021).
    - One parameter for the less recent year (include a small set of example selectable values, including 2000).
  - Set these parameters to **2000** (less recent) and **2021** (more recent).
  - Filter the dataset to only these two years.
  - Pivot/reshape so that the grain becomes **one row per country**, with two separate fields:
    - Population Density 2000
    - Population Density 2021
  - (At this stage the dataset should contain 215 rows in total, one per country retained after the inner join and exclusions.)

- Change and ranking calculations:
  - Compute the percentage change in population density from 2000 to 2021 as:
    - **% Change in Population Density = 100 * (Population Density 2021 − Population Density 2000) / Population Density 2000**
  - Create a rank for **% Change in Population Density** such that the country with the greatest percentage change has rank 1. Use “competition ranking” (ties share the minimum rank).
  - Create another rank for **Population Density 2021** such that the country with the highest density in 2021 has rank 1. Use the same tie handling.
  - Identify:
    - The top 10 countries by Population Density 2021.
    - The top 10 countries by % Change in Population Density (2000–2021).
  - For the final CSV outputs, format numeric values by rounding to 9 decimal places and then removing trailing zeros (and any trailing decimal point if the value becomes an integer).

- Output the data as specified below.

## Output

- output_01.csv
  - 3 fields:
    - Country
    - Population Density 2021
    - Rank Population Density 2021

- output_02.csv
  - 5 fields:
    - Country
    - Population Density 2000
    - Population Density 2021
    - % Change in Population Density
    - Rank % Change