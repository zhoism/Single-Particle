---
tags: [project-prime, openclaw, session-handoff, day-5, stage-3, skills]
type: handoff
status: consumed
created: 2026-06-04
---

> **Outcome — consumed 2026-06-05.** Day 5 went beyond its Stage-3 scope: built Stages 3, 4, AND 5 (`tleap-build`, `amber-md-run`, `cpptraj-analysis`) and ran the full local AMBER MD happy path green end-to-end on 1L2Y (MM-GBSA ΔG −13.29 kcal/mol). See [[Dev_Log]] 2026-06-05 and the successor handoff [[Next_Session_Prompt_OpenClaw_Day6]] (evaluation + Discord). The live agent-turn verification (pre-flight 1f below) was NOT done — carried forward to Day 6 as the Discord prerequisite.

# Next Session Starter — OpenClaw Day 5 / Phase 3 Stage 3 (tleap-build)

> Created 2026-06-04 at end of Day 4. Day 4 built `antechamber-ligandprep` (acceptance 3/3 PASS, substrate ✓ Ready) but the live agent-turn verification was blocked by a sustained Google AI Studio 503 outage on the agent payload. Day 5 starts with that deferred verification as pre-flight 1f, then moves to Stage 3 (tleap-build) per [[Phase3_Taskboard_Manifest]]. Same template as Stage 2 — wrapper-internal chain, goal-oriented SKILL.md, acceptance against golden-path. Paste the §The prompt to paste fenced block into a fresh Claude Code session (run from the vault).

## Day 4 recap (what's done — don't re-discover)

- **`antechamber-ligandprep` skill built and committed.** Four files at `project-prime/skills/antechamber-ligandprep/` (SKILL.md, scripts/wrapper.py, references/heuristics.md, test_acceptance.sh). Four commits in `project-prime/` (`f2307db` baseline → `817f78d` Case 3 dry-run skip → `121f0f9` 5e-3 tolerance → `29a99ce` drop bins gating). These were the repo's first 4 commits; project-prime had no prior history.
- **Acceptance 3/3 PASS.** Golden benzene PDB → `BNZ.mol2` with `ca`/`ha` types; methane SMILES → `MTH.mol2` with `c3`/`hc`; malformed PDB → ok=false with parseable error. See [[Dev_Log]] 2026-06-04.
- **Substrate ✓ Ready.** `openclaw skills info antechamber-ligandprep` reports Ready, Visible to model, Available as command.
- **Gateway env patch applied & persisted DON'T REDO.** `~/.openclaw/openclaw.json` now has `env.vars.AMBERHOME`, `env.vars.PATH` (composed standard + conda bin), and `tools.exec.pathPrepend`. Verify with `openclaw config get env.vars.AMBERHOME`. Patch file at `/tmp/openclaw-amber-env-patch.json5` (regeneratable; not committed anywhere).
- **Day 4 starter file flipped to `consumed`** (after Day 5 starts and verifies; see §After the session below).

## Decisions banked — do NOT re-litigate

- **Wrapper does the work; SKILL.md describes the goal.** Single exec call per skill turn. Latency + reliability + determinism, three load-bearing reasons. See [[OpenClaw_CLI_Map]] §Stage 2 design intuition and [[openclaw-canonical-paths]] §6.
- **Single-line JSON `metadata` in SKILL.md frontmatter.** OpenClaw 2026.5.28's embedded parser quirk; multi-line silently fails to load.
- **Net-charge validation tolerance is `5e-3`.** Antechamber's 6-decimal mol2 precision accumulates ~2e-3 per small molecule. 5e-3 is the standard MD-community "effectively neutral" gate that still catches real `--nc` mismatches. See `wrapper.py` validate() and 2026-06-04 Dev_Log.
- **`metadata.openclaw.requires` should NOT include `bins`.** Gateway's load-time `which` check uses the gateway process's own PATH, not `env.vars.PATH` (which only reaches spawned subprocesses). The wrapper's own preflight (PATH first, `$AMBERHOME/bin` fallback) is the real gate. Keep `requires.env: ["AMBERHOME"]` — that one does work because env vars (unlike PATH) get injected. Re-add bins only if a future OpenClaw release fixes load-time PATH injection.
- **Test_acceptance.sh skips Case 3 (malformed) under `--dry-run`.** Dry-run plans the chain without inspecting content, so the malformed PDB plans identically to a good one; the "fails gracefully" contract is meaningful only when subprocesses execute.
- **Max 3 named OpenClaw agents total** (`main` + future `planner` + future `recovery`), NOT a swarm. See memory `multi_agent_scope`.

## What's NOT done (deferred, non-blocking)

