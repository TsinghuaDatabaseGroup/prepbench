## Context
It's time for TC22 and in celebration of the hybrid virtual and in person conference this year we're bringing you a TC themed challenge! We want to compile a list of those who were unable to attend the sessions they registered for.

## Requirements

- Input the data
- In the Registrations Input, tidy up the Online/In Person field
- From the Email field, extract the company name
  - We define the company name as being the text following the @ symbol, up to the .
- Count the number of sessions each registered person is planning to attend
- Join on the Session Lookup table to replace the Session ID with the Session name
- Join the In Person Attendees dataset to the cleaned Registrations
  - You will need multiple join clauses
  - Think about the Join Type, we only want to return the names of those that did not attend the sessions they registered for
- Filter to only include those who registered to be In Person
- Join the Online Attendees dataset to the cleaned Registrations
  - You will need multiple join clauses
  - Think about the Join Type, we only want to return the names of those that did not attend the sessions they registered for
- Filter to only include those who registered to be Online
- Union together these separate streams to get a complete list of those who were unable to attend the sessions they registered for
- Count the number of sessions each person was unable to attend
- Calculate the % of sessions each person was unable to attend
  - Round this to 2 decimal places
- Remove unnecessary fields
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - Company
    - First Name
    - Last Name
    - Email
    - Online/In Person
    - Session not attended
    - Not Attended %
