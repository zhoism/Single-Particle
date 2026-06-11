---
name: __SKILL_NAME__
description: __ONE_SENTENCE_GOAL_ORIENTED_DESCRIPTION__. Take __INPUTS__, return __OUTPUTS__. Designed for AMBER-side preparation; handles arbitrary ligands/systems, not a hardcoded test case.
metadata: {"requires":{"bins":["__BIN1__","__BIN2__"],"env":["AMBERHOME"]},"inputs":{"__INPUT_KEY__":"__TYPE__"},"outputs":{"__OUTPUT_KEY__":"__PATH_OR_PATTERN__"},"validation":["__GATE1__","__GATE2__"],"dry_run":true,"source":"project-prime/skills/__SKILL_NAME__"}
---

# __SKILL_NAME__

## Goal

__ONE_PARAGRAPH_ON_WHAT_THIS_SKILL_DOES_AT_THE_DOMAIN_LEVEL. Describe the chemistry / MD-stage outcome, not the binaries. Example: "Prepare an explicit-solvent-ready ligand library from a SMILES string or PDB extract — clean the input, derive partial charges (AM1-BCC via antechamber), check for missing parameters (parmchk2), and emit the .mol2 + .frcmod that tleap will load."__

## When to use

- __TRIGGER_1__
- __TRIGGER_2__

## Inputs

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `__INPUT_KEY__` | __TYPE__ | yes | __DESCRIPTION__ |
| `--name` | string | no (default `LIG`) | Residue name for the prepared library. 1–4 chars, no special chars. |
| `--charge` | int | no (default 0) | Net formal charge for AM1-BCC. |
| `--dry-run` | flag | no | Emit the planned commands + computed paths without executing. |
| `--output-dir` | path | no (default `./`) | Where to write artifacts. |

## Outputs

JSON envelope on stdout:

```json
{
  "ok": true,
  "skill": "__SKILL_NAME__",
  "stage": "ligand-prep",
  "dry_run": false,
  "outputs": {
    "mol2": "/path/to/LIG.mol2",
    "frcmod": "/path/to/LIG.frcmod",
    "lib": "/path/to/LIG.lib"
  },
  "validation": {
    "atom_count": 18,
    "charge_sum": 0.0,
    "frcmod_missing": []
  },
  "errors": []
}
```

stderr is human-readable progress.

## Validation gates

- __GATE_1_DESCRIPTION__ (e.g., "All heavy atoms typed; no `du` placeholder types").
- __GATE_2_DESCRIPTION__ (e.g., "Net charge within 1e-4 of the requested value").
- __GATE_3_DESCRIPTION__ (e.g., "Zero `ATTN` lines in frcmod with bond/angle parameters").

## Errors

| Error | Cause | Recovery |
|-------|-------|----------|
| `SQM_CONVERGENCE_FAILED` | AM1-BCC SCF didn't converge | Try `--charge` adjustment or hand-typed input; see `references/heuristics.md` |
| `MISSING_PARAMETERS` | `parmchk2` emitted `ATTN` lines | Manual frcmod edit or alternative force field; see heuristics |
| `INVALID_INPUT` | SMILES doesn't parse / PDB malformed | Caller must clean input before retry |

## How it works

Wrapper-internal chain (one `exec` call, executed by Python):

1. __STEP_1__ (e.g., obabel SMILES → 3D structure).
2. __STEP_2__ (e.g., antechamber GAFF2 + AM1-BCC).
3. __STEP_3__ (e.g., parmchk2 missing-parameter check).
4. tleap dry-load to confirm the library is parseable.
5. Validation sweep against the gates above.

Each step's stdout/stderr is captured to a per-run directory; the envelope returns paths.

## References

See `references/heuristics.md` for parameter heuristics adapted from upstream `computational-chemistry-agent-skills/__UPSTREAM_PATH__/SKILL.md` (LGPL-3.0). Cite, do not depend on, the upstream package.

## Acceptance test

`bash test_acceptance.sh` runs three cases:
1. **Golden** — known-good input from the smoke-test or phase3-advisor-demo.
2. **Unrelated** — a different valid input to confirm scalability.
3. **Malformed** — confirms graceful failure with a clear error code.

All three must pass before this skill is promoted from BUILT to COMPLETE in `Phase3_Taskboard_Manifest.md`.
