## Context

After the Sudzilla conference, the team collected attendee survey responses. You need to reshape and derive metrics from these responses so the event can be summarized and analyzed, including a Net Promoter Score (NPS) and per-response fields that are easier to work with.

NPS is based on the question “On a scale of 0–10, how would you rate Sudzilla?” where:
- Promoters are ratings of 9–10
- Detractors are ratings of 0–6
- Ratings of 7–8 are neither promoters nor detractors but are still counted as respondents

The NPS formula is:  
(Promoters − Detractors) / Number of respondents × 100

## Requirements

- Input the data.
  - Read both `input_01.csv` and `input_02.csv`.
  - Use `input_02.csv` as the primary source for all calculations and for producing both outputs (it contains the needed response-level fields, including timestamps).

- Work out the Net Promoter Score for Sudzilla using the field `On a scale of 0-10, how would you rate Sudzilla?`.
  - Treat each row in `input_02.csv` as one respondent.
  - Compute:
    - `Promoter` = count of respondents with rating ≥ 9
    - `Detractor` = count of respondents with rating ≤ 6
    - `Total Respondents` = total number of respondent rows (including those rated 7–8)
    - `NPS Score` = ((Promoter − Detractor) / Total Respondents) × 100
  - Round `NPS Score` to 1 decimal place.
  - Output this summary as a single-row table.

- Split the `Which three words would you use describe to Sudzilla? (separate with a comma)` field into individual words and apply a grouping/standardization technique to "clean" these words.
  - Create a new field named `Which three words would you use describe to Sudzilla? (separate with a comma) Split` containing one standardized word per row.
  - Reshape the data so that each original respondent can produce multiple rows: one row per unique standardized word for that respondent (uniqueness should be enforced case-insensitively within each respondent so repeated words do not create duplicates for that respondent).
  - Apply a predefined standardization/grouping step that maps word variants to canonical word forms (the goal is to consolidate equivalent responses; this step may change row counts compared with a naive split).
  - Standardization steps:
    - Split the field by comma and strip whitespace from each word.
    - Remove trailing punctuation marks (periods, commas, exclamation marks, question marks, semicolons, colons) from words, except preserve the word "minty." with its trailing period.
    - Map each word (after punctuation removal, converted to lowercase) to its canonical form using the predefined mapping table below (keys are lowercase).
    - The mapping should handle case normalization (some canonical forms are lowercase, some have capital letters) and consolidate semantically equivalent variants.
  - Canonical word mapping (lowercase key -> canonical form):

