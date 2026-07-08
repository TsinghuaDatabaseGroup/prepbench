## Requirements

- Input the data
- Remove the airport names from the From and To fields
  - e.g. New York-JFK should just read New York
- Create a Route field which concatenates the From and To fields with a hyphen
  - e.g. Dubai - Dallas
- Split out the Distance field so that we have one field for the Distance in km and one field for the Distance in miles
  - Ensure these fields are numeric
- Rank the flights based on Distance
  - Use a dense rank in order to match the wikipedia page
- The Scheduled duration is a Date/Time data type. Change this to a string so that we only keep the time element
- Update the First flight field to be a date
- Join on the lat & longs for the From and To cities
- Output the data

## Output

- output_01.csv
  - 15 fields:
    - Rank
    - From
    - To
    - Route
    - Airline
    - Flight number
    - Distance - mi
    - Distance - km
    - Scheduled duration
    - Aircraft
    - First flight
    - From Lat
    - From Lng
    - To Lat
    - To Lng
