---
tags: [project-prime, handoffs, status, priority, index]
type: status
status: active
updated: 2026-06-27
---

# Forward queue — status & priority dashboard

> At-a-glance view of every open handoff / future-work / gap, so we always know **what's next**. The per-file `status:` frontmatter is the **source of truth**; `README.md` has the richer per-item annotations; this is the compact dashboard. Snapshot **2026-06-27** (vault `f85ba57`, project-prime `b375f39`, both clean + pushed).

## ⭐ Priority queue (set the order here)

*Suggested seed below — tell me your order and I'll lock it in. Dependencies noted; you can't sanely put #6 before #1, etc.*

| Order | Item | Why here |
|---|---|---|
| 1 | **mdin_edit_CoherenceFix** | Small, self-contained, unblocks the 1 broken test + adds `needs_human`; you're warm on it. |
| 2 | **AMBER_Gate_Encoding** | Highest-value remaining *hardening* — burns down `Gap_Gate_Coverage`. |
| 3 | **ntx_irest_CoherenceGate** | One gate in #2's family; could fold into #2. |
| 4 | **RunOutput_Convention** | Cheap hygiene — stops recurring git-noise; needs one verifying re-run. |
| 5 | **mdin_edit_Whitelist** | Incremental capability (more editable params). |
| 6 | **HermesAgent_Eval** | Pure research; do when you want a survey, not urgent. |
| — | *candidates (7–11)* | Decision-gated — promote when you decide to start one (see below). |

## 🟢 Ready — paste-and-go

| Handoff | What | Status |
|---|---|---|
| **mdin_edit_CoherenceFix** | Fix the 1 oracle drift-guard + add `needs_human` confirm | `ready` |
| **AMBER_Gate_Encoding** | Encode the 4 P1 failure-mode gates into the skills | `ready` |
| **ntx_irest_CoherenceGate** | Encode the `ntx`↔`irest` restart-coherence gate (real verifier hole) | `ready` |
| **mdin_edit_Whitelist** | Expand mdin-edit's editable-parameter set | `ready` |
| **HermesAgent_Eval** | Research + verdict on the Hermes agent framework (not a migration) | `ready` |

## 🟡 Candidate — needs a "go" / approach decision first

| Handoff | What | Status |
|---|---|---|
| **RunOutput_Convention** | Route all runs under the ignored `runs/` dir (kill git-noise at the source); symptom tidy already landed (`b375f39`) | `candidate` |
| **mdin_edit_Arbitrary_Shapes** | Make mdin-edit edit ANY mdin set (stage-name-agnostic + multi-card `TEMP0`) — do after CoherenceFix | `candidate` |
| **Run_Confirmation_Gate** | Confirm-before-launch; **approach picked 2026-06-27 = Level 2 + TTY**; low-urgency (advisor #4 shipped at edit level) | `candidate` |
| **Proposer_Agent** | Outer propose-then-verify agent around the frozen core (oracle-first plan); biggest agentic expansion | `candidate` |
| **Headroom_ContextCompression** | Compress tool-output for token savings; low urgency on free tier | `candidate` |
| **Graphify_ReferenceCorpus** | Shelved tool; possible = index `Amber26.pdf` + ref library; gated on Q1–Q4 first | `candidate-decision-gated` |

## 🔵 Big open directions (Gap notes — not paste-ready)

| Gap | What | Status |
|---|---|---|
| **Gap_Remote_HPC_Backend** | Production remote HPC backend (Scenario B). **Externally blocked** — needs Single Particle to provide it; can't be "next" by choice. | `open` |
| **Gap_Gate_Coverage** | Umbrella for the 15 candidate gates (P1=4/P2=7/P3=4); #2 & #3 above burn it down. | `partially-filled` |
| **Gap_MachineLearned_ForceFields** | Would ML force fields help; espaloma-parameterization the architecture-preserving experiment. | `open` |

## Dependencies / sequencing

- **CoherenceFix (#1) → Arbitrary_Shapes** (coherence fix before arbitrary shapes).
- **AMBER_Gate_Encoding & ntx_irest both draw from Gap_Gate_Coverage**; ntx_irest is one gate in that family — foldable into the gate-encoding session.
- **Gap_Remote_HPC** is externally blocked — priority can't make it happen.

## ✔ Consumed (done, for the record)

- **AMBER_FailureMode_Sweep** — produced `Research_AMBER_Failure_Modes` + `Gap_Gate_Coverage` (the gate backlog above).
