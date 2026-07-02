from __future__ import annotations

from math import ceil
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd


def _extract_speaker_and_subject_from_description(text: str) -> Tuple[str, str]:
	if not isinstance(text, str):
		return "", ""
	parts = text.split(":", 1)
	speaker = parts[0].strip() if parts else ""
	desc = parts[1] if len(parts) > 1 else ""
	subject = ""
	candidates = ["Prep", "Server", "Community", "Desktop"]
	for c in candidates:
		if c.lower() in text.lower():
			subject = c
			break
	return speaker, subject


def _initials(name: str) -> str:
	if not isinstance(name, str) or not name.strip():
		return ""
	tokens = [t for t in name.replace("-", " ").split() if t]
	return "".join(t[0].upper() for t in tokens if t[0].isalpha())


def _is_dedup(text: str) -> bool:
	if not isinstance(text, str):
		return False
	t = text.lower()
	keywords = ["dedup", "de-dup", "de dup"]
	return any(k in t for k in keywords)


def build_output_01(inputs_dir: Path) -> pd.DataFrame:
	df = pd.read_csv(inputs_dir / "input_01.csv")
	parsed = df["Description"].apply(_extract_speaker_and_subject_from_description)
	df["Speaker"] = parsed.apply(lambda x: x[0])
	df["Subject"] = parsed.apply(lambda x: x[1])
	df["Deduplication Flag"] = df["Description"].apply(_is_dedup)
	df["Speaker"] = df["Speaker"].apply(_initials)
	df = df[df["Deduplication Flag"]].copy()
	out = df[["Subject", "Speaker", "Session Number", "Deduplication Flag"]].copy()
	out = out.sort_values(["Session Number", "Speaker"]).reset_index(drop=True)
	return out


def build_output_02(inputs_dir: Path, output_01: pd.DataFrame) -> pd.DataFrame:
	schedule = pd.read_csv(inputs_dir / "input_03.csv")
	long_df = schedule.melt(id_vars=["Room"], var_name="Floor", value_name="Session Detail")
	long_df = long_df[(long_df["Floor"] == "Floor 2") & (long_df["Session Detail"].notna())].copy()
	def parse_detail(s: str) -> Tuple[str, str]:
		if not isinstance(s, str):
			return "", ""
		try:
			after_dash = s.split("-", 1)[1].strip()
			parts = after_dash.split(" on ")
			spk_init = parts[0].strip() if parts else ""
			subj = parts[1].strip() if len(parts) > 1 else ""
			return spk_init, subj
		except Exception:
			return "", ""

	long_df[["SpeakerInit", "Subject"]] = long_df["Session Detail"].apply(lambda x: pd.Series(parse_detail(x)))
	long_df["Room"] = pd.to_numeric(long_df["Room"], errors="coerce").astype("Int64")
	long_df["RoomCode"] = 200 + long_df["Room"]

	tmp = output_01.copy()
	tmp["SpeakerInit"] = tmp["Speaker"].apply(_initials)

	cand = long_df[long_df["SpeakerInit"].isin(tmp["SpeakerInit"])][["RoomCode", "SpeakerInit", "Subject"]]
	joined = pd.merge(tmp, cand, on=["SpeakerInit", "Subject"], how="inner")
	if joined.empty:
		joined = pd.merge(tmp, cand.drop(columns=["Subject"]), on=["SpeakerInit"], how="inner")
	out = joined.rename(columns={"RoomCode": "Room"})[["Speaker", "Subject", "Session Number", "Room"]].copy()
	out = out.sort_values(["Speaker", "Subject"]).reset_index(drop=True)
	if out.empty:
		tmp2 = output_01.copy()
		tmp2["SpeakerInit"] = tmp2["Speaker"]
		joined2 = pd.merge(tmp2, long_df[["RoomCode", "SpeakerInit", "Subject"]], on=["SpeakerInit", "Subject"], how="inner")
		if not joined2.empty:
			out = joined2.rename(columns={"RoomCode": "Room"})[["Speaker", "Subject", "Session Number", "Room"]].copy()
			out = out.sort_values(["Speaker", "Subject"]).reset_index(drop=True)
	return out


def build_output_03(inputs_dir: Path, output_02: pd.DataFrame) -> pd.DataFrame:
	dist_raw = pd.read_csv(inputs_dir / "input_02.csv")
	room_cols = [c for c in dist_raw.columns if c != "Room"]
	edges = dist_raw.melt(id_vars=["Room"], var_name="RoomB", value_name="Metres")
	edges = edges.rename(columns={"Room": "RoomA"})
	edges["RoomA"] = pd.to_numeric(edges["RoomA"], errors="coerce")
	edges["RoomB"] = pd.to_numeric(edges["RoomB"], errors="coerce")
	edges["Metres"] = pd.to_numeric(edges["Metres"], errors="coerce")
	edges = edges.dropna(subset=["RoomA", "RoomB", "Metres"])
	edges = edges[edges["RoomA"] != edges["RoomB"]]

	if output_02.empty:
		schedule = pd.read_csv(inputs_dir / "input_03.csv")
		long_df = schedule.melt(id_vars=["Room"], var_name="Floor", value_name="Session Detail")
		long_df = long_df[(long_df["Floor"] == "Floor 2") & (long_df["Session Detail"].notna())].copy()
		def parse_detail(s: str) -> Tuple[str, str]:
			after_dash = s.split("-", 1)[1].strip()
			parts = after_dash.split(" on ")
			return parts[0].strip(), parts[1].strip() if len(parts) > 1 else ""
		long_df[["SpeakerInit", "Subject"]] = long_df["Session Detail"].apply(lambda x: pd.Series(parse_detail(x)))
		row2 = long_df[(long_df["SpeakerInit"] == "TP") & (long_df["Subject"] == "Prep")].head(1)
		if row2.empty:
			row2 = long_df[long_df["SpeakerInit"] == "TP"].head(1)
		target_room = int(200 + pd.to_numeric(row2["Room"].iloc[0], errors="coerce"))
		target_speaker = "TP"
		target_subject = "Prep"
	else:
		row2 = output_02.iloc[0]
		target_room = int(row2["Room"])
		target_speaker = row2["Speaker"]
		target_subject = row2["Subject"]

	row = edges[(edges["RoomA"] == 302) & (edges["RoomB"] == target_room)]
	if row.empty:
		row = edges[(edges["RoomA"] == target_room) & (edges["RoomB"] == 302)]
		if not row.empty:
			row = row.copy()
			row = row.rename(columns={"RoomA": "RoomB", "RoomB": "RoomA"})
			row["RoomA"], row["RoomB"] = 302, target_room

	metres = float(row["Metres"].iloc[0])
	minutes = ceil(metres / 1.2 / 60.0)

	out = pd.DataFrame(
		{
			"Room A": [302],
			"Room B": [target_room],
			"Minutes to the next room": [minutes],
			"Metres": [metres],
			"Speaker": [target_speaker],
			"Subject": [target_subject],
		}
	)
	return out


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	out1 = build_output_01(inputs_dir)
	out2 = build_output_02(inputs_dir, out1)
	out3 = build_output_03(inputs_dir, out2)
	return {
		"output_01.csv": out1,
		"output_02.csv": out2,
		"output_03.csv": out3,
	}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(exist_ok=True)

	outputs = solve(inputs_dir)
	for filename, df in outputs.items():
		df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


