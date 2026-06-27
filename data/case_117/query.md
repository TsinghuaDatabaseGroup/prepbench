## Context
This week's challenge is focused on Dates and the calculation functions available to you. This week we would like you to prepare your data for building a Gantt chart and supporting information on a dashboard (you don't have to build the dashboard but bonus points if you do!). Prep Air (our fake airline) has had a number of projects that have been over-running and the leadership team want to know why. The data starts in a state I've seen in a few systems. Preparing the data to make analysis easier is the aim this week.

## Requirements

- Input the data
- Workout the 'Completed Date' by adding on how many days it took to complete each task from the Scheduled Date
- Rename 'Completed In Days from Schedule Date' to 'Days Difference to Schedule'
- Your workflow will likely branch into two at this point:
  - Pivot Task to become column headers with the Completed Date as the values in the column
  - You will need to remove some data fields to ensure the result of the pivot is a single row for each project, sub-project and owner combination.
  - Calculate the difference between Scope to Build time
  - Calculate the difference between Build to Delivery time
  - Pivot the Build, Deliver and Scope column to re-create the 'Completed Dates' field and Task field
    - You will need to rename these
  - You don't need to do anything else to this second flow
- Now you will need to:
  - Join Branch 1 and Branch 2 back together
  - Calculate which weekday each task got completed on as we want to know whether these are during the weekend or not for the dashboard
  - Clean up the data set to remove any fields that are not required.
- Output the data

## Output

- output_01.csv
  - 10 fields:
    - Completed Weekday
    - Task
    - Scope to Build Time
    - Build to Delivery Time
    - Days Difference to Schedule
    - Project
    - Sub-project
    - Owner
    - Scheduled Date
    - Completed Date
