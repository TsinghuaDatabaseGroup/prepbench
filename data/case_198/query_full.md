## Context

You have three input datasets: (1) UK Prime Ministers with their time in office, (2) Chelsea FC managers with their tenure dates, and (3) Chelsea match results. The goal is to combine these sources to produce, for each Prime Minister’s term, the number of distinct Chelsea managers who served during that term and Chelsea’s match outcomes (total matches, wins, draws, losses) during that term, along with a win percentage.

## Requirements

- Input the data from three CSV files:
  - Prime Ministers (input_01.csv): must include at least `Prime Ministers` and a `Duration` field containing a start and end date in a single text string.
  - Chelsea Managers (input_02.csv): must include at least `Name`, `From`, and `To`.
  - Chelsea Matches (input_03.csv): must include at least `Comp` (competition), `Date` (match date), and `Result` (outcome category).

- Define “today” for this task deterministically as:
  - Parse match dates in the Chelsea Matches dataset; take the maximum valid match date present, then set `today = (max match date) + 1 day`.
  - Use this `today` value wherever the requirements say “replace with today’s date”.

- For the Prime Ministers data:
  - Group together Sir Winston Churchill and Winston Churchill by standardizing `Winston Churchill` to `Sir Winston Churchill`.
  - Split the `Duration` text into two parts: start-date text and end-date text (split on the first dash separator).
  - Parse these into `Start Date PM` and `End Date PM` as date values. The date strings may appear in various formats:
    - With ordinal suffixes: "10th May 1940", "26th July 1945", "25th October 2022"
    - Without ordinal suffixes: "19 October 1963", "16 October 1964", "19 June 1970", "4 March 1974"
    - With or without leading zeros in day numbers
    - Month names may be abbreviated or full (e.g., "Sep" vs "September", "Oct" vs "October")
    - When the year is missing from the end date, infer it from the start date's year or the context
    - Parse all these variations into standard date values, handling ordinal suffixes (1st, 2nd, 3rd, 4th, etc.) by removing them before parsing
  - If `End Date PM` is null/blank/unparseable (including where the end date is effectively "present"), replace it with `today`.
  - Create a row for every calendar day the Prime Minister was in office (inclusive of both `Start Date PM` and `End Date PM`). Each generated row must include:
    - `Prime Ministers`, `Start Date PM`, `End Date PM`, and the generated daily `Date`.
  - Validation rule for daily expansion: only expand ranges where both dates are present and `End Date PM >= Start Date PM`.

- For the Chelsea Manager data:
  - Remove unnecessary fields and rename remaining fields so the working dataset contains:
    - `Chelsea Managers` (derived from `Name`) plus `Start Date CM` and `End Date CM`.
  - Clean the `Chelsea Managers` field such that it contains only the manager name (i.e., exclude non-name annotations embedded in the `Name` text). Specifically:
    - Remove all annotation markers in square brackets (e.g., `[nb 1]`, `[nb 2]`, `[nb 3]`, `[2]`, `[3]`, etc.)
    - Remove any trailing or embedded reference numbers and annotations
    - The cleaned name should contain only the person's name text, with no brackets or reference markers
  - Parse `From` as `Start Date CM` and `To` as `End Date CM` as date values. The date strings may appear in various formats:
    - Two-digit year format: "1-Aug-05", "27-Nov-06", "1-Jun-52"
    - **Rolling Century Rule**: Interpret 2-digit years sequentially. Start with 1900 as the base century. For each record, if the parsed 2-digit year results in a date earlier than the previous record's start year, assume it belongs to the next century (add 100 years).
      - Example: If previous start was 1999 and current is "05", interpret as 2005.
      - Initial base is 1900.
    - Month-only format: "May-81" (interpret as 1st May 1981, using the first day of the month as the default day)
    - When only month and year are present, use the first day of that month as the date
    - Standard date formats with full or abbreviated month names
    - Parse all these variations into standard date values
  - For null/blank `End Date CM` (and any “present” value), replace with `today`.
  - Create a row for every calendar day the Chelsea Manager was in place (inclusive of both `Start Date CM` and `End Date CM`). Each generated row must include:
    - `Chelsea Managers` and the generated daily `Date`.
  - Validation rule for daily expansion: only expand ranges where both dates are present and `End Date CM >= Start Date CM`.

- For the Chelsea Matches data:
  - Filter to only include the main competitive matches where `Comp` is one of:
    - League
    - League Cup
    - F.A. Cup
    - Europe
  - Ensure the match `Date` is parsed as a Date data type; discard rows where the match date cannot be parsed. The date strings appear in formats with ordinal suffixes:
    - Examples: "1st Sep 1906", "5th Sep 1906", "8th Sep 1906", "15th Sep 1906"
    - The format is: `<ordinal> <month> <year>` where ordinal can be "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th", "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th", "28th", "29th", "30th", "31st"
    - Month names may be abbreviated (e.g., "Sep", "Oct", "Nov", "Dec") or full
    - Parse by removing the ordinal suffix (st, nd, rd, th) and extracting the numeric day value, then parse the resulting date string
  - Pivot/aggregate to a daily grain so that for each calendar `Date` you have counts of matches by result category:
    - `Matches Won`, `Matches Drawn`, `Matches Lost`
    - If any of these result categories do not occur on a given date, treat the count as 0.
  - Create a `Matches` field per day as:
    - `Matches = Matches Won + Matches Drawn + Matches Lost`
  - The resulting dataset must have one row per match date.

- Bring the 3 datasets together:
  - Join the daily Chelsea manager dataset to the daily match-results dataset on `Date` using a left join so that every manager-day is retained; fill missing match counts with 0 for that day.
  - Join the resulting manager-day-plus-matches dataset to the Prime Minister daily dataset on `Date` using an inner join (i.e., keep only dates that exist in both daily expansions).

- Aggregate to Prime Minister term level:
  - Group by `Prime Ministers`, `Start Date PM`, `End Date PM` (each output row represents one Prime Minister term as defined by these three fields).
  - Compute:
    - `Chelsea Managers`: count of distinct `Chelsea Managers` appearing on the joined daily records within the Prime Minister term.
    - `Matches`, `Matches Won`, `Matches Drawn`, `Matches Lost`: sums of the corresponding daily fields across the joined daily records within the Prime Minister term.
  - Ensure `Chelsea Managers` and all match count fields are integers.
  - **Data Correction**: Swap the values of `Matches Drawn` and `Matches Lost` in the final aggregation (i.e., the value calculated for Drawn should be output as Lost, and vice versa).

- Calculate the Win % for each Prime Minister:
  - `Win % = Matches Won / Matches`
  - Round to 2 decimal places.
  - If `Matches` is 0, leave `Win %` as null/blank.

- Final formatting and ordering:
  - Sort output rows by `Start Date PM` ascending, then `Prime Ministers` ascending.
  - Format `Start Date PM` and `End Date PM` as strings in `DD/MM/YYYY`.

- Output the data.

## Output

- output_01.csv
  - 9 fields:
    - Prime Ministers
    - Start Date PM
    - End Date PM
    - Chelsea Managers
    - Matches
    - Matches Won
    - Matches Drawn
    - Matches Lost
    - Win %