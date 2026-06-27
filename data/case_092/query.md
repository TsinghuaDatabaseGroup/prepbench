## Context

At Prep Air, we have decided to do some research into the risks of running an airline. We want to complete some analysis on some historic aviation incident reports so we can try to identify potential areas where we can make our airline safer. We have taken a selection of reports from the AeroInside website, who document various incident reports from around the world. Each report contains information about the incident, but is a free text field so doesn't really have a structure. In this challenge, we want to parse out the key information from the string, and then see how many incidents occur that are related to our key categories.

## Requirements

- Input the data
- Parse out the following information from the incident string:
  - Aircraft - eg, American B738
  - Location - Amsterdam
  - Date - Apr 21st 2016
  - Incident Description - details about the incident
- Convert date field from string to a date
- Combine similar incident types. Eg, Attendant & Attendants or Pressure & Pressurize.
- Create a total for how many incidents happened within each category
- Output the data

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
