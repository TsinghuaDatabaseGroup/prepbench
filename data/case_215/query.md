## Context
The challenge this week is heavily inspired by a real life scenario and I'm sure many organisations will be able to relate to the quirky rules they have to follow when doing regulatory reporting. Often with the reasoning behind it being "because that's the way it's always been done!" Data Source Bank must assign new customers to the next working day, even if they join at the weekend, or online on a public holiday. What's more, they need to report their total new customers for the month on the last working day of the month. This means any customers joining on that last working day will actually be counted in the following month. For example, 31st December 2021 was a Friday. The total number of customers for December would be reported on this day. Any customers joining on the day of 31st December 2021 itself will be counted in January's count of new customers. What makes this even more confusing is trying to align with branches in Ireland. Ireland will of course have different Bank Holidays and so the definition of a working day becomes harder to define. For DSB, the UK reporting day supersedes the ROI reporting day. If the UK has a bank holiday where ROI does not, these customers will be reported on the next working day in the UK. If ROI has a bank holiday where the UK does not, the customer count will be 0 for ROI, but it will still be treated as a working day when assigning the reporting month start/end.

## Requirements

- Input the data
- Fill down the years and create a date field for the UK bank holidays
- Combine with the UK New Customer dataset
- Create a Reporting Day flag
  - UK bank holidays are not reporting days
  - Weekends are not reporting days
- For non-reporting days, assign the customers to the next reporting day
- Calculate the reporting month, as per the definition above
- Filter out January 2024 dates
- Calculate the reporting day, defined as the order of days in the reporting month
  - You'll notice reporting months often have different numbers of days!
- Now let's focus on ROI data. This has already been through a similar process to the above, but using the ROI bank holidays. We'll have to align it with the UK reporting schedule
- Rename fields so it's clear which fields are ROI and which are UK
- Combine with UK data
- For days which do not align, find the next UK reporting day and assign new customers to that day (for more detail, refer to the above description of the challenge)
- Make sure null customer values are replaced with 0's
- Create a flag to find which dates have differing reporting months when using the ROI/UK systems
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - Misalignment Flag
    - Reporting Month
    - Reporting Day
    - Reporting Date
    - New Customers
    - ROI New Customers
    - ROI Reporting Month
