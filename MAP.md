---
tags: [project-prime, map, index, meta]
type: map
status: active
---

# MAP — high-level index

*At-a-glance project state: what's **done**, **in-flight**, and **blocked**. Refreshed weekly + on big shifts per [[Definition_of_Done]] §5. This is the index — the long-form live state is `project_prime_status.md` (auto-memory) and the time-ordered trail is [[Dev_Log]]. Pointers, not duplicates.*

**Last updated:** 2026-06-26

---

## ✅ Done

- **Local AMBER MD pipeline — COMPLETE (9 OpenClaw skills, Stages 2–8).** Antechamber ligand prep · tleap-build · pmemd MD · cpptraj-analysis · `plip-profile` (Stage 6) · `md-planner` (Stage 7, planning layer) · `amber-recover` (Stage 8, bounded recovery) · `mdin-edit` (NL parameter editor). Happy path GREEN on 1L2Y, 3HTB, 181L. See [[Phase3_Taskboard_Manifest]], [[Implementation_Summary_Report]].
- **Agentic drive proven** — `openclaw agent` NL drive byte-verified; Discord @-mention drives the full detached pipeline e2e with live notifications. Default model `google/gemini-3-flash-preview` (MD runs locally = $0).
- **mdin-edit advisor feedback** addressed + packaged ([[Research_Advisor_Feedback_mdin_edit]]).
- **Phase 1 market landscape** delivered (`Market_Landscape_Report.md` + Summary + `Actionable_Recommendations.md`).
- **Dev discipline** — Definition-of-Done + Stop-nudge drift backstop ([[Definition_of_Done]], 2026-06-26).

## 🔄 In-flight / forward queue

*Source of truth = `status:` in each `handoffs/` file; see `handoffs/README.md`.*

- **Gate encoding** — `ntx`↔`irest` restart-coherence gate ([[Next_Session_Prompt_ntx_irest_CoherenceGate]], ready) · 4 P1 AMBER failure-mode gates ([[Next_Session_Prompt_AMBER_Gate_Encoding]], ready) · `mdin-edit` whitelist expansion (ready). Backlog tracked in [[Gap_Gate_Coverage]] (partially-filled).
- **Hermes-Agent eval** — research + verdict, not migration ([[Next_Session_Prompt_HermesAgent_Eval]], ready).
- **Proposer agent** — outer propose-then-verify supervisory agent, oracle-first build plan ([[Future_Work_Proposer_Agent]], candidate-not-started).
- **Headroom context-compression** — route OpenClaw tool-output through Headroom; low urgency on free tier ([[Future_Work_Headroom_ContextCompression]], candidate).
- **graphify spikes** (2026-06-26) — vault structural-only god-node/orphan analysis + index `Amber26.pdf` into a queryable graph (banked, [[Research_graphify]]).

## ⛔ Blocked

- **[[Gap_Remote_HPC_Backend]]** (open) — whether a production remote HPC backend (Scenario B) ever becomes available. Externally blocked; needs confirmation from Single Particle. Local (Scenario A) is the confirmed current path.

## 🧩 Open gaps

- [[Gap_Remote_HPC_Backend]] — open · [[Gap_MachineLearned_ForceFields]] — open · [[Gap_Gate_Coverage]] — partially-filled.

## ⚠️ Open decisions

- **`phase3-explicit-solvent-md/heat-3.in`** was edited `value2 310→300`, erasing the deliberate `temp0≠value2` mismatch that `mdin-edit`'s oracle asserts must persist → its self-test/mutation go red at ground-truth load. Decide: revert the demo to 310, or update the oracle's expectation. See [[Dev_Log]] (2026-06-26) + [[Gap_Gate_Coverage]].
- **project-prime** `fix/audit-gates-and-tests-20260626` (6 verified bug-fixes, 3 commits) is **local-not-pushed** — review + push pending per [[Definition_of_Done]] §4.
