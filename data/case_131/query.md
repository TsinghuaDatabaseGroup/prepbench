## Context

My partner is an amazing Excel user as are many of her colleagues. When in a pub, a frequent *getting to know you* question was "What's your favourite Excel function?". As a SQL / Tableau user, after my first meeting I knew I had to up my game. SUMIFS became my go to answer and that is one of the functions we will look to replicate in Prep this week. SUMIF, or SUMIFS if you have multiple conditions, allows you to scan a data set and summarise the values that match any condition you create. When working with large tables with multiple entries per category, this is a great way to create some totals to help you analyse the data set. Whilst SUMIF doesn't exist within Prep, the IF function and aggregation step can be used to create the same effect. Excel allows for lots of different types of aggregations so whilst SUMIF was my go-to answer: average, minimum, count etc are all possible too. The challenge this week is forming the logic in Prep to replicate SUMIFS and AVERAGEIFS.

## Requirements

- Input the data
- Form Flight name
- Workout how many days between the sale and the flight departing
- Classify daily sales of a flight as:
  - Less than7 days before departure
  - 7 or more days before departure
- Mimic the SUMIFS and AverageIFS functions by aggregating the previous requirements fields by each Flight and Class
- Round all data to zero decimal places
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Flight
    - Class
    - Avg. daily sales 7 days or more until the flight
    - Avg. daily sales less than 7 days until the flight
    - Sales less than 7 days until the flight
    - Sales 7 days or more until the flight
