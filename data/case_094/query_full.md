## Context
Prep Air wants to propose a deterministic, passenger-friendly way to allocate airport gates during the busiest time of day. Each flight is assigned to a stand by the airport; Prep Air’s task is to assign an appropriate gate that can access that stand while minimizing passenger bus usage where possible. Some stands require passengers to travel by bus (remote stands), and different gates have different travel times to reach those remote stands; bus time should be minimized for flights that require it.

## Requirements
- Input the data.
  - Use the Stands dataset to determine which gates can access each stand and whether the stand requires a bus.
  - Use the Remote Stands travel-time dataset to obtain, for each gate, the time to reach remote stands.
  - Use the Stand Allocations dataset to obtain each flight’s stand assignment and boarding start time.
  - Use the Gate Availability dataset to obtain the set of discrete time slots when each gate is available to be booked.
- In the Stands dataset, split out the gates which can access each stand and reshape.
  - Create a long-form mapping at the grain of (Stand, Gate) with a boolean “Requires Bus?” flag for the stand.
  - Stand identifiers and Gate identifiers should be interpreted as integers; if the source values include a leading letter (e.g., “S” for stands or “G” for gates), remove that prefix when converting to integers.
- Bring in details for how long it will take to reach stands 10-12.
  - Build a lookup mapping each Gate (as an integer) to its “Time to Reach Remote Stands” (as an integer).
- In the Stand Allocations dataset, create a date time field for when boarding begins.
  - Interpret the provided “Time” as HHMM on the date 2020-02-01 (zero-pad to 4 digits if needed), yielding a timestamp for the boarding start.
- The gate is needed for 45 mins for each flight i.e. a flight which is boarding at 6am will need the gate up to (but not including) 6.45am.
  - Model this as three consecutive 15-minute booking slots starting at the boarding start time: start + 0 minutes, +15 minutes, and +30 minutes. All three slots must be available at the chosen gate to assign the flight.
- Use the Gate Availability dataset as the source of truth for which (Gate, DateTime slot) combinations exist and can be booked.
  - A flight can only be assigned to a gate if all required booking slots exist for that gate in the availability data and are unassigned at the time of booking.
- The gates should be assigned following this process (deterministically), booking flights one-by-one in priority order:
  - First, assign any flights that are only accessible from 1 gate (based on the stand-to-gate mapping).
  - Next, assign flights at remote stands (stands where “Requires Bus?” is true) to minimise bus transport times for passengers.
  - Next, assign remaining flights to gates with the highest transport times to remote stands, so that if additional flights come in, the gates with lower transport times would be available.
  - Across all categories above, process flights in chronological order of boarding start time; for any ties at the same start time, lower flight numbers have priority.
- Within each flight category, choose the gate to attempt first as follows (then pick the first gate that has all required time slots available):
  - For flights accessible from only 1 gate: that single accessible gate.
  - For remote-stand flights: among the stand’s accessible gates, try gates in ascending order of “Time to Reach Remote Stands”; break ties by lower gate number.
  - For remaining flights: among the stand’s accessible gates, try gates in descending order of “Time to Reach Remote Stands”; break ties by lower gate number.
- When a flight is booked into a gate’s time slots:
  - Populate those time-slot rows with the flight’s Stand, Flight, and “Requires Bus?” as “Y” or “N”.
  - Populate “Time to Reach Stand” as the gate’s “Time to Reach Remote Stands” when “Requires Bus?” = “Y”; otherwise set it to 0.
- Output the data.
  - The output should be at the grain of one row per (Gate, available DateTime slot) from the availability input.
  - Include rows for time slots with no assigned flight; in those rows, Stand, Flight, Requires Bus?, and Time to Reach Stand should be blank/null.

## Output

- output_01.csv
  - 6 fields:
    - Gate
    - Stand
    - Date
    - Flight
    - Requires Bus?
    - Time to Reach Stand