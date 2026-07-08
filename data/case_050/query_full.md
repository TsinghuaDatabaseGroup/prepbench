## Context
Chin & Beard Suds Co. collected customer survey responses but did not prevent customers from submitting multiple responses, creating duplicates that distort Net Promoter Score (NPS) analysis. The goal is to produce a clean, de-duplicated dataset that supports analysis of both a customer’s first-impression NPS and their most up-to-date NPS, while still being usable for aggregations at country and store level.

## Requirements
- Input the data.
  - Read `input_01.csv`, which contains one row per survey answer, with a survey-response identifier (e.g., `Response`) and a `Question Number`/`Answer` pair.
  - Treat `Response` as the identifier for a single completed survey instance; multiple rows may share the same `Response` (one per question answered).

- Change the Question Number for the question asked (i.e., reshape the answer rows into named fields per response).
  - For each `Response`, create the following response-level fields from the corresponding `Question Number` values:
    - `1` = completion date (date component)
    - `2` = completion time (time component)
    - `3` = NPS recommendation score
    - `3a` = positive free-text reason (“If you would, why?”)
    - `3b` = negative free-text reason (“If you wouldn't, why?”)
  - If a `Response` has multiple rows for the same `Question Number`, keep the first available answer for that response/question combination.

- Carry forward customer/store attributes at the response level.
  - For each `Response`, take `Country`, `Store`, `Name`, and `DoB` from the response’s records (using a single consistent record per `Response`).

- Clean the Country and Store names.
  - Standardise country names to English place names.
  - Standardise store names so that store naming is consistent within each country.

- Clean up the dates and times to create a `Completion Date` as a Date Time field.
  - Parse the completion date (from Question `1`) and completion time (from Question `2`) and combine them into a single datetime timestamp.
  - If the time represents midnight as “24:00”, interpret it as `00:00` and roll the completion datetime forward by one day.
  - If either the date or time cannot be parsed for a response, set its completion datetime to null; such responses must not be used for first/latest selection.

- Understand the age of the customer based on their Date of Birth (DoB).
  - Nulls are ok: if DoB is missing or cannot be interpreted as a date, the age should be null.
  - Compute age as the difference in calendar years between the reference date **22nd January 2020** and the customer's year of birth (i.e., `2020 - birth_year`).

- Define eligible responses for first/latest selection.
  - An eligible response is one that has a non-null `Completion Date` (i.e., both the date and time components were successfully parsed and combined into a valid datetime timestamp).
  - Only eligible responses can be considered for first/latest selection within each customer group.

- Find the first answer for each customer in each store and country.
  - Define the grouping keys as: `Country`, `Store`, `Name`.
  - Within each group, identify the eligible response with the earliest completion datetime as the "first".

- Find the latest answer for each customer in each store and country (if there are multiple responses).
  - Within each group, identify the eligible response with the latest completion datetime as the “latest”.
  - Retain at most two records per group: the first eligible response and the latest eligible response.
    - **Selection Rule**: If the identified "First" and "Latest" responses are the exact same record (same Response ID), output only that one row. If they are different records, output both rows.

- Remove any answers that are not a customer's first or latest.
  - After the first/latest selection, keep only the selected response records.
  - Set `Result (First / Latest)` to:
    - `First` for the first-kept record in the group
    - `Latest` for the latest-kept record in the group when both a distinct first and a distinct latest are kept; otherwise the single kept record should remain labelled `First`.

- Classify the `NPS Recommendation` question based on the standard logic:
  - Convert the NPS score (Question `3`) to an integer where possible; if it cannot be converted, treat it as null.
  - Create indicator fields:
    - `Detractor` = 1 if score is 0–6 (inclusive), else null
    - `Passive` = 1 if score is 7–8 (inclusive), else null
    - `Promoter` = 1 if score is 9–10 (inclusive), else null

- Output formatting rules needed for consistent downstream analysis.
  - Output `Completion Date (Date Time stamp)` as a datetime string formatted `DD/MM/YYYY HH:MM:SS`.
  - Output the NPS score in the field `Would you recommend C&BS Co to your friends and family?` as an integer (nullable).
  - Output `Age of Customer` as an integer (nullable).

- Output the data.

## Output

- output_01.csv
  - 12 fields:
    - Country
    - Store
    - Name
    - Completion Date (Date Time stamp)
    - Result (First / Latest)
    - Would you recommend C&BS Co to your friends and family?
    - Promoter
    - Passive
    - Detractor
    - Age of Customer
    - If you would, why?
    - If you wouldn't, why?