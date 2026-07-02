from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd


ORDER_PATTERNS: List[str] = [
    r"(?:\bON\b|ON:|Order|ORD|\bO\b)\s*[:=#-]?\s*(\d{3,})",
    r"#\s*(\d{5,})",
]
CUSTOMER_PATTERNS: List[str] = [
    r"(?:Cust(?:omer)?|CID|Customer|Cust)\s*[:=#-]?\s*(\d+)",
    r"\bC\b\s*[:=#-]?\s*(\d+)",
    r"\bID\b\s*[:=#-]?\s*(\d+)",
]
ITEM_PATTERNS: List[str] = [
    r"(?:Item|IN|I)\s*[:=#-]?\s*(\d{1,2})",
    r"#\s*(\d{1,2})(?!\d)",
]


def _parse_complaint(text: str) -> Tuple[int, int, int]:
    digits = re.findall(r"\d+", text)
    remaining = digits.copy()

    def pop_token(token: str | None):
        if token is None:
            return
        for idx, value in enumerate(remaining):
            if value == token:
                remaining.pop(idx)
                return

    def pick_by_patterns(patterns: List[str]) -> str | None:
        for pat in patterns:
            match = re.search(pat, text, flags=re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    order_token = pick_by_patterns(ORDER_PATTERNS)
    if order_token is None:
        for token in remaining:
            if len(token) >= 5:
                order_token = token
                break
    if order_token is None:
        raise ValueError(f"无法解析订单号：{text}")
    pop_token(order_token)
    order_number = int(order_token)

    customer_token = pick_by_patterns(CUSTOMER_PATTERNS)
    if customer_token is None:
        for token in remaining:
            if len(token) >= 3:
                customer_token = token
                break
    if customer_token is None:
        for token in remaining:
            if len(token) >= 2:
                customer_token = token
                break
    if customer_token is None:
        if remaining:
            customer_token = remaining[0]
        else:
            raise ValueError(f"无法解析客户号：{text}")
    pop_token(customer_token)
    customer_id = int(customer_token)

    item_token = pick_by_patterns(ITEM_PATTERNS)
    if item_token is None:
        for token in reversed(remaining):
            if len(token) <= 2:
                item_token = token
                break
    if item_token is None:
        if remaining:
            item_token = remaining[-1]
        else:
            raise ValueError(f"无法解析商品项号：{text}")
    item_number = int(item_token)

    return order_number, customer_id, item_number


def _parse_complaints(df: pd.DataFrame) -> pd.DataFrame:
    parsed = [_parse_complaint(text) for text in df["Complaint"]]
    out = pd.DataFrame(
        parsed, columns=["Order Number", "Customer ID", "Item Number"])
    out = out.drop_duplicates(
        subset=["Order Number", "Item Number"]).reset_index(drop=True)
    return out


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    orders = pd.read_csv(inputs_dir / "input_01.csv")
    batches = pd.read_csv(inputs_dir / "input_02.csv")
    complaints_raw = pd.read_csv(inputs_dir / "input_03.csv", dtype=str)

    orders["Scent"] = orders["Scent"].fillna("N/A")
    batches["Scent"] = batches["Scent"].fillna("N/A")

    orders["Order Number"] = orders["Order Number"].astype(int)
    orders["Batch Number"] = orders["Batch Number"].astype(int)
    orders["Customer ID"] = orders["Customer ID"].astype(int)
    orders["Item Number"] = orders["Item Number"].astype(int)
    orders["Price"] = orders["Price"].astype(float)

    batches["Batch Number"] = batches["Batch Number"].astype(int)
    batches["Size of Order"] = batches["Size of Order"].astype(int)

    complaints = _parse_complaints(complaints_raw)

    complaint_details = complaints.merge(
        orders,
        on=["Order Number", "Customer ID", "Item Number"],
        how="left",
        suffixes=("", "_order"),
    )
    if complaint_details["Batch Number"].isna().any():
        missing = complaint_details.loc[
            complaint_details["Batch Number"].isna(
            ), ["Order Number", "Item Number"]
        ]
        raise ValueError(f"存在无法匹配的投诉记录：{missing.to_dict('records')}")

    ambiguous_orders = (
        orders.groupby("Order Number")["Customer ID"].nunique()
    )
    ambiguous_orders = set(ambiguous_orders[ambiguous_orders > 1].index)
    complaint_details["is_ambiguous"] = complaint_details["Order Number"].isin(
        ambiguous_orders
    )

    batch_sold = orders.groupby("Batch Number")[
        "Order Number"].size().rename("sold_qty")
    batch_complaints = complaint_details.groupby("Batch Number")["Order Number"].size().rename(
        "complaint_qty"
    )

    price_per_product = orders.groupby("Product")["Price"].agg("nunique")
    if (price_per_product != 1).any():
        raise ValueError("同一产品存在多种价格，无法确定批次单价")
    price_per_product = orders.groupby("Product")["Price"].agg("first")

    batch_stats = batches.merge(
        batch_sold, on="Batch Number", how="left"
    ).merge(batch_complaints, on="Batch Number", how="left")
    batch_stats["sold_qty"] = batch_stats["sold_qty"].fillna(0).astype(int)
    batch_stats["complaint_qty"] = batch_stats["complaint_qty"].fillna(
        0).astype(int)
    batch_stats["unit_price"] = batch_stats["Product"].map(price_per_product)
    batch_stats["complaint_rate"] = 0.0
    mask = batch_stats["sold_qty"] > 0
    batch_stats.loc[mask, "complaint_rate"] = (
        batch_stats.loc[mask, "complaint_qty"] /
        batch_stats.loc[mask, "sold_qty"]
    )
    batch_stats["recall"] = batch_stats["complaint_rate"] > 0.2

    batch_stats["recall_loss"] = 0.0
    recall_mask = batch_stats["recall"]
    batch_stats.loc[recall_mask, "recall_loss"] = (
        batch_stats.loc[recall_mask, "Size of Order"] *
        batch_stats.loc[recall_mask, "unit_price"]
    )
    recall_total = round(float(batch_stats["recall_loss"].sum()), 2)

    complaint_with_flags = complaint_details.merge(
        batch_stats[["Batch Number", "recall"]], on="Batch Number", how="left"
    )
    refund_rows = complaint_with_flags[
        (~complaint_with_flags["recall"]
         ) | complaint_with_flags["is_ambiguous"]
    ]
    refund_total = round(float(refund_rows["Price"].sum()), 2)
    total_loss = round(recall_total + refund_total, 2)

    refund_summary = pd.DataFrame(
        {
            "Type of Refund": ["Recall Whole Batch", "Refund Items Only", "Total Amount Lost"],
            "Money Lost": [recall_total, refund_total, total_loss],
        }
    )

    batch_stats["stock_remaining"] = batch_stats["Size of Order"] - \
        batch_stats["sold_qty"]
    batch_stats.loc[batch_stats["recall"], "stock_remaining"] = 0
    stock_remaining = (
        batch_stats.groupby(["Product", "Scent"], as_index=False)[
            "stock_remaining"].sum()
    )
    ambiguous_recall = complaint_with_flags[
        complaint_with_flags["is_ambiguous"] & complaint_with_flags["recall"]
    ]
    if not ambiguous_recall.empty:
        adjust = (
            ambiguous_recall.groupby(["Product", "Scent"])
            .size()
            .reset_index(name="ambiguous_count")
        )
        stock_remaining = stock_remaining.merge(
            adjust, on=["Product", "Scent"], how="left"
        )
        stock_remaining["ambiguous_count"] = (
            stock_remaining["ambiguous_count"].fillna(0).astype(int)
        )
        stock_remaining["stock_remaining"] = (
            stock_remaining["stock_remaining"] -
            stock_remaining["ambiguous_count"]
        ).clip(lower=0)
        stock_remaining = stock_remaining.drop(columns=["ambiguous_count"])
    stock_remaining.rename(
        columns={"stock_remaining": "Stock Remaining"}, inplace=True)
    stock_remaining["Stock Remaining"] = stock_remaining["Stock Remaining"].astype(
        int)
    stock_remaining = stock_remaining.sort_values(
        ["Product", "Scent"]).reset_index(drop=True)

    return {
        "output_01.csv": refund_summary,
        "output_02.csv": stock_remaining,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for filename, df in results.items():
        output_path = cand_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False, encoding="utf-8")
