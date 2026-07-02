import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    CUTOFF = pd.Timestamp(2023, 2, 21)

    input_tiers_csv = inputs_dir / "input_01.csv"
    input_costs_csv = inputs_dir / "input_02.csv"
    input_customers_csv = inputs_dir / "input_03.csv"

    tiers = pd.read_csv(input_tiers_csv, dtype=str).fillna("")
    tiers.columns = [c.strip() for c in tiers.columns]
    tiers["Tier Grouping"] = tiers["Tier Grouping"].astype(int)
    tiers["TierNumRule"] = tiers["Tier"].str.extract(r"(\d+)").astype(int)
    tiers["Benefits"] = tiers["Benefits"].str.replace(
        " & ", ", ", regex=False).str.strip()
    tiers = tiers[tiers["Benefits"].ne("")].copy()

    customers = pd.read_csv(input_customers_csv, dtype=str).fillna("")
    customers.columns = [c.strip() for c in customers.columns]
    if "CustomerID" in customers.columns and "Customer ID" not in customers.columns:
        customers = customers.rename(columns={"CustomerID": "Customer ID"})
    customers["Number of Flights"] = pd.to_numeric(
        customers["Number of Flights"], errors="coerce").fillna(0).astype(int)
    customers["Last Date Flown"] = pd.to_datetime(
        customers["Last Date Flown"], errors="coerce")
    customers["First Flight"] = pd.to_datetime(
        customers["First Flight"], errors="coerce")
    customers = customers[customers["Last Date Flown"] >= CUTOFF].copy()
    years = (customers["Last Date Flown"].dt.year -
             customers["First Flight"].dt.year).fillna(0).astype(int) + 1
    customers["AvgFlightsPerYear"] = customers["Number of Flights"] / \
        years.clip(lower=1)

    costs = pd.read_csv(input_costs_csv, dtype=str).fillna("")
    costs.columns = [c.strip() for c in costs.columns]
    costs["Benefit"] = costs["Benefit"].str.strip()
    raw = costs["Cost"].str.replace(",", "").str.replace(
        "£", "").str.strip().str.lower()
    costs["CostValue"] = pd.to_numeric(raw.str.extract(
        r"([0-9]+(?:\.[0-9]+)?)")[0], errors="coerce").fillna(0.0)
    costs["Frequency"] = "yearly"
    costs.loc[raw.str.contains("per flight", na=False),
              "Frequency"] = "per flight"
    costs = costs[["Benefit", "CostValue", "Frequency"]]

    def compute_for_bin(bin_size: int) -> pd.DataFrame:
        cust = customers.copy()
        cust["TierNumCust"] = (
            cust["Number of Flights"] // bin_size).astype(int)

        tsel = tiers[tiers["Tier Grouping"] == bin_size].copy()
        ben = (tsel.assign(BenefitList=tsel["Benefits"].str.split(","))
               .explode("BenefitList"))
        ben["Benefit"] = ben["BenefitList"].fillna("").str.strip()
        ben = ben[ben["Benefit"].ne(
            "")][["TierNumRule", "Benefit"]].drop_duplicates()
        if ben.empty or cust.empty:
            return pd.DataFrame(columns=["Tier", "Year Cost", "Number of Customers"])

        rule_levels = pd.DataFrame(
            {"TierNumRule": sorted(ben["TierNumRule"].unique())})
        cust_small = cust[["Customer ID",
                           "TierNumCust", "AvgFlightsPerYear"]].copy()
        cust_small["__k__"] = 1
        rule_levels["__k__"] = 1
        pairs = cust_small.merge(
            rule_levels, on="__k__", how="inner").drop(columns="__k__")
        pairs = pairs[pairs["TierNumCust"] >= pairs["TierNumRule"]]

        ladders = (pairs.merge(ben, on="TierNumRule", how="inner")
                        .merge(costs, on="Benefit", how="inner"))

        ladders["Year Cost"] = ladders["CostValue"].where(
            ladders["Frequency"].eq("yearly"),
            ladders["CostValue"] * ladders["AvgFlightsPerYear"]
        )

        n_by_tier = (ladders[["TierNumCust", "Customer ID"]]
                     .drop_duplicates()
                     .groupby("TierNumCust", as_index=False)["Customer ID"]
                     .nunique()
                     .rename(columns={"Customer ID": "Number of Customers"}))
        cost_by_tier = ladders.groupby("TierNumCust", as_index=False)[
            "Year Cost"].sum()

        out = (n_by_tier.merge(cost_by_tier, on="TierNumCust", how="left")
                        .rename(columns={"TierNumCust": "Tier"})
                        .sort_values("Tier", ignore_index=True))[["Tier", "Year Cost", "Number of Customers"]]
        return out

    out5 = compute_for_bin(5)
    out10 = compute_for_bin(10)
    return {"output_01.csv": out5, "output_02.csv": out10}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for fname, df in results.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
