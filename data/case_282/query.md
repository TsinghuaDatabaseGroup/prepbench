## Requirements

- Input the data
- Join together the Stages and Stage Type table
- Create a field called 'Time Trial ?' to determine if the stage was a Time Trial (Time trials are shown as either Individual Time Trials (ITT)s or Team Time Trials (TTT)s)
- Create an 'Origin - Destination' field and a 'Stage Number' field (For the Stage Number, capture the Prologue stage as 0)
- Join in the 'Wins' data. Keep all of the stages and add additional details of the stages Cavendish has won (You'll need to prepare the data to be able to join to the data set you've built thus far)
- Remove all duplicate fields created within the Joins
- Input the Grand Tour Starts but keep only the Tour de France starts
- Rename: GC to 'General Classification Finishing Position'; Points to 'Points Finishing Position'
- Join the races started to the overall data set to provide the overall finishing position and points finishing position
- Create a 'Stages Won?' field from the Stage Number Won to a 'Yes' when Cavendish won the stage or NULL if not.
- Output the data

## Output

- output_01.csv
  - 9 fields:
    - Stage Won?
    - Stage Number
    - Origin - Destination
    - Time Trial?
    - General Classification Finishing Position
    - Points Finishing Position
    - Year
    - KM
    - Stage Type
