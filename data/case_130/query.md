## Context
This week we are looking at a technique that is ubiquitous within Excel - the Pivot Table. We again re-visit the Allchains bike store and look restructuring a sales table across different items and stores.

## Requirements

- Input the data
- Remove any rows that contain returns (documented in the 'Status' field with a 'Return to Manufacturer')
- Remove the Status and Date fields
- Find the total items sold for each store by using a Fixed LOD calculation where we group by store and sum the number of items
- Pivot the table using a Rows to Columns pivot where we have the Item as our Pivoted Fields (the columns) and Sum Number of Items as the Rows
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Items sold per store
    - Wheels
    - Tyres
    - Saddles
    - Brakes
    - Store
