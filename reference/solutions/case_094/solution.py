from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd


@dataclass
class Flight:
    flight_no: str
    stand: int
    start: pd.Timestamp
    accessible_gates: List[int]
    requires_bus: bool


def _parse_time_value(value: int | str) -> pd.Timestamp:

    value_str = str(value).zfill(4)
    hour = int(value_str[:2])
    minute = int(value_str[2:])
    return pd.Timestamp(2020, 2, 1, hour, minute)


def _expand_stands(stands_df: pd.DataFrame) -> pd.DataFrame:
    expanded = (
        stands_df.assign(
            Stand=stands_df["Stand"].str.lstrip("S").astype(int),
            _requires_bus=stands_df["Requires Bus?"].str.upper().eq("Y"),
            _gates=stands_df["Accessed by Gates"].str.split(","),
        )
        .explode("_gates")
        .assign(
            Gate=lambda df: df["_gates"].str.strip(
            ).str.lstrip("G").astype(int),
            **{"Requires Bus?": lambda df: df["_requires_bus"]},
        )
        [["Stand", "Gate", "Requires Bus?"]]
    )
    return expanded


def _build_flights(alloc_df: pd.DataFrame, stand_access: pd.DataFrame) -> List[Flight]:
    gate_map = (
        stand_access.groupby("Stand")["Gate"].apply(
            lambda s: sorted(set(s))).to_dict()
    )
    bus_map = (
        stand_access.groupby("Stand")["Requires Bus?"].any().to_dict()
    )

    flights: List[Flight] = []
    for _, row in alloc_df.iterrows():
        stand = int(row["Stand"])
        start = _parse_time_value(row["Time"])
        flight_no = str(row["Flight"])
        accessible = gate_map[stand]
        flights.append(
            Flight(
                flight_no=flight_no,
                stand=stand,
                start=start,
                accessible_gates=accessible,
                requires_bus=bus_map[stand],
            )
        )

    return flights


def _generate_time_slots(start: pd.Timestamp, duration_minutes: int = 45) -> List[pd.Timestamp]:
    return [start + pd.Timedelta(minutes=offset) for offset in (0, 15, 30)]


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    stands_df = pd.read_csv(inputs_dir / "input_01.csv")
    remote_df = pd.read_csv(inputs_dir / "input_02.csv")
    allocations_df = pd.read_csv(inputs_dir / "input_03.csv")
    availability_df = pd.read_csv(inputs_dir / "input_04.csv")

    stand_access = _expand_stands(stands_df)
    remote_time_map = {
        int(row["Gate"].lstrip("G")): int(row["Time to Reach Remote Stands"])
        for _, row in remote_df.iterrows()
    }

    flights = _build_flights(allocations_df, stand_access)

    def _category(f: Flight) -> str:
        if len(f.accessible_gates) == 1:
            return "unique"
        if f.requires_bus:
            return "remote"
        return "remaining"

    order_by_category = {"unique": 0, "remote": 1, "remaining": 2}
    flights.sort(key=lambda f: (
        order_by_category[_category(f)], f.start, f.flight_no))

    availability_df["Gate"] = availability_df["Gate"].astype(int)
    availability_df["Date"] = pd.to_datetime(availability_df["Date"])

    gate_slots: Dict[int, Dict[pd.Timestamp, dict]] = {
        gate: {date: {} for date in group["Date"]}
        for gate, group in availability_df.groupby("Gate")
    }

    def _gate_has_slots(gate: int, slots: Iterable[pd.Timestamp]) -> bool:
        gate_map = gate_slots[gate]
        return all(slot in gate_map and not gate_map[slot] for slot in slots)

    def _book_slots(
        gate: int,
        slots: Iterable[pd.Timestamp],
        stand: int,
        flight: str,
        requires_bus: bool,
    ) -> None:
        time_to_stand = remote_time_map[gate] if requires_bus else 0
        gate_map = gate_slots[gate]
        for slot in slots:
            gate_map[slot] = {
                "Stand": stand,
                "Flight": flight,
                "Requires Bus?": "Y" if requires_bus else "N",
                "Time to Reach Stand": time_to_stand,
            }

    gate_ordering = {
        "unique": lambda f: f.accessible_gates,
        "remote": lambda f: sorted(
            f.accessible_gates, key=lambda g: (remote_time_map[g], g)
        ),
        "remaining": lambda f: sorted(
            f.accessible_gates, key=lambda g: (-remote_time_map[g], g)
        ),
    }

    for flight in flights:
        slots = _generate_time_slots(flight.start)
        gate_order = gate_ordering[_category(flight)](flight)
        chosen_gate = next(
            (g for g in gate_order if _gate_has_slots(g, slots)), None)

        if chosen_gate is None:
            raise ValueError(
                f"No available gate for flight {flight.flight_no}")

        _book_slots(chosen_gate, slots, flight.stand,
                    flight.flight_no, flight.requires_bus)

    records = [
        {
            "Gate": gate,
            "Stand": entry.get("Stand") if entry else pd.NA,
            "Date": slot,
            "Flight": entry.get("Flight") if entry else pd.NA,
            "Requires Bus?": entry.get("Requires Bus?") if entry else pd.NA,
            "Time to Reach Stand": entry.get("Time to Reach Stand") if entry else pd.NA,
        }
        for gate in sorted(gate_slots)
        for slot, entry in sorted(gate_slots[gate].items())
    ]

    result_df = pd.DataFrame.from_records(records)

    result_df["Gate"] = result_df["Gate"].astype(int)
    result_df["Date"] = pd.to_datetime(result_df["Date"])

    return {"output_01.csv": result_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
