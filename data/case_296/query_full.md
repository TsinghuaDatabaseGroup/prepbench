## Context
You are given yearly tables from Wikipedia’s “Forbes list of the world's highest-paid athletes” (one table per year) plus a separate source table. The objective is to standardize the schema across all yearly tables, convert earnings fields to numeric values, attach the source information to every row, and combine everything into one dataset suitable for time-based analysis.

## Requirements
- Input the data.
  - Use the 13 yearly input files as the year tables and the remaining input file as the source table.
- Bring all the year tables together into a single table.
  - Treat each input year table as having one row per athlete for that year.
  - Append (union/concatenate) the year tables into one combined table after standardizing their columns.
- Merge any mismatched fields.
  - Standardize column names across all year tables so the combined output has a consistent set of fields: Rank, Name, Sport, Country, Total earnings, Salary/Winnings, Endorsements.
  - Where different year tables use different headers for the same concept, map them into the same standardized output field before combining.
- Create a numeric Year field.
  - Add a Year column to each year table prior to combining, using the year associated with that table.
  - Ensure Year is numeric in the final output.
- Clean up the fields with the monetary amounts.
  - Convert the three earnings fields (Total earnings, Salary/Winnings, Endorsements) to numeric values.
  - Remove non-numeric symbols used as formatting (such as currency symbols and separators) before parsing.
  - Make sure that any value expressed in millions is translated to the full amount (e.g. “$6 million” becomes 6,000,000).
  - If a monetary value cannot be parsed into a number, leave it as null rather than inventing a value.
- Bring in the source information so that it is associated with each row.
  - Read the source value from the source input file and attach it to every row in the combined dataset as the Source field (i.e., the same Source value is repeated for all rows).
- Remove unnecessary fields.
  - Keep only the nine required output fields and drop everything else.
- Output the data.

## Output

- output_01.csv
  - 9 fields:
    - Year
    - Rank
    - Name
    - Sport
    - Country
    - Total earnings
    - Salary/Winnings
    - Endorsements
    - Source