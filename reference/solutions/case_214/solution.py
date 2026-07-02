from pathlib import Path
import math
import numpy as np
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    branches = pd.read_csv(inputs_dir / "input_01.csv")
    customers = pd.read_csv(inputs_dir / "input_02.csv")

    def to_radians(series: pd.Series) -> pd.Series:
        return series * math.pi / 180.0

    branches_rad = branches.copy()
    customers_rad = customers.copy()
    branches_rad["Branch Lat Rad"] = to_radians(branches_rad["Branch Lat"])
    branches_rad["Branch Long Rad"] = to_radians(branches_rad["Branch Long"])
    customers_rad["Address Lat Rad"] = to_radians(customers_rad["Address Lat"])
    customers_rad["Address Long Rad"] = to_radians(customers_rad["Address Long"])

    earth_radius_miles = 3963.0

    branches_rad["_key"] = 1
    customers_rad["_key"] = 1
    cross = customers_rad.merge(branches_rad, on="_key", how="outer", suffixes=("", "_b"))

    lat1 = cross["Address Lat Rad"]
    lon1 = cross["Address Long Rad"]
    lat2 = cross["Branch Lat Rad"]
    lon2 = cross["Branch Long Rad"]
    inner = (np.sin(lat1) * np.sin(lat2)) + (np.cos(lat1) * np.cos(lat2) * np.cos(lon2 - lon1))
    inner = np.clip(inner, -1.0, 1.0)
    cross["DistanceRaw"] = earth_radius_miles * np.arccos(inner)

    nearest_idx = cross.groupby("Customer", as_index=False)["DistanceRaw"].idxmin()["DistanceRaw"]
    nearest = cross.loc[nearest_idx].copy()

    nearest["Distance"] = nearest["DistanceRaw"].round(2)

    nearest["Customer Priority"] = (
        nearest.sort_values(["Distance", "Customer"], ascending=[True, True])
        .groupby("Branch")
        .cumcount() + 1
    )

    out = nearest[[
        "Branch",
        "Branch Long",
        "Branch Lat",
        "Distance",
        "Customer Priority",
        "Customer",
        "Address Long",
        "Address Lat",
    ]].copy()

    numeric_cols = [
        "Branch Long",
        "Branch Lat",
        "Distance",
        "Customer Priority",
        "Customer",
        "Address Long",
        "Address Lat",
    ]
    for c in numeric_cols:
        out[c] = pd.to_numeric(out[c])

    out = out.sort_values(by=["Branch Long", "Customer Priority"], ascending=[True, True]).reset_index(drop=True)

    return {
        "output_01.csv": out
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True, parents=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
