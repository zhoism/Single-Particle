---
tags: [project-prime, openclaw, session-handoff, day-4]
type: handoff
status: ready
created: 2026-06-03
---

# Next Session Starter — OpenClaw Phase Day 4

> Created 2026-06-03 (late) at end of Day 3. Day 3 cleared Stage 1 (substrate verification 3/3 PASS), deep-read OpenClaw primary docs, re-assessed upstream library, articulated the 5-level scaling architecture, and applied Stage 2 step 1 (`skills.load.extraDirs` patched). Day 4 starts at Stage 2 of `Phase3_Taskboard_Manifest.md`. Paste the code block into a fresh Claude Code session (run from the vault).

## Day 3 recap (what's done — don't re-discover)

- **Substrate verified.** Stage 1 PASS 3/3. JSON output reliable; `exec` tool fires real shell; multi-tool chain works (but explicit "use N tool calls" triggers Flash 120s idle stalls — phrase prompts in goals, not topology). Transcripts at `project-prime/runs/substrate-verification/`.
- **Deep doc-read complete.** All load-bearing facts captured in [[openclaw-canonical-paths]] memory (16 sections) and vault note `OpenClaw_CLI_Map.md` (human-readable companion, 591 lines, with §Stage 2 design intuition).
- **Stage 2 step 1 DONE.** `skills.load.extraDirs` patched into `~/.openclaw/openclaw.json` registering `project-prime/skills/` with watcher on. **Do NOT re-apply.** Verify with `openclaw config get skills.load`.
- **Architectural decisions banked:**
  - Wrapper-internal chaining (1 exec call per skill turn, NOT agent-orchestrated sub-steps) — see [[openclaw-canonical-paths]] §6 latency analysis + `OpenClaw_CLI_Map.md` §Stage 2 design intuition.
  - Max 3 OpenClaw agents total (main + future planner + future recovery), NOT a 22-agent swarm — see memory `multi_agent_scope`.
  - 4 upstream patterns to adopt: iterative-one-sub-task-at-a-time planning (Stage 7); dry-run-before-submit (Stage 4); `${ENV_VAR}` + envsubst injection (wrappers that generate input files); validate SKILL.md against upstream `.schema/skill-frontmatter.schema.json`.
- **What's NOT done** (deferred):
  - Stage 0 cleanup: gateway token rotation, plaintext-secrets migration, plugin allowlist hygiene. Non-blocking.

## The prompt to paste

```
Continuation of Phase 3 — OpenClaw Day 4. Day 3 cleared Stage 1 (substrate
verification 3/3 PASS) + deep-doc-read + Stage 2 step 1 applied (skills.load.extraDirs
patched).

Today's work: Stage 2 (Skill_Antechamber_LigandPrep) per Phase3_Taskboard_Manifest.

Read these vault notes + memories BEFORE acting (in this order):

- memory: openclaw-canonical-paths (CRITICAL — 16 sections, load-bearing CLI/runtime
  facts including SKILL.md authoring §8 and skill loading §9)
- memory: project-prime-status, openclaw-install-state, openclaw-vertex-gap,
  upstream-chemistry-skills-library, phase3-advisor-demo, amber26-pdf-section-map,
  multi-agent-scope
- vault: Dev_Log.md (2026-06-03 entries on top — there are TWO, original + cont.),
  Phase3_Taskboard_Manifest.md (Stage 2 section), OpenClaw_CLI_Map.md (§SKILL.md
  authoring + §Skill loading + §Stage 2 design intuition), Actionable_Recommendations.md
  (§1 BUILD/INTEGRATE/ADOPT triage), Skill_Antechamber_LigandPrep.md (existing vault
  sketch — supersedes when Stage 2 lands)

Immediate sequence (Stage 2 — DO NOT extend scope to Stage 3+):

1. PRE-FLIGHT — confirm Day 3 state still holds (5 min):
   a. openclaw gateway status (running, write-capable)
   b. openclaw config get skills.load (should return extraDirs + watch + debounce)
   c. openclaw models status | grep cooldown (should NOT show cooldown)
   d. ls project-prime/skills/ (should exist, empty — ready to scaffold)
   e. ls upstream-reference/computational-chemistry-agent-skills/molecular-dynamics/antechamber/
      (reference SKILL.md available for adaptation, LGPL-3.0)

2. SCAFFOLD project-prime/skills/antechamber-ligandprep/ (~60 min):
   - SKILL.md (single-line JSON metadata per OpenClaw embedded parser quirk;
     name: antechamber-ligandprep; quoted noun-phrase description; license MIT
     or LGPL-3.0-or-later if adapting upstream prose;
     metadata: { "openclaw": { "requires": { "bins": ["antechamber", "parmchk2",
     "obabel", "pdb4amber"], "env": ["AMBERHOME"] }, "os": ["darwin"] } };
     goal-oriented body — describe what user can achieve, NOT how to sequence
     tool calls; use {baseDir}/scripts/wrapper.py to reference wrapper)
   - scripts/wrapper.py (deterministic Python; accepts input file path / output
     dir / optional res-name / optional net-charge; runs obabel → antechamber
     -c bcc -at gaff2 → parmchk2 -s gaff2 internally; validates outputs;
     supports --dry-run flag per upstream dpdisp-submit pattern; returns ONE
     JSON envelope: {success, outputs: {mol2, frcmod}, atom_types, net_charge,
     errors}; system-agnostic — no hardcoded "benzene"/"181L"/specific atom counts)
   - references/ (adapted antechamber heuristics from upstream SKILL.md with
     LGPL-3.0 attribution + link to source)
   - test_acceptance.sh (3 cases: golden-path benzene from PDB 181L,
     an unrelated test ligand like methane, and a malformed PDB to exercise the
     wrapper's error path; assert success=true for first two, success=false
     with parseable errors for third)

3. VERIFY substrate integration (~15 min):
   - openclaw skills list | grep antechamber-ligandprep → shows ready (watcher
     should auto-pick up; if not, gateway restart)
   - openclaw skills info antechamber-ligandprep → shows correct metadata
   - One real agent turn with goal-oriented prompt: "Prepare benzene
     (`{baseDir-equivalent path to test PDB}`) for AMBER MD." Verify
     toolSummary.calls=1 (single exec call to wrapper, NOT 3 separate calls)
     and final reply references real wrapper output.

4. LOG + flip manifest status (~10 min):
   - Append Dev_Log entry (or 2026-06-04 if rolled over) — what was scaffolded,
     what acceptance test verified, what surprised.
   - Edit Phase3_Taskboard_Manifest.md Stage 2 status PENDING → COMPLETE with
     pointer to skill dir + test transcript.
   - STOP. Stage 3 (tleap-build) is for a separate session.

Hard constraints (from project memory — do not violate):

- All real inference goes through `--gateway`. `--local` needs catalog
  duplication and is not the canonical path. See [[openclaw-canonical-paths]] §3.
- LLM is BARRED from deterministic execution. Skills are Python/shell wrappers
  invoked from a SKILL.md instruction block — NOT LLM-constructed CLI calls.
- SKILL.md prose must describe GOALS, not tool-call topology (explicit
  topology directives stall Flash at 120s idle). See [[openclaw-canonical-paths]] §6.
- `metadata` MUST be single-line JSON in SKILL.md frontmatter. See [[openclaw-canonical-paths]] §8.
- Physical realism non-negotiable (dt ≤ 2fs, etc.).
- Bounded recovery only; never freeform fixes. (Stage 8 concern, not Stage 2.)
- Runnable code lives in /Users/kevinzhou/Downloads/Single Particle/project-prime/skills/,
  NOT in the vault.
- Upstream reference at /Users/kevinzhou/Downloads/Single Particle/upstream-reference/
  is LGPL-3.0 — adapt instruction text and parameter heuristics into our own
  skills, but do NOT depend on the package at runtime; acknowledge adapted text.
- Don't paste raw ~/.openclaw/openclaw.json into chat. Use `openclaw config get <path>`.
- Skill design = wrapper-internal chaining (one exec call per skill turn) per
  Day 3 latency findings.

Plan first per Phase3_Taskboard_Manifest before any execution. Stage 2 acceptance
test (golden-path benzene + unrelated ligand + malformed input) must pass before
manifest flips to COMPLETE.
```

