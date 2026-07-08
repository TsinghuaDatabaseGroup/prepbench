from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd

MEASURE_SPECS: Dict[tuple[str, str], dict[str, object]] = {
    ("Orders", "% Shipped in 3 days"): {
        "measure": "% Orders Shipped in 3 days",
        "is_percent": True,
    },
    ("Orders", "% Shipped in 5 days"): {
        "measure": "% Orders Shipped in 5 days",
        "is_percent": True,
    },
    ("Returns", "% Processed in 3 days"): {
        "measure": "% Returns Processed in 3 days",
        "is_percent": True,
    },
    ("Returns", "% Processed in 5 days"): {
        "measure": "% Returns Processed in 5 days",
        "is_percent": True,
    },
    ("Complaints", "# Received"): {
        "measure": "# Complaints Received",
        "is_percent": False,
    },
}

SHOP_FILE_MAP: Dict[str, str] = {
    "input_01.csv": "Bath",
    "input_02.csv": "Bristol",
    "input_03.csv": "Exmouth",
    "input_04.csv": "Hastings",
    "input_05.csv": "Leicester",
    "input_06.csv": "Newcastle",
    "input_07.csv": "Nottingham",
    "input_08.csv": "Plymouth",
    "input_09.csv": "Portsmouth",
    "input_10.csv": "Reading",
    "input_11.csv": "Southampton",
    "input_12.csv": "Torquay",
}

SHOP_ORDER: List[str] = [
    "Leicester",
    "Bristol",
    "Plymouth",
    "Exmouth",
    "Nottingham",
    "Newcastle",
    "Southampton",
    "Hastings",
    "Bath",
    "Reading",
    "Torquay",
    "Portsmouth",
]

OUTPUT_COLUMNS: List[str] = [
    "Shop",
    "Date",
    "% Orders Shipped in 3 days",
    "Target - % Orders Shipped in 3 days",
    "% Orders Shipped in 5 days",
    "Target - % Orders Shipped in 5 days",
    "% Returns Processed in 3 days",
    "Target - % Returns Processed in 3 days",
    "% Returns Processed in 5 days",
    "Target - % Returns Processed in 5 days",
    "# Complaints Received",
    "Target - # Complaints Received",
]

PERCENT_COLUMNS = OUTPUT_COLUMNS[2:10]
COUNT_COLUMNS = OUTPUT_COLUMNS[10:]


def _parse_target(raw_value: object, is_percent: bool) -> float | None:
    if pd.isna(raw_value):
        return None
    text = str(raw_value).strip()
    if not text:
        return None
    text = text.replace(">", "").replace("%", "")
    try:
        value = float(text)
    except ValueError:
        return None
    if is_percent and value > 1:
        value /= 100
    return value


def _clean_source_frame(df: pd.DataFrame) -> pd.DataFrame:
    if "Department" not in df:
        return pd.DataFrame()

    df = df.copy()

    add_mask = df["Department"].astype(str).str.contains(
        "Additonal Metrics", case=False, na=False)
    if add_mask.any():
        df = df.loc[: add_mask.idxmax() - 1]

    df[["Department", "Target"]] = df[["Department", "Target"]].ffill()

    df = df.dropna(subset=["Breakdown"])
    df["Breakdown"] = (
        df["Breakdown"]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    df = df[df["Breakdown"].str.lower() != "breakdown"]

    df["Department"] = df["Department"].astype(str).str.strip()
    return df


def _extract_records(path: Path, shop: str) -> List[dict]:
    df = pd.read_csv(path, header=3)
    df = _clean_source_frame(df)
    if df.empty:
        return []

    date_columns: List[str] = []
    for column in df.columns:
        parsed = pd.to_datetime(column, errors="coerce")
        if pd.notna(parsed):
            date_columns.append(column)

    if not date_columns:
        return []

    melted = df[["Department", "Target", "Breakdown"] + date_columns].melt(
        id_vars=["Department", "Target", "Breakdown"],
        value_vars=date_columns,
        var_name="Date",
        value_name="Value",
    )
    melted["Date"] = pd.to_datetime(melted["Date"], errors="coerce")
    melted = melted.dropna(subset=["Date", "Value"])
    melted["Value"] = pd.to_numeric(melted["Value"], errors="coerce")
    melted = melted.dropna(subset=["Value"])

    records: List[dict] = []
    for _, row in melted.iterrows():
        key = (row["Department"], row["Breakdown"])
        spec = MEASURE_SPECS.get(key)
        if spec is None:
            continue
        measure_name = spec["measure"]
        is_percent = bool(spec["is_percent"])
        value = float(row["Value"])
        target_value = _parse_target(row["Target"], is_percent)

        records.append(
            {
                "Shop": shop,
                "Date": row["Date"],
                "Measure": measure_name,
                "Value": value,
            }
        )

        if target_value is not None:
            records.append(
                {
                    "Shop": shop,
                    "Date": row["Date"],
                    "Measure": f"Target - {measure_name}",
                    "Value": target_value,
                }
            )

    return records


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    records: List[dict] = []
    for file_name, shop in SHOP_FILE_MAP.items():
        csv_path = inputs_dir / file_name
        if not csv_path.exists():
            continue
        records.extend(_extract_records(csv_path, shop))

    long_df = pd.DataFrame(records)
    if long_df.empty:
        result = pd.DataFrame(columns=OUTPUT_COLUMNS)
        return {"output_01.csv": result}

    pivot = long_df.pivot_table(
        index=["Shop", "Date"],
        columns="Measure",
        values="Value",
        aggfunc="first",
    ).reset_index()
    pivot.columns.name = None

    shop_rank = {shop: idx for idx, shop in enumerate(SHOP_ORDER)}
    pivot["shop_order"] = pivot["Shop"].map(shop_rank)
    pivot = pivot.sort_values(["shop_order", "Date"]
                              ).drop(columns="shop_order")

    pivot["Date"] = pivot["Date"].dt.strftime("%d/%m/%Y")

    for column in PERCENT_COLUMNS:
        if column in pivot:
            pivot[column] = pivot[column].astype(float).round(2)

    for column in COUNT_COLUMNS:
        if column in pivot:
            pivot[column] = pivot[column].round().astype("Int64")

    pivot = pivot[OUTPUT_COLUMNS]
    return {"output_01.csv": pivot}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
