---
tags: [phase-3, openclaw, planning, manifest, execution-plan]
type: manifest
status: "stages 3-8 built — full local pipeline + planner + recovery; only Gap_Remote_HPC_Backend open"
created: 2026-06-01
---

# Phase 3 Taskboard Manifest — OpenClaw Substrate + First Skill

> **Status (2026-06-08, Advisor task — `mdin-edit` parameter editor):** Built a NEW OpenClaw skill **`mdin-edit`** (`project-prime/skills/mdin-edit/`, ✓ ready) for the advisor's natural-language **parameter-EDITING** task over his pre-prepared `phase3-explicit-solvent-md/` mdin set — distinct from `amber-md-run` (which *generates*). The agent maps NL → `--stage/--param/--value`; the wrapper does an **idempotent, byte-minimal parse-replace** (numeric-token-only, never appends, re-run byte-identical), **bounds-checked** (`dt≤0.002`, `temp0≤400`, `restraint_wt≥0`, `nstlim>0`, `6≤cut≤12` with advisory WARN <8 so the advisor's `cut=7.0` passes; shared `check_amber.py` validator untouched), **stage-aware** (`group:third-onward`={heat-3,press-3,relax,prod}, `group:all`; refuses params not in a stage; `restraint_wt` skipped where `ntr=0`), with **`temp0`↔`&wt value2` coupling** that auto-fixes the heat-3 `temp0=300`/`value2=310` mismatch, an **atomic write + post-edit self-check** (independent parser), and a change log. Validation logic is **vendored** from `md-param-check` (self-contained). Deliverables: the Amber26 **§23.6** write-up (`references/mdin-params.md`, advisor Task 1) + an 11-case `test_acceptance.sh` (asserts file BYTES) all green (full + dry-run). Committed project-prime `fd5ae2b`. **Deferred (user-scoped):** `--submit` reduced-`nstlim` smoke + live `openclaw agent` NL drive. See [[Dev_Log]] 2026-06-08 (cont. 2) + the skill's SKILL.md.
> 
> **Status (2026-06-08, Day 8 — Discord orchestration + Stage-2 correctness fix):** **Phase B Discord small-task gate PASSED** — a user @-mention drove `antechamber-ligandprep` through the bot (free Cerebras `gpt-oss-120b`) → in-channel reply, $0 (the long-MD-vs-~120s-idle async path remains a deferred *build*). **Plus a silent bug caught + fixed during QC:** the 1L2Y indole ligand was being mis-typed as **non-aromatic** (`c2/c5/ce/cf/ne`, ring **N–H dropped**) because the PDB path ran `pdb4amber --nohyd` (strip H) → `obabel -p 7.4` (re-add H), forcing obabel to re-perceive bonds from a heavy-atom-only skeleton where it `Failed to kekulize aromatic bonds`; antechamber (fed the obabel mol2) trusted the broken bonds; **all four output gates passed → a silent failure** present identically in the overnight + happy-path runs, so the prior MM-GBSA ΔG (≈ −13) was computed on a mis-parameterized ligand. **Fix:** H-present PDBs now route straight to `antechamber -fi pdb -j 4` (antechamber's own perception kekulizes correctly, acdoctor kept ON); new **fatal** `AROMATIC_PERCEPTION_FAILED` gate on obabel kekulize failures; acceptance **Case 4** (indole) added as the regression guard the benzene-only fixture lacked. Corrected happy path (20 ps) GREEN: Stage-2 types `ca/cc/cd/h4/ha/hn/na` (NE1→na, HE1→hn restored), **MM-GBSA ΔG −17.18 kcal/mol** (closer to the article's ≈ −16). **Prior ΔG figures (−12.84 / −13.11 / −13.29) are SUPERSEDED — computed on the mis-typed ligand.** See [[Dev_Log]] 2026-06-08 + [[antechamber-aromatic-kekulize-bug]]. **Phase B async (2026-06-08 cont.):** built the `pipeline-async` skill (detached full-run launcher; agent replies "started" then the detached job posts per-stage progress + final ΔG via the LLM-free `openclaw message send`) + a manual-start 429 self-alert watcher (`scripts/watch_ratelimits.sh`). Dry-run-verified end-to-end (6/6 notifications, $0); live e2e is user-driven. Deferred: arbitrary-ligand parsing, always-on watcher LaunchAgent.
> 
> **Status (2026-06-07, Day 7 — Cerebras free provider):** Phase A now PROVEN on a FREE provider. Pivoted the agent to `cerebras/gpt-oss-120b` (Google free tier = ~1 agent turn/day; Cerebras free ≈ 1M tokens/day; OpenClaw natively supports `cerebras/*`). An overnight run drove the **full 4-skill pipeline end-to-end via the agent**: 12/12 analyses, **MM-GBSA ΔG −12.84 kcal/mol**, $0. Caveats: ~15-min turns brushed the 900s agent `--timeout` (raise it); back-to-back heavy turns can 120s-idle-stall (Cerebras 60k tok/min). Live-agent-turn gate (Day 6) **and** full multi-turn orchestration (Day 7) both ✅. ⚠️ user set `pmset disablesleep 1` overnight — must revert. Discord (Phase B) needs the user awake. See [[Dev_Log]] 2026-06-07.
> 
> **Status (2026-06-05, Day 6 — Evaluation):** EVALUATION pass complete. Happy path re-ran GREEN on 1L2Y (20 ps: 4/4 `ok:true`, 12 analyses, 15 PNGs, MM-GBSA ΔG −13.11). All 4 per-skill acceptance suites PASS (golden + unrelated + malformed; every malformed case fails *gracefully* — structured `ok:false`, not a crash). Deep output QC independently re-confirmed every baked-in correctness rule (comp_dry-before-solvateoct, heat `temp0`==`&wt value2`, dt=2fs+SHAKE, cut/Langevin, ntp=1/barostat=2/iwrap=1, PCA two-call, cluster repout); independent `check_amber.py` over the generated namelists → **VERDICT PASS**. Added a repeatable `/eval-happy-path` command (`.claude/commands/`). **Live-agent-turn gate still BLOCKED** by a sustained Google AI Studio 503 (3rd occurrence) — our side proven healthy (gateway routed `main`, both flash + pro returned 503); the bounded auto-retry (extended to 30 attempts / ~5 h) **EXHAUSTED at ~18:44 PT without flipping** — and the error shifted **503→429** partway (attempts 3–30 mostly `429 RESOURCE_EXHAUSTED`), so the **free-tier daily quota** is now the wall, not just Google capacity. Fix = enable AI Studio billing (paid tier) or drive one turn after the free-tier quota reset (~midnight Pacific). **✅ RESOLVED 2026-06-06 00:38 PT — GATE FLIPPED:** after the daily quota reset, one `openclaw agent --json` turn (run to measure token cost) drove antechamber-ligandprep as **exactly ONE exec call** (`toolSummary calls=1, failures=0`) → `LIG.mol2`+`LIG.frcmod`. The local AMBER MD pipeline is now verified end-to-end *as an agent*, not just via the harness. See [[Dev_Log]] 2026-06-05 (Day 6).
> 
> **Status (2026-06-05, Day 5 — Build):** Substrate ✅, LLM auth ✅, Stage 1 ✅, Stage 2 (antechamber-ligandprep) ✅, **Stages 3–5 BUILT ✅** (tleap-build, amber-md-run, cpptraj-analysis) — the full local AMBER MD happy path now runs end-to-end on 1L2Y via `project-prime/run_happy_path.sh` (antechamber → tleap → MD → 10-analysis suite + MM-GBSA). Each skill has a 3-case acceptance test passing. This replicates the baifan-wang amber-md happy path on our OpenClaw deterministic-wrapper architecture (see [[Research_amber_md_skill]]). Differentiators (PLIP, planner, bounded recovery, remote HPC) remain deferred. See [[Dev_Log]] 2026-06-05.
> 
> **Prior status (2026-06-03):** Substrate install ✅, upstream reference cloned ✅, LLM auth ✅ (Day 2), Stage 1 substrate verification ✅ (Day 3 — 3/3 PASS, see [[Dev_Log]] 2026-06-03), skill authoring not yet started.
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

