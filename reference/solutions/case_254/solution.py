from pathlib import Path
import pandas as pd
from typing import Dict


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    names_df = pd.read_csv(inputs_dir / "input_01.csv")
    raw = pd.read_csv(inputs_dir / "input_02.csv")

    def build_initials_mapping(df: pd.DataFrame) -> dict:
        parts = df["Name"].astype(str).str.split("-", n=1, expand=True)
        parts[0] = parts[0].str.strip()
        parts[1] = parts[1].str.strip()
        letter_to_word = dict(zip(parts[0], parts[1]))

        def initials_to_name(initials: str) -> str:
            initials = str(initials).strip()
            if len(initials) != 2:
                return initials
            first, last = initials[0], initials[1]
            return f"{letter_to_word.get(first, first)} {letter_to_word.get(last, last)}"

        return initials_to_name

    initials_to_name = build_initials_mapping(names_df)

    first_cols = ["Toy", "Quota", "Production Manager", "Quality Assurance", "Fun Levels Tester", "Chief Wrapper"]
    current_cols = list(raw.columns)
    new_cols = []
    for idx, col in enumerate(current_cols):
        if idx < 6:
            new_cols.append(first_cols[idx])
        else:
            new_cols.append(raw.iloc[0, idx])
    raw.columns = new_cols
    raw = raw.iloc[1:].reset_index(drop=True)

    def parse_list_marker(text: str):
        text = str(text)
        prefix = "Number of Children on the "
        if text.startswith(prefix):
            list_name = text[len(prefix):]
            if list_name.endswith(" List"):
                list_name = list_name[:-5]
            return list_name
        return None

    raw["List"] = raw["Toy"].apply(parse_list_marker)
    marker_mask = raw["Toy"].astype(str).str.startswith("Number of Children on the ")
    raw["Number of Children"] = pd.NA
    raw.loc[marker_mask, "Number of Children"] = pd.to_numeric(raw.loc[marker_mask, "Quota"], errors="coerce")
    list_children_map = (
        raw.loc[raw["List"].notna(), ["List", "Number of Children"]]
        .dropna()
        .drop_duplicates(subset=["List"])
        .set_index("List")["Number of Children"]
        .to_dict()
    )
    raw["List"] = raw["List"].ffill()
    raw["Number of Children"] = raw["Number of Children"].ffill()

    data = raw.loc[~marker_mask].copy()

    data["Quota_prop"] = pd.to_numeric(data["Quota"], errors="coerce")
    data["Number of Children"] = pd.to_numeric(data["Number of Children"], errors="coerce")
    data["Quota"] = (data["Quota_prop"] * data["Number of Children"]).round(0).astype("int64")

    data["Production Manager"] = data["Production Manager"].apply(initials_to_name)

    week_cols = []
    for c in data.columns:
        if c in first_cols or c in ["List", "Number of Children"]:
            continue
        try:
            pd.to_datetime(c)
            week_cols.append(c)
        except Exception:
            pass

    id_cols = ["List", "Number of Children", "Toy", "Production Manager", "Quota"]
    long_df = data[id_cols + week_cols].melt(
        id_vars=id_cols,
        value_vars=week_cols,
        var_name="Week",
        value_name="Toys Produced",
    )
    long_df["Toys Produced"] = pd.to_numeric(long_df["Toys Produced"], errors="coerce").fillna(0).astype("int64")
    long_df["Week_dt"] = pd.to_datetime(long_df["Week"])
    long_df["Week"] = long_df["Week_dt"].dt.strftime("%d/%m/%Y")

    long_df = long_df.sort_values(by=["List", "Toy", "Week_dt"])
    long_df["Running Sum of Toys Produced"] = long_df.groupby(["List", "Toy"])["Toys Produced"].cumsum()

    long_df["Over or Under Quota?"] = (long_df["Running Sum of Toys Produced"] > long_df["Quota"]).map({True: "Over", False: "Under"})

    long_df["Number of Children"] = long_df["List"].map(list_children_map).astype("int64")

    output_01 = long_df[
        ["List", "Number of Children", "Toy", "Production Manager", "Quota", "Week", "Toys Produced", "Running Sum of Toys Produced", "Over or Under Quota?"]
    ].reset_index(drop=True)

    agg = long_df.groupby(["List", "Number of Children", "Toy", "Quota"], as_index=False).agg(
        **{"Toys Produced": ("Toys Produced", "sum")}
    )
    agg["Toys Over/Under Quota"] = agg["Toys Produced"] - agg["Quota"]

    def allocate_spares(group: pd.DataFrame) -> pd.DataFrame:
        group = group.copy()
        total_produced = int(group["Toys Produced"].sum())
        num_children = int(group["Number of Children"].iloc[0])
        group["Spare Toys"] = 0
        group["Toys Ready to be Gifts"] = group["Toys Produced"]
        if total_produced > num_children:
            surplus = total_produced - num_children
            over = group["Toys Over/Under Quota"]
            idx = over.idxmax()
            group.loc[idx, "Spare Toys"] = surplus
            group.loc[idx, "Toys Ready to be Gifts"] = group.loc[idx, "Toys Produced"] - surplus
        return group

    output_02 = (
        agg.groupby(["List", "Number of Children"], group_keys=False)
        .apply(allocate_spares)
        .copy()
    )

    output_02 = output_02[["List", "Toy", "Quota", "Toys Produced", "Toys Ready to be Gifts", "Spare Toys", "Toys Over/Under Quota"]].reset_index(drop=True)

    return {
        "output_01.csv": output_01,
        "output_02.csv": output_02,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    for old in cand_dir.glob("*.csv"):
        try:
            old.unlink()
        except Exception:
            pass

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


