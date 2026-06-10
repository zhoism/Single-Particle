---
tags: [project-prime, openclaw, session-handoff, stage6, plip, interaction-profiling]
type: handoff
status: ready
created: 2026-06-09
---

# Next Session Starter — Stage 6 PLIP (protein–ligand interaction profiling)

> Created 2026-06-09 at the end of the Track-(b) session. **Track (b) — arbitrary-target input is DONE** (the pipeline now runs any protein + ligand; proven on 1L2Y + a 2nd system 3HTB). Next frontier = **Stage 6: PLIP** — profile the protein–ligand interactions on the production trajectory and surface them as a structured result. This is a genuine differentiator: the baifan-wang `amber-md` prior art ([[amber-md-prior-art]]) stops at MM-GBSA and does NOT do interaction profiling. Paste the §The prompt to paste block into a fresh Claude Code session (run from the vault).

## Recap (what's done — don't re-discover)

- **Track (b) DONE** — `run_happy_path.sh` + `skills/pipeline-async` now take `--protein/--ligand/--charge/--name` (default to the 1L2Y fixture; the no-target launch command is byte-identical; legacy positional `SIM_PS`/`OUTDIR` preserved; inputs staged under bare names; up-front validation). Proven GREEN: **1L2Y regression** (ΔG −18.16, unchanged) + a **NEW target 3HTB** (T4 lysozyme L99A/M102Q + 2-propylphenol JZ4, 2636/27512 atoms, ΔG −27.41, ligand H-handled correctly) end-to-end, and **NL-driven** on live `google/gemini-3-flash-preview`. Commit project-prime **`95f20ed`** (`master`, not pushed). See [[Dev_Log]] 2026-06-09 (cont.).
- **The four pipeline skills + `run_happy_path.sh` + `pipeline-async` are all system-agnostic now.** A new target = drop a protein PDB + a ligand (PDB/mol2/sdf/SMILES) and pass `--protein/--ligand`.
- **Config state that must still hold:** paid Google AI Studio key is in; **default model = `google/gemini-3-flash-preview`**; the Discord bot connects via the per-guild `users` allowlist (NOT `groupAllowFrom`). `scripts/env.sh` prepends an nvm node≥22 for the detached notify path.
- **PLIP is already installed** in the `prime-amber` conda env (**plip 3.0.0**) — verified at install time ([[project-prime-status]], 2026-05-19). No new install needed; it's reachable once `scripts/env.sh`/the conda env is active.
- **There is a PLIP precedent in the repo:** `project-prime/golden-path/` (the pre-skills T4-lysozyme+benzene `181L` golden path) ran PLIP and fingerprinted the cavity (6 hydrophobic contacts). Its `analyze.cpptraj` holds the resname-normalization fix (see below). Mine it for the recipe; do NOT assume the skill-era pipeline already does PLIP — it stops at cpptraj-analysis (Stage 5).

## Decisions banked — do NOT re-litigate