**Status:** BUILT 2026-06-04 (acceptance 3/3 PASS; substrate ✓ Ready, visible to model; live agent-turn verification deferred to Day 5 pre-flight check 1f due to upstream Google 503 outage on agent payload). See [[Dev_Log]] 2026-06-04 entry. Artifacts at `project-prime/skills/antechamber-ligandprep/` (4 git commits in `project-prime/`: `f2307db` → `29a99ce`). Will flip to COMPLETE once the live agent turn lands. **Day 6 (2026-06-05):** live turn re-attempted via `openclaw agent --json` on the golden ligand — hit the *same* Google 503 on both flash + pro (gateway, auth, and skill-routing all proven healthy: the call reached Google and got a clean provider-side 503). Bounded auto-retry (`/tmp/live_turn_retry.sh`, extended to 30 attempts @10 min) ran ~5 h and **EXHAUSTED ~18:44 PT** — gate did not flip; error shifted 503→429 (free-tier quota now the wall). Flip when a turn lands after enabling AI Studio billing or the daily quota reset. **✅ FLIPPED 2026-06-06 00:38 PT** — after the next-day quota reset, one `openclaw agent --json` turn invoked the wrapper as a single exec call (`calls=1, failures=0`) and produced `LIG.mol2`+`LIG.frcmod`. **Stage 2 live-agent-turn = COMPLETE** (and by extension the wrapper-architecture pattern is proven live for all four skills).

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

