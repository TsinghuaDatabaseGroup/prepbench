from __future__ import annotations
import pandas as pd
from pathlib import Path
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:

    words_df = pd.read_csv(inputs_dir / "input_01.csv")
    scaffold_df = pd.read_csv(inputs_dir / "input_02.csv")
    scrabble_df = pd.read_csv(inputs_dir / "input_03.csv")

    tiles_data = []
    for _, row in scrabble_df.iterrows():
        scrabble_text = row["Scrabble"]
        points_match = re.search(r'(\d+)\s+points?', scrabble_text)
        if points_match:
            points = int(points_match.group(1))
        else:
            if "0 points" in scrabble_text:
                points = 0
            else:
                continue

        tile_pattern = r'([A-Z])\s*×\s*(\d+)'
        matches = re.findall(tile_pattern, scrabble_text)
        for tile, freq in matches:
            tiles_data.append({
                "Tile": tile,
                "Frequency": int(freq),
                "Points": points
            })

    tiles_df = pd.DataFrame(tiles_data)

    total_tiles = tiles_df["Frequency"].sum()
    tiles_df["% Chance"] = (tiles_df["Frequency"] / total_tiles).round(2)

    scaffold_values = scaffold_df[scaffold_df["Scaffold"]
                                  <= 7]["Scaffold"].tolist()

    word_letter_list = []
    for _, word_row in words_df.iterrows():
        word = word_row["7 letter word"]
        for scaffold in scaffold_values:
            if scaffold <= len(word):
                letter = word[scaffold - 1].upper()
                word_letter_list.append({
                    "7 letter word": word,
                    "Scaffold": scaffold,
                    "Letter": letter
                })

    word_letter_df = pd.DataFrame(word_letter_list)

    letter_count_df = word_letter_df.groupby(
        ["7 letter word", "Letter"]).size().reset_index(name="Number of Occurrences")

    merged_df = letter_count_df.merge(
        tiles_df, left_on="Letter", right_on="Tile", how="inner")

    def calculate_chance(row):
        if row["Number of Occurrences"] > row["Frequency"]:
            return 0.0
        base_chance = row["% Chance"]
        return base_chance ** row["Number of Occurrences"]

    merged_df["Letter % Chance"] = merged_df.apply(calculate_chance, axis=1)

    merged_df["Points Contribution"] = merged_df["Points"] * \
        merged_df["Number of Occurrences"]

    result_df = merged_df.groupby("7 letter word").agg({
        "Points Contribution": "sum",
        "Letter % Chance": "prod"
    }).reset_index()

    result_df.columns = ["7 letter word", "Total Points", "% Chance"]


    result_df = result_df[result_df["% Chance"] > 0]

    result_df["Likelihood Rank"] = result_df["% Chance"].rank(
        method="dense", ascending=False).astype(int)

    result_df["Points Rank"] = result_df["Total Points"].rank(
        method="dense", ascending=False).astype(int)

    output_df = result_df[["Points Rank", "Likelihood Rank",
                           "7 letter word", "% Chance", "Total Points"]].copy()

    output_df = output_df.sort_values(
        ["Points Rank", "Likelihood Rank", "7 letter word"]).reset_index(drop=True)

    return {
        "output_01.csv": output_df
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
