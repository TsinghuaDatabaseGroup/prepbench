from pathlib import Path
import pandas as pd
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    def parse_price(x: str) -> float:
        if pd.isna(x):
            return float("nan")
        return float(re.sub(r"[,$]", "", str(x)).replace("$", ""))

    files = sorted(inputs_dir.glob("input_*.csv"), key=lambda p: p.name)
    frames: list[pd.DataFrame] = []
    for f in files:
        m = re.search(r"input_(\d+)\.csv$", f.name)
        month_no = int(m.group(1)) if m else 0
        df = pd.read_csv(f, dtype=str)
        df["__row"] = range(1, len(df) + 1)
        df["__file"] = f.name
        df["__month"] = month_no
        frames.append(df)

    df = pd.concat(frames, ignore_index=True)

    df["Sector"] = df["Sector"].astype(str).str.strip().replace(
        {"nan": None, "NaN": None, "": None, "n/a": None, "N/A": None})
    df["id"] = df["id"].astype(int)
    df["Purchase Price"] = df["Purchase Price"].map(parse_price)

    df = df.sort_values(["__month", "id"], kind="mergesort").copy()
    df["Trade Order"] = df.groupby("Sector", dropna=False).cumcount() + 1

    df_keep = df[["Sector", "Trade Order", "Purchase Price"]].copy()

    df_keep["Rolling Avg. Purchase Price"] = (
        df_keep.groupby("Sector", dropna=False)["Purchase Price"]
        .rolling(window=3, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
        .round(2)
    )

    counts = df_keep.groupby("Sector", dropna=False).size()
    valid_labels = [label for label in counts.index if pd.notna(
        label) and counts[label] >= 100]
    mask = df_keep["Sector"].isin(valid_labels)
    if df_keep["Sector"].isna().sum() >= 100:
        mask = mask | df_keep["Sector"].isna()
    df_keep = df_keep[mask]

    groups: list[pd.DataFrame] = []
    for _, g in df_keep.groupby("Sector", dropna=False, sort=False):
        g = g.sort_values("Trade Order", kind="mergesort")
        if len(g) > 100:
            g = g.iloc[-100:].copy()
        else:
            g = g.copy()
        g["Previous Trades"] = range(1, len(g) + 1)
        groups.append(g)

    out = pd.concat(groups, ignore_index=True)[
        ["Previous Trades", "Trade Order", "Sector", "Rolling Avg. Purchase Price"]
    ]

    out = (
        out.sort_values(["Sector", "Previous Trades"], kind="mergesort")
        .reset_index(drop=True)
    )

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
