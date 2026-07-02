from pathlib import Path
import pandas as pd
from datetime import datetime


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    all_files = sorted(inputs_dir.glob("input_*.csv"))
    dfs: list[pd.DataFrame] = []
    for f in all_files:
        df = pd.read_csv(f, dtype=str, encoding="utf-8")
        dfs.append(df)
    if dfs:
        df_all = pd.concat(dfs, ignore_index=True)
    else:
        df_all = pd.DataFrame(columns=[
                              "Tournament", "Date", "Series", "Round", "Winner", "Loser", "Comment"])

    use_cols = ["Tournament", "Date", "Series",
                "Round", "Winner", "Loser", "Comment"]
    df_all = df_all[use_cols].copy()

    def norm_name(x: str) -> str:
        if pd.isna(x):
            return x
        s = str(x).strip()
        s_low = s.lower()
        mapping = {
            "roger federer": "Federer R.",
            "federer roger": "Federer R.",
            "r. federer": "Federer R.",
            "federer r": "Federer R.",
            "federer r.": "Federer R.",
            "rafael nadal": "Nadal R.",
            "nadal rafael": "Nadal R.",
            "r. nadal": "Nadal R.",
            "nadal r": "Nadal R.",
            "nadal r.": "Nadal R.",
            "novak djokovic": "Djokovic N.",
            "djokovic novak": "Djokovic N.",
            "n. djokovic": "Djokovic N.",
            "djokovic n": "Djokovic N.",
            "djokovic n.": "Djokovic N.",
            "andy murray": "Murray A.",
            "murray andy": "Murray A.",
            "a. murray": "Murray A.",
            "murray a": "Murray A.",
            "murray a.": "Murray A.",
        }
        return mapping.get(s_low, s)

    df_all["Winner"] = df_all["Winner"].map(norm_name)
    df_all["Loser"] = df_all["Loser"].map(norm_name)

    ser = df_all["Series"].astype(str).str.strip()
    tnm = df_all["Tournament"].astype(str).str.strip()
    slam_names = {"Australian Open", "French Open", "Wimbledon", "US Open"}
    mask_series = ser.str.lower() == "grand slam"
    mask_tnm = tnm.isin(slam_names)
    df_all = df_all[mask_series | mask_tnm].copy()

    df_all["Date"] = pd.to_datetime(
        df_all["Date"], errors="coerce", dayfirst=False)
    df_all = df_all.dropna(subset=["Date"]).copy()

    players = ["Federer R.", "Murray A.", "Nadal R.", "Djokovic N."]
    df_all = df_all[(df_all["Winner"].isin(players)) |
                    (df_all["Loser"].isin(players))].copy()

    wins_blocks: list[pd.DataFrame] = []
    losses_blocks: list[pd.DataFrame] = []
    for p in players:
        pm = df_all[(df_all["Winner"] == p) | (df_all["Loser"] == p)].copy()
        if pm.empty:
            continue
        pm["Win/Loss"] = (pm["Winner"] == p).map({True: "Win", False: "Loss"})
        pm = pm.sort_values(["Date", "Tournament", "Round"],
                            kind="mergesort").reset_index(drop=True)
        wins_only = pm[pm["Win/Loss"] == "Win"].copy().head(200)
        if wins_only.empty:
            continue
        cutoff = wins_only.iloc[-1]["Date"]
        pm = pm[pm["Date"] <= cutoff].copy()
        pm["Win Number"] = pd.NA
        pm["Days Since Last Win"] = pd.NA
        last_win_dt = None
        win_no = 0
        for idx, row in pm.iterrows():
            if row["Win/Loss"] == "Win":
                win_no += 1
                pm.at[idx, "Win Number"] = win_no
                if last_win_dt is not None:
                    pm.at[idx, "Days Since Last Win"] = int(
                        (row["Date"] - last_win_dt).days)
                last_win_dt = row["Date"]
        pm["Player of Interest"] = p
        wins_blocks.append(pm[pm["Win/Loss"] == "Win"].copy())
        losses_blocks.append(pm[pm["Win/Loss"] == "Loss"].copy())

    order_map = {"Federer R.": 1, "Murray A.": 2,
                 "Nadal R.": 3, "Djokovic N.": 4}
    if wins_blocks:
        for i in range(len(wins_blocks)):
            wins_blocks[i]["_ord"] = wins_blocks[i]["Player of Interest"].map(
                order_map)
        wins_concat = pd.concat(
            sorted(wins_blocks, key=lambda d: d["_ord"].iloc[0]), ignore_index=True)
        wins_concat = wins_concat.drop(columns=["_ord"], errors="ignore")
    else:
        wins_concat = pd.DataFrame(columns=["Player of Interest", "Tournament", "Round", "Date",
                                            "Win/Loss", "Win Number", "Days Since Last Win", "Winner", "Loser", "Comment"])

    if losses_blocks:
        losses_concat = pd.concat(losses_blocks, ignore_index=True)
        losses_concat = losses_concat.sort_values(
            ["Date", "Tournament", "Round"], kind="mergesort").reset_index(drop=True)
    else:
        losses_concat = pd.DataFrame(columns=["Player of Interest", "Tournament", "Round", "Date",
                                              "Win/Loss", "Win Number", "Days Since Last Win", "Winner", "Loser", "Comment"])

    df_out = pd.concat([wins_concat, losses_concat], ignore_index=True)

    order_map = {"Federer R.": 1, "Murray A.": 2,
                 "Nadal R.": 3, "Djokovic N.": 4}
    if not df_out.empty:
        df_out["_ord"] = df_out["Player of Interest"].map(order_map)
        df_out = df_out.sort_values(["_ord", "Date"], kind="mergesort").drop(
            columns=["_ord"]).reset_index(drop=True)
        df_out["Date"] = df_out["Date"].dt.strftime("%d/%m/%Y")
        for c in ["Win Number", "Days Since Last Win"]:
            df_out[c] = pd.to_numeric(
                df_out[c], errors="coerce").astype("Int64")

    df_out = df_out[[
        "Player of Interest", "Tournament", "Round", "Date", "Win/Loss",
        "Win Number", "Days Since Last Win", "Winner", "Loser", "Comment"
    ]]

    return {"output_01.csv": df_out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
