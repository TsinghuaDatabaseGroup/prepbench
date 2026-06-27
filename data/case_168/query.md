## Context
This challenge was inspired by a recent use case from a client. It involves bringing together 2 datasets which have different levels of aggregation. They were initially trying to do this in Tableau Desktop but getting a bit muddled with the calculations going on "in the background." So let's use the power of Prep to map out the process and make everything much clearer.

## Requirements

- Input the data
- Check the location field for spelling errors
- Fix the date fields so they are recognised as date data types
- Aggregate the data to find the total duration of each streaming session (as identified by the timestamp)
- We need to update the content_type field:
  - For London, Cardiff and Edinburgh, the content_type is defined as "Primary"
  - For other locations, maintain the "Preserved" content_type and update all others to have a "Secondary" content_type
- To join to the Avg Pricing Table, we need to work out when each user's first streaming session was. However, it's a little more complex than that.
  - For "Primary" content, we take the overall minimum streaming month, ignoring location
  - For all other content, we work out the minimum active month for each user, in each location and for each content_type
- We're now ready to join to the Avg Pricing Table
- For "Preserved" content, we manually input the Avg Price as £14.98
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - userID
    - timestamp
    - location
    - content_type
    - duration
    - Avg_Price
