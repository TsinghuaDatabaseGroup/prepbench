## Requirements

- Input the data
- For the London Tube Stations table:
  - There are a lot of unnecessary fields, only keep information about the station name and location
  - Clean up the field names
  - There are a lot of duplicate rows. Make sure each row is unique
- For the Attraction Footfall table:
  - Filter out attractions with missing data
  - Reshape the data so there is a row for each year, for each attraction
  - The footfall values need to be multiplied by 1000 to give their true values
  - Calculate the average footfall for each attraction, whilst keeping all the detail of individual years. Call the new field 5 Year Avg Footfall
  - Rank the attractions based on this 5 Year Avg Footfall
- For the Location Lat Longs table:
  - The information about the latitude and longitude is contained in a single field, split these values into 2 separate fields
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Attraction Rank
    - Attraction
    - 5 Year Avg Footfall
    - Year
    - Attraction Footfall

- output_02.csv
  - 3 fields:
    - Attraction Name
    - Attraction Latitude
    - Attraction Longitude

- output_03.csv
  - 3 fields:
    - Station
    - Station Longitude
    - Station Latitude
