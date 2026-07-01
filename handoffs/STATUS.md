---
tags: [project-prime, handoffs, status, priority, index]
type: status
status: active
updated: 2026-06-30
---

# Forward queue — status & priority dashboard

> At-a-glance view of every open handoff / future-work / gap, so we always know **what's next**. The per-file `status:` frontmatter is the **source of truth**; `README.md` has the richer per-item annotations; this is the compact dashboard. Snapshot **2026-06-30** (project-prime `fc14443`, vault + code both clean + pushed). **GateHardening_Followups consumed 2026-06-30 → the gate-durability pass is done** (structural fail-CLOSED CROSS_GAP parmed-validated · `needs_human` mutation coverage · cpptraj real-format fixture · doc fixes); its handoff file was **removed from this folder**, Outcome retained in Consumed below. Earlier: **GB_Radii_Fix consumed 2026-06-29 → the P1 gate batch fully closed (4/4)**; the 3 concurrent 2026-06-27 sessions (Hermes-eval · AMBER-gate-encoding · mdin-coherence-fix) + the graphify trial + the parallel-session code review all **merged + consumed** (their handoff files removed 2026-06-27). Outcome records for all consumed items live in the Consumed section below + memory + `Dev_Log.md`.

## ⭐ Priority queue (set the order here)

*Suggested seed below — tell me your order and I'll lock it in. Dependencies noted; you can't sanely put #6 before #1, etc.*

| Order | Item | Why here |
|---|---|---|
| ✓ | ~~**GateHardening_Followups**~~ | **CONSUMED 2026-06-30** — the durability pass; all 6 nits done (project-prime `fc14443`). File removed. |
| ✓ | ~~**GB_Radii_Fix**~~ | **CONSUMED 2026-06-29** — mbondi2 retype + ΔG re-baseline (1L2Y −17.78 / 3HTB −25.85) + detector→fatal all landed (project-prime `61f6a2f`). P1 batch fully closed. |
| 2 | **RunOutput_Convention** | Cheap hygiene — stops recurring git-noise; needs one verifying re-run. |
| 3 | **mdin_edit_Whitelist** | Incremental capability (more editable params). |
| — | *candidates (4–8)* | Decision-gated — promote when you decide to start one (see below). |

*(Consumed 2026-06-30: **GateHardening_Followups**. Consumed 2026-06-29: **GB_Radii_Fix**. Consumed 2026-06-27: ntx_irest_CoherenceGate, HermesAgent_Eval, AMBER_Gate_Encoding, mdin_edit_CoherenceFix, Graphify_ReferenceCorpus, CodeReview_Parallel_Sessions. → see Consumed below.)*

## 🟢 Ready — paste-and-go

| Handoff | What | Status |
|---|---|---|
| **mdin_edit_Whitelist** | Expand mdin-edit's editable-parameter set | `ready` |

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
- **GB_Radii_Fix** (consumed 2026-06-29) completed the P1 batch — all 4 P1 gates now fatal/encoded; remaining gate work is the P2/P3 backlog in [[Gap_Gate_Coverage]].
- **Gap_Remote_HPC** is externally blocked — priority can't make it happen.

## 🔀 Concurrency — parallel-safe map (RETIRED 2026-06-27)

✅ The three concurrent 2026-06-27 sessions (Hermes-eval · AMBER-gate-encoding · mdin-coherence-fix) all **merged to `main` + cleaned up** (worktrees removed, branches deleted in both repos). The live collision map is retired. The reusable principle for the next parallel burst: sessions clash if they share **files** (stage explicit paths; isolate worktrees), **runtime** (one OpenClaw gateway / one toolchain runner), or **vault/memory** (Dev_Log/MAP/Gap are git-mergeable — stack newest-first; `MEMORY.md`/`project_prime_status.md` are outside git → serialize, re-read before edit).

## ✔ Consumed (done, for the record — a handoff's file is removed from this folder when it is consumed; the record below + memory + `Dev_Log.md` are canonical)

