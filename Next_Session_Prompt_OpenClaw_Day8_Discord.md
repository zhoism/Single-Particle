---
tags: [project-prime, openclaw, session-handoff, day-8, phase-b, discord]
type: handoff
status: consumed
created: 2026-06-07
---

# Next Session Starter — OpenClaw Day 8 / Phase B (Discord orchestration)

> Created 2026-06-07. The full local AMBER MD pipeline now runs end-to-end **as an OpenClaw agent** (proven on both paid-google and FREE Cerebras). Phase B is the last piece: drive a skill / the pipeline **through the Discord bot** (@-mention → agent runs it → replies). Paste the §The prompt to paste block into a fresh Claude Code session (run from the vault). **Phase B needs you present** — the bot only acts on your @-mention, so this can't be automated.

## Day 7 recap (what's done — don't re-discover)

- **Pipeline PROVEN as an agent, two ways.** (1) Single-skill live-agent-turn flipped on paid-google (2026-06-06). (2) **Full 4-skill chain** (antechamber → tleap → MD 5 ps → cpptraj) driven by ONE agent turn on **FREE Cerebras `gpt-oss-120b`** (2026-06-07 overnight): 12/12 analyses, MM-GBSA ΔG −12.84 kcal/mol, $0. See [[Dev_Log]] 2026-06-07 + 2026-06-05 (cont.).
- **Default model is now `cerebras/gpt-oss-120b`.** OpenClaw natively supports `cerebras/*`; free ≈ 1M tokens/day. Auth profile `cerebras:manual` is set. (Revert to google: `openclaw models set google/gemini-3-flash-preview`.)
- **Stages 2–5 BUILT + QC'd** in `project-prime/skills/` (HEAD `2e9d8a4`); `run_happy_path.sh` is the agent-free spine; `/eval-happy-path` command exists for the deterministic QC pass.
- **Discord bot is LIVE** — guild `1511130058306228311`, `requireMention: true`, allowlist user `370013420013223937`. Bundled `discord` skill handles message ops.
- **Vault housekeeping (this session):** all prior starters (OpenClaw Day4/5/6 + the original `Next_Session_Prompt_OpenClaw.md` + `Next_Session_Prompt_Phase1Report.md`) were **deleted as retired**. This is the single active starter.

## Decisions banked — do NOT re-litigate

- **Cerebras is the free multi-turn provider.** Google free tier = ~1 agent turn/day (token 429s); Cerebras free ran the whole pipeline for $0. See [[project-prime-status]] (2026-06-07 update). Paid-google is the fallback for reliability (cents/turn).
- **Commodity baseline by design.** The local happy path replicates baifan-wang's amber-md on our deterministic-wrapper architecture — see [[amber-md-prior-art]]. Don't re-debate "someone already built it."
- **Wrapper does the work; SKILL.md describes the goal; one exec call per skill turn.** Phrase agent/Discord prompts as GOALS, not tool-call topology (topology prompts trigger idle stalls). See [[openclaw-canonical-paths]].
- **Path-with-space + the baked-in correctness rules** stay as-is (comp_dry-before-solvateoct, heat temp0==&wt value2, strip-with-solvated, PCA two-call, cluster repout). Don't "simplify" them away.

## What's NOT done (deferred, non-blocking)

- **The long-MD vs ~120s-idle problem (THE crux of Phase B).** A full pipeline turn is ~15 min — far over OpenClaw's ~120s LLM idle timeout and Discord's synchronous reply model. Start small; the async path is a *build* (see prompt).
- **Cerebras reliability.** Back-to-back heavy turns can 120s-idle-stall (60k tokens/min cap) — space them. A ~15-min turn also brushed the 900s agent `--timeout` (raise past 900s for long turns).
- **Stage 6 PLIP / Stage 7 planner / Stage 8 bounded recovery / remote HPC** — untouched by design.
- **`disablesleep`** — if `sudo pmset -c disablesleep 1` is still set from the overnight run, revert it (`sudo pmset -c disablesleep 0`). See [[revert-disablesleep-reminder]].

## The prompt to paste

