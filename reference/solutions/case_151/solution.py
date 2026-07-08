from pathlib import Path
from typing import Dict
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    df_complaints = pd.read_csv(inputs_dir / "input_01.csv", dtype=str)
    df_keywords = pd.read_csv(inputs_dir / "input_02.csv", dtype=str)

    df_complaints = df_complaints[["Name", "Complaint"]].copy()
    df_keywords = df_keywords[["Keyword", "Department"]].copy()

    df_complaints["Complaint_lc"] = df_complaints["Complaint"].fillna("").str.strip().str.lower()

    kw_list = []
    for _, r in df_keywords.iterrows():
        kw = (r["Keyword"] or "").strip()
        dept = (r["Department"] or "").strip()
        if kw == "" or dept == "":
            continue
        kw_list.append({"kw": kw.lower(), "dept": dept})

    counts = df_complaints.groupby("Name").size().rename("Complaints per Person").to_dict()

    out_rows = []
    for _, row in df_complaints.iterrows():
        name = row["Name"]
        comp_lc = row["Complaint_lc"]

        matches = []
        for item in kw_list:
            pos = comp_lc.find(item["kw"]) if item["kw"] else -1
            if pos >= 0:
                matches.append((pos, item["kw"], item["dept"]))
        matches.sort(key=lambda x: x[0])

        if matches:
            dept_to_kws: Dict[str, list] = {}
            for _, kw, dept in matches:
                dept_to_kws.setdefault(dept, [])
                if kw not in dept_to_kws[dept]:
                    dept_to_kws[dept].append(kw)
            for dept, kws in dept_to_kws.items():
                out_rows.append({
                    "Complaint": comp_lc,
                    "Complaints per Person": int(counts.get(name, 0)),
                    "Complaint causes": ", ".join(kws),
                    "Department": dept if dept else "Unknown",
                    "Name": name,
                })
        else:
            out_rows.append({
                "Complaint": comp_lc,
                "Complaints per Person": int(counts.get(name, 0)),
                "Complaint causes": "other",
                "Department": "Unknown",
                "Name": name,
            })

    out_df = pd.DataFrame(out_rows, columns=[
        "Complaint",
        "Complaints per Person",
        "Complaint causes",
        "Department",
        "Name",
    ])

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

