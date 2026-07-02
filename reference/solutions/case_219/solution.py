from __future__ import annotations
import pandas as pd
import re
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    pop_df = pd.read_csv(inputs_dir / "input_02.csv", skiprows=3, dtype=str)
    
    pop_df = pop_df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], errors="ignore")
    
    pop_df["Country Name"] = pop_df["Country Name"].str.strip()
    
    year_cols = [str(year) for year in range(1960, 2022)]
    id_vars = ["Country Name"]
    pop_pivot = pd.melt(
        pop_df,
        id_vars=id_vars,
        value_vars=year_cols,
        var_name="Year",
        value_name="Population"
    )
    pop_pivot["Year"] = pop_pivot["Year"].astype(int)
    pop_pivot["Population"] = pd.to_numeric(pop_pivot["Population"], errors="coerce")
    
    def clean_country_name(name: str) -> str:
        if pd.isna(name):
            return name
        name = str(name).strip()
        if name in ["Virgin Islands (U.S.)"]:
            return "Virgin Islands"
        if name in ["São Tomé and Príncipe"]:
            return "Sao Tome and Principe"
        if name in ["Curacao"]:
            return "Curaçao"
        return name
    
    pop_pivot["Country Name"] = pop_pivot["Country Name"].apply(clean_country_name)
    
    size_df = pd.read_csv(inputs_dir / "input_01.csv", dtype=str)
    
    def extract_km2(value: str) -> float:
        if pd.isna(value):
            return pd.NA
        value = str(value).strip()
        match = re.match(r'^([\d,]+\.?\d*)', value)
        if match:
            return float(match.group(1).replace(",", ""))
        return pd.NA
    
    size_df["Land in km2"] = size_df["Land in km2 (mi2)"].apply(extract_km2)
    
    def clean_country_name_size(name: str) -> str:
        if pd.isna(name):
            return name
        name = str(name).strip()
        name = re.sub(r'\[.*?\]', '', name).strip()
        name = re.sub(r'\(.*?\)', '', name).strip()
        name = re.sub(r'^[^\w]+', '', name).strip()
        if name in ["Virgin Islands", "U.S. Virgin Islands"]:
            return "Virgin Islands"
        if name in ["Jan Mayen", "Svalbard"]:
            return "Svalbard"
        if name in ["São Tomé and Príncipe"]:
            return "Sao Tome and Principe"
        if name in ["Channel Islands", "Guernsey", "Jersey"]:
            return "Channel Islands"
        return name
    
    size_df["Country / Dependency"] = size_df["Country / Dependency"].apply(clean_country_name_size)
    
    size_agg = size_df.groupby("Country / Dependency", as_index=False)["Land in km2"].sum()
    size_agg = size_agg.rename(columns={"Country / Dependency": "Country Name"})
    
    merged = pop_pivot.merge(size_agg, on="Country Name", how="inner")
    
    merged = merged[merged["Country Name"] != "World"]
    
    def calc_density(pop, area):
        if pd.isna(pop) or pd.isna(area) or area == 0:
            return pd.NA
        pop_dec = Decimal(str(pop))
        area_dec = Decimal(str(area))
        density = pop_dec / area_dec
        density = density.quantize(Decimal('0.000000000001'), rounding=ROUND_HALF_UP)
        return float(density)
    
    merged["Population Density"] = merged.apply(
        lambda row: calc_density(row["Population"], row["Land in km2"]), axis=1
    )
    
    merged_filtered = merged[merged["Year"].isin([2000, 2021])].copy()
    
    pivot_df = merged_filtered.pivot_table(
        index="Country Name",
        columns="Year",
        values="Population Density",
        aggfunc="first"
    ).reset_index()
    pivot_df.columns = ["Country", "Population Density 2000", "Population Density 2021"]
    
    pivot_df["Population Density 2000"] = pd.to_numeric(pivot_df["Population Density 2000"], errors="coerce")
    pivot_df["Population Density 2021"] = pd.to_numeric(pivot_df["Population Density 2021"], errors="coerce")
    
    def calc_pct_change(dens_2021, dens_2000):
        if pd.isna(dens_2021) or pd.isna(dens_2000) or dens_2000 == 0:
            return pd.NA
        dens_2021_dec = Decimal(str(dens_2021))
        dens_2000_dec = Decimal(str(dens_2000))
        pct_change = 100 * (dens_2021_dec - dens_2000_dec) / dens_2000_dec
        pct_change = pct_change.quantize(Decimal('0.000000000001'), rounding=ROUND_HALF_UP)
        return float(pct_change)
    
    pivot_df["% Change in Population Density"] = pivot_df.apply(
        lambda row: calc_pct_change(row["Population Density 2021"], row["Population Density 2000"]), axis=1
    )
    pivot_df["Rank % Change"] = pivot_df["% Change in Population Density"].rank(
        method="min", ascending=False
    ).astype(int)
    
    
    def format_number(x):
        if pd.isna(x):
            return x
        rounded = round(float(x), 9)
        s = f"{rounded:.9f}"
        s = s.rstrip('0').rstrip('.')
        return s if s else '0'
    
    output1 = pivot_df.nlargest(10, "Population Density 2021")[["Country", "Population Density 2021"]].copy()
    output1["Rank Population Density 2021"] = output1["Population Density 2021"].rank(
        method="min", ascending=False
    ).astype(int)
    output1["Population Density 2021"] = output1["Population Density 2021"].apply(format_number)
    output1 = output1[["Country", "Population Density 2021", "Rank Population Density 2021"]]
    
    output2 = pivot_df.nlargest(10, "% Change in Population Density")[
        ["Country", "Population Density 2000", "Population Density 2021", 
         "% Change in Population Density", "Rank % Change"]
    ].copy()
    output2["Population Density 2000"] = output2["Population Density 2000"].apply(format_number)
    output2["Population Density 2021"] = output2["Population Density 2021"].apply(format_number)
    output2["% Change in Population Density"] = output2["% Change in Population Density"].apply(format_number)
    
    return {
        "output_01.csv": output1,
        "output_02.csv": output2,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for fname, df in results.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

