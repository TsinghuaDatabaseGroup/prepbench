## Context

You have three input tables related to London attractions and London Underground stations. The goal is to (1) produce a year-level footfall dataset for attractions that also includes a 5-year average and a rank, (2) produce a cleaned attractions latitude/longitude lookup, and (3) produce a cleaned tube stations latitude/longitude lookup.

## Requirements

- Input the data from three CSV files:
  - Attraction Footfall (input_01.csv)
  - Location Lat Longs (input_02.csv)
  - London Tube Stations (input_03.csv)

- For the Attraction Footfall table (produce output_01.csv):
  - Ensure the first/identifier column is named **Attraction** (rename it from its original header if needed).
  - Filter out attractions with missing data by removing any rows that have missing/null values in any required field for this dataset (including any file-level missing-value markers that should be interpreted as nulls during ingestion).
  - Reshape the data from wide to long so there is one row per **Attraction** per **Year**:
    - Treat the year columns as five consecutive years: **2019, 2020, 2021, 2022, 2023**.
    - Create a **Year** field containing the year as an integer.
    - Create an **Attraction Footfall** field containing the corresponding footfall value for that attraction-year.
    - The output grain must be **one row per attraction-year**.
  - Multiply **Attraction Footfall** by **1000** to convert values to their true scale.
  - Calculate **5 Year Avg Footfall** for each attraction as the arithmetic mean of the (scaled) **Attraction Footfall** values across the five years.
    - Keep all year-level rows; the 5-year average must be repeated on each attraction’s year rows (i.e., join the per-attraction average back to the long, year-level data on **Attraction**).
  - Rank the attractions based on **5 Year Avg Footfall**:
    - Rank in descending order (largest average gets rank 1).
    - Use a dense ranking approach: ties share the same rank, and the next distinct value increments the rank by 1.
    - Store the rank as an integer in **Attraction Rank**.
  - Output exactly these fields in this order:
    - Attraction Rank, Attraction, 5 Year Avg Footfall, Year, Attraction Footfall

- For the Location Lat Longs table (produce output_02.csv):
  - The latitude and longitude are contained in a single field; split this into two separate fields:
    - Parse the combined coordinate field into **Attraction Latitude** and **Attraction Longitude**.
    - Convert both latitude and longitude to numeric values.
  - Output exactly these fields in this order:
    - Attraction Name, Attraction Latitude, Attraction Longitude

- For the London Tube Stations table (produce output_03.csv):
  - There are a lot of unnecessary fields; keep only the station name and location fields:
    - Use the station name field **Station**.
    - Use the latitude and longitude fields provided as **Right_Latitude** and **Right_Longitude**.
  - Clean up the field names by renaming:
    - Right_Latitude → **Station Latitude**
    - Right_Longitude → **Station Longitude**
  - There are a lot of duplicate rows; make sure each row is unique by removing exact duplicate rows after selecting/renaming the required columns.
  - Output exactly these fields in this order:
    - Station, Station Longitude, Station Latitude

- Output the data to the three specified CSVs.

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