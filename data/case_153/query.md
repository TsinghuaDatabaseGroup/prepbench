## Requirements

- Input the data
  - Removing any unnecessary fields (parental fields) will make this challenge easier to see what is happening at each step
- Format the pupil's name in *First Name Last Name* format (ie Carl Allchin)
- Create the date for the pupil's birthday in calendar year 2022 (not academic year)
- Work out what day of the week the pupil's birthday falls on
  - Remember if the birthday falls on a Saturday or Sunday, we need to change the weekday to Friday
- Work out what month the pupil's birthday falls within
- Count how many birthdays there are on each weekday in each month
  - Note: there is an issue with my output as I use the birthday month rather than the 2022 date of the birthday (thanks Rosario). Output updated 17/1/22 9:45 PM GMT)
- Output the data

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
