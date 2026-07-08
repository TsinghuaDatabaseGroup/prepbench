## Context

This week's challenge involves creating contact details for parents. We have the pupil's name, although it's not in the correct format, and will use the pupil's last name to match to the parent's details. We also have the employer for the parental contact so we can form an email address to contact them.

## Requirements

- Input the data
- Form the pupil's name correctly for the records in the format Last Name, First Name
- Form the parental contact's name in the same format as the pupil's
  - The Parental Contact Name 1 and 2 are the first names of each parent.
  - Use parental contact column to select which parent first name to use along with the pupil's last name
- Create the email address to contact the parent using the format Parent First Name.Parent Last Name@Employer.com
- Create the academic year the pupils are in
  - Each academic year starts on 1st September.
  - Year 1 is anyone born after 1st Sept 2014
  - Year 2 is anyone born between 1st Sept 2013 and 31st Aug 2014 etc
- Remove any unnecessary columns of data
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Academic Year
    - Pupil's Name
    - Parental Contact Full Name
    - Parental Contact Email Address
