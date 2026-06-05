---
tags: [amber, tleap, topology, solvation, mm-gbsa, built]
---
# Skill: tleap-build (Phase 3 Stage 3) ✅ BUILT 2026-06-05

**The User Pain Point:** `tleap` is unforgiving and the *order* of operations silently determines downstream correctness. Saving the "dry" complex topology after solvation produces a topology that secretly contains water — which then breaks every stripped-trajectory analysis with `Number of atoms … does not match`. Hand-writing `leap.in` and tracking save order is error-prone.

**The OpenClaw Solution:** A deterministic wrapper that generates a *correct* `leap.in` and runs `tleap`, with the LLM outside the execution path (the [[Phase3_Taskboard_Manifest]] "lobster-like" discipline). Takes a protein PDB + the ligand `mol2`/`frcmod` from [[Skill_Antechamber_LigandPrep]], produces:
- `comp_oct.{top,crd}` — solvated, neutralized (MD input)
- `comp_dry.{top,crd}` — dry complex (analysis), saved **BEFORE** `solvateoct`
- `protein.top` + `ligand.top` — independent components for MM-GBSA

**What it fixes vs upstream amber-md** (see [[Research_amber_md_skill]]):
- Saves `comp_dry` before solvation (upstream `leap.in` gets this wrong).
- Loads the ligand as a **mol2** so `combine` auto-renumbers it — no brittle `sed` residue-collision hack (the 1L2Y indole is `MOL A 6`, colliding with ALA 6).
- Validation gates: `leap.log` no ERROR, **dry < solvated atoms** (regression test for the save-order bug), **protein+ligand == dry** combine invariant, system neutral.

**Gotchas hit:** (1) the input PDB carried PDB-v2 hydrogen names (`1HB`) that ff19SB rejects → `pdb4amber --nohyd`, LEaP rebuilds H. (2) The project path has a space (`Single Particle`) and LEaP tokenizes on whitespace → inputs copied into the run dir under bare names, `cwd=run_dir`.

**Acceptance:** `skills/tleap-build/test_acceptance.sh` — golden (protein+ligand, 306 dry / ~5986 solvated atoms), unrelated (protein-only build), malformed (missing protein → graceful fail). 3/3 PASS.

**Artifacts:** `project-prime/skills/tleap-build/{SKILL.md, scripts/wrapper.py, references/heuristics.md, test_acceptance.sh}`. Chained in `project-prime/run_happy_path.sh`.

**Source:** [[Research_amber_md_skill]] steal-list #1/#3; upstream `input-templates.md` §5; Amber26.pdf ch.14 (see [[amber26-pdf-section-map]]).
