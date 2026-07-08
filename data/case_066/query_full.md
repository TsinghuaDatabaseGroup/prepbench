## Context
You have received an encrypted text message and a substitution cipher. The goal is to decode the message by splitting it into individual characters (while preserving their original order), translating each character via the cipher, and then recombining the decoded characters into the final decoded message.

## Requirements
- Input the data
  - Read the encrypted message from `input_01.csv` using the field `Encrypted Message`.
    - Use the first non-null value in `Encrypted Message` as the message to decode.
  - Read the cipher mapping from `input_03.csv` using the fields `Cipher` and `Alphabet`.
    - Only cipher rows where both `Cipher` and `Alphabet` are present are valid for decoding.
- Find a way to split each character of the encrypted message onto a separate line.
  - Create one row per character in the message, including spaces.
  - Make sure you retain the original order of the message by assigning and keeping a zero-based position index for each character (0 for the first character, 1 for the second, etc.).
- Use the cipher to decode the message.
  - Decode each character as follows:
    - If the character is a space (`' '`), keep it as a space.
    - Otherwise, look up the character in the cipher mapping where `Cipher` equals the encrypted character, and replace it with the corresponding `Alphabet` value.
    - If there is no matching cipher mapping for a character, keep the original character unchanged.
  - This is logically a left join from the character rows to the cipher table on `encrypted_char = Cipher`, retaining all characters even when no match is found.
- Concatenate the individual decoded characters back into a single string.
  - Concatenate decoded characters in ascending `position` order to form one final decoded message string.
  - Make sure those spaces haven't become nulls! (Spaces must remain spaces in the concatenated result; unmatched characters must remain as their original character.)
- Output the data
  - Produce a single-row output containing the fully concatenated decoded message.

## Output

- output_01.csv
  - 1 fields:
    - Decoded Message