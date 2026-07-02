from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    songs_fp = inputs_dir / "input_01.csv"
    cust_fp = inputs_dir / "input_02.csv"

    df_songs = pd.read_csv(songs_fp)
    df_cust = pd.read_csv(cust_fp, dtype={"Customer ID": str})

    df_songs["Date"] = pd.to_datetime(df_songs["Date"])

    df_songs = df_songs.sort_values("Date").reset_index(drop=True)
    df_songs["prev_date"] = df_songs["Date"].shift(1)
    df_songs["gap_min"] = (
        df_songs["Date"] - df_songs["prev_date"]).dt.total_seconds() / 60.0
    df_songs["new_session"] = df_songs["gap_min"].isna() | (
        df_songs["gap_min"] >= 59)
    df_songs["Session #"] = df_songs["new_session"].cumsum().astype(int)

    df_songs["Song Order"] = df_songs.groupby("Session #").cumcount() + 1

    sessions = (
        df_songs.groupby("Session #", as_index=False)["Date"]
        .min()
        .rename(columns={"Date": "session_start"})
        .sort_values("session_start")
        .reset_index(drop=True)
    )

    df_cust["Entry Time"] = pd.to_datetime(
        df_cust["Entry Time"])
    df_cust = df_cust.sort_values("Entry Time").reset_index(drop=True)

    matched = pd.merge_asof(
        sessions,
        df_cust,
        left_on="session_start",
        right_on="Entry Time",
        direction="backward",
        tolerance=pd.Timedelta(minutes=10),
        allow_exact_matches=True,
    )

    def fmt_id(x):
        if pd.isna(x):
            return ""
        s = str(x)
        if s.isdigit() and len(s) >= 7:
            try:
                return f"{int(s):.2E}"
            except Exception:
                return s
        return s

    matched["Customer ID"] = matched["Customer ID"].map(fmt_id)
    matched = matched[["Session #", "Customer ID"]]

    out_df = df_songs.merge(matched, on="Session #", how="left")
    out_df["Customer ID"] = out_df["Customer ID"].fillna("")

    out_df["Date"] = out_df["Date"].dt.round(
        "min").dt.strftime("%d/%m/%Y %H:%M:%S")
    out_df = out_df[["Session #", "Customer ID",
                     "Song Order", "Date", "Artist", "Song"]]
    out_df = out_df.sort_values(
        ["Session #", "Song Order"]).reset_index(drop=True)

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    out = solve(inputs_dir)
    for fname, df in out.items():
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