## Stages 3–5 — BUILT 2026-06-05 (local happy path complete)

Built as deterministic-wrapper skills in `project-prime/skills/`, each with a
3-case acceptance test (golden + unrelated/subset + malformed) passing, and all
four chained green by `project-prime/run_happy_path.sh` on the 1L2Y fixture.

- **Stage 3 — `tleap-build`** ✅ — protein PDB + ligand (mol2+frcmod) → solvated
  neutralized topology. Generates a correct `leap.in` (saves `comp_dry` BEFORE
  `solvateoct` — fixing the upstream bug; saves `protein.top`/`ligand.top` for
  MM-GBSA). Validation: `leap.log` no ERROR, dry<solvated atoms, protein+ligand==dry
  combine invariant, neutral. 1L2Y: 306 dry / ~5986 solvated atoms.
- **Stage 4 — `amber-md-run`** (was "Skill_Sander_Run") ✅ — generates the 6-step
  chain (min1/2/3, heat, density, product), `md-param-check`-clean namelists,
  portable `run.sh`, runs to completion. **Engine seam** (Gap_Remote_HPC_Backend):
  serial `pmemd` default (~15.6 ns/day on this Mac), `pmemd.MPI`/`sander` opt-in;
  `--sim-ps` parameterizes production. DPDispatcher deferred (not needed for local;
  the seam is where it plugs in later).
- **Stage 5 — `cpptraj-analysis`** (was "Skill_Cpptraj_Analysis") ✅ — full
  10-analysis suite + free-energy landscape + MM-GBSA, each → .dat + .png. Fixes
  the upstream cpptraj footguns (two-call PCA, single-command clustering,
  hbond-empty-is-a-finding), auto-detects residue masks, strips with the SOLVATED
  topology. 1L2Y/indole MM-GBSA ΔG ≈ −14 kcal/mol (short run; article ≈ −16).

**See/do/verify:** `--dry-run` on any wrapper prints the generated inputs (SEE);
`run_happy_path.sh [sim_ps]` runs the chain (DO); per-skill `test_acceptance.sh` +
the harness assertions (4 ok:true envelopes, ≥12 analyses, ≥10 PNGs, ΔG<0) VERIFY.

## Parameter-editor skill — `mdin-edit` BUILT 2026-06-08 (advisor task)

A deterministic NL parameter-editor over the advisor's pre-prepared mdin set
(`phase3-explicit-solvent-md/`) — the EDITOR counterpart to the Stage-4 generator
`amber-md-run`. Skill at `project-prime/skills/mdin-edit/` (✓ ready), committed `fd5ae2b`.

