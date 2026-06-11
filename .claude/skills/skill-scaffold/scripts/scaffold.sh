#!/usr/bin/env bash
# Scaffold a new OpenClaw chemistry skill at project-prime/skills/<name>/.
#
# Usage: scaffold.sh <skill-name>
#
# Example: scaffold.sh antechamber-ligandprep

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <skill-name>" >&2
  echo "  skill-name: kebab-case, e.g., antechamber-ligandprep" >&2
  exit 1
fi

SKILL_NAME="$1"

# Validate skill name
if ! [[ "$SKILL_NAME" =~ ^[a-z][a-z0-9-]*$ ]]; then
  echo "ERROR: skill name must be kebab-case (lowercase letters, digits, hyphens)" >&2
  exit 1
fi

SCAFFOLD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="$SCAFFOLD_DIR/templates/skill"
SKILLS_ROOT="/Users/kevinzhou/Downloads/Single Particle/project-prime/skills"
TARGET="$SKILLS_ROOT/$SKILL_NAME"

if [[ -e "$TARGET" ]]; then
  echo "ERROR: $TARGET already exists. Refusing to overwrite." >&2
  echo "       If you want to re-scaffold, move or delete the existing dir first." >&2
  exit 1
fi

mkdir -p "$SKILLS_ROOT"
echo "[scaffold] creating $TARGET" >&2
cp -R "$TEMPLATE_DIR" "$TARGET"

# Stamp __SKILL_NAME__ throughout
TODAY="$(date +%Y-%m-%d)"
find "$TARGET" -type f \( -name "*.md" -o -name "*.py" -o -name "*.sh" \) -print0 | \
  while IFS= read -r -d '' f; do
    sed -i.bak "s|__SKILL_NAME__|$SKILL_NAME|g; s|__TODAY__|$TODAY|g" "$f"
    rm -f "$f.bak"
  done

# Make scripts executable
chmod +x "$TARGET/scripts/wrapper.py" "$TARGET/test_acceptance.sh"

echo "[scaffold] done. Next steps:" >&2
echo "  1. Edit $TARGET/SKILL.md — fill the single-line JSON metadata + Inputs/Outputs/Errors." >&2
echo "  2. Edit $TARGET/scripts/wrapper.py — fill REQUIRED_BINS, the step functions, validation." >&2
echo "  3. Edit $TARGET/references/heuristics.md — adapt upstream heuristics, cite LGPL-3.0." >&2
echo "  4. Edit $TARGET/test_acceptance.sh — set golden / unrelated / malformed inputs." >&2
echo "  5. Run $SCAFFOLD_DIR/scripts/validate-skill.sh $SKILL_NAME" >&2
echo "  6. Run bash $TARGET/test_acceptance.sh --dry-run" >&2
echo "  7. Run bash $TARGET/test_acceptance.sh (full execution)" >&2
echo "  8. Update Phase3_Taskboard_Manifest.md: stage flipped to BUILT." >&2
echo "  9. devlog-append skill: log the scaffold." >&2
