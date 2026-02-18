#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "${REPO_ROOT}"

CASE_SELECTOR="${1:-1}"
MODEL_NAME="${2:-deepseek/deepseek-v3.2}"
MAX_ROUNDS="${3:-5}"
MAX_REWRITE_ROUNDS="${4:-3}"
MAX_VALIDATION_ROUNDS="${5:-3}"

echo "[RUN] build_gt_code"
PYTHONPATH=src python -m data_synthesis.run build_gt_code \
  --case "${CASE_SELECTOR}" \
  --model "${MODEL_NAME}" \
  --max-rounds "${MAX_ROUNDS}" \
  --force

echo "[RUN] build_flow"
PYTHONPATH=src python -m data_synthesis.run build_flow \
  --case "${CASE_SELECTOR}" \
  --model "${MODEL_NAME}" \
  --max-rounds "${MAX_ROUNDS}" \
  --force

echo "[RUN] build_disamb"
PYTHONPATH=src python -m data_synthesis.run build_disamb \
  --case "${CASE_SELECTOR}" \
  --model "${MODEL_NAME}" \
  --max-rewrite-rounds "${MAX_REWRITE_ROUNDS}" \
  --max-validation-rounds "${MAX_VALIDATION_ROUNDS}" \
  --force

MODEL_DIR="${MODEL_NAME//\//__}"
echo "[DONE] outputs:"
echo "  src/data_synthesis/output/gt_codegen/${MODEL_DIR}/"
echo "  src/data_synthesis/output/workflow/${MODEL_DIR}/"
echo "  src/data_synthesis/output/disamb_build/${MODEL_DIR}/"
