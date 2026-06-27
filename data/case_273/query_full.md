## Context
All data for this two-stage task is provided from a single source workbook and has been supplied as separate input tables/files. The goal is to (1) produce a consolidated wildlife reference table and (2) identify wildlife whose natural habitat temperature ranges fall outside San Diego’s observed temperature range, then prioritize those cases.

## Requirements
### Stage 1 — Build the consolidated wildlife reference (output_01.csv)
- Input the data.
- Bring the Animal & Plant Details tables together into one aligned table:
  - Standardize field names so both sources use:
    - `Name` (rename `Animal` and `Plant` to `Name` respectively)
    - `Status` (rename the misspelled plant field `Stattus` to `Status`)
  - Add a `Table Names` field to each source to retain its origin (e.g., “Animal Details” vs “Plant Details”), then union the two sources into a single details table.
- From this combined details table, keep only the fields needed for analysis: `Name`, `Table Names`, `Status`, and `Class`.
- Use `Table Names` to derive whether each row is an animal or a plant:
  - Create a new field `Wildlife` with values `Animal` or `Plant` based on whether `Table Names` indicates animal vs plant.
- Standardize `Class` to the English name where possible:
  - If `Class` contains an English name in parentheses, replace `Class` with only the text inside the parentheses.
  - Otherwise, keep the original `Class` value.
- Combine the resulting details with the Wildlife table (the table containing `Wildlife`, `Name`, `Region`, and `Habitat`):
  - Fix the known encoding issue for apostrophes in `Name` so that names match between the two tables.
  - Join the tables using an inner join on (`Wildlife`, `Name`), expecting a complete match across both tables (i.e., no wildlife should be lost) and treating the relationship as one-to-one.
- Remove any unnecessary fields so the Stage 1 output contains exactly the required six fields.

### Stage 2 — Temperature-range assessment and prioritization (output_02.csv)
- Reduce the San Diego Climate table to a single temperature range in Fahrenheit:
  - San Diego low temperature (`sd_low`) = minimum of `Low °F`
  - San Diego high temperature (`sd_high`) = maximum of `High °F`
- Use habitat estimates to obtain temperature ranges per habitat:
  - From the Habitats (estimates) table, extract numeric Fahrenheit values for each habitat's minimum and maximum temperatures and store them as habitat-level `MinF` and `MaxF`.
  - The temperature values in the Habitats (estimates) table are stored as strings in the format "X degrees Fahrenheit (Y degrees Celsius)" or "X degree Fahrenheit (Y degrees Celsius)" (note: singular "degree" may appear). Extract only the Fahrenheit numeric value (the number before "degree" or "degrees Fahrenheit"):
    - Parse the string to find the numeric value that appears before "degree" or "degrees Fahrenheit".
    - Handle both singular ("degree") and plural ("degrees") forms.
    - Handle both standard minus sign (-) and en-dash (–) as negative indicators.
    - Ignore the Celsius value in parentheses; only extract the Fahrenheit value.
    - Examples: "–4 degrees Fahrenheit (–20 degrees Celsius)" → -4; "120 degrees Fahrenheit (50 degrees Celsius)" → 120; "–76 degree Fahrenheit (–60 degrees Celsius)" → -76.
- Handle multi-habitat wildlife:
  - The `Habitat` field in Stage 1 may contain multiple habitats separated by commas; transform the data to a row-per-habitat per wildlife species by splitting on the comma-and-space delimiter and exploding to multiple rows.
- Combine the exploded wildlife-by-habitat rows with habitat temperature ranges:
  - Left join on `Habitat` to bring in `MinF` and `MaxF` for each habitat.
- Reduce back to a single row per wildlife species with wild temperature bounds:
  - Group by (`Wildlife`, `Name`) and compute:
    - overall wild minimum temperature = minimum of `MinF` across the species’ habitats
    - overall wild maximum temperature = maximum of `MaxF` across the species’ habitats
  - Carry forward `Status`, `Class`, and `Region` for the species.
- Create the two calculated fields comparing San Diego to the species’ wild range:
  1. `Habitat Notes`
     - `Ideal` if `sd_low >= wild_min` and `sd_high <= wild_max`
     - `Above` if `sd_high > wild_max`
     - `Below` if `sd_low < wild_min`
  2. `Degrees outside Ideal`
     - If `Above`: `sd_high - wild_max` (positive)
     - If `Below`: `sd_low - wild_min` (negative)
     - If `Ideal`: `0`
- Filter to only wildlife that are not in their ideal temperature range (i.e., exclude `Habitat Notes = Ideal`).
- Create the Priority Order:
  - Bring in the Care Priority lookup table by joining on `Status` (left join) so no wildlife are lost.
  - Handle Priority Number assignment based on Status:
    - If a wildlife species has a missing `Status` (null or empty), then `Priority Number` = null and `Priority Order` = null.
    - If a wildlife species has a non-null `Status` but the Status does not exist in the Care Priority lookup table (i.e., the join produces a null Priority Number), then treat the missing Priority Number as `6` for ranking purposes.
    - In summary: missing Status → Priority Number = null, Priority Order = null; Status exists but not in lookup → Priority Number = 6, Priority Order calculated using 6.
  - Compute `abs_degrees` = absolute value of `Degrees outside Ideal`.
  - Build `Priority Order` as follows:
    - Order statuses by ascending Priority Number (excluding null statuses).
    - For each status in that order, rank unique `abs_degrees` values from largest to smallest; assign consecutive Priority Order values across statuses (continuing the count from the prior status).
    - Wildlife sharing the same status and the same `abs_degrees` receive the same Priority Order value.
- Add `Habitat` back to the final result as the original Stage 1 habitat string for each wildlife species.
- Remove any unnecessary fields and output the final table with exactly the required nine fields.

## Output

- output_01.csv
  - 6 fields:
    - Wildlife
    - Name
    - Class
    - Region
    - Habitat
    - Status

- output_02.csv
  - 9 fields:
    - Wildlife
    - Name
    - Priority Order
    - Habitat Notes 
    - Degrees outside Ideal
    - Status
    - Class
    - Region
    - Habitat