---
tags: [project-prime, openclaw, session-handoff, day-6, evaluation, discord]
type: handoff
status: ready
created: 2026-06-05
---

# Next Session Starter — OpenClaw Day 6 / Evaluation + Discord

> Created 2026-06-05 at end of Day 5. Day 5 built Stages 3–5 (`tleap-build`, `amber-md-run`, `cpptraj-analysis`) and the full local AMBER MD happy path ran GREEN end-to-end on 1L2Y (12/12 analyses, 15 PNGs, MM-GBSA ΔG = −13.29 kcal/mol). **Day 6 is an EVALUATION session, not a build session** — the user manually runs/inspects the pipeline, then we attempt to drive the four skills through the OpenClaw Discord bot. Paste the §The prompt to paste fenced block into a fresh Claude Code session (run from the vault).

## Day 5 recap (what's done — don't re-discover)

- **Stages 3–5 BUILT + committed.** `project-prime/skills/{tleap-build,amber-md-run,cpptraj-analysis}/` (4 files each: SKILL.md single-line-JSON metadata, scripts/wrapper.py with `--dry-run`+JSON envelope, references/heuristics.md, test_acceptance.sh). Committed in `project-prime/` as **`2e9d8a4`** (also tracked the previously-uncommitted .gitignore/CLAUDE.md/pyproject.toml/env.lock.yml + golden-path 1L2Y fixture).
- **Happy path GREEN.** `project-prime/run_happy_path.sh [sim_ps]` chains antechamber→tleap→MD→analysis. 100 ps run: 4 ok:true envelopes, 12/12 analyses, 15 PNGs, ΔG −13.29 kcal/mol, 626 s production. Output (gitignored) at `project-prime/happy-path-run/`.
- **Each skill's `test_acceptance.sh` passes** (golden + unrelated/subset + malformed).
- **Vault updated.** [[Phase3_Taskboard_Manifest]] Stages 3–5 → BUILT; new [[Skill_Tleap_Build]] / [[Skill_AMBER_MD_Run]] / [[Skill_CPPTraj_Analysis]]; [[Dev_Log]] 2026-06-05 entry; [[Research_amber_md_skill]] (prior-art + steal-list). Vault committed on `main`.
- **Toolchain that must still hold:** full AmberTools 24.8 in conda env `prime-amber`; `pmemd`/`pmemd.MPI` in `~/Downloads/pmemd26/bin`. Engine default = serial `pmemd` (~15.6 ns/day on this Mac).

## Decisions banked — do NOT re-litigate

