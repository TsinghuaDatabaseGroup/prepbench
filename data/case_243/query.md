## Context

This Preppin' Data Challenge requires you to process the school's log of student class choices that were recorded in a structure that made sense for timetabling and reshape it so that the school has a breakdown of drop-out rates for each subject. Because the data was inputted manually there are typos in subjects that need to be corrected.

## Requirements

- Input the data
- Make sure Prep reads the first line of the file as headers.
- Pivot the data so that we have a row for each class choice.
- Group the Subject Names on Spelling to standardise the subject names and exclude nulls.
- Create a flag to mark the groups that are dropped or active.
- Aggregate the Data by Subject and Active Flag and count the students in each group (note you'll need to use Count rather than Count Distinct).
- Pivot the data so that we have a column for a count of students actively enrolled in a subject and for those who have dropped out of a subject.
- Make some row-level calculations to show the total enrollment in a subject (active + dropouts) and then create a rate for each subject showing the % of total enrollments that dropped out.
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Subject
    - Drop Outs
    - Active
    - Total Enrolled
    - Drop Out Rate
