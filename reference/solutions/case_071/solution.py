import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_01 = pd.read_csv(inputs_dir / "input_01.csv")
    input_02 = pd.read_csv(inputs_dir / "input_02.csv")
    input_03 = pd.read_csv(inputs_dir / "input_03.csv")
    
    roman_numeral = input_01["Number"].iloc[0]
    
    roman_map = dict(zip(input_02["Roman Numeral"], input_02["Numeric Equivalent"]))
    
    scaffold_df = input_03.copy()
    scaffold_df = scaffold_df.head(len(roman_numeral))
    
    chars = list(roman_numeral)
    scaffold_df["Character"] = chars
    scaffold_df["Position"] = scaffold_df["Scaffold"] - 1
    
    result_df = scaffold_df.merge(
        input_02, 
        left_on="Character", 
        right_on="Roman Numeral", 
        how="left"
    )
    
    result_df["Value"] = result_df["Numeric Equivalent"]
    
    next_values = []
    for i in range(len(result_df)):
        if i < len(result_df) - 1:
            next_values.append(result_df.iloc[i + 1]["Numeric Equivalent"])
        else:
            next_values.append(0)
    
    result_df["Next Value"] = next_values
    
    result_df["Adjusted Value"] = result_df.apply(
        lambda row: -row["Value"] if row["Value"] < row["Next Value"] else row["Value"],
        axis=1
    )
    
    numeric_equivalent = result_df["Adjusted Value"].sum()
    
    output_df = pd.DataFrame({
        "Number": [roman_numeral],
        "Numeric Equivalent": [int(numeric_equivalent)]
    })
    
    return {"output_01.csv": output_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

