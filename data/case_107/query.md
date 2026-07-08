## Context
We will need to make some assumptions as part of our data prep:
- Customers often don't sing the entire song
- Sessions last 60 minutes
- Customers arrive a maximum of 10 minutes before their sessions begin

## Requirements

- Input the data
- Calculate the time between songs
- If the time between songs is greater than (or equal to)59 minutes, flag this as being a new session
- Create a session number field
- Number the songs in order for each session
- Match the customers to the correct session, based on their entry time
  - The Customer ID field should be null if there were no customers who arrived 10 minutes (or less) before the start of the session
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Session #
    - Customer ID
    - Song Order
    - Date
    - Artist
    - Song
