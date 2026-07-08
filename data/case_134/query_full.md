## Context
You are given a catalogue of frame sizes and a list of pictures with their sizes. The goal is to assign each picture to a frame that can contain it (allowing the frame to be rotated), selecting the best-fitting frame by minimizing unused frame area.

## Requirements
- Input the data.
  - Read frames from `input_01.csv` and pictures from `input_02.csv`.
  - Frames are identified by their size label in the frames file; pictures are identified by the `Picture` field in the pictures file.
- Split up the sizes of the pictures and the frames into lengths and widths.
  - Parse each `Size` label into two numeric side lengths in centimeters.
  - Supported size formats are:
    - Rectangles in centimeters: `Ncm x Mcm`
    - Squares in centimeters: `Ncm2` (treat as `Ncm x Ncm`)
    - Rectangles in inches: `N" x M"` (convert each side to centimeters)
  - Remember an inch is 2.54cm (multiply inch values by 2.54 to convert to cm).
- Frames can always be rotated, so make sure you know which is the min/max side.
  - For every parsed size (both pictures and frames), normalize the dimensions to `(Max Side, Min Side)` where `Max Side = max(length, width)` and `Min Side = min(length, width)`.
- See which pictures fit into which frames.
  - A frame fits a picture if, after normalization, `Frame_Max >= Picture_Max` and `Frame_Min >= Picture_Min`.
- Work out the area of the frame vs the area of the picture and choose the frame with the smallest excess.
  - Compute `Picture_Area = Picture_Max * Picture_Min` and `Frame_Area = Frame_Max * Frame_Min`.
  - For each picture, consider only frames that fit and compute `Excess = Frame_Area - Picture_Area` (which will be non-negative for fitting frames).
  - Select the frame with the smallest `Excess`.
  - Tie-breaker: if multiple frames have the same smallest excess, choose the one that appears first in `input_01.csv` (earliest row order).
  - If no frame fits a picture, output a blank/NULL frame value for that picture.
- Output the data.
  - Output one row per picture, preserving the original picture order from `input_02.csv`.
  - In the output, report the picture’s normalized sides as integers by rounding `Picture_Max` and `Picture_Min` to the nearest whole number before writing.

## Output

- output_01.csv
  - 4 fields:
    - Picture
    - Frame
    - Max Side
    - Min Side