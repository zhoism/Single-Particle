---
tags: [project-prime, handoffs, status, priority, index]
type: status
status: active
updated: 2026-06-27
---

# Forward queue — status & priority dashboard

> At-a-glance view of every open handoff / future-work / gap, so we always know **what's next**. The per-file `status:` frontmatter is the **source of truth**; `README.md` has the richer per-item annotations; this is the compact dashboard. Snapshot **2026-06-27** (project-prime `5d500b0`, both clean + pushed). The 3 concurrent 2026-06-27 sessions (Hermes-eval · AMBER-gate-encoding · mdin-coherence-fix) plus the graphify trial and the parallel-session code review all **merged + consumed**; the **7 consumed handoff files were removed from this folder 2026-06-27** (ntx_irest_CoherenceGate landed same day; Outcome record retained in the Consumed section below + memory + `Dev_Log.md`).

## ⭐ Priority queue (set the order here)

*Suggested seed below — tell me your order and I'll lock it in. Dependencies noted; you can't sanely put #6 before #1, etc.*

| Order | Item | Why here |
|---|---|---|
| 1 | **GB_Radii_Fix** | The remaining `Gap_Gate_Coverage` gate work (ntx_irest landed 2026-06-27): apply `mbondi2` + re-baseline ΔG + flip the GB-radii detector fatal. |
| 2 | **RunOutput_Convention** | Cheap hygiene — stops recurring git-noise; needs one verifying re-run. |
| 3 | **mdin_edit_Whitelist** | Incremental capability (more editable params). |
| — | *candidates (4–8)* | Decision-gated — promote when you decide to start one (see below). |

