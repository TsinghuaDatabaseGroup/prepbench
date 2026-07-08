## Context
This week challenge comes from one of our 100% club - Michael Heighway. Over to Michael to explain the challenge:
"So this is based on a real request that I received. We have been implementing Tableau across the organization and a team got excited about what could be done. They went and created their own tracking sheet to try to help with the data collection. While they got dates correct, datetime was a concept that they didn't quite understand. The "time" entry column ended up a free text field with lots of creative input.
There are more columns in the original of course but the key to the challenge is making sense of the date and time variables. The team is responsive around the clock so any time within a day could be valid. When the manager tried to analyze the data in Tableau they hit a roadblock with the times. Their hope was to be able to see what made sense for shift coverage. As the Tableau/Prep expert, I was tapped to try and clean up after the fact to allow for analysis and to enable a smooth transfer to an actual database."
So Preppers are you up for the challenge?

## Requirements

- Input the data
- Make the Time format suitable to fit the 24 hour clock
  - Factor in AM / PM
  - Ensure 12 am hour is captured correctly as 00:xx
- Remove unnecessary fields
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Date
    - Time
    - Date Time
