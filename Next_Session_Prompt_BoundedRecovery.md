---
tags: [project-prime, openclaw, session-handoff, bounded-recovery, error-recovery, amber]
type: handoff
status: ready
created: 2026-06-10
---

# Next Session Starter — Bounded Error Recovery (AMBER runtime recovery skill)

> Created 2026-06-10 at the end of the Stage-6 PLIP session. **Frontier chosen by the user: bounded error recovery.** The full local AMBER MD pipeline (Stages 0–6) is green; the next differentiator is the vault's strongest paper-cited element — a deterministic, mathematically-bounded recovery loop that detects MD runtime crashes and salvages the run *without* letting the LLM invent physics. The design is already spec'd in the vault — **implement it, don't re-derive it.** Paste the §The prompt to paste block into a fresh Claude Code session (run from the vault).

## Recap (what's done — don't re-discover)

- **Stages 0–6 DONE** — six green deterministic-wrapper skills (`antechamber-ligandprep`, `tleap-build`, `amber-md-run`, `cpptraj-analysis`, `plip-profile`, + `mdin-edit`, `pipeline-async`). Full local happy path GREEN, system-agnostic, NL-drivable, wired end-to-end. project-prime HEAD **`920afdd`** (master, local, not pushed). See [[Dev_Log]] 2026-06-10.
- **`amber-md-run` is the substrate the recovery loop wraps.** It runs the `min1·min2·min3·heat·density·production` pmemd chain through a `run_md()`/`ENGINE` seam, restart-chained (each stage's `.rst7` feeds the next), capturing each stage's `mdout` (`.out`). That `.out` + the `.rst7` chain are exactly the artifacts a recovery loop reads (detect from `mdout`) and rewinds to (restore last good `.rst7`). Read its wrapper first.
- **The bounded-recovery DESIGN is already in the vault — paper-cited, NotebookLM-verified.** `Skill_Bounded_Recovery_AMBER` (✅ strongest-tier, arXiv:2603.25522 methane-oxidation case study) + `Workflow_Error_Recovery_Loop` define the tiered loop, the detection-is-deterministic rule, and the halt conditions. This session is the *build*, not the design.
- **Config state still holds:** paid Google key in; default `google/gemini-3-flash-preview`; gateway on 127.0.0.1:18789; skills auto-load via `skills.load.extraDirs` watcher. The physical-realism bounds are encoded in `check_amber.py` / the `md-param-check` skill — the recovery mutation must respect them.

## Decisions banked — do NOT re-litigate

- **Tiered recovery (build BOTH tiers).** Tier 1 = restore the last good checkpoint (`.rst7`) and resume *as-is* (handles transient hardware/timeout/idle failures, zero physics risk). Tier 2 = bounded parameter mutation (lower `dt`, disable SHAKE) **only if Tier 1 re-crashes at/near the same step**, within hard limits, then restore normal parameters once the system is stable over N steps. **Mutation is the escalation, NEVER the first move** — this is the whole "you're letting an AI change physics" defensibility argument. See [[Skill_Bounded_Recovery_AMBER]] + [[Design_Determinism_Spectrum]].
- **Detection is DETERMINISTIC, not agentic.** Parse `mdout`/stderr with regex for the real failure signatures (NaN; coordinate overflow `*****`; `vlimit exceeded`; SHAKE failure; temperature blow-up; non-zero pmemd rc / no normal termination). The LLM is barred from the execution + diagnosis path — it only picks the skill. See [[openclaw-canonical-paths]] (deterministic-wrapper discipline) + CLAUDE.md SOPs.
- **HALT is bounded.** If recovery exceeds the bounded limits (max retries / `dt` hits its floor / still crashing at/near the same step), HALT with a structured `ok:false` that requests human guidance — never unbounded deviation or wasted compute. See [[Workflow_Error_Recovery_Loop]].
- **Physical-realism hard limits are the guardrail** (CLAUDE.md SOP #3): `dt` has a conservative floor (e.g. ≥ 0.5 fs); SHAKE-off is bounded (a set number of steps, then restored); the mutation can only move *toward* stability within `check_amber.py`'s bounds. The mutation engine reuses those bounds (don't invent new ones).
- **Strict-verifier loop** ([[Arch_Recursion_LOWE]] Predict→Test→Falsify→Improve): hypothesize a bounded fix → run N steps → check whether it re-crashed → escalate tier or halt. This is the loop's control structure.
- **Max 3 named agents** ([[multi-agent-scope]]) — recovery is a *skill* (optionally + one named recovery agent later), not a swarm.

## What's NOT done (deferred, non-blocking — do NOT start without confirming)

- **Remote/cluster crash-log gathering** ([[Infra_DPDispatcher]] / [[Gap_Remote_HPC_Backend]]) — local recovery first; the cluster path is the production-scale gate to settle with the advisor.
- **Tier-2 mutations beyond `dt`/SHAKE** (re-minimize, shrink `cut`, reseed velocities) — start with the spec's `dt`/SHAKE example; broaden only if needed.
- **The planner / `Arch_Taskboard_Manifest` layer** — the other roadmap frontier, deferred.
- **Wiring recovery into `run_happy_path.sh`/`amber-md-run`** as an always-on loop — reasonable at session end if the standalone skill is green (guard it; keep the happy path green).

## The prompt to paste

```
Continuation of the Single Particle / OpenClaw + AMBER project — building the BOUNDED ERROR RECOVERY skill (the user picked this frontier). Stages 0–6 are done; the full local AMBER MD pipeline is green. project-prime HEAD 920afdd (master, local). Default model paid google/gemini-3-flash-preview.

Today's work: build a deterministic-wrapper skill that detects a real pmemd MD crash and salvages the run via a TIERED bounded-recovery loop (Tier 1 checkpoint-restore as-is; Tier 2 bounded dt-lower/SHAKE-off only on re-crash; halt on bounded-limit). Bounded-recovery ONLY — do NOT start the planner / Taskboard / HPC.

Read these vault notes + memories BEFORE acting (in order):
- memory: project-prime-status (CRITICAL — current state; six green skills; amber-md-run is the substrate the loop wraps)
- memory: openclaw-canonical-paths (exec not bash; --gateway; SKILL.md single-line JSON metadata; deterministic-wrapper discipline; env.sh gotchas — zsh nomatch + set -u/amber.sh)
- memory: feedback-verify-and-eval + vault Eval_Criteria.md (THE working practice; it caught a real HIGH bug each of the last two sessions)
- memory: antechamber-aromatic-kekulize-bug (the silent-error culture)
- vault: Skill_Bounded_Recovery_AMBER (the tiered DESIGN — paper-cited; implement this), Workflow_Error_Recovery_Loop (the loop + halt conditions), Arch_Recursion_LOWE (Predict→Test→Falsify→Improve), Design_Determinism_Spectrum (the autonomy-not-capability positioning), Dev_Log.md (2026-06-10 entry)

Decisions banked, do NOT re-litigate:
- Tiered: Tier 1 checkpoint-restore as-is (safe default); Tier 2 bounded dt-lower/SHAKE-off ONLY on re-crash at/near the same step, within hard limits, restore normal once stable. Mutation is escalation, never first move.
- Detection is deterministic (regex on mdout/stderr: NaN, overflow *****, vlimit exceeded, SHAKE failure, temp blow-up, no normal termination), NOT agentic. LLM only picks the skill.
- Bounded HALT: max retries / dt floor (≥0.5 fs) / still crashing → structured ok:false requesting human. Reuse check_amber.py / md-param-check bounds; don't invent new ones.

Immediate sequence (bounded-recovery ONLY):
1. PRE-FLIGHT (~5 min): run AMBER work under `bash -c 'set +u; source scripts/env.sh >/dev/null 2>&1; set -u; …'` (env.sh trips zsh nomatch + set -u via amber.sh); which pmemd cpptraj; git -C project-prime log --oneline -1 (expect 920afdd+); openclaw skills list (six skills ✓ ready); curl -s -o /dev/null -w "%{http_code}" 127.0.0.1:18789/ (200). Foreground Claude Bash is sandboxed (126 on conda binaries) — background or disable-sandbox for conda work.
2. MAP: read skills/amber-md-run/scripts/wrapper.py — how it runs the pmemd chain (run_md/ENGINE), where the per-stage .rst7 + mdout (.out) land, how it detects/handles a stage failure today (if at all). Read check_amber.py / the md-param-check skill for the hard bounds the Tier-2 mutation must respect.
3. INDUCE A REAL CRASH (the test ground-truth — do NOT mock): craft an mdin that genuinely crashes pmemd on the 1L2Y fixture (e.g. dt far too large with SHAKE off, or deliberately clashing/blown-up start coords) and capture the REAL mdout failure signature. The detector + recovery must handle genuine pmemd instability, not a simulated string.
4. BUILD skills/amber-recover (or similar) — deterministic wrapper, --dry-run + JSON envelope: (a) deterministic detector classifies the mdout/stderr failure; (b) Tier 1 restores the last good .rst7 and resumes as-is; (c) on re-crash at/near the same step, Tier 2 applies a bounded fix (dt -> conservative within floor; SHAKE off for a bounded window) and resumes, restoring normal params once stable over N steps; (d) bounded HALT -> ok:false + human-request. One exec call per skill turn; wrapper enforces the loop, SKILL.md describes the goal.
5. TEST: test_acceptance.sh — golden (induced crash -> recovered run reaches normal termination); Tier-2 escalation (a crash surviving Tier 1 -> Tier 2 fires -> stabilizes); halt (unrecoverable within bounds -> ok:false + human-request, not a crash); malformed -> ok:false. Add an independent oracle for the detector regexes (real mdout fixtures, fault-injection). Cross-python (conda 3.11).
6. (If green) optionally wrap run_md/amber-md-run with the recovery loop — guarded; keep the 1L2Y happy path green.
7. NL DRIVE: one `openclaw agent` turn — "the MD run crashed, recover it" -> the recovery skill with the right inputs; byte/behaviour-verify vs the CLI.
8. CLOSING: USE the devlog-append skill (not a hand-written entry) to log the session; USE the next-session-prompt skill to write the next handoff (planner OR settle Gap_Remote_HPC_Backend); flip THIS handoff status->consumed + Outcome footer; update Phase3_Taskboard_Manifest stage status if it tracks stages; run the adversarial second-AI review per Eval_Criteria.md BEFORE declaring done; commit local-not-pushed.

Stop conditions:
- If you cannot induce a GENUINE pmemd crash, STOP — do not build/test against mocked failures; the skill must recover a real instability.
- If a Tier-2 mutation would breach a physical-realism hard limit (dt floor), HALT — do not push past the bound. Halting IS the correct behaviour; that is the bounded-recovery guarantee.
- Never let the LLM diagnose or choose the fix — detection + recovery are deterministic; the LLM only picks the skill.

Scope-fence: BOUNDED ERROR RECOVERY ONLY. Do NOT start the planner / Arch_Taskboard_Manifest, HPC / DPDispatcher, or any Tier-2 mutation beyond dt/SHAKE without confirming.
```

## After the session — update this file

1. Flip frontmatter `status: ready` → `status: consumed`.
2. Add an `## Outcome` footer: consumed YYYY-MM-DD, 1-sentence outcome, link to the [[Dev_Log]] entry.

## Cross-links

- [[Dev_Log]] 2026-06-10 — "Stage 6 DONE: PLIP interaction profiling" — the session that produced this handoff (its `Next:` line points here).
- `Next_Session_Prompt_Stage6_PLIP.md` (consumed) — the prior handoff.
- vault: [[Skill_Bounded_Recovery_AMBER]], [[Workflow_Error_Recovery_Loop]], [[Arch_Recursion_LOWE]], [[Design_Determinism_Spectrum]].
- memories: [[project-prime-status]], [[feedback-verify-and-eval]], [[openclaw-canonical-paths]], [[multi-agent-scope]].
