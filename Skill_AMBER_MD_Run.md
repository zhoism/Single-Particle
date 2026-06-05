---
tags: [amber, pmemd, sander, md, equilibration, production, engine-seam, built]
---
# Skill: amber-md-run (Phase 3 Stage 4) ✅ BUILT 2026-06-05

*(Manifest originally called this "Skill_Sander_Run"; built as `amber-md-run` with an engine seam — pmemd default, sander fallback.)*

**The User Pain Point:** A real MD run is a chain of seven-ish input files (`min1/2/3`, heat, density, production) whose parameters must be internally consistent and physically sane. Hand-writing them invites the exact bugs the project's [[md-param-check]] exists to catch — the advisor's `heat-3.in` `temp0`/`&wt` mismatch, the hardcoded-AMBERHOME portability bug, dt-too-large / SHAKE-off realism bugs.

**The OpenClaw Solution:** A deterministic wrapper that *generates* the 6-step chain with [[md-param-check]]-clean namelists + a portable `run.sh`, then executes locally to completion. The LLM never hand-writes a namelist (the upstream amber-md failure mode).

**Physical-realism guarantees (by construction):** `dt=0.002` with SHAKE (`ntc=2,ntf=2`); `8≤cut≤12`; Langevin `ntt=3 gamma_ln=2.0 ig=-1`; `temp0`==`&wt value2` in heat (no heat-3 bug); `ntp=1 barostat=2` (MC) for NPT; `iwrap=1` production. No hardcoded engine path.

**Engine seam ([[Gap_Remote_HPC_Backend]]):** `--engine` = serial `pmemd` (default, ~15.6 ns/day on this Mac for 1L2Y; default 200 ps of MD ≈ 19 min), `pmemd.MPI` (mpirun), or `sander` (conda fallback). `--sim-ps` parameterizes production. Scenario B (remote `pmemd.cuda` + scheduler via DPDispatcher) swaps this seam only — recipe files untouched. **DPDispatcher integration explicitly deferred** (not needed for local; the seam is where it plugs in). prmtop built by AmberTools 24.8 reads fine in pmemd 26 (verified).

**Recovery hook:** `.out` scanned for `vlimit exceeded` / `SHAKE failed` → surfaced as `MD_CRASH[stage]`. This is the seam [[Skill_Bounded_Recovery_AMBER]] (Stage 8) will act on.

**Acceptance:** `skills/amber-md-run/test_acceptance.sh` — golden (`--steps min`, 3 .rst, no crashes), dry-run namelist invariants (heat temp0==value2, product barostat=2+iwrap=1), malformed (missing topology). PASS.

**Artifacts:** `project-prime/skills/amber-md-run/{SKILL.md, scripts/wrapper.py, references/heuristics.md, test_acceptance.sh}`.

**Source:** [[Research_amber_md_skill]] steal #7; upstream `input-templates.md`; [[md-param-check]] rules; [[pmemd-local-build]]; Amber26.pdf ch.23–24.
