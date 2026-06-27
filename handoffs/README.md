# Handoffs & Future Work

Session-handoff prompts (`Next_Session_Prompt_*`) and future-work candidates
(`Future_Work_*`). Each is a **paste-ready starter for a fresh Claude Code
session** (recap + decisions-banked + a "prompt to paste" block). The `status:`
field in each file's frontmatter is the source of truth; this index is the
forward queue at a glance.

**Convention:** new session handoffs and future-work notes go in this folder.
Obsidian `[[wikilinks]]` resolve by filename, so links work regardless of folder.

## ▶ Ready — actionable next sessions
- [[Next_Session_Prompt_AMBER_Gate_Encoding]] — encode the 4 P1 AMBER failure-mode gates (template: the `SYSTEM_NOT_NEUTRAL` structural fix).
- [[Next_Session_Prompt_ntx_irest_CoherenceGate]] — encode the `ntx`↔`irest` restart-coherence gate (a real verifier hole: `irest=1, ntx=1` passes today). Opens by asking 4 scope questions; gate-only recommended. Replaced the `Gap_ntx_irest_restart_topology` note 2026-06-24.
- [[Next_Session_Prompt_mdin_edit_Whitelist]] — expand `mdin-edit`'s editable-parameter whitelist (Tier-1 scalars: `gamma_ln`/`taup`/`pres0`/`tempi`/`maxcyc`/`ncyc`).
- [[Next_Session_Prompt_mdin_edit_CoherenceFix]] — Phase 1: flip the one stale `oracle.py` ground-truth guard (heat-3 is now coherent `300/300`) + Option-A hermetic repair fixture + rewrite 3 docs. Phase 2: ADD the `needs_human` confirm gate for a pre-existing `temp0`/`&wt` mismatch (port from `amber-recover`). Diagnosis verified by running; `test_acceptance.sh` already green. 2026-06-26.
- [[Next_Session_Prompt_HermesAgent_Eval]] — evaluate the Hermes agent framework (research + verdict, not a migration).

## ◆ Candidate — opt-in, decision-gated
- [[Future_Work_Proposer_Agent]] — outer propose-then-verify supervisory agent (contains an oracle-first build plan; not started by design).
- [[Future_Work_Headroom_ContextCompression]] — route OpenClaw tool-output through Headroom (ContextEngine plugin) for token savings; assessed 2026-06-24, cache-busting risk verified fixed; scoped to observational content only; low urgency while on free Cerebras.
- [[Future_Work_Run_Confirmation_Gate]] — confirm-before-launch ("Proceed?") gate for agent/Discord-driven runs; decision banked 2026-06-26 — lives at the agent/conversation layer **or** a staged-spec `stage-run`/`confirm-run` handshake, **not** a blocking prompt inside the skill (would deadlock `exec`/detached pipeline/`md-planner`/the test harness). Approach pick pending.
- [[Next_Session_Prompt_Graphify_ReferenceCorpus]] — graphify knowledge-graph tool: assessed + shelved ([[Research_graphify]]), banks the Q1–Q4 evaluation questions to settle **before** any spike. Strongest real use = index the reference corpus (`Amber26.pdf` + mailing-list + 66-skill lib); gated on conceptual-navigation-vs-precise-lookup (lean: steer away from graphify for the gate backlog). Never writes into vault notes. Decision-gated, to be called when ready. 2026-06-26.
- [[Future_Work_mdin_edit_Arbitrary_Shapes]] — make `mdin-edit` edit ANY mdin set (stage-name-agnostic discovery + multi-card `TEMP0` handling), not just the advisor's — the "consume arbitrary inputs" half of build-and-use. Do **after** [[Next_Session_Prompt_mdin_edit_CoherenceFix]]. 2026-06-26.
- [[Next_Session_Prompt_RunOutput_Convention]] — durable prevention for run-output git-noise: route all runs under the already-ignored `runs/` (vs today's ad-hoc top-level dirs). Touches `run_happy_path.sh` (no OUTDIR default) + async pipeline + test wire-ins → needs a verifying re-run. Symptom tidy already landed (project-prime `b375f39`, `git status` 384→0). 2026-06-26.

## ✔ Consumed — kept for the Outcome record + cross-links
- [[Next_Session_Prompt_AMBER_FailureMode_Sweep]] — the failure-mode sweep (done 2026-06-19 → produced [[Research_AMBER_Failure_Modes]] + the gate-encoding handoff).

## Bigger open direction (not a paste-ready prompt)
- [[Gap_Remote_HPC_Backend]] — production remote HPC backend (lives at vault root as a `Gap_` note; the largest forward item, externally blocked).
