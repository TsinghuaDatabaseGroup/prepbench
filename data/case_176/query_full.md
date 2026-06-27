## Context

You are given two input datasets: a guest list (parties and their needs) and a room list (room capacities and features). The goal is to generate the set of valid guest-to-room pairings that satisfy capacity, bed preference, and accessibility constraints, then score each pairing by how well the room satisfies the party’s additional requests. Finally, keep only the best-scoring options per party and apply an additional rule to avoid assigning small parties to the largest-capacity rooms.

## Requirements

- Input the data from:
  - `input_01.csv` (guests/parties), using at least: `Party`, `Adults`, `Children`, `Double/Twin`, `Requires Accessible Room?`, `Additional Requests`
  - `input_02.csv` (rooms), using at least: `Room`, `Adults`, `Children`, `Features`

- Before bringing the 2 datasets together, determine how many Additional Requests each guest has made:
  - Update `Additional Requests` values of *N/A* to `null`.
  - Treat `null` (and blank) `Additional Requests` as “no requests”, i.e., a request count of `0`.
  - Otherwise, interpret `Additional Requests` as a comma-separated list of request tokens; the request count is the number of tokens in that list.
  - Keep the original `Additional Requests` text for output (after mapping *N/A* to `null`).

- Match the guests to the rooms which have capacity for their entire party:
  - Consider a guest-room pairing valid on capacity only if:
    - `Room Adults >= Party Adults`, and
    - `Room Children >= Party Children`.
  - This matching is conceptually a cross-join of guests to rooms followed by filtering to only the valid pairings.

- Filter so that double/twin bed preferences are adhered to:
  - A pairing is valid only if the guest’s `Double/Twin` preference is present as a feature token in the room’s `Features`.

- Ensure guests who have accessibility requirements are only matched with accessible rooms:
  - If `Requires Accessible Room?` is false, accessibility does not constrain the match.
  - If `Requires Accessible Room?` is true, the room’s `Features` must include the token `Accessible`.

- Calculate the Request Satisfaction % for each remaining guest-room pairing:
  - Only the following request tokens contribute to satisfaction:
    - `Bath` is satisfied if the room features include `Bath`.
    - `High Floor` is satisfied if the room features include `High Floor`.
    - `Near to lift` is satisfied if the room features include `Near to lift`.
    - `NOT Near to lift` is satisfied if the room features do **not** include `Near to lift`.
  - Any other request tokens are treated as not satisfied.
  - Let:
    - `total_requests` = the number of request tokens in `Additional Requests` (after splitting by commas; `0` if `Additional Requests` is `null`/blank).
    - `satisfied_requests` = the number of request tokens satisfied by the room using the rules above.
  - Compute:
    - If `total_requests == 0`, then `Request Satisfaction % = 100`.
    - Otherwise, `Request Satisfaction % = round( (satisfied_requests / total_requests) * 100 )`, rounded to the nearest integer.

- Filter so that guests are only left with rooms with the highest Request Satisfaction %:
  - For each `Party`, find the maximum `Request Satisfaction %` across that party’s valid pairings.
  - Keep only the pairings for that party whose `Request Satisfaction %` equals that maximum (i.e., ties are retained unless removed by a later rule).

- Finally, for the rooms with the largest capacity, ensure guests with larger parties are prioritised. Filter the data to remove parties that could fit into smaller rooms:
  - Remove any remaining pairing where the room has adult capacity at least 4 (`Room Adults >= 4`) while the party has 2 or fewer adults (`Party Adults <= 2`).

- Apply the final explicit override used in the allocation logic:
  - For the party `Gendrich`, when considering rooms with `Room Adults == 4`, retain only `Room == 601` and remove the other `Room Adults == 4` options.

- Output the data:
  - Output grain: one row per remaining valid guest-room pairing after all filters above.
  - Use the room `Features` text as-is in the output.
  - Ensure numeric fields are output as integers and `Requires Accessible Room?` as a boolean.
  - Sort the output by `Party` ascending, then `Room` ascending for deterministic ordering.

## Output

- output_01.csv
  - 11 fields:
    - Party
    - Adults in Party
    - Children in Party
    - Double/Twin
    - Requires Accessible Room?
    - Additional Requests
    - Request Satisfaction %
    - Room
    - Adults
    - Children
    - Features