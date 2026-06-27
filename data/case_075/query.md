## Context
Each attendee paid the equivalent to £100 (GBP) for a ticket and they have a few options about how they can have their refund:
1. Full Refund - This is a full cash refund back to them.
2. Credit Note - We can create credit notes to be used next year.
3. No Refund - They can waive their refund and give us the money.
Each refund will be refunded in the currency of their selected country.
We have been given one Excel file with multiple tabs: Attendee List, Account Manager, Exchange Rates.

## Requirements

- Input the data
- Extract the company email from the email. For this task we will assume that it is the word straight after the @ symbol.
- Join the AM & Attendee tables together. Make sure you retain the case from the company field in the Account Manager table. (Eg, First letter capitalised for each company)
- Calculate the ticket price in the local currency
- Sort the data so that all the AM's clients are grouped together, and the AM with the most clients is first (the order of clients doesn't matter)
- Calculate how much money we will receive/lose from each country & local currency
- Output the data

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
