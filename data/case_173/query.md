## Requirements

- Input the data
- To create our gantt chart we'll need to work out how long each character is talking. To do this we can work out the difference from one timestamp to the next. However for the last lines of dialogue we'll need to know when the episode ends. To do this we'll need to union the dialogue with the episode details to find the last timestamp
- Create a rank of the timestamp for each episode, ordered by earliest timestamp
  - Think carefully about the type of rank you want to use
- Create a new column that is -1 the rank, so we can lookup the next line
- Create a duplicate dataset and remove all columns except
  - episode
  - next_line
  - time_in_secs
- Inner join these two datasets
- Calculate the dialogue durations
- Some character names are comma separated, split these names out and trim any trailing whitespace
  - It's ok to leave "ALL" as "ALL"
- Reshape the data so we have a row per character
- Filter the data for just Gameplay sections
- Ensure no duplication of rows has occurred
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - Episode
    - name
    - start_time
    - Duration
    - youtube_timestamp
    - dialogue
    - section
