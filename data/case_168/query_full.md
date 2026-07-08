## Context
You are preparing a single session-level dataset by combining a detailed streaming-sessions file with an average pricing reference table that is maintained at a higher level of aggregation. The aim is to make all intermediate logic explicit: standardise key fields, aggregate sessions to the correct grain, classify each session into a consistent `content_type`, determine the correct “first active month” used for pricing, and then attach the corresponding average price.

## Requirements
- Input the data from the two provided CSV files:
  - The streaming sessions dataset (`input_02.csv`), which includes at minimum: `userID`, a datetime field `t`, `location`, `content_type`, and `duration`.
  - The average pricing dataset (`input_01.csv`), which includes at minimum: `Month`, `Content_Type`, and `Avg_Price`.

- Check the `location` field for spelling errors and correct them as follows:
  - Replace `Edinurgh` with `Edinburgh`.

- Fix the date field in the sessions data so it is recognised as a date/datetime type:
  - Parse the sessions field `t` as a datetime (ISO 8601).
  - Later, format the final output `timestamp` as `DD/MM/YYYY HH:MM:SS`.

- Aggregate the sessions data to find the total duration of each streaming session (as identified by the timestamp), using this exact output grain:
  - One output row represents a unique `(userID, timestamp, location)` session.
  - For each `(userID, timestamp, location)` group:
    - `duration` must be the sum of `duration` within the group.
    - Carry forward the group’s original `content_type` value for use in the subsequent reclassification step. If multiple different `content_type` values are present within the same group, take the first value encountered in the original data order (i.e., preserve the value from the first row of the group as it appears in the input file).

- Update the `content_type` field using these rules (applied after the aggregation above):
  - For `location` in **London**, **Cardiff**, or **Edinburgh**, set `content_type` to `"Primary"` (regardless of its prior value).
  - For all other locations:
    - Preserve `"Preserved"` as `"Preserved"`.
    - Set all other cases (including blank/missing or any value other than `"Preserved"`) to `"Secondary"`.

- Determine the “first active month” that will be used to join to the Avg Pricing Table:
  - **Important**: This step must be performed **after** the `content_type` update step above, using the updated `content_type` values.
  - Derive each row’s streaming month from `timestamp` at month granularity, and represent months in the format `MM YYYY`.
  - Apply different “minimum month” logic depending on the updated `content_type`:
    - For `"Primary"` content: for each `userID`, compute the overall minimum streaming month across that user’s `"Primary"` rows (using the updated `content_type` values), **ignoring location**, and use this same minimum month for all of that user’s `"Primary"` rows.
    - For all other content types (i.e., not `"Primary"`): compute the minimum streaming month separately for each `(userID, location, content_type)` combination (using the updated `content_type` values), and use that minimum month for rows in the same combination.

- Join to the Avg Pricing Table:
  - Use a left join from the session-level dataset to the pricing table.
  - Match the derived minimum month (`MM YYYY`) to `Month`, and match the session `content_type` to `Content_Type`.
  - Bring in `Avg_Price` from the pricing table.
  - **Note**: Since the pricing table only contains `Content_Type` values of `"Primary"` and `"Secondary"` (and does not contain `"Preserved"`), rows with `content_type` = `"Preserved"` will have `NULL` values for `Avg_Price` after the join.

- For `"Preserved"` content, override the joined value and manually set `Avg_Price` to **£14.98**:
  - After performing the join above, for all rows where `content_type` = `"Preserved"`, set `Avg_Price` to **£14.98** regardless of whether the join returned a value or `NULL`.

- Finalise the output:
  - Keep only the required fields.
  - Ensure `timestamp` is output as `DD/MM/YYYY HH:MM:SS`.
  - Sort the final output rows by `userID`, then `timestamp`, then `location`, then `content_type` (all ascending) to produce a deterministic file.

- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - userID
    - timestamp
    - location
    - content_type
    - duration
    - Avg_Price