---
tags: [project-prime, openclaw, amber, mdin-edit, feature, session-handoff]
type: handoff
status: ready
created: 2026-06-19
---

# Next Session Starter — Expand the `mdin-edit` editable-parameter whitelist

> Created 2026-06-19. **This is a FEATURE session for ONE skill (`mdin-edit`), not a gate-encoding/validation session.** Goal: let the NL parameter-editor safely edit *more* `&cntrl`/`&wt` parameters than the current five. It is deliberately **separate** from the AMBER gate-encoding work ([[Next_Session_Prompt_AMBER_Gate_Encoding]]) — the only shared thing is the `check_amber` bounds layer. Paste the §The prompt to paste block into a fresh Claude Code session (run from the vault).

## Why this is low-friction (the seed — don't re-derive)

`mdin-edit` already does idempotent, byte-minimal, bounds-checked, self-checked, stage-aware edits. Its **rendering layer already recognizes** the candidate params — they're in `FLOAT_PARAMS`/`INT_PARAMS` so they render correctly; they're simply **not yet editable** because they lack a `HARD_BOUNDS` entry:

```python
# skills/mdin-edit/scripts/wrapper.py (current)
INT_PARAMS   = {"nstlim", "istep1", "istep2", "maxcyc", "ncyc"}
FLOAT_PARAMS = {"dt", "cut", "temp0", "restraint_wt", "value1", "value2",
                "tempi", "gamma_ln", "pres0", "taup"}
HARD_BOUNDS  = { dt, temp0, restraint_wt, nstlim, cut }   # <- the editable whitelist (5)
SUPPORTED_PARAMS = set(HARD_BOUNDS)
```

So expanding the whitelist = **add a `HARD_BOUNDS` entry (bound + message) + stage-applicability + acceptance/oracle cases** for each new param. The rendering is already correct.

## The plan

### Tier 1 — safe scalar adds (rendering ready; do these)

Each is a scalar with a clear physical bound and a clear stage applicability. **Source the bound from `check_amber`/Amber26 §23.6, do NOT invent it.** Verify each against the manual before encoding.

| Param | Proposed bound (verify!) | Applies to (stage gate) | Notes |
|-------|--------------------------|--------------------------|-------|
| `gamma_ln` | `1.0 ≤ gamma_ln ≤ 5.0` (check_amber `GAMMA_LN_RANGE`) | Langevin stages only (`ntt=3`) — heat/density/prod, **skip in min** | Reuse check_amber's existing range verbatim. |
| `taup` | `0 < taup ≤ ~10 ps` (typical 1–5) | NPT only (`ntp=1`) — density/press | Pressure relaxation time. |
| `pres0` | `~1.0` (e.g. `0 < pres0 ≤ ~10 bar`) | NPT only (`ntp=1`) | Reference pressure; rarely changed. |
| `tempi` | `0 ≤ tempi ≤ 400 K` | heat stages | Initial temperature (often 0 on restart). |
| `maxcyc` (int) | `maxcyc > 0` | minimization only (`imin=1`) | Min cycle count. |
| `ncyc` (int) | `0 < ncyc ≤ maxcyc` | minimization only (`imin=1`) | Steepest-descent→CG switch; **coupled to `maxcyc`** — validate the pair. |

The stage-applicability pattern already exists (`restraint_wt` keys off `ntr`; `temp0` couples to `&wt value2`) — mirror it: a param is editable in a stage only when the namelist context makes it meaningful; skip-in-group / fail-on-single when not.

### Tier 2 — DEFER (regime-changing / coupled; NOT scalar value edits)

Do **not** add these as simple whitelist entries — they change the physics regime or need cross-param coupling logic:
- `ntc`/`ntf` (SHAKE), `ntb`/`ntp` (ensemble), `ntt` (thermostat type), `imin` — changing any of these alters what *other* params mean (e.g. `ntt` changes whether `gamma_ln`/`tautp` apply). A value-editor must not flip regimes silently.
- `istep1`/`istep2` (the `&wt` ramp step window) — coupled to `nstlim` and the `value1→value2` ramp; editing them needs ramp-consistency logic, not a scalar bound. Borderline; design the coupling explicitly or leave for a later tier.

If a requested param is Tier 2, the skill should **reject it with a clear message** (not silently edit) — same posture as today's `PARAM_NOT_FOUND`/out-of-scope handling.

## Decisions banked — do NOT re-litigate

