## Context
A few weeks back we mentioned that we were cleaning up our mailing lists. Well, now our marketing department is looking to generate further revenue and believes a great way of doing that is rewarding our highest spending customers by emailing them “15 per***scent*** discount” codes! They’ve decided the optimal cut-off for who receives these codes is the top 8% of customers by total sales from orders placed within the last 6 months. The data contains sales for the last 12 months (as of 24/05/2019). From this they want a list of all the email addresses for the top 8% of customers (by total sales over the last 6 months) along with their rank and the total sales value.

## Requirements

- Input the data
- Download the "Data for Processing" folder containing all the input files.
- Find a way to import & combine all the data from the file without deleting the non-sales data that was accidentally sent to you. The rest of the detail in the file names isn’t important.
- Find a way to rank the customers by total sales across orders placed within the last 6 months.
  - **NB:** *For this challenge, calculate "last 6 months" from 24/05/2019, not today's date.*
- Find a way to filter these down to customers in the top 8%.
- Produce a neatly formatted output matching the structure shown and described below.
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Last 6 Months Rank
    - Email
    - Order Total
