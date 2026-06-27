## Context

The Prep School needs a complete weekday calendar for the spring half-term period, combining known term events with a recurring after-school club schedule. The provided events list includes key dates within the term, but the calendar must be expanded to include every school day between the first and last day of term.

## Requirements

- Input the events dataset from `inputs/input_02.csv`. Treat its `Date` field as a day-first date.
- Determine the term boundaries from the events data:
  - **First Day of Term** = the minimum `Date` in the events dataset.
  - **Last Day of Term** = the maximum `Date` in the events dataset.
- Use a “new rows” style expansion to generate a complete sequence of calendar dates from the First Day of Term through the Last Day of Term, **inclusive** (one row per date before weekend removal).
- Remove weekends so that the calendar contains only school days (Monday through Friday).
- Create a `Day of Week` column as the weekday name for each remaining date, using the full English names (Monday, Tuesday, Wednesday, Thursday, Friday).
- Input the After School Club dataset from `inputs/input_01.csv` and combine it with the generated weekday calendar so that each date is assigned the club that runs on that `Day of Week`:
  - Join the weekday calendar to the club mapping **on `Day of Week`** using a **left join** (keep all generated weekdays even if no club is found for a day).
- Combine the events with the generated weekday calendar so that each date is assigned its event (if any):
  - Join the weekday+club calendar to the events data **on `Date`** using a **left join** (keep all generated weekdays even if no event exists for a date).
- Update nulls in the `Event` field to `N/A` after joining.
- Format `Date` in the final output as text in `DD/MM/YYYY`.
- Output the resulting dataset with exactly the required fields.

## Output

- output_01.csv
  - 4 fields:
    - Date
    - Event
    - Day of Week
    - After School Club