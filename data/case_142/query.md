## Requirements

- Input the data
- From the *Business Unit A* Input, create a Date Lodged field
- Use the lookup table to update the risk rating
- Bring Business Unit A & B together
- We want to classify each case in relation to the beginning of the quarter (01/10/21):
  - Opening cases = if the case was lodged before the beginning of the quarter
  - New cases = if the case was lodged after the beginning of the quarter
- In order to count cases closed/deferred within the quarter, we want to call out cases with a completed or deferred status
- For each rating, we then want to count how many cases are within the above 4 classifications
- We then want to create a field for Cases which will carry over into the next quarter
  - i.e. Opening Cases + New Cases - Completed Cases - Deferred Cases
- Reshape the data to match the final output
- Output the data

## Output

- output_01.csv
  - 3 fields:
    - Status
    - Cases
    - Rating
