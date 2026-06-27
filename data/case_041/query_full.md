## Context
Chin & Beard Suds Co has received customer complaints about recently shipped items and has implemented a policy to either refund individual complained-about items or, when complaints are sufficiently concentrated, recall an entire production batch. You need to quantify the financial impact under this policy (refunds only, whole-batch recalls, and the combined total) and determine updated on-hand stock levels after applying refunds and recalls. Complaint records are free-text and must be parsed to identify the affected order, customer, and item.

## Requirements
- Input the data.
  - Use three inputs:
    - **Orders** (input_01.csv): order line items including at least Order Number, Customer ID, Item Number, Batch Number, Product, Scent, and Price.
    - **Batches** (input_02.csv): batch purchase information including at least Batch Number, Product, Scent, and Size of Order (the total units acquired for the batch).
    - **Complaints** (input_03.csv): a column named Complaint containing free-text complaint strings.
  - Treat missing/blank Scent values in both the orders and batches inputs as the literal value **"N/A"** for downstream grouping/reporting.

- Parse out the order number, customer number and item number from each complaint.
  - For each complaint text, extract exactly three integers: **Order Number**, **Customer ID**, and **Item Number**.
  - **Parsing rules** (apply in order, removing matched tokens from consideration after each step):
    - **Order Number extraction**:
      - First, attempt to match using explicit markers (case-insensitive): patterns matching "ON", "ON:", "Order", "ORD", or "O" followed by optional separators (":", "=", "#", "-") and digits; or "#" followed by 5+ digits.
      - If no marker match is found, select the first digit sequence with length >= 5 from all remaining digits in the text.
      - If no Order Number can be identified, the process must fail for that complaint.
    - **Customer ID extraction**:
      - First, attempt to match using explicit markers (case-insensitive): patterns matching "Cust", "Customer", "CID", "Cust No", or "C" followed by optional separators (":", "=", "#", "-") and digits; or "ID" followed by optional separators and digits.
      - If no marker match is found, select the first digit sequence with length >= 3 from remaining digits.
      - If still not found, select the first digit sequence with length >= 2 from remaining digits.
      - If still not found, select the first remaining digit sequence.
      - If no Customer ID can be identified, the process must fail for that complaint.
    - **Item Number extraction**:
      - First, attempt to match using explicit markers (case-insensitive): patterns matching "Item", "IN", or "I" followed by optional separators (":", "=", "#", "-") and 1-2 digits; or "#" followed by 1-2 digits (not followed by another digit).
      - If no marker match is found, scan remaining digits from right to left and select the first digit sequence with length <= 2.
      - If still not found, select the last remaining digit sequence.
      - If no Item Number can be identified, the process must fail for that complaint.
  - **Data normalization**: After extraction, convert all three integers by removing leading zeros (e.g., "00673" → 673, "01256" → 1256) to ensure matching with the orders data.
  - After parsing, remove duplicate complaint records at the grain of **(Order Number, Item Number)** (i.e., keep only one complaint per order/item combination).

- Work out which orders have received a complaint.
  - Join the parsed complaints to the orders data using an exact match on **Order Number + Customer ID + Item Number** (left join of complaints to orders).
  - If any parsed complaint does not match a corresponding order line, the process must fail (do not silently drop or impute unmatched complaints).

- Calculate how much money we have lost from refunds alone, recalling entire orders (20% of items of a product complained about and the loss is on the entire batch whether sold or not) and the total sum:
  - Calculate the % of ordered items from a batch which have received a complaint.
    - Define, per **Batch Number**:
      - **sold_qty** = count of order line items in Orders for that batch.
      - **complaint_qty** = count of matched complaint line items for that batch.
      - **complaint_rate** = complaint_qty / sold_qty when sold_qty > 0; otherwise 0.
  - If this is above 20%, then we will class the whole batch as refunded and therefore lose out on money from all ordered items, and the remaining unordered stock.
    - A batch is **recalled** when **complaint_rate > 0.20** (strictly greater than 20%).
    - Determine a single **unit price per Product** from the orders data; if a product appears with more than one distinct Price in the orders data, the process must fail (unit price is not uniquely defined).
    - For each recalled batch, compute **recall loss** as:
      - recall_loss = (Size of Order) * (unit price for that Product)
    - **Recall Whole Batch** money lost is the sum of recall_loss across all recalled batches, rounded to 2 decimals.
  - If the % of ordered items from a batch is less than 20%, then we will just refund the items which we have received complaints on.
    - **Refund Items Only** money lost is the sum of Price across complaint-matched order lines that are **not** in a recalled batch.
    - Additionally, if an **Order Number** is associated with more than one distinct Customer ID in the orders data (an “ambiguous” order), then complaint lines from that order are treated as **Refund Items Only** even if their batch is recalled.
    - Round the Refund Items Only total to 2 decimals.
  - Compute **Total Amount Lost** as (Recall Whole Batch + Refund Items Only), rounded to 2 decimals.
  - The refund/loss output must contain exactly three categories with these exact labels:
    - Recall Whole Batch
    - Refund Items Only
    - Total Amount Lost

- Work out how much stock we have remaining after all our orders, refunds and stock recalls.
  - Compute remaining stock at the **batch** level first:
    - stock_remaining = (Size of Order) − sold_qty
    - If the batch is recalled, set stock_remaining to 0 (all stock in the batch is removed from availability).
  - Aggregate stock to the reporting level of **(Product, Scent)** by summing batch-level stock_remaining.
  - Adjustment for ambiguous-order complaints in recalled batches:
    - For complaint lines that are both (a) from an ambiguous order and (b) belong to a recalled batch, subtract the count of such complaint lines from Stock Remaining for the corresponding (Product, Scent).
    - Do not allow Stock Remaining to go below 0 after this adjustment.
  - Output Stock Remaining as an integer.
  - Sort the final stock output by Product ascending, then Scent ascending.

- Output the data.

## Output

- output_01.csv
  - 2 fields:
    - Type of Refund
    - Money Lost

- output_02.csv
  - 3 fields:
    - Product
    - Scent
    - Stock Remaining