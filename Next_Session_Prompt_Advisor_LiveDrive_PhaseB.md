---
tags: [project-prime, openclaw, session-handoff, advisor-task, mdin-edit, phase-b, discord]
type: handoff
status: consumed
created: 2026-06-09
---

# Next Session Starter — Advisor mdin-edit tail (live NL drive + `--submit`) + Phase B full-pipeline-from-Discord

> Created 2026-06-09. Two tracks, decided with the user this session:
> **Track 1 (autonomous, do first):** finish the advisor's `mdin-edit` task — the live `openclaw agent` NL drive + the `--submit` feature.
> **Track 2 (needs the user present + a PAID Google API key the user is about to add):** drive the **full pipeline from Discord** end-to-end (the `pipeline-async` skill is built + dry-run-verified; the live e2e was previously blocked by the free-tier multi-turn ceiling — the paid key removes that).
> Paste the §The prompt to paste block into a fresh Claude Code session, run from the vault.

---

## 0. Read FIRST (orientation — do before acting)

- **memory `project-prime-status`** — CRITICAL. Current state, the ΔG retraction, Phase A/B status, the mdin-edit build + overnight testing result.
- **memory `openclaw-canonical-paths`** — load-bearing OpenClaw facts (exec not bash; `--gateway`; `message send` is LLM-free; 120s idle timeout; SKILL.md single-line JSON metadata; failover cooldowns).
- **memory `antechamber-aromatic-kekulize-bug`** — don't cite old ΔG; never `--nohyd` a ligand.
- **vault `Dev_Log.md`** — top 3 entries (2026-06-08 ×3: aromatic fix + Phase B async + mdin-edit build + overnight testing).
- **This file**, and the skill itself: `project-prime/skills/mdin-edit/SKILL.md` (esp. the **Deferred** section — `--submit` + live NL drive are exactly the two things to build) and `skills/mdin-edit/tests/README.md` (the regression guard).

---

## 1. Where the project stands (don't re-discover)

The system is a **decoupled hybrid agent**: the LLM picks the skill + fills args; deterministic Python does every chemistry-critical mutation and self-validates. State as of 2026-06-09:

