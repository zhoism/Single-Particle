---
tags: [project-prime, map, index, meta]
type: map
status: active
---

# MAP — high-level index

*At-a-glance project state: what's **done**, **in-flight**, and **blocked**. Refreshed weekly + on big shifts per [[Definition_of_Done]] §5. This is the index — the long-form live state is `project_prime_status.md` (auto-memory) and the time-ordered trail is [[Dev_Log]]. Pointers, not duplicates.*

**Last updated:** 2026-06-27

---

## ✅ Done

- **Local AMBER MD pipeline — COMPLETE (9 OpenClaw skills, Stages 2–8).** Antechamber ligand prep · tleap-build · pmemd MD · cpptraj-analysis · `plip-profile` (Stage 6) · `md-planner` (Stage 7, planning layer) · `amber-recover` (Stage 8, bounded recovery) · `mdin-edit` (NL parameter editor). Happy path GREEN on 1L2Y, 3HTB, 181L. See [[Phase3_Taskboard_Manifest]], [[Implementation_Summary_Report]].
- **Agentic drive proven** — `openclaw agent` NL drive byte-verified; Discord @-mention drives the full detached pipeline e2e with live notifications. Default model `google/gemini-3-flash-preview` (MD runs locally = $0).
- **mdin-edit advisor feedback** addressed + packaged ([[Research_Advisor_Feedback_mdin_edit]]).
- **Phase 1 market landscape** delivered (`Market_Landscape_Report.md` + Summary + `Actionable_Recommendations.md`).
- **Dev discipline** — Definition-of-Done + Stop-nudge drift backstop ([[Definition_of_Done]], 2026-06-26).
- **Code audit hardening (project-prime)** — 6 verified bug-fixes + ~1800 lines of oracle/gate tests, verified 210 assertions green + merged to `origin/main` (`fb6c1a9`, 2026-06-26).
- **Hermes Agent evaluated → DECLINED** (2026-06-27) — Nous Research's self-evolution-headline "OpenClaw alternative"; research only, no migration. Primary-source crux: the self-improvement loop edits `SKILL.md` definitions, not code; default execution is LLM-mediated. Engine room stays frozen; the one thesis-compatible coupling (a gated recovery *proposer*) folds into the Proposer agent. Sharpened [[Design_Determinism_Spectrum]] into a self-mutation / execution-mediation pair. [[Research_Hermes_Agent]].

## 🔄 In-flight / forward queue

*Source of truth = `status:` in each `handoffs/` file; see `handoffs/README.md`.*

- **Gate encoding** — the **4 P1 AMBER gates landed 2026-06-27** + the **GB-radii `mbondi2` fix + detector→FATAL landed 2026-06-29** ([[Next_Session_Prompt_GB_Radii_Fix]] consumed; project-prime `61f6a2f`; ΔG re-baselined 1L2Y −17.78 / 3HTB −25.85) → the **P1 batch is fully closed (4/4)**. The `ntx`↔`irest` restart-coherence gate also landed ([[Next_Session_Prompt_ntx_irest_CoherenceGate]] consumed 2026-06-27). Remaining: `mdin-edit` whitelist (ready) + the P2/P3 backlog in [[Gap_Gate_Coverage]] (partially-filled).
- **Proposer agent** — outer propose-then-verify supervisory agent, oracle-first build plan ([[Future_Work_Proposer_Agent]], candidate-not-started).
- **Headroom context-compression** — route OpenClaw tool-output through Headroom; low urgency on free tier ([[Future_Work_Headroom_ContextCompression]], candidate).
- **Run-confirmation gate** — confirm-before-launch for agent/Discord runs; decision banked (agent-layer or staged-spec `stage-run`/`confirm-run` handshake, not an in-skill blocking prompt), approach pick pending ([[Future_Work_Run_Confirmation_Gate]], candidate). 2026-06-26.

## ⛔ Blocked

- **[[Gap_Remote_HPC_Backend]]** (open) — whether a production remote HPC backend (Scenario B) ever becomes available. Externally blocked; needs confirmation from Single Particle. Local (Scenario A) is the confirmed current path.

## 🧩 Open gaps

- [[Gap_Remote_HPC_Backend]] — open · [[Gap_MachineLearned_ForceFields]] — open · [[Gap_Gate_Coverage]] — partially-filled.

## ✅ Recently resolved (2026-06-26 – 27)

- **AMBER P1 failure-mode gates — all 4 ENCODED** 2026-06-27 (project-prime `f188b79`/`7582194`, merged `origin/main`): `SOLVENT_NOT_ADDED` + `CROSS_GAP_SPURIOUS_BOND` (tleap-build, FATAL) + PLIP `--nohydro` guard + non-fatal `GB_RADII_IGB_MISMATCH` detector. [[Next_Session_Prompt_AMBER_Gate_Encoding]] consumed; the detector's actual fix → [[Next_Session_Prompt_GB_Radii_Fix]] **consumed 2026-06-29** (parmed mbondi2 retype + flipped FATAL; ΔG re-baselined 1L2Y −17.78 / 3HTB −25.85). [[Gap_Gate_Coverage]] P1 row fully burned down (4/4).
- **mdin-edit coherence fix + `needs_human` gate** — DONE 2026-06-27. Suite was RED (a stale heat-3 ground-truth canary asserting the *old* mismatch); flipped it + fixed an exposed py3.11 harness break + corrected the 310-typo docs (project-prime `174ca3f`), then added the `needs_human` coherence gate + `--couple`/`--keep-value2` (`be656a4`, value2-only). Green py3.11+3.14 (full fuzz 245522/0, acceptance, mutation 14/14); 3-agent adversarial review passed. [[Next_Session_Prompt_mdin_edit_CoherenceFix]] consumed; parser-scope follow-ups in [[Gap_Gate_Coverage]].
- **`heat-3.in` temp0/&wt mismatch** — RESOLVED. The coherent `300/300` is correct; the advisor's original `value2=310` was a **mistake**, not a deliberate fixture (user's call). Knock-on `mdin-edit` test update **DONE** 2026-06-27 (above).
- **project-prime audit branch** — DONE. `fix/audit-gates-and-tests-20260626` verified (210 assertions) + merged to `origin/main` (`fb6c1a9`) + pushed. The local branch is now an ancestor of `origin/main` — safe to delete (`git branch -d`).
- **graphify** — **TRIALED → REJECTED** 2026-06-27 (tested as a navigable-Amber-manual backend for the future proposer): no parameter-level concepts (dt/ntt/igb/mbondi absent) + ~60% hallucinated edges → precise-lookup beats concept-graph, with evidence. [[Next_Session_Prompt_Graphify_ReferenceCorpus]] resolved-rejected; [[Research_graphify]]; memory `graphify-assessment`.
