## Context

Recently here at Chin & Beard Suds Co, we've become suspicious that some our employees in our flagship store (found on the 96th floor of the Shard) are slacking off and taking their jobs for granted. We think their productivity might be linked with how close they are to the nearest manager and who they're interacting with.
To investigate this we've spent time undercover observing 3 random employees during a typical working day and recording whether they're on task. We record in intervals of between 1 & 3 mins and also note down the rough proximity of the manager on duty and who they interacted with most during each interval. We've also noted down the time we started observing each employee but not the actual start time of each interval.
This current data format doesn't work well in Tableau, so we need to do some clean-up and find a way to get some actual date-times for each interval.

## Requirements

- Input the data
- For each employee and interval:
  - Create a single field for who they interacted with.
  - Create a single field for the manager's proximity.
  - Create a single field for whether they were on task or not.
  - Calculate the actual start time.
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - Task Engagement
    - Manager Proximity
    - Interaction
    - Employee
    - Observation Start Time
    - Observation Length (mins)
    - Observation Interval
