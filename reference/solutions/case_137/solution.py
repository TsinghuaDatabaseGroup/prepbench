from pathlib import Path
from typing import Dict, List
import re
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    films_path = inputs_dir / "input_01.csv"
    trilogies_path = inputs_dir / "input_02.csv"

    df_films = pd.read_csv(films_path)
    df_trilogies = pd.read_csv(trilogies_path)

    order_split = df_films["Number in Series"].str.split("/", expand=True)
    df_films["Film Order"] = order_split[0].astype(int)
    df_films["Total Films in Series"] = order_split[1].astype(int)
    df_films["Rating"] = pd.to_numeric(df_films["Rating"], errors="coerce")

    df_trilogies["Trilogy_clean"] = (
        df_trilogies["Trilogy"].str.replace(
            r"\s*trilogy$", "", regex=True).str.strip()
    )


    name_to_title_patterns: dict[str, List[str]] = {
        "Lord of the Rings": [r"Lord of the Rings"],
        "The Godfather": [r"Godfather"],
        "The Dark Knight": [r"Dark Knight|Batman Begins"],
        "Dollars": [r"Dollars|Good, the Bad and the Ugly"],
        "Once Upon a Time": [r"Once Upon a Time in the West|Once Upon a Time in America|Fistful of Dynamite"],
        "Toy Story": [r"Toy Story"],
        "The Before": [r"Before (Sunrise|Sunset|Midnight)"],
        "Back to the Future": [r"Back to the Future"],
        "The Vengeance": [r"Vengeance|Oldboy|Chinjeolhan"],
        "Three Colours": [r"Three Colou?rs?:? (Blue|White|Red)"],
        "Death": [r"Babel|21 Grams|Love's a Bitch"],
        "The Hobbit": [r"Hobbit"],
        "Three Flavours Cornetto": [r"Shaun of the Dead|Hot Fuzz|World's End"],
        "Matrix": [r"Matrix"],
        "Evil Dead": [r"Evil Dead|Army of Darkness"],
        "Captain America": [r"Captain America"],
        "Millennium": [r"Dragon Tattoo|Played with Fire|Hornets' Nest"],
        "Iron Man": [r"Iron Man"],
        "X-Men": [r"^X-Men"],
        "Wolverine": [r"Wolverine|Logan"],
        "Ocean's": [r"^Ocean's"],
        "Mad Max": [r"^Mad Max"],
        "The Naked Gun": [r"Naked Gun"],
        "Spider-Man": [r"Spider-Man"],
        "Madagascar": [r"^Madagascar"],
        "Mexico": [r"El mariachi|Desperado|Once Upon a Time in Mexico"],
        "MIB": [r"Men in Black"],
        "Star Wars": [r"Star Wars: (Return of the Jedi|Episode IV|Episode V)"],
        "Prequel": [r"Star Wars: Episode (I|II|III)"]
    }

    def select_group_and_rows(trilogy_name: str) -> pd.DataFrame:
        patterns = name_to_title_patterns.get(
            trilogy_name, [re.escape(trilogy_name)])
        best_gid = None
        best_hits = -1
        best_rows = None
        for gid, sub in df_films.groupby("Trilogy Grouping"):
            mask = pd.Series(False, index=sub.index)
            for pat in patterns:
                mask = mask | sub["Title"].str.contains(
                    pat, case=False, regex=True, na=False)
            hits = mask.sum()
            if hits > best_hits:
                best_hits = hits
                best_gid = gid
                best_rows = sub[mask].copy()
        if best_rows is None or best_rows.empty:
            any_mask = pd.Series(False, index=df_films.index)
            for pat in patterns:
                any_mask = any_mask | df_films["Title"].str.contains(
                    pat, case=False, regex=True, na=False)
            best_rows = df_films[any_mask].copy()
        if best_gid is not None:
            group_full = df_films[df_films["Trilogy Grouping"]
                                  == best_gid].copy()
            matched_ids = set(best_rows.index)
            group_full = group_full.assign(
                __matched=group_full.index.isin(matched_ids).astype(int))
            group_full = group_full.sort_values(
                ["__matched", "Film Order", "Title"], ascending=[False, True, True])
            if best_rows.shape[0] >= 3:
                selected = best_rows.sort_values(
                    ["Film Order", "Title"]).head(3).copy()
            else:
                selected = group_full.head(3).copy()
        else:
            selected = best_rows.sort_values(
                ["Film Order", "Title"]).head(3).copy()
        return selected

    records = []
    for _, row in df_trilogies.sort_values("Trilogy Ranking").iterrows():
        tri_rank = int(row["Trilogy Ranking"])
        tri_clean = row["Trilogy_clean"]
        sub = select_group_and_rows(tri_clean)
        tri_avg = round(sub["Rating"].mean(), 1)
        sub = sub.assign(**{
            "Trilogy Ranking": tri_rank,
            "Trilogy": tri_clean,
            "Trilogy Average": tri_avg,
        })
        sub = sub[[
            "Trilogy Ranking",
            "Trilogy",
            "Trilogy Average",
            "Film Order",
            "Title",
            "Rating",
            "Total Films in Series",
        ]]
        records.append(sub)

    out_df = pd.concat(records, ignore_index=True)
    out_df = out_df.sort_values(
        ["Trilogy Ranking", "Film Order", "Title"]).reset_index(drop=True)

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        df.to_csv((cand_dir / fname), index=False, encoding="utf-8")
