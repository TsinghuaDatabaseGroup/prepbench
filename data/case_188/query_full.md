## Context

Using Elden Ring melee-weapon base-stat tables, produce a curated view of which weapons deliver the highest total attack damage at each overall attribute requirement level. The intent is to support a playthrough by showing, for every possible summed requirement threshold, the top-damaging weapon(s) that can be wielded at that threshold.

## Requirements

- Input the data.
- Load the dataset from `input_01.csv`.

- Split the dataset into two logical tables (both derived from the same input file):
  - **Damage Stats** containing: `Name`, `Category`, `Phy`, `Mag`, `Fire`, `Ligh`, `Holy`.
  - **Level Requirements** containing: `Name`, `Str`, `Dex`, `Int`, `Fai`, `Arc`.

- Parse the Damage Stats fields (`Phy`, `Mag`, `Fire`, `Ligh`, `Holy`) as follows:
  - Each cell contains two parts representing (1) **attack damage** and (2) **damage resistance**.
  - A dash (`-`) represents 0 (i.e., no value).
  - Reshape (pivot longer) so there is one row per weapon per damage type, with:
    - one column identifying the damage type (the original column name), and
    - one column holding the original combined value.
  - Split the combined value into two columns:
    - `Attack Damage` (first part)
    - `Damage Resistance` (second part)
  - Replace any dash (`-`) with 0 in `Attack Damage` and `Damage Resistance`, and convert these columns to whole numbers (integers). If a part is missing or not usable as a number, treat it as 0.

- Parse the Level Requirements fields (`Str`, `Dex`, `Int`, `Fai`, `Arc`) as follows:
  - Each cell contains two parts representing (1) **required level** and (2) **attribute scaling rating**.
  - A dash (`-`) represents 0 (i.e., no requirement or scaling).
  - Reshape (pivot longer) so there is one row per weapon per attribute, with:
    - one column identifying the attribute (the original column name), and
    - one column holding the original combined value.
  - Split the combined value into two columns:
    - `Required Level` (first part)
    - `Attribute Scaling` (second part)
  - Replace any dash (`-`) with 0 in `Required Level` (and treat missing or non-numeric required-level parts as 0), then convert `Required Level` to whole numbers (integers). `Attribute Scaling` may be retained as an integer field but is not used in the final selection logic.

- Compute weapon-level totals:
  - **Total Attack Damage** per `Name` = sum of `Attack Damage` across all damage types (Phy/Mag/Fire/Ligh/Holy).
  - **Total Required Level** per `Name` = sum of `Required Level` across all attributes (Str/Dex/Int/Fai/Arc).

- Join the totals together:
  - Join Total Attack Damage and Total Required Level using an **inner join** on `Name` (weapons must exist in both totals to be included).
  - Attach `Category` for each `Name` from the input data; if there are multiple category rows per `Name`, keep a single category record per `Name` (any consistent single choice is acceptable, e.g., the first encountered).

- Select the best weapon(s) at each total requirement level:
  - For each distinct **Total Required Level**, rank weapons by **Total Attack Damage** in descending order using a dense ranking approach.
  - Filter to rank = 1, keeping all tied weapons that share the maximum total attack damage for that Total Required Level.

- Prepare the final output:
  - Keep only `Name`, `Category`, Total Required Level, and Total Attack Damage.
  - Rename Total Required Level to `Required Level` and Total Attack Damage to `Attack Damage`.
  - Sort the result by `Required Level` ascending.
- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Name
    - Category
    - Required Level
    - Attack Damage