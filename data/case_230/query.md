## Context
The Prep School is keen on developing athletes from amongst their students. They want to identify and rank the top 100m and 200m athletes. Each student listed has taken part in either the 100m or 200m sprint. Some work needs to be done to find, rank and clean the dataset.

## Requirements

- Input the data
- Join the students basic information with their event and track time
- Join the benchmark table with the right students
  - Note: the number of rows should still be 300 after the join
- Filter out the students that did not fall within the benchmark
- There has been an error with the collection of the times, so remove any 200m times that fall below 25 seconds
- Rank the students fastest to slowest for each event
- Output the data

## Output

- output_01.csv
  - 9 fields:
    - Rank
    - id
    - first_name
    - last_name
    - Gender
    - Age
    - Event
    - time
    - Benchmark
