## Context

The Prep School are holding a disco for Year 5 and 6. Each student has chosen a song they would like played – but the DJ will only play songs with 5 or more votes! Your challenge is to find out which songs are going to be played at the disco.

## Requirements

- Input the data
- The organiser would like to join the student details to the students' song choices – join Year 5 Contact Details to Year 5 Song Choices, and the same for the Year 6 datasets.
- All the students need to be in the same table in order to count votes for each song. Use a Union step to combine the Year 5 data and the Year 6 data.
- There are now two columns that describe which song each pupil has voted for (Song Recommendation and Song Choice) we would like this information to be all in one column.
- Now we need to count how many pupils voted for each song in each year group.
- Using a clean step, rename the Full Name column 'Number of Votes'.
- Finally, let's see which songs made the cut. Using a clean step, filter the count of Full Name so that only songs with 5 or more votes are kept in the data set.
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Number of Votes
    - Year Group
    - Song Recommendation
