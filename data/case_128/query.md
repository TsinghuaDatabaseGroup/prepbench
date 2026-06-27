# 2021: Week 29 - PD x WOW - Tokyo 2020 Calendar

## Context
The data comes from the Olympics website. This was taken on Wednesday 14th July so the schedule for some events may have changed since!

### Inputs
1. Event Schedule: A list of all the event dates, times and locations throughout the games.
2. Venue Details: A list of all of the different venue locations.

## Requirements

- Input the data
- Create a correctly formatted DateTime field
- Parse the event list so each event is on a separate row
- Group similar sports into a Sport Type field
- Combine the Venue table
- Calculate whether the event is a 'Victory Ceremony' or 'Gold Medal' event.
- Output the data

## Output

- output_01.csv
  - 9 fields:
    - Latitude
    - Longitude
    - Medal Ceremony?
    - Sport Group
    - Events Split
    - UK Date Time
    - Date
    - Sport
    - Venue
