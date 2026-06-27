## Context

You are preparing a tidy, analysis-ready dataset of monthly tourist arrivals to the Maldives (2010–2020) from a source file that is wide by month. The intent is to keep country-level rows where available, and to also quantify the residual “Unknown” arrivals at the continent level (because continent totals exist even when not all underlying countries are present), plus a separate “Unknown” category for UN passport holders and others.

## Requirements

- Input the data from `input_01.csv`.

- Pivot all month fields into a single column so the dataset becomes long:
  - Treat `id`, `Series-Measure`, `Hierarchy-Breakdown`, and `Unit-Detail` as identifier columns.
  - Convert all remaining month columns into two fields:
    - `Month` (the original month column name)
    - `Value` (the corresponding cell value)

- Rename the fields and enforce data types:
  - Rename `Hierarchy-Breakdown` to `Breakdown`.
  - Rename `Value` to `Number of Tourists`.
  - Parse `Month` as a date using the month-year pattern shown in the headers (e.g., `%b-%y`).
  - Convert `Number of Tourists` to a numeric type, then cast to integer after validation (see next step).

- Filter out the nulls:
  - Remove rows where `Number of Tourists` is null after numeric conversion.

- Filter the dataset so `Number of Tourists` represents tourist-arrival counts by keeping only these series:
  - All rows where `Series-Measure` starts with `Tourist arrivals from ` (used for continent totals and country rows).
  - The specific series `Tourist arrivals - UN passport holders and others` (used to produce an additional “Unknown” category).

- Remove totals/subtotals while retaining the lowest usable granularity and constructing “Unknown” where needed, using two streams:

  1) **Country stream (explicit country rows)**
     - From the `Tourist arrivals from ...` rows, derive a `target` value by removing the prefix `Tourist arrivals from ` from `Series-Measure`.
     - Treat rows as *country rows* when `target` is not one of these continent labels:
       - `Europe`, `Asia`, `Africa`, `Americas`, `Oceania`, `the Middle East`
     - Create `Country` from `target`.
     - Set `Breakdown` for these rows to the final level of the hierarchy path by taking the last segment of the existing `Breakdown` value when split on ` / ` (this yields the continent name for each country row).
     - Keep only the following country/continent combinations (discard all other country rows):
       - Europe: Germany, Italy, Russia, United Kingdom, France
       - Asia: China, India
       - Oceania: Australia
       - Americas: United States
     - Keep these as the country-level portion of the output with fields: `Breakdown`, `Number of Tourists`, `Month`, `Country`.

  2) **Continent stream (continent totals → computed Unknown-by-continent)**
     - From the `Tourist arrivals from ...` rows, treat rows as *continent totals* when `target` is one of:
       - `Europe`, `Asia`, `Africa`, `Americas`, `Oceania`, `the Middle East`
     - For these rows, interpret `Number of Tourists` as the continent total for that month.
     - Aggregate the **Country stream** up to continent level by summing `Number of Tourists` grouped by:
       - `Month`
       - `Breakdown` (which is the continent name for the country rows)
     - Join continent totals to the aggregated country sums using a left join on:
       - `Month`
       - Continent name (continent totals’ `target` matched to the aggregated countries’ continent)
     - For each continent-month, compute:
       - `Unknown (Number of Tourists)` = `Continent Total` − `Countries Sum`
       - If a continent-month has no matching country sum, treat `Countries Sum` as 0.
       - If the subtraction is negative, set the result to 0 (do not allow negative unknown counts).
     - Output these computed rows with:
       - `Breakdown` = the continent name
       - `Country` = `Unknown`
       - `Number of Tourists` = the computed unknown value
       - `Month` = the month

  3) **UN passport holders and others → Unknown**
     - From the series `Tourist arrivals - UN passport holders and others`, output rows with:
       - `Breakdown` = `UN passport holders and others`
       - `Country` = `Unknown`
       - `Number of Tourists` = the series value
       - `Month` = the month

- Union the outputs from:
  - the selected country rows,
  - the computed continent-level Unknown rows,
  - and the UN passport holders and others Unknown rows (if present),
  aligning columns by name.

- Format the final `Month` field as `DD/MM/YYYY` (day-first) as exact text.

- Ordering (to make the output deterministic):
  - Within each month, order the country rows in this sequence:
    1. (Europe, Germany)
    2. (Europe, Italy)
    3. (Europe, Russia)
    4. (Europe, United Kingdom)
    5. (Asia, China)
    6. (Asia, India)
    7. (Europe, France)
    8. (Oceania, Australia)
    9. (Americas, United States)
  - Within each month, order the “Unknown” rows by `Breakdown` in this sequence:
    - Europe, Asia, Africa, Americas, Oceania, the Middle East, UN passport holders and others
  - Overall, sort by `Month` ascending, and then apply the relevant within-month ordering described above.

- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Breakdown
    - Number of Tourists
    - Month
    - Country
