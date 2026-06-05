---
tags: [project-prime, openclaw, session-handoff, day-4, skills]
type: handoff
status: consumed
created: 2026-06-03
updated: 2026-06-04
consumed: 2026-06-04
---

## Outcome

Consumed 2026-06-04 across two sessions (paused mid-acceptance, resumed in a fresh chat). Stage 2 `antechamber-ligandprep` skill built, committed across 4 `project-prime/` git commits (`f2307db` baseline → `29a99ce` final), acceptance 3/3 PASS, substrate ✓ Ready. Live agent-turn verification deferred to Day 5 pre-flight 1f due to upstream Google 503 outage on the agent payload (direct inference worked throughout). Three design decisions banked (5e-3 charge tolerance, drop openclaw.requires.bins, dry-run Case 3 skip) — see [[Dev_Log]] 2026-06-04. Continuation in [[Next_Session_Prompt_OpenClaw_Day5]].


# Next Session Starter — OpenClaw Phase Day 4

> **🛑 PAUSED MID-SESSION 2026-06-04 — fresh-chat handoff log.** A Day 4 attempt ran through pre-flight + scaffold + populate + validate + acceptance dry-run, then halted at the acceptance-test full-execution step on a Case 3 (malformed) failure. The state below is what's on disk; resume by reading this section FIRST, then continuing from "Resume point" below. Do NOT re-run pre-flight, scaffold, or populate — those are persisted on disk.

## Session log (what landed on disk before pause)

**Pre-flight (Step 1) — DONE, all 5 checks PASS:**
- Gateway running (pid 86638), write-capable, loopback 127.0.0.1:18789, version 2026.5.28. Cosmetic nvm-Node warnings ignored per [[openclaw-canonical-paths]].
- `openclaw config get skills.load` returns `extraDirs: [/Users/kevinzhou/Downloads/Single Particle/project-prime/skills], watch: true, watchDebounceMs: 250` — Day 3 patch persisted.
- `openclaw models status` shows no cooldown; default `google/gemini-3-flash-preview`, fallback `google/gemini-3.1-pro-preview`, `api_key=1` for google profile `google:manual=AQ.Ab8RN...b6d8yOGg`.
- `project-prime/skills/` exists, only `.gitkeep` present at start.
- Upstream antechamber SKILL.md available at `~/Downloads/Single Particle/upstream-reference/computational-chemistry-agent-skills/molecular-dynamics/antechamber/SKILL.md`.
- All required bins (`antechamber`, `parmchk2`, `obabel`, `pdb4amber`, `tleap`) resolve to `/opt/homebrew/Caskroom/miniforge/base/envs/prime-amber/bin/` in the working shell. `AMBERHOME=/opt/homebrew/Caskroom/miniforge/base/envs/prime-amber`.

**Scaffold (Step 2) — DONE.** Ran `.claude/skills/skill-scaffold/scripts/scaffold.sh antechamber-ligandprep`. Created `/Users/kevinzhou/Downloads/Single Particle/project-prime/skills/antechamber-ligandprep/` with `SKILL.md`, `scripts/wrapper.py`, `references/heuristics.md`, `test_acceptance.sh`. All four files were then POPULATED (template stubs replaced with antechamber-specific content):

