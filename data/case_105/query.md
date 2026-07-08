## Context
For this week's challenge we're looking at a dataset that was used in December 2020 for Sports Viz Sunday (thanks to Kate Brown for sharing!) This dataset comes from the PGA and LPGA 2019 Golf tours and lists the total prize money for the top 100 players. For those of us who aren't too familiar with golf, the PGA is the men's tour, whilst the LPGA is the women's tour.

## Requirements

- Input the data
- Answer these questions:
  - What's the Total Prize Money earned by players for each tour?
  - How many players are in this dataset for each tour?
  - How many events in total did players participate in for each tour?
  - How much do players win per event? What's the average of this for each tour?
  - How do players rank by prize money for each tour? What about overall? What is the average difference between where they are ranked within their tour compared to the overall rankings where both tours are combined?
    - Here we would like the difference to be positive as you would presume combining the tours would cause a player's ranking to increase
- Combine the answers to these questions into one dataset
- Pivot the data so that we have a column for each tour, with each row representing an answer to the above questions
- Clean up the Measure field and create a new column showing the difference between the tours for each measure
  - We're looking at the difference between the LPGA from the PGA, so in most instances this number will be negative
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Measure
    - PGA
    - LPGA
    - Difference between tours