- **Pipeline Stages 2–5 BUILT + GREEN** — `antechamber-ligandprep` → `tleap-build` → `amber-md-run` → `cpptraj-analysis`, chained by `run_happy_path.sh` on 1L2Y. Corrected **MM-GBSA ΔG = −17.18 kcal/mol** (prior −13.x figures RETRACTED after the aromatic fix — do not cite them).
- **Phase A** (full 4-skill pipeline driven *by the agent*) **PROVEN** on free Cerebras `gpt-oss-120b`, $0.
- **Phase B** (Discord): small-task gate **PASSED** live; the **`pipeline-async`** skill (detached full-run launcher) + per-stage Discord notifications + a manual-start 429 watcher are **BUILT + dry-run-verified** — but the **live full-pipeline e2e was never run** (was blocked by the free-tier ~1-turn/day ceiling).
- **`mdin-edit`** (the advisor's NL parameter-editor over his pre-prepared mdin set) **BUILT + RIGOROUSLY TESTED** — overnight harness: 491 checks / 0 failures; 5 engine bug classes found + fixed; mutation 8/8. **Deferred tail = this session's Track 1.**

All commits are **local, not pushed** (project-prime `master`, vault `main`). project-prime HEAD `7dbc5bd`.

---

## 2. Scope — settled this session (record, don't re-litigate)

The **original pipeline** and the **advisor task are NOT mutually exclusive** — two entry points into the same thesis, at different points on the autonomy spectrum (`Design_Determinism_Spectrum`):

- **`amber-md-run` GENERATES** namelists from scratch — the *agent* owns the protocol (system-agnostic 6-step min/heat/density/prod chain).
- **`mdin-edit` EDITS** a human-authored namelist set — the *human* owns the protocol (the advisor's 10-stage `min1, min2, heat-1..3, press-1..3, relax, prod` chain); the agent makes surgical, bounds-checked, idempotent, change-logged edits.

Same architecture, same guardrails (`mdin-edit` vendored the validator from the pipeline). The advisor task is arguably the **stronger** proof of the thesis — it operates on a *real external* production input set, and matches how MD is actually used (chemists keep their own validated protocols and want auditable edits, not regeneration).

**The one open decision (not urgent):** which protocol is *canonical for the end-to-end demo / report* — our generated 6-step chain, or the advisor's 10-stage chain (driven by `mdin-edit` + `--submit`). They coexist as two modes; just be explicit in the report which is "the demo."

---

## 3. Track 1 — finish the advisor's mdin-edit task (autonomous; do first)

### 1a. `--submit` feature
**Goal:** prove the *edited* mdin set actually runs locally — productize what the Tier-3 smoke already does ad hoc.

The mechanics already exist in **`skills/mdin-edit/tests/smoke_edit_run.sh`**, which: copies the demo set → uses `mdin-edit` itself to cut `nstlim` → rewrites the advisor's hardcoded `AMBERHOME` in `submit.sh` to `source scripts/env.sh` (foreign-path-clean) → runs the `min1..prod` pmemd chain with restart chaining → asserts rc==0 + no "Terminated Abnormally" + non-empty `.rst7`. It passes 10/10.

`--submit` = lift that into the skill as a flag/path: copy `submit.sh` + topology + the (already-edited) mdin set, rewrite `AMBERHOME` → local toolchain via `scripts/env.sh`, optionally reduce `nstlim` via this same engine, run the chain, return a structured envelope (per-stage rc, normal-termination check, final `.rst7`). **Reuse `smoke_edit_run.sh`'s logic — do not reinvent it.**

**Done when:** a `--submit` invocation copies → (edits) → AMBERHOME-rewrites → runs a reduced-nstlim pmemd chain to normal termination on the advisor's topology; an acceptance case is added; the full `tests/` harness is still green under **both** conda 3.11 and system 3.14.

### 1b. Live NL drive
**Goal:** prove the agent's NL → `--stage/--param/--value` mapping works *as an agent*, not just via CLI.

Drive `mdin-edit` through `openclaw agent` with goal-phrased prompts the advisor would actually type, e.g.:
- "set the timestep to 1 fs in the first heating stage" → `--stage heat-1 --param dt --value 0.001`
- "relax the positional restraints to 1.0 from the third pressurization stage onward" → `--stage group:third-onward --param restraint_wt --value 1.0`
- "ramp the target temperature to 310 K across the later stages" → `--stage group:third-onward --param temp0 --value 310`

**Done when:** an `openclaw agent` turn picks `mdin-edit`, fires **exactly one `exec` call** (`toolSummary calls=1, failures=0`), and produces a valid edit on a COPY whose bytes match what the CLI would produce. Operate on a copy — never the advisor's originals.

### mdin-edit CLI reference
```
python3 {baseDir}/scripts/wrapper.py --md-dir <COPY> --stage <stage|group:third-onward|group:all> \
        --param <dt|cut|temp0|restraint_wt|nstlim> --value <n> [--dry-run]
```
Bounds: `0<dt≤0.002`, `0<temp0≤400`, `restraint_wt≥0`, `nstlim>0` int, `6≤cut≤12` (advisory WARN `6≤cut<8`). `temp0` in an `nmropt=1` heating stage couples `&wt value2`. COPY-first discipline is the caller's job.

### Regression guard — re-run after ANY wrapper change
```
cd skills/mdin-edit/tests
python3 oracle_selftest.py      # 38/38
python3 fuzz_mdin_edit.py       # ~240k assertions, 0 fail
python3 mutation_test.py        # 8/8
bash    smoke_edit_run.sh       # 10/10 (needs scripts/env.sh)
```
Use the **system** python (3.14) for the harness; keep the **engine 3.11-safe** (the bug that nearly shipped: `open(newline="")`, not `Path.read_text(newline=)`).

---

## 4. Track 2 — full pipeline from Discord (needs the user + the new PAID key)

The `pipeline-async` skill + notifications are **built + dry-run-verified** (6/6 notifications, $0). What's new: the user is adding a **paid Google AI Studio key**, which removes the free-tier ~1-turn/day ceiling that blocked the live multi-turn run. With the paid key you can run the full conversational pipeline from a Discord @-mention.

**Decisions banked (do NOT re-litigate):** notify via **LLM-free `openclaw message send`** (works during a 429; no webhook/raw token); **detached** (`start_new_session=True`) not sub-agents/polling (zero LLM after launch → dodges the 120s idle limit); **one DRY chain** (`run_happy_path.sh` opt-in `NOTIFY_CHANNEL` mode); scope = fixed 1L2Y + `--sim-ps`, manual-start watcher.

**Sequence (user-triggered — Discord can't be automated):**
1. After the paid key is added: `openclaw models auth paste-api-key --provider google`; decide model (gemini-3-flash-preview for cost, or keep cerebras default and use Google as fallback). Confirm `openclaw models status` (no cooldown) + gateway 200 + bot connected.
2. User @-mentions the bot "run the full pipeline at 30 ps". Confirm: agent invokes `pipeline-async` (one exec call), replies "started" + run-id, and the detached job posts 🚀→🧪→🧬→⚛️→📊→✅ (with the RMSD png) over ~10–15 min. Cross-check the on-disk run.
3. Arm the watcher: `bash scripts/watch_ratelimits.sh &` (`NOTIFY_DRYRUN=1` first to confirm).

**Done when:** a real @-mention drives the full pipeline detached and the per-stage + final ΔG (−17.18-class) messages land in the channel.

---

## 5. Key facts & gotchas (load-bearing)

- **Paths:** code = `/Users/kevinzhou/Downloads/Single Particle/project-prime/`; vault = `.../Single Particle/Single Particle/`. The path has a **SPACE** → tleap/cpptraj/MMPBSA tokenize on whitespace; copy inputs under bare names + reference relatively.
- **Toolchain:** `source project-prime/scripts/env.sh` (pmemd at `~/Downloads/pmemd26/bin`, conda `prime-amber` for AmberTools). OpenClaw runs **conda python 3.11** — keep wrappers 3.11-safe.
- **Inference:** via `--gateway` (LaunchAgent loopback `127.0.0.1:18789`). Shell tool is **`exec`** (not `bash`). Default model `cerebras/gpt-oss-120b`; paid Google key incoming. A full Cerebras agent turn is ~15 min (raise `--timeout` past 900s) and can 120s-idle-stall back-to-back; paid Google eases this.
- **Discord:** guild `1511130058306228311` allowlisted, `requireMention:true`. `openclaw message send` is LLM-free (delivers during a 429). No native error-delivery flag / agent-failure hook → the 429 alert is a log watcher.
- **SKILL.md metadata must be single-line JSON.** Skills register via `skills.load.extraDirs` in `openclaw.json` (already patched; don't re-apply).
- **Don't cite retracted ΔG (−12.84/−13.11/−13.29).** Corrected = −17.18. Never `--nohyd` a ligand.

---

## 6. The prompt to paste

```
Continuation of the Single Particle / OpenClaw + AMBER agentic-workflow project. Two tracks decided last session:

TRACK 1 (autonomous, DO FIRST) — finish the advisor's mdin-edit task: build `--submit` (prove the edited mdin set runs locally — productize tests/smoke_edit_run.sh's logic: copy set + topology, rewrite AMBERHOME via scripts/env.sh, reduce nstlim via the engine, run the pmemd chain to normal termination, structured envelope) and the live NL drive (drive mdin-edit through `openclaw agent` with goal-phrased prompts → correct --stage/--param/--value, one exec call, valid edit on a COPY).

TRACK 2 (needs me present + a PAID Google key I'm adding) — the live full-pipeline-from-Discord e2e: pipeline-async + notifications are built + dry-run-verified; the paid key removes the free-tier multi-turn ceiling that blocked it. I @-mention the bot → full detached run → per-stage + final ΔG posts.

Read BEFORE acting: memory project-prime-status (CRITICAL), openclaw-canonical-paths, antechamber-aromatic-kekulize-bug; vault Dev_Log.md (2026-06-08 ×3); skills/mdin-edit/SKILL.md (the Deferred section = the two Track-1 items) + tests/README.md.

Banked, do NOT re-litigate: mdin-edit vs amber-md-run are complementary (edit vs generate — same thesis, autonomy spectrum); Phase B notify = LLM-free `openclaw message send`, detached not sub-agents, one DRY chain; scope = fixed 1L2Y + --sim-ps. Corrected ΔG −17.18 (don't cite −13.x). Keep the wrapper python-3.11-safe.

Immediate sequence:
1. PRE-FLIGHT: `source project-prime/scripts/env.sh`; `which tleap pmemd cpptraj MMPBSA.py`; `git -C project-prime log --oneline -1` (expect 7dbc5bd or later); `openclaw skills list` (mdin-edit + pipeline-async ✓ ready); `openclaw models status`.
2. TRACK 1a `--submit`: reuse tests/smoke_edit_run.sh's logic; add an acceptance case; re-run the full tests/ harness green under py3.11 + py3.14 (oracle_selftest 38, fuzz, mutation 8/8, smoke 10/10).
3. TRACK 1b live NL drive: one `openclaw agent` turn, goal-phrased prompt → mdin-edit, one exec call, valid edit on a COPY; capture toolSummary.
4. TRACK 2 (when I say the paid key is in + I'm at the keyboard): wire the key, confirm gateway/bot, I @-mention "run the full pipeline at 30 ps", verify the 6 notifications + on-disk run; arm scripts/watch_ratelimits.sh.

Commit each unit local-not-pushed (project-prime master, vault main); Dev_Log entry + update memory project-prime-status + MEMORY.md at the end.

Stop conditions: if Track 1 needs a design change beyond the smoke's existing logic → note it, proceed with the straightforward version. If a wrapper change breaks the harness → fix to green before moving on. For Track 2, wait for my go (paid key + I'm present).

Scope-fence: Track 1 (both items) + Track 2 live e2e. Do NOT start Stage 6 (PLIP), arbitrary-ligand parsing, the always-on watcher LaunchAgent, or HPC/DPDispatcher without confirming. (Stage 6 PLIP is the next frontier AFTER these — see Next_Session_Prompt_OpenClaw_Day9.md.)
```

---

## 7. After the session — update this file

1. Flip frontmatter `status: ready` → `status: consumed`.
2. Add a `## Outcome` footer: consumed YYYY-MM-DD, 1-sentence outcome, link to the [[Dev_Log]] entry.

## Outcome

Consumed 2026-06-09. **Track 1 done.** `--submit` built (productizes the edit→run smoke; real run 10/10 stages to normal termination; full harness green under py3.14 + engine py3.11; project-prime `master` `b2d97fd`, not pushed). **Live NL drive byte-verified** through `openclaw agent` (cerebras, $0): prompt 1 (heat-1 dt→0.001) and prompt 3 (group:third-onward temp0→310 with `&wt` coupling) each produced edits **byte-identical to the CLI baseline**, `failures=0`. Provider flakiness noted (429 on both providers once; a provider-timeout once) and the `{baseDir}` path-resolution gotcha (supply the absolute wrapper path in the prompt). **Track 2 (Discord full-pipeline e2e) NOT started** — still gated on the paid Google key + user present. See [[Dev_Log]] 2026-06-09.

## Cross-links

- [[Dev_Log]] 2026-06-09 — `--submit` + live NL drive (this session's outcome).
- [[Dev_Log]] 2026-06-08 (×3) — aromatic fix, Phase B async, mdin-edit build + overnight testing.
- `Next_Session_Prompt_OpenClaw_Day9.md` — Phase B live e2e + **Stage 6 (PLIP)**; PLIP is the frontier *after* these two tracks. (This file supersedes Day9 for the immediate next session; Day9's PLIP content stays valid for later.)
- `Next_Session_Prompt_OpenClaw_Day8_Discord.md`, `Next_Session_Prompt_Advisor_mdin_Editor.md` — consumed; safe to delete.
- memories: [[project-prime-status]], [[openclaw-canonical-paths]], [[antechamber-aromatic-kekulize-bug]].
