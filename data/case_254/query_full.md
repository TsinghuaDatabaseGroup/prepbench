## Context

Santa is preparing a production tracking dashboard for toys made throughout the year. The objective is to (1) produce a weekly dataset that shows when each toy’s cumulative production exceeds its quota, and (2) produce a toy-level annual summary per list that also determines how any list-level surplus should be converted into “spare toys” so the number of gift-ready toys matches the number of children on each list.

## Requirements

- Input the data.
  - Use `input_01.csv` as the reference table for mapping initials to name components.
  - Use `input_02.csv` as the production table containing toys, quotas, staff initials, and weekly production quantities.

- Extract the information for which toys belong to which list.
  - In `input_02.csv`, list membership is defined by section header/marker rows whose `Toy` text indicates the list name and where the corresponding `Quota` cell holds the list's "Number of Children".
  - **List name extraction rule**: The marker rows have `Toy` values in the format "Number of Children on the [List Name] List". To extract the list name for the output `List` field, remove the prefix "Number of Children on the " from the `Toy` text, and also remove the trailing " List" suffix. For example:
    - "Number of Children on the Nicest List" → "Nicest"
    - "Number of Children on the Nicer than Most List" → "Nicer than Most"
    - "Number of Children on the Nice List" → "Nice"
  - Assign each subsequent toy row to the most recent list marker above it, and carry the associated "Number of Children" down to all toy rows in that list section.
  - Remove the marker rows themselves from the toy-level production dataset (they are not real toys).

- Update the Quota to represent the number of toys needed.
  - Treat the toy-level `Quota` in `input_02.csv` as a proportion of the list’s “Number of Children”.
  - Compute the required toy quota as:  
    **Quota (count) = round(Quota (proportion) × Number of Children, to 0 decimals)**, then store as an integer.

- Match the Elves' Initials to their Names.
  - Only the **Production Manager** needs to be retained; other staff roles in the input are not required for the outputs.
  - Build a mapping from `input_01.csv` where each row provides a single-letter initial and the corresponding name word.
  - Convert each Production Manager’s two-letter initials into a two-word name by mapping:
    - first letter → first word
    - second letter → second word  
    and concatenate as `"FirstWord SecondWord"`.

- Reshape the data so we have a Date field.
  - Make sure the data type matches.

- For the first output, Santa wants to find out in which week certain toys exceed their Quota.
  - For each **List × Toy**, sort weeks chronologically and compute:
    - `Running Sum of Toys Produced` = cumulative sum of `Toys Produced` over weeks.
    - `Over or Under Quota?` = `"Over"` if `Running Sum of Toys Produced` is strictly greater than `Quota`, otherwise `"Under"`.

- Output this dataset as `output_01.csv` at the grain of **List × Toy × Week** with the required fields.

- For the second output, Santa wants to see some top level figures for the year and determine how quotas translate into gifts vs spares.
  - Aggregate to the **List × Toy** level (keeping `Quota` as the computed absolute quota count) and compute:
    - `Toys Produced` = sum of weekly `Toys Produced` across all weeks for that List × Toy.
    - `Toys Over/Under Quota` = `Toys Produced - Quota`.
  - Check at the list level whether there are enough toys for the `Number of Children` on that list by comparing total toys produced across all toys on the list to the number of children.
  - So that Santa doesn't take too many Toys on his sleigh, if a list has produced more toys than children:
    - Let **surplus** = (total list `Toys Produced`) − (`Number of Children`).
    - Assign **all** surplus to `Spare Toys` for the single toy on that list with the maximum `Toys Over/Under Quota` (i.e., the greatest overproduction). If there is a tie for maximum, select the first among the tied toys under the dataset’s existing order.
    - Set `Toys Ready to be Gifts` for that selected toy to `Toys Produced − Spare Toys`.
    - For all other toys on the list, set `Spare Toys = 0` and `Toys Ready to be Gifts = Toys Produced`.
  - If a list does not have surplus (total produced ≤ number of children), then for all toys on that list:
    - `Spare Toys = 0`
    - `Toys Ready to be Gifts = Toys Produced`

- Output the aggregated dataset as `output_02.csv` at the grain of **List × Toy** with the required fields.

## Output

- output_01.csv
  - 9 fields:
    - List
    - Number of Children
    - Toy
    - Production Manager
    - Quota
    - Week
    - Toys Produced
    - Running Sum of Toys Produced
    - Over or Under Quota?

- output_02.csv
  - 7 fields:
    - List
    - Toy
    - Quota
    - Toys Produced
    - Toys Ready to be Gifts
    - Spare Toys
    - Toys Over/Under Quota