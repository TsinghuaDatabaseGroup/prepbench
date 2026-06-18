from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the PrepBench dataset layout.")
    parser.add_argument("--data-root", default="data", help="Path to data/case_xxx directories.")
    parser.add_argument(
        "--gt-root",
        default="src/evaluate/gt",
        help="Path to ground-truth case directories.",
    )
    parser.add_argument("--expected-cases", type=int, default=306)
    return parser.parse_args()


def read_json_object(path: Path, errors: list[str]) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return
    if not isinstance(data, dict):
        errors.append(f"{path}: expected a JSON object")


def case_sort_key(path: Path) -> int:
    try:
        return int(path.name.split("_", 1)[1])
    except Exception:
        return 10**9


def main() -> int:
    args = parse_args()
    data_root = Path(args.data_root)
    gt_root = Path(args.gt_root)
    errors: list[str] = []

    if not data_root.is_dir():
        errors.append(f"missing data root: {data_root}")
        cases: list[Path] = []
    else:
        cases = sorted(
            [path for path in data_root.glob("case_*") if path.is_dir()],
            key=case_sort_key,
        )

    if not gt_root.is_dir():
        errors.append(f"missing GT root: {gt_root}")
        gt_cases: list[Path] = []
    else:
        gt_cases = sorted(
            [path for path in gt_root.glob("case_*") if path.is_dir()],
            key=case_sort_key,
        )

    case_names = {path.name for path in cases}
    gt_case_names = {path.name for path in gt_cases}
    input_table_count = 0

    if len(cases) != args.expected_cases:
        errors.append(f"expected {args.expected_cases} data cases, found {len(cases)}")
    if len(gt_cases) != args.expected_cases:
        errors.append(f"expected {args.expected_cases} GT cases, found {len(gt_cases)}")

    expected_names = {f"case_{idx:03d}" for idx in range(1, args.expected_cases + 1)}
    missing_data_cases = sorted(expected_names - case_names)
    missing_gt_cases = sorted(expected_names - gt_case_names)
    extra_data_cases = sorted(case_names - expected_names)
    extra_gt_cases = sorted(gt_case_names - expected_names)

    if missing_data_cases:
        errors.append(f"missing data cases: {', '.join(missing_data_cases[:10])}")
    if missing_gt_cases:
        errors.append(f"missing GT cases: {', '.join(missing_gt_cases[:10])}")
    if extra_data_cases:
        errors.append(f"extra data cases: {', '.join(extra_data_cases[:10])}")
    if extra_gt_cases:
        errors.append(f"extra GT cases: {', '.join(extra_gt_cases[:10])}")

    for case_dir in cases:
        for name in ("query.md", "query_full.md", "amb_kb.json"):
            path = case_dir / name
            if not path.is_file():
                errors.append(f"{case_dir}: missing {name}")
        amb_kb_path = case_dir / "amb_kb.json"
        if amb_kb_path.is_file():
            read_json_object(amb_kb_path, errors)

        input_dir = case_dir / "inputs"
        if not input_dir.is_dir():
            errors.append(f"{case_dir}: missing inputs/")
            continue
        csv_files = sorted(input_dir.glob("*.csv"))
        input_table_count += len(csv_files)
        if not csv_files:
            errors.append(f"{case_dir}: no input CSV files")

    for gt_case_dir in gt_cases:
        config_path = gt_case_dir / "config.json"
        if not config_path.is_file():
            errors.append(f"{gt_case_dir}: missing config.json")
        else:
            read_json_object(config_path, errors)
        if not sorted(gt_case_dir.glob("output_*.csv")):
            errors.append(f"{gt_case_dir}: no output CSV files")

    print(
        f"cases={len(cases)} input_tables={input_table_count} "
        f"gt_cases={len(gt_cases)} errors={len(errors)}"
    )
    for error in errors:
        print(f"ERROR: {error}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
