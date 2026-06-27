# Handoffs & Future Work

Session-handoff prompts (`Next_Session_Prompt_*`) and future-work candidates
(`Future_Work_*`). Each is a **paste-ready starter for a fresh Claude Code
session** (recap + decisions-banked + a "prompt to paste" block). The `status:`
field in each file's frontmatter is the source of truth; this index is the
forward queue at a glance.

**Convention:** new session handoffs and future-work notes go in this folder.
Obsidian `[[wikilinks]]` resolve by filename, so links work regardless of folder.

**▶ Priority dashboard:** [[STATUS]] — the at-a-glance priority queue + dependencies (set the order there). This README is the richer per-item annotation; `STATUS.md` is the compact "what's next" view.

## ▶ Ready — actionable next sessions
- [[Next_Session_Prompt_ntx_irest_CoherenceGate]] — encode the `ntx`↔`irest` restart-coherence gate (a real verifier hole: `irest=1, ntx=1` passes today). Opens by asking 4 scope questions; gate-only recommended. Replaced the `Gap_ntx_irest_restart_topology` note 2026-06-24.
- [[Next_Session_Prompt_GB_Radii_Fix]] — apply the GB-radii (`mbondi2`) fix + re-baseline ΔG, then flip the `GB_RADII_IGB_MISMATCH` detector fatal. Small, well-scoped follow-up spun out of the AMBER P1 gate-encoding session. 2026-06-27.
- [[Next_Session_Prompt_mdin_edit_Whitelist]] — expand `mdin-edit`'s editable-parameter whitelist (Tier-1 scalars: `gamma_ln`/`taup`/`pres0`/`tempi`/`maxcyc`/`ncyc`).
- [[Next_Session_Prompt_GateHardening_Followups]] — **non-blocking** durability / test-quality / doc-accuracy nits from the 2026-06-27 code review (PASS, no blockers). 6 small test-first tasks across the 4 gate skills: add a `needs_human` mutation mutant, harden CROSS_GAP (structural-or-canary + `\b`), commit a real-format prmtop fixture + fix an mbondi3 comment, re-scope the plip "zero-regression" claim, correct mdin-params.md parser-scope wording, pin the test interpreter. Tasks 1–3 carry the real value. 2026-06-27.

## ◆ Candidate — opt-in, decision-gated
- [[Future_Work_Proposer_Agent]] — outer propose-then-verify supervisory agent (contains an oracle-first build plan; not started by design).
- [[Future_Work_Headroom_ContextCompression]] — route OpenClaw tool-output through Headroom (ContextEngine plugin) for token savings; assessed 2026-06-24, cache-busting risk verified fixed; scoped to observational content only; low urgency while on free Cerebras.
- [[Future_Work_Run_Confirmation_Gate]] — confirm-before-launch ("Proceed?") gate for agent/Discord-driven runs. **Approach picked 2026-06-27: Level 2 (`stage-run`/`confirm-run`) + a TTY-guarded `--confirm`**; NOT a blocking prompt in the skill (deadlocks `exec`/detached/`md-planner`/harness), NOT Level 3 (raw-shell `exec` makes ironclad-over-the-agent moot). Low-urgency — advisor #4 is already shipped at the *edit* level; this is the *launch*-level generalization.
- [[Future_Work_mdin_edit_Arbitrary_Shapes]] — make `mdin-edit` edit ANY mdin set (stage-name-agnostic discovery + multi-card `TEMP0` handling), not just the advisor's — the "consume arbitrary inputs" half of build-and-use. Do **after** [[Next_Session_Prompt_mdin_edit_CoherenceFix]]. 2026-06-26.
- [[Next_Session_Prompt_RunOutput_Convention]] — durable prevention for run-output git-noise: route all runs under the already-ignored `runs/` (vs today's ad-hoc top-level dirs). Touches `run_happy_path.sh` (no OUTDIR default) + async pipeline + test wire-ins → needs a verifying re-run. Symptom tidy already landed (project-prime `b375f39`, `git status` 384→0). 2026-06-26.

## ✔ Consumed — Outcome record (handoff files removed 2026-06-27; full record lives in memory + `Dev_Log.md` + the linked Research/Gap notes)
- **AMBER_FailureMode_Sweep** — the failure-mode sweep (done 2026-06-19 → produced [[Research_AMBER_Failure_Modes]] + the gate-encoding handoff).
- **HermesAgent_Eval** — Hermes Agent evaluated 2026-06-27 → **declined** (research only, no migration). Produced [[Research_Hermes_Agent]]; engine room stays frozen. The thesis-compatible coupling (a gated recovery *proposer*) folds into [[Future_Work_Proposer_Agent]] + [[Gap_Gate_Coverage]].
- **AMBER_Gate_Encoding** — 4 P1 gates encoded 2026-06-27 (merged project-prime `origin/main`): `SOLVENT_NOT_ADDED` + `CROSS_GAP_SPURIOUS_BOND` + PLIP `--nohydro` + non-fatal `GB_RADII_IGB_MISMATCH`. Detector's actual fix spun out → [[Next_Session_Prompt_GB_Radii_Fix]] (Ready).
- **mdin_edit_CoherenceFix** — done 2026-06-27 (merged project-prime `origin/main`): flipped the stale heat-3 canary + py3.11 harness fix + `needs_human` coherence gate (`--couple`/`--keep-value2`). Parser-scope follow-up in [[Gap_Gate_Coverage]].
- **Graphify_ReferenceCorpus** — graphify **TRIALED** 2026-06-27 as a proposer-manual backend → **REJECTED** (concept-graph has no parameter-level concepts; pairwise edges ~60% hallucinated). Precise-lookup > concept-graph, with evidence. [[Research_graphify]].
- **CodeReview_Parallel_Sessions** — independent 2nd-pass review of the 2026-06-27 gate code (project-prime `b375f39..fee1fbe`, 4 skills) → **PASS** 2026-06-27 (empirical pass + 24-agent adversarial workflow converged; 0 HIGH/MED, 14 LOW/INFO, project-prime UNCHANGED). LOW/INFO hardening banked → [[Next_Session_Prompt_GateHardening_Followups]] (Ready).

## Bigger open direction (not a paste-ready prompt)
- [[Gap_Remote_HPC_Backend]] — production remote HPC backend (lives at vault root as a `Gap_` note; the largest forward item, externally blocked).
