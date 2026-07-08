from __future__ import annotations
from pathlib import Path
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    inp_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(inp_path)

    df = df[df["type"].isin(["TV", "Movie"])].copy()
    df = df[df["rating"].notna() & df["genre"].notna()].copy()
    df = df[df["members"] >= 10000].copy()

    df["genre"] = df["genre"].astype(str)
    df["genre"] = df["genre"].str.split(",")
    df = df.explode("genre")
    df["genre"] = df["genre"].str.strip()

    agg = (
        df.groupby(["genre", "type"], as_index=False)
        .agg(
            **{
                "Avg Rating": ("rating", "mean"),
                "Max Rating": ("rating", "max"),
                "Avg Viewers": ("members", "mean"),
            }
        )
    )

    def round_half_up_series(s: pd.Series, ndigits: int) -> pd.Series:
        quant = Decimal('1').scaleb(-ndigits)
        return s.apply(lambda v: float(Decimal(str(v)).quantize(quant, rounding=ROUND_HALF_UP)))

    agg["Avg Rating"] = round_half_up_series(agg["Avg Rating"], 2)
    agg["Max Rating"] = round_half_up_series(agg["Max Rating"], 2)
    agg["Avg Viewers"] = round_half_up_series(agg["Avg Viewers"], 0).astype(int)

    df_sorted = df.sort_values(by=["genre", "type", "rating", "members", "name"], ascending=[True, True, False, False, True])
    prime = df_sorted.groupby(["genre", "type"], as_index=False).first()[["genre", "type", "name", "rating"]]
    prime = prime.rename(columns={"name": "Prime Example", "rating": "Max Rating"})

    out = agg.merge(prime[["genre", "type", "Prime Example"]], on=["genre", "type"], how="left")

    out = out.rename(columns={
        "genre": "Genre",
        "type": "Type",
    })

    out = out[["Genre", "Type", "Avg Rating", "Max Rating", "Avg Viewers", "Prime Example"]]

    out = out.sort_values(by=["Genre", "Type", "Avg Rating", "Max Rating", "Avg Viewers", "Prime Example"]).reset_index(drop=True)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).write_text("", encoding="utf-8")
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