- **Interface:** `--md-dir <copy> --stage <stage|group:third-onward|group:all> --param
  <dt|cut|temp0|restraint_wt|nstlim> --value <n> [--dry-run]`. Work on a COPY; the LLM
  parses NL, the wrapper does the edit.
- **Guarantees:** idempotent parse-replace (never appends; re-run byte-identical), bounds +
  stage-aware targeting (refuses absent params; `restraint_wt` skipped where `ntr=0`),
  `temp0`↔`&wt value2` coupling (fixes the heat-3 mismatch), all-or-nothing atomic write +
  post-edit self-check, change log. Validation logic vendored from `md-param-check`.
- **Tested:** `test_acceptance.sh` 11 cases asserting actual file bytes (golden, idempotency,
  out-of-bounds, no-append, the 3 advisor extensions, ntr=0 skip/fail, malformed) — all green
  full + dry-run.
- **Deliverables:** §23.6 write-up (`references/mdin-params.md`, Task 1); guarantees summary in
  SKILL.md (Task 4).
- **Deferred (user-scoped):** `--submit` (copy + `AMBERHOME` rewrite via `scripts/env.sh` +
  reduced-`nstlim` smoke) and the live `openclaw agent` NL drive.

## Stages 6–8 — all BUILT 2026-06-10

- **Stage 6 — `plip-profile`** ✅ BUILT 2026-06-10 — non-covalent interaction
  profiling (cpptraj medoid frame → resname-normalize → PLIP → 8-category
  envelope). Wired non-fatally into `run_happy_path.sh`. See [[Dev_Log]] 2026-06-10.
- **Stage 7 — `md-planner`** ✅ BUILT 2026-06-10 (project-prime `76e9fef`) —
  [[Arch_Taskboard_Manifest]] in skill form. The main agent maps a goal → a JSON
  **plan manifest** (selects/parameterizes/wires stages from the known catalog);
  the wrapper is a **pure deterministic** validator (G0–G6: known-catalog, DAG-
  acyclic, inputs-satisfied-vs-registry, imported `check_amber` bounds, typed
  params, unknown-param reject) + compiler (byte-inspectable plan) + executor
  (gates each transition, HALT on failure — recovery stays Stage 8's; calls the
  wrappers directly, never touches `run_happy_path.sh`). Validator oracle
  (py3.9+3.11), registry drift guard, real-pmemd acceptance + **LIVE full chain
  manifest-first** (ΔG −17.94), live NL-drive, adversarial-reviewed+fixed (crash-
  on-malformed, two false-negatives, dt-to-CLI, degraded signal). See [[Dev_Log]]
  2026-06-10 (cont. 2) + `references/plan-manifest.md` (🟡 our framing of plan-and-
  execute — cite Plan-and-Solve / LangGraph, NOT "Taskboard Manifest").
- **Stage 8 — `amber-recover`** ✅ BUILT 2026-06-10 (project-prime `8a1e849`) —
  the differentiator, the vault's strongest paper-cited element. Deterministic
  mdout crash detector → **Tier 1** checkpoint-restore as-is → **Tier 2** bounded
  SHAKE-off + tiny-dt stabilize-then-restore (every mutated namelist gated by
  vendored `check_amber`) → bounded **HALT** `needs_human`. Acts on the
  `MD_CRASH[stage]` seam via the opt-in `scripts/recover_hook.sh` in
  `run_happy_path.sh` (guarded, non-fatal). Acceptance 7/7 real pmemd + detector
  oracle (py3.9+3.11) + live NL-drive byte-verified + adversarial review
  (PASS-WITH-CONCERNS → fixed Infinity silent-pass + original-namelist bounds gate
  → PASS). See [[Dev_Log]] 2026-06-10 + [[Skill_Bounded_Recovery_AMBER]].

Also deferred: **Discord orchestration** of the happy path (Phase B — bot is live;
the long-MD-vs-120s-idle wrinkle is the only open design point), and the
**memsearch / mempalace** semantic-memory spike (see [[Research_amber_md_skill]]
deferred note). Each later stage gets its own manifest entry when its turn comes.

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
