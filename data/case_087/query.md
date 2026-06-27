## Context
Welcome to Tableau Conference-ish! Every year we like to create a special conference focused challenge. This year is no different. We can't meet in person this year so instead we've arranged to capture the zoom logs of comments from the prep focused session at the Conference. We want to understand who attended and how many questions and answers were delivered through this format.

Inputs: One file but a few sheets: Individual session logs. There are three sessions: one for APAC, one for EMEA and one for AM (the Americas).

## Requirements

- Input the data
- Make a date time field to represent local time. The session was on 7th October 2020 at 2pm for everyone.
- Make sure you know which comment came from which session
- Split the comments into two:
  - Everyone's first comment (except Carl Allchin's) is saying where they are from and whether it's their first session
  - Every subsequent comment is either a question or answer
- Work out where people are from for cities and countries.
  - Clean up any rogue values
  - EMEA and APAC list their city and country
  - Folks from AM list their city and country unless they are from the US where they list their city and state. Feel free to add in the country as the United States rather than the State.
  - Apply a data role of city and country and ONLY return VALID results
  - **Participants to exclude due to invalid City/Country validation:** Arsene Xie, Leona Lai, Jenny Martin, Rosario Gauna
- Count the number of questions and answers at each session excluding everyone's first comment
- Work out the times to make them all equal Greenwich Mean Time (GMT)
  - APAC is 11 hours before GMT
  - EMEA is 1 hour before GMT
  - AM is 5 hours after GMT
- Output two data sets
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Instances
    - Question or Answer
    - Location

- output_02.csv
  - 6 fields:
    - Date (GMT)
    - Location
    - City
    - First Time Indicator
    - Country
    - Who
