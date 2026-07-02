import pandas as pd
from pathlib import Path
from typing import Optional
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    position_list = pd.read_csv(inputs_dir / "input_01.csv")
    player_list_raw = pd.read_csv(inputs_dir / "input_02.csv")

    raw = pd.read_csv(inputs_dir / "input_03.csv", header=None)
    header_idx = None
    for i in range(len(raw)):
        if str(raw.iloc[i, 0]).strip() == "No.":
            header_idx = i
            break
    if header_idx is None:
        raise RuntimeError("未找到表头行 'No.'，无法解析 input_03.csv")

    header = raw.iloc[header_idx].astype(str).tolist()
    data = raw.iloc[header_idx + 1:].copy()
    data.columns = header
    lineup = data.reset_index(drop=True)
    lineup.columns = [str(c).strip() for c in lineup.columns]

    def parse_result(row):
        result_str = row.get("Result")
        location = row.get("Location")
        if pd.isna(result_str) or result_str == "":
            return (0, 0)
        parts = str(result_str).split("-", 1)
        if len(parts) != 2:
            return (0, 0)
        a = int(parts[0])
        b = int(parts[1])
        if location == "H":
            return (a, b)
        return (b, a)

    goals = lineup.apply(parse_result, axis=1)
    lineup["Liverpool Goals"] = goals.apply(lambda x: x[0])
    lineup["Opposition Goals"] = goals.apply(lambda x: x[1])

    out1 = (
        lineup.groupby(["Formation", "Oppo Form."])
        .agg({
            "No.": "count",
            "Liverpool Goals": "sum",
            "Opposition Goals": "sum",
        })
        .reset_index()
    )
    out1.columns = [
        "Formation",
        "Oppo Form.",
        "Games Played",
        "Liverpool Goals",
        "Opposition Goals",
    ]
    out1["Avg Goals Scored"] = out1["Liverpool Goals"] / out1["Games Played"]
    out1["Avg Goals Conceded"] = out1["Opposition Goals"] / out1["Games Played"]
    out1 = out1[
        [
            "Formation",
            "Oppo Form.",
            "Games Played",
            "Liverpool Goals",
            "Avg Goals Scored",
            "Opposition Goals",
            "Avg Goals Conceded",
        ]
    ]
    out1.columns = [
        " Formation",
        "Oppo Form.",
        "Games Played",
        "Liverpool Goals",
        "Avg Goals Scored",
        "Opposition Goals",
        "Avg Goals Conceded",
    ]

    def clean_player_name(name_str: str):
        if pd.isna(name_str):
            return None, None
        s = str(name_str).strip()
        s = s.replace("\u00A0", " ")
        m = re.match(r"\d+\s*([^()]+?)\s*\(([GDMA])\)", s)
        if not m:
            return None, None
        player = m.group(1).strip()
        code = m.group(2)
        typ = {"G": "Goalkeeper", "D": "Defender", "M": "Midfielder", "A": "Attacker"}[code]
        return player, typ

    rows = []
    for _, r in player_list_raw.iterrows():
        p, t = clean_player_name(r.get("Player Name"))
        if p:
            rows.append({"Player Name": p, "Preferred Position Type": t})
    player_list = pd.DataFrame(rows)

    pos_map = {}
    for _, r in position_list.iterrows():
        pos_map[(str(r["Formation Name"]).strip(), int(r["Player Position"]))] = (
            str(r["Position Name"]).strip(),
            str(r["Position Type"]).strip(),
        )

    def map_player(short_name: str) -> Optional[str]:
        if pd.isna(short_name):
            return None
        s = str(short_name).strip()
        if not s:
            return None
        hit = player_list[player_list["Player Name"] == s]
        if len(hit) > 0:
            return hit.iloc[0]["Player Name"]
        sl = s.lower()
        best = None
        best_len = 0
        for _, rr in player_list.iterrows():
            fn = rr["Player Name"]
            if sl in fn.lower() and len(s) > best_len:
                best = fn
                best_len = len(s)
        return best or s

    cols = list(lineup.columns)
    sub_positions = {}
    for idx, c in enumerate(cols):
        if c in {"sub1", "sub2", "sub3"}:
            sub_positions[c] = idx

    records: list[dict] = []

    for _, match in lineup.iterrows():
        formation = str(match.get("Formation")).strip()
        mno = match.get("No.")
        try:
            mnum = int(float(mno))
        except Exception:
            mnum = None
        match_len = 90

        player_segments = {}

        for pos in range(1, 12):
            col = str(pos)
            if col in match.index and pd.notna(match[col]) and str(match[col]).strip() != "":
                player = map_player(match[col])
                key = (formation, pos)
                if key in pos_map:
                    pname, ptype = pos_map[key]
                    seg_key = (player, pname, ptype)
                    if seg_key not in player_segments:
                        player_segments[seg_key] = []
                    player_segments[seg_key].append([0, match_len])

        for subk in ["sub1", "sub2", "sub3"]:
            if subk not in sub_positions:
                continue
            idx = sub_positions[subk]
            try:
                off_pos_raw = match.iloc[idx]
                on_no_raw = match.iloc[idx + 1] if idx + 1 < len(match) else None
                minute_raw = match.iloc[idx + 2] if idx + 2 < len(match) else None

                off_pos = int(float(off_pos_raw)) if pd.notna(off_pos_raw) and str(off_pos_raw).strip() != "" else None
                on_no = str(int(float(on_no_raw))) if pd.notna(on_no_raw) and str(on_no_raw).strip() != "" else None
                sub_time = float(minute_raw) if pd.notna(minute_raw) and str(minute_raw).strip() != "" else None
            except Exception:
                off_pos, on_no, sub_time = None, None, None

            if off_pos is None or on_no is None or sub_time is None:
                continue

            off_col = str(off_pos)
            if off_col in match.index and pd.notna(match[off_col]) and str(match[off_col]).strip() != "":
                off_player = map_player(match[off_col])
                key = (formation, off_pos)
                if key in pos_map:
                    pname, ptype = pos_map[key]
                    seg_key = (off_player, pname, ptype)
                    if seg_key in player_segments:
                        for seg in player_segments[seg_key]:
                            if seg[1] == match_len:
                                seg[1] = min(sub_time, match_len)
                                break

            sub_player = None
            if on_no in match.index and pd.notna(match[on_no]) and str(match[on_no]).strip() != "":
                sub_player = map_player(match[on_no])

            if sub_player is not None:
                key = (formation, off_pos)
                if key in pos_map:
                    pname, ptype = pos_map[key]
                    seg_key = (sub_player, pname, ptype)
                    if seg_key not in player_segments:
                        player_segments[seg_key] = []
                    player_segments[seg_key].append([sub_time, match_len])

        for (player, pname, ptype), segs in player_segments.items():
            total_mins = sum(max(0, seg[1] - seg[0]) for seg in segs)
            records.append({
                "Match No": mnum,
                "Player Name": player,
                "Position Name": pname,
                "Position Type": ptype,
                "Mins Played": int(round(total_mins)),
            })

    rec_df = pd.DataFrame(records)

    rec_df = rec_df.merge(player_list, on="Player Name", how="left")

    out2_grp = (
        rec_df.groupby(["Player Name", "Position Type", "Position Name"], dropna=False)
        .agg({"Match No": "count", "Mins Played": "sum"})
        .reset_index()
    )
    out2_grp.columns = [
        "Player Name",
        "Position Type",
        "Position Name",
        "No Times Played",
        "Mins Played",
    ]

    rec_df["Is OoP"] = rec_df["Position Type"] != rec_df["Preferred Position Type"]
    oop_by_player_pos = (
        rec_df[rec_df["Is OoP"]]
        .groupby(["Player Name", "Position Type", "Position Name"])
        .size()
        .reset_index(name="Games OoP")
    )

    out2 = out2_grp.merge(oop_by_player_pos, on=["Player Name", "Position Type", "Position Name"], how="left")
    out2["Games OoP"] = out2["Games OoP"].fillna(0).astype(int)

    player_oop_total = (
        rec_df[rec_df["Is OoP"]]
        .drop_duplicates(["Player Name", "Match No"])
        .groupby("Player Name")
        .size()
        .reset_index(name="Total OoP")
    )
    out2 = out2.merge(player_oop_total, on="Player Name", how="left")
    out2["Games OoP"] = out2["Total OoP"].fillna(0).astype(int)
    out2 = out2.drop(columns=["Total OoP"])

    out2["Player Name"] = out2["Player Name"].astype(str) + " "

    out2 = out2[
        [
            "Player Name",
            "Position Type",
            "Position Name",
            "No Times Played",
            "Mins Played",
            "Games OoP",
        ]
    ]

    return {"output_01.csv": out1, "output_02.csv": out2}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).write_text("", encoding="utf-8")
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
