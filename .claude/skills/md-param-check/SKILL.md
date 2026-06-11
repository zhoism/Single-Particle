---
name: md-param-check
description: Use to validate AMBER MD input files (.in) and submit scripts against the project's hard physical/methodological limits. Triggers on "check the MD params", "validate this .in file", "is heat-3 OK", "check the submit script paths", or whenever a new MD stage / advisor handoff lands. Catches the heat-3 temp0/&wt mismatch class of bug, the hardcoded-AMBERHOME class of portability bug, and the dt-too-large / SHAKE-disabled class of physics-realism bug. Runs a deterministic Python validator; emits a per-file verdict.
---

# md-param-check — AMBER namelist + submit script sanity sweep

Project `CLAUDE.md` SOP §3: "Physical realism is non-negotiable for MD parameters — enforce hard limits like `dt ≤ 2fs`, non-bonded `cut` ranges, SHAKE constraints." The 2026-06-01 advisor handoff surfaced two real bugs in the canonical recipe that this skill exists to catch:

- **`heat-3.in`**: `&cntrl temp0=300.0` vs `&wt value2=310.0` — Langevin follows the &wt-set TEMP0, so the system ramps to 310 K. The advisor's intent is unclear; either is defensible but the file is internally inconsistent.
- **`submit.sh`**: `AMBERHOME=/Application/software/Amber26/pmemd26` — that's the advisor's machine. Will fail on ours (`~/Downloads/pmemd26/`).

## When to invoke

- User pastes a `.in` file or refers to a new MD stage.
- User mentions "the submit script" or asks about a portable run.
- Phase 3 advisor demo (or any similar handoff) arrives with input files.
- A new skill (e.g., sander-pmemd-wrapper) is being scaffolded and needs to emit AMBER-correct namelists.
- After a `Skill_*` produces a `.in` file as output, validate before running.

## Hard rules (the limits the validator enforces)

| Parameter | Rule | Source |
|-----------|------|--------|
| `dt` | ≤ 0.002 ps (= 2 fs) when SHAKE is on; ≤ 0.001 when SHAKE off | SOP §3, Amber26.pdf §23.6 |
| `cut` (explicit solvent) | 8.0 ≤ cut ≤ 12.0 Å | SOP §3 |
| SHAKE on dt ≥ 0.002 | `ntc=2, ntf=2` required | SOP §3, AMBER best practice |
| Thermostat | `ntt=3` (Langevin) with `gamma_ln ∈ [1, 5]` typically | Advisor demo standard |
| `temp0` vs `&wt value2` | Must be consistent when `nmropt=1` | heat-3 lesson, 2026-06-01 |
| Barostat | `ntp=1, barostat=2` (MC) for production NPT; `ntp=0` for heating | Advisor demo standard |
| `iwrap` | `iwrap=1` for long production (prevents diffusion artifacts in trajectory) | Amber26.pdf §23.6 |
| `restraintmask` | Must reference real atoms; mask syntax per Amber26.pdf ch.25 | Advisor demo (`!:WAT,Cl-,K+,Na+ & !@H=`) |
| `ig` | `ig=-1` for randomized Langevin seed (avoids run-to-run determinism) | Best practice |

For submit scripts:
- No hardcoded paths under `/Application/`, `/opt/`, advisor-machine-specific roots.
- `AMBERHOME` resolved from environment (or `$(dirname $(which pmemd))/..`) — not literal-string-assigned.

## Procedure

**Step 0 — Read context:**
- `checks/check_amber.py` — the deterministic validator.
- `reference/canonical-recipe.md` — the 11-stage advisor demo as exemplar.
- `reference/sop3.md` — SOP §3 hard limits with rationale.

**Step 1 — Identify scope.**
- Single file → run `python3 checks/check_amber.py <file.in>`.
- Directory → run `python3 checks/check_amber.py <dir>/` (validates all `.in` + any `submit.sh`).
- Specific stage check → reference `reference/canonical-recipe.md` for that stage's expected shape.

**Step 2 — Run the validator.** Emits structured output:
```
[file.in]
  PASS: dt = 0.002 (within SHAKE-on limit)
  PASS: cut = 9.0 (within [8, 12])
  WARN: nmropt=1 with &wt TEMP0 ramp ends at value2=310.0 but &cntrl temp0=300.0
  FAIL: ntc=2 but ntf=1 (SHAKE bonds-to-H present in dynamics but not in force calc)
```

**Step 3 — Triage findings.**
- **FAIL** = physical-realism violation; do NOT run as-is.
- **WARN** = inconsistency or non-standard choice; needs author intent confirmation.
- **PASS** = within rule envelope; safe to proceed.

**Step 4 — Recommend fix.** For each FAIL/WARN, suggest the specific edit. Cite the rule source (SOP §3 or Amber26.pdf section). Reference `phase3_advisor_demo` memory for the heat-3 case specifically — the user has already banked context on it.

**Step 5 — Re-validate after fix.** Run again; confirm clean.

**Step 6 — If portability bug found:** Recommend the `AMBERHOME`-from-env or `which pmemd` pattern. Cite `phase3_advisor_demo` memory.

## Anti-patterns

- Do NOT silently "fix" a temp0 / &wt mismatch. The author intent matters — heat-3 might be a typo, OR it might be a deliberate over-heating. Confirm with user before editing.
- Do NOT assume the advisor's submit.sh path was intentional. The 2026-06-01 handoff explicitly carried this gotcha; it's not bug-as-feature.
- Do NOT add SHAKE constraints when the user is doing free-energy with bond-breaking. SHAKE is the default but not universal.
- Do NOT enforce `iwrap=1` on heat/min stages — only relevant for long production trajectory.
- Do NOT use this skill on QM/MM, REMD, or λ-window inputs — the validator only knows the explicit-solvent classical-MD parameter envelope. Those need a wider validator.

## Cross-references

- Memory `phase3_advisor_demo` — the canonical 11-stage recipe, restraint mask, submit.sh AMBERHOME gotcha, heat-3 temp0/&wt inconsistency.
- Memory `amber26_pdf_section_map` — jump-reads for sander §23.6 (p.429, keyword source-of-truth), pmemd §24.3 (p.499), atom-mask syntax ch.25 (p.509).
- Project `CLAUDE.md` SOP §3 — the canonical hard limits.
- Vault `phase3-explicit-solvent-md/` — the actual files this skill was designed against.
- Vault `Skill_Bounded_Recovery_AMBER.md` — Stage 8 recovery uses this same rule envelope to plan a recovery branch.
