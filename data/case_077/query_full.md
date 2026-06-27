## Context
You have three input datasets related to the Olympic Games: (1) a host cities/countries table, (2) a historical medallists table, and (3) a country-to-code lookup. The goal is to produce three standardized outputs: a cleaned medallists extract, a host cities extract with a derived host-country field, and a country-by-year medal summary.

## Requirements
- Input the data.
  - Use the country-code lookup as the authoritative mapping between country names and 3-letter country codes.
  - Use the hosts table as the authoritative source for host metadata (including the combined host string and the start/end dates).
  - Use the medallists table as the authoritative source for individual medal records.

- Make sure every medal has both a Country and Country Code associated with it.
  - If a medal record is missing `Country`, fill it using the lookup via the record’s country code.
  - If a medal record is missing the country code, fill it using the lookup via the record’s country name.
  - After attempting to fill, remove any medal records that still do not have both fields populated (since they cannot be reliably attributed to a country).

- Group together Canoe/Kayak and Canoeing Sports.
  - Standardize `Sport` so that any value representing Canoeing is labeled exactly as `Canoe / Kayak`.
  - Specifically, replace `Canoeing` with `Canoe / Kayak` in the `Sport` field.

- Change Sport from Swimming to Aquatics.
  - Standardize `Sport` so that Swimming is labeled exactly as `Aquatics`.

- Replace the word "metres"/"metre" in Events with an "m" abbreviation.
  - In the `Event` field, replace whole-word occurrences of “metres” and “metre” with `m`.

- Replace the word "kilometres" in Events with an "km" abbreviation.
  - In the `Event` field, replace whole-word occurrences of “kilometres” with `km`.
  - Also handle cases where a distance number is directly followed by “kilometres” so that it becomes `<number>km`.

- Standardize km-walk Event formatting in Athletics:
  - For **Athletics events in Year 2016 only**: Format walking events with a space: `20 km walk`, `50 km walk`.
  - For **Athletics events in all other years**: Format walking events without a space: `20km walk`, `50km walk`.
  - Apply similar normalization for related distance events (e.g., `marathon 10 km` → `marathon 10km`, `20 km race walk` → `20km race walk`).

- Group together sensible Disciplines.
  - Standardize `Discipline` using consistent labels. Apply the following deterministic renames (only these listed mappings should be applied):
    - Normalize Greco-Roman wrestling variants to `Greco-Roman`.
    - Normalize modern pentathlon variants to `Modern Pentathalon`.
    - Normalize synchronized swimming variants to `Synchronized Swimming`.
    - Normalize beach volleyball, mountain bike, and gymnastics discipline labels to their standardized forms (`Beach volleyball`, `Mountain Bike`, `Artistic G.`, `Rhythmic G.`).
  - For Cycling, standardize the following discipline values to `Cycling Track`:
    - Replace `Track cycling` and `Road cycling` with `Cycling Track`.
    - Preserve `BMX` and `Mountain Bike` as-is (do not change these discipline values).
    - Preserve gender identifiers (`M`, `W`) and year values (e.g., `1908`) as-is; these are not discipline classifications.

- Output cleaned Medallists Dataset.
  - Produce `output_03.csv` at the medal-record level (one row per medal record retained after validation), containing the required fields only.
  - Remove fully duplicate rows so that exact duplicate records are not repeated in the output.
  - Sort the cleaned medallists output deterministically by: `Year` (ascending), `Sport` (ascending), `Event` (ascending), `Medal` in the order Gold → Silver → Bronze, `Event_Gender` in the order M → W, then `Country` (ascending).

- Aggregate to a row for each Event medal (i.e. we know longer need the Athlete names Level of Detail).
  - When preparing country medal counts, de-duplicate medal records down to a unique "event medal" grain before counting.
  - Use the following event-medal uniqueness rules:
    - For `Canoe / Kayak`, treat medals as unique by (`Country`, `Year`, `Medal`, `Event`, `Sport`, `Event_Gender`) excluding `Discipline` from the uniqueness key. This is because Canoe/Kayak discipline variants (such as `Canoe / Kayak F`, `Flatwater`, `Slalom`, `Sprint`) represent different ways of categorizing the same competitive events, and the same event medal should not be double-counted across these discipline variants.
    - For all other sports, treat medals as unique by (`Country`, `Year`, `Medal`, `Event`, `Sport`, `Event_Gender`, `Discipline`) so distinct disciplines remain distinct when relevant.

- Create a table showing total Gold, Silver and Bronze medals from each country for each year.
  - Starting from the de-duplicated event-medal grain above, count medals by `Country` and `Year`, separately for `Gold`, `Silver`, and `Bronze`.
  - The output grain for `output_01.csv` must be one row per (`Country`, `Year`).
  - If a country-year has no medals of a given type, output an empty value (blank) for that medal-type column rather than `0`.
  - Sort `output_01.csv` by `Year` descending, then `Country` ascending.

- Output Country Medals Dataset.
  - Write the aggregated country-by-year medal summary to `output_01.csv` with exactly the specified fields.

- Using the Hosts dataset, create a field for the Host Country.
  - Derive `Host City` and `Host Country` by splitting the host descriptor into city and country components (city first, country second).
  - Standardize host dates so `Start Date` and `End Date` are formatted as `DD/MM/YYYY`.
  - Derive `Year` from the (standardized) `Start Date`.

- Change the United Kingdom to Great Britain.
  - In the derived `Host Country` field, replace `United Kingdom` with `Great Britain`.

- Output Host Cities Dataset.
  - Write the cleaned/derived hosts table to `output_02.csv` with exactly the specified fields.
  - Sort `output_02.csv` by `Year` ascending.

- Output the data
  - Note: 去重处理 — `output_03.csv` 中存在完全重复行（例如 "India, IND, Hockey, Gold, hockey, \"SINGH, Singh\", 1980, M, Hockey" 重复出现），已在最终输出中删除重复记录以确保主键唯一性与评估一致。

## Output

- output_01.csv
  - 5 fields:
    - Country
    - Gold
    - Silver
    - Bronze
    - Year

- output_02.csv
  - 9 fields:
    - Year
    - Host City
    - Host Country
    - Start Date
    - End Date
    - Games
    - Nations
    - Sports
    - Events

- output_03.csv
  - 9 fields:
    - Country
    - Code
    - Sport
    - Medal
    - Event
    - Athlete
    - Year
    - Event_Gender
    - Discipline