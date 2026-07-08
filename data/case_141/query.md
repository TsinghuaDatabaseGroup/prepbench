## Context
This week we are going to use one of the newer features in Tableau Prep, New Rows. New Rows was released in Prep Builder version 2021.3 so you will need that version or later of Prep for this challenge (unless you want to scaffold your data yourself). To date, Tableau Prep has assessed each row of data separately but we all know data can often be incomplete and that made for some tough challenges. With the New Rows step within Prep Builder this should make working with incomplete data sets much easier (and in some cases possible where it wasn't before). Allchains Bike Stores have been fund raising in one of their stores. Customers are given the option of donating to charity when they buy a new bike. Sadly, the team haven't been recording the data accurately and the donations only get totalled up at sporadic points throughout the month. We need to understand roughly how much is being raised each day. Also, are our customers more generous on a certain day of the week?

## Requirements

- Input the data
- Create new rows for any date missing between the first and last date in the data set provided
- Calculate how many days of fundraising there has been by the date in each row (1st Jan would be 0)
- Calculate the amount raised per day of fundraising for each row
- Workout the weekday for each date
- Average the amount raised per day of fundraising for each weekday
- Output the data

## Output

- output_01.csv
  - 5 fields:
    - Avg raised per weekday
    - Value raised per day
    - Days into fund raising
    - Date
    - Total Raised to date
