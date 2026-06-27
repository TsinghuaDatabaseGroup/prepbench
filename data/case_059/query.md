## Context
In the Chin & Beard Suds Co IT department we are always looking to support our colleagues in the best way possible. As always, we are looking to improve our service and want to understand how the support department is currently performing. We have collected support ticket information from part of this year and want to answer some questions. A new line of data is created every time the status changes. This creates a sequential Status No, giving us a history of the progress each ticket has made.

## Requirements

- Input the data
- Input Data - This was updated on 26th Jan, to remove some duplicate Ticket IDs
- Clean Ticket ID/Names
- What is the current ticket status? Are they still open, how long have they been open, and how many business days has that been?
  - Business days are Monday-Friday, don’t worry about bank holidays! Some of our workers work on the weekends, if a case is closed on the weekend then we roll this back to the Friday. If a case is logged on the weekend, we roll these to the Monday.
  - Business days are also calculated down to the minute level. Eg, if a case was logged on 1st Jan 2020 00:00:00 then closed on 2nd Jan 2020 12:00:00 then this would be 1.5 days.
- Answer the following questions:
  - How many cases are in each status?
  - How many closed tickets have missed their SLA? How many are on track to meet their SLA?
  - What departments have the best SLA achieved %?
    - Closed cases only
    - Higher the percentage, the more cases have been closed under the SLA limit set
    - Rank from highest % to lowest %
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Current Status
    - Ticket Count

- output_02.csv
  - 2 fields:
    - Metric
    - Total

- output_03.csv
  - 3 fields:
    - Department Rank
    - Department
    - Achieved %
