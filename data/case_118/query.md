## Context
This week we are trying to find out more detail on what is going on with the project over runs in Prep Air (every data prepper's favourite airline). To get more detail than just what was shared last week we've uncovered the commentary log that sits behind our project management system. Like any system that holds the detail shown on the programme's interface in a log file, it has great detail but held in an unfriendly way. We need your help to get stuck into the messy data and extract out the useful details. One Excel file with five sheets of data: one main page of data with four lookup tables that will help you change some abbreviations and codes to be full words.

## Requirements

- Input the data
There are lots of different ways you can do this challenge so rather than a step-by-step set of requirements, feel free to create each of these data fields in whatever order you like:
- 'Week' with the word week and week number together 'Week x'
- 'Project' with the full project name
- 'Sub-Project' with the full sub-project name
- 'Task' with the full type of task
- 'Name' with the owner of the task's full name
- 'Days Noted' some fields have comments that say how many days tasks might take. This field should note the number of days mentioned if said in the comment otherwise leave as a null.
- 'Detail' the description from the system output with the project details in the [ ]
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - Week
    - Project
    - Sub-Project
    - Task
    - Name
    - Days Noted
    - Detail
