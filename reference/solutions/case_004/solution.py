from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")
    df["DATE"] = pd.to_datetime(df["DATE"])

    hoa = df["OPPONENT"].str.startswith(
        "vs").map({True: "Home", False: "Away"})

    opp_clean = df["OPPONENT"].str.replace(r"^(vs|@)\s*", "", regex=True)

    def split_pair(col: pd.Series):
        parts = col.str.rsplit(" ", n=1, expand=True)
        return parts[0], parts[1].astype(int)

    hp_player, hp_value = split_pair(df["HI POINTS"])
    hr_player, hr_value = split_pair(df["HI REBOUNDS"])
    ha_player, ha_value = split_pair(df["HI ASSISTS"])

    wol = df["RESULT"].str[0]

    out = pd.DataFrame({
        "Opponent (clean)": opp_clean,
        "HI ASSISTS - Player": ha_player,
        "HI ASSISTS - Value": ha_value,
        "HI REBOUNDS - Player": hr_player,
        "HI REBOUNDS - Value": hr_value,
        "HI POINTS - Player": hp_player,
        "HI POINTS - Value": hp_value,
        "Win or Loss": wol,
        "Home or Away": hoa,
        "True Date": df["DATE"].dt.strftime("%d/%m/%Y"),
        "OPPONENT": df["OPPONENT"],
        "RESULT": df["RESULT"],
    })

    order = df["DATE"].sort_values().index
    w_cum = (wol == "W").astype(int).loc[order].cumsum()
    l_cum = (wol == "L").astype(int).loc[order].cumsum()
    wl_text = (w_cum.astype(str) + "-" + l_cum.astype(str)).reindex(out.index)
    out["W-L"] = wl_text

    out_sorted = out.sort_values(by=["True Date"]).reset_index(drop=True)

    return {"output_01.csv": out_sorted}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    result = solve(inputs_dir)
    for fname, df in result.items():
        (cand_dir / fname).write_text("")
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
