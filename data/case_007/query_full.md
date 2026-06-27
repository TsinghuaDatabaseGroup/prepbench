## Context
A shipping distribution company operates departures using multiple boat types and sells cargo space on each departure based on weight and volume. Departure-level capacity is recorded in a “Departure Details” table, while each customer allocation of space is recorded in an “Allocation Details” table. The company needs an automated way to identify departures where the total allocated cargo exceeds the boat’s maximum weight and/or maximum volume so these issues can be flagged before departure day.

## Requirements
- Input the data.
- Download the input file(s).
- Use `input_01.csv` as the Departure Details table (this table defines the set of departures to report on and contains each departure’s maximum allowable weight and volume).
- Use `input_02.csv` as the Allocation Details table (this table contains individual allocation records, including allocated weight and allocated volume).
- Compute total allocated weight and volume per departure as follows:
  - In Allocation Details, derive `Ship ID` and `Departure Date` from the `Departure ID` field, where `Departure ID` is formatted as `<Ship ID>-DD-MM-YYYY`.
    - `Ship ID` is the portion before the final hyphen and date segment.
    - `Departure Date` must be converted to an ISO-style text key `YYYY-MM-DD` for matching purposes.
  - Group Allocation Details by (`Ship ID`, `Departure Date`) and sum:
    - `Weight Allocated`
    - `Volume Allocated`
- Combine allocation totals onto Departure Details:
  - Left join the aggregated allocation totals to Departure Details on (`Ship ID`, `Departure Date`) so that every departure in Departure Details appears in the result even if it has no allocations.
  - For departures with no matching allocations, set `Weight Allocated` and `Volume Allocated` to 0 (as integers).
  - Preserve the original row order from the Departure Details input in the final output.
- Flag capacity breaches for each departure:
  - `Max Weight Exceeded?` is `True` when `Weight Allocated` > `Max Weight`, otherwise `False`.
  - `Max Volume Exceeded?` is `True` when `Volume Allocated` > `Max Volume`, otherwise `False`.
- Format `Departure Date` in the final output as `DD/MM/YYYY` text.
- Output the data.

## Output

- output_01.csv
  - 8 fields:
    - Ship ID
    - Departure Date
    - Max Weight
    - Max Volume
    - Weight Allocated
    - Volume Allocated
    - Max Weight Exceeded?
    - Max Volume Exceeded?