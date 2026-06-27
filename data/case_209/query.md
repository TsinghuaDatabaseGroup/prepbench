## Requirements

- Input the data
- Reshape the data so we have 5 rows for each customer, with responses for the Mobile App and Online Interface being in separate fields on the same row
- Clean the question categories so they don't have the platform in from of them
  - e.g. Mobile App - Ease of Use should be simply Ease of Use
- Exclude the Overall Ratings, these were incorrectly calculated by the system
- Calculate the Average Ratings for each platform for each customer
- Calculate the difference in Average Rating between Mobile App and Online Interface for each customer
- Catergorise customers as being:
  - Mobile App Superfans if the difference is greater than or equal to 2 in the Mobile App's favour
  - Mobile App Fans if difference >= 1
  - Online Interface Fan
  - Online Interface Superfan
  - Neutral if difference is between -1 and 1
- Calculate the Percent of Total customers in each category, rounded to 1 decimal place
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Preference
    - % of Total
