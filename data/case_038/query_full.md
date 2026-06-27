## Context

You are given a clinic visit-level dataset and need to produce patient-level visit metrics that are attached back to each individual visit record. The goal is to identify, for every visit, when the patient first visited the clinic, how many total visits the patient has had, what number visit the current record represents in that patient’s sequence of visits, and whether the visit is the patient’s first (new) or a returning visit.

## Requirements

- Input the data.
- Connect to the Input data set `input_01.csv`, which contains (at minimum) the fields: `Date of Servce`, `VisitID`, `PatientID`, `Visit Type`, and `Doctor`.
- Use join and aggregation logic to compute metrics on each patient based on the dates they have visited the clinic, and attach those metrics back to each visit row (i.e., the output remains at the visit-record grain: one output row per input visit row).
- Parse `Date of Servce` as a date for sequencing and aggregation.
- Establish a deterministic ordering of visits within each `PatientID`:
  - Sort visits by `PatientID` ascending, then by parsed visit date ascending, and for ties on the same date sort by `VisitID` ascending.
- Create a field that provides the date a patient first visited the clinic:
  - For each `PatientID`, compute the minimum parsed visit date across that patient's visits.
  - Attach this value to every visit row for that patient as `First visit date`.
- Create a field that provides the number of times a patient has visited the clinic in total:
  - For each `PatientID`, count the total number of visit rows for that patient.
  - Attach this value to every visit row for that patient as `Total Patient visits`.
- Create a field that gives a patient’s visit number for each visit:
  - Within each `PatientID`, assign `Patient visit number` as 1 for the first visit in the deterministic ordering above, 2 for the next, and so on.
- Write a calculation that flags when a particular visit is a patient’s first visit:
  - If `Patient visit number` equals 1, set `New Patient Flag` to `New patient`; otherwise set it to `Returning patient`.
- Format date fields in the output as text using `DD/MM/YYYY`:
  - Format `Date of Servce` from the parsed visit date.
  - Format `First visit date` from the computed first-visit date.
- Output the data.

## Output

- output_01.csv
  - 9 fields:
    - Date of Servce
    - VisitID
    - PatientID
    - Visit Type
    - Doctor
    - Patient visit number
    - First visit date
    - Total Patient visits
    - New Patient Flag