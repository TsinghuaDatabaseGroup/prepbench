## Context
I often see dashboards and wonder about the data prep behind them. Sometimes the most beautiful of dashboards can be hiding the most horrendous of data preparation. Let's take this Viz of the Day from dataschooler Matthew Armstrong. The visualisation itself is fairly simple, but how did the data start off?

## Requirements

- Input the data
- Lines of the poem will not contain any HTML, css or js *e.g. , e9=new Object() etc.* Filter out any rows which are not lines of the poem
- Wordsworth is very original, so there shouldn't be any duplicate lines in our data set. Filter out any repeated rows
- The first line of each poem is also the title of the poem. Ensure this is the case and number the lines of each poem
- Split the data out so there is a line for each word and assign a word number for each line
- Split the data into individual letters and combine with the associated Scrabble score
- Aggregate so each word has a Scrabble score
- Create a flag for the highest scoring word in each poem
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - Poem
    - Line #
    - Line
    - Word #
    - Word
    - Score
    - Highest Scoring Word?
