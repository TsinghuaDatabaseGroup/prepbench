from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, Optional


TYPE_ORDER = [
    "Single-table reference",
    "Multi-table alignment",
    "Group-level concept",
    "Row-level concept",
    "Operation incomplete",
    "Operation inconsistent",
    "Operation boundary",
]


def _resolve_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _discover_case_dirs(results_root: Path) -> list[Path]:
    direct = sorted(
        [p for p in results_root.glob("case_*") if p.is_dir()],
        key=lambda p: p.name,
    )
    if direct:
        return direct

    nested = sorted(
        [p for p in results_root.rglob("case_*") if p.is_dir() and (p / "solution").is_dir()],
        key=lambda p: str(p),
    )
    return nested


def _read_json_object(path: Path) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
    if not path.exists():
        return None, "NOT_FOUND"
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return None, f"INVALID_JSON: {exc}"
    if not isinstance(parsed, dict):
        return None, "INVALID_SCHEMA: root must be object"
    return parsed, None


def _safe_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def _safe_ratio(num: float, den: float) -> float:
    return (num / den) if den > 0 else 0.0


def _extract_slot_id(answer: Any) -> Optional[str]:
    if not isinstance(answer, dict):
        return None
    for key in ("slot_id", "ref"):
        value = answer.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _load_slot_type_map(case_dir: Path) -> tuple[Dict[str, str], Dict[str, int], Optional[str]]:
    amb_kb_path = case_dir / "amb_kb.json"
    parsed, error = _read_json_object(amb_kb_path)
    if parsed is None:
        return {}, {t: 0 for t in TYPE_ORDER}, error

    ambiguities = parsed.get("ambiguities")
    if not isinstance(ambiguities, list):
        return {}, {t: 0 for t in TYPE_ORDER}, "INVALID_SCHEMA: ambiguities must be list"

    slot_to_type: Dict[str, str] = {}
    total_slots_by_type = {t: 0 for t in TYPE_ORDER}
    for item in ambiguities:
        if not isinstance(item, dict):
            continue
        slot_id = item.get("id")
        kind = item.get("kind")
        if not isinstance(slot_id, str) or not slot_id.strip():
            continue
        if not isinstance(kind, str) or kind not in total_slots_by_type:
            continue
        slot_id = slot_id.strip()
        slot_to_type[slot_id] = kind
        total_slots_by_type[kind] += 1

    return slot_to_type, total_slots_by_type, None