*Newly Ready — **slot into the order where you want**: **GB_Radii_Fix** (apply the `mbondi2` fix + re-baseline ΔG + flip the GB-radii detector fatal; gates' deferred 4th-P1 follow-up) · **GateHardening_Followups** (non-blocking durability/test-quality nits from the 2026-06-27 code review — PASS, no blockers). Order above is the prior seed minus the items consumed today — re-rank as you like.*

*(Consumed 2026-06-27 → see Consumed below: ntx_irest_CoherenceGate, HermesAgent_Eval, AMBER_Gate_Encoding, mdin_edit_CoherenceFix, Graphify_ReferenceCorpus, CodeReview_Parallel_Sessions.)*

## 🟢 Ready — paste-and-go

| Handoff | What | Status |
|---|---|---|
| **GB_Radii_Fix** | Apply the `mbondi2` fix + re-baseline ΔG, then flip the GB-radii detector fatal | `ready` |
| **mdin_edit_Whitelist** | Expand mdin-edit's editable-parameter set | `ready` |
| **GateHardening_Followups** | Non-blocking durability/test-quality/doc nits from the 2026-06-27 code review (6 small test-first tasks; tasks 1–3 carry the value) | `ready` |

## 🟡 Candidate — needs a "go" / approach decision first

| Handoff | What | Status |
|---|---|---|
| **RunOutput_Convention** | Route all runs under the ignored `runs/` dir (kill git-noise at the source); symptom tidy already landed (`b375f39`) | `candidate` |
| **mdin_edit_Arbitrary_Shapes** | Make mdin-edit edit ANY mdin set (stage-name-agnostic + multi-card `TEMP0`) — do after CoherenceFix | `candidate` |
| **Run_Confirmation_Gate** | Confirm-before-launch; **approach picked 2026-06-27 = Level 2 + TTY**; low-urgency (advisor #4 shipped at edit level) | `candidate` |
| **Proposer_Agent** | Outer propose-then-verify agent around the frozen core (oracle-first plan); biggest agentic expansion | `candidate` |
| **Headroom_ContextCompression** | Compress tool-output for token savings; low urgency on free tier | `candidate` |

## 🔵 Big open directions (Gap notes — not paste-ready)

| Gap | What | Status |
|---|---|---|
| **Gap_Remote_HPC_Backend** | Production remote HPC backend (Scenario B). **Externally blocked** — needs Single Particle to provide it; can't be "next" by choice. | `open` |
| **Gap_Gate_Coverage** | Umbrella for the 15 candidate gates (P1=4/P2=7/P3=4); #2 & #3 above burn it down. | `partially-filled` |
| **Gap_MachineLearned_ForceFields** | Would ML force fields help; espaloma-parameterization the architecture-preserving experiment. | `open` |

## Dependencies / sequencing

- **Arbitrary_Shapes** follows the now-landed **CoherenceFix** (consumed 2026-06-27).
- **GB_Radii_Fix draws from Gap_Gate_Coverage** — the P1 batch + `ntx_irest_CoherenceGate` landed 2026-06-27 (both consumed); GB_Radii_Fix is the remaining gate work.
- **Gap_Remote_HPC** is externally blocked — priority can't make it happen.

## 🔀 Concurrency — parallel-safe map (RETIRED 2026-06-27)

✅ The three concurrent 2026-06-27 sessions (Hermes-eval · AMBER-gate-encoding · mdin-coherence-fix) all **merged to `main` + cleaned up** (worktrees removed, branches deleted in both repos). The live collision map is retired. The reusable principle for the next parallel burst: sessions clash if they share **files** (stage explicit paths; isolate worktrees), **runtime** (one OpenClaw gateway / one toolchain runner), or **vault/memory** (Dev_Log/MAP/Gap are git-mergeable — stack newest-first; `MEMORY.md`/`project_prime_status.md` are outside git → serialize, re-read before edit).

## ✔ Consumed (done, for the record — the 7 handoff files were removed from this folder 2026-06-27; the record below + memory + `Dev_Log.md` are now canonical)

- **ntx_irest_CoherenceGate** (2026-06-27) — `ntx`↔`irest` restart-coherence gate **ENCODED** (project-prime `5d500b0`; `check_amber.py` + 3 vendored copies; FATAL `irest/ntx incoherent`, real-pmemd-ground-truthed — pmemd aborts `"ntx and irest are inconsistent!"`). Review found+fixed a HIGH `parse_namelists` comment-truncation bug (gate hardened locally; shared-parser fix deferred). #2 editor-toggle / #3 advisory stay deferred. [[Gap_Gate_Coverage]].
- **AMBER_FailureMode_Sweep** — produced `Research_AMBER_Failure_Modes` + `Gap_Gate_Coverage` (the gate backlog above).
- **HermesAgent_Eval** (2026-06-27) — evaluated → **declined** (research only, no migration). Produced [[Research_Hermes_Agent]]; engine room stays frozen; the one thesis-compatible coupling (a gated recovery *proposer*) folds into **Proposer_Agent** + `Gap_Gate_Coverage`.
- **AMBER_Gate_Encoding** (2026-06-27) — all **4 P1 gates encoded** (project-prime `f188b79`/`7582194`, merged `origin/main`): `SOLVENT_NOT_ADDED` + `CROSS_GAP_SPURIOUS_BOND` (tleap-build, FATAL) + PLIP `--nohydro` guard + non-fatal `GB_RADII_IGB_MISMATCH` detector. The detector's actual fix → newly-Ready **GB_Radii_Fix**.
- **mdin_edit_CoherenceFix** (2026-06-27) — flipped the stale heat-3 ground-truth canary (+ fixed an exposed py3.11 harness break) + added the `needs_human` coherence gate (`--couple`/`--keep-value2`, value2-only). Green py3.11+3.14; merged `origin/main` (project-prime `be656a4`). Parser-scope follow-up banked in [[Gap_Gate_Coverage]].
- **Graphify_ReferenceCorpus** (2026-06-27) — graphify **TRIALED** as a navigable-Amber-manual backend for the future proposer → **REJECTED**: software-centric ontology has zero parameter-level concepts (dt/ntt/igb/mbondi absent) → baseline lookup wins; pairwise edges ~60% hallucinated / ~20% fabricated. Confirms precise-lookup > concept-graph, with evidence. [[Research_graphify]] (trial-rejected); memory `graphify-assessment`.
- **CodeReview_Parallel_Sessions** (2026-06-27) — independent 2nd-pass review of the 2026-06-27 gate code (project-prime `b375f39..fee1fbe`, 4 skills) → **PASS** (0 HIGH/MED, 14 LOW/INFO; project-prime UNCHANGED). LOW/INFO hardening banked → newly-Ready **GateHardening_Followups**.
