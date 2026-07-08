## Context

Prep School must select applicants for the new academic year. Each applicant applies to exactly one of five courses (Business Management, Computer Science, Psychology, Engineering, Data Analytics). Each course has 20 places (100 total), and places must be allocated per course using a fixed regional quota of 75% East and 25% West (i.e., 15 East + 5 West per course).

Selections are made within each course by prioritising higher overall Grade Score, with proximity to the school (smaller distance) used as the tie-breaker when Grade Scores are equal. After selecting the accepted students, each accepted student’s secondary school should be labelled as High / Average / Low performing within their region based on that school’s contribution to filling the region’s available seats.

## Requirements

- Input the data.
- Create a student initials field from each student’s Full Name using:
  - the first letter of the first name, plus the first letter of the second name token;
  - if the second name token is double-barrelled (contains a hyphen), use only the first letter of the first part of that token.
- Join the applicants’ core table to the Additional Information table such that the result retains exactly 4,000 unique student records (one output record per student in the Additional Information table).
  - Perform the join by constructing a deterministic matching key using the student’s Date of Birth, School Name, and the three subject grade fields (English, Maths, Science), plus the computed initials to disambiguate where necessary.
  - If the applicants table contains more than one record matching the same join key, keep the match with the smallest Distance From School (Miles).
  - If any records still do not match when using the key that includes initials, perform a fallback match using the same key but excluding initials.
  - After the join, every student record must have a populated Subject Selection and Distance From School (Miles).
- Develop a ranking system that ranks each student within each (Subject Selection, Region) combination using:
  - primary sort: Grade Score descending (higher is better);
  - tie-breaker: Distance From School (Miles) ascending (closer is better).
- For each Subject Selection (course), select exactly:
  - the top 15 ranked students from the East region, and
  - the top 5 ranked students from the West region.
- Delete all rejected students, leaving only the 100 accepted students (20 per course across 5 courses).
- Remove unnecessary fields so the final dataset contains only the required output fields.
- For accepted students, compute secondary-school performance within each Region as follows:
  - Count accepted students per (Region, School Name).
  - Convert that count into a percentage of the total available seats for that Region, where total seats are:
    - East: 75 seats (15 seats × 5 courses),
    - West: 25 seats (5 seats × 5 courses).
  - Within each Region, label schools in a new column named School Status:
    - “High Performing” for the school(s) with the highest acceptance percentage in that region,
    - “Low Performing” for the school(s) with the lowest acceptance percentage in that region,
    - “Average Performing” for all other schools in that region.
  - Attach School Status back onto each accepted student using (Region, School Name).
- Ensure Date of Birth is output in `YYYY-MM-DD` format.
- Arrange the final rows deterministically by Subject Selection, then Region, then Grade Score (descending), then Distance From School (Miles) (ascending).
- Delete any unwanted fields and rearrange to give the output shown below.
- Output the data.

## Output

- output_01.csv
  - 11 fields:
    - Student ID
    - Full Name
    - Date of Birth
    - Region
    - School Name
    - School Status
    - Subject Selection
    - English
    - Maths
    - Science
    - Grade Score