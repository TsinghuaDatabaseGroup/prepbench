## Context

You are preparing an automated Secret Santa email list. Each participant (the “Secret Santa”) should be assigned exactly one recipient (the “Secret Santee”) based on alphabetical ordering of participant names, and you will generate standardized email subject/body text to send the assignments.

## Requirements

- Input the data.
- Treat each row in the input as one Secret Santa participant and their email address.
- Assign Secret Santas to Secret Santees that follow them in the alphabet:
  - Sort all participants by the `Secret Santa` name in ascending alphabetical order.
  - For each participant in this sorted list, assign their Secret Santee as the next participant in the sorted list.
  - The last participant in the sorted list wraps around: their Secret Santee is the first participant in the sorted list (i.e., if no one follows Tom alphabetically, Tom’s Secret Santee is Ellie as the first alphabetically).
- Create fields to support automated emailing:
  - `Email Subject` must be the constant text: `Secret Santa`
  - `Email Body` must be exactly:  
    `{Secret Santa} the results are in your secret santee is: {Secret Santee}. Good luck finding a great gift!`  
    where `{Secret Santa}` is the participant’s name and `{Secret Santee}` is the assigned recipient’s name.
- Output the data:
  - Produce one output row per Secret Santa participant, containing the email and the generated subject/body.
  - Output rows must be ordered in reverse of the alphabetical sort order used for assignment (i.e., from the last name in the alphabetical list back to the first).

## Output

- output_01.csv
  - 3 fields:
    - Email
    - Email Subject
    - Email Body