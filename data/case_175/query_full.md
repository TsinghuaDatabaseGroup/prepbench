## Context

You are preparing a curated table of the world’s longest flights. Starting from a flights list and a city coordinate lookup, standardize the origin/destination city names, derive route and distance fields, compute a distance-based rank that matches Wikipedia-style dense ranking, convert date/time fields into the required representations, and enrich each flight with latitude/longitude for both endpoints.

## Requirements

- Input the data from:
  - `input_01.csv`: the flights table (one row per flight record).
  - `input_02.csv`: a cities lookup table containing `City`, `Lat`, and `Lng`.

- Remove the airport names/codes from the `From` and `To` fields so they contain only the city name.
  - This removal should handle cases where an airport qualifier is appended to the city (for example, after a dash/en-dash suffix like `New York-JFK`, or via an added slash segment such as `City/Qualifier`), leaving just the city portion.

- Create a `Route` field by concatenating the cleaned `From` and `To` values with ` - ` (space-hyphen-space).

- Split the `Distance` field into two numeric fields:
  - `Distance - km`: extract the distance value expressed in kilometers from the `Distance` text.
  - `Distance - mi`: extract the distance value expressed in miles from the `Distance` text.
  - Ensure both extracted distance fields are numeric (integers).

- Rank the flights based on distance:
  - Compute `Rank` as a dense rank using `Distance - km` in descending order (longest distance = rank 1).
  - Use dense ranking (no gaps in rank values when distances tie).

- Convert `Scheduled duration` to a string containing only the time element:
  - If the field is a Date/Time type, format it as a time-only string in `HH:MM:SS`.
  - Otherwise, keep it as a string representation.

- Update the `First flight` field to be a date formatted as `DD/MM/YYYY`:
  - Parse month-name formats like `Mon D, YYYY` and `Month D, YYYY` into `DD/MM/YYYY`.
  - If `First flight` is already in `DD/MM/YYYY`, keep it in that format.

- Join latitude/longitude for both endpoints using `input_02.csv`:
  - Join `From` to `input_02.csv` on `From = City` using a left join; append `From Lat` and `From Lng`.
  - Join `To` to `input_02.csv` on `To = City` using a left join; append `To Lat` and `To Lng`.
  - If a city is not found in the lookup, keep the flight row and leave the corresponding coordinates blank/null.

- Output the data with exactly the specified fields, and sort the final output by `Rank` ascending.

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