- **`SKILL.md`** — single-line JSON `metadata` containing BOTH `openclaw.requires.{bins,env}` (for OpenClaw's loader gating) AND flat `requires.{bins,env}` (for the project's validate-skill.sh which grep-extracts flat). Bins: `[antechamber, parmchk2, obabel, pdb4amber]`. Env: `[AMBERHOME]`. OS: `[darwin]`. Description is goal-oriented (no tool-call topology). Body documents inputs/outputs/validation gates/errors/how-it-works/acceptance.
- **`scripts/wrapper.py`** — full pipeline. Resolves bins via `shutil.which` then `$AMBERHOME/bin` fallback (never hardcoded). Classifies input as `pdb` / `mol2` / `sdf` / `smiles` by existence + extension; SMILES is the fallback when input is not an existing file. Chain: PDB→`pdb4amber --nohyd`→`obabel -p 7.4 .mol2`→`antechamber -c bcc -at gaff2 -rn <NAME> -nc <CHARGE> -pf y`→`parmchk2 -s gaff2`. SMILES skips pdb4amber, uses `obabel -:<smiles> --gen3d -p 7.4` instead. mol2 passes through. Each step streams stdout/stderr to `<run_dir>/NN_label.{out,err}`. `--dry-run` plans without executing. Validation gates: mol2 charge column populated, no `du` atom types, no `ATTN` lines in frcmod, `|charge_sum − requested| ≤ 1e-3`. Errors return JSON envelope with `ok: false` and a coded reason (`MISSING_BINARY` / `MISSING_ENV` / `INVALID_INPUT` / `INPUT_PREP_FAILED` / `SQM_CONVERGENCE_FAILED` / `MISSING_PARAMETERS` / `NET_CHARGE_MISMATCH`). `classify_step_failure()` reads `sqm.out` / `antechamber.log` to upgrade antechamber failures to `SQM_CONVERGENCE_FAILED` when appropriate.
- **`references/heuristics.md`** — LGPL-3.0-or-later attribution to upstream `molecular-dynamics/antechamber/SKILL.md`. Sections: why-this-file-exists, 5 heuristics (`-c bcc`, `-at gaff2`, `-nc` discipline, pdb4amber prefix, obabel `-p 7.4`), 5 anti-heuristics (no GAFF1, no `-dr n`, no RESP without ESP grid, no `AMBERHOME` hardcoding, no multi-line YAML metadata), 4 recurring-failure rows.
- **`test_acceptance.sh`** — 3 cases. Case 1 golden: `project-prime/golden-path/ligand_raw.pdb` (benzene BNZ extracted from PDB 181L, validated 2026-05-21), `--name BNZ --charge 0`, asserts `ok: true` AND atom types include `ca`+`ha`. Case 2 unrelated: `--input C` (methane SMILES), `--name MTH --charge 0`, asserts `ok: true` AND atom types include `c3`+`hc`. Case 3 malformed: writes a junk PDB with `HETATM XXXX...` garbage to `malformed.pdb`, asserts `ok: false` with non-empty `errors[]`. Two heredoc bugs in the extra-type-check helpers (quoted `<<'PY'` with broken `"'"$VAR"'"` escapes) were FIXED to use argv passing — see edits in the file.

**Validation (Step 4a) — DONE, all hard checks PASS.** `.claude/skills/skill-scaffold/scripts/validate-skill.sh antechamber-ligandprep` reports: SKILL.md exists, metadata is single-line JSON, wrapper.py executable, wrapper supports `--dry-run`, test_acceptance.sh executable, heuristics.md cites LGPL-3.0, description goal-oriented (no prescriptive topology detected). WARNs on bins-not-on-PATH because validate runs in a stripped non-interactive shell — wrapper's `$AMBERHOME/bin` fallback handles this at runtime. No hard failures.

**Acceptance --dry-run (Step 4b) — Cases 1 + 2 PASS, Case 3 FAIL.** Output shows planned command chains for golden (4 steps: pdb4amber → obabel → antechamber → parmchk2) and unrelated (3 steps: obabel-smiles → antechamber → parmchk2). Golden + Unrelated `ok: true` as expected for dry-run. **Case 3 (Malformed) returned `ok: True, errors: []` in dry-run mode** — the malformed-PDB envelope was a "successful plan" because dry-run never executes pdb4amber/obabel, so the malformed content is never parsed. test_acceptance.sh's assertion expected `ok: false` for Case 3 even in dry-run, so the assertion failed. **THIS IS THE PAUSE POINT.**

## Resume point — what the fresh session needs to decide + do

The Case 3 dry-run failure is a real design question, not a bug to silently fix:

**Option A — accept the dry-run/full-run split.** Case 3's contract is "fail gracefully when input is malformed," which is meaningful only when the chain actually executes. Skip Case 3 in dry-run mode (test_acceptance.sh checks `[[ -z "$DRY_RUN" ]]` and bypasses the malformed assertion). Then `test_acceptance.sh --dry-run` proves the command plans resolve; `test_acceptance.sh` (no flag) proves the chain works AND fails-gracefully on garbage. This is the cleaner separation of concerns.

