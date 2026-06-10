---
tags: [project-prime, openclaw, session-handoff, bounded-recovery, planner, roadmap]
type: handoff
status: ready
created: 2026-06-10
---

# Next Session Starter — post-Stage-6: pick the next frontier (bounded recovery / planner / HPC gate)

> Created 2026-06-10 at the end of the Stage-6 PLIP session. **Stage 6 (PLIP interaction profiling) is DONE** — the local AMBER MD pipeline now goes prep → topology → MD → analysis (MM-GBSA) → **interaction fingerprint**, runs any protein+ligand, is NL-drivable, and is wired end-to-end. The remaining roadmap items are the harder differentiators. **The first action next session is a DECISION** — which frontier to build — because they're scope-defining (per [[feedback-verify-and-eval]]). Paste the §The prompt to paste block into a fresh Claude Code session (run from the vault).

## Recap (what's done — don't re-discover)

- **Stage 6 DONE** — `project-prime/skills/plip-profile/` (deterministic wrapper): cpptraj extracts a representative dry complex frame (default `--frame medoid`, deterministic), Python normalizes AMBER variant resnames (the PLIP phantom-ligand footgun, proven load-bearing), PLIP runs, the XML is parsed into a structured 8-category interaction envelope. Engine oracle 55/55 (py3.9+3.11), acceptance 18/18, NL-driven byte-verified on live `google/gemini-3-flash-preview`, wired into `run_happy_path.sh` as a **non-fatal Stage 6 addendum** (fresh 1L2Y GREEN, ΔG −18.63, regression unperturbed). Adversarial review found + fixed a HIGH silent-pass (unmapped non-standard residue → phantom; now a loud `UNMAPPED_NONSTANDARD_RESIDUES` gate). Commit local-not-pushed. See [[Dev_Log]] 2026-06-10 + [[project-prime-status]].
- **The full local happy path + all six stages are GREEN and system-agnostic.** Skills: antechamber-ligandprep, tleap-build, amber-md-run, cpptraj-analysis, plip-profile (+ mdin-edit, pipeline-async). All deterministic wrappers; the LLM only picks the skill.
- **Config state:** paid Google key in; default model `google/gemini-3-flash-preview`; gateway on 127.0.0.1:18789; skills auto-loaded via `skills.load.extraDirs` watcher. `scripts/env.sh` bootstraps the toolchain for detached runs (gotchas: trips zsh `nomatch` interactively, and `set -u` via amber.sh's unguarded `DYLD_FALLBACK_LIBRARY_PATH` — wrap `set +u`/`set -u` or run under bash).

## The decision (first action — ONE AskUserQuestion gate)

Three candidate frontiers, all scoped in the vault. Recommend **bounded recovery** (roadmap-default; the strongest paper-cited element — NotebookLM confirmed the methane-oxidation case study). Present these for sign-off before building:

1. **Bounded error recovery (RECOMMENDED)** — `Workflow_Error_Recovery_Loop` + `Skill_Bounded_Recovery_AMBER`. A deterministic, mathematically-bounded recovery loop for MD runtime failures (crash → tiered response: checkpoint-restore first, then bounded param mutation only on re-crash — e.g. lower `dt`, disable SHAKE, resume — never let the LLM invent physics). The strict-verifier Predict→Test→Falsify→Improve pattern from `Arch_Recursion_LOWE`. This is the "AI changing physics safely" differentiator and answers the incumbents' autonomy critique (`Design_Determinism_Spectrum`). Needs: a way to *induce* real MD failures (bad dt / SHAKE-off / blown-up coords) to test against.
2. **Planner / Taskboard-Manifest layer** — `Arch_Taskboard_Manifest`. Translate a scientific goal into an explicit validated stage/input/output/validation spec *before* execution (the plan-and-execute pattern; `llm-task` with JSON-Schema validation is the natural tool — see [[openclaw-canonical-paths]] §10). Lazy-loaded, stage-validated. The "reason about the workflow before running it" layer.
3. **`Gap_Remote_HPC_Backend`** — the production-scale decision (local is CPU-only; no `pmemd.cuda`). This is a CALL TO SETTLE WITH THE ADVISOR (Scenario A local vs B remote dispatch via DPDispatcher/SSHContext), not a local build. Surface it; don't build speculatively.

## Decisions banked — do NOT re-litigate

- **Stage 6 is settled.** Don't rebuild plip-profile; it's green + reviewed + wired. v2 items (per-frame interaction occupancy/time-series; functional-metal systems; pocket-centred medoid) are noted, not started — confirm before building any.
- **Deterministic-wrapper discipline holds** (CLAUDE.md SOPs): any new skill is a deterministic wrapper (`--dry-run` + JSON envelope + `test_acceptance.sh` golden/unrelated/malformed), the LLM only picks the skill. Match the existing skills' shape.
- **Verify-and-eval is the working practice** ([[feedback-verify-and-eval]] / `Eval_Criteria.md`): pre-run decision gate → deterministic gates → adversarial second-AI review per deliverable. It has now caught a real HIGH-severity bug two sessions running (the arbitrary-target F1 and the Stage-6 silent-pass) — keep using it.
- **Max 3 named agents** ([[multi-agent-scope]]) — recovery/planner are *skills* (+ at most a named recovery/planner agent), not a swarm.
- **Single-trajectory numbers are sanity numbers** — ΔG and the interaction profile are demonstrations, not precise affinities/occupancies.

## The prompt to paste

```
Continuation of the Single Particle / OpenClaw + AMBER project. Stage 6 (PLIP interaction profiling) is DONE — the full local pipeline (prep → topology → MD → MM-GBSA → interaction fingerprint) is green, system-agnostic, NL-drivable, wired end-to-end. project-prime HEAD is the Stage-6 commit (master, local, not pushed). Default model paid google/gemini-3-flash-preview.

Read BEFORE acting (in order):
- memory project-prime-status (CRITICAL — current state; Stage 6 done; the six green skills)
- memory feedback-verify-and-eval + vault Eval_Criteria.md (THE working practice: pre-run decision gate → deterministic gates → adversarial second-AI review; it caught a real HIGH bug each of the last two sessions)
- memory openclaw-canonical-paths (exec not bash; --gateway; SKILL.md single-line JSON metadata; llm-task for schema-validated planner output; deterministic-wrapper discipline; env.sh gotchas — zsh nomatch + set -u/amber.sh)
- memory antechamber-aromatic-kekulize-bug + amber-md-prior-art (the silent-error culture; our differentiators)
- vault Dev_Log.md (2026-06-10 + 2026-06-09 entries) ; vault Skill_Bounded_Recovery_AMBER, Workflow_Error_Recovery_Loop, Arch_Taskboard_Manifest, Arch_Recursion_LOWE, Design_Determinism_Spectrum, Gap_Remote_HPC_Backend

FIRST ACTION — a DECISION GATE (one AskUserQuestion): which frontier to build next?
(1) Bounded error recovery [RECOMMENDED] — Workflow_Error_Recovery_Loop + Skill_Bounded_Recovery_AMBER: a deterministic tiered recovery loop for MD runtime failures (checkpoint-restore first, bounded param mutation only on re-crash; never let the LLM invent physics). Strongest paper-cited element.
(2) Planner / Taskboard-Manifest — Arch_Taskboard_Manifest: goal → validated stage/input/output spec before execution; llm-task + JSON-Schema is the natural fit.
(3) Gap_Remote_HPC_Backend — a call to settle Scenario A (local) vs B (remote DPDispatcher dispatch) with the advisor; not a local build.

Then build per the chosen frontier as a deterministic-wrapper skill: scaffold via /skill-scaffold, --dry-run + JSON envelope, test_acceptance.sh (golden + unrelated + malformed→ok:false), an independent oracle for any pure logic, deterministic gates, THEN an adversarial second-AI review told to find faults vs Eval_Criteria.md. If bounded recovery: you'll need a way to INDUCE real MD failures (bad dt, SHAKE off, blown-up coordinates) to test the loop against real crashes, not mocks.

Banked, do NOT re-litigate: Stage 6 is done (don't rebuild plip-profile); deterministic-wrapper discipline; max 3 named agents (recovery/planner are skills); single-trajectory numbers are sanity numbers. Run AMBER/PLIP/cpptraj work under `bash -c 'set +u; source scripts/env.sh >/dev/null 2>&1; set -u; …'` (env.sh trips zsh nomatch + set -u via amber.sh). Foreground Claude Bash is sandboxed (126 on conda binaries) — background or disable-sandbox for conda work.

Scope-fence: build ONLY the chosen frontier. Do NOT start the others without confirming.
```

## After the session — update this file

1. Flip frontmatter `status: ready` → `status: consumed`.
2. Add an `## Outcome` footer: consumed YYYY-MM-DD, 1-sentence outcome, link to the [[Dev_Log]] entry.

## Cross-links

- [[Dev_Log]] 2026-06-10 — "Stage 6 DONE: PLIP interaction profiling" — the session that produced this handoff.
- `Next_Session_Prompt_Stage6_PLIP.md` (consumed) — the prior handoff.
- memories: [[project-prime-status]], [[feedback-verify-and-eval]], [[openclaw-canonical-paths]], [[amber-md-prior-art]], [[multi-agent-scope]].
