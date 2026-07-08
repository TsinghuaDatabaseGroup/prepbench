from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    def build_iban(row: pd.Series) -> str:
        sort_code = str(row["Sort Code"]).replace("-", "")
        account_number = str(row["Account Number"])
        check_digits = str(row["Check Digits"])
        swift = str(row["SWIFT code"])
        return f"GB{check_digits}{swift}{sort_code}{account_number}"

    banks = pd.read_csv(inputs_dir / "input_01.csv", dtype=str)
    tx = pd.read_csv(inputs_dir / "input_02.csv", dtype=str)

    merged = tx.merge(banks, on="Bank", how="left", validate="many_to_one")
    merged["IBAN"] = merged.apply(build_iban, axis=1)

    out = merged[["Transaction ID", "IBAN"]].copy()
    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).write_text("", encoding="utf-8")
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


