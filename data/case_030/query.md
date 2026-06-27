## Context
Data is everywhere and when your colleague finds a fun dataset then it instantly needs to be cleaned. This is what happened when Andy Kriebel found the Serpentine Swimming Club tweets that record the temperature and a fun comment about what happened that day. So what words get used more as the temperatures increase? How about those 'nippy' 10oC days? Well I've produced a simple Tableau Public view to let you analyse the output and check your results.

## Requirements

- Input the data
- Only keep tweets that give water / air temperatues
- Extract Water and Air Temperatures as separate columns
- Remove Common English words by linking the 2nd Input
- Remove unrequired fields and remove punctuation from your words from the tweets
- Output the data

- Ensure the result CSV is de-duplicated by full tuple (entire row), keeping only the first occurrence.

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
