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
- **Code audit hardening (project-prime)** — 6 verified bug-fixes + ~1800 lines of oracle/gate tests, verified 210 assertions green + merged to `origin/main` (`fb6c1a9`, 2026-06-26).

## 🔄 In-flight / forward queue

*Source of truth = `status:` in each `handoffs/` file; see `handoffs/README.md`.*

- **Gate encoding** — `ntx`↔`irest` restart-coherence gate ([[Next_Session_Prompt_ntx_irest_CoherenceGate]], ready) · 4 P1 AMBER failure-mode gates ([[Next_Session_Prompt_AMBER_Gate_Encoding]], ready) · `mdin-edit` whitelist expansion (ready). Backlog tracked in [[Gap_Gate_Coverage]] (partially-filled).
- **Hermes-Agent eval** — research + verdict, not migration ([[Next_Session_Prompt_HermesAgent_Eval]], ready).
- **Proposer agent** — outer propose-then-verify supervisory agent, oracle-first build plan ([[Future_Work_Proposer_Agent]], candidate-not-started).
- **Headroom context-compression** — route OpenClaw tool-output through Headroom; low urgency on free tier ([[Future_Work_Headroom_ContextCompression]], candidate).
- **Run-confirmation gate** — confirm-before-launch for agent/Discord runs; decision banked (agent-layer or staged-spec `stage-run`/`confirm-run` handshake, not an in-skill blocking prompt), approach pick pending ([[Future_Work_Run_Confirmation_Gate]], candidate). 2026-06-26.
- **graphify** (2026-06-26) — assessed + **shelved, to be called when ready**; not adopted as a dependency. Strongest real use = index the reference corpus (`Amber26.pdf` + mailing-list + 66-skill lib), decision-gated on conceptual-navigation-vs-precise-lookup. Open questions + threads banked in [[Next_Session_Prompt_Graphify_ReferenceCorpus]] ([[Research_graphify]]).
## ⛔ Blocked

- **[[Gap_Remote_HPC_Backend]]** (open) — whether a production remote HPC backend (Scenario B) ever becomes available. Externally blocked; needs confirmation from Single Particle. Local (Scenario A) is the confirmed current path.

## 🧩 Open gaps

- [[Gap_Remote_HPC_Backend]] — open · [[Gap_MachineLearned_ForceFields]] — open · [[Gap_Gate_Coverage]] — partially-filled.

## ✅ Recently resolved (2026-06-26 – 27)

- **mdin-edit coherence fix + `needs_human` gate** — DONE 2026-06-27. Suite was RED (a stale heat-3 ground-truth canary asserting the *old* mismatch); flipped it + fixed an exposed py3.11 harness break + corrected the 310-typo docs (project-prime `174ca3f`), then added the `needs_human` coherence gate + `--couple`/`--keep-value2` (`be656a4`, value2-only). Green py3.11+3.14 (full fuzz 245522/0, acceptance, mutation 14/14); 3-agent adversarial review passed. [[Next_Session_Prompt_mdin_edit_CoherenceFix]] consumed; parser-scope follow-ups in [[Gap_Gate_Coverage]].
- **`heat-3.in` temp0/&wt mismatch** — RESOLVED. The coherent `300/300` is correct; the advisor's original `value2=310` was a **mistake**, not a deliberate fixture (user's call). Knock-on `mdin-edit` test update **DONE** 2026-06-27 (above).
- **project-prime audit branch** — DONE. `fix/audit-gates-and-tests-20260626` verified (210 assertions) + merged to `origin/main` (`fb6c1a9`) + pushed. The local branch is now an ancestor of `origin/main` — safe to delete (`git branch -d`).
