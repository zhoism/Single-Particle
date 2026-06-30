---
tags: [amber, cpptraj, mmpbsa, analysis, rmsd, pca, mm-gbsa, built]
---
# Skill: cpptraj-analysis (Phase 3 Stage 5) ✅ BUILT 2026-06-05

**The User Pain Point:** Post-MD analysis is ten separate cpptraj/MMPBSA invocations, each with its own input file, plus matplotlib plotting — and several have non-obvious footguns that silently emit empty data. Doing this by hand per simulation is exactly the tedium the agent should absorb.

**The OpenClaw Solution:** A deterministic wrapper that runs the full suite and emits a `.dat` + `.png` per analysis: strip (preprocess) → RMSD, RMSF, Rg, SASA, DSSP, H-bonds, Cα distance matrix, k-means clustering, PCA, free-energy landscape, thermodynamics, MM-GBSA. Inline matplotlib (numpy/pandas in `prime-amber`).

**What it fixes vs upstream amber-md** (the example `.in` files are the *buggy* "before" versions — see [[Research_amber_md_skill]]):
- **Strip uses the SOLVATED topology** (`comp_oct`) to match the trajectory atom count, writes a dry `strip.nc`; downstream uses `comp_dry`. Upstream strips with `comp_dry` against the solvated trajectory — only "works" because their comp_dry is secretly solvated.
- **PCA is two cpptraj calls** (`diagmatrix`+`run`, then `projection`) — one call → "evecs contains no data".
- **Clustering keeps `repout` inside the single kmeans command** (splitting reverts to hieragglo).
- **H-bond "no data" is a finding**, not an error (indole binds via hydrophobic / π–π; reported with an explanatory figure).
- **Residue masks auto-detected** from the dry topology (not hardcoded `:1-20`/`:21`).
- **Parsing gotchas** handled: `evecs.dat` hand-parsed (not `read_csv`); `summary.DENSITY` may be 1-col; cluster `summary.dat` header skipped.
- **Path-with-space safe** (copy in + relative refs, as in [[Skill_Tleap_Build]]).

**MM-GBSA:** `MMPBSA.py -sp comp_oct -cp comp_dry -rp protein -lp ligand -y product.nc`, `igb=5 saltcon=0.1`. **The dry component tops (`-cp`/`-rp`/`-lp`) are retyped to `mbondi2` via `parmed changeRadii` before MM-GBSA** — igb=5 requires mbondi2 (Amber Table 4.1); a surviving radii mismatch is now FATAL (see [[Research_AMBER_Failure_Modes]] P1 #1, fixed 2026-06-29). Post-fix baselines: **1L2Y/indole ΔG ≈ −17.78**, **3HTB/JZ4 ≈ −25.85** kcal/mol (single-traj 100 ps sanity; negative = favorable; article ≈ −16 on 1 ns). *(Pre-mbondi2-fix mbondi numbers −18.16 / −27.41 superseded 2026-06-29; the pre-2026-06-08 ≈ −14 figure was the mis-typed non-aromatic ligand, also superseded — see [[antechamber-aromatic-kekulize-bug]].)* This is the headline quantitative result; PLIP interaction profiling ([[Phase3_Taskboard_Manifest]] Stage 6) is the differentiator beyond it (since built as `plip-profile`).

**Acceptance:** `skills/cpptraj-analysis/test_acceptance.sh` — golden (full suite, ≥12 analyses + ΔG<0 + GB radii retyped to mbondi2/consistent), subset (`rmsd,rg` only), malformed (missing trajectory), **Case 4 (GB-radii fatal gate: forced-off fix → `ok:false` with core produced)**. PASS.

**Artifacts:** `project-prime/skills/cpptraj-analysis/{SKILL.md, scripts/wrapper.py, scripts/process_mdout.perl, references/heuristics.md, test_acceptance.sh}`.

**Source:** [[Research_amber_md_skill]] steal #4/#5/#6; upstream `analysis.md`; Amber26.pdf ch.25 (atom masks).
