## Context

You are preparing a timesheet-style dataset that records hours worked by employees across projects and dates. The goal is to reshape the data into an analysis-ready form, compute per-person average hours worked per day, compute each person’s share of hours spent by area of work, and then produce a final table restricted to the “Client” area of work.

## Requirements

- Input the data.
- Treat the input as a wide table where:
  - The first column contains combined employee information (including at least the employee name and “Area of Work”).
  - The second column is the Project field.
  - All remaining date columns represent work dates and must be pivoted into a single Date column.
- Remove any rows that contained a total in the Project field by excluding rows where the Project value starts with `Overall Total for `.
- Transform the structure of the table so that all date columns are moved into a single `Date` column with a corresponding `Hours` value column (i.e., pivot/melt columns-to-rows for all date fields).
  - **Ambiguity resolution**: When pivoting, ignore any date columns that have empty or missing column names. Only pivot columns that have valid date values as their headers.
  - **Ambiguity resolution**: During the pivot operation, if a cell in a date column is empty or contains only whitespace, treat that cell's value as an empty string or null. These empty values will be handled during aggregation (see below).
- Split the combined "Name, Age, Area of Work" field into separate fields and derive at least:
  - `Name`
  - `Area of Work`
  (Age does not need to be retained for the final output.)
  - **Ambiguity resolution**: The field format is "Name, Age: Area of Work" where the comma and space (`, `) separate Name from Age, and the colon and space (`: `) separate Age from Area of Work. Extract `Name` as the part before the first `, `, and `Area of Work` as the part after the first `: `.
- Exclude records where `Hours` is `Annual Leave`. Then convert `Hours` to a decimal (numeric) value and drop rows where `Hours` cannot be parsed as a number.
  - **Ambiguity resolution**: After pivoting, if the `Hours` column contains the exact string "Annual Leave" (case-sensitive), exclude that entire record. This means that if a date column originally contained "Annual Leave" as its value, after pivoting it becomes a row where `Hours = "Annual Leave"`, and such rows should be removed before numeric conversion.
- Calculate daily total hours per employee by aggregating to one row per `Name` and `Date` (summing `Hours` across all projects and areas for that person on that date).
  - **Ambiguity resolution**: When summing `Hours`, treat empty strings, null values, or missing values as 0 (zero hours worked). Only numeric values and the string "0" should contribute to the sum.
- From this daily table, calculate for each person:
  - The total number of distinct days worked (`DaysWorked`), defined as the count of dates where daily hours are greater than zero.
  - The total number of hours worked across all days.
  - The average number of hours worked per day as:  
    `Avg Number of Hours worked per day = TotalHours_All / DaysWorked`.
- Starting from the long table with `Name`, `Area of Work`, `Date`, and numeric `Hours`:
  - Remove rows where `Area of Work` is `Chats` (case-insensitive comparison on the trimmed `Area of Work` value).
  - Calculate the total hours per person and area (excluding `Chats`) by aggregating `Hours` grouped by `Name` and `Area of Work`.
  - In a separate aggregation, calculate the total hours per person across all (non-`Chats`) areas, grouped by `Name` only.
  - Join these results so that for each `Name` and `Area of Work` you also have the total non-`Chats` hours for that person.
  - For each `Name` and `Area of Work`, calculate the percentage of total hours as:  
    `(% of Total) = ROUND((AreaHours / TotalHours_NonChats) * 100)`  
    (round to the nearest integer percentage).
  - **Ambiguity resolution**: Format the `% of Total` field as an integer followed by the `%` symbol (e.g., `75%`, `87%`), not as a decimal number.
- Restrict the table to only those rows where `Area of Work` equals `Client` (case-insensitive comparison on the trimmed value).
- Join this `Client`-only table with the per-person averages table so that, for each person whose `Area of Work` is `Client`, you have:
  - `Name`
  - `Area of Work`
  - `% of Total`
  - `Avg Number of Hours worked per day`.
- Ensure that `Avg Number of Hours worked per day` is stored as a numeric field and is rounded to a suitable precision (e.g., 9 decimal places).
- Sort the final table by `Avg Number of Hours worked per day` ascending, and then by `Name` ascending.
- Output the final data to `output_01.csv` with exactly the following fields:
  - `Name`
  - `Area of Work`
  - `% of Total`
  - `Avg Number of Hours worked per day`.