- **GateHardening_Followups** (2026-06-30) — the LOW/INFO durability / test-quality / doc nits from the 2026-06-27 review, all 6 done (project-prime `61f6a2f → fc14443`, 4 commits, each RED→GREEN + independently reviewed + pushed). **CROSS_GAP made fail-CLOSED** — a structural bond-length detector (`prmtop_bonds`+`read_amber_coords`+`structural_long_bonds`) from comp_dry `BONDS`+`.crd` as the primary signal, log-scrape backstop, `\b` anchor — **parmed-validated bond-for-bond** (311 bonds, real 1L2Y) + no false-fire on the real build; a 3-agent review hardened its parse paths (mandatory-block→None, crd-NATOM cross-check, `%COMMENT` tolerance). **`needs_human` halt now has a mutation mutant** (`drop-needs-human-gate`, SURVIVE→KILLED 15/15). **`prmtop_radius_set` pinned to a committed real-format fixture**; mbondi3 `(Bondi2)` comment fixed; plip salt-bridge wording scoped; `mdin-params.md` corrected (empirically grounded — validator BROADER than the gate; `d`-exp `value2` *trips* the halt). Test hygiene: `sys.executable` + isolated scratch. Rigor findings: task 4's "zero regression" claim was already gone; the [[Gap_Gate_Coverage]] `d`-exponent note re-confirmed **accurate, not stale**. See [[Dev_Log]] 2026-06-30, [[Gap_Gate_Coverage]].
- **GB_Radii_Fix** (2026-06-29) — the last open P1 from the failure-mode sweep. **Route A (parmed):** `a_mmgbsa` retypes the dry MM-GBSA tops mbondi→mbondi2 via `parmed changeRadii` before MM-GBSA; detector **flipped FATAL** via `suite_ok` (closes the `ok=core_ok`/MM-GBSA-not-core trap). ΔG re-baselined (user-signed-off): **1L2Y −17.78** (was −18.16) · **3HTB −25.85** (was −27.41). Oracle 73/0 + acceptance Cases 1 & 4 + two adversarial reviews (SOUND-WITH-FIXES; ParmEd-source-confirmed descriptor rewrite). project-prime `61f6a2f` (pushed). **P1 batch now 4/4 fully closed.** [[Gap_Gate_Coverage]].
- **ntx_irest_CoherenceGate** (2026-06-27) — `ntx`↔`irest` restart-coherence gate **ENCODED** (project-prime `5d500b0`; `check_amber.py` + 3 vendored copies; FATAL `irest/ntx incoherent`, real-pmemd-ground-truthed — pmemd aborts `"ntx and irest are inconsistent!"`). Review found+fixed a HIGH `parse_namelists` comment-truncation bug (gate hardened locally; shared-parser fix deferred). #2 editor-toggle / #3 advisory stay deferred. [[Gap_Gate_Coverage]].
- **AMBER_FailureMode_Sweep** — produced `Research_AMBER_Failure_Modes` + `Gap_Gate_Coverage` (the gate backlog above).
- **HermesAgent_Eval** (2026-06-27) — evaluated → **declined** (research only, no migration). Produced [[Research_Hermes_Agent]]; engine room stays frozen; the one thesis-compatible coupling (a gated recovery *proposer*) folds into **Proposer_Agent** + `Gap_Gate_Coverage`.
- **AMBER_Gate_Encoding** (2026-06-27) — all **4 P1 gates encoded** (project-prime `f188b79`/`7582194`, merged `origin/main`): `SOLVENT_NOT_ADDED` + `CROSS_GAP_SPURIOUS_BOND` (tleap-build, FATAL) + PLIP `--nohydro` guard + non-fatal `GB_RADII_IGB_MISMATCH` detector. The detector's actual fix → **GB_Radii_Fix** (consumed 2026-06-29).
- **mdin_edit_CoherenceFix** (2026-06-27) — flipped the stale heat-3 ground-truth canary (+ fixed an exposed py3.11 harness break) + added the `needs_human` coherence gate (`--couple`/`--keep-value2`, value2-only). Green py3.11+3.14; merged `origin/main` (project-prime `be656a4`). Parser-scope follow-up banked in [[Gap_Gate_Coverage]].
- **Graphify_ReferenceCorpus** (2026-06-27) — graphify **TRIALED** as a navigable-Amber-manual backend for the future proposer → **REJECTED**: software-centric ontology has zero parameter-level concepts (dt/ntt/igb/mbondi absent) → baseline lookup wins; pairwise edges ~60% hallucinated / ~20% fabricated. Confirms precise-lookup > concept-graph, with evidence. [[Research_graphify]] (trial-rejected); memory `graphify-assessment`.
- **CodeReview_Parallel_Sessions** (2026-06-27) — independent 2nd-pass review of the 2026-06-27 gate code (project-prime `b375f39..fee1fbe`, 4 skills) → **PASS** (0 HIGH/MED, 14 LOW/INFO; project-prime UNCHANGED). LOW/INFO hardening banked → newly-Ready **GateHardening_Followups**.
