## Requirements

- Input the data
- Add a year field for the Series: Series 1 and 2 were in 2004; subsequent series are annual (Series 3 in 2005, etc.)
- Remove repeated table headers from the dataset
- Split the Week field into a numeric value and extra details into Theme Week; further split Theme Week so Final/Semi Final/Quarter Final details go into a Stage field
- Split the Score field into Total Score and Judges Scores (since the number of judges varies by series/week)
- For group dances (identified by "group" or "marathon" in the Dance field):
  - Update the Couple field to "Group"
  - Ensure only 1 row per group dance
- Split the Music field into separate rows for each song, with Song and Artist in separate fields
- Combine the Film and Musical fields into one (max 1 theme per week)
- Remove unnecessary fields
- Output the data

## Output

- output_01.csv
  - 13 fields:
    - Year
    - Series
    - Week
    - Stage
    - Theme
    - Theme Detail
    - Couple
    - Total Score
    - Judges Scores
    - Dance
    - Song
    - Artist
    - Result
