#!/usr/bin/env bash
# Validate all JSON files in tests/vectors/ with the free validator
set -euo pipefail
for f in tests/vectors/*.json; do
  # Skip auto-generated smoke files and intentionally bad examples
  if [[ "$f" == *"_smoke_"* ]] || [[ "$f" == *"bad_"* ]]; then
    echo "Skipping: $f"
    continue
  fi
  echo "Validating $f"
  python3 tools/npp_validator.py "$f" || { echo "FAILED: $f"; exit 1; }
done
echo "All packets passed."
