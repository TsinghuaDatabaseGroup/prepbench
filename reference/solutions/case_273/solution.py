import re
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def _extract_english_class(name: str) -> str:
        if not isinstance(name, str):
            return name
        m = re.search(r"\(([^()]+)\)", name)
        if m:
            eng = m.group(1).strip()
            eng = eng.replace("-", "")
            return eng
        return name.strip()

    def _clean_apostrophes(text: str) -> str:
        if not isinstance(text, str):
            return text
        return text.replace("&#039;", "'")

    def _parse_fahrenheit_range(cell: str) -> float:
        if not isinstance(cell, str):
            return np.nan
        s = cell.replace("–", "-")
        m = re.search(r"(-?\d+)\s*degree[s]?\s*Fahrenheit", s, flags=re.IGNORECASE)
        if m:
            return float(m.group(1))
        return np.nan

    def build_stage_one(inputs_dir: Path) -> pd.DataFrame:
        animals = pd.read_csv(inputs_dir / "input_01.csv")
        plants = pd.read_csv(inputs_dir / "input_04.csv")
        wildlife_map = pd.read_csv(inputs_dir / "input_06.csv")

        plants = plants.rename(columns={"Plant": "Name", "Stattus": "Status"})
        animals = animals.rename(columns={"Animal": "Name"})

        animals_part = animals[["Name", "Status", "Class"]].copy()
        animals_part["Table Names"] = "Animal Details"

        plants_part = plants[["Name", "Status", "Class"]].copy()
        plants_part["Table Names"] = "Plant Details"

        details = pd.concat([animals_part, plants_part], ignore_index=True)

        details["Class"] = details["Class"].apply(_extract_english_class)

        details["Wildlife"] = details["Table Names"].map(
            lambda t: "Animal" if "Animal" in str(t) else ("Plant" if "Plant" in str(t) else None)
        )

        wildlife_map["Name"] = wildlife_map["Name"].apply(_clean_apostrophes)
        details["Name"] = details["Name"].apply(_clean_apostrophes)

        stage_one = pd.merge(
            wildlife_map[["Wildlife", "Name", "Region", "Habitat"]],
            details[["Wildlife", "Name", "Status", "Class"]],
            on=["Wildlife", "Name"],
            how="inner",
            validate="one_to_one",
        )

        stage_one = stage_one[["Wildlife", "Name", "Class", "Region", "Habitat", "Status"]].copy()
        return stage_one

    def build_stage_two(stage_one: pd.DataFrame, inputs_dir: Path) -> pd.DataFrame:
        climate = pd.read_csv(inputs_dir / "input_05.csv")
        sd_low = climate["Low °F"].min()
        sd_high = climate["High °F"].max()

        habitats = pd.read_csv(inputs_dir / "input_03.csv")
        habitats["MinF"] = habitats["Min Temp"].apply(_parse_fahrenheit_range)
        habitats["MaxF"] = habitats["Max Temp"].apply(_parse_fahrenheit_range)
        habitat_range = habitats[["Habitat", "MinF", "MaxF"]].copy()

        s2 = stage_one.copy()
        s2 = s2.assign(Habitat=s2["Habitat"].str.split(", "))
        s2 = s2.explode("Habitat", ignore_index=True)

        s2 = s2.merge(habitat_range, on="Habitat", how="left")

        agg = (
            s2.groupby(["Wildlife", "Name"], as_index=False)
            .agg({
                "MinF": "min",
                "MaxF": "max",
                "Status": "first",
                "Class": "first",
                "Region": "first",
            })
        )

        def habitat_note_and_degrees(minf: float, maxf: float):
            if pd.isna(minf) or pd.isna(maxf):
                return None, np.nan
            if sd_low >= minf and sd_high <= maxf:
                return "Ideal", 0.0
            if sd_high > maxf:
                return "Above", float(sd_high - maxf)
            if sd_low < minf:
                return "Below", float(sd_low - minf)
            return None, np.nan

        notes = []
        degrees = []
        for a, b in zip(agg["MinF"], agg["MaxF"]):
            n, d = habitat_note_and_degrees(a, b)
            notes.append(n)
            degrees.append(d)
        agg["Habitat Notes"] = notes
        agg["Degrees outside Ideal"] = degrees

        agg = agg[agg["Habitat Notes"] != "Ideal"].copy()

        pr = pd.read_csv(inputs_dir / "input_02.csv")
        pr = pr.rename(columns={"Priority": "Priority Number"})
        agg = agg.merge(pr, on="Status", how="left")
        agg["Priority Number"] = agg["Priority Number"].fillna(6)

        agg["abs_degrees"] = agg["Degrees outside Ideal"].abs()
        status_priority = (
            agg.drop_duplicates(subset=["Status"]).sort_values(["Priority Number"])
        )
        ordered_statuses = [s for s in status_priority["Status"].tolist() if pd.notna(s)]

        agg["Priority Order"] = np.nan
        offset = 0
        for status in ordered_statuses:
            mask = agg["Status"] == status
            unique_abs = (
                agg.loc[mask, "abs_degrees"].dropna().sort_values(ascending=False).unique().tolist()
            )
            bucket_map = {v: (i + 1 + offset) for i, v in enumerate(unique_abs)}
            agg.loc[mask, "Priority Order"] = agg.loc[mask, "abs_degrees"].map(bucket_map)
            offset += len(unique_abs)

        combined_hab = stage_one[["Wildlife", "Name", "Habitat"]].drop_duplicates()
        agg = agg.merge(combined_hab, on=["Wildlife", "Name"], how="left")

        out2 = agg[[
            "Wildlife",
            "Name",
            "Priority Order",
            "Habitat Notes",
            "Degrees outside Ideal",
            "Status",
            "Class",
            "Region",
            "Habitat",
        ]].copy()

        return out2

    stage_one = build_stage_one(inputs_dir)
    stage_two = build_stage_two(stage_one, inputs_dir)

    return {
        "output_01.csv": stage_one,
        "output_02.csv": stage_two,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
