## Context
Have you ever been working with a dataset in Tableau Desktop and noticed some duplication occurring? Of course, this is something you can fix with some potentially tricky LODs or Table Calc filters, but wouldn't it be nicer for your dataset to be viz ready before heading into Desktop?
If you attended the Tableau Fringe Festival last year, this concept may feel familiar, as I did a quick demo explaining why I, personally, would prefer to use Prep to solve my duplication issues. You can find the video here if you like.
The dataset we'll be working with for this challenge follows the same theme as the Fringe Festival. We have information relating to which of our Clients are attending our training sessions. Also included in our dataset is which Account Managers look after which Clients. However, we have historical information about Account Ownership which is leading to duplication. So how can we fix it?

## Requirements

- Input the data
- For each Client, work out who the most recent Account Manager is
- Filter the data so that only the most recent Account Manager remains
  - Be careful not to lose any attendees from the training sessions!
- In some instances, the Client ID has changed along with the Account Manager. Ensure only the most recent Client ID remains
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - Training
    - Contact Email
    - Contact Name
    - Client
    - Client ID
    - Account Manager
    - From Date
  - Training and Contact Email must be output exactly as in the input (case, spacing, and punctuation preserved).
  - From Date must be output as exact text.
  - From Date must use DD/MM/YYYY format (preserve day/month/year with leading zeros).
