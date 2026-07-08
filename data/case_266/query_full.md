## Context

You are asked to remap the 2024 Gregorian calendar into an alternative calendar where every month is exactly 28 days long. Using this remapping, generate the original date and its corresponding “new date”, then keep only the dates where the month number changes between the original system and the new 28-day-month system.

## Requirements

- Input the data.
- Use the year **2024** (a leap year) and generate **one row per calendar day** from **2024-01-01 through 2024-12-31**, inclusive (366 days total).
- For each generated day, compute its **day-of-year** index in 2024, where January 1st is day 1.
- Define the new calendar system with **28-day months**:
  - **New Month** = `floor((day_of_year - 1) / 28) + 1` (this yields months 1 through 14).
  - **New Day** = `((day_of_year - 1) mod 28) + 1` (this yields days 1 through 28, with month 14 containing only days 1 and 2).
  - This creates **14 months**, with the **14th month containing just 2 days** (because 2024 has 366 days).
- Create two formatted date strings (both as text):
  - **Date**: the original Gregorian date in `DD/MM/YYYY` format for 2024.
  - **New Date**: a remapped date string in the format `New day of the month / New month / 2024`, i.e., `DD/MM/2024`, where:
    - the day component is `New Day` and the month component is `New Month`,
    - both day and month are **2-digit, zero-padded** (e.g., `01`, `12`, `14`).
- Filter the generated rows to only include dates where the **month has changed in the new system**, meaning:
  - keep a row if the **original Gregorian month number** (1–12) is **not equal** to `New Month`.
- Output the resulting dataset.

## Output

- output_01.csv
  - 2 fields:
    - Date
    - New Date