from pathlib import Path

import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_films = pd.read_csv(inputs_dir / "input_01.csv")
    df_trilogies = pd.read_csv(inputs_dir / "input_02.csv")

    order_split = df_films["Number in Series"].str.split("/", expand=True)
    df_films["Film Order"] = order_split[0].astype(int)
    df_films["Total Films in Series"] = order_split[1].astype(int)
    df_films["Rating"] = pd.to_numeric(df_films["Rating"], errors="coerce")

    group_stats = (
        df_films.groupby("Trilogy Grouping", as_index=False)
        .agg(
            Trilogy_Average_Raw=("Rating", "mean"),
            Highest_Rating=("Rating", "max"),
        )
        .sort_values(
            ["Trilogy_Average_Raw", "Highest_Rating", "Trilogy Grouping"],
            ascending=[False, False, True],
        )
        .reset_index(drop=True)
    )
    group_stats["Trilogy Ranking"] = group_stats.index + 1
    group_stats["Trilogy Average"] = group_stats["Trilogy_Average_Raw"].round(1)

    df_trilogies["Trilogy"] = (
        df_trilogies["Trilogy"]
        .str.replace(r"\s*trilogy$", "", regex=True, case=False)
        .str.strip()
    )

    films_ranked = df_films.merge(
        group_stats[["Trilogy Grouping", "Trilogy Ranking", "Trilogy Average"]],
        on="Trilogy Grouping",
        how="left",
        validate="many_to_one",
    )
    out_df = films_ranked.merge(
        df_trilogies[["Trilogy Ranking", "Trilogy"]],
        on="Trilogy Ranking",
        how="inner",
        validate="many_to_one",
    )

    out_df = out_df[[
        "Trilogy Ranking",
        "Trilogy",
        "Trilogy Average",
        "Film Order",
        "Title",
        "Rating",
        "Total Films in Series",
    ]]
    out_df = out_df.sort_values(
        ["Trilogy Ranking", "Film Order", "Title"]
    ).reset_index(drop=True)

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        df.to_csv((cand_dir / fname), index=False, encoding="utf-8")