- **Bounds come from `check_amber`/Amber26 §23.6, never invented.** Where check_amber already has the rule (e.g. `gamma_ln` 1–5), reuse it verbatim so the editor and the validator agree. *(This is the only real link to the [[Next_Session_Prompt_AMBER_Gate_Encoding|gate-encoding session]]: if that session adds a new check_amber MD-namelist invariant, source the matching whitelist bound from it.)*
- **Every new param keeps the skill's invariants:** idempotent (re-run byte-identical), byte-minimal (numeric-token replace, never append), bounds-checked, stage-aware, post-edit self-check, all-or-nothing batch.
- **Extend BOTH test layers:** the byte-level `test_acceptance.sh` (add golden + out-of-bounds + wrong-stage + idempotency cases per new param) AND the `tests/` harness (independent oracle + fuzz/matrix + mutation) — that harness is the regression guard; a new param that isn't covered by it isn't done.
- **Tier 2 params stay rejected**, not silently edited. No regime flips.
- This is a **single-skill feature**, scoped to `mdin-edit`. It does NOT touch the other 8 skills, `run_happy_path.sh`, or the gate backlog.

## What's NOT in scope

- The AMBER failure-mode **gate-encoding** session ([[Next_Session_Prompt_AMBER_Gate_Encoding]]) — different layer (detection invariants in tleap/antechamber/cpptraj/plip), different skills.
- Adding NEW namelists or restructuring the advisor's `mdin` set — this only widens which existing params are editable.

## The prompt to paste

```
Continuation of the Single Particle / OpenClaw + AMBER project. This is a FEATURE session for ONE skill: expand mdin-edit's editable-parameter whitelist. It is SEPARATE from the gate-encoding work — only shared link is the check_amber bounds layer.

Read BEFORE acting:
- vault: handoffs/Next_Session_Prompt_mdin_edit_Whitelist.md (THIS plan — the Tier-1 params + bounds + the Tier-2 defer list + the discipline)
- code: skills/mdin-edit/scripts/wrapper.py (HARD_BOUNDS / FLOAT_PARAMS / INT_PARAMS / the stage-applicability + temp0<->&wt coupling), skills/mdin-edit/tests/ (the oracle+fuzz+mutation harness), skills/mdin-edit/test_acceptance.sh, references/mdin-params.md (the Amber26 §23.6 write-up)
- code: skills/*/check_amber*.py (the bounds source — reuse, don't invent)
- memory: project-prime-status, feedback-verify-and-eval. Check vocabulary.md before any new term.

Banked, do NOT re-litigate:
- Add Tier-1 scalar params only (gamma_ln, taup, pres0, tempi, maxcyc, ncyc), each: a HARD_BOUNDS entry with a check_amber/Amber26-sourced bound + stage-applicability (mirror how restraint_wt keys off ntr) + byte-level acceptance cases + tests/-harness coverage.
- ncyc is coupled to maxcyc (0 < ncyc <= maxcyc) — validate the pair.
- DEFER Tier-2 (ntc/ntf/ntb/ntt/imin/istep1/istep2): regime-changing or coupled; reject with a clear message, do NOT silently edit.
- Keep ALL existing mdin-edit invariants (idempotent, byte-minimal, self-check, all-or-nothing). The repo is published (private github.com/zhoism/Single-Particle-pipeline, main) -> commit + push.

Sequence: for each Tier-1 param — (1) confirm the bound against check_amber/Amber26 §23.6; (2) add the HARD_BOUNDS entry + stage-applicability; (3) add byte-level acceptance cases (golden / out-of-bounds / wrong-stage / idempotent) + extend tests/ oracle+fuzz+mutation; (4) run the full harness under py3.9 (system) + py3.11 (conda); (5) commit + push. Then devlog-append + update project-prime-status.

Scope-fence: mdin-edit ONLY. Add Tier-1 scalars, fully tested + committed + pushed. Do NOT add Tier-2 regime params, do NOT touch other skills or run_happy_path.sh.
```

## After the session — update this file

1. Flip `status: ready` → `status: consumed`.
2. Add an `## Outcome` footer: which params were added, bounds used (+ source), tests added, commits/pushes, any Tier-1 param that turned out to need coupling (moved to Tier-2).

## Cross-links

- [[Next_Session_Prompt_AMBER_Gate_Encoding]] — the sibling (gate-encoding) session; separate work, shared `check_amber` foundation.
- [[Eval_Criteria]] — verify-and-eval discipline (acceptance + adversarial review).
- memories: [[project-prime-status]], [[feedback-verify-and-eval]], [[amber26-pdf-section-map]] (the manual jump-table; §23.6 = sander/pmemd namelist params).