def run_disambiguation_batch(results_root: Path, *, data_root: Path) -> Dict[str, Any]:
    if not data_root.is_dir():
        raise FileNotFoundError(f"data_root is not a directory: {data_root}")

    gt_case_dirs = sorted(
        [p for p in data_root.glob("case_*") if p.is_dir()],
        key=lambda p: p.name,
    )
    if not gt_case_dirs:
        raise FileNotFoundError(f"No case_* directories found under data_root: {data_root}")

    discovered_case_dirs = _discover_case_dirs(results_root)
    case_dir_by_name: Dict[str, Path] = {}
    for case_dir in discovered_case_dirs:
        case_dir_by_name.setdefault(case_dir.name, case_dir)

    case_rows: list[Dict[str, str]] = []
    by_type_questions = {t: 0 for t in TYPE_ORDER}
    by_type_unique_hits = {t: 0 for t in TYPE_ORDER}
    by_type_total_slots = {t: 0 for t in TYPE_ORDER}

    summary_found = 0
    summary_invalid = 0
    results_missing = 0
    total_questions_used = 0

    for gt_case_dir in gt_case_dirs:
        case_name = gt_case_dir.name
        slot_to_type, total_slots_by_type, amb_error = _load_slot_type_map(gt_case_dir)
        for t in TYPE_ORDER:
            by_type_total_slots[t] += total_slots_by_type[t]

        result_case_dir = case_dir_by_name.get(case_name)
        clarify_summary_path = (
            (result_case_dir / "clarify" / "summary.json")
            if result_case_dir is not None
            else Path("")
        )

        status = "OK"
        error_message = ""
        questions_used = 0
        hit_questions = 0
        unique_hit_slots = 0
        hit_questions_by_type = {t: 0 for t in TYPE_ORDER}
        unique_hit_slots_by_type = {t: set() for t in TYPE_ORDER}

        if amb_error is not None:
            status = "AMB_KB_INVALID"
            error_message = amb_error

        if result_case_dir is None:
            status = "RESULT_NOT_FOUND" if status == "OK" else status
            if not error_message:
                error_message = f"Result case directory not found: {results_root / case_name}"
            results_missing += 1
        else:
            summary_obj, summary_error = _read_json_object(clarify_summary_path)
            if summary_obj is None:
                if summary_error == "NOT_FOUND":
                    status = "CLARIFY_NOT_FOUND" if status == "OK" else status
                    if not error_message:
                        error_message = f"Missing clarify summary: {clarify_summary_path}"
                else:
                    status = "CLARIFY_INVALID" if status == "OK" else status
                    if not error_message:
                        error_message = f"Invalid clarify summary: {summary_error}"
                    summary_invalid += 1
            else:
                qa_history = summary_obj.get("qa_history")
                questions_used = _safe_int(summary_obj.get("questions_used", 0))
                if not isinstance(qa_history, list):
                    status = "CLARIFY_INVALID" if status == "OK" else status
                    if not error_message:
                        error_message = "Invalid clarify summary: qa_history must be list"
                    summary_invalid += 1
                else:
                    summary_found += 1
                    for qa in qa_history:
                        if not isinstance(qa, dict):
                            continue
                        if str(qa.get("classification") or "").strip().lower() != "hit":
                            continue
                        slot_id = _extract_slot_id(qa)
                        if slot_id is None:
                            continue
                        slot_type = slot_to_type.get(slot_id)
                        if slot_type is None:
                            continue
                        hit_questions += 1
                        hit_questions_by_type[slot_type] += 1
                        unique_hit_slots_by_type[slot_type].add(slot_id)

        for t in TYPE_ORDER:
            by_type_questions[t] += hit_questions_by_type[t]
            by_type_unique_hits[t] += len(unique_hit_slots_by_type[t])

        unique_hit_slots = sum(len(s) for s in unique_hit_slots_by_type.values())
        total_slots = sum(total_slots_by_type.values())
        total_questions_used += questions_used
        precision = _safe_ratio(float(unique_hit_slots), float(questions_used))
        recall = _safe_ratio(float(unique_hit_slots), float(total_slots))
        f1 = _safe_ratio(2.0 * precision * recall, precision + recall)

        case_rows.append(
            {
                "case_name": case_name,
                "status": status,
                "questions_used": str(questions_used),
                "hit_questions": str(hit_questions),
                "unique_hit_slots": str(unique_hit_slots),
                "total_slots": str(total_slots),
                "precision": f"{precision:.6f}",
                "recall": f"{recall:.6f}",
                "f1": f"{f1:.6f}",
                "results_case_dir": str(result_case_dir.resolve()) if result_case_dir else "",
                "clarify_summary_path": str(clarify_summary_path.resolve()) if result_case_dir else "",
                "error_message": error_message,
            }
        )

    disamb_summary_csv = results_root / "disamb_summary.csv"
    disamb_by_type_csv = results_root / "disamb_by_type.csv"
    disamb_metrics_json = results_root / "disamb_metrics.json"
    disamb_f1_txt = results_root / "disamb_f1.txt"

    summary_fields = [
        "case_name",
        "status",
        "questions_used",
        "hit_questions",
        "unique_hit_slots",
        "total_slots",
        "precision",
        "recall",
        "f1",
        "results_case_dir",
        "clarify_summary_path",
        "error_message",
    ]
    with disamb_summary_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(case_rows)

    by_type_rows: list[Dict[str, str]] = []
    for t in TYPE_ORDER:
        questions = by_type_questions[t]
        unique_hits = by_type_unique_hits[t]
        total_slots = by_type_total_slots[t]
        precision = _safe_ratio(float(unique_hits), float(questions))
        recall = _safe_ratio(float(unique_hits), float(total_slots))
        f1 = _safe_ratio(2.0 * precision * recall, precision + recall)
        by_type_rows.append(
            {
                "ambiguity_type": t,
                "questions": str(questions),
                "unique_hit_slots": str(unique_hits),
                "total_slots": str(total_slots),
                "precision": f"{precision:.6f}",
                "recall": f"{recall:.6f}",
                "f1": f"{f1:.6f}",
            }
        )

    with disamb_by_type_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "ambiguity_type",
                "questions",
                "unique_hit_slots",
                "total_slots",
                "precision",
                "recall",
                "f1",
            ],
        )
        writer.writeheader()
        writer.writerows(by_type_rows)

    total_hit_questions = sum(by_type_questions.values())
    total_unique_hits = sum(by_type_unique_hits.values())
    total_slots = sum(by_type_total_slots.values())
    precision = _safe_ratio(float(total_unique_hits), float(total_questions_used))
    recall = _safe_ratio(float(total_unique_hits), float(total_slots))
    f1 = _safe_ratio(2.0 * precision * recall, precision + recall)

    metrics = {
        "total_cases": len(gt_case_dirs),
        "summary_found_cases": summary_found,
        "summary_invalid_cases": summary_invalid,
        "result_missing_cases": results_missing,
        "questions_used": total_questions_used,
        "hit_questions": total_hit_questions,
        "unique_hit_slots": total_unique_hits,
        "total_slots": total_slots,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "by_type": by_type_rows,
    }
    disamb_metrics_json.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    disamb_f1_txt.write_text(f"{f1:.6f}\n", encoding="utf-8")

    print(
        f"[evaluate.disamb] cases={len(gt_case_dirs)} summary_found={summary_found} "
        f"questions_used={total_questions_used} hit_questions={total_hit_questions} "
        f"unique_hits={total_unique_hits} total_slots={total_slots} "
        f"precision={precision:.6f} recall={recall:.6f} f1={f1:.6f} "
        f"summary={disamb_summary_csv} by_type={disamb_by_type_csv} metrics={disamb_metrics_json} f1_txt={disamb_f1_txt}"
    )
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute disambiguation precision/recall/F1 from clarify artifacts under one results root."
    )
    parser.add_argument(
        "--results-root",
        required=True,
        type=str,
        help="Path like @output/<model>/<run_mode>, containing case_* directories.",
    )
    parser.add_argument(
        "--data-root",
        default="",
        type=str,
        help="Optional benchmark data root containing case_*/amb_kb.json (default: <repo>/data).",
    )
    args = parser.parse_args()

    results_root = Path(args.results_root).resolve()
    if not results_root.is_dir():
        raise FileNotFoundError(f"results_root is not a directory: {results_root}")

    data_root = Path(args.data_root).resolve() if args.data_root else (_resolve_repo_root() / "data").resolve()
    run_disambiguation_batch(results_root, data_root=data_root)


if __name__ == "__main__":
    main()
