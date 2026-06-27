## Context

Prep Air is researching aviation operational risk using historical incident reports sourced from the AeroInside website. Each incident is currently stored as a single free-text string, so the task is to (1) parse structured fields from that text and (2) categorize incidents into predefined safety-related categories in order to quantify how often each type of incident occurs.

## Requirements

- Input the data.
  - Read the incident reports from `input_01.csv`. Each row contains an incident narrative in a field named `Incident`.
  - Read the category list from `input_02.csv`. Each row contains a category name in a field named `Category`.

- Parse out the following information from each incident string:
  - Aircraft
  - Location
  - Date
  - Incident Description
- The incident string is expected to follow the structure:
  - `[Aircraft] at|near [Location] on [Date], [Incident Description]`
  - Use `at` or `near` as the location separator.
- If an incident string does not match the expected structure, populate:
  - `Aircraft`, `Location`, and `Date` as blank, and
  - `Incident Description` as the full original incident string.

- Convert the parsed date from a string into a standardized date representation:
  - When the parsed date is in the form `Mon DD(th|st|nd|rd) YYYY` (ordinal suffix optional), output it as `DD/MM/YYYY` with a 2-digit day and month.
  - If the date cannot be parsed into that structure, keep the parsed date text as-is (or blank if the incident could not be parsed).

- Combine similar incident types when identifying which categories apply to an incident:
  - Category matching is case-insensitive and is based on whether the category keyword appears as a substring within the incident description text.
  - In addition to direct keyword matches, apply these explicit combination/expansion rules when assigning categories from the incident description:
    - Treat mentions of “attendant” or “attendants” as matching the category `Attendant`.
    - Treat mentions of “pressure”, “pressurize”, or “pressurization” as matching the category `Pressure`.
    - Treat mentions of “takeoff” or “take off” as matching the category `Takeoff`.
    - Treat mentions of “landing” as matching the category `Landing`.
    - Treat mentions of “runway” as matching the category `Runway`.
    - Treat mentions of “engine” or “engines” as matching the category `Engine`.
    - Treat mentions of “thrust” as matching the category `Thrust`.
    - Treat mentions of “turbulence” as matching the category `Turbulence`.
    - Treat mentions of “bird” as matching the category `Bird`.
    - Treat mentions of “electrical” as matching the category `Electrical`.
  - An incident may match multiple categories; count it once in each matched category.

- Create a total for how many incidents happened within each category:
  - Use the category list from `input_02.csv` as the reporting set.
  - For each category in that list, compute the number of incidents whose incident description matches that category using the rules above.
  - Output only categories with at least 1 matched incident.
  - Sort the category totals alphabetically by `Category`.

- Output the data:
  - `output_02.csv` is the parsed incident details at the grain of one row per input incident (same row order as the input).
  - `output_01.csv` is the category summary at the grain of one row per reported category (after filtering to categories with non-zero counts).

## Output

- output_01.csv
  - 2 fields:
    - Category
    - Number of Incidents

- output_02.csv
  - 4 fields:
    - Date
    - Location
    - Aircraft
    - Incident Description