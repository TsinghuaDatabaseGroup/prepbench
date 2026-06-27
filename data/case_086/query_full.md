## Context
Prepare William Wordsworth poem text for a Scrabble-style scoring analysis that can be used to build a simple dashboard: keep only true poem lines, break text down to words, score each word using Scrabble letter values, and identify the highest-scoring word(s) within each poem.

## Requirements
- Input the data from `input_01.csv`.

- Filter to retain only rows that represent actual lines of the poems (i.e., exclude rows that contain HTML/CSS/JavaScript or other non-poem content, such as code-like fragments). Rows that are empty, too short to be a meaningful line, or contain no alphabetic characters must not be treated as poem lines.
  
  **Ambiguity resolution for filtering non-poem lines:**
  - **HTML/CSS/JavaScript identification rules:** Exclude rows that meet any of the following criteria:
    - Contain HTML angle brackets (`<` or `>`)
    - Match case-insensitive patterns for HTML tags: `<SCRIPT`, `</SCRIPT`, `<STYLE`, `</STYLE`, `<HEAD`, `</HEAD`, `<BODY`, `</BODY`, `<HTML`, `</HTML`, `<BR`, `<DIV`, `<P>`
    - Match case-insensitive patterns for JavaScript/CSS code: `STYLE=`, `JAVASCRIPT`, `OBJECT()`, `E9=`, `URCHIN`, `ADSBYGOOGLE`, `GOOGLE_AD`, `DATA-AD`, `WINDOW.`, `PUSH({})`, `_UACCT`, `SIZE =`, `728X90`, `468X60`, `336X280`, `300X250`, `300X600`
    - Contain an equals sign (`=`) and the first 20 characters contain no alphabetic characters (typically JavaScript assignments)
    - Contain multiple equals signs, or contain both equals sign and semicolon (code-like syntax)
  - **"Too short" standard:** After cleaning (removing `_x000D_` markers and trimming whitespace), exclude rows where the cleaned text length is less than 3 characters.
  - **Alphabetic character requirement:** The cleaned text must contain at least one alphabetic character (A-Z, a-z).

- Standardize the poem line text to a single `Line` field for downstream processing (this is the text that will be numbered and split into words). Use the cleaned `Line` value consistently for deduplication and word-splitting.
  
  **Data cleaning steps:**
  - Remove `_x000D_` markers from the text
  - Trim leading and trailing whitespace
  - Remove leading patterns matching `--` (one or more dashes) followed by optional whitespace
  - Remove all occurrences of `--` (double dashes) within the line
  - Trim whitespace again after cleaning

- Wordsworth is very original, so there shouldn't be any duplicate lines in our data set. Filter out any repeated rows by removing duplicate `(Poem, Line)` combinations, keeping the first occurrence in the poem’s original order.

- The first line of each poem is also the title of the poem. Treat the first retained line within each poem as line `1` (the title line) and assign an increasing `Line #` to subsequent retained lines within the same poem.
  - Determine the original order of lines within each poem using the input’s row ordering field (so line numbering follows the source sequence).
  - Do not assign line numbers to rows that are excluded because they are not valid poem lines or do not yield any valid words.

- Split the data out so there is a line for each word and assign a word number for each line.
  - Output grain: one row per word occurrence within a specific poem line.
  - For each `(Poem, Line #, Line)`:
    - Extract words as contiguous alphabetic sequences (A–Z). Before extracting, treat apostrophes and hyphens as not part of words (so they do not create separate tokens and do not contribute characters to scoring).
      **Ambiguity resolution for apostrophes and hyphens:** Remove apostrophes (`'`) and hyphens (`-`) from the text before word extraction. This means words like "earth's" become "EARTHS" (as a single word), and "evening-moon" becomes "EVENINGMOON" (as a single word). After removal, extract contiguous alphabetic sequences using word boundaries.
    - If a line yields zero extracted words, exclude that line from the output (and therefore it should not advance the line numbering).
    - Assign `Word #` starting at 1 for the first word in the line and increasing by 1 in reading order.

- Split the data into individual letters and combine with the associated Scrabble score, then aggregate so each word has a Scrabble score.
  - Compute `Score` per word as the sum of Scrabble letter values across its letters using the standard mapping:
    - A1, B3, C3, D2, E1, F4, G2, H4, I1, J8, K5, L1, M3, N1, O1, P3, Q10, R1, S1, T1, U1, V4, W4, X8, Y4, Z10.
  - Output `Word` in uppercase and score it based on its letters (non-letter characters must not contribute to the score).

- Create a flag for the highest scoring word in each poem.
  - For each `Poem`, find the maximum `Score` across all output rows for that poem.
  - Set `Highest Scoring Word?` to `True` for every row whose `Score` equals that poem-level maximum (i.e., if there are ties, flag all tied highest-scoring words); otherwise `False`.

- Output the data to the required file and fields.

## Output

- output_01.csv
  - 7 fields:
    - Poem
    - Line #
    - Line
    - Word #
    - Word
    - Score
    - Highest Scoring Word?