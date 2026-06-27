---
tags: [project-prime, gap, gates, failure-modes]
type: gap
status: partially-filled
identified-from:
  - "[[Next_Session_Prompt_AMBER_FailureMode_Sweep]]"
  - "[[Eval_Criteria]]"
filled-by:
  - "[[Research_AMBER_Failure_Modes]]"
---

# 🟡 Gap: Is the deterministic gate set derived from the field's known failure modes, or only from what we hit?

> Gap note. `status: partially-filled` — the gap was **surveyed** 2026-06-19 (no longer un-examined), but most surveyed candidates are still un-encoded backlog, and one shipping gate was found broken. Surface this whenever a report or design claim asserts "we cover AMBER's failure modes."

## What the gap is

The pipeline's safety argument rests on its deterministic gates ([[Design_Determinism_Spectrum]]). Until 2026-06-19 that gate set was **reactive + opportunistic**: the textbook physical-realism limits in `check_amber`, plus the handful of silent failures we personally crashed into or surfaced adversarially (e.g. [[antechamber-aromatic-kekulize-bug]]). It was **not** derived from a systematic reading of AMBER's large *documented* corpus of "ways it silently does the wrong thing" (the manual's known-limitations, the mailing-list archives, documented GAFF/antechamber mis-typing, tleap/MMPBSA caveats).

## Why it matters

It is the difference between a defensible report claim ("covers physical-realism limits + a surveyed set of known failure modes, acknowledged-incomplete") and an overclaim ("encodes the field's accumulated knowledge"). It also determines how far the [[Future_Work_Proposer_Agent]] could ever safely roam — capability is bounded by what the verifier can check, so growing the gate set *is* growing safe capability.

## What partially fills it (2026-06-19)

[[Research_AMBER_Failure_Modes]] — the first systematic per-stage sweep of primary sources → a prioritized, adversarially-reviewed candidate-gate backlog (38 surveyed → 15 kept: P1=4 / P2=7 / P3=4; 23 dropped with reasons). This converts the gap from *un-examined* to *surveyed-with-a-backlog*.

It also surfaced — and this session **fixed** — a **currently-shipping correctness defect**: `SYSTEM_NOT_NEUTRAL` in `tleap-build` was **vacuous on 100% of production runs** (its `leap.log` regex never matched the skill's output) and would **false-fire** if it ever did (it captured the pre-neutralization charge). Verified across all 13 production `leap.log`s, then **repaired** to a structural prmtop CHARGE-block check (project-prime `5647b0a`, local). This is itself evidence for the gap: a gate we *believed* protected the pipeline did not.

**2026-06-26 code-audit pass — 2 more silent-failure→gate encodings + the test layer hardened** (branch `fix/audit-gates-and-tests-20260626`, merged to `main` `fb6c1a9` + pushed to origin/main). A full read-only audit of the executable surface (~5k LOC python + ~1k LOC shell) → 6 verified bugs fixed test-first. Two are new gates of the canonical silent-failure→gate kind ([[antechamber-aromatic-kekulize-bug]] template): (a) the golden-path/smoke-test `assert_no_nan` divergence gate **missed `Infinity`** (gfortran prints the literal token; a run diverging to Infinity passed as clean) → now `NaN|[-+]?Infinity\b|******`, aligned with [[Skill_Bounded_Recovery_AMBER]]'s detector; (b) `antechamber-ligandprep`'s `validate()` **silent-passed an empty/whitespace frcmod** (no ATTN lines ⇒ no error) → explicit empty-frcmod gate. Both proven RED→GREEN + real-toolchain smoke (no false-fire on a real frcmod). Also closed the **test-coverage** half of the gap for 4 under-tested skills (cpptraj-analysis / antechamber / tleap-build / pipeline-async had only acceptance scripts → added deterministic oracles + a shell-gate suite). Same lesson reinforced: prefer structural/value checks; an Infinity-blind regex is the divergence-gate analogue of the SYSTEM_NOT_NEUTRAL log-scrape miss.

**2026-06-27 P1-encoding pass — all 4 P1 candidates encoded** (project-prime `main` `f188b79` + `7582194`, pushed). `SOLVENT_NOT_ADDED` (structural WAT-count) + `CROSS_GAP_SPURIOUS_BOND` (bounded `bond of N angstroms` log-scrape, ground-truthed by a real induced gap + committed fixture) in tleap-build; PLIP `--nohydro` determinism guard in plip-profile — all **FATAL**, 0 false-fire over the real GREEN artifacts. The 4th, **GB-radii ↔ igb**, was encoded as a **NON-FATAL detector** (`GB_RADII_IGB_MISMATCH`) by user decision — a fatal gate would redden every run and the mbondi2 fix shifts the reported ΔG, so the fix is deferred to [[Next_Session_Prompt_GB_Radii_Fix]] (the detector is the tripwire; flip-to-fatal is one line). Each cleared the full [[Eval_Criteria]] discipline + adversarial review (all SOUND). Details + per-candidate verification in [[Research_AMBER_Failure_Modes]] (now `status: p1-encoded`). The P2/P3 backlog (11) stays open. The posture stays **surveyed + acknowledged-incomplete**, never "complete."

## What would fully fill it

1. **✅ P1s ENCODED 2026-06-27** — all four top candidates from [[Research_AMBER_Failure_Modes]] cleared the full discipline ([[Eval_Criteria]]: cheap deterministic proxy → oracle/regression test against the real GREEN artifacts → adversarial review → commit + push). 3 fatal + 1 non-fatal detector (GB-radii, fix deferred to [[Next_Session_Prompt_GB_Radii_Fix]]). **Lesson reinforced:** prefer **structural prmtop/file checks over `leap.log`-regex scraping** (SOLVENT counted from RESIDUE_LABEL, neutrality from the CHARGE block); where a log-scrape is unavoidable (CROSS_GAP — teLeap's own warning is the only signal) bound it conservatively AND pin it to a real induced-gap fixture. Remaining: the P2/P3 backlog (11).
2. **✅ DONE — `SYSTEM_NOT_NEUTRAL` redesigned** to read the prmtop CHARGE block (sum ÷ 18.2223, assert `|q| < 0.5`) instead of scraping the log (project-prime `5647b0a`, oracle + 48-build regression). The first application of the "structural over log-scrape" lesson.
3. **Keep the posture honest:** even after encoding, the claim stays "surveyed + acknowledged-incomplete," never "complete." No auto-generated gates — the LLM proposes; a human-cleared deterministic check is the only thing trusted ([[Design_Determinism_Spectrum]]).

## Cross-links
- [[Research_AMBER_Failure_Modes]] — the survey + backlog (the partial fill).
- [[Eval_Criteria]] — the four-step gate discipline.
- [[Design_Determinism_Spectrum]] — why gates are the safety boundary; why we never auto-author them.
- [[antechamber-aromatic-kekulize-bug]] — the canonical silent-failure→gate template.
- [[Next_Session_Prompt_ntx_irest_CoherenceGate]] — the `ntx`↔`irest` coherence gate (was the `Gap_ntx_irest_restart_topology` note, now a ready encoding-session handoff; `check_amber` has none today).
- [[Gap_Remote_HPC_Backend]], [[Gap_MachineLearned_ForceFields]] — sibling open gaps.
