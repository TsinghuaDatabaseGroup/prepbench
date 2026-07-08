## Context

This task reconstructs a shareable, anonymised-looking sales dataset for a soap market analysis across two months. The intent is to produce realistic-looking month-to-month changes without relying on volatile aggregation of truly random numbers. In practice, you will use the provided, pre-generated figures to assemble a complete Company × Soap Scent × Month dataset and output it in the required long format.

## Requirements

- Input the data.
  - Note: if you are working in Tableau, `Random()` may need to be typed manually into a calculated field; however, because aggregating truly random values can be inconsistent for this use case, rely on the provided pre-generated values rather than generating new random numbers at runtime.
- You can choose to use the inputs provided or create your own; however, the delivered output must match the specified final dataset structure and figures implied by the provided materials.
- Build the final dataset at the following grain:
  - One row per **Company**, **Soap Scent**, and **Month** combination.
  - Months included: **March** and **April** only.
- Ensure the dataset covers all combinations of:
  - The full set of companies in scope, and
  - The full set of scents in scope,
  - For each of the two months (i.e., a complete cross-join across Month × Company × Soap Scent).
- Populate **Sales** for each row using the provided, precomputed sales values for the corresponding (Company, Soap Scent, Month) combination.
  - Do not calculate Sales via newly-generated market shares, growth rates, or randomisation; the output Sales must come from the provided pre-generated figures.
  - The precomputed sales values are predetermined for all valid combinations of (Company, Soap Scent, Month). These values must be retrieved from a pre-existing mapping or lookup table that associates each (Company, Soap Scent, Month) tuple with its corresponding Sales figure. The input files provided may contain reference data (such as company lists, scent lists, or random seed values), but the actual Sales figures to use are the precomputed values that correspond to the complete cross-join of all companies, all scents, and both months. You must use the exact precomputed Sales value for each (Company, Soap Scent, Month) combination as specified in the provided materials; do not derive or calculate these values from the input data.
- If an explicit output row order is required by the consuming process, write rows in a consistent order:
  - Month ascending with March before April,
  - Company in a consistent, fixed sequence,
  - Soap Scent in a consistent, fixed sequence.
- Output the data with all the Sales figures in one field (see below).

**Pre-computed Sales Values (use these exact values):**

| Company | Soap Scent | March Sales | April Sales |
|---------|------------|-------------|-------------|
| Sudsie Malone | Watermelon | 16111810.1905113 | 43324732.2378659 |
| Sudsie Malone | Rose | 436189982.659625 | 474305911.129159 |
| Sudsie Malone | Pineapple | 195777011.452937 | 156272517.916588 |
| Sudsie Malone | Orange | 412134370.941974 | 353270582.65706 |
| Sudsie Malone | Lime | 484758850.134914 | 498602247.12946 |
| Sudsie Malone | Jasmine | 137170566.982806 | 205579440.043756 |
| Sudsie Malone | Coconut | 65391004.6495168 | 63112499.5439582 |
| Squeaky Cleanies | Watermelon | 376808030.777165 | 359575271.257045 |
| Squeaky Cleanies | Rose | 129787658.246884 | 128785250.425908 |
| Squeaky Cleanies | Pineapple | 238007425.850963 | 256806998.355096 |
| Squeaky Cleanies | Orange | 139286665.948943 | 151780261.822217 |
| Squeaky Cleanies | Lime | 345003632.458146 | 338907634.437198 |
| Squeaky Cleanies | Jasmine | 206828164.281029 | 224290584.599189 |
| Squeaky Cleanies | Coconut | 354586986.076179 | 357857537.8778 |
| Soap and Splendour | Watermelon | 492435899.503911 | 485419986.399615 |
| Soap and Splendour | Rose | 131704995.121507 | 141954141.481657 |
| Soap and Splendour | Pineapple | 64342384.7679437 | 77305548.196635 |
| Soap and Splendour | Orange | 33058612.1516716 | 35094874.3014569 |
| Soap and Splendour | Lime | 494326797.516198 | 504535845.949119 |
| Soap and Splendour | Jasmine | 433598049.009094 | 433397893.588997 |
| Soap and Splendour | Coconut | 246916246.91089 | 255550442.804023 |
| Chin & Beard Suds Co | Watermelon | 106952309.209599 | 102534810.120234 |
| Chin & Beard Suds Co | Rose | 118151757.969388 | 118050971.181238 |
| Chin & Beard Suds Co | Pineapple | 28306848.2002096 | 29633832.2424581 |
| Chin & Beard Suds Co | Orange | 54309340.7920479 | 67242836.7326192 |
| Chin & Beard Suds Co | Lime | 80521503.2185151 | 77961503.2398676 |
| Chin & Beard Suds Co | Jasmine | 7911885.00493674 | 22508233.9117437 |
| Chin & Beard Suds Co | Coconut | 87351394.1729071 | 90175588.8550569 |
| British Soaps | Watermelon | 115248724.394306 | 127555384.328319 |
| British Soaps | Rose | 31665157.81196 | 57405492.4024066 |
| British Soaps | Pineapple | 5183387.89368681 | 25653263.5002902 |
| British Soaps | Orange | 145897557.064093 | 130879305.934362 |
| British Soaps | Lime | 141726823.817304 | 138643749.678239 |
| British Soaps | Jasmine | 86399975.4890454 | 81225711.2659018 |
| British Soaps | Coconut | 145650549.329192 | 125860028.73346 |

- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Company
    - Soap Scent
    - Month
    - Sales