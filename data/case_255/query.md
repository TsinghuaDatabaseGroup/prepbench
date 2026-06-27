## Context
We've been asked for many years is a way to understand the difficulty and techniques used by past challenges. At last, we bring you the data behind that! I've been chipping away at this in the background for many, many weeks and, unsurprisingly, there are definitely a few inconsistencies that we'll need to clean up! Never let your users have free text input, right? This will not only help everyone participating in Preppin' Data find the challenges they're most interested in, but it will also help us identify gaps and create challenges that continue to use different skillsets.

## Requirements

- Input the data
- Split the themes, so each theme/technique has its own field
- Reshape the data so all the themes are in 1 field
- Group the themes together to account for inaccuracies
  - Don't worry about being too accurate here, the main things to focus on it grouping things like Join/Joins and Aggregate/Aggregation. The way we've chosen to do it leaves us with 73 values, but that did involve a lot of manual grouping.
- Reshape the data so we can see how many challenges each Technique appears in, broken down by Level (as per the output)
- Create a Total field across the levels for each Technique
- Rank the challenges based on the Total field to find out which Techniques we should prioritise for challenge making
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - Priority
    - Technique
    - Beginner
    - Intermediate
    - Advanced
    - 3-in-1
    - Total
