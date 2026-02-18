#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "${REPO_ROOT}"

MODE="${1:-build_gt_code}"
CASE_SELECTOR="${2:-1}"
MODEL_NAME="${3:-deepseek/deepseek-v3.2}"

shift $(( $# >= 3 ? 3 : $# ))

echo "[RUN] mode=${MODE} case=${CASE_SELECTOR} model=${MODEL_NAME}"
PYTHONPATH=src python -m data_synthesis.run "${MODE}" \
  --case "${CASE_SELECTOR}" \
  --model "${MODEL_NAME}" \
  --force \
  "$@"
