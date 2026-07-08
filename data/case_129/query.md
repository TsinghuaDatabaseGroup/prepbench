## Context
There is one input this week, detailing the time of each trip the lift takes, including which floor the passengers enter the lift and which floor the passengers leave the lift. For simplicity, assume that the lift does not stop mid-journey to pick up new passengers, but completes its current trip before starting a new one.

## Requirements

- Input the data
- Create a TripID field based on the time of day
  - Assume all trips took place on 12th July 2021
- Calculate how many floors the lift has to travel between trips
  - The order of floors is B, G, 1, 2, 3, etc.
- Calculate which floor the majority of trips begin at - call this the Default Position
- If every trip began from the same floor, how many floors would the lift need to travel to begin each journey?
  - e.g. if the default position of the lift were floor 2 and the trip was starting from the 4th floor, this would be 2 floors that the lift would need to travel
- How does the average floors travelled between trips compare to the average travel from the default position?
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Default Position
    - Avg travel from default position
    - Avg Travel between trips currently
    - Difference
