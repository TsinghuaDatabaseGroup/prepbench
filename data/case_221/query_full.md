## Context

You are preparing conference session data to identify the speaker your boss is looking for. The only hint is that the person is presenting a talk about data deduplication on the 2nd floor. The work is split into three levels (Beginner, Intermediate, Advanced), where each level’s output is used as an input to the next level.

## Requirements

### Beginner Level

- Input the data from `input_01.csv`.
- Split out the `Description` field into:
  - **Speaker Name**: the text before the first colon (`:`).
  - **Presentation Description**: the text after the first colon (`:`). (This does not need to be kept in the final output; it is used to derive other fields.)
- Create the initials for each speaker and use these initials as the `Speaker` value in the output.
  - Initials rule: split the speaker name into name parts (treat hyphens as word separators) and concatenate the first letter of each part in uppercase.
- Categorize each presentation into a `Subject` using the first matching keyword found in the `Description` (case-insensitive), checking in this priority order:
  1) Prep  
  2) Server  
  3) Community  
  4) Desktop
- Create a Boolean `Deduplication Flag` that is **True** if `Description` contains any of the following substrings (case-insensitive): `dedup`, `de-dup`, or `de dup`. Otherwise set it to **False**.
- Filter to only talks that mention deduplication (`Deduplication Flag` = True).
- Remove unnecessary fields so that only the required output fields remain.
- Output the result to `output_01.csv`.
- Ensure a deterministic row order by sorting by `Session Number` (ascending) then `Speaker` (ascending).

### Intermediate Level

- Input the data from `input_03.csv`.
- Pivot/reshape the schedule so that each record represents a single session assignment, with these fields available at minimum:
  - `Room`
  - `Floor` (derived from the original floor column headers)
  - `Session Detail` (the session text value from the original cells)
- Filter to:
  - `Floor` = `Floor 2`
  - `Session Detail` is not null
- Split out `Session Detail` to derive:
  - `Speaker` initials: the text after the first hyphen (`-`) and before the delimiter ` on `.
  - `Subject`: the text after the delimiter ` on `.
- Create a room number that also gives detail of the floor number:
  - Convert `Room` to a number and compute `Room` for Floor 2 as `200 + Room`. (This produces values like 202 for Room 2 on Floor 2.)
- Join this Floor 2 session table to `output_01.csv` using an inner join on:
  - Speaker initials (from `output_01.csv` `Speaker`) to the parsed speaker initials from `Session Detail`
  - `Subject`
- After the join, keep only sessions on the 2nd floor (the earlier Floor 2 filter should already enforce this).
- Remove unnecessary fields so that only the required output fields remain.
- Output the result to `output_02.csv` and ensure it contains 1 row.
- Ensure a deterministic row order by sorting by `Speaker` (ascending) then `Subject` (ascending).

### Advanced Level

- Input the data from `input_02.csv`, which represents room-to-room distances as a matrix.
- Reshape the distance matrix so that each record represents a directed room pair with:
  - `Room A` (row room identifier)
  - `Room B` (column room identifier)
  - `Metres` (distance)
- Exclude null rows by removing any records where `Room A`, `Room B`, or `Metres` is null.
- Exclude values between the same room by removing records where `Room A` = `Room B`.
- Join to `output_02.csv` to obtain the target room (the room where the deduplication talk is happening).
- You’re currently in Room 302. Select the single distance record representing travel between Room 302 and the target room:
  - Use the record where (`Room A` = 302 and `Room B` = target room); if only the reverse direction exists, use that distance but report the output with `Room A` = 302 and `Room B` = target room.
- Assume a walking speed of 1.2 m/s. Compute `Minutes to the next room` as:
  - `ceil( Metres / 1.2 / 60 )`
  - Round up to the nearest whole minute (ceiling).
- Remove unnecessary fields so that only the required output fields remain.
- Output the result to `output_03.csv` and ensure it contains 1 row.

## Output

- output_01.csv
  - 4 fields:
    - Subject
    - Speaker
    - Session Number
    - Deduplication Flag

- output_02.csv
  - 4 fields:
    - Speaker
    - Subject
    - Session Number
    - Room

- output_03.csv
  - 6 fields:
    - Room A
    - Room B
    - Minutes to the next room
    - Metres
    - Speaker
    - Subject