- **Arbitrary-target is settled.** Don't re-parameterize `run_happy_path.sh`/`pipeline-async` — they already take `--protein/--ligand/--charge/--name`. Build Stage 6 as a NEW skill (`Skill_*` → scaffold via `/skill-scaffold`) that consumes the dry complex topology + trajectory the way `cpptraj-analysis` does.
- **PLIP resname footgun (load-bearing — this is THE Stage 6 trap):** AMBER writes protonation/disulfide-variant residue names (`HIE/HID/HIP/CYX/GLH/ASH/LYN/…`). PLIP reads a PDB and treats anything it doesn't recognize as a residue as a **phantom small-molecule ligand** → it will "find" fake ligands among your protein residues and/or miss the real one. The golden-path fix (in `golden-path/analyze.cpptraj`) **normalizes those resnames back to standard PDB names before PLIP**. Reuse that mapping. Verify PLIP keys on the actual ligand residue (the `--name`, e.g. `MOL`/`JZ4`), not a mis-typed protein residue.
- **PLIP needs a PDB of the complex, not a trajectory.** Decide the frame policy: profile a **representative frame** (e.g. the top cluster representative cpptraj already computes, or the last/median frame) — start there, single-frame, for a clean v1. A full per-frame interaction time-series is a v2 (note it, don't build it first). `cpptraj` extracts the frame; strip to the **dry** complex (no water/ions) before PLIP.
- **Never `--nohyd` a ligand**; PLIP needs explicit H to assign H-bonds/donors-acceptors correctly — the production complex already has H (tleap added them). Use the dry complex topology + a frame with H intact.
- **Physical realism + determinism discipline stays** (CLAUDE.md SOPs): the skill is a deterministic wrapper (`--dry-run` + JSON envelope + `test_acceptance.sh` golden/unrelated/malformed), the LLM only picks the skill. Match the existing skills' shape.

## What's NOT done (deferred, non-blocking — do NOT start without confirming)

- **Wiring Stage 6 into `run_happy_path.sh`/`pipeline-async`** as a Stage 6 step (after building + acceptance-testing the standalone skill). Reasonable to do at the end of the session if the skill is green.
- **Per-frame interaction time-series / occupancy** (v2 of PLIP analysis).
- **Bounded error recovery** (`Workflow_Error_Recovery_Loop` + `Skill_Bounded_Recovery_AMBER`), **planner / `Arch_Taskboard_Manifest`** layer — the differentiators after Stage 6.
- **`Gap_Remote_HPC_Backend`** — the production-scale decision (local is CPU-only). A call to settle with the advisor, not a local build.
- Pushing commits; always-on watcher LaunchAgent.

## The prompt to paste

```
Continuation of the Single Particle / OpenClaw + AMBER project — Stage 6: PLIP protein–ligand interaction profiling on the production trajectory. Track (b) arbitrary-target input is DONE; the pipeline runs any protein+ligand. project-prime HEAD 95f20ed (master, local). Default model is paid google/gemini-3-flash-preview.

Read BEFORE acting (in order):
- memory project-prime-status (CRITICAL — current state; Track (b) done; PLIP 3.0.0 installed)
- memory amber-md-prior-art (PLIP is one of OUR differentiators the prior art lacks)
- memory antechamber-aromatic-kekulize-bug (never --nohyd a ligand; H must be present)
- memory openclaw-canonical-paths (exec not bash; --gateway; SKILL.md single-line JSON metadata; deterministic-wrapper discipline)
- vault Dev_Log.md (2026-06-09 entries) ; project-prime/golden-path/analyze.cpptraj (the PLIP resname-normalization precedent) ; skills/cpptraj-analysis/SKILL.md (how the dry complex topology + representative frame are produced)

Banked, do NOT re-litigate: arbitrary-target is settled (run_happy_path.sh + pipeline-async already take --protein/--ligand/--charge/--name — build Stage 6 as a NEW deterministic-wrapper skill, don't touch those). THE trap is the PLIP resname footgun — AMBER HIE/CYX/etc. must be normalized to standard PDB names before PLIP or it invents phantom ligands among protein residues (fix is in golden-path/analyze.cpptraj). PLIP needs a DRY complex PDB frame (strip water/ions; keep ligand H). Start single-frame on a representative frame (top cluster rep / last frame), per-frame time-series is v2.

Immediate sequence (Stage 6 PLIP ONLY):
1. PRE-FLIGHT (~5 min): source project-prime/scripts/env.sh (under bash, NOT interactive zsh — env.sh has a known zsh-nomatch glob quirk); which plip cpptraj pmemd; python -c "import plip; print(plip.__version__)" (expect 3.0.0); git -C project-prime log --oneline -1 (expect 95f20ed+); openclaw skills list ; openclaw models status (default gemini-3-flash-preview); curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18789/ (200). NOTE: foreground Claude Bash calls are sandboxed and 126 on conda-binary exec — run AMBER/PLIP work via a backgrounded `bash -c 'source scripts/env.sh && …'` (the proven pattern), not a foreground sandboxed shell.
2. MAP: read golden-path/{analyze.cpptraj,run.sh,README} for the working PLIP recipe + resname normalization; read skills/cpptraj-analysis to see what dry-complex topology / representative frame / cluster rep it already emits (reuse, don't recompute).
3. BUILD: scaffold skills/plip-profile (or similar) via /skill-scaffold — deterministic wrapper, --dry-run + JSON envelope, that: (a) takes the dry complex topology + trajectory (+ ligand resname), (b) extracts a representative frame to a dry PDB via cpptraj, (c) normalizes AMBER resnames → standard PDB, (d) runs PLIP, (e) parses PLIP's XML/report into a structured envelope (interaction types + residues + counts: hydrophobic, H-bond, π-stacking, salt-bridge, etc.), (f) writes a human-readable summary. Bound/validate inputs; fail gracefully (structured ok:false).
4. TEST: test_acceptance.sh — (a) golden: run on the existing 1L2Y or 3HTB run output, assert PLIP found the REAL ligand (not a phantom protein residue) + ≥1 sane interaction; (b) malformed → ok:false; (c) a resname-variant case proving normalization fired. Then run it on a real prior run dir (regression-1L2Y/ or new-target-run/ both exist with full trajectories).
5. (If green) optionally wire Stage 6 into run_happy_path.sh after cpptraj-analysis (guarded; keep 1L2Y regression green).
6. NL DRIVE: one openclaw agent turn — "profile the protein–ligand interactions for run X" → the plip skill with the right inputs.
7. CLOSING: devlog-append; update memory project-prime-status + MEMORY.md; flip this handoff status→consumed + Outcome footer; write next-session-prompt for the step after (bounded recovery OR planner). Commit local-not-pushed.

Stop conditions:
- If PLIP mis-identifies the ligand or invents phantom ligands, the resname normalization isn't covering a variant — extend the mapping; don't hack around it downstream.
- If a representative frame is ambiguous, use the cpptraj top-cluster representative (already computed) or the last production frame — don't rabbit-hole on frame selection.
- If wiring Stage 6 into run_happy_path.sh risks the 1L2Y regression, keep it standalone and ship the skill green first.

Scope-fence: Stage 6 PLIP ONLY. Do NOT start bounded recovery, the planner/Taskboard-Manifest, or HPC/DPDispatcher without confirming.
```

## After the session — update this file

1. Flip frontmatter `status: ready` → `status: consumed`.
2. Add an `## Outcome` footer: consumed YYYY-MM-DD, 1-sentence outcome, link to the [[Dev_Log]] entry.

## Cross-links

- [[Dev_Log]] 2026-06-09 (cont.) — "Track (b) DONE: arbitrary-target input" — the session that produced this handoff.
- `Next_Session_Prompt_ArbitraryTarget.md` (consumed) — the prior handoff.
- memories: [[project-prime-status]], [[amber-md-prior-art]], [[antechamber-aromatic-kekulize-bug]], [[openclaw-canonical-paths]].
