---
tags: [project-prime, openclaw, session-handoff, arbitrary-target, phase-b]
type: handoff
status: consumed
created: 2026-06-09
---

# Next Session Starter — Arbitrary-Target Input (generalize the pipeline beyond 1L2Y)

> Created 2026-06-09 at end of the Track-1/Track-2 session. **Track 1** (mdin-edit `--submit` + live NL drive) and **Track 2** (Discord live full-pipeline e2e, with per-step notifications) are both DONE and proven. Next work = **Track (b): make the pipeline run an ARBITRARY user-supplied target (protein PDB + ligand), not just the hardcoded 1L2Y fixture.** Paste the §The prompt to paste block into a fresh Claude Code session (run from the vault).

## Recap (what's done — don't re-discover)

- **Track 2 DONE** — a Discord @-mention drives the full detached pipeline (ligand prep → topology → MD → analysis + MM-GBSA) on free-running Flash, with **live per-step notifications** (🚀 → each stage's ▶️/✓ → all 6 MD steps min1..product as each `.rst` lands → ⏳ heartbeats → ✅ with ΔG + RMSD plot). Proven end-to-end (run `pa-20260609-214553`, ΔG −18.49 kcal/mol, 0 send failures).
- **The notify bug (found+fixed+committed `f3524aa`, local):** the detached job inherits the gateway exec PATH where a stale `/usr/local/bin/node` v20 sat ahead of nvm → `openclaw` aborted with "Node 22.19+ required" and the error was swallowed. Fix in `scripts/env.sh` (prepend an nvm bin with node ≥22 + openclaw); `scripts/notify_discord.sh` now surfaces the real error; `run_happy_path.sh` gained the verbose NOTIFY mode. **Don't re-debug this.**
- **Track 1 DONE** — `mdin-edit --submit` (edit→run smoke productized) + live NL drive byte-verified. See [[Dev_Log]] 2026-06-09.
- **Config state that must still hold:** paid Google AI Studio key is in (`google:manual`); **default model = `google/gemini-3-flash-preview`** (set via `openclaw models set`); gateway was restarted 2026-06-09 ~15:52 and the Discord bot is connected (per-guild `users` allowlist is the working mechanism). project-prime HEAD **`f3524aa`** (NOT pushed).

## Decisions banked — do NOT re-litigate

- **The four pipeline skills are already system-agnostic** (`antechamber-ligandprep`, `tleap-build`, `amber-md-run`, `cpptraj-analysis` — "no hardcoded ligand"). The 1L2Y hardcoding lives ONLY in **`run_happy_path.sh`** (`FIX="$ROOT/golden-path/1L2Y"` + fixed filenames `ligand.pdb`, `1L2Y-1.pdb`) and **`skills/pipeline-async`** (fixed target). Track (b) = parameterize those two, not the skills.
- **Never `--nohyd` a ligand**; an H-present ligand PDB must route to `antechamber -fi pdb` (the `antechamber-aromatic-kekulize-bug` lesson). Don't cite retracted ΔG (−13.x); corrected reference ≈ −17 (single-trajectory MM-GBSA is a sanity number, not precise).
- **Notify = LLM-free `openclaw message send`**, detached job, one DRY chain (`NOTIFY_CHANNEL` opt-in). Don't switch to webhooks/sub-agents.
- **`channels.discord.groupAllowFrom` is NOT a valid schema key** in OpenClaw 2026.5.28 — do not re-add it (it aborts the gateway). The per-guild `users` allowlist is correct.

## What's NOT done (deferred, non-blocking — do NOT start without confirming)

- **`Gap_Remote_HPC_Backend`** — the real gate to production-scale science (local is CPU-only ~15 ns/day). A *decision* to settle with the advisor, not a local build.
- **Stage 6 PLIP**, **bounded error recovery** (`Workflow_Error_Recovery_Loop`), **planner / Taskboard-Manifest** layer — the next differentiators AFTER arbitrary-target input.
- Always-on watcher LaunchAgent; pushing commits.

## The prompt to paste

```
Continuation of the Single Particle / OpenClaw + AMBER project — Track (b): generalize the local pipeline to run an ARBITRARY user-supplied target (protein PDB + ligand), not just the hardcoded 1L2Y fixture. Track 1 (mdin-edit) and Track 2 (Discord live e2e) are DONE; project-prime HEAD f3524aa (local). Default model is paid google/gemini-3-flash-preview.

Read BEFORE acting (in order):
- memory project-prime-status (CRITICAL — current state, Track 1+2 done, the node/notify fix)
- memory antechamber-aromatic-kekulize-bug (never --nohyd a ligand; H-present PDB → antechamber -fi pdb)
- memory openclaw-canonical-paths (exec not bash; --gateway; SKILL.md single-line JSON; LLM-free message send)
- vault Dev_Log.md (2026-06-09 entries) ; skills/{pipeline-async,amber-md-run,antechamber-ligandprep,tleap-build,cpptraj-analysis}/SKILL.md

Banked, do NOT re-litigate: the four pipeline skills are already system-agnostic — the 1L2Y hardcoding is ONLY in run_happy_path.sh (FIX=golden-path/1L2Y + fixed filenames) and skills/pipeline-async; never --nohyd a ligand; notify via LLM-free `openclaw message send`; do NOT add channels.discord.groupAllowFrom (invalid schema).

Immediate sequence (arbitrary-target input ONLY):
1. PRE-FLIGHT (~5 min): source project-prime/scripts/env.sh; which tleap pmemd cpptraj MMPBSA.py; git -C project-prime log --oneline -1 (expect f3524aa+); openclaw skills list (pipeline-async ✓); openclaw models status (default gemini-3-flash-preview, no cooldown); curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18789/ (200).
2. MAP the hardcoding: read run_happy_path.sh (the FIX= block + the s2/s3 input args) and skills/pipeline-async/scripts/wrapper.py (the fixed-target launch). Confirm the four skills already take --protein/--ligand-style inputs.
3. PARAMETERIZE: add --protein <pdb> and --ligand <pdb|smiles|mol2> (+ --charge, default 0) to run_happy_path.sh and pipeline-async, defaulting to the 1L2Y fixture so existing runs/tests stay byte-green. Validate inputs gracefully (missing/malformed → structured ok:false, not a crash). Keep the space-in-path discipline (copy inputs under bare names) and the NOTIFY_CHANNEL + env.sh node-prepend behavior intact.
4. TEST: (a) regression — run on 1L2Y, still green (4/4 ok, ΔG<0); (b) a NEW target end-to-end (pick a small protein+ligand, e.g. a PDB with a clean small-molecule ligand) to completion. Verify the ligand was H-handled correctly (no --nohyd; aromatic types sane).
5. NL DRIVE: one `openclaw agent` / Discord turn — "run MD on <protein> with <ligand>" → pipeline-async with the right --protein/--ligand args.
6. CLOSING: devlog-append; update memory project-prime-status + MEMORY.md; next-session-prompt for the step after (Stage 6 PLIP). Commit local-not-pushed.

Stop conditions:
- If a new target exposes a ligand-prep edge case (charge, metals, cofactors), note it and fall back to a clean test ligand — don't rabbit-hole on exotic chemistry.
- If parameterizing would break the 1L2Y regression, keep 1L2Y as the default path and fix to green before moving on.

Scope-fence: arbitrary-target INPUT ONLY. Do NOT start Stage 6 (PLIP), bounded recovery, the planner, or HPC/DPDispatcher without confirming.
```

## Outcome

**Consumed 2026-06-09.** Track (b) DONE — `run_happy_path.sh` + `pipeline-async` parameterized with `--protein/--ligand/--charge/--name` (default 1L2Y, no-target launch byte-identical); proven on the **1L2Y regression** (ΔG −18.16, unchanged) AND a **NEW target 3HTB (T4 lysozyme + 2-propylphenol JZ4)** end-to-end GREEN (2636/27512 atoms, ΔG −27.41, ligand H-handled correctly), with the **NL drive** verified on live `google/gemini-3-flash-preview`. Commit project-prime `95f20ed`. Next handoff: `Next_Session_Prompt_Stage6_PLIP.md`. See [[Dev_Log]] 2026-06-09 (cont.) — "Track (b) DONE: arbitrary-target input".

## After the session — update this file

1. ~~Flip frontmatter `status: ready` → `status: consumed`.~~ ✓
2. ~~Add an `## Outcome` footer.~~ ✓

## Cross-links

- [[Dev_Log]] 2026-06-09 — the Track-1/Track-2 session that produced this handoff.
- `Next_Session_Prompt_Advisor_LiveDrive_PhaseB.md` (consumed) — the prior handoff.
- memories: [[project-prime-status]], [[antechamber-aromatic-kekulize-bug]], [[openclaw-canonical-paths]].
