## Context
Chin & Beard Suds Co. wants to manage its marketing mailing list in the presence of unsubscribe requests submitted via a website form that captures only first name, last name, and the unsubscribe date. The business needs (a) an updated list of customers who can still be marketed to, including customers who previously unsubscribed but later resubscribed, and (b) an analytical summary showing unsubscribe timing, customer value, resubscription behavior, and product interest—while also retaining subscribed and resubscribed customers for comparison.

## Requirements
- Input the data from the three provided CSV files:
  - Mailing list (contains at least email, Sign-up Date, and Liquid/Bar indicators).
  - Unsubscribe list (contains at least first_name, last_name, and Date).
  - Customer sales / lifetime value (contains at least email, Liquid Sales to Date, Bar Sales to Date).
- Treat the Liquid / Bar 1/0 indicators as interest flags only (i.e., convert them to boolean “Interested …” fields for grouping and output; do not use the original 1/0 values directly in analysis).
- Join the Mailing List to the Unsubscribe List to determine each customer's unsubscribe date using a name-to-email matching key constructed as follows:
  - From the unsubscribe list: build a key as **first initial + last name**.
  - From the mailing list: derive a key from the email local-part (before "@").
  - Match by checking whether the mailing-list-derived key **starts with** the unsubscribe-derived key (case-insensitive comparison). If multiple unsubscribe keys match a single email, select the match with the **longest** unsubscribe key (most specific).
  - If multiple unsubscribe records exist for the same unsubscribe-derived key, keep only the **latest** (maximum) unsubscribe date.
  - If an email has no match, its unsubscribe date remains blank/null.
- Parse and interpret dates deterministically:
  - Parse mailing list **Sign-up Date** (from input_01.csv) as a date in `YYYY-MM-DD` format (e.g., `2016-01-14`).
  - Parse unsubscribe list **Date** (from input_02.csv) as a date in `DD.MM.YYYY` format (e.g., `23.04.2018`).
- Derive customer **Status** using the attached unsubscribe date and sign-up date:
  - **Subscribed**: no unsubscribe date is found.
  - **Resubscribed**: an unsubscribe date is found and it is **earlier than** the sign-up date.
  - **Unsubscribed**: an unsubscribe date is found and it is **on or after** the sign-up date.
- Add customer value measures by joining sales to the mailing list on **email** (left join from mailing list to sales).
- Derive interest fields for outputs:
  - **Interested in Liquid Soap** = boolean version of the Liquid indicator.
  - **Interested In Soap Bars** = boolean version of the Bar indicator.
- Create two outputs:
  1. A summarised dataset for analysis that includes unsubscribed customers bucketed by tenure-to-unsubscribe, and also includes subscribed/resubscribed groups for context.
  2. An email-level dataset representing the customers who can still be marketed to (Subscribed and Resubscribed only).
- Tenure bucketing for unsubscribed customers:
  - Compute “months before unsubscribed” as the difference in whole months ignoring day-of-month:  
    \[(Unsubscribe year − Sign-up year) * 12 + (Unsubscribe month − Sign-up month)\]
  - Bin this month difference into the following groups with left-inclusive boundaries: **0-3, 3-6, 6-12, 12-24, 24+**.
  - For Subscribed and Resubscribed rows in the summary output, leave the tenure group blank.
- Aggregations for the summarised output:
  - Group by **Months before Unsubscribed group**, **Status**, **Interested in Liquid Soap**, **Interested In Soap Bars**.
  - Aggregate:
    - **email** = count of emails in the group.
    - **Liquid Sales to Date** = sum within the group.
    - **Bar Sales to Date** = sum within the group.
- Output formatting and inclusion rules:
  - The marketable email-level output must include only **Resubscribed** and **Subscribed** customers (exclude Unsubscribed).
  - In the email-level output, format **Sign-up Date** and (when present) **Unsubscribe Date** as `DD/MM/YYYY`; for Subscribed customers set **Unsubscribe Date** to a blank string.
  - Order the summarised output deterministically by:
    1) tenure bucket order: 0-3, 3-6, 6-12, 12-24, 24+, then blank;  
    2) status order: Unsubscribed, then Resubscribed, then Subscribed;  
    3) Interested in Liquid Soap (ascending), then Interested In Soap Bars (ascending).
  - Output the data as the two CSVs described below.

## Output

- output_01.csv
  - 7 fields:
    - Months before Unsubscribed group
    - Status
    - Interested in Liquid Soap
    - Interested In Soap Bars
    - email
    - Liquid Sales to Date
    - Bar Sales to Date

- output_02.csv
  - 8 fields:
    - Status
    - email
    - Interested in Liquid Soap
    - Interested In Soap Bars
    - Sign-up Date
    - Unsubscribe Date
    - Liquid Sales to Date
    - Bar Sales to Date