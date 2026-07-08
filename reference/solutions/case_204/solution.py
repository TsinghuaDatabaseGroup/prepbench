import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    df["Bank"] = df["Transaction Code"].str.split("-").str[0]
    
    df["Online or In-Person"] = df["Online or In-Person"].map({1: "Online", 2: "In-Person"})
    
    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], format="%d/%m/%Y %H:%M:%S")
    df["Transaction Date"] = df["Transaction Date"].dt.day_name()
    
    
    output_01 = df.groupby("Bank", as_index=False)["Value"].sum()
    output_01 = output_01.sort_values("Bank")
    
    output_02 = df.groupby(["Bank", "Online or In-Person", "Transaction Date"], as_index=False)["Value"].sum()
    output_02 = output_02.sort_values(["Bank", "Online or In-Person", "Transaction Date"])
    
    output_03 = df.groupby(["Bank", "Customer Code"], as_index=False)["Value"].sum()
    output_03 = output_03.sort_values(["Bank", "Customer Code"])
    
    output_03["Customer Code"] = output_03["Customer Code"].astype(str)
    
    return {
        "output_01.csv": output_01,
        "output_02.csv": output_02,
        "output_03.csv": output_03,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    
    for filename, df in outputs.items():
        output_path = cand_dir / filename
        df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"已生成: {output_path}")

