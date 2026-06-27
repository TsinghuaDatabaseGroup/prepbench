## Context

You are preparing a contact-details extract for parents/guardians based on pupil records. Each record contains the pupil’s first and last name (not yet formatted for reporting), two possible parental first names, an indicator of which parental contact to use, and the preferred employer domain needed to construct an email address. You must also assign each pupil to an academic year based on their date of birth, where academic years start on 1 September.

## Requirements

- Input the data.
  - Read `input_01.csv`.
  - Treat each input row as one pupil record and produce one output row per input row.

- Form the pupil's name correctly for the records in the format `Last Name, First Name`.
  - Use the fields `pupil last name` and `pupil first name` to construct `Pupil's Name` as:  
    `pupil last name` + `", "` + `pupil first name`.

- Form the parental contact's name in the same format as the pupil's.
  - The Parental Contact Name 1 and 2 are the first names of each parent.
  - Use `Parental Contact` to select which parent first name to use:
    - If `Parental Contact` equals `1`, use `Parental Contact Name_1`.
    - Otherwise, use `Parental Contact Name_2`.
  - Construct `Parental Contact Full Name` as:  
    `pupil last name` + `", "` + selected parent first name.

- Create the email address to contact the parent using the format `Parent First Name.Parent Last Name@Employer.com`.
  - Use the selected parent first name as `Parent First Name`.
  - Use the pupil’s last name as `Parent Last Name`.
  - Use `Preferred Contact Employer` as the employer portion.
  - Construct `Parental Contact Email Address` exactly as:  
    selected parent first name + `"."` + `pupil last name` + `"@"` + `Preferred Contact Employer` + `".com"`.

- Create the academic year the pupils are in.
  - Each academic year starts on 1st September.
  - Parse `Date of Birth` as a date using the format `M/D/YYYY` (month/day/four-digit year).
  - Determine the pupil’s “academic start year” from their date of birth:
    - If the birth date is on or after 1 September of the birth year, the academic start year is the birth year.
    - If the birth date is before 1 September of the birth year, the academic start year is the birth year minus 1.
  - Convert academic start year to `Academic Year` using these rules (consistent with “Year 1 is anyone born after 1st Sept 2014; Year 2 is anyone born between 1st Sept 2013 and 31st Aug 2014 etc”):
    - If academic start year is 2014 or later, `Academic Year = 1`.
    - If academic start year is 2013, `Academic Year = 2`.
    - If academic start year is 2012, `Academic Year = 3`.
    - If academic start year is 2011, `Academic Year = 4`.
    - For earlier academic start years, continue the same pattern:  
      `Academic Year = (2014 - academic start year) + 1`.
  - Output `Academic Year` as an integer.

- Remove any unnecessary columns of data.
  - Keep only the required output fields listed below.

- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Academic Year
    - Pupil's Name
    - Parental Contact Full Name
    - Parental Contact Email Address