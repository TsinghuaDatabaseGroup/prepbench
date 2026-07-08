## Context

For many of the Preppin' Data challenges, we generate randomised data in order to keep the datasets freely shareable. Sometimes this can end up being more challenging than the challenge itself!
If you've ever had to anonymise data so that you can publish a visualisation that you built using sensitive data, or built a dataset to work off of whilst waiting for access to the live data, then I'm sure you can sympathise with how frustrating this can be! You don't want the numbers to be so random that they appear unrealistic, but you also don't want to manually decide upon each value.
Randomising the data at the lowest level of detail is one option, but can result in values varying too drastically when aggregating the data. A growth rate of 56% from one month to the next isn't always very realistic!
This week's challenge is all about the process of generating the data for last week's challenge. It's unlikely you'll get the exact same numbers since we're randomizing the data, but as long as they look sensible, then that's the main goal!

## Requirements

- Input the data
Important: Tableau's Random function doesn't show up when you search for it, but typing Random() into a calculated field works! (Even though it doesn't turn blue). However, I found aggregating these randomised values to be inconsistent and inappropriate for the method I was using. So I have included a list of randomly generated values to use instead.
- You can choose to use the inputs provided or create your own!
- Calculate the Total Market Sales for April.
- Generate the Market Share for March for each Company.
  - Remember, summing together all the Market Shares should come to 100%.
  - Hint: I found this method useful!
  - Hint: To generate a number between *a* and *b* the following formula may be useful: Random()*(*b*-*a*)+*a*
  - Remember: Market Shares shouldn't be negative!
- The Market Share for April shouldn't fluctuate drastically from month to month. ±0.2% seems sensible.
  - I couldn't find a way to do this randomly and still maintain a 100% total, so a cheeky if statement is acceptable here.
- Calculate Sales for each Company for March and April.
- Calculate the Growth for each Company.
- Bring in the Scents for each Company.
- Generate the Growth rate for each Scent in each Company.
  - Make sure the growth rates for each scent sum together to equal the growth rate for the whole company.
- Use these growth rates to calculate the difference in Sales from March to April.
- Generate the Sales for March for each Scent in each Company.
  - Make sure it sums together to equal the Total Company Sales for March.
- Calculate the Sales for April for each Scent in each Company.
- Output the data with all the Sales figures in one field (see below)

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

- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Company
    - Soap Scent
    - Month
    - Sales
