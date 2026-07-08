## Context

Contact-centre agents capture customer interactions using free-text notes, which makes it difficult to consistently measure key contact reasons. The goal is to produce an analysis-ready dataset (suitable for loading into Tableau) that, at the level of each qualifying contact, identifies whether the interaction relates to a balance check, a statement request, or a complaint, and ties those interactions back to both Policy Number and Customer ID. The dataset must also include a true calendar date for each contact day so that daily volumes can be analysed.

## Requirements

- Input the data from the two provided weekly files:
  - `input_01.csv`
  - `input_02.csv`

- Create a true calendar date per record (“True Date”) by converting the weekday value in the input `Date` field into a specific date:
  - Treat the `Date` field as a weekday name (Monday–Sunday).
  - For `input_01.csv`, use Monday of that week as **2019-06-17** and assign:
    - Monday = 17/06/2019, Tuesday = 18/06/2019, …, Sunday = 23/06/2019.
  - For `input_02.csv`, use Monday of that week as **2019-06-24** and assign:
    - Monday = 24/06/2019, Tuesday = 25/06/2019, …, Sunday = 30/06/2019.
  - Format “True Date” as a string in `DD/MM/YYYY`.

- Determine how the customer contacted the company:
  - No separate contact-channel output is required for this task; classification is limited to identifying whether the contact is about a balance check, a statement request, or raising a complaint (as defined below).

- Create a separate column for the Policy Number by extracting it from the free-text `Notes` field:
  - Extract the digits that immediately follow a `#` character (i.e., the policy number is the numeric portion of a `#<digits>` pattern in `Notes`).
  - Store the result as an integer in `Policy Number`.

- Remove contacts that don't have a Policy Number:
  - Exclude any record where a policy number cannot be extracted from `Notes`.

- Identify whether the contact was about a balance check, getting a statement or raising a complaint by creating three indicator fields derived from `Notes`:
  - `Statement?` = 1 if `Notes` contains the substring “statement” (case-insensitive), else 0.
  - `Balance?` = 1 if `Notes` contains the substring “balance” (case-insensitive), else 0.
  - `Complaint?` = 1 if `Notes` contains the substring “complain” (case-insensitive), else 0.
  - These indicators are independent (a single record may set multiple indicators to 1).

- Keep `Customer ID` from the input as an integer.

- Get rid of unrequired columns:
  - The final output must contain only the specified six fields and no additional columns.

- Output the data:
  - Append (row-bind) the qualifying records from both input weeks into a single output file.
  - Each output row represents one input contact record that has a valid extracted Policy Number.

## Output

- output_01.csv
  - 6 fields:
    - Statement?
    - True Date
    - Balance?
    - Complaint?
    - Policy Number
    - Customer ID