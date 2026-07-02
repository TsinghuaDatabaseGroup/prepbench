from pathlib import Path
from typing import Dict
import pandas as pd
import re


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    input1_path = inputs_dir / "input_01.csv"
    input2_path = inputs_dir / "input_02.csv"

    df = pd.read_csv(input1_path)
    df.columns = [c.strip() for c in df.columns]

    cfg = pd.read_csv(input2_path)
    cfg.columns = [c.strip() for c in cfg.columns]

    animal_terms_raw = []
    if "Animal Ingredients" in cfg.columns and not cfg["Animal Ingredients"].empty:
        for term in str(cfg.loc[0, "Animal Ingredients"]).split(","):
            t = term.strip()
            if t:
                animal_terms_raw.append(t)
    seen = set()
    animal_terms = []
    for t in animal_terms_raw:
        tl = t.lower()
        if tl not in seen:
            seen.add(tl)
            animal_terms.append(tl)

    desired_priority = [
        "milk", "whey", "lactose", "egg", "honey",
        "gelatin", "gelatine", "collagen", "elastin", "keratin",
        "pepsin", "isinglass", "shellac", "lard", "aspic", "beeswax"
    ]
    pri_index = {t: i for i, t in enumerate(desired_priority)}
    known = [t for t in animal_terms if t in pri_index]
    unknown = [t for t in animal_terms if t not in pri_index]
    known.sort(key=lambda x: pri_index[x])
    animal_terms = known + unknown

    e_numbers = []
    if "E Numbers" in cfg.columns and not cfg["E Numbers"].empty:
        for num in str(cfg.loc[0, "E Numbers"]).split(","):
            n = num.strip()
            if n:
                e_numbers.append(n)
    e_num_pattern = None
    if e_numbers:
        group = "|".join(map(re.escape, e_numbers))
        e_num_pattern = re.compile(rf"(?i)\bE?\s*(?:{group})\b")

    def extract_contains(text: str) -> list:
        s = (text or "")
        s_l = s.lower()
        found = set()
        for term in animal_terms:
            pattern = re.compile(
                rf"(?i)(?<![a-zA-Z]){re.escape(term)}(?![a-zA-Z])")
            if pattern.search(s_l):
                found.add(term)
        if ("gelatin" in found) or ("gelatine" in found):
            found.add("gelatin")
            found.add("gelatine")
        has_e = False
        if e_num_pattern is not None and e_num_pattern.search(s):
            has_e = True
        ordered = [t for t in animal_terms if t in found]
        return ordered, has_e

    non_vegan_rows = []
    vegan_rows = []

    for _, row in df.iterrows():
        desc = row.get("Description", None)
        ingred = row.get("Ingredients/Allergens", None)
        contains_list, has_e = extract_contains(str(ingred))
        if contains_list or has_e:
            non_vegan_rows.append({
                "Product": row["Product"],
                "Description": desc,
                "Contains": ", ".join(contains_list)
            })
        else:
            vegan_rows.append({
                "Product": row["Product"],
                "Description": desc
            })

    df_non = pd.DataFrame(non_vegan_rows, columns=["Product", "Description", "Contains"]) if non_vegan_rows else pd.DataFrame(
        columns=["Product", "Description", "Contains"])
    df_veg = pd.DataFrame(vegan_rows, columns=[
                          "Product", "Description"]) if vegan_rows else pd.DataFrame(columns=["Product", "Description"])

    outputs: Dict[str, pd.DataFrame] = {
        "output_01.csv": df_veg,
        "output_02.csv": df_non,
    }
    return outputs


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    out_map = solve(inputs_dir)
    for fname, df in out_map.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
