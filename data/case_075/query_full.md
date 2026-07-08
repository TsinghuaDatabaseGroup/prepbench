## Context
Attendees purchased tickets priced at £100 (GBP) and can choose one of three refund options: a full cash refund, a credit note for next year, or no refund (waiving the refund). Refund accounting must be expressed in each attendee’s local currency based on their selected country.

You are provided with three input datasets representing the Attendee List, Account Manager assignments, and Exchange Rates.

## Requirements
- Input the data from the provided files:
  - Attendee List (attendee-level records, including name, email, country, and refund type).
  - Account Manager table (mapping companies to account managers).
  - Exchange Rates (GBP to local currency rates).
- Derive a company identifier from each attendee’s email:
  - Take the substring immediately after the `@` symbol.
  - From that substring, take only the portion before the first `.` (dot).
  - Use this derived value solely for matching to the Account Manager table.
- Join the Account Manager and Attendee datasets:
  - Create a matching key from the Account Manager table by lowercasing its company field (the field named `Company List`).
  - Left-join attendees to the Account Manager table on:
    - attendee derived company identifier (lowercased for matching) = lowercased `Company List`.
  - Retain all attendee rows even if no Account Manager match exists.
  - For the output “Company Name” field, use the original-cased company name from the Account Manager table (`Company List`) so that capitalization is preserved as provided there.
- Assign a currency to each attendee based on country using the following fixed mapping:
  - United States → USD
  - France → EUR
  - Germany → EUR
  - Italy → EUR
  - Spain → EUR
  - Canada → CAD
  - Mexico → MXN
  - United Kingdom → GBP
- Calculate the ticket price in local currency:
  - Base ticket price is 100 GBP.
  - From the Exchange Rates table, derive a currency code by taking the part of its `Currency` value before the `-` (e.g., `CAD-GBP` → `CAD`).
  - Treat the provided `Rate` as: **1 GBP = Rate units of the local currency**.
  - For each attendee, compute `Ticket Price Local` as `int(100 * rate_for_currency)`.
    - If the attendee currency is GBP, set `Ticket Price Local` to 100.
    - If a rate is missing for a non-GBP currency, use a rate of 1.
  - The `int(...)` conversion must be applied to the computed value (i.e., produce an integer ticket price).
- Sort and label attendees for account-manager grouping:
  - Compute each Account Manager’s client count as the number of attendee rows associated with that Account Manager (excluding missing Account Manager values).
  - Sort attendee rows by:
    1) Account Manager client count (descending),
    2) Account Manager name (ascending),
    with missing Account Manager values ordered last.
  - Create an `Order` field that ranks Account Managers from 1..N, where 1 is assigned to the Account Manager with the most clients. Break ties by Account Manager name ascending. Attendees with no Account Manager should have a missing `Order`.
- Calculate money gain/loss per attendee and aggregate by country and currency:
  - Define attendee-level `Money Gain/Loss` using `Ticket Price Local` and `Refund Type`:
    - `Full Refund` → `-Ticket Price Local`
    - `Credit Note` → `+Ticket Price Local`
    - `No Refund` → `+Ticket Price Local`
    - Any other or missing refund type → 0
  - Aggregate to country-currency level by summing `Money Gain/Loss` grouped by `Country` and `Currency`.
  - Sort the aggregated output by:
    1) `Money Gain/Loss` (descending),
    2) `Currency` (ascending),
    3) `Country` (ascending).
- Output the data files exactly as specified below, with the stated column names and column order.

## Output

- output_01.csv
  - 10 fields:
    - Order
    - Ticket Price Local
    - First Name
    - Last Name
    - Email
    - Company Name
    - Country
    - Currency
    - Refund Type
    - Account Manager

- output_02.csv
  - 3 fields:
    - Money Gain/Loss
    - Currency
    - Country