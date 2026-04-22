#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HARNESS_DIR="${ROOT_DIR}/harness"

if [[ ! -d "${HARNESS_DIR}/.venv" ]]; then
  echo "error: harness virtual environment not found at ${HARNESS_DIR}/.venv" >&2
  exit 1
fi

if [[ -f "${HARNESS_DIR}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${HARNESS_DIR}/.env"
  set +a
fi

cd "${HARNESS_DIR}"

CORE_CASES=(
  safe_baseline
  direct_override
  prompt_leakage
)

EXTENDED_CASES=(
  role_confusion
  obfuscated_injection
  indirect_injection
  indirect_injection_hidden_metadata
  indirect_injection_priority_conflict
  indirect_injection_cross_document
  indirect_injection_html_comment
  indirect_injection_quoted_text
  indirect_injection_tabular
  indirect_injection_dual_task
  indirect_injection_multi_hop
  tool_manipulation
  tool_manipulation_policy_bypass
  data_exfiltration_tool_use
  unauthorized_action_execution
  context_poisoning
  persistent_injection
  contextual_injection
  delayed_trigger_injection
)

run_case_set() {
  local provider="$1"
  shift
  local model="$1"
  shift
  local cases=("$@")

  echo ""
  echo "=== Provider: ${provider} | Model: ${model} ==="

  for case_name in "${cases[@]}"; do
    echo ""
    echo "--- ${case_name} ---"
    .venv/bin/python run_case.py "${case_name}" --provider "${provider}" --model "${model}" || true
  done

  echo ""
  echo "--- benchmark_matrix (${provider}) ---"
  local case_csv
  case_csv="$(IFS=,; echo "${cases[*]}")"
  .venv/bin/python run_benchmark.py --provider "${provider}" --model "${model}" --cases "${case_csv}" || true
}

if [[ -n "${OPENAI_API_KEY:-}" ]]; then
  run_case_set "openai" "${OPENAI_MODEL:-gpt-4.1-mini}" "${CORE_CASES[@]}" "${EXTENDED_CASES[@]}"
else
  echo "Skipping OpenAI matrix: OPENAI_API_KEY not set"
fi

if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
  run_case_set "anthropic" "${ANTHROPIC_MODEL:-claude-sonnet-4-20250514}" "${CORE_CASES[@]}" "${EXTENDED_CASES[@]}"
else
  echo "Skipping Anthropic matrix: ANTHROPIC_API_KEY not set"
fi

if [[ -n "${MISTRAL_API_KEY:-}" ]]; then
  run_case_set "mistral" "${MISTRAL_MODEL:-mistral-small-latest}" "${CORE_CASES[@]}" "${EXTENDED_CASES[@]}"
else
  echo "Skipping Mistral matrix: MISTRAL_API_KEY not set"
fi
