from __future__ import annotations
from pathlib import Path
import pandas as pd
import re
from typing import Dict

INCH_TO_CM = 2.54


def _parse_size_label(label: str) -> tuple[float, float]:
    s = str(label).strip()
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*cm\s*2\s*", s, flags=re.IGNORECASE)
    if m:
        v = float(m.group(1))
        return (v, v) if v >= v else (v, v)

    m = re.fullmatch(
        r"\s*(\d+(?:\.\d+)?)\s*cm\s*x\s*(\d+(?:\.\d+)?)\s*cm\s*", s, flags=re.IGNORECASE)
    if m:
        a = float(m.group(1))
        b = float(m.group(2))
        return (max(a, b), min(a, b))

    m = re.fullmatch(
        r"\s*(\d+(?:\.\d+)?)\s*\"\s*x\s*(\d+(?:\.\d+)?)\s*\"\s*", s)
    if m:
        a_in = float(m.group(1))
        b_in = float(m.group(2))
        a = a_in * INCH_TO_CM
        b = b_in * INCH_TO_CM
        return (max(a, b), min(a, b))

    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*\"\s*2\s*", s)
    if m:
        v = float(m.group(1)) * INCH_TO_CM
        return (v, v)

    raise ValueError(f"Unrecognized size format: {label}")


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    frames_path = inputs_dir / "input_01.csv"
    pics_path = inputs_dir / "input_02.csv"

    df_frames = pd.read_csv(frames_path)
    df_pics = pd.read_csv(pics_path)

    frame_records = []
    for _, row in df_frames.iterrows():
        label = str(row["Size"])
        max_cm, min_cm = _parse_size_label(label)
        area = max_cm * min_cm
        frame_records.append({
            "FrameLabel": label.strip(),
            "F_Max": max_cm,
            "F_Min": min_cm,
            "F_Area": area,
            "Order": _,
        })
    frames_norm = pd.DataFrame(frame_records)

    pic_records = []
    for _, row in df_pics.iterrows():
        pic = str(row["Picture"]).strip()
        size_label = str(row["Size"]).strip()
        p_max, p_min = _parse_size_label(size_label)
        pic_records.append({
            "Picture": pic,
            "P_Max": p_max,
            "P_Min": p_min,
            "P_Area": p_max * p_min,
            "PicOrder": _,
        })
    pics_norm = pd.DataFrame(pic_records)

    out_rows = []
    for _, pic in pics_norm.sort_values("PicOrder").iterrows():
        P_Max, P_Min, P_Area = pic["P_Max"], pic["P_Min"], pic["P_Area"]
        candidates = frames_norm[(frames_norm["F_Max"] >= P_Max) & (
            frames_norm["F_Min"] >= P_Min)].copy()
        candidates["Excess"] = candidates["F_Area"] - P_Area
        candidates = candidates[candidates["Excess"] >= 0]
        if candidates.empty:
            chosen_label = None
        else:
            candidates = candidates.sort_values(
                ["Excess", "Order"], ascending=[True, True])
            chosen_label = candidates.iloc[0]["FrameLabel"]
        out_rows.append({
            "Picture": pic["Picture"],
            "Frame": chosen_label,
            "Max Side": int(round(P_Max)),
            "Min Side": int(round(P_Min)),
        })

    out_df = pd.DataFrame(
        out_rows, columns=["Picture", "Frame", "Max Side", "Min Side"])

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).write_text("", encoding="utf-8")
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
