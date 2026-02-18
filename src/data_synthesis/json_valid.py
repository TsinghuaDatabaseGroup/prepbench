#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from core.case_assets import resolve_reference_solution_path

# Regex patterns for detecting non-ASCII / uncommon language characters
# CJK Unified Ideographs (Chinese, Japanese Kanji, Korean Hanja) - Basic Multilingual Plane only
# Extended planes (U+20000+) require \U escapes and are rare in practice
CJK_PATTERN = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
# Emoji ranges (common emoji blocks)
EMOJI_PATTERN = re.compile(
    r"[\U0001F600-\U0001F64F"  # Emoticons
    r"\U0001F300-\U0001F5FF"  # Misc Symbols and Pictographs
    r"\U0001F680-\U0001F6FF"  # Transport and Map
    r"\U0001F1E0-\U0001F1FF"  # Flags
    r"\U00002702-\U000027B0"  # Dingbats
    r"\U0001F900-\U0001F9FF"  # Supplemental Symbols
    r"\U0001FA00-\U0001FA6F"  # Chess, Extended-A
    r"\U0001FA70-\U0001FAFF"  # Symbols Extended-A
    r"\U00002600-\U000026FF"  # Misc symbols
    r"]"
)

# Thresholds for readability checks
MIN_LINES_FOR_READABLE_JSON = 3  # JSON with ambiguities should have at least this many lines
MAX_CHARS_PER_LINE_THRESHOLD = 1500  # Lines exceeding this are considered hard to read (ref fields can be long)


ALLOWED_KINDS = {
    "Single-table reference",
    "Multi-table alignment",
    "Group-level concept",
    "Row-level concept",
    "Operation incomplete",
    "Operation inconsistent",
    "Operation boundary",
}
OLD_TAXONOMY_ID_PREFIX_PATTERN = re.compile(r"^\d+_[DCO][123](_|$)")


def _read_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return None, f"invalid JSON: {exc}"
    if not isinstance(data, dict):
        return None, "root is not a JSON object"
    return data, None


