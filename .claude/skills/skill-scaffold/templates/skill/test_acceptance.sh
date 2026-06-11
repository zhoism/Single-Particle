#!/usr/bin/env bash
# __SKILL_NAME__ acceptance test.
#
# Three test cases per the manifest's general acceptance discipline:
#   1. Golden — known-good input from smoke-test or phase3-advisor-demo.
#   2. Unrelated — a different valid input, confirms scalability.
#   3. Malformed — confirms graceful failure with a clear error code.
#
# All three must pass before the skill is promoted from BUILT to COMPLETE
# in Phase3_Taskboard_Manifest.md.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WRAPPER="$SKILL_DIR/scripts/wrapper.py"
RUN_BASE="$SKILL_DIR/test-runs"
mkdir -p "$RUN_BASE"

DRY_RUN=""
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN="--dry-run"
  echo "[acceptance] dry-run mode" >&2
fi

pass() { echo "PASS: $1" >&2; }
fail() { echo "FAIL: $1" >&2; exit 1; }

# ---- Case 1: Golden ------------------------------------------------------
echo "[case 1] Golden — __GOLDEN_INPUT_DESCRIPTION__" >&2
GOLDEN_INPUT="__GOLDEN_INPUT_PATH_OR_VALUE__"  # e.g., benzene SMILES "c1ccccc1"
GOLDEN_OUT="$RUN_BASE/golden"
rm -rf "$GOLDEN_OUT" && mkdir -p "$GOLDEN_OUT"

if python3 "$WRAPPER" --input "$GOLDEN_INPUT" --name "TST" --output-dir "$GOLDEN_OUT" $DRY_RUN \
     > "$GOLDEN_OUT/envelope.json"; then
  python3 -c "import json,sys; e=json.load(open('$GOLDEN_OUT/envelope.json')); sys.exit(0 if e['ok'] else 1)" \
    && pass "Golden" || fail "Golden envelope ok=false"
else
  fail "Golden wrapper non-zero exit"
fi

# ---- Case 2: Unrelated ---------------------------------------------------
echo "[case 2] Unrelated — __UNRELATED_INPUT_DESCRIPTION__" >&2
UNRELATED_INPUT="__UNRELATED_INPUT_PATH_OR_VALUE__"  # e.g., a different valid ligand
UNRELATED_OUT="$RUN_BASE/unrelated"
rm -rf "$UNRELATED_OUT" && mkdir -p "$UNRELATED_OUT"

if python3 "$WRAPPER" --input "$UNRELATED_INPUT" --name "UNR" --output-dir "$UNRELATED_OUT" $DRY_RUN \
     > "$UNRELATED_OUT/envelope.json"; then
  python3 -c "import json,sys; e=json.load(open('$UNRELATED_OUT/envelope.json')); sys.exit(0 if e['ok'] else 1)" \
    && pass "Unrelated" || fail "Unrelated envelope ok=false"
else
  fail "Unrelated wrapper non-zero exit"
fi

# ---- Case 3: Malformed ---------------------------------------------------
echo "[case 3] Malformed — confirms graceful failure" >&2
MALFORMED_INPUT="__MALFORMED_INPUT_VALUE__"  # e.g., "not-a-smiles!!!"
MALFORMED_OUT="$RUN_BASE/malformed"
rm -rf "$MALFORMED_OUT" && mkdir -p "$MALFORMED_OUT"

# We EXPECT non-zero exit. The envelope MUST have ok=false and a clear error string.
python3 "$WRAPPER" --input "$MALFORMED_INPUT" --name "BAD" --output-dir "$MALFORMED_OUT" $DRY_RUN \
  > "$MALFORMED_OUT/envelope.json" || true

if python3 -c "
import json, sys
e = json.load(open('$MALFORMED_OUT/envelope.json'))
ok = (e.get('ok') is False) and len(e.get('errors', [])) > 0
sys.exit(0 if ok else 1)
"; then
  pass "Malformed (graceful failure)"
else
  fail "Malformed did NOT fail gracefully — wrapper either succeeded or returned a bad envelope"
fi

echo "[acceptance] all cases passed" >&2
