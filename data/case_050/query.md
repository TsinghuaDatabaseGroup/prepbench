## Context
Duplicates, duplicates, duplicates. In large datasets they are very difficult to identify and remove. They may occur due to data errors, data load issues or simply poor process design. Well the latter has struck at Chin & Beard Suds Co.
When surveying our customers' opinions, we didn't take in to account that some customers would share their opinions multiple times. To get an accurate representation of our customers' opinions and form different versions of the firm's Net Promoter Score (NPS) to allow us to analyse:
- A customer's first impression NPS score
- The customer's most up-to-date NPS score
To do this, we need you to clean and de-duplicate the data. The aim of the output is to be flexible to answer questions on NPS scores at not just the First or Latest but at the Country or Store Level too. Don't worry, we can leave those calculations for our analysts - they just need clean data to work with.

## Requirements

- Input the data
- Change the Question Number for the question asked
- Clean the Country and Store names
  - We only want English names for places
- Clean up the dates and times to create a 'Completion Date' as a Date Time field
- Understand the age of the customer based on their Date of Birth (DoB)
  - Nulls are ok
  - Their age is taken to the date of 22nd January 2020
- Find the first answer for each customer in each store and country
- Find the latest answer for each customer in each store and country (if there are multiple responses)
- Remove any answers that are not a customer's first or latest
- Classify the 'NPS Recommendation' question based on the standard logic:
  - 0-6 makes the customer a 'Detractor'
  - 7-8 makes the customer a 'Passive'
  - 9-10 makes the customer a 'Promoter'
- Output the data

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
