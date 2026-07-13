## Requirements

- Input the data
- The webscraping isn't quite perfect and the table headers are repeated throughout the dataset, make sure these are removed
- Make sure that the Week field is numeric
- The Score field is made up of the Total Score and individual judges scores
  - Create a field for the total score
  - Count how many judges there were
  - Create an Avg Judge's Score field
    - i.e. Total Score/Number of Judges
- Since we're interested in couple's improvement from the start of the series and the end of the series, we only need to retain rows relating to the couple's first dance (which may not have been in week 1) and their dances in the final
  - This means we're only interested in couples who made it to the final
- Couples dance multiple times in the final. Take the average of their Avg Judge's Score
- Find the Percentage difference between their Avg Judge's Score for their first dance and the average for their dances in the final
- The final output should contain a row for each couple, with their Percentage difference and only the Avg Judge's Score in the final, along with the Result
  - i.e. whether they won, were a runner-up or came third
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Series
    - Couple
    - Finalist Positions
    - Avg Judge's Score
    - % Change
