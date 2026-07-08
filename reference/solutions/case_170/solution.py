import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    products_df = pd.read_csv(inputs_dir / "input_01.csv")
    sales_df = pd.read_csv(inputs_dir / "input_02.csv")
    size_table_df = pd.read_csv(inputs_dir / "input_03.csv")
    
    size_id_to_size = dict(zip(size_table_df["Size ID"], size_table_df["Size"]))
    
    product_to_code = {}
    for _, row in products_df.iterrows():
        code = row["Product Code"]
        if code.startswith("SB"):
            num = code[2:]
            product_to_code[f"B{num}"] = code
        elif code.startswith("LS"):
            num = code[2:]
            product_to_code[f"L{num}"] = code
    
    product_info = {}
    for _, row in products_df.iterrows():
        product_info[row["Product Code"]] = {
            "Size": row["Size"],
            "Scent": row["Scent"]
        }
    
    sales_df["Recorded Size"] = sales_df["Size"].map(size_id_to_size)
    
    sales_df["Product Code"] = sales_df["Product"].map(product_to_code)
    
    sales_df["Correct Size"] = sales_df["Product Code"].map(lambda x: product_info.get(x, {}).get("Size"))
    sales_df["Scent"] = sales_df["Product Code"].map(lambda x: product_info.get(x, {}).get("Scent"))
    
    correct_mask = sales_df["Recorded Size"] == sales_df["Correct Size"]
    correct_sales = sales_df[correct_mask].copy()
    wrong_sales = sales_df[~correct_mask].copy()
    
    output_01 = correct_sales[["Recorded Size", "Scent", "Product", "Store"]].copy()
    output_01.columns = ["Product Size", "Scent", "Product", "Store"]
    output_01 = output_01.drop_duplicates().reset_index(drop=True)
    
    wrong_sales["Product Size"] = wrong_sales["Correct Size"]
    wrong_agg = wrong_sales.groupby(["Product", "Product Size", "Scent"]).size().reset_index(name="Sales with the wrong size")
    wrong_agg["Sales with the wrong size"] = wrong_agg["Sales with the wrong size"].astype(int)
    output_02 = wrong_agg[["Sales with the wrong size", "Product", "Product Size", "Scent"]].copy()
    output_02.columns = ["Sales with the wrong size", "Product Code", "Product Size", "Scent"]
    output_02 = output_02.reset_index(drop=True)
    
    return {
        "output_01.csv": output_01,
        "output_02.csv": output_02
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
