## Context
Welcome to Preppin' Data 2020 Week 14. Fun fact: DS14 started at the Data School a year ago today! It seemed only fitting that a member of DS14 should therefore come up with this week's challenge. So, this week we're thinking about how to get your data in the right structure to build spider charts (aka radar charts) in Tableau Desktop. What better data to use than the measurements of actual spiders? The data comes from figshare.com and contains information about 2,841 different spiders - preferable to going out and collecting the data for ourselves.

## Requirements

- Input the data
- Filter out any specimen that doesn't have a measurement for each trait or those with '*'s against measurements.
- Clean up fields containing '_'s.
- We only want to consider species for whom the measurements of at least 10 different specimens were recorded.
- We'd like to aggregate our data to only contain the average measurements for each species.
- For each trait we want to normalise the values for each species so that they range between 0 and 1: zi=xi−min(x)max(x)−min(x)
  - Zi : The normalised value for the current **species and trait**.
  - Xi : The current value for the current **species and trait.**
  - Min(X) : The smallest overall value for the current **trait across all species.**
  - Max(X) : The largest overall value for the current **trait across all species.**
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Normalised Value
    - Max Value
    - Min Value
    - Value
    - Trait
    - Species
