#!/usr/bin/env bash
# Explicit external security qualification; never reports green if a tool is missing.
set -euo pipefail
if [[ "${FHS_APPROVED_TOOLCHAIN_REF:-}" == "" ]]; then
  echo 'NOT_RUN: Owner-approved toolchain evidence ref missing' >&2
  exit 42
fi
for tool in actionlint zizmor gitleaks; do
  if ! command -v "$tool" >/dev/null; then
    echo "NOT_RUN: required qualified tool is unavailable: $tool" >&2
    exit 42
  fi
done
actionlint .github/workflows/fhs-entry-check.yml
zizmor .github/workflows/fhs-entry-check.yml
gitleaks git --redact --exit-code 1 .
echo "LOCAL_SECURITY_TOOLS_COMPLETED_ONLY; evidence=${FHS_APPROVED_TOOLCHAIN_REF}"
