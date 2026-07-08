## Context
As an extra challenge, typed calculations are forbidden! That's right, we've got another CLICK ONLY challenge for you to really showcase the power of Tableau Prep. Remember to keep an eye on the recommendations and you are allowed to rename things.

## Requirements
- Input the data
- The first issue is that some people forgot they filled in the survey and filled it out twice with the same information. We need to filter out these duplicates.
- For the first output, we want a count of how many people are watching on each device.
  - Unfortunately, this was a free text box on the survey. Many responses have multiple values.
  - The Devices Input contains the device types we were hoping for.
  - All other answers should be labelled as "Other" - excluding blanks/"etc." responses.
- For the second output, we want to rank each show by its average rating.
  - Separate out the shows that respondents have been watching.
  - Remove the years in the brackets at the end of each film/show in the UK Netflix content list. Make sure there are no duplicates.
  - Join the list of UK Netflix content to the survey responses, so we can check that there hasn't been any confusion (lying) going on when writing a show in the "Other" response free text.
    - Only accept "other" responses that have one show in the free text answer, as otherwise we won't know which show the rating refers to!
  - Prepare the ratings responses so that we have one column containing all the show names and one containing all the ratings.
  - Now combine this with our list of verified shows and the people who watched them.
  - Calculate the average rating for each show.
  - Create a dense rank so we know what order we should watch these shows in.
- Output the data

## Output

- output_01.csv
  - 2 fields:
    - Device
    - Count

- output_02.csv
  - 3 fields:
    - Rank
    - Show
    - Rating
