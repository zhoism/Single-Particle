---
tags: [project-prime, openclaw, amber, mmgbsa, gates, gb-radii, session-handoff]
type: handoff
status: ready
created: 2026-06-27
---

# Next Session Starter — Apply the GB-radii (mbondi2) fix + re-baseline ΔG, then flip the detector fatal

> Created 2026-06-27 during the AMBER P1 gate-encoding session ([[Next_Session_Prompt_AMBER_Gate_Encoding]]). The GB-radii ↔ igb mismatch was the 4th P1. The **detector ships now as a NON-FATAL finding** (decision banked below); the **actual fix is deferred to this session** because it changes the reported MM-GBSA ΔG and needs a fresh baseline. This is a small, well-scoped follow-up.

## The problem (already detected, not yet fixed)

`cpptraj-analysis` runs MM-GBSA with `igb=5`, but every prmtop is built with default **`mbondi`** radii. Amber26 Table 4.1 says igb=5 is parameterized for **`mbondi2`** — so the GB solvation term is computed under mismatched radii on **100% of runs**. The mismatch is real but the error is *quiet* (ΔG stays negative and plausible — e.g. the 1L2Y baseline −18.16 was produced under the mismatch).

## What already shipped (do NOT re-derive)

- A **non-fatal detector** is live in `skills/cpptraj-analysis/scripts/wrapper.py` (project-prime, branch merged to `main` 2026-06-27): `MMGBSA_IGB = 5` (single source of truth for the igb written to `mmgbsa.in` AND the check), `IGB_RADIUS_SET` map (Amber Table 4.1), pure helpers `prmtop_radius_set()` + `gb_radii_check()`. On a mismatch it emits a `GB_RADII_IGB_MISMATCH` **finding** into `validation.gb_radii` and the mmgbsa result `note` — it is **never** appended to `errors` and never flips `ok`. Verified end-to-end: a real 1L2Y MMPBSA run stays `ok:true`, ΔG unchanged (−18.16), finding present. Oracle 60/60 (conda py3.11) + 78/78 real-prmtop regression + adversarial review SOUND.
- **Decision (2026-06-27, user):** ship the non-fatal detector now, **defer the fix** (it shifts ΔG → needs a re-baseline). The detector is the tripwire; this session lands the fix and flips it fatal.

## The work this session

1. **Pick the fix route (the one key decision — batch into a pre-run AskUserQuestion):**
   - **(a) `ante-MMPBSA.py -radii mbondi2` (PREFERRED).** Regenerate ONLY the MM-GBSA component topologies (`-cp/-rp/-lp` = comp_dry / protein / ligand) with mbondi2, inside `a_mmgbsa`, leaving the MD build recipe (`tleap-build`) untouched. Smallest blast radius; the solvated MD topology (`comp_oct`, used by pmemd) is unchanged.
   - **(b) tleap `set default PBRadii mbondi2`** before `saveamberparm` in `tleap-build/build_leap_in`. Cleaner conceptually but touches the **frozen build recipe** and rebuilds every topology → bigger surface.
   - BOTH shift the reported MM-GBSA ΔG → require a fresh happy-path run + a **new ΔG baseline number** (STOP-and-surface the new number; it supersedes −18.16 / −27.41 / etc.).
2. **Apply the chosen fix** (oracle/acceptance test it; prove the radii in the regenerated prmtop read `mbondi2` and the detector now reports `consistent:true`).
3. **Re-baseline ΔG** on 1L2Y (and ideally 3HTB), record the new numbers, annotate the old ΔGs as pre-mbondi2-fix in memory + Dev_Log.
4. **Flip the detector fatal:** the helper already returns the `GB_RADII_IGB_MISMATCH` finding — change the wire-in so it is appended to the analysis `errors` (one line; the structure is in place). Re-run the regression to prove it now stays GREEN (because the fix made every build consistent) — a gate that reddens a known-good build is wrong, so the fix MUST land before the flip.
5. Full DoD record pass + commit + push.

## Scope fence / banked

- **STOP-and-surface the new ΔG baseline number** before treating it as canonical.
- Prefer route (a) unless there's a reason to touch the build recipe; if route (b), treat `tleap-build` as frozen-core and surface the recipe change.
- Don't conflate this with the `mdin-edit` whitelist or other backlog. This is GB-radii only.
- The detector + tests already exist — this is the FIX + re-baseline + fatal-flip, not a re-encode.

## The prompt to paste

```
Continuation of the Single Particle / OpenClaw + AMBER project. Land the deferred GB-radii fix. A NON-FATAL GB_RADII_IGB_MISMATCH detector already ships in cpptraj-analysis (igb=5 but prmtops built with mbondi; Table 4.1 wants mbondi2). This session: apply the radii fix, re-baseline the MM-GBSA ΔG, then flip the detector fatal.

Read first: handoffs/Next_Session_Prompt_GB_Radii_Fix.md (THIS plan), Research_AMBER_Failure_Modes.md (P1 #1), Eval_Criteria.md. Code: skills/cpptraj-analysis/scripts/wrapper.py (prmtop_radius_set / gb_radii_check / a_mmgbsa). Memory: project-prime-status.

Key decision (pre-run AskUserQuestion): fix route (a) ante-MMPBSA.py -radii mbondi2 (GB-only, preferred) vs (b) tleap set default PBRadii mbondi2 (touches the build recipe). BOTH shift ΔG -> STOP-and-surface the new baseline number.

Then: apply fix (test it: regenerated prmtop reads mbondi2, detector -> consistent:true), re-baseline ΔG on 1L2Y (+3HTB), annotate old ΔGs as pre-fix, flip the detector finding -> fatal (one-line wire-in change; the helper already returns it), prove the regression stays GREEN. Parallel session -> isolate in a git worktree. Full DoD record pass + commit + push.
```

## After the session — update this file

1. Flip `status: ready` → `status: consumed`.
2. Add an `## Outcome`: route chosen, new ΔG baseline(s), commit hashes, detector-fatal flip confirmed.

## Cross-links
- [[Research_AMBER_Failure_Modes]] — P1 #1 (the source of this gate).
- [[Next_Session_Prompt_AMBER_Gate_Encoding]] — the session that shipped the non-fatal detector.
- [[Gap_Gate_Coverage]] — coverage this completes.
- [[Eval_Criteria]] — the pre-run-gate + ΔG-sanity discipline.
- memories: [[project-prime-status]], [[feedback-verify-and-eval]], [[amber26-pdf-section-map]].
