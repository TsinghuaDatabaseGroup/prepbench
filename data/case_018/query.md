## Requirements

- Input the data
- Consider only TV shows and Movies - we aren't making some straight to video OVA here.
- Ignore any anime without a rating or without any genres.
- Ignore any anime with less than 10000 viewers (i.e. [Members]) - we expect to have way more than this.
- For each genre and type combination (e.g. Action & TV, Romance & Movie) return the following information:
  - The average rating (to 2 decimal places).
  - The average viewership (to 0 decimal places).
  - The maximum rating.
  - A prime example of the genre and type combination (i.e. the anime with the max rating for the combo).
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Genre
    - Type
    - Avg Rating
    - Max Rating
    - Avg Viewers
    - Prime Example
