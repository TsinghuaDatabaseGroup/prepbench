## Context

You are building a single, analysis-ready dataset for a Book Shop where the grain is **one row per item sold per order line**. The core table is created by unioning multiple sales extracts, and then enriching each sales line with related book, author, publisher, series, awards, checkout, and ratings information—without ever changing the sales-line row count.

## Requirements

- Input the data.

- Union all Sales datasets together (the sales extracts) to create the base table at **one row per item in a sale**.  
  - This sales-line grain must be maintained for the entire workflow (i.e., the unioned sales row count must not increase or decrease due to subsequent steps).

- Join all other datasets in the workbook onto the unioned sales table, while ensuring the number of rows **never changes**.
  - Use **left joins from the sales-line table** so that every sales line remains present even when enrichment data is missing.
  - If a related dataset can have multiple rows per sales line key (i.e., would create a one-to-many join), do **not** join at the detailed level; instead, **summarize it to a single row per join key** before joining, as follows:
    - **Awards**: aggregate to one row per **Title** with:
      - `Number of Awards Won (avg only)` = count of award records for that Title.
    - **Checkouts**: aggregate to one row per **Book ID** with:
      - `Total Checkouts` = sum of `Number of Checkouts`.
      - `Number of Months Checked Out` = count of distinct `CheckoutMonth`.
    - **Ratings**: aggregate to one row per **Book ID** with:
      - `Average Rating` = mean of `Rating` (round to 9 decimal places).
      - `Number of Reviewers` = count of distinct `ReviewerID`.
      - `Number of Reviews` = count of rating/review records.
  - Construct/join keys required for enrichment:
    - From the genre/series dataset, ensure there is a `Book ID` field available for joining. If the dataset provides `BookID1` and `BookID2`, create `Book ID` by concatenating them in order (`BookID1` + `BookID2`). Otherwise, use the existing Book ID field if already present.
  - Apply joins in a way that preserves the intended enrichment logic:
    - Join sales to book metadata on **ISBN** to bring in `Book ID` and book attributes (`Format`, `PubID`, `Publication Date`, `Pages`, `Print Run Size (k)`, `Price`).
    - Join to the books table on **Book ID** to bring in `Title` and `AuthID`.
    - Join to authors on **AuthID** to bring author attributes.
    - Join aggregated awards on **Title**.
    - Join publishers on **PubID**.
    - Join aggregated checkouts on **Book ID**.
    - Join aggregated ratings on **Book ID**.
    - Join genre/series attributes on **Book ID**.
    - Join series dimension on **SeriesID**.

- Remove any duplicate fields created by the joins (i.e., keep only one copy of each required attribute).

- Remove the two fields created (in Prep at least) as the result of the Union, if present:
  - Table Names
  - Sheet Names

- Output formatting rules that affect the final values:
  - Format `Sale Date`, `Birthday`, and `Publication Date` as strings in `DD/MM/YYYY` (zero-padded). If a date is missing, output it as an empty string.
  - Output the following fields as integer strings with no decimals; if missing, output an empty string:
    - `Pages`, `Print Run Size (k)`, `Year Established`, `Marketing Spend`, `Number of Awards Won (avg only)`,
      `Number of Months Checked Out`, `Total Checkouts`, `Volume Number`, `Planned Volumes`,
      `Book Tour Events`, `Number of Reviewers`, `Number of Reviews`.
  - Keep numeric fields as numeric; do not replace missing aggregate values with 0 (they should remain missing/blank in the output).
  - Round `Average Rating` to **9 decimal places** and output with zero-padded precision.
  - For text fields in the final output, represent missing values as empty strings.

- Output the data.

## Output

- output_01.csv
  - 38 fields:
    - Book ID
    - Sale Date
    - ISBN
    - Discount
    - ItemID
    - OrderID
    - First Name
    - Last Name
    - Birthday
    - Country of Residence
    - Hrs Writing per Day
    - Title
    - AuthID
    - Format
    - PubID
    - Publication Date
    - Pages
    - Print Run Size (k)
    - Price
    - Publishing House
    - City
    - State
    - Country
    - Year Established
    - Marketing Spend
    - Number of Awards Won (avg only)
    - Number of Months Checked Out
    - Total Checkouts
    - Genre
    - SeriesID
    - Volume Number
    - Staff Comment
    - Series Name
    - Planned Volumes
    - Book Tour Events
    - Average Rating
    - Number of Reviewers
    - Number of Reviews
  - Sale Date, Birthday, and Publication Date must be formatted exactly as `DD/MM/YYYY` (zero-padded); blank if missing.
  - The following fields must be integer strings with no decimals; blank if missing: Pages, Print Run Size (k), Year Established, Marketing Spend, Number of Awards Won (avg only), Number of Months Checked Out, Total Checkouts, Volume Number, Planned Volumes, Book Tour Events, Number of Reviewers, Number of Reviews.
