---
tags: [phase-3, openclaw, planning, manifest, execution-plan]
type: manifest
status: stage-2-built
created: 2026-06-01
---

# Phase 3 Taskboard Manifest — OpenClaw Substrate + First Skill

> **Status (2026-06-03):** Substrate install ✅, upstream reference cloned ✅, LLM auth ✅ (Day 2), Stage 1 substrate verification ✅ (Day 3 — 3/3 PASS, see [[Dev_Log]] 2026-06-03), skill authoring not yet started.
> 
> This note is the execution plan for Phase 3. Stages have explicit inputs, outputs, and validation conditions per the [[Arch_Taskboard_Manifest]] discipline — no stage proceeds without validation pass. The LLM is NOT in the loop for any of the deterministic validations below; all checks are bash/regex/file-existence/numeric-bound assertions.

---

## Architectural framing (do not re-litigate per session)

Three layers, only one of which is "the framework":

| Layer | Source | Status |
|---|---|---|
| **Substrate** (agent loop + skill loader + tools) | OpenClaw 2026.5.28 (Steinberger, npm) | INSTALLED |
| **Decomposition** (planning skill → domain skills → dispatcher skill) | Ding et al. 2026, arXiv:2603.25522 | Modeled, BUILD our own |
| **Recovery + verification** (Tier 1 checkpoint, Tier 2 bounded mutation) | Multisim + LOWE | ADOPTed disciplines, BUILD in our recovery skill |
| **Trust + guardrails** (4-label provenance, approval gates) | OpenBrain + Tippy | ADOPTed disciplines, enforced inside skill code |

OpenClaw is the substrate we run inside. The "framework" the report describes is our own composition of paper-decomposition + adopted disciplines. **"Lobster DAGs / llm-task / approval gates" are NOT OpenClaw primitives** ([[Actionable_Recommendations]] already labels approval gates as ADOPTED from Tippy); the vault's [[OpenClaw_Lobster_DAGs]] note overstates this and is correctly tier-flagged 🟡.

**Hard "lobster-like" discipline (the contribution):** our skills are *hardened deterministic wrappers* — the SKILL.md tells the agent which Python/shell script to invoke with what inputs; the script does the work and validates outputs; the LLM is *outside* the deterministic path. This contrasts with the upstream [[upstream-chemistry-skills-library]] model where SKILL.md is instruction text and the LLM constructs the CLI call.

---

## Stage 0 — LLM Auth Resolution (PREREQ for all downstream stages)