**Option B — have the wrapper validate input in dry-run.** Add a `--dry-run` step that runs cheap syntactic checks (PDB has `HETATM`/`ATOM` records with valid column widths; SMILES parses via obabel `--gen3d off` or similar) BEFORE returning the planned envelope. More work, but Case 3 then tests both modes uniformly.

**Recommendation: Option A.** Keep the wrapper minimal. Update test_acceptance.sh to skip the Case 3 assertion under `--dry-run` (the case still emits its planned envelope; the assertion just doesn't fire). Then re-run `test_acceptance.sh --dry-run` (expect all 3 PASS), then run the full `test_acceptance.sh` (expect Cases 1+2 ok=true with the type checks, Case 3 ok=false with parseable errors).

After acceptance passes:

**Step 5 — Verify substrate integration (~15 min)** (Step 3 of the original prompt):
- `openclaw skills list | grep antechamber-ligandprep` — should appear (watcher should auto-pick up via `extraDirs`; if not, `openclaw gateway restart`).
- `openclaw skills info antechamber-ligandprep` — should show correct metadata.
- One real agent turn with goal-oriented prompt: "Prepare benzene (`/Users/kevinzhou/Downloads/Single Particle/project-prime/golden-path/ligand_raw.pdb`) for AMBER MD." Verify `toolSummary.calls=1` (single exec call to wrapper) and the final reply references real wrapper output. **CAUTION:** the OpenClaw gateway's LaunchAgent environment may NOT have `AMBERHOME` set or the conda env's bin on PATH — the wrapper's `metadata.openclaw.requires.env: [AMBERHOME]` gating may filter the skill out at load time. Diagnosis order: (a) check whether the skill appears in `openclaw skills list`; (b) if missing, the gating filtered it — set `AMBERHOME` via `openclaw config set` under whatever exec-env-injection path the gateway exposes, or add `prime-amber`'s bin to `tools.exec.pathPrepend`; (c) if the skill loads but the wrapper fails with `MISSING_BINARY`, same fix path. See [[openclaw-canonical-paths]] §4 (env.PATH override is rejected for host exec; use `tools.exec.pathPrepend` instead).

**Step 6 — Log + flip manifest + Day 5 handoff (~10 min):**
- Invoke `devlog-append` skill. Entry type = "substantial." Cover: scaffold landed; SKILL.md/wrapper.py/heuristics/test populated; validate passed; acceptance dry-run found Case 3 design question, resolved via Option A; full acceptance passed (assuming it does after fix); first real use of `skill-scaffold` + `devlog-append` skills. Date: 2026-06-04 (or whatever today is in the fresh session).
- Edit `Phase3_Taskboard_Manifest.md` Stage 2: PENDING → COMPLETE with pointer to `project-prime/skills/antechamber-ligandprep/` + test-runs transcript.
- Invoke `next-session-prompt` skill to draft `Next_Session_Prompt_OpenClaw_Day5.md` for Stage 3 (tleap-build).
- Flip THIS file's frontmatter `status: in-progress-paused` → `status: consumed` with a one-line outcome footer.
- STOP. Stage 3 (tleap-build) is for the Day 5 session.

## Open items the paused session did NOT resolve

- **Case 3 dry-run design call** — pick Option A or B above. (Recommendation: A.)
- **OpenClaw gateway env** — whether the substrate sees `AMBERHOME` + the conda env's bin. Will surface in Step 5; have the `tools.exec.pathPrepend` patch ready as the likely fix.
- **Metadata shape** — the populated SKILL.md uses BOTH `metadata.openclaw.requires.*` AND flat `metadata.requires.*` (single-line JSON). This was a belt-and-suspenders call to satisfy both OpenClaw's loader gating AND the project's validate-skill.sh. If the fresh session decides one is canonical, drop the other.

## Files touched this session (for git status orientation)

Created (untracked, ready to commit after acceptance passes):
- `project-prime/skills/antechamber-ligandprep/SKILL.md`
- `project-prime/skills/antechamber-ligandprep/scripts/wrapper.py`
- `project-prime/skills/antechamber-ligandprep/references/heuristics.md`
- `project-prime/skills/antechamber-ligandprep/test_acceptance.sh`
- `project-prime/skills/antechamber-ligandprep/test-runs/` (gitignored — acceptance scratch)

Modified:
- `Single Particle/Next_Session_Prompt_OpenClaw_Day4.md` (this file — added the resume log you're reading).

No memory writes this session. No vault note creations. No manifest edits yet. No Dev_Log entry yet.

---



> Created 2026-06-03 (late) at end of Day 3. Day 3 cleared Stage 1 (substrate verification 3/3 PASS), deep-read OpenClaw primary docs, re-assessed upstream library, articulated the 5-level scaling architecture, and applied Stage 2 step 1 (`skills.load.extraDirs` patched). Day 4 starts at Stage 2 of `Phase3_Taskboard_Manifest.md`. Paste the code block into a fresh Claude Code session (run from the vault).
>
> **Updated 2026-06-04:** seven Claude Code skills were built between Day 3 and Day 4 (project-scope at `.claude/skills/` + user-scope `memory-bank` at `~/.claude/skills/`). They auto-discover in the fresh session by frontmatter. **`skill-scaffold` is directly load-bearing for Step 2** — it scaffolds `antechamber-ligandprep/` with the load-bearing constraints (single-line JSON metadata, `--dry-run`, JSON envelope, LGPL-3.0 attribution) pre-stamped. **`devlog-append` is load-bearing for Step 4.** **`next-session-prompt` is load-bearing for the Day 5 handoff.** See §Claude Code skills available below.

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
  - Skills are built but NOT yet field-tested under invocation. First real use of `skill-scaffold` is Step 2 below; first real use of `devlog-append` is Step 4. If a skill misbehaves, fall through to the manual procedure (the SKILL.md body documents it) — don't get stuck.

## Claude Code skills available (built 2026-06-04)

Seven skills are now installed and should appear in the fresh session's available-skills system reminder. Invoke by name (`/<skill-name>`) or proactively when triggers match.

**Project scope — `.claude/skills/` (vault-tracked, will be in git):**

- **`skill-scaffold`** — **load-bearing for Step 2.** Creates a new OpenClaw skill directory at `project-prime/skills/<name>/` with SKILL.md (single-line JSON metadata), `scripts/wrapper.py` (with `--dry-run` + JSON envelope), `references/heuristics.md` (LGPL-3.0 attribution template), `test_acceptance.sh` (golden + unrelated + malformed). Includes `scaffold.sh` + `validate-skill.sh` scripts.
- **`devlog-append`** — **load-bearing for Step 4.** Append a Dev_Log entry in the project convention (reverse-chronological, marker + pointers, not duplicates). Has length-calibrated examples (marker / substantial / decision-banked).
- **`next-session-prompt`** — **load-bearing for the Day 5 handoff at end of session.** Generates the next `Next_Session_Prompt_*.md` with the decisions-banked / pre-flight / scope-fence structure this file uses.
- **`md-param-check`** — runs a working Python validator against AMBER `.in` files + submit scripts. Catches dt/cut/SHAKE violations, temp0/&wt mismatches (the heat-3 class), hardcoded foreign paths (the advisor `AMBERHOME` class). NOT load-bearing for Stage 2 (Stage 2 is ligand prep, not MD execution); will become load-bearing at Stage 4 (sander/pmemd wrapper).
- **`vault-note-new`** — creates typed vault notes (`Arch_*` / `Skill_*` / `Design_*` / `Gap_*` / `connections/*`) with correct frontmatter, prefix discipline, vocab check, tier badges. Fires only if Stage 2 produces something note-worthy beyond the skill itself.
- **`intake-verify`** — Gemini intake → matrix ROW / NO-row / scope-out decision for the Market Landscape report. NOT relevant to Stage 2 (report-side).

**User scope — `~/.claude/skills/`:**

- **`memory-bank`** — write/update auto-memory entries in the project-prime memory dir with file + MEMORY.md index discipline. Fires if Day 4 banks new decisions (e.g., a Stage 2 design call worth preserving across sessions).

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
- Claude Code skills (auto-discover from .claude/skills/ + ~/.claude/skills/; built
  2026-06-04): skill-scaffold (load-bearing for Step 2), devlog-append (load-bearing
  for Step 4), next-session-prompt (load-bearing for Day 5 handoff). Also available
  but not load-bearing for Stage 2: md-param-check, vault-note-new, memory-bank,
  intake-verify. Invoke the relevant SKILL.md body BEFORE the manual procedure;
  fall through to manual only if the skill misbehaves.

Immediate sequence (Stage 2 — DO NOT extend scope to Stage 3+):

1. PRE-FLIGHT — confirm Day 3 state still holds (5 min):
   a. openclaw gateway status (running, write-capable)
   b. openclaw config get skills.load (should return extraDirs + watch + debounce)
   c. openclaw models status | grep cooldown (should NOT show cooldown)
   d. ls project-prime/skills/ (should exist, empty — ready to scaffold)
   e. ls upstream-reference/computational-chemistry-agent-skills/molecular-dynamics/antechamber/
      (reference SKILL.md available for adaptation, LGPL-3.0)

2. SCAFFOLD project-prime/skills/antechamber-ligandprep/ (~60 min):
   - INVOKE the `skill-scaffold` Claude Code skill. It will run
     `.claude/skills/skill-scaffold/scripts/scaffold.sh antechamber-ligandprep`
     which creates the dir + 4 templated files with load-bearing constraints
     already in place (single-line JSON metadata, --dry-run, JSON envelope,
     LGPL-3.0 attribution template). The skill's SKILL.md documents the
     procedure if anything misbehaves; if the scaffolder fails for any reason,
     fall through to the manual file-by-file spec below.

   Then POPULATE the templated stubs with the antechamber-specific content:
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
   - references/heuristics.md (adapted antechamber heuristics from upstream
     SKILL.md with LGPL-3.0 attribution + link to source)
   - test_acceptance.sh (3 cases: golden-path benzene from PDB 181L,
     an unrelated test ligand like methane, and a malformed PDB to exercise the
     wrapper's error path; assert success=true for first two, success=false
     with parseable errors for third)

   Then VALIDATE:
   - `.claude/skills/skill-scaffold/scripts/validate-skill.sh antechamber-ligandprep`
     should report all PASS (single-line JSON metadata, wrapper executable,
     --dry-run supported, requires.bins on PATH, goal-oriented description).
   - `bash project-prime/skills/antechamber-ligandprep/test_acceptance.sh --dry-run`
     should succeed (plans without executing).
   - `bash project-prime/skills/antechamber-ligandprep/test_acceptance.sh` runs the
     full 3-case suite.

3. VERIFY substrate integration (~15 min):
   - openclaw skills list | grep antechamber-ligandprep → shows ready (watcher
     should auto-pick up; if not, gateway restart)
   - openclaw skills info antechamber-ligandprep → shows correct metadata
   - One real agent turn with goal-oriented prompt: "Prepare benzene
     (`{baseDir-equivalent path to test PDB}`) for AMBER MD." Verify
     toolSummary.calls=1 (single exec call to wrapper, NOT 3 separate calls)
     and final reply references real wrapper output.

4. LOG + flip manifest status (~10 min):
   - INVOKE the `devlog-append` Claude Code skill. It will append a Dev_Log
     entry in the project convention (reverse-chronological, marker + pointers,
     not duplicates). Entry type = "substantial" (multi-deliverable session
     with stage transition). Cover: what was scaffolded, what acceptance test
     verified, what surprised, the first real use of skill-scaffold +
     devlog-append themselves (if anything worth noting). Date: whatever today
     is in this session (likely 2026-06-04 or later).
   - Edit Phase3_Taskboard_Manifest.md Stage 2 status PENDING → COMPLETE with
     pointer to skill dir + test transcript.
   - INVOKE the `next-session-prompt` Claude Code skill to draft
     `Next_Session_Prompt_OpenClaw_Day5.md` for Stage 3 (tleap-build). Flip
     THIS file's frontmatter `status: ready` → `status: consumed` with a
     one-line outcome footer. The new Day 5 starter inherits the don't-re-do
     list + adds whatever Stage 2 banked.
   - STOP. Stage 3 (tleap-build) is for the Day 5 session.

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
