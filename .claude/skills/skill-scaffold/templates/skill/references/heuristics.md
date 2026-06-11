# __SKILL_NAME__ — parameter heuristics

Adapted from `~/Downloads/Single Particle/upstream-reference/computational-chemistry-agent-skills/__UPSTREAM_PATH__/SKILL.md` (LGPL-3.0). Cite, do not depend on, the upstream package at runtime.

## Why this file exists

OpenClaw's stock SKILL.md skills are "documentation-skills" — LLM constructs the call from prose heuristics. Our skills are "hardened-deterministic-skills" — Python wrapper does the work. But the heuristics still matter, because:

1. **Stage 8 recovery** needs them to choose a recovery branch when a parameter fails.
2. **Future planner agent** (Stage 7) uses them to decide which skill to invoke.
3. **Audit trail** — when a result is questioned, the heuristic chain explains why each parameter was chosen.

So we keep heuristics in a sibling file, not in SKILL.md (which is goal-oriented per the wrapper-internal-chaining principle).

## Heuristics

### __HEURISTIC_1_NAME__

__When-applies__: __conditions__
__Why__: __physical or methodological reason__
__Source__: __upstream-path or paper-ref__

### __HEURISTIC_2_NAME__

(...)

## Anti-heuristics (don't do this)

- __ANTI_1__: e.g., "Don't use GAFF1 — it's superseded by GAFF2 (2014) and OpenClaw's antechamber default is gaff2."
- __ANTI_2__: e.g., "Don't run sqm without `qm_theory='AM1'` for the BCC step — other levels are unsupported by the BCC parameter set."

## Recurring failure modes

| Failure | Symptom | Root cause | Recovery |
|---------|---------|------------|----------|
| __FAIL_1__ | __symptom__ | __cause__ | __recovery__ |
| __FAIL_2__ | __symptom__ | __cause__ | __recovery__ |

## Attribution

Upstream: `jinzhezenggroup/computational-chemistry-agent-skills`, LGPL-3.0. Specific file(s) referenced:
- `__UPSTREAM_PATH__/SKILL.md` (heuristics adapted)
- `__UPSTREAM_PATH__/__ANY_OTHER_FILE__` (if applicable)

Cloned read-only locally for reference at `~/Downloads/Single Particle/upstream-reference/`.
