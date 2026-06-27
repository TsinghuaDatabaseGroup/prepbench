## Context
Good news everyone! Joe was thrilled with the solution we came up with to solve his missing data problem. However, he realised that when he replicated it with the actual data, there was still one part that wasn't quite right. You see, if the missing training sessions occur on the very first date in the dataset, the workflow we built last week will not fill in the scores since we are only filling down from previous sessions. So in the below example, Agility session would only be filled in from the 4th August onwards. Joe would like the values for the 2nd & 3rd August to be 0.

## Requirements

- Input the data
- Replace the input data from last week's workflow with the new datasource
- In a new branch, keep only the first training session for each player and each session
- Work out the minimum date in the entire dataset
- Add in the dates between the minimum date and first session
- Assign these generated dates a Score of 0 and set their flag to be "Pre First Session"
- Combine these new rows with the new rows generated in last weeks challenge
- Be careful of duplication
- Ensure no weekends exist in your dataset
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Flag
    - Session Date
    - Player
    - Session
    - Score
