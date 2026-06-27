## Context
The Prep School wants to discourage term-time holidays by awarding attendance certificates at the end of the school year. They need to (1) identify the pupil(s) with the best attendance across the entire school and (2) identify the top 5% of pupils by attendance rate within each year group.

## Requirements
- Input the data.
  - Use three term-level attendance files (inputs `input_01.csv`, `input_02.csv`, `input_03.csv`) containing, at minimum, each pupil’s First Name, Last Name, Days Present, and Days Absent for that term.
  - Use the year group lookup file (`input_04.csv`) containing First Name, Last Name, and Year Group.
- Build a pupil identifier and display name:
  - Treat a pupil as uniquely identified by the combination of **First Name** and **Last Name**.
  - Create **Full Name** as `First Name + " " + Last Name`.
- Calculate each pupil’s attendance rate across the whole year:
  - Stack/append the three term datasets into a single set of term records.
  - For each pupil (First Name, Last Name), sum **Days Present** across all terms and sum **Days Absent** across all terms.
  - Compute **Total Days** = (yearly Days Present sum) + (yearly Days Absent sum).
  - Compute **Year Attendance Rate** = `(yearly Days Present sum / Total Days) * 100`, rounded to **2 decimal places**.
- Produce the overall school "Super Star Attendance" output (`output_01.csv`):
  - Find the maximum **Year Attendance Rate** across all pupils.
  - Keep all pupil(s) whose Year Attendance Rate equals that maximum (i.e., include ties).
  - Set **Rank** to `1` for every retained row.
  - For deterministic ordering when multiple pupils tie, order tied pupils by the order of their first appearance in the combined (term-1 then term-2 then term-3) stacked term records.
- Join on the Year Group data to support year-group awards:
  - Join `input_04.csv` to the yearly attendance results on **First Name** and **Last Name** using a **left join** from the year-group table to the attendance results (retain all rows from the year-group table).
- Produce the year-group “Great Attendance!” output (`output_02.csv`):
  - For each **Year Group**, identify the “top 5%” of pupils using a percentile-threshold approach:
    - Within each Year Group, compute the **95th percentile** of Year Attendance Rate using **linear interpolation**.
    - Select all pupils in that Year Group whose Year Attendance Rate is **greater than or equal to** that 95th-percentile threshold (include ties at the threshold).
    - If this selection would yield zero pupils for a Year Group, instead select exactly the single top pupil for that Year Group after applying the sorting rule below.
  - For deterministic selection and output within each Year Group, sort candidates by:
    1) Year Attendance Rate descending, then
    2) the original row order in the year-group input file ascending (use the year-group file’s row sequence as the tie-breaker).
  - Output only the three required fields for the selected pupils.
- Output the data as the two CSV files specified below.

## Output

- output_01.csv
  - 3 fields:
    - Full Name
    - Year Attendance Rate
    - Rank

- output_02.csv
  - 3 fields:
    - Year Group 
    - Full Name
    - Year Attendance Rate