from pathlib import Path

import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    inputs_dir = Path(inputs_dir)

    gigs = pd.read_csv(inputs_dir / "input_02.csv")
    longlats = pd.read_csv(inputs_dir / "input_01.csv")
    homes = pd.read_csv(inputs_dir / "input_03.csv")

    invisible_chars = ["\u00ad", "\u200b", "\ufeff"]

    def clean_text(series: pd.Series) -> pd.Series:
        series = series.fillna("").astype(str).str.strip()
        for char in invisible_chars:
            series = series.str.replace(char, "", regex=False)
        return series

    longlats = longlats.assign(
        Location=clean_text(longlats["Location"])
    )
    coords = longlats["LongLats"].str.split(",", n=1, expand=True)
    longlats = longlats.assign(
        Latitude=pd.to_numeric(coords[0].str.strip(), errors="coerce"),
        Longitude=pd.to_numeric(coords[1].str.strip(), errors="coerce"),
    ).drop(columns=["LongLats"]).drop_duplicates(subset=["Location"], keep="first")

    gigs = gigs.assign(
        Concert=gigs["Concert"].fillna("").astype(str).str.strip(),
        Artist=clean_text(gigs["Artist"]),
        Venue=clean_text(gigs["Venue"]),
        Location=clean_text(gigs["Location"]),
    )

    concerts = gigs["Concert"]
    artists = gigs["Artist"]
    parts = concerts.str.split("/", expand=True)
    parts = parts.apply(lambda col: col.str.strip())
    has_slash = concerts.str.contains("/", regex=False)
    need_blank = has_slash & ~parts.eq("").any(axis=1)
    parts.insert(0, "_blank", pd.Series("", index=parts.index))
    parts.loc[~need_blank, "_blank"] = pd.NA

    stacked = parts.stack().str.strip()
    row_pos = stacked.index.get_level_values(0).to_numpy()
    slash_mask = has_slash.to_numpy()[row_pos]
    stacked = stacked.where(slash_mask, "")
    artist_index = artists.reindex(stacked.index.get_level_values(0))
    stacked = stacked.mask(stacked.to_numpy() == artist_index.to_numpy(), "")

    exploded = (
        gigs.loc[stacked.index.get_level_values(0)]
        .assign(**{"Fellow Artists": stacked.values})
        .reset_index(drop=True)
    )

    gigs_with_coords = exploded.merge(
        longlats, on="Location", how="left", sort=False)

    homes = homes.rename(
        columns={"Longitude": "Home Longitude", "Latitude": "Home Latitude"}
    )
    homes["Artist"] = clean_text(homes["Artist"])
    homes["Hometown"] = clean_text(homes["Hometown"])
    homes["Home Longitude"] = pd.to_numeric(
        homes["Home Longitude"], errors="coerce")
    homes["Home Latitude"] = pd.to_numeric(
        homes["Home Latitude"], errors="coerce")

    enriched = gigs_with_coords.merge(
        homes, on="Artist", how="inner", sort=False)

    enriched["Longitude"] = pd.to_numeric(
        enriched["Longitude"], errors="coerce")
    enriched["Latitude"] = pd.to_numeric(enriched["Latitude"], errors="coerce")
    enriched = enriched.dropna(subset=["Longitude", "Latitude"])
    concert_dates = pd.to_datetime(enriched["Concert Date"], errors="coerce")
    enriched["Concert Date"] = concert_dates.dt.strftime("%d/%m/%Y").fillna("")
    enriched["Fellow Artists"] = enriched["Fellow Artists"].fillna("")

    output_cols = [
        "Longitude",
        "Latitude",
        "Fellow Artists",
        "Artist",
        "Concert Date",
        "Concert",
        "Venue",
        "Location",
        "Hometown",
        "Home Longitude",
        "Home Latitude",
    ]
    base_output = enriched[output_cols].drop_duplicates(
        subset=output_cols, keep="first")

    preference_map = {
        "red tour": ["RED Tour", "Red Tour", "RED tour"],
        "divide tour": ["Divide tour", "Divide Tour"],
        "x tour": ["x Tour", "X Tour", "X tour"],
        "the red tour": ["The Red Tour", "The RED TOUR"],
    }
    key_without_concert = [col for col in output_cols if col != "Concert"]
    keep_mask = pd.Series(False, index=base_output.index)
    for _, group in base_output.groupby(key_without_concert, sort=False):
        if len(group) == 1:
            keep_mask.loc[group.index[0]] = True
            continue
        lowered = group["Concert"].str.lower()
        if lowered.nunique() == 1:
            norm = lowered.iloc[0]
            chosen_idx = None
            for candidate in preference_map.get(norm, []):
                match = group[group["Concert"] == candidate]
                if not match.empty:
                    chosen_idx = match.index[0]
                    break
            if chosen_idx is None:
                chosen_idx = group.index[0]
            keep_mask.loc[chosen_idx] = True
        else:
            keep_mask.loc[group.index] = True

    final = base_output[keep_mask].reset_index(drop=True)

    return {"output_01.csv": final}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False)
