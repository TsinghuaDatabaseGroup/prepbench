## Context
A shipping distribution company transports valuable cargo for customers all around the world using three different types of boat. They keep the basic details for each departure in a table called Departure Details. They sell and allocate space on their departures based on the weight and volume of the cargo. They keep the details of each allocation in a table called Allocation Details. In the last 3 months they’ve begun noticing issues where more weight or volume is being allocated than the boats can actually carry. This means customers are turning up at the port with cargo which the company is then having to turn away and refund. They want to identify and flag departures with weight or volume allocation issues before the day of departure.

## Requirements

- Input the data
- Download the input file.
- Figure out how much weight and volume has been allocated for each departure in the Allocation Details table.
- Find a way to flag departures on the Departure Details table which have had too much cargo weight or volume allocated.
- Output the data

## Output

- output_01.csv
  - 8 fields:
    - Ship ID
    - Departure Date
    - Max Weight
    - Max Volume
    - Weight Allocated
    - Volume Allocated
    - Max Weight Exceeded?
    - Max Volume Exceeded?
