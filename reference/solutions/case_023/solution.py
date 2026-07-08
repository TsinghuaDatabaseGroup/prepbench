import pandas as pd
from pathlib import Path
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_files = sorted(inputs_dir.glob("input_*.csv"))

    base_monday0 = pd.Timestamp("2019-07-15")
    day_offset = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }

    frames: list[pd.DataFrame] = []
    for idx, file in enumerate(input_files):
        df = pd.read_csv(file)

        df["Name"] = df["Notes"].str.extract(r"^(.*?)\s+wants", flags=re.IGNORECASE)
        df["Name"] = df["Name"].str.title()

        df["Value"] = (
            df["Notes"].str.extract(r"£(\d+)", flags=re.IGNORECASE).astype(int)
        )

        product_info = df["Notes"].str.extract(r"of\s+(.*?)$", flags=re.IGNORECASE)[0]
        df["Scent"] = product_info.str.split().str[0].str.title()
        df["Product"] = product_info.str.split().str[1:].str.join(" ").str.title()

        base_monday = base_monday0 + pd.Timedelta(days=7 * idx)
        df["Date"] = base_monday + pd.to_timedelta(df["Day"].map(day_offset), unit="D")

        df["Notes"] = df["Notes"].str.lower()
        df["Scent"] = df["Scent"] + " "

        frames.append(df[["Date", "Name", "Value", "Scent", "Product", "Notes"]])

    output_df = pd.concat(frames, ignore_index=True)

    return {"output_01.csv": output_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    results = solve(inputs_dir)

    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8", date_format="%d/%m/%Y")
