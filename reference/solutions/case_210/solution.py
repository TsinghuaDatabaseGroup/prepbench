import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    account_holders = pd.read_csv(inputs_dir / "input_01.csv", dtype=str)
    account_info = pd.read_csv(inputs_dir / "input_02.csv", dtype=str)
    transaction_detail = pd.read_csv(inputs_dir / "input_03.csv", dtype=str)
    transaction_path = pd.read_csv(inputs_dir / "input_04.csv", dtype=str)
    
    transaction_path = transaction_path.rename(columns={
        "Account_From": "Account From",
        "Account_To": "Account To"
    })
    
    def normalize_account_holder_id(holder_id):
        holder_id_str = str(holder_id).strip()
        if holder_id_str and holder_id_str != "nan":
            try:
                return str(int(holder_id_str))
            except (ValueError, TypeError):
                return holder_id_str
        return holder_id_str
    
    account_info_expanded = []
    for _, row in account_info.iterrows():
        account_holder_ids = str(row["Account Holder ID"]).strip()
        if pd.notna(account_holder_ids) and account_holder_ids and account_holder_ids != "nan":
            ids = [id.strip() for id in account_holder_ids.split(",")]
            for holder_id in ids:
                if holder_id:
                    new_row = row.copy()
                    new_row["Account Holder ID"] = normalize_account_holder_id(holder_id)
                    account_info_expanded.append(new_row)
    
    account_info = pd.DataFrame(account_info_expanded)
    
    account_info["Account Number"] = account_info["Account Number"].astype(str)
    
    account_holders["Account Holder ID"] = account_holders["Account Holder ID"].apply(normalize_account_holder_id)
    account_holders["Contact Number"] = account_holders["Contact Number"].astype(str).replace("nan", "")
    def fix_phone_number(phone):
        phone_str = str(phone).strip()
        if phone_str and phone_str.isdigit():
            if len(phone_str) == 10 and phone_str.startswith("7"):
                phone_str = "0" + phone_str
            elif len(phone_str) == 10 and not phone_str.startswith("07"):
                phone_str = "0" + phone_str
        return phone_str
    account_holders["Contact Number"] = account_holders["Contact Number"].apply(fix_phone_number)
    
    transaction_detail["Transaction ID"] = transaction_detail["Transaction ID"].astype(str).replace("nan", "")
    transaction_path["Transaction ID"] = transaction_path["Transaction ID"].astype(str).replace("nan", "")
    transaction_path["Account To"] = transaction_path["Account To"].astype(str).replace("nan", "")
    transaction_path["Account From"] = transaction_path["Account From"].astype(str).replace("nan", "")
    
    transactions = transaction_detail.merge(
        transaction_path,
        on="Transaction ID",
        how="inner"
    )
    
    transactions = transactions[transactions["Cancelled?"] == "N"]
    
    transactions["Value"] = pd.to_numeric(transactions["Value"], errors="coerce")
    transactions = transactions[transactions["Value"] > 1000]
    transactions = transactions[transactions["Value"].notna()]
    
    transactions = transactions.merge(
        account_info,
        left_on="Account From",
        right_on="Account Number",
        how="inner",
        suffixes=("", "_from_account")
    )
    
    transactions = transactions[transactions["Account Type"] != "Platinum"]
    
    transactions = transactions.merge(
        account_holders,
        on="Account Holder ID",
        how="inner"
    )
    
    transactions["Transaction Date"] = pd.to_datetime(transactions["Transaction Date"], format="%Y-%m-%d", errors="coerce")
    transactions["Transaction Date"] = transactions["Transaction Date"].dt.strftime("%d/%m/%Y")
    
    transactions["Balance Date"] = pd.to_datetime(transactions["Balance Date"], format="%Y-%m-%d", errors="coerce")
    transactions["Balance Date"] = transactions["Balance Date"].dt.strftime("%d/%m/%Y")
    
    output_columns = [
        "Transaction ID",
        "Account To",
        "Transaction Date",
        "Value",
        "Name",
        "Date of Birth",
        "Contact Number",
        "First Line of Address",
        "Account Number",
        "Account Type",
        "Balance Date",
        "Balance"
    ]
    
    output_df = transactions[output_columns].copy()
    
    def normalize_transaction_id(tid):
        tid_str = str(tid).strip()
        if tid_str and tid_str.isdigit():
            return str(int(tid_str))
        return tid_str
    
    output_df["Transaction ID"] = output_df["Transaction ID"].apply(normalize_transaction_id)
    output_df["Account To"] = output_df["Account To"].astype(str)
    output_df["Value"] = pd.to_numeric(output_df["Value"], errors="coerce")
    output_df["Account Number"] = output_df["Account Number"].astype(str)
    output_df["Balance"] = pd.to_numeric(output_df["Balance"], errors="coerce")
    output_df["Value"] = output_df["Value"].fillna(0)
    output_df["Balance"] = output_df["Balance"].fillna(0)
    
    output_df = output_df.sort_values(by="Transaction ID").reset_index(drop=True)
    
    return {
        "output_01.csv": output_df
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

