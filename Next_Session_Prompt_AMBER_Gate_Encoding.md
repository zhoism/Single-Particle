---
tags: [project-prime, openclaw, amber, gates, failure-modes, session-handoff, encoding]
type: handoff
status: ready
created: 2026-06-19
---

# Next Session Starter — Encode the AMBER failure-mode gates (P1 backlog)

> Created 2026-06-19 after the failure-mode sweep ([[Research_AMBER_Failure_Modes]]) produced a prioritized, adversarially-reviewed candidate-gate backlog and the one shipping defect (`SYSTEM_NOT_NEUTRAL`) was already fixed as the **template**. **This is an ENCODING session, not research** — turn the top backlog candidates into real, tested, committed deterministic gates, each cleared through the full discipline. Paste the §The prompt to paste block into a fresh Claude Code session (run from the vault).

## Seed — what's already done (don't re-derive)

- **The sweep is consumed** ([[Next_Session_Prompt_AMBER_FailureMode_Sweep]] → `status: consumed`): 38 surveyed → **15 kept** (P1=4 / P2=7 / P3=4), 23 dropped with reasons. Full table + proxy invariants live in [[Research_AMBER_Failure_Modes]].
- **One candidate is already encoded — use it as the TEMPLATE.** `SYSTEM_NOT_NEUTRAL` (tleap-build) was a vacuous log-scrape; repaired to a **structural prmtop CHARGE-block** check (`prmtop_net_charge()`), with an oracle test + a regression over all real `comp_oct.top` builds (0 false-alarms). Commit `5647b0a`; test `skills/tleap-build/tests/test_neutrality_gate.py`. Read that diff first — it is exactly the shape every gate in this session should take.
- **The code repo is now PUBLISHED** (private `github.com/zhoism/Single-Particle-pipeline`, branch `main`). So unlike earlier sessions, commits here **should be pushed** (`git push origin main`), not left local-only.

## The work — encode the 4 remaining P1 candidates

Each, owning skill + the proxy invariant from [[Research_AMBER_Failure_Modes]] (read the note for the full adversarial-review caveats):

| Candidate | Skill / file | Proxy invariant | Watch-out |
|-----------|--------------|-----------------|-----------|
| **GB-radii ↔ igb mismatch** | `cpptraj-analysis` (root cause in `tleap-build`) | grep prmtop `%FLAG RADIUS_SET`; assert it matches the `igb` in `mmgbsa.in` via Amber Table 4.1 (igb 1→mbondi, 2\|5→mbondi2, 7→bondi, 8→mbondi3) | Highest-impact (fires on **every** run today). The detection GATE is safe; the upstream FIX (`set default PBRadii mbondi2` in tleap) **changes the built radii → shifts MM-GBSA ΔG**, so it needs a happy-path re-run + a new ΔG baseline. Treat gate vs. fix separately; the fix touches `build_leap_in` → STOP-and-surface before changing the recipe. |
| **`SOLVENT_NOT_ADDED`** | `tleap-build` | assert WAT count in `comp_oct` prmtop ≥ floor (≥100; real runs 1890–8290) **and** `solvent_residues_added > 0` | The **prmtop-WAT-count** half is load-bearing; the log-regex half shares the brittleness that killed `SYSTEM_NOT_NEUTRAL`. Cleanest/safest — closest sibling to the template. |
| **`CROSS_GAP_SPURIOUS_BOND`** | `tleap-build` | scan `leap.log` for `bond of\s+([0-9.]+)\s+angstroms`; assert no captured length > ~3.0 Å | It scrapes tleap's OWN warning (a log-scraper, not a geometry oracle) — tune the bound; don't oversell it. Disulfide/covalent-ligand `bond` commands are the only legit >3 Å case (not on the happy path). |
| **PLIP `--nohydro`** | `plip-profile` | (a) hard-assert `--nohydro` is in the PLIP argv; (b) run PLIP twice on a fixed frame, require identical `totals.by_type` | Adding `--nohydro` shifts trust to OpenBabel bond perception — a real trade-off, not free. The argv assertion is zero-false-alarm; the twice-run diff over-triggers until `--nohydro` lands. |

P2/P3 stay backlog unless one clears the full bar trivially. **Do AT MOST these 4 (plus any P2 that is genuinely cheap + clean).**

## Decisions banked — do NOT re-litigate

- **Every gate clears the full discipline** ([[Eval_Criteria]]): cheap deterministic **proxy invariant** → **oracle/regression test** → **adversarial review** → **commit + push**. A gate is `inferred` until it clears all four.
- **Prefer STRUCTURAL prmtop/file checks over `leap.log`-regex scraping** — the `SYSTEM_NOT_NEUTRAL` failure was exactly a log-scrape that silently stopped matching. (CROSS_GAP is unavoidably a log-scrape; bound it conservatively and label it.)
- **Prove no false-alarm before committing:** run each new gate over ALL real GREEN artifacts in the repo (the 48-build regression pattern from the template). A gate that reddens a known-good build is wrong.
- **The frozen core stays frozen.** Add gates to the existing `validate()`; do NOT modify `run_happy_path.sh`; do NOT restructure a wrapper (STOP-and-surface if a candidate needs wire-in). No auto-generated gates — the LLM proposes, a human-cleared deterministic check is the only trusted thing.
- **If a NEW shipping silent failure surfaces** (a gate we thought existed but is vacuous, like SYSTEM_NOT_NEUTRAL was), STOP and flag it loudly — correctness issue, not a backlog item.

