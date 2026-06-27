## Context

The Talent Acquisition team needs to analyze applicant qualifications. The raw data contains application information encoded in a single text string that must be parsed to extract relevant fields.

## Requirements

- Input the data from `input_01.csv`.
- Filter to rows containing "Work Experience:" (this removes header rows and year separators).
- Parse each qualifying row to extract:
  - `Application Month`: Extract month and year (e.g., "January 2023").
  - `Work Experience`: Extract the experience range text.
  - `Number Supervised`: Extract the supervised count range text.
  - `Industry Experience`: Extract Yes/No.
  - `Candidate Count`: Extract the count in parentheses at the end.
- Convert `Application Month` to the month-ending date and format as `DD/MM/YYYY`.
- Determine preferred qualification flags:
  - Work Experience: The lower bound of the range must be >= 4 years.
  - Number Supervised: The upper bound of the range (or the single value) must be > 10.
  - Industry Experience: Must be "Yes".
- Flag rows meeting all three preferred qualifications.
- Aggregate by `Application Month`:
  - Sum `Candidate Count` as `Total Candidates`.
  - Count rows meeting preferred qualifications as `Candidates with Preferred Qualifications`.
- Calculate `% of Candidates` as `(Candidates with Preferred Qualifications / Total Candidates) * 100`, rounded to 1 decimal place.

## Output

- output_01.csv
  - 4 fields:
    - Application Month
    - Total Candidates
    - Candidates with Preferred Qualifications
    - % of Candidates
