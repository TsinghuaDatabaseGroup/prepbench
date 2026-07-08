## Context
This week's challenge is inspired by some real life consulting work, replacing a very manual task with an automated process! Unique IDs are a great way to label your data, but issues can arise when trying to match internal IDs to 3rd Party IDs, as there could have been changes made to the naming convention by any number of people.
So how do we go about making some educated guesses and getting together a list of IDs that we can take back to the 3rd Party to complain about?

## Requirements

- Input the data
- Find the IDs that match perfectly and label them as such.
- For the remaining unmatched Internal and 3rd Party IDs, create all the possible matching IDs for each Scent.
- For each 3rd Party ID, find the Internal ID with the lowest sales difference.
- For each Internal ID, find the 3rd Party ID with the lowest sales difference.
- You should now have no duplicated IDs.
- Classify these IDs as "Matched on Scent".
- Join these IDs to the "Matched IDs".
- Classify IDs from Internal and 3rd Party Data which have not been matched and join these to create the output.
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Status
    - ID
    - 3rd Party ID
    - Scent
    - Sales
    - 3rd Party Sales
