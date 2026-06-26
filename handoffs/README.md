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
- [[Next_Session_Prompt_HermesAgent_Eval]] — evaluate the Hermes agent framework (research + verdict, not a migration).

## ◆ Candidate — opt-in, decision-gated
- [[Future_Work_Proposer_Agent]] — outer propose-then-verify supervisory agent (contains an oracle-first build plan; not started by design).
- [[Future_Work_Headroom_ContextCompression]] — route OpenClaw tool-output through Headroom (ContextEngine plugin) for token savings; assessed 2026-06-24, cache-busting risk verified fixed; scoped to observational content only; low urgency while on free Cerebras.

## ✔ Consumed — kept for the Outcome record + cross-links
- [[Next_Session_Prompt_AMBER_FailureMode_Sweep]] — the failure-mode sweep (done 2026-06-19 → produced [[Research_AMBER_Failure_Modes]] + the gate-encoding handoff).

## Bigger open direction (not a paste-ready prompt)
- [[Gap_Remote_HPC_Backend]] — production remote HPC backend (lives at vault root as a `Gap_` note; the largest forward item, externally blocked).
