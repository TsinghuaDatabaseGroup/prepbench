## Context

Dreamforce week highlights a common Tableau Desktop capability: standard Salesforce connections that expose a familiar, analysis-ready schema. The goal is to recreate a subset of that standard connection behavior in Tableau Prep-style logic by combining Salesforce-style Opportunity, Account, and User entities so that key “Created By” and “Owned By” user names are available alongside core Opportunity and Account attributes. Using the integrated dataset, produce separate outputs that directly answer three business questions about highest total amounts and account-level opportunity volume.

## Requirements

- Input the data.
  - Use three input files:
    - `input_01.csv` as the Opportunity dataset.
    - `input_02.csv` as the User dataset (used to map user IDs to user names).
    - `input_03.csv` as the Account dataset.

- Build a base, analysis-ready Opportunity–Account dataset (this will be the row-level dataset for `output_01.csv`).
  - Opportunity projection and renaming:
    - Keep only these Opportunity fields: `Id`, `Name`, `StageName`, `Amount`, `AccountId`, `OwnerId`, `CreatedById`.
    - Rename:
      - `Id` → `Opportunity ID`
      - `Name` → `Opportunity Name`
  - User name mapping:
    - From the User dataset, build an ID-to-name mapping using `Id` → `Name`.
    - For each Opportunity row, derive:
      - `Created By Name` = User `Name` matched from Opportunity `CreatedById`
      - `Owner Name` = User `Name` matched from Opportunity `OwnerId`
    - These are lookups/joins on user ID; if there is no match, the derived name fields must remain null.
  - Account projection, renaming, and user name mapping:
    - Keep only these Account fields: `Id`, `Name`, `Type`, `OwnerId`, `CreatedById`.
    - Rename:
      - `Id` → `Account Id`
      - `Name` → `Account Name`
      - `Type` → `Account Type`
      - `OwnerId` → `Account OwnerId`
      - `CreatedById` → `Account CreatedById`
    - Derive:
      - `Account Owner Name` = User `Name` matched from `Account OwnerId`
      - `Account Created By Name` = User `Name` matched from `Account CreatedById`
    - If there is no user match, these derived name fields must remain null.
  - Opportunity-to-Account linkage:
    - Left-join Opportunities to Accounts using Opportunity `AccountId` = Account `Account Id`.
    - Keep all Opportunity rows even if there is no matching Account; Account-related fields should be null when unmatched.
    - From Account, bring in: `Account Name`, `Account Type`, `Account Owner Name`, `Account Created By Name`.
    - Do not retain the auxiliary join key field `Account Id` in the final base dataset; keep the original Opportunity `AccountId`.
  - Final base dataset content and grain:
    - Grain: one row per Opportunity record.
    - Select and output exactly the 13 fields listed for `output_01.csv`, using the specified names.

- Create datasets which will easily answer some questions:
  - Who is the Opportunity Owner with the Highest Amount?
    - Aggregate the base dataset by `Owner Name`.
    - Compute `Amount` as the sum of Opportunity `Amount` within each owner group.
    - Include groups where `Owner Name` is null (i.e., treat null as its own group rather than dropping it).
    - Sort results by:
      1) `Amount` descending
      2) `Owner Name` ascending (as a deterministic tie-breaker)
    - Output this as `output_02.csv` with exactly the fields listed.
  - Who is the Account Owner with the Highest Amount?
    - Aggregate the base dataset by `Account Owner Name`.
    - Compute `Amount` as the sum of Opportunity `Amount` within each account-owner group.
    - Include groups where `Account Owner Name` is null.
    - Sort results by:
      1) `Amount` descending
      2) `Account Owner Name` ascending (as a deterministic tie-breaker)
    - Output this as `output_03.csv` with exactly the fields listed.
  - Which Account has the most Opportunities & Amount?
    - Aggregate the base dataset by `Account Name`.
    - Compute:
      - `Number of Opportunities` = count of distinct `Opportunity ID` within each account group
      - `Amount` = sum of Opportunity `Amount` within each account group
    - Include groups where `Account Name` is null.
    - Sort results by:
      1) `Amount` descending
      2) `Account Name` ascending (as a deterministic tie-breaker)
    - Output this as `output_04.csv` with exactly the fields listed.

- Create an output for each question.
- Output the data.

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