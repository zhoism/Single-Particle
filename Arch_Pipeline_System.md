---
tags: [project-prime, openclaw, architecture, phase-b, system-overview, proof]
type: arch
status: snapshot-2026-06-08
created: 2026-06-08
---

✅ **Verified / proven live 2026-06-08.** This note explains the working system end-to-end: how it is built, how a simulation runs through it, and the proof for every claim. Companion to [[OpenClaw_CLI_Map]] (CLI facts) and [[Phase3_Taskboard_Manifest]] (stage plan). Evidence is cited inline (commit hashes, run ids, file paths).

> ⏳ **SNAPSHOT — describes the 2026-06-08 Phase-B state (5 skills).** The pipeline has since grown to **NINE** skills (added `plip-profile`, `mdin-edit`, `amber-recover`, `md-planner`), and the Stage-6/7/8 items listed in §7 as "Deferred by design" (PLIP, planner, bounded-recovery) are now **BUILT** (by 2026-06-10). The architecture and worked example below remain accurate for their date — for current status see [[Phase3_Taskboard_Manifest]] + [[project-prime-status]].

# The agentic MD pipeline — how it's built, how it runs, and proof

## 1. The thesis in one breath

A **decoupled hybrid agent**: an LLM decides *what* to run, but never touches *how* the science executes. You @-mention a Discord bot; it launches a full explicit-solvent **AMBER molecular-dynamics** pipeline in the background; the pipeline runs as hardened **deterministic Python wrappers**; progress and results stream back to Discord over an **LLM-free** channel. The LLM is the front door; the science is bulletproof regardless of which model (or rate limit) is behind it.

## 2. Architecture (the layers, top to bottom)

```
[ You, in Discord ]
      │  @-mention: "run the full MD pipeline at 20 ps"
      ▼
[ Discord bot  ↔  OpenClaw gateway ]      127.0.0.1:18789  (macOS LaunchAgent)
      │  routes to the `main` agent — model: google/gemini-3-flash-preview
      ▼
[ AGENT: the LLM picks ONE skill ]   ◄── the ONLY LLM-in-the-loop step
      │  one `exec` call → pipeline-async wrapper
      ▼
[ pipeline-async : detached launch ]   returns {status:launched, run_id} in <1s
      │  nohup setsid bash -c  (new session → survives the agent turn ending)
      ▼
[ run_happy_path.sh : the DETERMINISTIC spine ]   ◄── NO LLM from here on
      ├─ Stage 2  antechamber-ligandprep → GAFF2 .mol2 (+AM1-BCC) + .frcmod
      ├─ Stage 3  tleap-build            → solvated, neutralized topology
      ├─ Stage 4  amber-md-run           → 6-step MD (min×3 → heat → density → product) via pmemd
      └─ Stage 5  cpptraj-analysis       → 12 analyses + MM-GBSA + plots
      │   after each stage → notify_discord.sh → `openclaw message send`  (LLM-FREE)
      ▼
[ Discord channel ]   🚀 started → 🧪 prep ✓ → 🧬 topology ✓ → ⚛️ MD ✓ → 📊 analysis ✓ → ✅ done (ΔG + RMSD plot)

[ watch_ratelimits.sh ]  (sidecar, manual-start)  tails the gateway log; if the agent turn 429s, posts a usage-limit alert to the channel — also LLM-free.
```

**The load-bearing idea:** the LLM is touched exactly once (deciding to launch). Everything downstream — the MD, the analysis, and even the Discord progress messages — runs without it. So a flaky/rate-limited model cannot corrupt the science or lose the results; it can only delay the initial trigger (which the watcher then reports).

## 3. System setup (the concrete components)

| Component | What | Where / proof |
|---|---|---|
| **Substrate** | OpenClaw 2026.5.28, gateway as a LaunchAgent | `127.0.0.1:18789`; [[openclaw-canonical-paths]] |
| **Model** | `google/gemini-3-flash-preview` (default, paid key); `cerebras/gpt-oss-120b` available as a free option | `openclaw models status` |
| **Channel** | Discord bot `@Single Particle`, guild `1511130058306228311`, channel `1511130059061067858`, `requireMention` | `openclaw channels status --probe` |
| **MD toolchain** | `prime-amber` conda env (AmberTools 24.8) + locally-built **pmemd 26** | sourced for detached runs via `project-prime/scripts/env.sh` |
| **Skills (5)** | deterministic wrappers, registered via `skills.load.extraDirs` | `openclaw skills list` → all `✓ ready` |
| **Code repo** | `project-prime/` (git, branch `main`) | runnable skills + spine + scripts |
| **Docs repo** | this vault (git, branch `main`) | design notes, Dev_Log, this file |

**The 5 skills** (each = a SKILL.md goal description + a `scripts/wrapper.py` that does the work and validates its own output; the LLM stays *outside* the wrapper):
1. `antechamber-ligandprep` — ligand → GAFF2 mol2 + frcmod
2. `tleap-build` — protein + ligand → solvated topology
3. `amber-md-run` — the 6-step MD chain via pmemd
4. `cpptraj-analysis` — 12-analysis suite + MM-GBSA + figures
5. `pipeline-async` — launches all four detached + streams progress to Discord (Phase B)

Supporting scripts (`project-prime/scripts/`): `notify_discord.sh` (LLM-free Discord post), `watch_ratelimits.sh` (429 alert sidecar), `env.sh` (toolchain bootstrap). The spine `run_happy_path.sh` chains the four science skills and (opt-in via `NOTIFY_CHANNEL`) posts per-stage progress.

## 4. How THIS simulation ran — worked example `pa-20260608-194730`