## NOT in scope (explicitly)

- **Expanding `mdin-edit`'s param whitelist is a SEPARATE feature, not this session.** mdin-edit currently edits 5 params (`dt, temp0, cut, nstlim, restraint_wt`, in `HARD_BOUNDS`). Broadening it (e.g. `gamma_ln`, `taup`, `ntpr`) is its own small task. The ONLY link to this session is the shared `check_amber` bounds layer: if you add a new `check_amber` invariant for an MD-namelist param here, that bound becomes the natural thing a future whitelist expansion would reuse. Do not conflate the two.
- The outer proposer-agent ([[Future_Work_Proposer_Agent]]) — opt-in, decision-gated.

## The prompt to paste

```
Continuation of the Single Particle / OpenClaw + AMBER project. This is an ENCODING session: turn the top candidates from the failure-mode sweep into real, tested, committed deterministic gates. The pipeline is feature-complete (9 green wrapper skills) and the code repo is now published (private github.com/zhoism/Single-Particle-pipeline, branch main) — push commits, don't leave them local.

Read these BEFORE acting (in order):
- vault: Next_Session_Prompt_AMBER_Gate_Encoding.md (THIS plan — the 4 P1 candidates + the discipline + the scope fence)
- vault: Research_AMBER_Failure_Modes.md (the full backlog + proxy invariants + adversarial caveats), Gap_Gate_Coverage.md, Eval_Criteria.md (the four-step gate discipline)
- code: skills/tleap-build/scripts/wrapper.py (the prmtop_net_charge / SYSTEM_NOT_NEUTRAL fix at commit 5647b0a) + skills/tleap-build/tests/test_neutrality_gate.py — this is the TEMPLATE every gate should copy.
- memory: project-prime-status, feedback-verify-and-eval. Check vocabulary.md before any new term.

Banked, do NOT re-litigate:
- Encode AT MOST the 4 remaining P1s (GB-radii/igb, SOLVENT_NOT_ADDED, CROSS_GAP bond, PLIP --nohydro), each through proxy invariant -> oracle/regression test -> adversarial review -> commit + push. Prove 0 false-alarms by running each gate over ALL real GREEN artifacts first.
- Prefer structural prmtop/file checks over leap.log scraping. Frozen core stays frozen (no run_happy_path.sh edits, no wrapper restructuring -> STOP-and-surface). No auto-generated gates.
- GB-radii: the GATE (detect mismatch) is safe, but the upstream FIX (set default PBRadii mbondi2) changes built radii -> shifts MM-GBSA dG -> needs a happy-path re-run + new baseline. STOP-and-surface before changing the recipe.
- NOT in scope: expanding mdin-edit's param whitelist (separate feature; only shared link is check_amber bounds).
- If a new vacuous/shipping silent failure surfaces, STOP and flag it loudly.

Sequence: for each P1 — (1) read the candidate + owning wrapper; (2) write the proxy invariant into the existing validate(); (3) write an oracle test (neutral/positive/malformed) + a regression over all real artifacts; (4) run both python versions (py3.9/3.11 system + conda); (5) adversarial self-check (does it fire? false-alarm? vacuous?); (6) commit + push. Then update Research_AMBER_Failure_Modes.md (mark encoded), Gap_Gate_Coverage.md, devlog-append, and project-prime-status memory.

Scope-fence: encode at most the 4 P1s, fully disciplined, committed + pushed. Do NOT modify run_happy_path.sh, do NOT touch mdin-edit's whitelist, do NOT change the GB radii recipe without surfacing the dG-baseline impact first.
```

## After the session — update this file

1. Flip `status: ready` → `status: consumed`.
2. Add an `## Outcome` footer: how many P1s encoded, commits/pushes, any that hit STOP-and-surface (GB-radii recipe), any new shipping defect found, links to the updated [[Research_AMBER_Failure_Modes]] + [[Dev_Log]].

## Cross-links

- [[Research_AMBER_Failure_Modes]] — the backlog + proxy invariants (the source of truth for this session).
- [[Gap_Gate_Coverage]] — the coverage gap each encoded gate further fills.
- [[Eval_Criteria]] — the proxy-invariant → oracle-test → adversarial-review → commit discipline.
- [[Next_Session_Prompt_AMBER_FailureMode_Sweep]] — the (consumed) sweep that produced the backlog + the `SYSTEM_NOT_NEUTRAL` template fix.
- [[Design_Determinism_Spectrum]] — why gates are the safety boundary; why we never auto-author them.
- memories: [[project-prime-status]], [[feedback-verify-and-eval]], [[amber26-pdf-section-map]].
