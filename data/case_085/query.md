## Context

The premise, as explained in Jonathan's viz, is that you can order up to 5 drinks a day, every day, for £20 a month. Unfortunately, the Preppin' Data team have slightly more complex orders than the viz allows you to input. So we'll need to use Tableau Prep to see if the deal is worthwhile for everyone and how much they could save!

## Requirements

- Input the data
- Restructure the orders so we have a line per person per drink, with a count of how many times they order that drink in a week
  - Remember: extra shots or syrups will have their own prices so should be on a separate row in the data
- Restructure the price list so we have each item with its price on a separate line
- Join the ordered drinks to their prices
  - Beware ordered drinks not having the exact same name as on the menu
- Calculate the monthly spend for each Dr Prepper
  - For simplicity, we assume there are 4 weeks in a month and that the month starts on a Monday and ends on a Sunday
- Calculate the potential savings for each person and advise whether or not they should take advantage of the deal
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Person
    - Monthly Spend
    - Potential Savings
    - Worthwhile?
