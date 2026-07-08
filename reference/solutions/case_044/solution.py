from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    sales_path = inputs_dir / "input_01.csv"
    staff_path = inputs_dir / "input_02.csv"

    df_sales = pd.read_csv(sales_path)
    df_sales_long = df_sales.melt(id_vars=["Date"], var_name="Store", value_name="Store Sales")

    df_staff = pd.read_csv(staff_path)
    df_staff["Team Member"] = df_staff["Team Member"].astype(str).str.strip()

    staff_count = (
        df_staff.groupby(["Date", "Store"], as_index=False)
        .size()
        .rename(columns={"size": "Staff Count"})
    )

    df_join = df_sales_long.merge(staff_count, on=["Date", "Store"], how="inner")

    df_join["Est per Staff per Day"] = df_join["Store Sales"] / df_join["Staff Count"]

    df_member_days = df_staff.merge(
        df_join[["Date", "Store", "Est per Staff per Day"]],
        on=["Date", "Store"],
        how="inner",
    )

    df_avg = (
        df_member_days.groupby(["Store", "Team Member"], as_index=False)["Est per Staff per Day"].mean()
    )

    df_avg["Estimate Sales per Staff Member"] = df_avg["Est per Staff per Day"].round(2)

    df_avg["Rank"] = (
        df_avg.groupby("Store")["Estimate Sales per Staff Member"]
        .rank(method="dense", ascending=False)
        .astype(int)
    )

    out = df_avg[[
        "Estimate Sales per Staff Member",
        "Store",
        "Team Member",
        "Rank",
    ]]

    out["Store"] = out["Store"].astype(str)
    out["Team Member"] = out["Team Member"].astype(str)
    out["Estimate Sales per Staff Member"] = out["Estimate Sales per Staff Member"].astype(float)
    out["Rank"] = out["Rank"].astype(int)

    out = out.sort_values(["Store", "Rank", "Team Member"], kind="mergesort").reset_index(drop=True)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
