## Requirements

- Input the data
- Before we bring the 2 datasets together, we want to know how many Additional Requests each guest has made
  - Update *N/A* values to *null* and make sure this counts as 0 Additional Requests
- Match the guests to the rooms which have capacity for their entire party
- Filter so that double/twin bed preferences are adhered to
- Ensure guests who have accessibility requirements are only matched with accessible rooms
- Calculate the Request Satisfaction % for each room
- Filter so that guests are only left with rooms with the highest Request Satisfaction %
- Finally, for the rooms with the largest capacity, we want to ensure guests with larger parties are prioritised. Filter the data to remove parties that could fit into smaller rooms
- Output the data

## Output

- output_01.csv
  - 11 fields:
    - Party
    - Adults in Party
    - Children in Party
    - Double/Twin
    - Requires Accessible Room?
    - Additional Requests
    - Request Satisfaction %
    - Room
    - Adults
    - Children
    - Features
