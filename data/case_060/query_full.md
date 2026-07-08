## Context
Prepare spider measurement data in a structure suitable for building spider (radar) charts by producing one normalised trait value per species, based on average measurements and scaled consistently across species for each trait.

## Requirements
- Input the data from `input_01.csv`.
- Treat the following six measurement fields as the set of required traits:
  - `Total_body_length`
  - `Prosoma_length`
  - `Prosoma_width`
  - `Prosoma_height`
  - `Tibia_I_length`
  - `Fang_length`
- Filter the dataset to retain only specimens (rows) that have a valid measurement for **every** trait listed above:
  - Exclude any specimen where any trait measurement is missing.
  - Exclude any specimen where any trait measurement contains an asterisk (`*`).
  - Exclude any specimen where any trait measurement is not a valid numeric value (i.e., cannot be converted to a number).
- Clean up fields containing underscores (`_`) by replacing underscores with spaces for:
  - `Species`
  - The trait name used in the final output (derived from the trait column names).
- Restrict analysis to species for which measurements were recorded for **at least 10 specimens** (i.e., at least 10 rows remaining for that species after the specimen-level filtering above).
- Aggregate the filtered data to species level by computing the **mean** of each of the six trait measurements for each species.
- Reshape the aggregated data to a long format so that each output row represents a single **Species–Trait** combination, with:
  - `Value` = the mean measurement for that species and trait.
  - `Trait` = the trait name (with underscores replaced by spaces).
- For each trait, compute the overall minimum and maximum across all species’ mean values:
  - `Min Value` = minimum `Value` among species for that `Trait`.
  - `Max Value` = maximum `Value` among species for that `Trait`.
- For each Species–Trait row, compute the normalised value using:
  - `Normalised Value = (Value - Min Value) / (Max Value - Min Value)`
  - If `Max Value` equals `Min Value` for a trait, set `Normalised Value` to `0.0` for that trait for all species.
- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Normalised Value
    - Max Value
    - Min Value
    - Value
    - Trait
    - Species