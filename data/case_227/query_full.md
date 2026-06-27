## Context

The Prep School in Dataville is selecting a small cohort from a combined pool of applicants nominated by two independent regions (East and West). Each region supplies applicant records in a slightly different format. The goal is to standardize both regional extracts, combine them into a single consistent applicant dataset, compute comparable grade-based scores, reshape the data so each student appears once with their subject grades and total score, and then enrich the results with school information via a lookup table.

## Requirements

- Input the data.
  - Use the East applicants table and the West applicants table as the two sources of student application records.
  - Input the School Lookup table for later enrichment.

- Standardize student identifiers and region.
  - For the East table:
    - Fix the Student ID column so that it contains only the 5-digit numeric student identifier (extract the numeric code from the existing Student ID value).
    - Add a Region field with the value `EAST`.
  - For the West table:
    - Split the Student ID column so that:
      - Student ID contains only the 5-digit numeric student identifier (the numeric portion of the existing Student ID).
      - A newly formed Region column identifies the region as `WEST`.

- Create a standardized student name field.
  - For both tables, use the First Name and Last Name columns to create a new `Full Name` column formatted as:
    - `FIRSTNAME LASTNAME`
    - all capital letters.

- Standardize date of birth formatting.
  - Make sure both tables have the same date format by converting `Date of Birth` to `YYYY-MM-DD` in both regional tables.

- Standardize grade representations.
  - For the West table, convert the values in the Grade column from numbers to letters using:
    - 1 = A, 2 = B, 3 = C, 4 = D, 5 = E, 6 = F
  - Keep the East table’s Grade values as letter grades.

- Combine regional records.
  - Combine (append/union) the standardized East and West tables into one table with 12,000 rows.
  - The combined table at this stage should be at the grain of one row per student per subject (i.e., each student contributes one row per subject).

- Score each subject grade.
  - Create a new scoring field for each row based on the letter grade:
    - A = 50, B = 40, C = 30, D = 20, E = 10, F = 0
  - If a row’s grade does not match one of the defined letter grades, assign a score of 0 for that row.

- Reshape to one row per student and compute total score.
  - Transform the combined long table so that each student is represented by only ONE row with:
    - three separate columns for their English, Maths, and Science grades (letter values), and
    - a `Grade Score` column equal to the sum of the three subject scores for that student.
  - Define the student uniquely by the combination of: Student ID, Full Name, Date of Birth, and Region.
  - When reshaping grades into subject columns, if more than one grade exists for the same student and subject, keep a single grade value (use the first available record for that student-subject).

- Enrich with school information.
  - Input the School Lookup table and combine it with the one-row-per-student table using Student ID as the join key.
  - Use a left join so that every student remains in the output even if there is no matching lookup record (school fields may be blank/null in that case).

- Clean and organise your table to match the required output structure.
  - Ensure the final dataset contains exactly the required fields with the required names.

- Output the data.

## Output

- output_01.csv
  - 10 fields:
    - Student ID
    - Full Name
    - Date of Birth
    - Region
    - School Name
    - School ID
    - English
    - Science
    - Maths
    - Grade Score