- **Live agent-turn verification of `antechamber-ligandprep`.** Day 4's `openclaw agent --message "Prepare benzene..." --json` failed with sustained 503s across 3 retries while direct `openclaw infer model run` returned "ack" cleanly — capacity-throttled on the larger agent payload. Re-attempt is **pre-flight check 1f**; success flips Stage 2 BUILT→COMPLETE. Trace at `project-prime/runs/substrate-verification/day4-stage2/agent-turn-503-trace.txt`.
- **Stage 0 cleanup** — gateway token rotation, plaintext-secrets migration, plugin allowlist hygiene. Non-blocking from Day 1.
- **Memory `openclaw-canonical-paths` §9 update** — add the gateway-env-injection asymmetry finding (env.vars works for AMBERHOME but env.vars.PATH does NOT affect gateway's own which-check; tools.exec.pathPrepend is exec-only). Low priority; do if time permits at end of Day 5.

## The prompt to paste

```
Continuation of Phase 3 — OpenClaw Day 5. Day 4 built and validated
antechamber-ligandprep (acceptance 3/3 PASS, substrate ✓ Ready) but
the live agent-turn verification was blocked by upstream Google 503.

Today's work: pre-flight (including the deferred live agent turn for
Stage 2) → Stage 3 (Skill_Tleap_Build) per Phase3_Taskboard_Manifest.

Read these vault notes + memories BEFORE acting (in this order):

- memory: openclaw-canonical-paths (CRITICAL — 16 sections, load-bearing
  CLI/runtime facts including SKILL.md authoring §8 and skill loading §9)
- memory: project-prime-status, openclaw-install-state, upstream-chemistry-skills-library,
  phase3-advisor-demo, amber26-pdf-section-map, multi-agent-scope
- vault: Dev_Log.md (2026-06-04 entry on top — Day 4 substantial entry with
  banked decisions for Stage 2), Phase3_Taskboard_Manifest.md (Stage 2 + 3
  sections), OpenClaw_CLI_Map.md (§SKILL.md authoring + §Skill loading +
  §Stage 2 design intuition), Actionable_Recommendations.md (§1 BUILD/INTEGRATE/ADOPT
  triage), Skill_Bounded_Recovery_AMBER.md (tleap's failure modes inform
  Stage 3's error envelope), Next_Session_Prompt_OpenClaw_Day4.md (Day 4
  paused-session log at top — context for the banked decisions)
- Claude Code skills (auto-discover from .claude/skills/ + ~/.claude/skills/):
  skill-scaffold (load-bearing for Step 3), devlog-append (load-bearing for
  Step 5), next-session-prompt (load-bearing for Day 6 handoff). Also
  available but not load-bearing for Stage 3: md-param-check, vault-note-new,
  memory-bank, intake-verify.

Decisions banked, do NOT re-litigate (from Day 4):
- Single-line JSON metadata in SKILL.md (OpenClaw embedded-parser quirk).
- Wrapper does the work; SKILL.md describes the goal (one exec call per turn).
- Net-charge tolerance 5e-3 (mol2 6-decimal precision accumulator; carry the
  same pattern to any Stage 3 charge-sum gate).
- Drop bins from metadata.openclaw.requires; keep env: ["AMBERHOME"].
- Skip malformed-case assertion under --dry-run.

Immediate sequence (Stage 3 only — DO NOT extend to Stage 4+):

1. PRE-FLIGHT — confirm Day 4 state still holds (~10 min):
   a. openclaw gateway status (running, write-capable)
   b. openclaw config get env.vars.AMBERHOME (should return the conda env path)
   c. openclaw config get tools.exec.pathPrepend (should return the conda bin)
   d. openclaw models status | grep cooldown (should NOT show cooldown)
   e. openclaw skills info antechamber-ligandprep (should show ✓ Ready)
   f. DEFERRED LIVE AGENT TURN — `openclaw agent --agent main --message
      "Prepare benzene for AMBER MD. Input at
      /Users/kevinzhou/Downloads/Single Particle/project-prime/golden-path/ligand_raw.pdb.
      Residue name BNZ, neutral charge, output to
      /Users/kevinzhou/Downloads/Single Particle/project-prime/runs/substrate-verification/day5-stage2-retry."
      --json --thinking minimal --timeout 600`. Verify toolSummary.calls=1
      (single exec call to wrapper, NOT 3 separate calls) and final reply
      references real wrapper output (mol2 + frcmod paths + ca/ha atom types).
      ON SUCCESS: flip Phase3_Taskboard_Manifest Stage 2 BUILT → COMPLETE in
      both frontmatter status and the Stage 2 §Status line. ON STILL-503:
      check `openclaw infer model run --gateway --prompt "ack"` to confirm
      provider is up; if up, wait 5-10 min and retry once; if persistently
      503, document and defer to Day 6 (don't block Stage 3 work on it).

2. PLAN Stage 3 per Phase3_Taskboard_Manifest before any execution. Sketch:
   - Inputs: a protein topology source (PDB file), a ligand library
     (.mol2 + .frcmod from antechamber-ligandprep output), optional water
     model (default tip3p), optional ion type (default Na+/Cl-).
   - Internal chain: pdb4amber (clean protein) → tleap script generation
     (envsubst from a template per upstream pattern) → tleap execution →
     output validation (parm7 atom count > 0, rst7 box dimensions sane,
     leap.log clean of "FATAL" lines).
   - Outputs: {parm7, rst7, leap.log} paths in JSON envelope.
   - Acceptance fixture: protein from PDB 181L + benzene from Stage 2 output
     → reproduce `project-prime/golden-path/system.{parm7,rst7}` from
     2026-05-21 (the validated golden-path fixture).

3. SCAFFOLD project-prime/skills/tleap-build/ via skill-scaffold skill
   (~60 min). Same procedure as Day 4 Stage 2. Skill kebab-name:
   tleap-build. Required bins: tleap, pdb4amber. Required env: AMBERHOME.
   Single-line JSON metadata; goal-oriented body; --dry-run on the wrapper;
   JSON envelope; LGPL-3.0 attribution on heuristics adapted from upstream
   `~/Downloads/Single Particle/upstream-reference/computational-chemistry-agent-skills/`
   (check for a tleap skill there; if none, no attribution needed).

4. VALIDATE: validate-skill.sh + test_acceptance.sh --dry-run + full
   test_acceptance.sh. Acceptance must pass before substrate verify.

5. CLOSING (do these before ending):
   a. Edit Phase3_Taskboard_Manifest.md: Stage 2 status (if pre-flight 1f
      succeeded, flip to COMPLETE) + Stage 3 status (PENDING → BUILT or
      COMPLETE depending on whether the live agent turn for Stage 3 also
      runs; same provider-503 risk applies).
   b. INVOKE devlog-append skill. Entry type = "substantial." Cover: Stage 2
      live-turn outcome, Stage 3 scaffold + acceptance, any new decisions banked.
   c. INVOKE next-session-prompt skill to draft Next_Session_Prompt_OpenClaw_Day6.md
      for Stage 4 (sander/pmemd wrapper).
   d. Flip THIS file's frontmatter status: ready → status: consumed with a
      one-line outcome footer.

Stop conditions:
- If pre-flight 1f STILL-503s after 5-10 min retry, DOCUMENT and continue
  with Stage 3 scaffold work — do NOT block the whole session on a provider
  outage.
- If `openclaw config get env.vars.AMBERHOME` returns Config-path-not-found,
  the Day 4 config patch was reverted by something. Re-apply from
  /tmp/openclaw-amber-env-patch.json5 (regenerate the file if /tmp was wiped;
  see Day 4 Dev_Log for the contents) and restart gateway.
- If Stage 2's antechamber-ligandprep skill is missing from `openclaw skills
  list`, watcher state desynced. `openclaw gateway restart` and verify.

Scope-fence: OpenClaw Day 5 / Phase 3 Stage 3 (tleap-build) ONLY.
DO NOT extend to Stage 4 (sander/pmemd) or Stage 5+ regardless of how
fast Stage 3 goes. Day 6 handles Stage 4.

Hard constraints (from project memory — do not violate):
- All real inference goes through `--gateway`. See [[openclaw-canonical-paths]] §3.
- LLM is BARRED from deterministic execution. Skills are Python/shell wrappers.
- SKILL.md prose must describe GOALS, not tool-call topology. See [[openclaw-canonical-paths]] §6.
- metadata MUST be single-line JSON in SKILL.md frontmatter.
- Physical realism non-negotiable (dt ≤ 2fs, etc. — Stage 4 concern but bake into
  any Stage 3 output validation that checks downstream-readiness).
- Runnable code in /Users/kevinzhou/Downloads/Single Particle/project-prime/skills/.
- Upstream reference is LGPL-3.0 — adapt instruction text, cite source, don't
  depend on the package at runtime.
- Skill design = wrapper-internal chaining per Day 3 latency findings.
- For project-prime git: each scaffolded skill + each design fix gets its own
  commit. The audit trail is the reversibility guarantee.

Plan first per Phase3_Taskboard_Manifest before any execution. Stage 3
acceptance test must pass before manifest flips to BUILT (and live agent
turn must succeed before BUILT → COMPLETE).
```

## After the session — update this file

When Day 5 consumes this handoff:
1. Flip frontmatter `status: ready` → `status: consumed`.
2. Add a footer: `## Outcome\n\nConsumed 2026-06-05 by Day 5 session. Outcome summary: <1-sentence>. See [[Dev_Log]] entry 2026-06-05.`
3. If the handoff was superseded mid-day (e.g., scope changed mid-session), flip to `status: superseded` with a pointer to whatever replaces it.

## Cross-links

- [[Dev_Log]] entry 2026-06-04 — the Day 4 session that produced this handoff.
- [[Phase3_Taskboard_Manifest]] — manifest stages 2 (BUILT, pending live-turn) and 3 (PENDING).
- [[Next_Session_Prompt_OpenClaw_Day4]] — superseded predecessor; contains the paused-session log + 4-step procedure that Day 4 followed.
- [[OpenClaw_CLI_Map]] §Stage 2 design intuition — generalizes to Stage 3.
- [[Skill_Antechamber_LigandPrep]] — vault sketch superseded by `project-prime/skills/antechamber-ligandprep/` artifacts.