```json
{
  "alarm": "alarm",
  "bad": "bad",
  "beardy": "beardy",
  "beef jerky": "beef jerky",
  "boring": "boring",
  "bubbly": "bubbly",
  "cerulean": "Cerulean",
  "challenging": "challenging",
  "clean": "Clean",
  "cleaning": "cleaning",
  "cleansing": "Cleansing",
  "creativity": "creativity",
  "cretaceous": "Cretaceous",
  "crowded": "crowded",
  "damp": "damp",
  "dangerous": "Dangerous",
  "deflating": "deflating",
  "dirty": "dirty",
  "eastenders": "Eastenders",
  "ecclesiastical": "Ecclesiastical",
  "effulgent": "Effulgent",
  "english": "English",
  "fast moving": "fast moving",
  "feckless": "Feckless",
  "felt": "felt",
  "feminine": "Feminine",
  "fizz-less": "fizz-less",
  "flat": "Flat",
  "flirty": "flirty",
  "foamy": "Foamy",
  "food": "food",
  "foodies": "Foodies",
  "fragrant": "fragrant",
  "fresh": "fresh",
  "frothy": "frothy",
  "fun": "Fun",
  "fuzzy": "Fuzzy",
  "gamechanger": "Gamechanger",
  "go somewhere else": "Go somewhere else",
  "hollyoaks": "Hollyoaks",
  "i": "I",
  "in": "in",
  "innovative": "Innovative",
  "inspirational": "Inspirational",
  "inspiring": "Inspiring",
  "intense": "Intense",
  "interactive": "interactive",
  "invigorating": "Invigorating",
  "joyous": "Joyous",
  "jurassic": "Jurassic",
  "lachrymose": "Lachrymose",
  "loud": "Loud",
  "marketing": "marketing",
  "messy": "messy",
  "minty.": "Minty.",
  "monsterous": "Monsterous",
  "murky": "Murky",
  "neighbours": "Neighbours",
  "nonsense": "nonsense",
  "not": "Not",
  "outrageous": "Outrageous",
  "overpowering": "overpowering",
  "overrated": "overrated",
  "party": "party",
  "provence": "Provence",
  "really": "really",
  "salubrious": "Salubrious",
  "scintillating": "Scintillating",
  "seismic": "Seismic",
  "service": "service",
  "slippery": "slippery",
  "smooth": "smooth",
  "soap": "soap",
  "soapy": "Soapy",
  "squeaky": "Squeaky",
  "sterile": "Sterile",
  "sudcellent": "Sudcellent",
  "suddy": "suddy",
  "sudriffic": "Sudriffic",
  "sudtastic": "Sudtastic",
  "sudzarific": "Sudzarific",
  "superb": "Superb",
  "synergy": "Synergy",
  "terrifying": "Terrifying",
  "theatrical": "Theatrical",
  "triassic": "Triassic",
  "vibrant": "vibrant",
  "waste": "waste",
  "well-paced": "Well-paced",
  "wet": "Wet",
  "wild": "wild"
}
```

- Change food rating fields to a 1–5 score (bad to good) and average the value. Rename this to `Food Rating Score`.
  - Use these three input fields:
    - `How would you rate the food at Sudzilla (breakfast)?`
    - `How would you rate the food at Sudzilla (lunch)?`
    - `How would you rate the food at Sudzilla (dinner)?`
  - Convert each of the three meal ratings to numeric scores using this ordinal mapping:
    - `Horrendous` → 1
    - `Just about edible but I was hungry` → 2
    - `Some good, some not so good` → 3
    - `Yum!` → 4
    - `Give the team a Michelin star!!` → 5
  - If a meal rating is missing or not in the mapping, treat it as null for scoring.
  - Compute `Food Rating Score` as the mean of the available (non-null) meal scores for that respondent.
  - Round `Food Rating Score` to 9 decimal places for output.

- Form an average score for the keynotes. Rename this to `Keynote Rating Score`.
  - Use these two input fields:
    - `On a scale of 0-10, how would you rate the opening keynote?`
    - `On a scale of 0-10, how would you rate the closing keynote?`
  - Compute `Keynote Rating Score` as the mean of the two keynote ratings for that respondent.
  - Round `Keynote Rating Score` to 1 decimal place for output.

- Prepare the detailed output rows and formatting.
  - Ensure `Timestamp` is parsed as a datetime and then formatted as `M/D/YYYY H:MM:SS AM/PM` (month/day/hour without leading zeros).
  - Rename the field `...why?` to `___why?`.
  - For the two text fields below, remove leading and trailing whitespace:
    - `What was your favourite giveaway at Sudzilla?`
    - `What was your favourite 'Soap Box' (breakout / customer speaker) session?`
  - After all transformations, remove fully duplicate rows in the detailed output (across all output columns), keeping the first occurrence.

- Output the data as two CSV files exactly as specified below.

## Output

- output_01.csv
  - 4 fields:
    - NPS Score
    - Total Respondents
    - Promoter
    - Detractor

- output_02.csv
  - 8 fields:
    - Which three words would you use describe to Sudzilla? (separate with a comma) Split
    - Keynote Rating Score
    - Food Rating Score
    - Timestamp
    - On a scale of 0-10, how would you rate Sudzilla?
    - ___why?
    - What was your favourite giveaway at Sudzilla?
    - What was your favourite 'Soap Box' (breakout / customer speaker) session?
