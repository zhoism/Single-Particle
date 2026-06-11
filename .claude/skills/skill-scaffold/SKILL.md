---
name: skill-scaffold
description: Use to create a new OpenClaw chemistry-pipeline skill directory at ~/Downloads/Single Particle/project-prime/skills/<name>/. Triggers on "scaffold a skill for X", "new skill", "create the antechamber skill", or when starting any Stage 2+ entry from Phase3_Taskboard_Manifest. Produces SKILL.md (single-line JSON metadata), scripts/wrapper.py (with --dry-run + JSON envelope), references/heuristics.md, and test_acceptance.sh (golden + unrelated + malformed). Registered via the existing extraDirs config.
---

# skill-scaffold — new OpenClaw chemistry skill

Project convention from `Phase3_Taskboard_Manifest.md` and the 2026-06-03 architectural call: **wrapper does the work, SKILL.md describes the goal.** Every Stage 2+ skill follows the same scaffold; this skill stamps it out and pre-populates the load-bearing constraints.

## When to invoke

- User says "scaffold a skill for X" / "new skill" / "create the X skill."
- Starting any Stage 2+ entry from `Phase3_Taskboard_Manifest.md` (antechamber-ligandprep, tleap-combine, sander-pmemd-wrapper, cpptraj-analyze, plip-fingerprint, recovery).
- The user has a chemistry binary chain (e.g., `obabel → antechamber → parmchk2`) and wants it wrapped as a single OpenClaw skill.

## Hard rules (the gotchas you will hit otherwise)

1. **SKILL.md `metadata` field MUST be single-line JSON.** OpenClaw 2026.5.28's embedded YAML/JSON parser does NOT accept multi-line metadata blocks despite the upstream schema allowing them. Single-line. Validated empirically on 2026-06-03. See `openclaw_canonical_paths` memory.
2. **One `exec` call per skill turn.** From Stage 1c latency finding: every inter-agent call ≈ 100s on Flash. Multi-call chains hit the 120s idle timeout. Wrapper-internal Python chaining is the architecture; SKILL.md describes the goal, NOT the tool-call topology.
3. **Description is goal-oriented, NOT prescriptive.** Strict prompts like "use N tool calls" trigger Flash idle-stalls. Write "Prepare a ligand for AMBER MD given a SMILES or PDB input," not "Run obabel, then antechamber, then parmchk2."
4. **`--dry-run` is mandatory.** From upstream `dpdisp-submit` pattern + Stage 8 recovery design: wrapper must support `--dry-run` that emits the planned commands + computed paths WITHOUT executing. This is the validation gate for Tier 2 recovery.
5. **JSON envelope output.** stdout is `{ok: bool, stage: str, outputs: {...}, errors: [...], dry_run: bool}`. stderr is human-readable progress. This makes the wrapper agent-friendly without changing it for human use.
6. **`exec` not `bash`.** Reference the tool as `exec` in any prose. Stage 1b verified.
7. **Skills dir is registered.** `~/.openclaw/openclaw.json` has `skills.load.extraDirs` including `/Users/kevinzhou/Downloads/Single Particle/project-prime/skills` with `watch: true`. New SKILL.md is picked up without restart. Do NOT re-apply the extraDirs patch — it's persisted from 2026-06-03.
8. **LGPL-3.0 attribution when borrowing from upstream.** Heuristics text adapted from `~/Downloads/Single Particle/upstream-reference/computational-chemistry-agent-skills/` must cite source path + LGPL-3.0 in the references file.

## Procedure

**Step 0 — Read context:**
- `Phase3_Taskboard_Manifest.md` for the stage's acceptance criteria.
- `templates/skill/` for the four template files.
- `scripts/scaffold.sh` — the actual scaffolder.
- If the skill mirrors an upstream skill (most do): `~/Downloads/Single Particle/upstream-reference/computational-chemistry-agent-skills/<corresponding-path>/SKILL.md` for heuristics to adapt.

