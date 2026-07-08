## Requirements

- Input the data
- Combine the files
- Keep only relevant fields
- Extract the Report years from the file paths
- Create a Year field based on the the first year in the Report name
- Some companies have changed names over the years. For each EmployerId, find the most recent report they submitted and apply this EmployerName across all reports they've submitted
- Create a Pay Gap field to explain the pay gap in plain English
- You may encounter floating point inaccuracies. Find out more about how to resolve them
- In this dataset, a positive DiffMedianHourlyPercent means the women's pay is lower than the men's pay, whilst a negative value indicates the other way around
- The phrasing should be as follows:
  - In this organisation, women's median hourly pay is X% higher/lower than men's.
  - In this organisation, men's and women's median hourly pay is equal.
- Output the data，deduplicate records to avoid duplicate rows affecting evaluation

## Output

- output_01.csv
  - 7 fields:
    - Year
    - Report
    - EmployerName
    - EmployerId
    - EmployerSize
    - DiffMedianHourlyPercent
    - Pay Gap
