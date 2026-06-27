## Context

Tableau Conference 2021 is here and we thought we'd put together a challenge themed around Brain Dates to celebrate! The idea is, how many people will you indirectly gain knowledge from as you attend brain dates? The people you're meeting with will have been to other brain dates across the conference, so they will be able to share their key insights and the collective knowledge will grow with every brain date held! I had a lot of fun putting this challenge together, even needing pen and paper at times to work out the final output, so I hope you'll enjoy putting your Preppin' skills to the test with this challenge too.

## Requirements

- Input the data
- Create a DateTime field for each Session
- Create a row for each Attendee and Join on the Lookup Table
- Create a Direct Contact Field for each Attendee
  - These are people they directly meet in the brain dates they attend
- Make sure Attendees don't have their own names listed as Direct Contacts
- Create an Indirect Contact field for each Attendee
  - These will be the Direct Contacts for each Attendee's Direct Contacts, for sessions that have happened prior to the session where they meet
  - Remember: order of sessions is important!
- If another attendee is classified as both a Direct and an Indirect Contact, classify them as a Direct Contact
- Reshape the data so that each row represents an attendee and a contact they've made, either Directly or Indirectly, for each subject matter
  - Ensure there are no duplicates!
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Subject
    - Attendee
    - Contact Type
    - Contact