## Likely friction points (forewarned)

- **`{baseDir}` substitution** in SKILL.md body — substituted at runtime to the skill folder absolute path. If wrapper.py needs a path relative to itself (not skill root), use Python's `os.path.dirname(__file__)` inside the script.
- **Single-line JSON `metadata` quirk** — easy to write multi-line YAML out of habit. The upstream antechamber SKILL.md uses multi-line YAML. Use single-line JSON for our skills (OpenClaw embedded parser preference; vault note `OpenClaw_CLI_Map.md` §SKILL.md authoring explains why).
- **`obabel` may not be in `AmberTools`** — `obabel` is OpenBabel, separate package. Check `which obabel` in `prime-amber` conda env. If absent: `conda install -c conda-forge openbabel` or use antechamber's `-fi pdb` directly without obabel preprocessing for PDB inputs.
- **antechamber sqm failure on rings + halogens** — known failure mode flagged in vault Skill_Antechamber_LigandPrep sketch. The wrapper should catch sqm exit non-zero + populate `errors[]` with the actual sqm output.
- **Watcher debounce timing** — `watchDebounceMs: 250` means rapid SKILL.md edits may batch. Wait ~1s after edit before `openclaw skills list` to verify.
- **PDB 181L might not be sitting in the project tree** — golden-path/ uses it; verify the path before the acceptance test rather than guessing.
- **Acceptance test should NOT depend on internet** — antechamber + parmchk2 + obabel are local; PDB 181L was already downloaded as part of golden-path setup; no network calls.

## Stage 0 cleanup still outstanding (low priority, non-blocking)

- Gateway token rotation: `openclaw doctor --generate-gateway-token` (loopback-only).
- Plaintext-secrets migration: `openclaw secrets configure` → `apply` → `audit --check`.
- Plugin allowlist hygiene: set `plugins.allow` to explicit trusted IDs.

## When Stage 2 lands

- Stage 3 (tleap-build) is next per Phase3_Taskboard_Manifest. Same template — wrapper-internal chain, goal-oriented SKILL.md, acceptance test against golden-path.
- Stages 4–6 follow the same Level 0/1 pattern (sander/pmemd, cpptraj, PLIP).
- Stage 7 (planner) moves to Level 2 — adopt the upstream's iterative-one-sub-task-at-a-time discipline + `llm-task` plugin for schema-validated stage emission.
- Stage 8 (bounded recovery) moves to Level 3 — Lobster workflow with approval gates for Tier 2 mutation.
