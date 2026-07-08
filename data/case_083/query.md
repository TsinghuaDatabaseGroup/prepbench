## Context
This week we're tackling some questions commonly asked by clients: How do I calculate working days in Tableau Prep? or Is there a networkdays function in Tableau Prep? Instead of calculating working days between support ticket open and closing dates, let's work out how many days you've worked in a specific time period. The inputs will need to be a little bespoke for this challenge. You will need: an input containing the date you'd like to start counting from; an input containing information about the number of days holiday you took each year; a bank holiday input for your country of residence (a few countries are included but you may need to find your own data); a scaffolding input.

## Requirements

- Input the data
- Create a row for every date between your start date and today's date
- Filter out the weekends
- Perform any necessary cleaning on the bank holiday dataset
- Exclude bank holidays
- Count how many rows you have (being sure to exclude the start date)
- Remove any holiday days
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Start Date
    - Today
    - Working Days
