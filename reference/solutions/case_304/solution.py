from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    life_path = inputs_dir / "input_01.csv"
    map_path = inputs_dir / "input_02.csv"

    df_life_raw = pd.read_csv(life_path)
    df_map = pd.read_csv(map_path)

    life_cols = [c.lower() for c in df_life_raw.columns]
    if "period life expectancy at birth - sex: all - age: 0" in life_cols:
        life_col = df_life_raw.columns[life_cols.index(
            "period life expectancy at birth - sex: all - age: 0")]
    elif any("life expectancy" in c for c in life_cols):
        life_col = [
            c for c in df_life_raw.columns if "life expectancy" in c.lower()][0]
    else:
        raise ValueError("未找到寿命列（Life Expectancy）")

    life_df = df_life_raw.rename(columns={life_col: "Life expectancy at birth"})[
        ["Entity", "Year", "Life expectancy at birth"]
    ].copy()
    life_df = life_df.rename(columns={"Life expectancy at birth": "LE"})

    df_map = df_map.rename(columns={"Country": "Country", "Continent": "Continent"})[
        ["Country", "Continent"]].copy()

    country_life = df_map.merge(
        life_df, left_on="Country", right_on="Entity", how="inner")
    country_life = country_life.drop(columns=["Entity"])
    country_life = country_life.rename(
        columns={"LE": "Country: Life expectancy at birth"})

    continents = sorted(df_map["Continent"].dropna().unique().tolist())
    cont_life = life_df[life_df["Entity"].isin(continents)].copy()
    cont_life = cont_life.rename(
        columns={"Entity": "Continent", "LE": "Continent: Life expectancy at birth"})

    df = country_life.merge(
        cont_life[["Continent", "Year", "Continent: Life expectancy at birth"]],
        on=["Continent", "Year"], how="left"
    )

    df = df[(df["Year"] >= 1950) & (df["Year"] <= 2020)].copy()

    df["Above Continent Avg?"] = (df["Country: Life expectancy at birth"]
                                  > df["Continent: Life expectancy at birth"]).astype(int)

    pivot_1950 = df[df["Year"] == 1950][["Country", "Continent", "Country: Life expectancy at birth"]].rename(
        columns={"Country: Life expectancy at birth": "LE_1950"}
    )
    pivot_2020 = df[df["Year"] == 2020][["Country", "Continent", "Country: Life expectancy at birth"]].rename(
        columns={"Country: Life expectancy at birth": "LE_2020"}
    )
    growth = pivot_1950.merge(
        pivot_2020, on=["Continent", "Country"], how="inner")
    growth["% Change"] = ((growth["LE_2020"] - growth["LE_1950"])
                          * 100.0 / growth["LE_1950"]).round(1)

    years_stats = (
        df.groupby(["Continent", "Country"], as_index=False)
        .agg(**{
            "Number of Years Above Avg": ("Above Continent Avg?", "sum"),
            "Number of Rows (Aggregated)": ("Year", "count"),
        })
    )
    years_stats = years_stats.rename(
        columns={"Number of Rows (Aggregated)": "Number of Years"})
    years_stats["% Years Above Continent Avg"] = (
        100.0 * years_stats["Number of Years Above Avg"] / years_stats["Number of Years"]).round(1)

    result = growth.merge(
        years_stats[["Continent", "Country", "% Years Above Continent Avg"]],
        on=["Continent", "Country"], how="left"
    )
    result["% Years Above Continent Avg"] = result["% Years Above Continent Avg"].fillna(
        0.0)

    result = result.sort_values(
        ["Continent", "% Change", "Country"], ascending=[True, False, True])

    def add_rank(group: pd.DataFrame) -> pd.DataFrame:
        g = group.copy()
        g.insert(1, "Rank", range(1, len(g) + 1))
        return g.head(3)
    final = result.groupby("Continent", group_keys=False).apply(add_rank)

    final = final[[
        "Continent",
        "Rank",
        "Country",
        "% Years Above Continent Avg",
        "% Change",
    ]].copy()
    final["Rank"] = final["Rank"].astype(int)

    return {"output_01.csv": final}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
