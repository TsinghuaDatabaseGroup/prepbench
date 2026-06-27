## Context
The Head Honchos of Chin & Beard Suds Co want to understand how their website is performing. Are the web pages being tested on the right devices and Operating Systems? Are we considering language and cultural references? To conduct this analysis, our website stats are held in a frustrating way but this analysis won't be done just once so we want to set up the flows so they are available in a reusable way to conduct this analysis whenever needed.

## Requirements

- Input the data
- Create a single table for each of Origin, Operating System and Browser
- Clean up values and percentages
  - Convert any < 1% values to 0.5
- If percent of total fields don't exist in any files, create these and make them an integer
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Change in % this month
    - Browser
    - This Month Pageviews Value
    - This Month Pageviews %
    - All Time Pageviews Value
    - All Time Pageviews %

- output_02.csv
  - 6 fields:
    - Change in % this month
    - Operating System
    - This Month Pageviews Value
    - This Month Pageviews %
    - All Time Pageviews Value
    - All Time Pageviews %

- output_03.csv
  - 6 fields:
    - Change in % pageviews
    - This Month Pageviews %
    - All Time Views %
    - Origin
    - All Time Pageviews
    - This Month Pageviews
