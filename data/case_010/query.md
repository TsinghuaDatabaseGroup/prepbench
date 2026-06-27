## Context
Following our complaints analysis last week, Chin & Beard Suds Co. (still our mythical organisation) is looking to manage its marketing mailing lists. Sadly, our customers are not just sporadically complaining, they are also choosing not to receive of marketing. We are continually releasing new scents in our products and we want to let our customers know.
Sadly for us, our website has an unsubscribe button that only let's people enter their First and Last Name. It does capture the date they want to unsubscribe so they can resubscribe at a later date. Our mailing list is a list of emails that are consistent enough that we can join these two data sets together, but not easily.
The business needs to understand not just who they can market too but also, how much revenue we are losing by our customers not showing interest in us. Luckily, we have the raw data to help us understand this but:
1. We want to have a nice list of emails that we CAN still market to (and include if they have unsubscribed and resubscribed as we might have to handle that)
2. We want a summarised dataset that lets us understand when customers unsubscribe, how much they have spent with us, do they resubscribe, what products are they interested in. Keep hold of Subscribed and Resubscribed Customers too for context in our analysis.

## Requirements

- Input the data
- The Liquid / Bar 1/0 indicators do not matter in the analysis
- Join the Mailing List to the Unsubscribe List to determine who can still receive our marketing messages
- Group the customers in to the following Status groups: Subscribed, Resubscribed and Unsubscribed.
- And, group the customers in to the following groups of their tenure on the mailing list: 0-3,3-6,6-12,12-24,24+ months
- Add in Customer Lifetime Value to understand our revenue from each customer
- Create two outputs as detailed in the numbered bullets above (Email list and Analysis of Unsubscribed Customers)
- Output the data

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
