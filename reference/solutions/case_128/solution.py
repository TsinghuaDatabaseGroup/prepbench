from __future__ import annotations
from pathlib import Path
from typing import Dict
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    sched_fp = inputs_dir / "input_01.csv"
    venue_fp = inputs_dir / "input_02.csv"

    df = pd.read_csv(sched_fp)
    venues = pd.read_csv(venue_fp)
    
    def clean_venue_sport(s: str) -> str:
        s = str(s).strip()
        s = s.replace('\xa0', ' ').strip()
        while s.endswith('.'):
            s = s[:-1].strip()
        s = " ".join(s.split())
        return s
    
    venues["Sport"] = venues["Sport"].apply(clean_venue_sport)

    def split_location(loc: str):
        if pd.isna(loc):
            return pd.NA, pd.NA
        parts = [p.strip() for p in str(loc).split(",")]
        if len(parts) != 2:
            return pd.NA, pd.NA
        try:
            lat = float(parts[0])
            lon = float(parts[1])
        except Exception:
            return pd.NA, pd.NA
        return lat, lon

    venues[["Latitude", "Longitude"]] = venues["Location"].apply(
        lambda x: pd.Series(split_location(x)))
    venues = venues.drop(columns=["Location"])

    def norm(s: str) -> str:
        s = " ".join(str(s).split()).strip().lower()
        s = s.replace(".", "")
        return s
    venues["_sport_norm"] = venues["Sport"].apply(norm)
    venues["_venue_norm"] = venues["Venue"].apply(norm)

    suffixes = ["st", "nd", "rd", "th"]

    def parse_date(d: str) -> datetime:
        d = str(d).replace("_", " ")
        parts = d.split(" ")
        if len(parts) >= 1:
            day = parts[0]
            for s in suffixes:
                day = day.replace(s, "")
            parts[0] = day
        clean = " ".join(parts)
        return datetime.strptime(clean, "%d %B %Y")

    def to_uk_text(d: datetime, t: str) -> tuple[int, str]:
        t = str(t).strip()
        try:
            if ":" in t:
                hh, mm = t.split(":", 1)
                hh = hh.zfill(2)
                mm = mm.zfill(2)
            else:
                raise ValueError("invalid time")
        except Exception:
            hh, mm = "00", "00"
        base = datetime(1899, 12, 30)
        serial = (d.date() - base.date()).days
        txt = f"{serial} days {hh}:{mm}:00"
        return serial, txt

    def split_events(s: str):
        if pd.isna(s):
            return [""]
        s = str(s).strip()
        if s == "-":
            return ["-"]
        if s == "":
            return [""]
        parts = [p.strip() for p in s.split(",") if p.strip() != ""]
        return parts if parts else [""]

    def clean_sport_name(s: str) -> str:
        s = str(s).strip()
        while s.endswith('.'):
            s = s[:-1].strip()
        s = " ".join(s.split())
        s = s.replace('\xa0', ' ').strip()
        if s in ['Baseball', 'Softball', 'Softball/Baseball']:
            s = 'Baseball/Softball'
        elif s in ['Beach Volley', 'Beach Volleybal']:
            s = 'Beach Volleyball'
        elif s == 'Artistic Gymnastic':
            s = 'Artistic Gymnastics'
        elif s == 'boxing':
            s = 'Boxing'
        elif s == 'Rugby':
            s = 'rugby'
        return s
    
    df["Sport"] = df["Sport"].apply(clean_sport_name)
    
    df["_DateParsed"] = df["Date"].apply(parse_date)
    df = df.assign(Events_Split_List=df["Events"].apply(split_events))
    df = df.explode("Events_Split_List", ignore_index=True)
    df["Sport_orig"] = df["Sport"].astype(str)

    uk_dt_info = df.apply(lambda r: to_uk_text(
        r["_DateParsed"], str(r["Time"])), axis=1, result_type="expand")
    df["_UK_DT"], df["UK Date Time"] = uk_dt_info[0], uk_dt_info[1]

    def norm(s: str) -> str:
        s = " ".join(str(s).split()).strip().lower()
        s = s.replace(".", "")
        return s

    sport_fix = {
        "softball/baseball": "baseball/softball",
        "beach volleyball": "beach volleyball",
    }

    def fix_sport(s: str) -> str:
        ns = norm(s)
        ns = sport_fix.get(ns, ns)
        return ns

    df["_sport_norm"] = df["Sport"].apply(fix_sport)
    df["_venue_norm"] = df["Venue"].apply(norm)
    
    df["_sport_original"] = df["Sport"].astype(str)

    def sport_group(s: str) -> str:
        s = str(s).strip()
        if s == "Baseball/Softball":
            return "Baseball"
        if s == "Artistic Gymnastics":
            return "Gymnastics"
        if s == "Trampoline Gymnastics":
            return "Gymnastics"
        if s == "Rhythmic Gymnastics":
            return "Rhythmic Gymnastics"
        if s in {"Artistic Swimming", "Swimming", "Marathon Swimming"}:
            return "Swimming"
        if s == "Diving":
            return "Diving"
        if s == "Water Polo":
            return "Water Polo"
        if s in {"Canoe Sprint", "Canoe Slalom"}:
            return "Canoeing"
        if s in {"Judo", "Karate", "Taekwondo"}:
            return "Martial Arts"
        if s == "Wrestling":
            return "Wrestling"
        if s == "Boxing":
            return "Boxing"
        if "Cycling" in s:
            return "Cycling"
        if s in {"3x3 Basketball", "Basketball"}:
            return "Basketball"
        if s == "Beach Volleyball":
            return "Volleyball"
        if s == "Volleyball":
            return "Volleyball"
        if s == "Table Tennis":
            return "Tennis"
        if s == "Tennis":
            return "Tennis"
        if "Ceremony" in s:
            return "Ceremony"
        if s == "Archery":
            return "Archery"
        if s == "Athletics":
            return "Athletics"
        if s == "Badminton":
            return "Badminton"
        if s == "Equestrian":
            return "Equestrian"
        if s == "Fencing":
            return "Fencing"
        if s == "Football":
            return "Football"
        if s == "Golf":
            return "Golf"
        if s == "Handball":
            return "Handball"
        if s == "Hockey":
            return "Hockey"
        if s == "Modern Pentathlon":
            return "Modern Pentathlon"
        if s == "Rowing":
            return "Rowing"
        if s == "Sailing":
            return "Sailing"
        if s == "Shooting":
            return "Shooting"
        if s == "Skateboarding":
            return "Skateboarding"
        if s == "Sport Climbing":
            return "Sport Climbing"
        if s == "Surfing":
            return "Surfing"
        if s == "Triathlon":
            return "Triathlon"
        if s == "Weightlifting":
            return "Weightlifting"
        if s == "diving":
            return "diving"
        if s == "football":
            return "football"
        if s == "rugby":
            return "Rugby"
        if s == "volleyball":
            return "Volleyball"
        if s == "Diving":
            return "Diving"
        if s == "Football":
            return "Football"
        return s

    def is_medal_event(e: str) -> bool:
        s = str(e).lower()
        return ("victory ceremony" in s) or ("gold medal" in s)

    df["Medal Ceremony?"] = df["Events_Split_List"].apply(is_medal_event)

    df = df.rename(columns={
        "Events_Split_List": "Events Split",
    })

    venues_key = venues[["_sport_norm", "_venue_norm", "Sport", "Venue", "Latitude", "Longitude"]].rename(
        columns={"Sport": "Sport_canon", "Venue": "Venue_canon"}
    )
    out = df.merge(
        venues_key,
        how="left",
        left_on=["_sport_norm", "_venue_norm"],
        right_on=["_sport_norm", "_venue_norm"],
        validate="m:1",
    )

    def clean_sport_text(s: str) -> str:
        s = str(s).strip()
        while s.endswith('.'):
            s = s[:-1].strip()
        s = " ".join(s.split())
        return s

    import numpy as np
    sport_from_orig = out["Sport_orig"].apply(clean_sport_text)
    
    is_lowercase = out["_sport_original"].str[0].str.islower()
    
    sport_pref = out["Sport_canon"].fillna(sport_from_orig)
    out["Sport"] = np.where(is_lowercase, sport_from_orig, sport_pref)

    out["Sport Group"] = out["Sport"].apply(sport_group)

    out["Date"] = pd.to_datetime(out["_DateParsed"]).dt.date

    out = out[[
        "Latitude",
        "Longitude",
        "Medal Ceremony?",
        "Sport Group",
        "Events Split",
        "UK Date Time",
        "Date",
        "Sport",
        "Venue",
    ]]

    out = out.sort_values(by=["UK Date Time", "Sport", "Venue",
                          "Events Split"], kind="mergesort").reset_index(drop=True)

    out["Latitude"] = pd.to_numeric(out["Latitude"], errors="coerce")
    out["Longitude"] = pd.to_numeric(out["Longitude"], errors="coerce")
    out["Medal Ceremony?"] = out["Medal Ceremony?"].astype(bool)
    for c in ["Sport Group", "Events Split", "UK Date Time", "Sport", "Venue"]:
        out[c] = out[c].astype(str)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, d in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        d.to_csv(cand_dir / fname, index=False, encoding="utf-8")
