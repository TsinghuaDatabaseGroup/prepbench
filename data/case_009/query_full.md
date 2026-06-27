## Context

Chin & Beard Suds Co wants to analyze complaint tweets that tag the company’s Twitter handle and identify common themes. To support repeatable analysis and downstream reporting, prepare a dataset that breaks each complaint tweet into its component words (excluding common stop words) while retaining the original tweet context for each word.

## Requirements

- Input the data.
  - Use `input_01.csv` as the source of tweets and read the tweet text from the `Tweet` field.
  - Use `input_02.csv` as the stop-word reference list and read stop words from the `Word` field.
- Remove the Chin & Beard Suds Co Twitter handle.
  - In each tweet’s text, remove the literal string `@C&BSudsCo`.
- Split the tweets up into individual words.
  - Create a cleaned copy of the tweet text for tokenization only.
  - In this cleaned copy, retain only alphabetic characters (A–Z, a–z) and spaces; remove all other characters.
  - Split the resulting text on whitespace to produce a list of word tokens for each tweet.
- Pivot the words so we get just one column of each word used in the tweets.
  - Output at a “word-within-tweet” grain: one row per (tweet, word) combination.
  - Within each tweet, keep only the first occurrence of each word (i.e., de-duplicate words per tweet while preserving the word’s first-appearance order for that tweet).
- Remove the 250 most common words in the English language.
  - Implement this by excluding any word whose normalized form appears in the provided stop-word list (`input_02.csv`).
  - Normalize both tweet words and stop words by (1) removing all non-alphabetic characters and (2) lowercasing, then filter out words whose normalized value matches a normalized stop word.
- Output a list of words used alongside the original tweet so we know the context for how the word was used.
  - The `Tweet` value in the output must be the original tweet text after removing `@C&BSudsCo` only; preserve punctuation and casing in this `Tweet` field.
  - Use the cleaned copy (alphabetic characters only) only for tokenization and stop-word filtering.
  - The `Words` value must be the token as produced from the cleaned tweet text (alphabetic characters only), prior to stop-word normalization.
- Output the data.

## Output

- output_01.csv
  - 2 fields:
    - Words
    - Tweet
