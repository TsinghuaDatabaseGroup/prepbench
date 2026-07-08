## Context
Each vehicle listing is treated as a distinct vehicle identified by its registration number. The goal is to calculate, for each dealership, the average number of days it takes to sell a vehicle, measured from the first time that vehicle was advertised on the site.

## Requirements
- Input the data from:
  - `input_01.csv` (Ads dataset)
  - `input_02.csv` (Users dataset)
- Break the Users data set into individual records (you should have 365 rows):
  - The Users file contains a single text field holding multiple user tokens separated by commas.
  - Split this text into one row per user token.
- Parse each user token into the following components:
  - The 1st 7 characters are the User ID (`user_id`).
  - The last character is the user type: private individual (`P`) or dealership (`D`) (`user_type`).
  - For dealership users only (`user_type = 'D'`), the 3 characters immediately after the 7-character User ID (characters 8–10 of the token) are the Dealership ID; for non-dealership users, Dealership ID is blank.
- With the Ads data, remove any unsold vehicles:
  - Treat a vehicle as sold only if `sale_date` is present (not null/blank).
- Join the datasets together:
  - Join Ads to Users using `user_id` with a left join (keep all sold ads, bringing in user attributes where available).
  - After the join, only retain records that correspond to dealership listings (`user_type = 'D'`). Records that do not match to a user (and therefore have no `user_type`) must not be included.
- Find when an advert is first posted:
  - Parse the ad’s publish timestamp (`publish_ts`) as a datetime using the format `DD/MM/YYYY HH:MM:SS`.
  - For each vehicle (grouped by `registration_number`), compute `first_publish` as the minimum `publish_ts`.
- Only keep the records where the advert was first posted:
  - Keep only ad rows whose `publish_ts` equals the computed `first_publish` for that `registration_number`.
  - If multiple rows tie at the same earliest timestamp for a vehicle, keep all tied rows.
- Find the time between when a vehicle is first advertised on the site to when the vehicle was sold:
  - Parse `sale_date` as a datetime.
  - Compute the elapsed time in days as:  
    \[
    \text{Days to Sell} = \left\lceil \frac{\text{sale\_date} - \text{first\_publish}}{24 \times 3600 \text{ seconds}} \right\rceil
    \]
    where the difference is measured in seconds and then converted to days.
- Find the average days for each sale a dealership has listed (group up to the nearest whole day):
  - For each `Dealership ID`, compute the mean of `Days to Sell` across that dealership’s retained (first-posted) sold ads.
  - Round the resulting dealership average up to the nearest whole day (ceiling), and output it as an integer.
- Output the data.

## Output

- output_01.csv
  - 2 fields:
    - Dealership ID
    - Dealership Avg Days to Sell