```
Continuation of Project Prime OpenClaw — Day 8, Phase B (Discord orchestration). The full local AMBER MD pipeline is built, QC'd, and PROVEN to run end-to-end as an OpenClaw agent (full 4-skill chain ran on FREE Cerebras gpt-oss-120b: 12/12 analyses, MM-GBSA ΔG −12.84, $0). Today: drive a skill / the pipeline through the Discord bot. I (the user) am present and will @-mention the bot — Discord can't be automated.

Read these BEFORE acting (in order):
- memory: project-prime-status (CRITICAL — current state, Cerebras unblock, Phase A done)
- memory: openclaw-canonical-paths (CRITICAL — exec tool, 120s idle timeout, Discord allowlist, goal-not-topology prompting), amber-md-prior-art, revert-disablesleep-reminder
- vault: Dev_Log.md (2026-06-07 + 2026-06-05 cont. entries), Phase3_Taskboard_Manifest.md (Day-7 status + Stages 6–8 + Discord deferred note)

Decisions banked, do NOT re-litigate: see "Decisions banked" in Next_Session_Prompt_OpenClaw_Day8_Discord.md (Cerebras = free multi-turn provider; commodity baseline; wrapper-does-the-work / goal-not-topology; baked-in correctness rules).

Immediate sequence (Phase B Discord ONLY — do NOT build Stage 6+/PLIP/recovery):

1. PRE-FLIGHT — confirm state still holds (~5 min):
   a. Toolchain: `source /opt/homebrew/Caskroom/miniforge/base/envs/prime-amber/amber.sh && export PATH="$HOME/Downloads/pmemd26/bin:$AMBERHOME/bin:$PATH"`; `which tleap cpptraj pmemd MMPBSA.py`.
   b. `cd "/Users/kevinzhou/Downloads/Single Particle/project-prime"`; `git log --oneline -1` → 2e9d8a4.
   c. Gateway up: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18789/health` → 200. Skills ready: `openclaw skills list` → the 4 project skills ✓. Model: `openclaw models status` (cerebras/gpt-oss-120b, or switch). Discord bot connected (channels status / probe).
   d. If `sudo pmset -g | grep SleepDisabled` shows 1, remind the user to revert (`sudo pmset -c disablesleep 0`).

2. START SMALL — prove Discord → agent → skill → reply (the gate for Phase B):
   - User @-mentions the bot in guild 1511130058306228311 with a TINY one-line goal that completes well under ~120s — e.g. "parameterize the ligand at golden-path/1L2Y/ligand.pdb (charge 0) with the antechamber skill and report the result," or a --dry-run.
   - Confirm: the bot picks the skill, the agent makes one exec call, and it REPLIES in-channel with the envelope. Capture what works / what stalls.

3. DECIDE on full-length runs (the crux):
   - If the small task works, assess whether a FULL pipeline run can complete synchronously in a Discord turn. It almost certainly CANNOT (~15 min >> 120s idle). 
   - If full-length needs the async path (background the MD via the `process` tool + status pings to the channel) → STOP and confirm scope with the user. That is a BUILD, not Phase-B evaluation.

4. CLOSING (before ending):
   a. Update Phase3_Taskboard_Manifest.md (Discord findings; flip Phase B status).
   b. devlog-append skill: log the Discord outcome.
   c. next-session-prompt skill: write the next starter (likely Phase-B async build OR Stage 6 PLIP) — or note none needed.

Stop conditions:
- If full-length Discord runs need the async/process-tool path → STOP, confirm scope (build, not eval).
- If Cerebras stalls repeatedly (120s idle) → space runs out, or switch to paid-google (`openclaw models set google/gemini-3-flash-preview`) for reliability; tell the user it's cents/turn.

Scope-fence: Phase B Discord orchestration ONLY. Do NOT start Stage 6 (PLIP), Stage 7/8, remote HPC, or the async build without confirming scope.
```

## After the session — update this file

1. Flip frontmatter `status: ready` → `status: consumed`.
2. Add `## Outcome` footer: consumed YYYY-MM-DD, 1-sentence outcome, link to [[Dev_Log]] entry.

## Cross-links

- [[Dev_Log]] entry 2026-06-07 — the session that produced this handoff.
- [[Phase3_Taskboard_Manifest]] — Stages 2–5 ✅ (incl. agent orchestration); Discord (Phase B) + Stages 6–8 deferred.
- [[project-prime-status]], [[openclaw-canonical-paths]], [[revert-disablesleep-reminder]] — memories to load first.

## Outcome

**Consumed 2026-06-08.** Phase B Discord small-task gate **PASSED** — a user @-mention drove `antechamber-ligandprep` through the bot on free Cerebras → in-channel reply ($0). QC of that reply then caught a **silent aromatic ligand mis-typing** (obabel kekulize failure → non-aromatic types + dropped ring N–H, all gates passing) that had affected every prior run; it was fixed (H-present PDB → `antechamber -fi pdb -j 4`; new `AROMATIC_PERCEPTION_FAILED` gate; corrected MM-GBSA ΔG −17.18), committed, and re-verified live through Discord. The session then **expanded Phase B**: an async `pipeline-async` skill (detached full run + per-stage Discord pings via LLM-free `openclaw message send`) and a manual-start 429 self-alert watcher. See [[Dev_Log]] 2026-06-08.
