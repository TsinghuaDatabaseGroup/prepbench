from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    inputs_dir = Path(inputs_dir)

    def _read_csv(filename: str) -> pd.DataFrame:
        return pd.read_csv(inputs_dir / filename)

    opp = _read_csv("input_01.csv")
    users = _read_csv("input_02.csv")
    acct = _read_csv("input_03.csv")

    name_map = users.set_index("Id")["Name"]

    opp = (
        opp[
            [
                "Id",
                "Name",
                "StageName",
                "Amount",
                "AccountId",
                "OwnerId",
                "CreatedById",
            ]
        ]
        .rename(columns={"Id": "Opportunity ID", "Name": "Opportunity Name"})
        .copy()
    )
    opp["Created By Name"] = opp["CreatedById"].map(name_map)
    opp["Owner Name"] = opp["OwnerId"].map(name_map)

    acct = (
        acct[["Id", "Name", "Type", "OwnerId", "CreatedById"]]
        .rename(
            columns={
                "Id": "Account Id",
                "Name": "Account Name",
                "Type": "Account Type",
                "OwnerId": "Account OwnerId",
                "CreatedById": "Account CreatedById",
            }
        )
        .copy()
    )
    acct["Account Owner Name"] = acct["Account OwnerId"].map(name_map)
    acct["Account Created By Name"] = acct["Account CreatedById"].map(name_map)

    opp_with_account = opp.merge(
        acct[
            [
                "Account Id",
                "Account Name",
                "Account Type",
                "Account Owner Name",
                "Account Created By Name",
            ]
        ],
        how="left",
        left_on="AccountId",
        right_on="Account Id",
        sort=False,
    )
    opp_with_account = opp_with_account.drop(columns=["Account Id"])

    output_cols = [
        "Opportunity Name",
        "StageName",
        "Amount",
        "Created By Name",
        "Owner Name",
        "Account Name",
        "Account Type",
        "Account Owner Name",
        "Account Created By Name",
        "Opportunity ID",
        "AccountId",
        "OwnerId",
        "CreatedById",
    ]
    output_01 = opp_with_account[output_cols].copy()

    output_02 = (
        output_01.groupby("Owner Name", as_index=False, dropna=False)["Amount"]
        .sum()
        .sort_values(["Amount", "Owner Name"], ascending=[False, True], ignore_index=True)
    )

    output_03 = (
        output_01.groupby("Account Owner Name",
                          as_index=False, dropna=False)["Amount"]
        .sum()
        .sort_values(
            ["Amount", "Account Owner Name"], ascending=[False, True], ignore_index=True
        )
    )

    output_04 = (
        output_01.groupby("Account Name", as_index=False, dropna=False)
        .agg(
            **{
                "Number of Opportunities": ("Opportunity ID", pd.Series.nunique),
                "Amount": ("Amount", "sum"),
            }
        )
        .sort_values(["Amount", "Account Name"], ascending=[False, True], ignore_index=True)
    )

    return {
        "output_01.csv": output_01,
        "output_02.csv": output_02,
        "output_03.csv": output_03,
        "output_04.csv": output_04,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