**Status:** PENDING (today's blocker).

**Inputs:**
- A regenerated AI Studio API key, generated against a NEW GCP project (keeps `single-XXXXXX` untouched since the $300 credit is excluded from AI Studio anyway — see [[gcp-credit-ai-studio-exclusion]]).
- Existing gcloud + ADC setup (works, but not used by OpenClaw given [[openclaw-vertex-gap]]).

**Approach (mandatory order):**
1. **Curl-verify the key BEFORE touching OpenClaw config.** Pattern (no shell-history exposure):
   ```bash
   read -s GEMINI_KEY
   curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_KEY" \
     | python3 -c "import json,sys; d=json.load(sys.stdin); print('ERROR:', d.get('error',{}).get('message','')) if 'error' in d else [print(m['name']) for m in d.get('models',[])[:10]]"
   unset GEMINI_KEY
   ```
2. Branch on curl result:
   - **Key returns model list** → real Gemini key, format issue from yesterday was cosmetic. Proceed to step 3.
   - **`API key not valid`** → key generated against wrong surface. Regenerate at [aistudio.google.com/apikey](https://aistudio.google.com/apikey), ensure prefix is `AIzaSy...`. Re-curl.
   - **`API has not been enabled`** → enable Generative Language API on the project at [console.cloud.google.com/apis/library/generativelanguage.googleapis.com](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com). Re-curl.
3. Wire into OpenClaw: `openclaw models auth paste-api-key --provider google` → paste key → `openclaw gateway restart`.
4. Verify default model alignment: `openclaw config get agents.defaults.model.primary` should be `google/gemini-2.5-flash` (set yesterday).

**Outputs:**
- AI Studio key validated against Google's API (curl test passes with model list returned).
- OpenClaw's auth-profiles.json contains a working `google` provider entry.
- `openclaw models status` shows no "Missing auth" warning.

**Validation conditions:**
- `openclaw agent --agent main --message 'Reply with ONLY this JSON: {"ack":true}' --json 2>&1 | grep -E '"ack":\s*true'` exits 0.
- Round-trip latency under 5 seconds (Flash should be fast).
- No `model_not_found` or auth-related error in stderr.

**Failure exits:**
- If after curl-verified key + paste-api-key + restart the smoke test still fails with `Unknown model` → escalate to: try `google/gemini-3-flash-preview` instead (catalog confirms it's registered); if that ALSO fails, OpenClaw's `google` plugin has a deeper issue and we pivot to `openclaw models auth login --provider google` (OAuth flow) as a last resort.

---

## Stage 1 — OpenClaw Substrate Verification

**Status:** ✅ COMPLETE 2026-06-03 (3/3 PASS — substrate verified usable for Stage 2). See [[Dev_Log]] 2026-06-03 entry; transcripts at `project-prime/runs/substrate-verification/`. Key findings: shell tool is named `exec` (not `bash`); `--json` trace surfaces tool-summary + final text only (not raw exec args/stdout); AI Studio auth-profile cooldown is per-provider (~60s) and blocks Pro fallback after a Flash idle-stream timeout; explicit "use N tool calls" instructions trigger Flash 120s idle stalls — SKILL.md should describe goals, not prescribe tool-call topology.

**Depends on:** Stage 0 complete.

**Inputs:** working `agent --message` call (Stage 0 output).

**Tasks:**
1. **JSON-structured LLM call** — confirm Gemini reliably returns valid JSON when prompted to. Run 3 calls with different schemas; all must parse.
2. **Bash tool execution** — confirm OpenClaw's agent can invoke the `bash` tool. Prompt: *"Use the bash tool to run `pwd` and return the output verbatim, nothing else."*
3. **Tool-chain** — confirm agent can sequence two tool calls: bash then JSON formatting. Prompt: *"Run `ls -la /tmp` via bash, then return a JSON object {dir:'/tmp', entry_count: <number>}."*

**Outputs:**
- Three documented agent-call transcripts (saved to `project-prime/runs/substrate-verification/`) showing JSON, bash, and chain working.
- Updated [[Dev_Log]] entry noting substrate is fully verified.

**Validation conditions:**
- All three transcripts pass; agent didn't hallucinate paths or fabricate command output.
- `pwd` output matches actual shell `pwd` (deterministic check).
- `ls -la /tmp` entry count from agent matches `ls -la /tmp | wc -l` (deterministic check).

---

## Stage 2 — Skill_Antechamber_LigandPrep (First Real Skill)

**Status:** BUILT 2026-06-04 (acceptance 3/3 PASS; substrate ✓ Ready, visible to model; live agent-turn verification deferred to Day 5 pre-flight check 1f due to upstream Google 503 outage on agent payload). See [[Dev_Log]] 2026-06-04 entry. Artifacts at `project-prime/skills/antechamber-ligandprep/` (4 git commits in `project-prime/`: `f2307db` → `29a99ce`). Will flip to COMPLETE once the live agent turn lands.

**Depends on:** Stage 1 complete + `prime-amber` conda env active.

**Inputs:**
- Upstream antechamber SKILL.md at `~/Downloads/Single Particle/upstream-reference/computational-chemistry-agent-skills/molecular-dynamics/antechamber/SKILL.md` (reference text — adapt heuristics + examples into our skill body).
- Golden-path Stage 2 recipe at `~/Downloads/Single Particle/project-prime/golden-path/` (acceptance test fixture — T4L L99A + benzene from PDB 181L).
- `.schema/skill-frontmatter.schema.json` from the upstream (frontmatter authority).
- Memory provenance discipline ([[Design_Memory_Provenance]]) — `observed` + `confirmed` only drive execution.

**Files to create:**
- `project-prime/skills/antechamber-ligandprep/SKILL.md` — frontmatter per upstream schema (`name`, `description`, `compatibility`, `license`, `metadata.openclaw.requires.{env: [AMBERHOME], bins: [antechamber, parmchk2, obabel, pdb4amber]}`); body adapted from upstream + explicit "INVOKE wrapper.py with these inputs" instruction block.
- `project-prime/skills/antechamber-ligandprep/wrapper.py` — deterministic Python that:
  - Accepts: input file path (PDB / SMILES / mol2), output directory, optional residue name, optional net charge.
  - Runs the chain: `obabel` (if input is SMILES) → `antechamber -c bcc -at gaff2` → `parmchk2 -s gaff2`.
  - Validates: output `.mol2` exists, has charge column populated, atom types are GAFF2-recognized; output `.frcmod` exists.
  - Returns JSON: `{success: bool, outputs: {mol2: path, frcmod: path}, atom_types: [...], net_charge: float, errors: []}`.
  - **System-agnostic** — no hardcoded "benzene", "181L", or specific atom counts. Same function works on any ligand.
- `project-prime/skills/antechamber-ligandprep/test_acceptance.sh` — runs wrapper.py against benzene from 181L (golden-path fixture) AND against an unrelated test ligand (e.g., methane from a fresh PDB), and asserts both succeed.

**Outputs:**
- A working SKILL.md/wrapper.py/test pair, committable to `project-prime/` git.
- Acceptance test passes for golden-path benzene AND for an unrelated ligand.
- Skill installed into OpenClaw via `openclaw skills add ./skills/antechamber-ligandprep -a main`; `openclaw skills list --eligible` shows it.

**Validation conditions:**
- `bash test_acceptance.sh` exits 0 for both ligands.
- Wrapper output `.mol2` is bit-for-bit identical to golden-path `ligand_gaff2.mol2` when run with the same inputs (the wrapper produces deterministic output for deterministic inputs).
- A small adversarial check: pass a malformed PDB (e.g., missing CONECT records) and confirm the wrapper returns `{success: false}` with a parseable error, NOT a silent failure.

**Failure exits:**
- If antechamber blows up on a non-standard ligand, the wrapper's error path is exercised; this is the seed of the [[Skill_Bounded_Recovery_AMBER]] integration (recovery skill would catch and retry with bounded parameter mutation). Out of Stage 2 scope; flag for Stage 6+.

---

## Stages 3–6 — Queued (not in this manifest's execution scope)

These are the remaining BUILD items per [[Actionable_Recommendations]] §1 and the remaining stages of the golden-path pipeline:

- **Stage 3 — Skill_Tleap_Build** — combine protein + ligand .frcmod into a solvated topology. Acceptance: golden-path Stage 3 outputs (`system.prmtop`, `system.inpcrd`).
- **Stage 4 — Skill_Sander_Run** — MD execution (minimize → heat → equilibrate → produce). Will likely use `tools/dpdisp-submit/SKILL.md` from upstream as DPDispatcher integration reference (local Shell+LocalContext mode). Acceptance: golden-path Stage 4 outputs (`*.nc`, `*.out` with no NaN, prod temp = 300 ± 2 K).
- **Stage 5 — Skill_Cpptraj_Analysis** — RMSD/RMSF/RoG extraction. Acceptance: golden-path Stage 5 outputs (`rmsd_backbone.dat`, `rmsf.dat`, ligand-RMSD).
- **Stage 6 — Skill_PLIP_Postprocess** — non-covalent interaction profiling. Acceptance: PLIP fingerprint matches golden-path PLIP output for 181L (6 hydrophobic contacts in the L99A cavity).
- **Stage 7 — Skill_Planning_Manifest** — the planner skill that orchestrates Stages 2–6 with validation gates between them. This is the [[Arch_Taskboard_Manifest]] in skill form.
- **Stage 8 — Skill_Bounded_Recovery_AMBER** — the differentiator. Tier 1 (checkpoint-restore) → Tier 2 (bounded parameter mutation: lower `dt`, disable SHAKE, etc.). Wraps Stage 4. Acceptance: deliberate failure injection (corrupt a frame, set bad `dt`) triggers correct recovery escalation.

Each later stage gets its own manifest entry when its turn comes; do not pre-author them speculatively.

---

## Open decisions deferred to manifest execution

- **OpenClaw `disable-model-invocation` vs custom "stop & ask" instruction block** as the approval-gate mechanism for the recovery skill's Tier 2 mutation step. Defer until Stage 8.
- **DPDispatcher (Shell+LocalContext) vs direct bash-tool invocation** for Stage 4. Upstream `dpdisp-submit` skill is a real reference; using DPDispatcher would future-proof the Scenario B (remote HPC) swap, but adds a dependency for local-only execution. Decide at Stage 4 start.
- **Whether to adopt the upstream's `agent-taskboard-manifest` skill wholesale** for Stage 7, OR build our own planning skill that matches the discipline overlay more strictly. The upstream's wraps a third-party spec (`light-cyan/AgentTaskboardManifest`) with human-review checkpoints; our discipline requires deterministic validation gates, not just human review. Likely build our own; revisit at Stage 7.

---

## Re-evaluation triggers (when to revisit this manifest)

- **New OpenClaw release** — re-check [[openclaw-vertex-gap]]. If a `google-vertex` provider plugin ships, pivot LLM auth back to Vertex and start drawing the $300 credit.
- **Stage 2 acceptance fails on the system-agnostic check** — the wrapper has a hidden hardcoding; refactor before Stage 3.
- **Advisor adds a new constraint** — escalate before changing the stage list.

---

**Source:** Drafted 2026-06-01 evening at the close of the OpenClaw install session. Consolidates findings from today's Dev_Log entry + [[Actionable_Recommendations]] §1 BUILD/INTEGRATE/ADOPT triage. Resume sequence in [[Next_Session_Prompt_OpenClaw_Day2]].
