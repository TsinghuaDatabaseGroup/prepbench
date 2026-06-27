## Context

As the Prep School principal, you have heard worrying reports about some of your students being constantly late to class. Naturally, you want to investigate these rumors and get to the bottom of what is happening in your establishment. Luckily, your pupils need to swipe their student cards to enter the building every morning. The attendance log you have access to describes the daily arrival time of 8 students for the year 2022. Null values are generated if the student is absent that day.

You are particularly interested in understanding on what day of the week your students are the latest and which students are "very late" (more than 5 minutes) the most often.

## Requirements

- Input the data
- Exclude null values from the Arrival Time field. These are days the student wasn't present
- Turn the Scheduled Start Time and Arrival Time fields into Date Time fields
- Calculate how many minutes late each student is each day
  - If they arrive before the Scheduled Start Time, they'll have a negative value for this field
- Rank the days of the week in order of Average Lateness
- Convert the Average Lateness into 2 fields: 1 for Minutes and 1 for Seconds
- Create Output 1
- Rank the students by the percentage of days they were "very late" (more than 5 minutes) during the year
- Create Output 2
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Rank
    - Day of the Week
    - Minutes Late
    - Seconds Late

- output_02.csv
  - 3 fields:
    - Rank
    - Student ID
    - % Days Very Late
