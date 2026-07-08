from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from evaluate.config import ConfigError, load_config
from evaluate.io_utils import read_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the PrepBench dataset layout.")
    parser.add_argument("--data-root", default="data", help="Path to data/case_xxx directories.")
    parser.add_argument(
        "--gt-root",
        default="src/evaluate/gt",
        help="Path to ground-truth case directories.",
    )
    parser.add_argument(
        "--solutions-root",
        default="reference/solutions",
        help="Path to public reference-solution case directories.",
    )
    parser.add_argument(
        "--case-links",
        default="data/case_links.txt",
        help="Path to one source URL per benchmark case.",
    )
    parser.add_argument("--expected-cases", type=int, default=306)
    return parser.parse_args()


def read_json_object(path: Path, errors: list[str]) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{path}: expected a JSON object")
        return None
    return data


def validate_gt_config(gt_case_dir: Path, config_path: Path, errors: list[str]) -> None:
    try:
        cfg = load_config(str(config_path))
    except ConfigError as exc:
        errors.append(f"{config_path}: {exc}")
        return

    configured_files = set(cfg.get("files", {}))
    output_files = {path.name for path in gt_case_dir.glob("output_*.csv")}
    missing_cfg = sorted(output_files - configured_files)
    extra_cfg = sorted(configured_files - output_files)
    if missing_cfg:
        errors.append(f"{config_path}: missing config entries for outputs: {', '.join(missing_cfg[:10])}")
    if extra_cfg:
        errors.append(f"{config_path}: config entries without GT outputs: {', '.join(extra_cfg[:10])}")

    for filename, spec in cfg.get("files", {}).items():
        gt_path = gt_case_dir / filename
        if not gt_path.is_file():
            continue
        df = read_csv(gt_path)
        if df is None:
            errors.append(f"{gt_path}: failed to read GT CSV")
            continue

        gt_cols = set(df.columns)
        config_cols = set(spec.get("columns", {}))
        missing_cols = sorted(gt_cols - config_cols)
        extra_cols = sorted(config_cols - gt_cols)
        if missing_cols:
            errors.append(f"{config_path}: {filename} has GT columns missing from config: {missing_cols}")
        if extra_cols:
            errors.append(f"{config_path}: {filename} has config columns missing from GT: {extra_cols}")

        key_cols = spec.get("key", [])
        missing_key_cols = [col for col in key_cols if col not in config_cols]
        if missing_key_cols:
            errors.append(f"{config_path}: {filename} key columns missing from columns: {missing_key_cols}")


def case_sort_key(path: Path) -> int:
    try:
        return int(path.name.split("_", 1)[1])
    except Exception:
        return 10**9


def parse_case_link(line: str) -> str:
    value = line.strip()
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return value.strip()


def validate_case_links(path: Path, expected_cases: int, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing case links file: {path}")
        return

    raw_lines = path.read_text(encoding="utf-8").splitlines()
    links = [parse_case_link(line) for line in raw_lines if line.strip()]
    if len(links) != expected_cases:
        errors.append(f"{path}: expected {expected_cases} links, found {len(links)}")

    seen: dict[str, int] = {}
    for idx, link in enumerate(links, 1):
        parsed = urlparse(link)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"{path}:{idx}: invalid URL: {link}")
        previous_idx = seen.get(link)
        if previous_idx is not None:
            errors.append(f"{path}:{idx}: duplicate URL also used on line {previous_idx}: {link}")
        seen[link] = idx


def main() -> int:
    args = parse_args()
    data_root = Path(args.data_root)
    gt_root = Path(args.gt_root)
    solutions_root = Path(args.solutions_root)
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

    if not solutions_root.is_dir():
        errors.append(f"missing solutions root: {solutions_root}")
        solution_cases: list[Path] = []
    else:
        solution_cases = sorted(
            [path for path in solutions_root.glob("case_*") if path.is_dir()],
            key=case_sort_key,
        )

    case_names = {path.name for path in cases}
    gt_case_names = {path.name for path in gt_cases}
    solution_case_names = {path.name for path in solution_cases}
    input_table_count = 0

    if len(cases) != args.expected_cases:
        errors.append(f"expected {args.expected_cases} data cases, found {len(cases)}")
    if len(gt_cases) != args.expected_cases:
        errors.append(f"expected {args.expected_cases} GT cases, found {len(gt_cases)}")
    if len(solution_cases) != args.expected_cases:
        errors.append(f"expected {args.expected_cases} solution cases, found {len(solution_cases)}")

    validate_case_links(Path(args.case_links), args.expected_cases, errors)

    expected_names = {f"case_{idx:03d}" for idx in range(1, args.expected_cases + 1)}
    missing_data_cases = sorted(expected_names - case_names)
    missing_gt_cases = sorted(expected_names - gt_case_names)
    missing_solution_cases = sorted(expected_names - solution_case_names)
    extra_data_cases = sorted(case_names - expected_names)
    extra_gt_cases = sorted(gt_case_names - expected_names)
    extra_solution_cases = sorted(solution_case_names - expected_names)

    if missing_data_cases:
        errors.append(f"missing data cases: {', '.join(missing_data_cases[:10])}")
    if missing_gt_cases:
        errors.append(f"missing GT cases: {', '.join(missing_gt_cases[:10])}")
    if missing_solution_cases:
        errors.append(f"missing solution cases: {', '.join(missing_solution_cases[:10])}")
    if extra_data_cases:
        errors.append(f"extra data cases: {', '.join(extra_data_cases[:10])}")
    if extra_gt_cases:
        errors.append(f"extra GT cases: {', '.join(extra_gt_cases[:10])}")
    if extra_solution_cases:
        errors.append(f"extra solution cases: {', '.join(extra_solution_cases[:10])}")

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
            validate_gt_config(gt_case_dir, config_path, errors)
        if not sorted(gt_case_dir.glob("output_*.csv")):
            errors.append(f"{gt_case_dir}: no output CSV files")

    for solution_case_dir in solution_cases:
        solution_path = solution_case_dir / "solution.py"
        if not solution_path.is_file():
            errors.append(f"{solution_case_dir}: missing solution.py")

    print(
        f"cases={len(cases)} input_tables={input_table_count} "
        f"gt_cases={len(gt_cases)} solution_cases={len(solution_cases)} "
        f"errors={len(errors)}"
    )
    for error in errors:
        print(f"ERROR: {error}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
