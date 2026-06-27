## Context
This is a challenge from one of the members of the 38th cohort of the Data School UK.
As part of your task to help the Prep School evaluate performance, you discovered that students in classes 9A and 9B seem to struggle the most. You are now tasked with creating a list of all students and the percentile range of their results for each subject. For students that are in classes 9A or 9B you also need to add a Flag column in the output.

## Requirements

- Input the data
- For each subject, split the grades into 4 groups
- Replace the tile number with the relevant value from the Tiles input
- Join the data with the Student Information
- Trim Class field
- Create a flag column for students in class 9A or 9B, who are in the lower quartile for 2 or more subjects
- Filter to just the students flagged in the previous step
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Full name
    - Flag
    - Class
    - English
    - Economics
    - Psychology