- **This is the COMMODITY baseline, deliberately.** It replicates baifan-wang's amber-md happy path on our deterministic-wrapper architecture. The differentiators (PLIP, planner, bounded recovery, remote HPC) are intentionally NOT built. See [[amber-md-prior-art]] memory — don't re-debate "did someone already build this."
- **Wrapper does the work; SKILL.md describes the goal; single exec call per turn.** Latency + reliability + determinism. See [[openclaw-canonical-paths]].
- **Path-with-space rule.** The project path has a space (`Single Particle`); tleap/cpptraj/MMPBSA tokenize input lines on whitespace → wrappers copy inputs in under bare names + reference relatively. Do NOT "simplify" this away.
- **Correctness rules baked into the wrappers** (don't reintroduce upstream bugs): comp_dry saved BEFORE solvateoct; protein PDB H stripped via `pdb4amber --nohyd`; PCA = two cpptraj calls; cluster `repout` in one command; strip uses the SOLVATED topology.
- **Memory-tool + LLM-Wiki ideas are DEFERRED.** [[memory-system-options]] (memsearch/mempalace) and [[llm-wiki-pattern]] — don't spin anything up; they're post-happy-path and the vault already IS the wiki.

## What's NOT done (deferred, non-blocking)

- **Live OpenClaw agent-turn verification.** Everything was verified via `run_happy_path.sh` (wrappers called directly). Driving the skills *conversationally through the gateway agent* (one line → agent chains them) is unverified — same deferred check as Stage 2's 1f. **This is the prerequisite for Discord and Day 6's main event.**
- **Discord orchestration** (Phase B). Bot is live (guild `1511130058306228311`, `requireMention`, allowlist user `370013420013223937`). Open design point: a full run is ~18 min, but the Google/Gemini LLM idle timeout is ~120 s — a single agent turn can't hold a long MD. Resolve by either (a) tiny `--sim-ps` (e.g. 10) so a turn finishes synchronously, or (b) background the MD via the `process` tool + status pings.
- **Stages 6–8 + remote HPC** — PLIP, planner, bounded recovery, DPDispatcher. Untouched by design.
- **Not committed:** older `golden-path/*` 181L recipes, `smoke-test/`, `docs/` in project-prime remain untracked (pre-date Day 5); the vault's `Amber26.pdf` + `phase3-explicit-solvent-md*` remain untracked (large binaries).

## Optional tooling improvements (assessed 2026-06-05 — BUILDS, not eval; only if user opts in)

Assessed at end of Day 5; noted here so they aren't rediscovered. All three are small *builds* — Day 6 is an evaluation session, so do these only if the user explicitly wants them, and treat as out-of-scope otherwise.

- **md-param-check assertion in `amber-md-run/test_acceptance.sh` (highest value).** The Stage-4 namelists are md-param-check-clean *by construction*, but there's no INDEPENDENT check in the tests — a future edit to the generator could break a limit silently. Add a one-line call to the `md-param-check` validator (`.claude/skills/md-param-check/checks/check_amber.py`) over the generated `*.in` and assert it passes. **Do NOT do this as a Claude Code PostToolUse hook** — a hook only fires for Claude-Code-initiated actions, so it wouldn't protect manual or OpenClaw-driven runs (wrong layer); and the `.in` files are written by wrapper.py via Python I/O inside exec, invisible to Write/Edit matchers anyway. Belt-and-suspenders, engine-agnostic.
- **`verify` subagent (`.claude/agents/*.md`).** Low priority. The acceptance scripts already ARE the deterministic gate; a subagent only adds failure-diagnosis + clean main-context + scoped read-only perms. Confirm the current `.claude/agents/` frontmatter format before authoring (unverified as of 2026-06-05).
- **`/loop` Curator pass for vault upkeep.** Periodic vocab-drift / orphan-note / gap review — the "lint" habit from the LLM-Wiki verdict ([[llm-wiki-pattern]]). Separate from the chemistry pipeline; do whenever, not necessarily Day 6.

## The prompt to paste

```
Continuation of Project Prime OpenClaw — Day 6. EVALUATION session: the local AMBER MD happy path (Stages 2–5) is built and ran green on 1L2Y; today we manually verify it and attempt Discord orchestration. We are EVALUATING my prior work, not building new features.

Read these BEFORE acting (in order):
- memory: project-prime-status (CRITICAL — current state, Stages 3–5 built)
- memory: amber-md-prior-art, openclaw-canonical-paths, memory-system-options, llm-wiki-pattern
- vault: Dev_Log.md (2026-06-05 entry), Phase3_Taskboard_Manifest.md (Stages 3–5 + 6–8 sections), Skill_Tleap_Build / Skill_AMBER_MD_Run / Skill_CPPTraj_Analysis

Decisions banked, do NOT re-litigate: see "Decisions banked" in Next_Session_Prompt_OpenClaw_Day6.md (commodity baseline by design; wrapper-does-the-work; path-with-space rule; the baked-in correctness rules; memory/LLM-wiki ideas deferred).

Immediate sequence (EVALUATION + Discord ONLY — do NOT build Stage 6+/PLIP/recovery):

1. PRE-FLIGHT — confirm Day-5 state still holds (~5 min):
   a. Activate toolchain: `source /opt/homebrew/Caskroom/miniforge/base/envs/prime-amber/amber.sh && export PATH="$HOME/Downloads/pmemd26/bin:$AMBERHOME/bin:$PATH"`; confirm `which tleap cpptraj pmemd MMPBSA.py`.
   b. `cd "/Users/kevinzhou/Downloads/Single Particle/project-prime"`; `git log --oneline -1` should show 2e9d8a4 (Stages 3–5).
   c. Confirm OpenClaw sees the new skills: `openclaw skills list` (or `skills info tleap-build`) → Ready/visible. Gateway up on 127.0.0.1:18789.

2. MANUAL EVALUATION (let the user drive; assist + diagnose):
   - Fast end-to-end: `bash run_happy_path.sh 20` (~5 min) → expect 4 ok:true envelopes, ≥12 analyses, ΔG<0. Open PNGs in happy-path-run/analysis/.
   - Spot-check a `--dry-run` (SEE): inspect a generated leap.in / heat.in.
   - Optionally re-run a per-skill `test_acceptance.sh`.
   - If anything fails, diagnose against the baked-in correctness rules; do NOT loosen a validation gate to make it pass.

3. LIVE AGENT-TURN (prerequisite for Discord) — drive ONE skill through the gateway, not the harness:
   - e.g. `openclaw agent --agent main --message "Use the tleap-build skill on protein golden-path/1L2Y/1L2Y-1.pdb with the antechamber-prepped MOL ligand"` (adapt). Confirm the agent invokes the wrapper as one exec call and returns the envelope. This flips the long-standing live-agent-turn gate.

4. DISCORD ORCHESTRATION attempt:
   - @-mention the bot in guild 1511130058306228311 with a one-line request to run the pipeline.
   - Long-MD vs ~120 s idle timeout is the crux: start with tiny `--sim-ps` (~10) so a turn completes synchronously; if that works, decide whether to invest in background `process`-tool + status pings for full-length runs.
   - Capture what works / what stalls; this informs whether Phase B needs the async path.

5. CLOSING:
   a. Update Phase3_Taskboard_Manifest.md (flip Stage 2/3–5 live-agent-turn status if verified; note Discord findings).
   b. devlog-append skill: log the evaluation + Discord outcome.
   c. next-session-prompt skill: Day 7 starter (likely Phase B Discord hardening OR Stage 6 PLIP) — or note none needed.

Optional (only if the user opts in — these are BUILDS, not eval): see "Optional tooling improvements" section of Next_Session_Prompt_OpenClaw_Day6.md — the highest-value one is adding an independent md-param-check assertion to amber-md-run/test_acceptance.sh (NOT a Claude Code hook — wrong layer). Treat as out-of-scope unless asked.

Stop conditions:
- If a validation gate fails, STOP and investigate the cause; do NOT weaken the gate.
- If Discord long-run needs the async/process-tool path, STOP and confirm scope with the user before building it (that's a build task, not evaluation).

Scope-fence: EVALUATION + Discord orchestration ONLY. Do NOT start Stage 6 (PLIP), Stage 7/8, or remote HPC.
```

## After the session — update this file

1. Flip frontmatter `status: ready` → `status: consumed`.
2. Add `## Outcome` footer: consumed YYYY-MM-DD, 1-sentence outcome, link to [[Dev_Log]] entry.

## Cross-links

- [[Dev_Log]] entry 2026-06-05 — the session that produced this handoff.
- [[Phase3_Taskboard_Manifest]] — Stages 3–5 BUILT; 6–8 + Discord deferred.
- [[Next_Session_Prompt_OpenClaw_Day5]] — superseded by this (Day 5 built Stages 3–5).
