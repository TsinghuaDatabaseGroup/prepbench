## Context

You have a pupil list that includes each pupil’s first name, last name, and date of birth. The goal is to build a 2022 birthday schedule and determine when cake is needed, then summarize how many cake days fall on each weekday within each month.

## Requirements

- Input the data
  - Removing any unnecessary fields (parental fields) will make this challenge easier to see what is happening at each step
- Create a per-pupil output row (the output grain is one row per pupil from the input file).
- Format the pupil's name in *First Name Last Name* format (ie Carl Allchin), using the pupil first name and pupil last name fields.
- Parse the pupil’s original date of birth as a date.
- Create the date for the pupil's birthday in calendar year 2022 (not academic year) by keeping the original month and day and setting the year to 2022.
- Work out what day of the week the pupil's birthday falls on for the 2022 birthday date.
  - Remember if the birthday falls on a Saturday or Sunday, we need to change the weekday to Friday:
    - If the 2022 birthday date is a Saturday, move the cake date back 1 day (to Friday).
    - If the 2022 birthday date is a Sunday, move the cake date back 2 days (to Friday).
    - Otherwise, the cake date stays as the 2022 birthday date.
  - Set **Cake Needed On** to the weekday name of this cake date.
- Work out what month the pupil's birthday falls within, using the month of the cake date (i.e., after applying the weekend-to-Friday adjustment), and represent it as the full month name.
- Count how many birthdays there are on each weekday in each month by grouping on **Month** and **Cake Needed On** and counting pupils in each group.
  - Attach this group count back onto each pupil row as **BDs per Weekday and Month** via a left join on **Month** and **Cake Needed On** so every pupil keeps their row.
- Format **Date of Birth** and **This Year's Birthday** as `DD/MM/YYYY` in the final output (zero-padded).
- Output **BDs per Weekday and Month** as an integer string with no decimals.
- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Pupil Name
    - Date of Birth
    - This Year's Birthday
    - Cake Needed On
    - Month
    - BDs per Weekday and Month
  - Date of Birth and This Year's Birthday must be formatted exactly as `DD/MM/YYYY` (zero-padded).
  - BDs per Weekday and Month must be an integer string with no decimals.
