## Context
Prep Air wants more detail behind recent project overruns by converting a project-management commentary log into an analysis-ready table. The raw commentary contains compact codes and abbreviations; a set of lookup tables provides the full wording for those codes. The goal is to parse the commentary into one row per logged item and enrich it with the full project, sub-project, task type, and owner name.

## Requirements
- Input the data.
  - Use the main commentary dataset (containing at least `Week` and `Commentary`) plus four lookup tables:
    - Project code → full project name
    - Sub-project code → full sub-project name
    - Task code → full task name/type
    - Owner abbreviation → full owner name
- Define the output grain precisely:
  - Each output row must represent **one parsed commentary segment** from within the `Commentary` field for a given `Week`.
  - A single `Commentary` cell may produce multiple output rows if it contains multiple bracketed segments.
- Parse the commentary into segments.
  - Treat the commentary text as a sequence of segments of the form:
    - a bracketed header: `[ ... ]`
    - followed by the segment’s detail text, continuing until the next `[` header begins or until the end of the commentary text.
  - For each segment, extract:
    - `header`: the text inside the brackets
    - `Detail`: the text following that header for the segment (excluding the brackets themselves)
  - Only process segments whose `header` contains a `/` separating a project code from the remaining codes; if a segment’s header does not include `/`, do not output a row for that segment.
- Derive and enrich the required fields for every parsed segment:
  - **Week**
    - Convert the input `Week` value to an integer week number.
    - Output as the string `Week x` (with the number substituted), e.g., `Week 3`.
  - **Project**
    - From `header`, take the portion before `/` as the project code.
    - Map that code to the full project name using the project lookup (left-join behavior: if not found, leave `Project` as null).
  - **Sub-Project** and **Task**
    - From `header`, take the portion after `/`. Interpret it as `subproject_code-task_code` split on the first `-`.
      - The part before `-` is the sub-project code.
      - The part after `-` is the task code (if missing, treat as null).
    - Map sub-project code to full sub-project name using the sub-project lookup (if not found, null).
    - Map task code to full task name/type using the task lookup (if not found, null).
  - **Name**
    - Determine the task owner from the segment `Detail` by locating abbreviations written as a standalone token followed by a period.
    - Use the **last** such abbreviation in the `Detail` (if multiple appear).
    - Only the abbreviations `tom`, `jen`, `jon`, and `car` are considered valid for this detection.
    - Map the detected abbreviation to the full owner name using the name lookup (if no valid abbreviation is found or not present in the lookup, output null).
  - **Days Noted**
    - In the segment `Detail`, search for the first occurrence of an integer immediately followed by the word `day` (allowing `day`/`days` via matching `day` as the keyword).
    - If found, output that integer value; otherwise output null.
  - **Detail**
    - Output the segment detail text as extracted for that segment (i.e., the description text that follows the bracketed header).
- Ordering:
  - Process weeks in ascending week-number order.
  - Within each week, preserve the original left-to-right order of segments as they appear in the `Commentary` text.
- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Week
    - Project
    - Sub-Project
    - Task
    - Name
    - Days Noted
    - Detail