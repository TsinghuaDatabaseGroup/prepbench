## Context
The introductory challenges are over for2022 so it's time to step up (a little). I've tried to use the techniques you've learnt over the past4 challenges to form the basis for this week. Also, I will provide a little less direct instruction and more requirements that you will need to workout how to approach them. This week's challenge is looking to take the numeric score our students' have received and turn it to:
- A letter grade (our students' parents prefer this)
- A score that goes towards their High School applications
The challenge's aim is understand how many points on average a student who receives an A gets. This will help us understand how many students would get a higher score than the average student receiving an A without receiving one.

## Requirements

- Input the data
- Divide the students grades into 6 evenly distributed groups (order by Score descending, then Student ID ascending to break ties).
  - By evenly distributed, it means the same number of students gain each grade within a subject
- Convert the groups to two different metrics:
  - The top scoring group should get an A, second group B etc through to the sixth group who receive an F
  - An A is worth10 points for their high school application, B gets8, C gets6, D gets4, E gets2 and F gets1.
- Determine how many high school application points each Student has received across all their subjects
- Work out the average total points per student by grade
  - ie for all the students who got an A, how many points did they get across all their subjects
- Take the average total score you get for students who have received at least one A and remove anyone who scored less than this.
- Remove results where students received an A grade (requirement updated2/2/22)
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - Avg student total points per grade
    - Total Points per Student
    - Grade
    - Points
    - Subject
    - Score
    - Student ID
