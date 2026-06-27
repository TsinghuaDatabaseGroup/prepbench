## Context
The Prep School issues termly grade reports for each student, with one file per term. Each report contains four subject grades and a report date that may be written in different date formats. The school needs two prepared datasets:
1) A term-by-term view of each student’s GPA (average across subjects) together with a 3-term moving average of GPA to support monitoring academic performance over time.
2) A prize-winners view showing only the students who qualify for awards in specific terms, including the award date (term date) and the 3-term moving average GPA used to determine eligibility.

## Requirements
- Input the data.
  - Read the six term files `input_01.csv` through `input_06.csv`.
  - Read the student lookup file `input_08.csv` containing student names.
- Bring together the term data into 1 table.
  - For each term file, add a `Term` field set to `Term 1` … `Term 6` (based on which file the row came from).
  - Append (union) all six terms into a single dataset at a grain of **one row per student per term**.
- Parse the different date time formats as we will need this for Output 2.
  - Create a standardized `Term Date` from the input `Date` field.
  - If the date is provided as a year-month only (YYYY-MM), treat it as that month’s report date by setting the day to the 16th.
  - All terms report on the 16th day of the month.
  - Output `Term Date` formatted as `DD/MM/YYYY`.
- Calculate each student's GPA for each term i.e. their average grade across subjects.
  - Compute `GPA` as the arithmetic mean of the four subject grade fields: `Subject_1_Grade`, `Subject_2_Grade`, `Subject_3_Grade`, and `Subject_4_Grade`.
  - Round `GPA` to 2 decimal places.
- Calculate a 3 term moving average of each student's GPA, rounded to 2 decimal places.
  - For each student (`id`), order terms chronologically by term number (Term 1 → Term 6).
  - Compute `3 Term GPA Moving Average` as a rolling mean over the current and prior two terms (window size = 3).
  - Only populate the moving average when all three terms exist for that student (i.e., require three terms in the window); otherwise leave it null/blank.
  - Round `3 Term GPA Moving Average` to 2 decimal places.
- Use the student lookup table to bring in names for the students and use calculated fields to get the full name of each student.
  - Build `Student Name` by concatenating the lookup fields as `first_name + ' ' + last_name`.
  - Join names onto the combined term dataset using a left join on `id` (keep all student-term rows even if a name is missing).
- For Output 1:
  - Finally create a variable that orders the table by Student Name Descending and Time Ascending so that the Prep School has an ordered table that they can look through alphabetically and see how the moving average of GPA changes over time.
    - Sort by `Student Name` descending, then by term number ascending.
    - Create `Rank` as the 1-based row number after this final sort.
- For Output 2:
  - In a separate flow after full name is calculated, filter to keep only terms 3 and 6, then create percentiles for each term based on the moving average of GPA.
    - Filter to `Term 3` and `Term 6` only.
    - Exclude rows where `3 Term GPA Moving Average` is null (since percentile/top selection is based on the moving average).
    - For each of the two terms independently, identify the top students by `3 Term GPA Moving Average` consistent with a “top 2%” selection implemented as a fixed top-count per term:
      - For Term 3: keep the top 11 rows.
      - For Term 6: keep the top 13 rows.
    - Within each term, order rows to determine “top” using these tie-breakers in sequence:
      1) `3 Term GPA Moving Average` descending
      2) `GPA` descending
      3) `Student Name` ascending
  - Filter to students in the top 2%.
- Output the data.
  - Write `output_01.csv` and `output_02.csv` with exactly the fields listed below.

## Output

- output_01.csv
  - 7 fields:
    - Rank
    - id
    - Student Name
    - Term
    - Term Date
    - GPA
    - 3 Term GPA Moving Average

- output_02.csv
  - 6 fields:
    - id
    - Student Name
    - Term
    - Term Date
    - GPA
    - 3 Term GPA Moving Average