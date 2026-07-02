from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve() -> Dict[str, pd.DataFrame]:
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    df_comp_map = pd.read_csv(inputs_dir / "input_01.csv")
    df_segments = pd.read_csv(inputs_dir / "input_02.csv")
    df_goals = pd.read_csv(inputs_dir / "input_03.csv")
    df_results = pd.read_csv(inputs_dir / "input_04.csv")

    df_goals["date"] = pd.to_datetime(df_goals["date"], errors="coerce")
    df_results["date"] = pd.to_datetime(df_results["date"], errors="coerce")

    ttext = df_results["tournament"].astype(str)
    qual_mask = ttext.str.contains("qualification", case=True, regex=True)
    non_fifa_mask = ttext.str.contains("CONIFA|Viva World Cup", case=False, regex=True)
    df_results = df_results.loc[~qual_mask & ~non_fifa_mask].copy()

    def map_competition(tournament: str) -> tuple[str | None, str | None]:
        if not isinstance(tournament, str):
            return None, None
        t = tournament.strip()
        low = t.lower()
        if "world cup" in low and "qualification" not in low:
            return "FIFA", "World Cup"
        if "copa am" in low:
            return "CONMEBOL", "Copa América"
        if ("uefa euro" in low) or ("european championship" in low):
            return "UEFA", "Euro"
        if ("africa cup of nations" in low) or ("african cup of nations" in low):
            return "CAF", "Africa Cup of Nations"
        if ("afc asian cup" in low) or ("asian cup" in low):
            return "AFC", "Asian Cup"
        if "oceania nations cup" in low:
            return "OFC", "Oceania Nations Cup"
        if ("concacaf gold cup" in low) or ("gold cup" in low) or ("concacaf championship" in low):
            return "CONCACAF", "Gold Cup"
        return None, None

    assoc_comp = df_results["tournament"].apply(map_competition)
    df_results["Football Association"] = assoc_comp.map(lambda x: x[0])
    df_results["Competition"] = assoc_comp.map(lambda x: x[1])

    valid_competitions = set(df_comp_map["Competition"].unique())
    df_results = df_results[df_results["Competition"].isin(valid_competitions)].copy()

    df_results["Year"] = df_results["date"].dt.year
    df_results = df_results[df_results["Year"] >= 1950].copy()
    df_results["Decade"] = (df_results["Year"] // 10) * 10

    df_results["Match ID"] = (
        df_results["date"].dt.strftime("%Y-%m-%d") + "|" + df_results["home_team"].astype(str) + "|" + df_results["away_team"].astype(str)
    )

    matches_decade = (
        df_results.groupby(["Competition", "Decade"], as_index=False)
        .agg(**{"Matches in a Decade per Competition": ("Match ID", "nunique")})
    )

    joined = df_goals.merge(
        df_results[[
            "date", "home_team", "away_team", "Competition", "Decade", "Match ID"
        ]],
        on=["date", "home_team", "away_team"],
        how="inner",
    )

    def minute_to_segment(m: object) -> str | None:
        try:
            val = int(m)
        except Exception:
            return None
        if val < 0:
            return None
        if val >= 90:
            return "90+"
        if val < 15:
            return "0-15"
        if val < 30:
            return "15-30"
        if val < 45:
            return "30-45"
        if val < 60:
            return "45-60"
        if val < 75:
            return "60-75"
        if val < 90:
            return "75-90"
        return None

    joined["Segment"] = joined["minute"].apply(minute_to_segment)
    joined = joined.dropna(subset=["Segment"]).copy()

    goals_agg = (
        joined.groupby(["Competition", "Decade", "Segment"], as_index=False)
        .size()
        .rename(columns={"size": "Total Goals"})
    )

    out = goals_agg.merge(matches_decade, on=["Competition", "Decade"], how="left")
    def div_and_round_half_up(num: int, den: int, ndigits: int = 2) -> float:
        import decimal
        if den == 0:
            return 0.0
        q = decimal.Decimal(10) ** -ndigits
        with decimal.localcontext() as ctx:
            ctx.rounding = decimal.ROUND_HALF_UP
            ctx.prec = 28
            val = (decimal.Decimal(int(num)) / decimal.Decimal(int(den))).quantize(q, rounding=decimal.ROUND_HALF_UP)
        return float(val)

    out["Expected number of Goals"] = [
        div_and_round_half_up(int(n), int(d)) for n, d in zip(out["Total Goals"], out["Matches in a Decade per Competition"]) 
    ]

    out = out[[
        "Competition",
        "Decade",
        "Segment",
        "Total Goals",
        "Matches in a Decade per Competition",
        "Expected number of Goals",
    ]].copy()

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve()
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


