## Context

Chin & Beard Suds Co. has experienced multiple system outages and needs a consolidated, comparable view of downtime across systems and error types. Two sources are available: (1) an automatically generated downtime log with precise timestamps, and (2) a manually maintained spreadsheet where staff record issues with less precision. The goal is to combine these sources so that automatic logs take precedence over overlapping manual entries, then quantify downtime and each event’s contribution to total downtime per system.

## Requirements

- Input the data from the two provided CSV files:
  - **Automatic log (input_01.csv)** containing at least: `Start Date / Time`, `End Date / Time`, `System`, `Error`.
  - **Manual log (input_02.csv)** containing separate date and time components at least: `Start Date`, `Start Time`, `End Date`, `End Time`, plus `System`, `Error`.

- Parse and construct timestamp fields:
  - For the automatic log, convert `Start Date / Time` and `End Date / Time` to true datetime values.
    - The expected format is `YYYY-MM-DD HH:MM:SS` (e.g., "2019-04-13 07:55:23").
    - Parse using standard datetime parsing that recognizes this format.
  - For the manual log, create:
    - `Start Date / Time` by combining `Start Date` + `Start Time` into a single datetime.
    - `End Date / Time` by combining `End Date` + `End Time` into a single datetime.
    - Combine by concatenating the date string, a single space character, and the time string (e.g., "2018-04-13" + " " + "09:00:00" → "2018-04-13 09:00:00").
    - The expected date format is `YYYY-MM-DD` and time format is `HH:MM:SS`.
    - Parse the combined string using standard datetime parsing.

- Resolve ambiguities in the data:
  - **Time precision differences**: The automatic log and manual log may record different time points for the same or overlapping events (e.g., automatic log records "09:03:22" while manual log records "09:00:00" for the same date and system). This is expected and does not affect the overlap detection logic, which uses interval intersection based on the parsed datetime values regardless of precision differences.

- Add an `Error Source` field to each dataset:
  - Automatic log rows must have `Error Source` = `Automatic Error log`.
  - Manual log rows must have `Error Source` = `Manual capture error list`.

- Bring the datasets together while removing duplicate/overlapping records from the manually captured dataset:
  - A manual record must be considered a duplicate (and removed) if it overlaps in time with **any** automatic-log record for the **same `System`**.
  - Define overlap using strict interval intersection:
    - An automatic interval overlaps a manual interval if  
      `auto_start < manual_end` **and** `auto_end > manual_start`.
  - Keep all automatic-log records; when overlap occurs, the automatic data must override the manual data by excluding the manual record entirely.

- Combine the remaining records into one event-level table (one row per downtime event after the manual overlap removal):
  - Preserve all automatic rows.
  - Append the remaining (non-overlapping) manual rows after the automatic rows.
  - To ensure deterministic output ordering, sort the retained manual rows by `Start Date / Time` in descending order before appending.

- Work out the duration of each event:
  - Compute the true duration as the difference between `End Date / Time` and `Start Date / Time` in seconds (used for downstream calculations even if not output directly).
  - Convert duration to hours as:  
    `hours = seconds / 3600`.
  - Create `Downtime in Hours` as the event duration in hours rounded to **1 decimal place**.

- Understand the “% of downtime” per system in hours:
  - For each `System`, compute:
    - `Total Downtime in Hours` = sum of `Downtime in Hours` across all events for that system, rounded to **1 decimal place**.
    - `% of system downtime` for each event = (event’s **unrounded** duration in hours) divided by that system’s **unrounded** total duration in hours, rounded to **2 decimal places**.

- Format datetime fields for output:
  - Output `Start Date / Time` and `End Date / Time` as strings in the format `DD/MM/YYYY HH:MM`.

- Output the data exactly with the required columns and file name.

## Output

- output_01.csv
  - 8 fields:
    - % of system downtime
    - Total Downtime in Hours
    - Downtime in Hours
    - Error Source
    - Error
    - Start Date / Time
    - End Date / Time
    - System