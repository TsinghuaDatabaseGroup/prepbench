## Context

You are given customer satisfaction survey data containing ratings for two platforms—Mobile App and Online Interface—across multiple question areas. The goal is to compare each customer’s average rating between the two platforms, classify their platform preference based on that difference, and report what percentage of all customers fall into each preference category.

## Requirements

- Input the data from `input_01.csv`, where each row represents a single customer and the columns include ratings for both platforms.
- Use only the four non-overall question ratings for each platform (exclude any “Overall Rating” fields, as they are not to be used in calculations).
  - Mobile App questions to include:
    - Mobile App - Ease of Use
    - Mobile App - Ease of Access
    - Mobile App - Navigation
    - Mobile App - Likelihood to Recommend
  - Online Interface questions to include:
    - Online Interface - Ease of Use
    - Online Interface - Ease of Access
    - Online Interface - Navigation
    - Online Interface - Likelihood to Recommend
- Treat the platform prefix (e.g., “Mobile App - ”, “Online Interface - ”) as part of the column identification only; comparisons should be made by aligning the same underlying question areas across platforms (Ease of Use, Ease of Access, Navigation, Likelihood to Recommend).
- For each customer, calculate:
  - The average Mobile App rating as the mean of the four included Mobile App question ratings.
  - The average Online Interface rating as the mean of the four included Online Interface question ratings.
  - The difference as:  
    `Average Mobile App rating − Average Online Interface rating`
- Categorise each customer into exactly one of the following groups based on the difference:
  - **Mobile App Superfan** if the difference is **greater than or equal to 2** (Mobile App higher).
  - **Mobile App Fan** if the difference is **greater than or equal to 1** but **less than 2**.
  - **Online Interface Superfan** if the difference is **less than or equal to -2** (Online Interface higher).
  - **Online Interface Fan** if the difference is **less than or equal to -1** but **greater than -2**.
  - **Neutral** if the difference is **strictly between -1 and 1**.
- Aggregate customers by preference category and compute the **Percent of Total** customers in each category as:  
  `(count in category / total customers) * 100`, rounded to **1 decimal place**.
- Output exactly one row per preference category, ordered as:
  1) Mobile App Fan  
  2) Neutral  
  3) Mobile App Superfan  
  4) Online Interface Fan  
  5) Online Interface Superfan
- Output the data.

## Output

- output_01.csv
  - 2 fields:
    - Preference
    - % of Total