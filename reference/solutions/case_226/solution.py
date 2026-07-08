from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    def read_inputs(inputs_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        students = pd.read_csv(inputs_path / "input_01.csv")
        scores = pd.read_csv(inputs_path / "input_02.csv")
        tiles = pd.read_csv(inputs_path / "input_03.csv")
        return students, scores, tiles

    def prepare_students(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = [col.strip() for col in df.columns]
        if "Full name" in df.columns:
            df["Full name"] = df["Full name"].astype(str).str.strip()
        if "Class" in df.columns:
            df["Class"] = df["Class"].astype(str).str.strip()
        return df

    def compute_quartiles(scores_df: pd.DataFrame, tiles_df: pd.DataFrame, students_df: pd.DataFrame) -> pd.DataFrame:
        scores_df = scores_df.copy()
        subjects = [c for c in scores_df.columns if c != "Student ID"]
        number_to_label = dict(zip(tiles_df["Number"], tiles_df["Range"]))
        for subj in subjects:
            base_series = scores_df[subj].astype(float)
            vals_sorted = sorted(base_series.tolist())
            n = len(vals_sorted)
            if n == 0:
                scores_df[subj] = "Interquartile range"
                continue
            n_low = n // 4
            if n_low == 0:
                bottom_threshold = float("-inf")
                top_threshold = float("inf")
            else:
                bottom_threshold = vals_sorted[n_low - 1]
                top_threshold = vals_sorted[-n_low]
            median = vals_sorted[n // 2] if n % 2 == 1 else (vals_sorted[n // 2 - 1] + vals_sorted[n // 2]) / 2.0

            tile_all = []
            for v in scores_df[subj].astype(float):
                if v <= bottom_threshold:
                    tile_all.append(4)
                elif v > top_threshold:
                    tile_all.append(1)
                elif v <= median:
                    tile_all.append(2)
                else:
                    tile_all.append(3)
            scores_df[subj + "_tile"] = tile_all
            scores_df[subj] = scores_df[subj + "_tile"].map(number_to_label)
            scores_df.drop(columns=[subj + "_tile"], inplace=True)
        keep_cols = ["Student ID"] + subjects
        return scores_df[keep_cols]

    students_df, scores_df, tiles_df = read_inputs(inputs_dir)
    students_df = prepare_students(students_df)
    labeled_scores_df = compute_quartiles(scores_df, tiles_df, students_df)

    merged = students_df.merge(labeled_scores_df, on="Student ID", how="left")

    subjects = ["English", "Economics", "Psychology"]
    is_target_class = merged["Class"].isin(["9A", "9B"])
    lower_quart_count = (merged[subjects] == "25th percentile").sum(axis=1)
    flagged = is_target_class & (lower_quart_count >= 2)
    merged["Flag"] = flagged.map({True: "Yes", False: "No"})

    output = merged[flagged].copy()

    output = output[["Full name", "Flag", "Class"] + subjects]

    output = output.sort_values(by=["Class", "Full name"], ascending=[False, True], kind="mergesort").reset_index(drop=True)

    return {
        "output_01.csv": output
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