**Test system:** PDB **1L2Y** (the Trp-cage miniprotein). Its tryptophan **indole** sidechain is treated as a separate small-molecule "ligand" binding the rest of the protein — a deliberate, reproducible **positive-control** system, not a drug. (The whole pipeline is system-agnostic; 1L2Y is just the fixture.)

Step by step, with evidence:
1. **You @-mentioned** the bot to run the full pipeline.
2. **The agent picked `pipeline-async`** and made one `exec` call; the wrapper returned `{status:"launched", run_id:"pa-20260608-194730"}` in under a second, and the agent replied "started" in-channel.
3. **The detached spine ran the four skills** on 1L2Y at **20 ps** production, sourcing the toolchain via `env.sh`, with `NOTIFY_CHANNEL` set.
4. **Each stage posted to Discord** (see the 2026-06-08 8:14 PM screenshot): `🚀 started → 🧪 prep ✓ → 🧬 topology ✓ (306/5989 atoms) → ⚛️ MD ✓ (wall 115 s) → 📊 analysis ✓ → ✅ done`.
5. **Result:** 12 analyses, **MM-GBSA ΔG = −17.6 kcal/mol**, plus the Backbone-RMSD plot, on disk at `project-prime/pipeline-async-run-pa-20260608-194730/` (gitignored — regenerated on demand).

## 5. What we built and fixed this session (2026-06-08)

1. **Caught + fixed a silent science bug** (the headline). QC of a Discord reply revealed the 1L2Y indole was being typed **non-aromatic** (`c2/ce/cf/ne`, ring N–H dropped) because the ligand prep stripped hydrogens then let OpenBabel re-perceive bonds, which failed to kekulize the aromatic ring; antechamber then trusted the broken bonds. **Every validation gate passed** — a silent failure that had affected *all* prior runs (so the earlier ΔG ≈ −13 was on a mis-parameterized ligand). Fix: H-present PDBs go straight to `antechamber -fi pdb -j 4` (its own perception kekulizes correctly) + a new fatal `AROMATIC_PERCEPTION_FAILED` gate + a regression test. Corrected typing → `ca/cc/cd/na/hn`. See [[antechamber-aromatic-kekulize-bug]].
2. **Built Phase B** — the async Discord orchestration above (`pipeline-async` skill, per-stage notifications, the 429 watcher).
3. **Fixed two launcher bugs found via live testing** — a login shell (`bash -lc`) was switching `node` and breaking the notify CLI; and the run log was being written into the dir the spine wipes. Both fixed (`bash -c`, sibling log).

## 6. Proof (the evidence trail)

**Commits — `project-prime` (`master`):**
- `c7e5948` — pipeline-async: detached-notify fix (non-login `bash -c`) + log location
- `f799d1c` — Phase B: async Discord pipeline launcher + 429 self-alert
- `f30414e` — fix silent aromatic mis-typing in antechamber-ligandprep
- `2e9d8a4` — Stages 3–5: tleap-build + amber-md-run + cpptraj-analysis

**Commits — vault (`main`):** `9745e19`, `03949e0` (this session's logs + handoffs).

**Correctness verification (independent of the pipeline's own `ok:true`):**
- **Ligand typing:** `6 ca, cc, cd, na, hn, ha, h4` — aromatic, N–H intact (NE1→na, HE1→hn); broken `c2/ce/cf/ne` absent.
- **Topology:** 306 dry = 290 protein + 16 ligand (combine invariant), `leap.log` 0 errors, 5989 solvated.
- **MD namelists:** dt = 2 fs, SHAKE (ntc/ntf=2), cut = 9, Langevin (ntt=3, γ=2.0), density/product ntp=1 + barostat=2 + iwrap=1, heat `temp0=300 == value2=300`.
- **MD stability:** 0 NaN, 0 "vlimit exceeded"; average temperature **299.91 K** (the `****` in min1 is the expected step-1 clash overflow; `TEMP 3.93` was the RMS-fluctuation line, not a temperature).
- **MM-GBSA:** decomposition is **vdW-dominated** (ΔVDWAALS ≈ −20.5) — exactly what an indole packing in a hydrophobic pocket should give, and what the *correct* aromatic typing enables.
- **Reproducibility:** two independent 20 ps runs → **−17.18** and **−17.6** kcal/mol (~0.4 apart). The 30 ps run's −19.2 is within the same short-run sampling spread.
- **Live proof:** the 2026-06-08 8:14 PM Discord screenshot — the full `🚀→✅` sequence + RMSD plot.

## 7. Honest caveats / what is deliberately NOT done

- **ΔG is a short-run estimate, not a converged binding affinity.** 20–30 ps, single trajectory; the value wanders ±1–2 kcal/mol with sampling. The *method* is verified correct; the *number* is illustrative. A real affinity needs ns-scale sampling and convergence checks.
- **Free-tier rate limits (429s)** can stall the *launch turn* (the LLM step). A paid tier removes this; the architecture already makes everything *after* launch model-independent. The watcher reports a stalled launch.
- **Deferred by design:** arbitrary-ligand requests (this runs the fixed 1L2Y demo), PLIP interaction profiling (Stage 6), the planner/bounded-recovery skills (Stages 7–8), remote-HPC dispatch ([[Gap_Remote_HPC_Backend]]), and an always-on watcher LaunchAgent.

## Cross-links
- [[Dev_Log]] 2026-06-08 + 2026-06-08 (cont.) — the build sessions.
- [[Phase3_Taskboard_Manifest]] — the stage plan + status.
- [[antechamber-aromatic-kekulize-bug]], [[project-prime-status]], [[openclaw-canonical-paths]] — memories.
