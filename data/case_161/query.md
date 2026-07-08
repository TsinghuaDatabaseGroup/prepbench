## Context
In celebration of International Women's Day (even though it was yesterday), I thought it would be fun to take a look at which movies pass the Bechdel Test. If you're unfamiliar, there are 3 criteria to passing the Bechdel Test:
1. The film has to have at least two [named] women in it,
2. who talk to each other,
3. about something besides a man
The results may surprise you!

## Requirements

- Input the data
- Parse out the data in the Download Data field so that we have one field containing the Movie title and one field containing information about whether of not the movie passes the Bechdel Test
- Before we deal with the majority of the html codes, I would recommend replacing '&amp;' instances with '&' because of this film on the website incorrectly converting the html code
  - Example: "Toki wo kakeru sh&#333;jo (The Girl Who Leapt Through Time)" 
- Extract the html codes from the Movie titles
  - These will always start with a '&' and end with a ';'
  - The maximum number of html codes in a Movie title is 5
- Replace the html codes with their correct characters
  - Ensure that codes which match up to spaces have a space in their character cell rather than a null value
- Parse out the information for whether a film passes or fails the Bechdel test as well as the detailed reasoning behind this
- Rank the Bechdel Test Categorisations from 1 to 5, 1 being the best result, 5 being the worst result
- Where a film has multiple categorisations, keep only the worse ranking, even if this means the movie moves from pass to fail
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Movie
    - Year
    - Pass/Fail
    - Ranking
    - Categorisation
