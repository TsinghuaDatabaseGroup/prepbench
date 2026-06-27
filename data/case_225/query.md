## Context
This week the Prep School has decided to evaluate the quality of their teaching. As this is not an easy task they are trying to tackle it from different points of view. They have a team conducting surveys and one analysing student performance over the past year. As part of the analytics team, you have been tasked with identifying which classes struggle the most with each course so that the school can provide targeted support or adapt their approach to the curriculum.

## Requirements

- Input the data
- Join the datasets together
- Aggregate to get the average grade per class for each subject
- Pivot the data to get 3 columns and rename - Subject, Grade and Class
- Add a clean step to rank
  - In Tableau Prep -> right click the Grade column - create calculated field - Rank - Group by Subject
- Filter to the worst performing class for each subject
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Subject
    - Grade
    - Class
