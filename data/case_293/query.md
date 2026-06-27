## Requirements

- Input the data
- Create an Initials field that is formed as two letters. The Consultant Forename and Consultant Surname fields hold the details (i.e. Carl Allchin in the data is 3,1 we need CA)
- Create an engagement start date and an engagement end date (the year is 2024 in case you are doing this task after the normal release week)
- Clean up the Grade field by finding the minimum grade per person within the data set (call this field 'Corrected Grade')
- Create an 'Engagement Order' based on the Engagement Start Date
- For each individual person (identified by unique initials), remove any engagements where the start date occurs before the previous Engagement End Date
- Join on the Grade details and remove the join clause fields
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Engagement Start Date
    - Engagement End Date
    - Initials
    - Engagement Order
    - Grade Name
    - Day Rate
