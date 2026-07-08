## Context
For TC22, compile a consolidated list of registrants who did not attend the conference sessions they registered for, across both in-person and online attendance types. The final output should identify each missed session per person and quantify how often each person missed their registered sessions.

## Requirements
- Input the data.
- Use the Registrations Input as the primary dataset of session registrations (one record per person–session registration, identified by the person fields and `Session ID`).
- In the Registrations Input, tidy up the `Online/In Person` field by standardizing it into two canonical values only:
  - `Online`
  - `In Person`
  - Data cleaning for `Online/In Person` field:
    - Convert all values to case-insensitive matching before standardization
    - Apply the following explicit mapping for spelling variants and errors:
      - `ONLINE`, `Onlin`, `Onlyne` → `Online`
      - `IN PERSON`, `Im Person`, `In Persn`, `In Persoon` → `In Person`
    - All other case-insensitive matches to "online" should map to `Online`
    - All other case-insensitive matches to "in person" or "in-person" should map to `In Person`
- From the `Email` field, extract the company name into a new field `Company`.
  - Define `Company` as the text after the `@` symbol and before the first `.` that follows.
  - Ambiguity resolution for company name extraction:
    - For emails like `user@de.vu`, extract `de` (the text between `@` and the first `.`)
    - For emails like `user@subdomain.company.com`, extract `subdomain` (the text between `@` and the first `.`)
    - This rule applies uniformly regardless of domain structure (single-level or multi-level domains)
    - If an email does not contain `@` or does not contain `.` after `@`, set `Company` to empty string or null
- Count the number of sessions each registered person is planning to attend:
  - Compute `Sessions Registered` as the count of registration records per person and attendance type, grouping by `First Name`, `Last Name`, `Email`, and `Online/In Person`.
  - Attach this per-person value back to each corresponding registration record.
- Join on the Session Lookup table to replace `Session ID` with the session name:
  - Left-join Registrations to the Session Lookup on `Session ID` to obtain the session name field `Session`.
- Identify sessions not attended for in-person registrants:
  - Filter registrations to `Online/In Person = 'In Person'`.
  - Join the In Person Attendees dataset to these filtered registrations using multiple join clauses:
    - Match on `Session`, `First Name`, and `Last Name`.
  - Use a join strategy that returns only those registration records with no matching attendee record (i.e., sessions that were registered for but not attended).
- Identify sessions not attended for online registrants:
  - Filter registrations to `Online/In Person = 'Online'`.
  - Join the Online Attendees dataset to these filtered registrations using multiple join clauses:
    - Match on `Session` and `Email`.
  - Use a join strategy that returns only those registration records with no matching attendee record (i.e., sessions that were registered for but not attended).
- Union together the in-person and online “not attended” results to produce a complete list of missed registered sessions.
  - The resulting dataset grain must be one row per person–session that was registered for but not attended.
- Rename the session name field to `Session not attended` for the missed-session rows.
- Count the number of sessions each person was unable to attend:
  - Compute `Sessions Not Attended` as the count of missed-session rows per person and attendance type, grouping by `First Name`, `Last Name`, `Email`, and `Online/In Person`.
  - Attach this per-person value back to each corresponding missed-session row.
- Calculate the % of sessions each person was unable to attend:
  - `Not Attended % = (Sessions Not Attended / Sessions Registered) * 100`
  - Round this to 2 decimal places.
- Remove unnecessary fields so that only the required output fields remain.
- Output the data.

## Output

- output_01.csv
  - 7 fields:
    - Company
    - First Name
    - Last Name
    - Email
    - Online/In Person
    - Session not attended
    - Not Attended %