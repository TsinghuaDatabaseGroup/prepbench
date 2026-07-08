## Context

When Lorna suggested we set-up a challenge for Tableau users to not only complete a Workout Wedesday live but use Tableau Prep Builder to prepare their data then we jumped at the chance to collaborate. This week is held as a live session so we have built a combined challenge that should only take a few hours in total even if you new to either tool. To celebrate Tableau's Music month Lorna found a great data source on one of her favourite artists (Ed Sheeran) that led me to ask a question about one of my faves (Ben Howard). We want to analyse the two artists careers based on their touring patterns and as two UK-based singer-songwriters who appeared on the UK music scene at similar times, how have they developed. We have taken the gig history from concertarchives.org and done a little pre-cleaning as we wanted the challenge to take a suitable amount of time and not be completely imposible. For this challenge we have given you this gigs data along with a file of longitudes and latitudes for the location of the city / town hosting the gig.

## Requirements

- Input the data
- Join the data sets together
  - We want to keep all of the 'Gigs Data' even if there isn't a matching Lat / Long
- Split LongLat field to form Longitude and Latitude then remove the original LongLat field
- Break up the Concert field to find Fellow Artists who performed in the same gig and clean the field up by:
  - If the Concert does not contain a "/" then Fellow Artists should be blank.
  - Remove the Artist name from the Fellow Artist field and just leave a blank.
- Each Fellow Artist should have their own row
- Remove obvious duplicate records
- Add in the Home locations for each of our featured artists
- Output the data

## Output

- output_01.csv
  - 11 fields:
    - Longitude
    - Latitude
    - Fellow Artists
    - Artist
    - Concert Date
    - Concert
    - Venue
    - Location
    - Hometown
    - Home Longitude
    - Home Latitude
