## Context
This week Prep Air are looking into their Net Promoter Score (NPS) and how this compares with a variety of other new airlines. NPS usually takes the form of asking customers "How likely are you to recommend this company on a scale of 0-10?" You then subtract the detractors of your company from the promoters and end up with a score between -100 and +100. The higher the NPS, the better! However, like most metrics, on its own it doesn't tell you a lot. Do customers feel strongly one way or the other about any airlines? So it would be good to compare Prep Air's NPS with other airline's Net Promoter Scores too! In this challenge we'll use Z-Scores to standardise the scores and see whether Prep Air is above or below average.

## Requirements
- Input the data
- Combine Prep Air dataset with other airlines
- Exclude any airlines who have had less than 50 customers respond
- Classify customer responses to the question in the following way:
  - 0-6 = Detractors
  - 7-8 = Passive
  - 9-10 = Promoters
- Calculate the NPS for each airline
  - NPS = % Promoters - % Detractors
  - Note: I rounded the %s down to the nearest whole number, so if your answer differs slightly from mine then this could be why!
- Calculate the average and standard deviation of the dataset
- Take each airline's NPS and subtract the average, then divide this by the standard deviation
- Filter to just show Prep Air's NPS along with their Z-Score
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Airline
    - NPS
    - Z-Score
