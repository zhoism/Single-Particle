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

**2026-06-27 — new candidate (mdin-edit / vendored validator numeric-parser scope).** The [[Next_Session_Prompt_mdin_edit_CoherenceFix|mdin-edit coherence-gate]] adversarial review surfaced a **pre-existing parser-scope gap shared by the coupling, the new `temp0`/`&wt value2` gate, AND the vendored `check_amber` validator**: the numeric/namelist regexes (`num`, `VAL`/`KV_RE`, `temp0_wt_span`) read only **single-quoted `type = 'TEMP0'`** blocks and **plain-decimal** tokens. Two silent-wrong classes follow on *arbitrary* (non-advisor) mdin: (a) a Fortran **`d`-exponent** literal like `value2 = 3.05d2` (= 305.0 to AMBER) is truncated to `3.05` → phantom mismatch, and a `--couple` rewrite produces `305.0d2` = **30 500 K** shipped `ok:true` (the self-check shares the blind spot, so it can't catch it); (b) a **non-finite** token (`nan`/`inf`) → `num()` returns NaN, not None → `nan > 0.5` is False → reads as coherent. Because the gate stays *consistent* with the validator (both blind), this was **not** treated as a Phase-2 regression — and Phase 2 actually *improves* the `d`-exponent case (it halts instead of silently corrupting). Candidate gate (P2-ish): reject any `temp0`/`value2` token that doesn't fully match the ASCII-finite-decimal grammar (`_VAL_ASCII` already exists for *input* validation) as `INVALID_VALUE` **before** the coherence decision — fixed in the shared parser layer, not bolted onto the gate (which would create gate↔validator inconsistency). Same "handle the parse edge structurally" family as the `assert_no_nan`/Infinity miss above. Lower priority than the P1 survey items; the advisor's demo uses neither form.

## What would fully fill it

1. **Encode the validated top candidates** (start with the P1s in [[Research_AMBER_Failure_Modes]]), each cleared through the full discipline ([[Eval_Criteria]]: cheap deterministic proxy → oracle/regression test against the real GREEN artifacts → adversarial review → local commit). **Lesson banked:** prefer **structural prmtop/file checks over `leap.log`-regex scraping** — the SYSTEM_NOT_NEUTRAL failure is exactly a log-scraping gate that silently stopped matching.
2. **✅ DONE — `SYSTEM_NOT_NEUTRAL` redesigned** to read the prmtop CHARGE block (sum ÷ 18.2223, assert `|q| < 0.5`) instead of scraping the log (project-prime `5647b0a`, oracle + 48-build regression). The first application of the "structural over log-scrape" lesson.
3. **Keep the posture honest:** even after encoding, the claim stays "surveyed + acknowledged-incomplete," never "complete." No auto-generated gates — the LLM proposes; a human-cleared deterministic check is the only thing trusted ([[Design_Determinism_Spectrum]]).

## Cross-links
- [[Research_AMBER_Failure_Modes]] — the survey + backlog (the partial fill).
- [[Eval_Criteria]] — the four-step gate discipline.
- [[Design_Determinism_Spectrum]] — why gates are the safety boundary; why we never auto-author them.
- [[antechamber-aromatic-kekulize-bug]] — the canonical silent-failure→gate template.
- [[Next_Session_Prompt_ntx_irest_CoherenceGate]] — the `ntx`↔`irest` coherence gate (was the `Gap_ntx_irest_restart_topology` note, now a ready encoding-session handoff; `check_amber` has none today).
- [[Gap_Remote_HPC_Backend]], [[Gap_MachineLearned_ForceFields]] — sibling open gaps.
