## Context
The objective is to identify which seats on each plane were not selected (i.e., not booked) by any customer. The inputs include multiple seat-booking extracts (provided as separate files) and a complete seating plan that enumerates every seat available on the plane. The result should list only those seats that exist in the seating plan but do not appear in any booking record.

## Requirements
- Input the data.
  - Read the seat bookings from `input_01.csv`, `input_02.csv`, and `input_03.csv`.
  - Read the full seating plan from `input_04.csv`.
- From each bookings input, retain only the fields needed to identify a seat: `Class`, `Seat`, and `Row`.
- Union the bookings datasets together into a single combined bookings table (stack rows across the three inputs).
- Treat a seat as “booked” if it appears at least once in the combined bookings data; therefore, reduce the combined bookings table to distinct seat keys defined by (`Class`, `Seat`, `Row`).
- Use the seating plan as the complete set of possible seats, and compare it to the distinct booked seat keys to identify unbooked seats:
  - Perform an anti-join / left-exclusion using the key (`Class`, `Seat`, `Row`) to return seats that are present in the seating plan but absent from the booked seat keys.
  - Only return records for seats that have not been booked.
- For deterministic output, sort the resulting unbooked seats by `Class` (ascending), then `Seat` (ascending), then `Row` (ascending).
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Class
    - Seat
    - Row