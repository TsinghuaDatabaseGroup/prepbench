## Requirements

- Input the data
- Join the tables together and remove unnecessary fields
- Identify weeks where orders were placed for new stock: This occurs whenever the Quantity Available is 10 or less
- Calculate how much Stock was ordered in these weeks: SuperBytes policy indicates they should order as many items as they need so their stock level is back to 30 (e.g., if the Quantity Available is 5 then they would order 25 items)
- Calculate the Quantity Sold each week, taking into consideration the new stock that has been ordered
- Across the dataset calculate the Total Quantity that has been sold for each Product in each Store, as well as the Avg Quantity Sold per Week and Avg Order Frequency (i.e., if the Order Frequency is 2 then this would mean the Store is ordering once every 2 weeks on average)
- Round these values to 1 decimal place
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Store
    - Category
    - Product
    - Total Quantity Sold
    - Avg Quantity Sold per Week
    - Avg Order Frequency
