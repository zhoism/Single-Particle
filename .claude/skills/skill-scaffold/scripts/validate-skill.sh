#!/usr/bin/env bash
# Validate a scaffolded OpenClaw skill against the load-bearing constraints.
#
# Usage: validate-skill.sh <skill-name>

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <skill-name>" >&2
  exit 1
fi

SKILL_NAME="$1"
SKILLS_ROOT="/Users/kevinzhou/Downloads/Single Particle/project-prime/skills"
SKILL_DIR="$SKILLS_ROOT/$SKILL_NAME"

if [[ ! -d "$SKILL_DIR" ]]; then
  echo "ERROR: $SKILL_DIR does not exist." >&2
  exit 1
fi

FAILED=0
report_fail() { echo "FAIL: $1" >&2; FAILED=1; }
report_pass() { echo "PASS: $1" >&2; }
report_warn() { echo "WARN: $1" >&2; }

# ---- 1. SKILL.md exists --------------------------------------------------
[[ -f "$SKILL_DIR/SKILL.md" ]] && report_pass "SKILL.md exists" \
  || { report_fail "SKILL.md missing"; exit 1; }

# ---- 2. Single-line JSON metadata ---------------------------------------
# Extract the metadata line and verify it parses as single-line JSON.
META_LINE=$(awk '/^metadata:/ { sub(/^metadata: /, ""); print; exit }' "$SKILL_DIR/SKILL.md")
if [[ -z "$META_LINE" ]]; then
  report_fail "metadata field missing in SKILL.md frontmatter"
elif ! python3 -c "import json,sys; json.loads(sys.argv[1])" "$META_LINE" 2>/dev/null; then
  report_fail "metadata is not single-line valid JSON"
  echo "       (OpenClaw 2026.5.28 parser requires single-line JSON; multi-line silently fails to load)" >&2
else
  report_pass "metadata is single-line JSON"
fi

# ---- 3. Wrapper exists + executable --------------------------------------
[[ -x "$SKILL_DIR/scripts/wrapper.py" ]] && report_pass "scripts/wrapper.py executable" \
  || report_fail "scripts/wrapper.py missing or not executable"

# ---- 4. --dry-run supported ---------------------------------------------
if python3 "$SKILL_DIR/scripts/wrapper.py" --help 2>/dev/null | grep -q -- "--dry-run"; then
  report_pass "wrapper supports --dry-run"
else
  report_fail "wrapper does NOT support --dry-run (mandatory per skill-scaffold rule 4)"
fi

# ---- 5. test_acceptance.sh exists ---------------------------------------
[[ -x "$SKILL_DIR/test_acceptance.sh" ]] && report_pass "test_acceptance.sh executable" \
  || report_fail "test_acceptance.sh missing or not executable"

# ---- 6. references/heuristics.md exists + cites LGPL ---------------------
if [[ -f "$SKILL_DIR/references/heuristics.md" ]]; then
  if grep -q "LGPL-3.0" "$SKILL_DIR/references/heuristics.md"; then
    report_pass "references/heuristics.md cites LGPL-3.0"
  else
    report_warn "references/heuristics.md missing LGPL-3.0 citation (required if any upstream text was adapted)"
  fi
else
  report_warn "references/heuristics.md missing (recommended even for skills with no upstream)"
fi

# ---- 7. requires.bins on PATH -------------------------------------------
if [[ -n "$META_LINE" ]]; then
  BINS=$(python3 -c "
import json, sys
try:
    m = json.loads(sys.argv[1])
    for b in m.get('requires', {}).get('bins', []):
        print(b)
except Exception:
    pass
" "$META_LINE")
  for b in $BINS; do
    if command -v "$b" >/dev/null 2>&1; then
      report_pass "binary on PATH: $b"
    else
      report_warn "binary NOT on PATH: $b (skill will fail at runtime unless env is set first)"
    fi
  done
fi

# ---- 8. Goal-oriented description (heuristic) ---------------------------
DESC_LINE=$(awk '/^description:/ { sub(/^description: /, ""); print; exit }' "$SKILL_DIR/SKILL.md")
if [[ -n "$DESC_LINE" ]]; then
  # Crude: flag prescriptive topology language
  if echo "$DESC_LINE" | grep -Eqi "(use [0-9]+ tool|in [0-9]+ step|invoke [a-z]+,? then [a-z]+)"; then
    report_warn "description appears to prescribe tool-call topology — Flash will idle-stall on this"
    report_warn "  rewrite as goal-oriented (\"prepare X given Y\" not \"run A then B\")"
  else
    report_pass "description is goal-oriented (no prescriptive topology detected)"
  fi
else
  report_fail "description missing in SKILL.md frontmatter"
fi

if [[ $FAILED -eq 0 ]]; then
  echo "[validate] all hard checks passed for $SKILL_NAME" >&2
  exit 0
else
  echo "[validate] $SKILL_NAME has failed checks; address before promoting to BUILT" >&2
  exit 1
fi