**Step 1 — Confirm the skill spec with the user.** Before scaffolding:
- Skill kebab-name (e.g., `antechamber-ligandprep`).
- Required binaries (e.g., `antechamber`, `parmchk2`, `obabel`, `pdb4amber`).
- Input contract (e.g., `--input` is a SMILES string OR a PDB file path; `--name` is the residue name).
- Output contract (e.g., emits `.mol2`, `.frcmod`, `.lib`).
- Manifest stage number it implements.

**Step 2 — Run `scripts/scaffold.sh <skill-name>`.** This:
- Creates `/Users/kevinzhou/Downloads/Single Particle/project-prime/skills/<name>/` with `scripts/`, `references/`, and the four files.
- Stamps `<name>` and today's date into the templates.
- Stops before populating skill-specific content — that's Step 3.

**Step 3 — Populate skill-specific content.** Fill in:
- **SKILL.md**: the single-line JSON `metadata` (`requires.bins`, `inputs`, `outputs`, `validation`), goal-oriented `description`, and an `Inputs/Outputs/Errors` section in the body.
- **scripts/wrapper.py**: the chain of subprocess calls with strict error handling, `--dry-run` support, JSON envelope on stdout.
- **references/heuristics.md**: parameter heuristics adapted from upstream (cite source + LGPL-3.0).
- **test_acceptance.sh**: 3 test cases — **golden** (known-good input from `phase3-advisor-demo` or smoke-test), **unrelated** (a different valid ligand to confirm scalability), **malformed** (invalid input to confirm graceful failure).

**Step 4 — Validate before commit.** Run:
- `scripts/validate-skill.sh <skill-name>` — checks SKILL.md frontmatter is single-line JSON-parseable, `requires.bins` are on PATH, wrapper.py is executable.
- `bash <skill-dir>/test_acceptance.sh --dry-run` — confirms the wrapper plan resolves without executing.
- `bash <skill-dir>/test_acceptance.sh` — full run; all three cases pass.

**Step 5 — Update manifest + log.** Flip the manifest stage from PENDING to BUILT (not COMPLETE — COMPLETE is after the OpenClaw agent successfully invokes it). Write a Dev_Log entry via `devlog-append` skill.

## Anti-patterns

- Do NOT use multi-line YAML for `metadata`. It parses on first read in your editor and silently fails to load in OpenClaw. The skill will appear missing.
- Do NOT prescribe tool-call topology in `description`. "Use 3 tool calls" → Flash idle-stall → skill never completes.
- Do NOT skip `--dry-run`. Tier 2 recovery in Stage 8 will need to call this on every wrapper to plan-without-mutating.
- Do NOT inline heuristics from upstream without LGPL-3.0 attribution + source path. The boundary is "borrow text, don't depend on package."
- Do NOT hardcode paths from `phase3-advisor-demo/submit.sh` (`/Application/software/Amber26/...`). That's the advisor's machine. Resolve binaries from PATH or `$AMBERHOME`. See `phase3_advisor_demo` memory.
- Do NOT re-apply the `extraDirs` config patch. It's persisted in `~/.openclaw/openclaw.json` from 2026-06-03.
- Do NOT commit `runs/` directories — they're gitignored. SKILL.md, wrapper.py, references/, test_acceptance.sh, and golden-path inputs ARE committed.

## Cross-references

- `Phase3_Taskboard_Manifest.md` — stage acceptance criteria, the load-bearing source.
- Memory `openclaw_canonical_paths` — single-line JSON metadata, `exec`-not-`bash`, gateway routing, cooldown gotchas.
- Memory `upstream_chemistry_skills_library` — upstream path + LGPL-3.0 + attribution rule.
- Memory `phase3_advisor_demo` — canonical 11-stage recipe, AMBERHOME pitfall, heat-3 inconsistency.
- Vault `OpenClaw_CLI_Map.md` §Stage 2 design intuition — the wrapper-internal-chaining rationale.
- Vault `Design_Skill_Decomposition.md` — atomic vs composite skills.
- Upstream reference: `~/Downloads/Single Particle/upstream-reference/computational-chemistry-agent-skills/molecular-dynamics/antechamber/SKILL.md` — the closest archetype for Stage 2.
