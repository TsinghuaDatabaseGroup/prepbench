## Requirements

- Input the data
- Remove repeated table headers from the dataset (due to imperfect webscraping)
- Ensure the Week field is numeric
- Process the Score field (composed of Total Score and individual judges scores):
  - Create a field for the total score
  - Count the number of judges
  - Create an Avg Judge's Score field (Total Score divided by Number of Judges)
- Retain only rows for each couple's first dance (may not be Week 1) and their dances in the final (only include couples who made it to the final)
- For couples who danced multiple times in the final, calculate the average of their Avg Judge's Score
- Find the Percentage difference between their Avg Judge's Score for the first dance and the average Avg Judge's Score in the final
- The final output should have one row per couple, including: Percentage difference, Avg Judge's Score in the final, and Result (win, runner-up, third place)
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Series
    - Couple
    - Finalist Positions
    - Avg Judge's Score
    - % Change
