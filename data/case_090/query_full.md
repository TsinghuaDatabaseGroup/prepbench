## Context
A global Halloween-costume retailer wants a like-for-like comparison of sales in the prior fiscal year versus the current fiscal year-to-date. The source data includes sales recorded at different discount levels, costume names in local languages, and some country-name entry errors. The goal is to standardize and reshape the data so that sales for fiscal year 2019 and fiscal year 2020 can be compared side-by-side.

## Requirements
Remember this is a **click-only** challenge, no typed calculations allowed!

- Input the data.
- Reshape the dataset so that sales recorded at different discount levels are combined into a single sales measure:
  - The input contains separate fields for sales at full, half, and quarter price; convert these into a long format so there is one sales amount per row, with an accompanying discount classification.
  - Exclude records where the sales value is missing.
- Standardize costume names by grouping all local-language costume names into their English translation:
  - After grouping, the `Costume` field must contain exactly these 9 English categories: Cat, Ghost, Vampire, Pirate, Zombie, Clown, Dinosaur, Devil, Werewolf.
- Correct country-name entry errors:
  - Standardize the affected country values to the correct spellings so that the final `Country` field uses the intended country names (including Indonesia, Luxembourg, Philippines, and Slovenia).
- Apply fiscal-year logic and filter to the required comparison windows (both date bounds inclusive):
  - 2019 fiscal year: 01/11/2018 through 31/10/2019.
  - 2020 fiscal year-to-date: 01/11/2019 through 27/10/2020.
  - Note: to achieve this without typed calculations, you need will need to be using version 2020.3.3
- Ensure all sales are represented consistently:
  - Create a `Price` field indicating the discount level, and ensure it contains only one of: `Full`, `Half`, or `Quarter` (based on which sales column the value came from).
  - Split the sales value into:
    - `Currency`: the currency descriptor that appears before the number; it may consist of one or more words/symbols.
    - the numeric sales amount, converted to a whole number by removing any decimal component.
- Aggregate and present sales for comparison across fiscal years:
  - Group and sum the whole-number sales amounts at the grain of `Costume`, `Country`, `Currency`, `Price`, and fiscal year.
  - Pivot fiscal year into columns so that 2019 and 2020 fiscal-year sales appear as two separate fields on the same row:
    - `2019 FY Sales` = summed sales within the 2019 fiscal-year window.
    - `2020 FY Sales` = summed sales within the 2020 fiscal-year-to-date window.
  - If a row has no sales for a given fiscal year, output 0 for that fiscal-year sales field.
- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Costume
    - Country
    - Currency
    - Price
    - 2019 FY Sales
    - 2020 FY Sales