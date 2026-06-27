## Context
This week is a continuation of the challenge that we started last week. As a recap, check the challenge post from Preppin' Data week 20.
Like any data project, new data is flowing in continually and our patient data is no exception. Sadly this week, we have received a CSV file instead of XLSX and we seem to have a different column name too... the joy of manual data capture.
Also, last week, we had included an additional tab of data that we didn't set any requirements for (although some of you jumped in and worked with that anyway!). The unused data was all about check-ups and how much additional cost they will place on Chin & Beard Suds Co. The same cost model is used but each check-up is classed as an individual visit.

## Requirements

- Input the data
- Add new Patient Data
- Add Frequency of Check-Ups data
- Use Frequency of Check-Ups to determine when a patient will re-enter hospital by using Frequency from the **date the patient leaves hospital**
- Understand the additional cost incurred by the extra days stayed (treat each Check-up as a new entry in to hospital - ie Check-up day one is £100 no matter length of previous stay)
- Refresh the Data Outputs from Week 20
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Avg Cost per Day
    - Total Cost per Day
    - Date in Hospital
    - Number of Patients

- output_02.csv
  - 3 fields:
    - Avg Cost per Day
    - Total Cost per Day
    - Patient Name
