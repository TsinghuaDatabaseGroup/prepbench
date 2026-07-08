## Context
Being an airline, Prep Air has to work closely with airports to ensure its passengers get the best experience possible. One airport in particular has been accused of driving passengers crazy by changing the gate allocations of flights multiple times before boarding occurs. Prep Air has discovered that this is due to the airport using a random number generator to assign gates for flights and manually correcting the errors in real time. Prep Air have been given the opportunity to demonstrate that they have a better way of allocating gates for the airport's busiest time of day. Whilst the stand numbers will still be set by the airport, we can at least ensure the corresponding gates are allocated in a more logical way. The diagram below should help illustrate which stands can be accessed by which gates. The remote stands (10-12) can be accessed by any gate via a bus. However, passengers don't enjoy the bus rides, so we should try to minimise the time that they have to spend on the buses!

## Requirements
- Input the data
- In the Stands dataset, split out the gates which can access each stand and reshape
- Bring in details for how long it will take to reach stands 10-12
- In the Stand Allocations dataset, create a date time field for when boarding begins
- The gate is needed for 45 mins for each flight i.e. a flight which is boarding at 6am will need the gate up to (but not including) 6.45am
- The gates should be assigned following this process:
  - If there are any flights that are only accessible from 1 gate, these should be assigned first
  - Flights at remote stands should be assigned next, to minimise bus transport times for passengers
  - Remaining flights should assigned to gates with the highest transport times to remote stands, so that if additional flights come in, the gates with lower transport times would be available
  - For any ties that we encounter, lower flight numbers should have priority as these are more important flights for Prep Air
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Gate
    - Stand
    - Date
    - Flight
    - Requires Bus?
    - Time to Reach Stand
