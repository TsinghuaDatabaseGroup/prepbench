## Context

This week comes a special challenge because it is Dreamforce conference week. Wherever you are in the world you can participate in Dreamforce as they have a virtual and in person element in San Francisco. This challenge is about trying to replicate one of many of the Standard Salesforce connections that you can have in Tableau Desktop. Tableau have created these standard connections, for when you connect Salesforce, which allows you to create the most common data schemas available. If you are not aware of what Salesforce is, it is a CRM platform which allows you to track leads & opportunities, and I'm sure it does much more than that. We have different experiences when we connect to Salesforce via Tableau Prep and Desktop, which is why we want to be careful to recreate some of those standard connections within Prep, to allow us to join onto a variety different data sets for future use. Another difference when we are connecting to Tableau Prep over Desktop is that the data is always being pulled through live, meaning we can investigate our data connections without bringing them into Tableau Desktop to make sure we are using the right fields, which makes it easier for everyone else to know which field they need to use. Your final output should look something like this: Hint: In desktop, they have renamed some of the tables in the connection, again to make it easier to use, for example Created By & Owned By are using the User Table.

## Requirements

- Input the data
- Now we want to create datasets which will easily answer some questions:
  - Who is the Opportunity Owner with the Highest Amount?
  - Who is the Account Owner with the Highest Amount?
  - Which Account has the most Opportunities & Amount?
- Create an output for each question
- Output the data

## Output

- output_01.csv
  - 13 fields:
    - Opportunity Name
    - StageName
    - Amount
    - Created By Name
    - Owner Name
    - Account Name
    - Account Type
    - Account Owner Name
    - Account Created By Name
    - Opportunity ID
    - AccountId
    - OwnerId
    - CreatedById

- output_02.csv
  - 2 fields:
    - Owner Name
    - Amount

- output_03.csv
  - 2 fields:
    - Account Owner Name
    - Amount

- output_04.csv
  - 3 fields:
    - Account Name
    - Number of Opportunities
    - Amount
