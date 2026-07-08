## Context
We are revisiting our Prep Air Airline this week by looking at some flight details and trying to provide some data driven answers. As part of running an airline we are always interested in how successful the in-flight service is and if we can make any improvements to try to boost sales. For this week's challenge we have been provided with a selection of different data sources and we want to combine them to answer some questions that will help us to understand some purchasing patterns on the flights. We have the following inputs:
**Passenger List**
A list of all the passengers from a selection of flights. This includes their name, a passenger number, the flight number and the total they purchased whilst on the flight. Note, not all flights are full and can hold a maximum of 120 passengers.
**Seat List**
A mapping of where each passenger sits within each flight. This is the same for all flights across our fleet and includes the row number and seat letter within each row.
**Flight Details**
These are details about the flight number, departure and arrival times.
**Plane Details**
This documents where the business class section is on each of the planes. We provide free in-flight purchases for Business Class passengers.

## Requirements

- Input the data
- Assign a label for where each seat is located.
  - A & F - Window Seats
  - B & E - Middle Seats
  - C & D - Aisle Seats
- Combine the Seat List and Passenger List tables.
- Parse the Flight Details so that they are in separate fields
- Calculate the time of day for each flight.
  - Morning - Before 12:00
  - Afternoon - Between 12:00 - 18:00
  - Evening - After 18:00
- Join the Flight Details & Plane Details to the Passenger & Seat tables. We should be able to identify what rows are Business or Economy Class for each flight.
- Answer the following questions:
  - What time of day were the most purchases made? We want to take a look at the average for the flights within each time period.
  - What seat position had the highest purchase amount? Is the aisle seat the highest earner because it's closest to the trolley?
  - As Business Class purchases are free, how much is this costing us?
- Bonus: If you have Tableau Prep 2021.1 or later, you can now output to Excel files. Can you combine all of the outputs into a single Excel workbook, with a different sheet for each output?
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Rank
    - Depart Time of Day
    - Avg per Flight

- output_02.csv
  - 3 fields:
    - Rank
    - Seat Position
    - Purchase Amount

- output_03.csv
  - 3 fields:
    - Rank
    - Business Class
    - Purchase Amount
