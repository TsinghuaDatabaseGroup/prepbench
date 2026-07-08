## Context

You have separate “Key Metrics” tables for multiple Shops, each containing performance values by month (and additional non-monthly summary columns) plus a Target value for each metric. The goal is to consolidate all Shops into one consistent monthly dataset, keep only the required measures, attach the corresponding targets, and reshape to a single wide table where each row represents a Shop-month.

## Requirements

- Input the data.
  - Read the Key Metrics CSV for each Shop (12 input files). Each file contains non-data header lines, so the table should be read starting from the 4th row (i.e., using the row that begins the column headers as the header row).
  - Assign the Shop name based on which input file it came from. Use the following mapping from input filename to Shop name:
    - input_01.csv → Bath
    - input_02.csv → Bristol
    - input_03.csv → Exmouth
    - input_04.csv → Hastings
    - input_05.csv → Leicester
    - input_06.csv → Newcastle
    - input_07.csv → Nottingham
    - input_08.csv → Plymouth
    - input_09.csv → Portsmouth
    - input_10.csv → Reading
    - input_11.csv → Southampton
    - input_12.csv → Torquay
  - Some input files contain an "Additonal Metrics" section (with a typo in the original spelling). Exclude all rows from the "Additonal Metrics" section onward when processing the data. Only process rows that appear before this section marker.

- Bring together the Key Metrics tables from each Shop.
  - Stack/union the extracted records from all Shops into one combined dataset.

- You’ll notice that we have fields which report the quarter in addition to the monthly values. We only wish to keep the monthly values.
  - Treat “monthly values” as the columns whose column headers can be parsed as dates. Only those date-parsable columns are eligible to become monthly observations; ignore all other non-date columns (including any quarterly summary columns).

- Reshape the data so that we have a Date field.
  - Convert the monthly date columns into rows (i.e., pivot longer / melt), producing records keyed by:
    - Shop
    - Date (the parsed date from the original column header)
    - Department
    - Breakdown
    - Target
    - Value (the numeric metric value for that Shop and Date)
  - Keep only rows where both Date and Value are present and Value is numeric.

- For Orders and Returns, we are only interested in reporting % values, whilst for Complaints we are only interested in the # Received.
  - Identify and keep only these measures, using the combination of Department and Breakdown:
    - Department = Orders, Breakdown = % Shipped in 3 days  → “% Orders Shipped in 3 days” (percent measure)
    - Department = Orders, Breakdown = % Shipped in 5 days  → “% Orders Shipped in 5 days” (percent measure)
    - Department = Returns, Breakdown = % Processed in 3 days → “% Returns Processed in 3 days” (percent measure)
    - Department = Returns, Breakdown = % Processed in 5 days → “% Returns Processed in 5 days” (percent measure)
    - Department = Complaints, Breakdown = # Received → “# Complaints Received” (count measure)
  - Discard all other Department/Breakdown combinations.

- We wish to update the Breakdown field to include the Department to make the Measure Name easier to interpret.
  - Implement this by mapping the (Department, Breakdown) pair to the explicit measure names listed above (e.g., “% Orders Shipped in 3 days”), so the measure is unambiguous across departments.

- We wish to have a field for each of the measures rather than a row per measure.
  - First construct a long-form dataset with fields: Shop, Date, Measure, Value, where Measure is one of the mapped measure names above.
  - Then pivot wider so that each (Shop, Date) becomes a single row and each Measure becomes its own column. If multiple values exist for the same (Shop, Date, Measure), take the first available value.

- We wish to have the targets for each measure as field that we can compare each measure to.
  - For each kept record, derive a numeric target from the Target field and create an additional long-form record with:
    - Measure = “Target - {measure name}”
    - Value = parsed target value
  - Target parsing rules:
    - Remove any “>” and “%” symbols before numeric conversion.
    - Convert to a number; if conversion fails or Target is blank/missing, do not create a target record.
    - For percent measures only: if the resulting numeric target is greater than 1, divide by 100 so targets are stored on a 0–1 scale.
  - After appending target records, pivot wider so the target measures become columns alongside the actual measures.

- Final formatting, ordering, and rounding:
  - Output grain: one row per Shop per monthly Date.
  - Format Date as `DD/MM/YYYY`.
  - Round the four percent measure columns and their four corresponding target columns to 2 decimal places.
  - Round “# Complaints Received” and “Target - # Complaints Received” to whole numbers and store them as integers.
  - Sort the output by Shop using this fixed order, then by Date ascending within Shop:
    1) Leicester, 2) Bristol, 3) Plymouth, 4) Exmouth, 5) Nottingham, 6) Newcastle, 7) Southampton, 8) Hastings, 9) Bath, 10) Reading, 11) Torquay, 12) Portsmouth.

- Output the data.

## Output

- output_01.csv
  - 12 fields:
    - Shop
    - Date
    - % Orders Shipped in 3 days
    - Target - % Orders Shipped in 3 days
    - % Orders Shipped in 5 days
    - Target - % Orders Shipped in 5 days
    - % Returns Processed in 3 days
    - Target - % Returns Processed in 3 days
    - % Returns Processed in 5 days
    - Target - % Returns Processed in 5 days
    - # Complaints Received
    - Target - # Complaints Received