## Context
You need to calculate the number of working days in a defined period, excluding weekends, bank holidays, and personal holiday days. The intent mirrors common “networkdays”/working-days questions: build a day-by-day scaffold over the period, remove non-working days, and return a single summary count.

## Requirements
- Input the data.
- Use a fixed analysis window:
  - **Start Date** is **2019-04-01**.
  - **Today** (the end date) is **2020-09-08**.
- Create a row for every calendar date in the interval **(Start Date, Today]** (i.e., start from the day after Start Date and include Today).
- Filter out weekends, treating Saturday and Sunday as non-working days.
- Perform any necessary cleaning on the bank holiday dataset so it can be used to identify bank-holiday dates (e.g., ensure the holiday date field is interpretable as a date).
- Exclude bank holidays that fall within the analysis window. For this task, exclude the following bank-holiday dates:
  - 2019-04-19
  - 2019-04-22
  - 2019-05-06
  - 2019-05-27
  - 2019-08-26
  - 2019-12-25
  - 2019-12-26
  - 2020-01-01
  - 2020-04-10
  - 2020-04-13
  - 2020-05-08
  - 2020-05-25
  - 2020-08-31
- Count how many remaining date rows you have after excluding weekends and bank holidays (the start date is already excluded by construction).
- Remove any holiday days taken personally by subtracting the total number of personal holiday days from the workday count:
  - Compute **Total Personal Holidays** as the sum of the `Holidays` field from the personal-holidays input.
  - **Working Days = (weekday, non–bank-holiday date count) − (Total Personal Holidays)**.
- Output a single-row result containing the Start Date, Today, and Working Days. Format Start Date and Today as `DD/MM/YYYY`.

## Output

- output_01.csv
  - 3 fields:
    - Start Date
    - Today
    - Working Days