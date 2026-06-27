## Context
This week we return to our Bike store to look at the painting process within the factory. Engineers are provided with indicator values as the process progresses. Data is only provided when a value changes, so assume the process value remains the same as the previous value until it is updated later in the process. Our goal here is to clean and structure the data into a tidy, long-form table that captures each update with its associated parameter and target/actual values.

## Requirements

- Input the data
- Create a Datetime field
- Parse the Bike Type and Batch Status for each batch
- Split out the value field into two fields: Target and Actual
- Keep one record per update per parameter (long format), preserving the stage where the update occurred
- Ensure the Data Parameter is one of: Current, Voltage, Gas Flow, Temperature, Pressure
- Output the cleaned data

## Output

- output_01.csv
  - 8 fields:
    - Batch No.
    - Name of Process Step
    - Bike Type
    - Batch Status
    - Datetime
    - Data Parameter
    - Target
    - Actual
