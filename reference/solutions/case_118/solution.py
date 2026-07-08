from __future__ import annotations
from pathlib import Path
import re
import pandas as pd

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    main = pd.read_csv(inputs_dir / "input_01.csv")
    proj_lu = pd.read_csv(inputs_dir / "input_02.csv")
    subproj_lu = pd.read_csv(inputs_dir / "input_03.csv")
    task_lu = pd.read_csv(inputs_dir / "input_04.csv")
    name_lu = pd.read_csv(inputs_dir / "input_05.csv")

    proj_map = {str(k).strip().upper(): v for k, v in zip(proj_lu["Project Code"], proj_lu["Project"])}
    subproj_map = {str(k).strip().lower(): v for k, v in zip(subproj_lu["Sub-Project Code"], subproj_lu["Sub-Project"])}
    if "op" in subproj_map:
        subproj_map.setdefault("ops", subproj_map["op"])
    task_map = {str(k).strip().lower(): v for k, v in zip(task_lu["Task Code"], task_lu["Task"])}

    name_map = {str(k).strip().lower(): v for k, v in zip(name_lu["Abbreviation"], name_lu["Name"])}

    seg_pattern = re.compile(r"\[(?P<header>[^\]]+)\]\s*(?P<detail>.*?)(?=(\s*\[|$))")
    author_pattern = re.compile(r"\b(tom|jen|jon|car)\.", re.IGNORECASE)
    days_pattern = re.compile(r"(\d+)\s*day", re.IGNORECASE)

    records = []

    main_sorted = main.copy()
    main_sorted["Week"] = main_sorted["Week"].astype(int)
    main_sorted = main_sorted.sort_values("Week")

    for _, row in main_sorted.iterrows():
        week_num = int(row["Week"]) if pd.notna(row["Week"]) else None
        week_label = f"Week {week_num}" if week_num is not None else None
        commentary = str(row["Commentary"]) if pd.notna(row["Commentary"]) else ""

        for m in seg_pattern.finditer(commentary):
            header = m.group("header").strip()
            detail = m.group("detail").strip()

            proj_code = None
            sub_code = None
            task_code = None
            if "/" in header:
                left, right = header.split("/", 1)
                proj_code = left.strip().upper()
                if "-" in right:
                    sub_code, task_code = right.split("-", 1)
                else:
                    parts = right.split("-")
                    if len(parts) >= 2:
                        sub_code, task_code = parts[0], parts[1]
                    elif len(parts) == 1:
                        sub_code, task_code = parts[0], None
                sub_code = (sub_code or "").strip().lower()
                task_code = (task_code or "").strip().lower()
            else:
                continue

            project_full = proj_map.get(proj_code)
            subproject_full = subproj_map.get(sub_code)
            task_full = task_map.get(task_code)

            name_full = None
            name_abbrev = None
            last_match = None
            for am in author_pattern.finditer(detail):
                last_match = am
            if last_match is not None:
                name_abbrev = last_match.group(1).lower()
                name_full = name_map.get(name_abbrev)
            else:
                name_full = None

            days_noted = None
            dm = days_pattern.search(detail)
            if dm:
                try:
                    days_noted = int(dm.group(1))
                except Exception:
                    days_noted = None

            records.append({
                "Week": week_label,
                "Project": project_full,
                "Sub-Project": subproject_full,
                "Task": task_full,
                "Name": name_full,
                "Days Noted": days_noted,
                "Detail": detail.strip()
            })

    out_df = pd.DataFrame.from_records(records, columns=[
        "Week", "Project", "Sub-Project", "Task", "Name", "Days Noted", "Detail"
    ])

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    from pathlib import Path
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    result = solve(inputs_dir)
    for fname, df in result.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

