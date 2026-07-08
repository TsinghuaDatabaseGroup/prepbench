## Context
There are 3 inputs this week: Host Countries, the history of all the medallists for each Olympics, a country codes lookup table.

## Requirements

- Input the data
- Make sure every medal has both a Country and Country Code associated with it
- Group together Canoe/Kayak and Canoeing Sports
- Group together sensible Disciplines
- Replace the word "metres"/"metre" in Events with an "m" abbreviation
- Replace the word "kilometres" in Events with an "km" abbreviation
- Change Sport from Swimming to Aquatics
- Output cleaned Medallists Dataset
- Aggregate to a row for each Event medal (i.e. we know longer need the Athlete names Level of Detail)
- Create a table showing total Gold, Silver and Bronze medals from each country for each year
- Output Country Medals Dataset
- Using the Hosts dataset, create a field for the Host Country
- Change the United Kingdom to Great Britain
- Output Host Cities Dataset
- Output the data
  - Remove exact duplicate records from the cleaned Medallists Dataset.

## Output

- output_01.csv
  - 5 fields:
    - Country
    - Gold
    - Silver
    - Bronze
    - Year

- output_02.csv
  - 9 fields:
    - Year
    - Host City
    - Host Country
    - Start Date
    - End Date
    - Games
    - Nations
    - Sports
    - Events

- output_03.csv
  - 9 fields:
    - Country
    - Code
    - Sport
    - Medal
    - Event
    - Athlete
    - Year
    - Event_Gender
    - Discipline
