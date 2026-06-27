## Context
This challenge is part of the ongoing series related to "Prep" School provided by DS38.
The Prep School is facing an epidemic - too many students are being taken out of class for term time holidays! Thus the staff have come up with their best idea to discourage swapping out Maths class for a ski holiday to Val Thorens, awards for good attendance, because there is no better way to incentivise children than with a laminated sheet of paper and a gold star. These awards will be presented at the end of the school year in the annual Prize Giving Ceremony.
As such, the Prep School needs to figure out which pupils are eligible for these awards. First, they want to give year group level awards, with the top 5% of students in each year group receiving this 'Great Attendance!' award. Secondly, they want to give a 'Super Star Attendance' award to the pupil(s) with the best attendance out of the entire school.

## Requirements

- Input the data
- Create a Full Name field for each student
- Calculate the attendance rate across the whole year (rounded to 2 decimal places)
- Find the student(s) with the overall highest attendance rate and output this as a CSV
- Join on the Year Group Data
- Find the top 5% of students with the highest attendance rates for each year group and output this as a CSV
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Full Name
    - Year Attendance Rate
    - Rank

- output_02.csv
  - 3 fields:
    - Year Group
    - Full Name
    - Year Attendance Rate
