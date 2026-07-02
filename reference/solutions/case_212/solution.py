from __future__ import annotations
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    account_info = pd.read_csv(inputs_dir / "input_01.csv")
    transaction_detail = pd.read_csv(inputs_dir / "input_02.csv")
    transaction_path = pd.read_csv(inputs_dir / "input_03.csv")

    transaction_path = transaction_path.rename(columns={
        "Account_From": "Account From",
        "Account_To": "Account To"
    })

    transaction_detail = transaction_detail[transaction_detail["Cancelled?"] != "Y"].copy(
    )

    transactions = transaction_path.merge(
        transaction_detail[["Transaction ID", "Transaction Date", "Value"]],
        on="Transaction ID",
        how="inner"
    )

    outgoing = transactions.copy()
    outgoing = outgoing.rename(columns={"Account From": "Account Number"})
    outgoing["Value"] = -outgoing["Value"]
    outgoing = outgoing[["Transaction ID",
                         "Account Number", "Transaction Date", "Value"]]

    incoming = transactions.copy()
    incoming = incoming.rename(columns={"Account To": "Account Number"})
    incoming = incoming[["Transaction ID",
                         "Account Number", "Transaction Date", "Value"]]

    all_transactions = pd.concat([outgoing, incoming], ignore_index=True)

    account_info_clean = account_info[[
        "Account Number", "Balance Date", "Balance"]].copy()
    account_info_clean["Transaction Date"] = account_info_clean["Balance Date"]
    account_info_clean["Value"] = None
    account_info_clean = account_info_clean[[
        "Account Number", "Transaction Date", "Value", "Balance"]]

    all_data = pd.concat(
        [all_transactions, account_info_clean], ignore_index=True)

    all_data["Transaction Date"] = pd.to_datetime(all_data["Transaction Date"])
    all_data = all_data.sort_values(
        by=["Account Number", "Transaction Date", "Value"],
        ascending=[True, True, False],
        na_position="last"
    )
    all_data["Transaction Order"] = all_data.groupby(
        "Account Number").cumcount() + 1


    initial_balances = account_info_clean.set_index("Account Number")[
        "Balance"].to_dict()

    def calculate_balance(group):
        group = group.sort_values("Transaction Order")
        balances = []
        for idx, row in group.iterrows():
            if row["Transaction Order"] == 1:
                balance = initial_balances.get(row["Account Number"], 0)
            else:
                prev_balance = balances[-1] if balances else initial_balances.get(
                    row["Account Number"], 0)
                current_value = row["Value"] if pd.notna(row["Value"]) else 0
                balance = prev_balance + current_value
            balances.append(balance)
        group["Balance"] = balances
        return group

    all_data = all_data.groupby(
        "Account Number", group_keys=False).apply(calculate_balance)

    all_data["Transaction Value"] = all_data.apply(
        lambda row: None if row["Transaction Order"] == 1 else row["Value"],
        axis=1
    )

    all_data["Balance"] = all_data["Balance"].round(2)

    all_data["Balance Date"] = all_data["Transaction Date"].dt.strftime(
        "%d/%m/%Y")

    output = all_data[[
        "Account Number",
        "Balance Date",
        "Transaction Value",
        "Balance"
    ]].copy()

    output = output.sort_values(
        by=["Account Number", "Balance Date", "Transaction Value"],
        ascending=[True, True, True],
        na_position="last"
    ).reset_index(drop=True)

    output["Account Number"] = output["Account Number"].astype(str)
    output["Balance Date"] = output["Balance Date"].astype(str)
    output["Transaction Value"] = output["Transaction Value"].apply(
        lambda x: None if pd.isna(x) else round(
            float(x), 2) if x is not None else None
    )
    output["Balance"] = output["Balance"].apply(lambda x: round(float(x), 2))

    return {
        "output_01.csv": output
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
