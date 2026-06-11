# Example: NO row with thesis hardening (Exscientia, 2026-05-27)

Verbose Gemini intake → NO row after the load-bearing claim was verified false.

## What came in (summarized)

Block (verbose teardown, no provenance tags). An uncited "Actionable Engineering Takeaways" paragraph claimed Exscientia's orchestrator "catches the error, reduces the timestep, increments the Langevin seed, and re-queues the crashed λ-window" — **Prime's exact niche**.

## What verification found

- **Claim unsubstantiated.** No evidence in Exscientia's papers, BioSimSpace docs, changelog, or GitHub issues of autonomous crash→param-mutation→re-queue. It's Gemini's own *architectural advice to the reader* (the section literally listed "Open-Source Tooling to Evaluate" as the framing), not a Exscientia feature. BioSimSpace is an interoperability/process layer; users hit crashes and fix them manually.
- **Real papers exist, neither about recovery:**
  - JCTC 2025 21(2):967 (`10.1021/acs.jctc.4c01427`) = ML/MM end-state corrections (ANI-2x/AIMNet2) for RBFE accuracy.
  - JCIM 2024 (`10.1021/acs.jcim.4c00220`) = active-learning triage (GP + Chemprop) — largely a **University of Edinburgh (Mey lab)** paper w/ Exscientia co-authors (org-halo trim).
- **Org context:** Recursion **completed its acquisition of Exscientia 2024-11-20** (SEC 6-K confirmed). Exscientia is now part of Recursion, which already holds the LOWE row.

## Decision

**NO row — default-NO holds on all three counts:**
1. **No new bottleneck:** Exscientia's MD work spreads across already-owned cells (binding affinity→FEP+, AL triage→LOWE, NNP correction/torsion fitting→Espaloma + MLIP engines).
2. **Not a new player:** now part of Recursion.
3. **Its standout claim, once corrected, is a third instance of the autonomy gap** (orchestrate/restart/triage, but don't autonomously mutate physics) alongside Multisim and Orion.

## Hardening pass

Banked point (3) as a one-sentence hardening of the **"open gap — autonomy" bullet** in *Where Project Prime fits*. Names Exscientia/BioSimSpace and explicitly states the auto-recovery claim could not be substantiated. Inoculates the thesis against the exact misconception that would arise if a reader independently encountered the same uncited claim.

## What did NOT happen

- NO matrix row.
- NO scope-out row (it's not materials — it's a deliberate redundancy no-add).
- Frontmatter `revision: 6`.
- New fabrication pattern logged in `phase1-report-format` memory.

## Mistake caught + corrected SAME SESSION

First pass: put a *defensive rebuttal* of the auto-recovery claim into the "open gap — autonomy" bullet. Re-pass with corrected intake: Exscientia is orthogonal — not a recovery near-miss like Multisim/Orion — so that placement was a category mismatch rebutting a claim the reader never sees.

**Removed** the rebuttal. **Restored** the clean Multisim+Orion autonomy-gap pair. **Added** one correctly-categorized orthogonal-accuracy line in the engine/prep grouping, citing JCTC 2025 (`4c01427`).

## Takeaways for the skill

- **Fabricated-recovery is THE thesis-threatening pattern.** Always verify autonomy claims against actual product docs / issue trackers.
- **Hardening only belongs in the report when a reader could independently reach the misconception.** If the claim is invisible (only in the Gemini block), don't import the rebuttal — it imports the misconception.
- **Org acquisitions matter.** Check current ownership before treating a tool as a standalone player.
- **Don't conflate orthogonal-accuracy with near-miss-recovery** when placing the hardening — they go in different bullets.
