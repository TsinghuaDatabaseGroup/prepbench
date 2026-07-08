## Context
You are given two related input datasets representing (1) customer complaints and (2) a reference list that maps complaint keywords to the department responsible. The goal is to attribute each complaint to one or more departments based on keyword matches, compute complaint volume per customer, and produce a structured output for downstream reporting.

## Requirements
- Input the data from two sources:
  - A complaints table containing at minimum the fields **Name** and **Complaint**.
  - A keyword-to-department table containing at minimum the fields **Keyword** and **Department**.
- Restrict processing to the required fields only:
  - From the complaints table: **Name**, **Complaint**.
  - From the keyword table: **Keyword**, **Department**.
- Standardize complaint text for matching and for output:
  - For each complaint, create a standardized complaint text by treating missing complaints as empty text, trimming leading/trailing whitespace, and converting to lowercase.
  - Use this standardized (lowercased) complaint text as the value written to the output **Complaint** field.
- Prepare the keyword-to-department reference for matching:
  - Exclude any keyword rows where **Keyword** or **Department** is empty.
  - For matching purposes, treat keywords as trimmed and lowercased text (the output department label should remain exactly as provided in the reference table).
- Count the number of complaints per customer:
  - Compute **Complaints per Person** as the total number of complaint records associated with each **Name**.
  - Attach this count to every output row for that person.
- Allocate complaints to departments via keyword matching (keyword-driven classification rather than a key-based join):
  - For each complaint, identify every keyword whose lowercased form appears as a substring within the standardized complaint text.
  - For each matched keyword, determine its first occurrence position in the complaint text and use this to order keywords by appearance (earlier positions first).
  - If a given keyword matches multiple times in the same complaint for the same department, include it only once for that department.
  - If a given keyword matches multiple different departments (i.e., the same keyword appears in multiple keyword-department mappings), include it once in each department's keyword list where it matches.
- Create a comma-separated field of keywords per complaint and department:
  - For each complaint, group matched keywords by **Department**.
  - For each (complaint, department) group, populate **Complaint causes** as the comma-separated list of that department’s matched keywords, ordered by first appearance in the complaint text.
  - Output one row per (complaint, department) when a complaint matches keywords from multiple departments.
- Handle unclassified complaints:
  - If a complaint matches no keywords, output exactly one row for that complaint with **Department** = `Unknown` and **Complaint causes** = `other`.
  - If a matched record has a missing department label, classify **Department** as `Unknown`.
- Output the data as specified.

## Output

- output_01.csv
  - 5 fields:
    - Complaint
    - Complaints per Person
    - Complaint causes
    - Department
    - Name