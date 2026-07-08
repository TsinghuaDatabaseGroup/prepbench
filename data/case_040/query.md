## Context

This week is Tableau Conference week. A major conference happened last week and they need some Data help! Sudzilla, the annual conference for all things soap, was attended by our very own Chin & Beard Suds Co. A survey was sent to all participants and the results are in but the structure of the data isn't ideal for the analysis we want to do.

Summarising survey responses to understand the overall event is challenge. One metric that often gets used is Net Promoter Score (NPS). This takes the questions "On a Scale of 0-10, would you recommend [Enter Event / Product] to friends and family?" and converts it in to a percentage score. The reason why NPS is better than traditional satisfaction scores is the customers who have poor experiences will do damage to your brand (detractors) rather than just looking at those who are promoting your brand (promoters).

Through research, Promoters were found to be those who gave scores of 9 or 10. Detractors were a large range of 0-6. Scores of 7-8 are ignored from the overall calculation but are factored in to the number of responses.

The calculation is: (Promoters - Detractors) / Number of respondents × 100

## Requirements

- Input the data
- Work out the Net Promoter Score for Sudzilla using "On a scale of 0-10, how would you rate Sudzilla?"
- Split the 'What three words...' field in to individual words and use a grouping technique to clean these words
  - The technique used may change row count - try to get close
- Change food rating fields to 1-5 score (bad to good) and average the value. Rename this to Food Rating Score.
- Form an average score for the keynotes. Rename this to 'Keynote Rating Score'
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - NPS Score
    - Total Respondents
    - Promoter
    - Detractor

- output_02.csv
  - 8 fields:
    - Which three words would you use describe to Sudzilla? (separate with a comma) Split
    - Keynote Rating Score
    - Food Rating Score
    - Timestamp
    - On a scale of 0-10, how would you rate Sudzilla?
    - ___why?
    - What was your favourite giveaway at Sudzilla?
    - What was your favourite 'Soap Box' (breakout / customer speaker) session?
