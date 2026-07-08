## Context

Welcome to the Tableau Conference Special for Preppin' Data. If it's your first time here then a very warm welcome to you! This week we have something pretty special planned for you with a 3 part challenge. The output for each part will flow through to the next part, allowing you to build to answer the ultimate question: Who is the person your boss has tasked you with finding and where are they?! The only information your boss has given you is that they're presenting about data deduplication on the 2nd floor. The rest is up to you!

**Note**: This challenge has three difficulty levels (Beginner, Intermediate, Advanced). Each level builds on the previous one - Intermediate Level requires Output 1, and Advanced Level requires Output 2. You can complete them sequentially or challenge yourself with the level that matches your skill.

## Requirements

### Beginner Level

- Input the data
- Split out the Description field into Speaker Name and Presentation Description
- Create the initials for each speaker
  - e.g. Jenny Martin becomes JM
- Categorize the Presentations into the following Subject areas:
  - Prep
  - Server
  - Community
  - Desktop
- Create a Boolean (True/False) field for identifying talks that mention deduplication
- Filter to on talks that mention deduplication
- Remove unnecessary fields
- Output the data (output_01.csv)

### Intermediate Level

- Input the data
- Pivot the data so the Room and Floor number are on the same row
  - Filter out any unnecessary rows
  - Rename fields
- Create a room number that also gives detail of the floor number
  - e.g. Room 2 on Floor 1 will be Room 102
- Split out the Session Detail field into Session Name, Speaker and Subject
- Join with Output 1
- Filter to the session on the 2nd floor
- Remove unnecessary fields
- Output the data (output_02.csv with 1 row)

### Advanced Level

- Input the data
- Reshape the data so we have a column for Room A, a column for Room B and a column for the distance between them (in meters)
- Exclude null rows
- Exclude values between the same room
- Assume you have a walking speed of 1.2 m/s. How many minutes will it take you to travel between rooms?
  - Round up to the nearest whole minute to account for busy conference corridors
- Join to Output 2
- You're currently in Room 302, how long will it take you to reach them?
- Remove unnecessary fields
- Output the data (output_03.csv with 1 row)

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
