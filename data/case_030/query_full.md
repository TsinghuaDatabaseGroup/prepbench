## Context
You are preparing tweet data from the Serpentine Swimming Club that records both water and air temperatures alongside a short free-text comment. The goal is to structure these tweets into a token-level dataset so you can analyze which comment words appear as temperatures change, while excluding common English words.

## Requirements
- Input the data.
  - Read the tweets dataset from `input_02.csv`, using at least the fields `Tweet Id`, `Text`, and `Created At`.
  - Read the common English words dataset from `input_01.csv`, using the field `Word` (and any other fields provided, such as `Rank`, if present).

- Only keep tweets that give water / air temperatues.
  - Keep only tweets whose `Text` contains both a Water temperature and an Air temperature entry.

- Extract Water and Air Temperatures as separate columns.
  - From each retained tweet's `Text`, parse and extract:
    - Water temperature in Fahrenheit and Celsius.
    - Air temperature in Fahrenheit and Celsius.
  - Temperature extraction rules:
    - The tweet text contains temperature information in the format: `Water - X.XF / X.XC; Air - X.XF / X.XC` (where X.X represents decimal numbers).
    - Extract the numeric values immediately following "Water -" and "Air -" respectively.
    - For each temperature entry, extract both the Fahrenheit value (ending with "F") and the Celsius value (ending with "C").
    - The Fahrenheit and Celsius values are separated by " / " and appear in the order: Fahrenheit first, then Celsius.
    - If the tweet text does not contain both Water and Air temperature entries in this format, or if any of the four temperature values (Water F, Water C, Air F, Air C) cannot be extracted, exclude that tweet from further processing.

- Standardize and format the timestamp.
  - Parse `Created At` as a datetime and output it formatted as `DD/MM/YYYY HH:MM:SS` (with timezone removed after parsing).

- Remove unrequired fields and remove punctuation from your words from the tweets.
  - Derive a `Comment` field from the tweet text as the human-readable comment portion:
    - Replace any line breaks with spaces.
    - Remove the leading temperature/status prefix from the tweet text to extract the comment portion:
      - The tweet text typically follows the pattern: `[date prefix] Water - X.XF / X.XC; Air - X.XF / X.XC. [comment text]`
      - Locate the Air temperature section, which ends with a Celsius value followed by either:
        - "C. " (the letter C, a period, and a space), or
        - "C " (the letter C and a space, if no period follows)
      - Remove all text from the beginning of the tweet up to and including "C. " if it exists. If "C. " does not exist, remove all text up to and including the "C " that immediately follows the Air temperature's Celsius value (the last temperature value in the sequence).
      - The remaining text after this removal is the `Comment` field.
      - Example: From `"12 Jun 2012: Water - 58.0F / 14.4C; Air - 57.0F / 13.9C. Oh dear me..."`, remove up to and including "C. ", resulting in `"Oh dear me..."`
    - Trim surrounding whitespace from the resulting `Comment` field.
  - Tokenize the `Comment` into individual words (`Comment Split`) by:
    - Converting to lowercase.
    - Replacing punctuation (non-word, non-whitespace characters) with spaces.
    - Splitting on whitespace to obtain tokens.

- Remove Common English words by linking the 2nd Input.
  - Normalize the common-words list (from `input_01.csv`) in a way consistent with the tokenization (lowercased, punctuation removed, trimmed).
  - Remove any tokens that appear in the normalized common-words list.

- Token selection rules per tweet.
  - Within each tweet, keep only the first occurrence of each remaining token (i.e., de-duplicate tokens per tweet while preserving the original token order).
  - Limit to at most 25 tokens per tweet after this per-tweet de-duplication; keep the earliest tokens in the comment order.
  - If a tweet has no remaining tokens after filtering, exclude it.

- Reshape to the required output grain.
  - Explode tokens so each remaining token becomes its own row.
  - For each (tweet, token) row, create two output rows:
    - One with `Category = "Water"` and temperatures populated from the extracted Water temperatures.
    - One with `Category = "Air"` and temperatures populated from the extracted Air temperatures.
  - The output grain must therefore be one row per (Tweet Id, token, Category).

- Output the data.
  - Keep only the required output fields and names as specified below.

- Ensure the result CSV is de-duplicated by full tuple (entire row), keeping only the first occurrence.
  - After constructing the final dataset, if any rows are exact duplicates across all output fields, drop duplicates by the full row content, keeping the first occurrence.

## Output

- output_01.csv
  - 7 fields:
    - Comment Split
    - Category
    - TempF
    - TempC
    - Comment
    - Tweet Id
    - Created At
  - Created At format must be exactly `DD/MM/YYYY HH:MM:SS`.