def _load_flow_nodes(flow_path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not flow_path.exists():
        # Some dataset layouts do not ship flow.json with each case.
        return None, None
    data, err = _read_json(flow_path)
    if err:
        return None, f"flow.json {err}"
    nodes = data.get("nodes")
    if not isinstance(nodes, dict):
        return None, "flow.json missing 'nodes' object"
    return nodes, None


def _load_solution_text(solution_path: Path) -> str:
    try:
        return solution_path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _check_uncommon_chars(text: str, context: str = "") -> list[str]:
    issues: list[str] = []
    
    emoji_matches = EMOJI_PATTERN.findall(text)
    if emoji_matches:
        unique_emojis = list(set(emoji_matches))[:5]
        issues.append(f"{context}contains emoji characters: {unique_emojis}")
    
    cjk_matches = CJK_PATTERN.findall(text)
    if cjk_matches:
        unique_cjk = list(set(cjk_matches))[:10]
        issues.append(f"{context}contains Chinese/CJK characters: {''.join(unique_cjk)}")
    
    return issues


def _check_entry_uncommon_chars(entry: dict[str, Any], idx: int) -> list[str]:
    issues: list[str] = []
    
    business_fields = ["source_text", "intent", "id", "kind"]
    for field in business_fields:
        val = entry.get(field)
        if isinstance(val, str) and val:
            field_issues = _check_uncommon_chars(val, context="")
            for issue in field_issues:
                issues.append(f"entry[{idx}].{field} {issue}")
    
    ref_val = entry.get("ref")
    if isinstance(ref_val, str) and ref_val:
        ref_issues = _check_uncommon_chars(ref_val, context="")
        for issue in ref_issues:
            issues.append(f"entry[{idx}].ref (from reference solution) {issue}")
    
    return issues


def _check_json_readability(text: str, has_ambiguities: bool) -> list[str]:
    issues: list[str] = []
    lines = text.splitlines()
    line_count = len(lines)
    
    if has_ambiguities:
        if line_count < MIN_LINES_FOR_READABLE_JSON:
            issues.append(
                f"JSON is compressed into {line_count} line(s) but contains ambiguities - "
                f"should be formatted for readability (recommend running: python -m json.tool)"
            )
    
    
    return issues


def _validate_ref_lines(ref: str, solution_text: str) -> list[str]:
    issues: list[str] = []
    if not solution_text:
        return ["reference solution missing or unreadable; cannot validate ref"]
    missing_lines: list[str] = []
    for line in ref.splitlines():
        if not line.strip():
            continue
        if line not in solution_text:
            missing_lines.append(line)
    if missing_lines:
        preview = "; ".join(missing_lines[:3])
        issues.append(f"ref lines not found in reference solution (examples): {preview}")
    return issues


def _validate_entry(
    entry: dict[str, Any],
    *,
    nodes: dict[str, Any] | None,
    solution_text: str,
    seen_ids: set[str],
    idx: int,
    check_ref_lines: bool,
) -> list[str]:
    issues: list[str] = []
    if not isinstance(entry, dict):
        return [f"entry[{idx}] is not an object"]

    keys = set(entry.keys())
    required = {"id", "kind", "node_id", "op", "ref"}
    optional = {"source_text", "intent"}

    if not required.issubset(keys):
        missing = sorted(required - keys)
        issues.append(f"entry[{idx}] missing keys: {missing}")

    opt_present = keys & optional
    if len(opt_present) != 1:
        issues.append(f"entry[{idx}] must have exactly one of source_text or intent")

    expected_len = 6
    if len(keys) != expected_len:
        issues.append(f"entry[{idx}] must have exactly {expected_len} keys (got {len(keys)})")

    extra = keys - (required | optional)
    if extra:
        issues.append(f"entry[{idx}] has unexpected keys: {sorted(extra)}")

    def _check_str(field: str) -> None:
        val = entry.get(field)
        if not isinstance(val, str):
            issues.append(f"entry[{idx}] {field} must be a string")
        elif not val.strip():
            issues.append(f"entry[{idx}] {field} must be non-empty")

    for field in required:
        _check_str(field)

    if "source_text" in entry:
        _check_str("source_text")
    if "intent" in entry:
        _check_str("intent")

    kind = entry.get("kind")
    if isinstance(kind, str) and kind and kind not in ALLOWED_KINDS:
        issues.append(f"entry[{idx}] kind not in allowed taxonomy: {kind}")

    entry_id = entry.get("id")
    if isinstance(entry_id, str) and entry_id:
        if OLD_TAXONOMY_ID_PREFIX_PATTERN.match(entry_id):
            issues.append(
                f"entry[{idx}] id uses deprecated taxonomy prefix: {entry_id}"
            )
        if entry_id in seen_ids:
            issues.append(f"entry[{idx}] duplicate id: {entry_id}")
        else:
            seen_ids.add(entry_id)

    node_id = entry.get("node_id")
    op = entry.get("op")
    if isinstance(node_id, str) and isinstance(op, str) and nodes:
        node = nodes.get(node_id)
        if node is None:
            issues.append(f"entry[{idx}] node_id not found in flow.json: {node_id}")
        else:
            node_kind = node.get("kind")
            if node_kind != op:
                issues.append(
                    f"entry[{idx}] op does not match flow.json kind for {node_id}: {op} != {node_kind}"
                )

    if check_ref_lines and isinstance(entry.get("ref"), str):
        issues.extend(_validate_ref_lines(entry["ref"], solution_text))

    return issues


def validate_case(
    case_dir: Path,
    *,
    check_ref_lines: bool,
    check_uncommon_chars: bool = True,
    check_readability: bool = True,
) -> list[str]:
    issues: list[str] = []
    amb_path = case_dir / "amb_kb.json"
    if not amb_path.exists():
        return ["missing amb_kb.json"]
    text = amb_path.read_text(encoding="utf-8")
    if not text.strip():
        return ["amb_kb.json is empty"]

    data, err = _read_json(amb_path)
    if err:
        return [f"amb_kb.json {err}"]

    ambiguities = data.get("ambiguities")
    if not isinstance(ambiguities, list):
        return ["ambiguities must be a list"]

    if check_readability:
        has_ambiguities = len(ambiguities) > 0
        issues.extend(_check_json_readability(text, has_ambiguities))

    nodes, nodes_err = _load_flow_nodes(case_dir / "flow.json")
    if nodes_err:
        issues.append(nodes_err)

    solution_path = resolve_reference_solution_path(case_dir)
    solution_text = _load_solution_text(solution_path) if solution_path is not None else ""
    seen_ids: set[str] = set()
    for idx, entry in enumerate(ambiguities):
        if check_uncommon_chars and isinstance(entry, dict):
            issues.extend(_check_entry_uncommon_chars(entry, idx))
        
        issues.extend(
            _validate_entry(
                entry,
                nodes=nodes,
                solution_text=solution_text,
                seen_ids=seen_ids,
                idx=idx,
                check_ref_lines=check_ref_lines,
            )
        )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate amb_kb.json format across cases.")
    parser.add_argument(
        "--data-dir",
        type=str,
        default="",
        help="Path to data directory (default: repo_root/data).",
    )
    parser.add_argument(
        "--case",
        type=str,
        default="",
        help="Single case name (e.g., case_001). If omitted, validate all cases.",
    )
    parser.add_argument(
        "--skip-ref-check",
        action="store_true",
        help="Skip checking whether ref lines appear in reference solution.",
    )
    parser.add_argument(
        "--skip-char-check",
        action="store_true",
        help="Skip checking for uncommon characters (emoji, CJK, non-ASCII).",
    )
    parser.add_argument(
        "--skip-readability-check",
        action="store_true",
        help="Skip checking JSON readability (single-line, long lines).",
    )
    parser.add_argument(
        "--show-ok",
        action="store_true",
        help="Print OK cases as well.",
    )
    parser.add_argument(
        "--only-char-check",
        action="store_true",
        help="Only run the uncommon character check (emoji, CJK, non-ASCII).",
    )
    parser.add_argument(
        "--only-readability-check",
        action="store_true",
        help="Only run the JSON readability check.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    data_dir = Path(args.data_dir) if args.data_dir else (repo_root / "data")
    if not data_dir.exists():
        print(f"[ERROR] data dir not found: {data_dir}")
        return 1

    if args.case:
        case_dirs = [data_dir / args.case]
    else:
        case_dirs = sorted(
            [p for p in data_dir.iterdir() if p.is_dir() and p.name.startswith("case_")]
        )

    check_ref = not args.skip_ref_check
    check_chars = not args.skip_char_check
    check_readability = not args.skip_readability_check
    
    if args.only_char_check:
        check_ref = False
        check_readability = False
        check_chars = True
    elif args.only_readability_check:
        check_ref = False
        check_chars = False
        check_readability = True

    total = 0
    failed = 0
    char_issues_count = 0
    readability_issues_count = 0
    
    for case_dir in case_dirs:
        total += 1
        issues = validate_case(
            case_dir,
            check_ref_lines=check_ref,
            check_uncommon_chars=check_chars,
            check_readability=check_readability,
        )
        if issues:
            failed += 1
            print(f"{case_dir.name}: FAIL")
            for issue in issues:
                print(f"  - {issue}")
                if "emoji" in issue.lower() or "cjk" in issue.lower() or "non-ascii" in issue.lower():
                    char_issues_count += 1
                elif "readability" in issue.lower() or "compressed" in issue.lower():
                    readability_issues_count += 1
        elif args.show_ok:
            print(f"{case_dir.name}: OK")

    print(f"\n{'=' * 50}")
    print(f"Checked {total} case(s). Failed: {failed}.")
    if check_chars:
        print(f"  - Cases with uncommon characters: {char_issues_count}")
    if check_readability:
        print(f"  - Cases with readability issues: {readability_issues_count}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
