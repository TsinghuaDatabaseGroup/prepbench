import pandas as pd
import numpy as np
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:

    def parse_data(df_raw: pd.DataFrame, gender: str) -> pd.DataFrame:
        months = {
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        }

        table = df_raw.fillna("").astype(
            str).apply(lambda col: col.str.strip())

        month_rows = table.index[table.apply(
            lambda r: r.isin(months).any(), axis=1)]
        if month_rows.empty:
            return pd.DataFrame(columns=["Month", "Rank", "Name", "Count", "Gender"])

        blocks: list[pd.DataFrame] = []
        for idx, start in enumerate(month_rows):
            end = month_rows[idx + 1] if idx + \
                1 < len(month_rows) else len(table)

            month_row = table.iloc[start]
            header_row = table.iloc[start +
                                    1] if start + 1 < len(table) else None
            data = table.iloc[start + 2: end]

            if header_row is None or data.empty:
                continue

            data = data[~data.apply(lambda r: "Total" in " ".join(r), axis=1)]
            data = data[(data != "").any(axis=1)]
            if data.empty:
                continue

            month_positions = np.where(month_row.isin(months))[0]
            if month_positions.size == 0:
                continue
            col_indices = np.sort(np.concatenate(
                [month_positions, month_positions + 1, month_positions + 2]
            ))
            col_months = np.repeat(
                month_row.iloc[month_positions].to_numpy(), 3)
            col_fields = np.tile(
                np.array(["Rank", "Name", "Count"]), len(month_positions))

            if col_indices.size == 0:
                continue

            block = data.iloc[:, col_indices].copy()
            block.columns = pd.MultiIndex.from_arrays([col_months, col_fields])

            stacked = block.stack(level=0, future_stack=True).reset_index()
            stacked = stacked.rename(
                columns={"level_0": "row_id", "level_1": "Month"})
            stacked["Gender"] = gender
            blocks.append(
                stacked[["Month", "Rank", "Name", "Count", "Gender"]])

        df_long = pd.concat(
            blocks, ignore_index=True) if blocks else pd.DataFrame()
        df_long = df_long[df_long["Rank"].str.isdigit() &
                          df_long["Count"].str.isdigit()]
        df_long["Rank"] = df_long["Rank"].astype(int)
        df_long["Count"] = df_long["Count"].astype(int)
        return df_long

    df_boys_raw = pd.read_csv(inputs_dir / "input_01.csv", header=None)
    df_boys = parse_data(df_boys_raw, "Boys")

    df_girls_raw = pd.read_csv(inputs_dir / "input_02.csv", header=None)
    df_girls = parse_data(df_girls_raw, "Girls")

    df_monthly = pd.concat([df_boys, df_girls], ignore_index=True)

    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    df_monthly["Month"] = pd.Categorical(
        df_monthly["Month"], categories=month_order, ordered=True)
    df_monthly = df_monthly.sort_values(
        ["Month", "Gender", "Rank"]).reset_index(drop=True)

    df_yearly = df_monthly.groupby(["Name", "Gender"])[
        "Count"].sum().reset_index()
    df_yearly = df_yearly.sort_values(
        ["Gender", "Count"], ascending=[True, False])

    top10_boys = df_yearly[df_yearly["Gender"] == "Boys"].head(10).copy()
    top10_girls = df_yearly[df_yearly["Gender"] == "Girls"].head(10).copy()

    top10_boys["2019 Rank"] = range(1, len(top10_boys) + 1)
    top10_girls["2019 Rank"] = range(1, len(top10_girls) + 1)

    df_top10 = pd.concat([top10_boys, top10_girls], ignore_index=True)
    df_top10 = df_top10[["2019 Rank", "Count", "Name", "Gender"]]
    df_top10 = df_top10.sort_values(
        ["Gender", "2019 Rank"]).reset_index(drop=True)

    df_monthly_output = df_monthly[[
        "Rank", "Count", "Name", "Month", "Gender"]].copy()

    return {
        "output_01.csv": df_top10,
        "output_02.csv": df_monthly_output,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
