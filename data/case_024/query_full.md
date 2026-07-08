## Context

You are analysing a WhatsApp group export where the message bodies have been replaced with placeholder text, but the true sender and timestamp metadata are retained. A second input provides a calendar classification so you can distinguish weekdays from weekends and public holidays (“Bank Holidays”). The goal is to produce a single summary output per participant that allows Kamilla and Bona to identify (from the reported metrics) who is most active overall and who sends the greatest share of messages during working hours, as well as compare message length via word-based measures.

## Requirements

- Input the data.
- Use both input files:
  - Use `input_02.csv` as the chat log source. Each record to be analysed is a single message contained in `Field_1`.
  - Use `input_01.csv` as the calendar lookup, mapping each calendar `Date` to its `Holiday?` classification.
- Parse each chat log message in `input_02.csv` from `Field_1` into:
  - a full timestamp (day/month/year and hour:minute:second),
  - the sender name,
  - the message text content.
  The expected structure is a bracketed timestamp followed by "Name: Message".
- Data cleaning and ambiguity resolution:
  - Date format: The timestamp in `input_02.csv` uses the format `DD/MM/YYYY` (day/month/year). For example, `12/05/2019` represents 12 May 2019, not 5 December 2019.
  - Sender name cleaning: Trim leading and trailing whitespace from sender names.
  - Word counting rules: When counting words, treat hyphens and dashes as word separators (e.g., "night - prowling" contains two words: "night" and "prowling"). Numeric sequences (digits only, such as "500") are not counted as words. Only sequences containing at least one letter (A–Z/a–z) or apostrophe are counted as words.
- Link each message to the calendar classification from `input_01.csv` by constructing a calendar key from the message timestamp equal to:
  - the day-of-month as a number (no leading zero requirement implied), followed by a space, followed by the full month name in English (e.g., “1 January”),
  and matching this key to `input_01.csv`’s `Date`.
  - Use a left join from messages to the calendar table so every parsed message remains in the analysis even if it does not find a calendar match.
- Define “at work” messages using both day type and time-of-day:
  - A message is eligible for “at work” only if its linked `Holiday?` value is exactly `Weekday`.
  - Working hours are 09:00:00–11:59:59 and 13:00:00–17:00:00, inclusive of endpoints (lunch break 12:00:00–12:59:59 is excluded).
- Compute message-level measures:
  - Treat each message as `Text = 1` (a count of messages).
  - Compute `Number of Words` for each message by counting word tokens according to the word counting rules specified in the "Data cleaning and ambiguity resolution" section above. (You must not use the `split` function.)
  - Compute `Text while at work` as 1 if the message meets the “at work” definition above, otherwise 0.
- Aggregate to one row per sender (`Name`) and produce:
  - `Text`: total number of messages sent by that person (sum of message-level `Text`).
  - `Number of Words`: total number of words across that person’s messages (sum of message-level `Number of Words`).
  - `Text while at work`: total number of “at work” messages for that person (sum of message-level `Text while at work`).
  - `Avg Words/Sentence`: `Number of Words / Text`, rounded to 1 decimal place using half-up rounding.
  - `% sent from work`: `(Text while at work / Text) * 100`, rounded to 1 decimal place using half-up rounding.
- Produce one single output file containing all required fields (no separate outputs for individual questions).
- Make the output deterministic by sorting the final rows by `Name` in ascending order.
- Output the data.

## Output

- output_01.csv
  - 6 fields:
    - Name
    - Text
    - Number of Words
    - Avg Words/Sentence
    - Text while at work
    - % sent from work