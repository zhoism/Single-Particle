---
tags: [infrastructure, amber, ambertools, install, conda-forge, macos, arm64]
type: infra
status: installed
---
# Infrastructure: Local AMBER Install (AmberTools 24.8)

> **Vault tier: ✅ Actually-executed install** — verified 2026-05-19 on macOS 15.7.4, Apple Silicon (arm64), CPU-only. AmberTools 24.8 + PLIP 3.0.0 in conda env `prime-amber`. All binaries arm64-native (not Rosetta).

**Core role:** Project Prime's local MD execution environment. Provides the AmberTools binaries (`sander`, `tleap`, `antechamber`, `parmchk2`, `cpptraj`, `pdb4amber`, `parmed`) plus the PLIP CLI that the OpenClaw skills will eventually orchestrate.

## Why conda-forge, not source

Source-build AMBER on osx-arm64 is the "Scenario A dependency hell" path called out in [[project-prime-status]] — Apple clang/OpenMP/Fortran toolchain interactions are fragile, and the only reason to ever build from source (`pmemd.cuda`) is N/A on this CPU-only Mac. conda-forge ships a tested arm64 binary that includes everything the project actually needs.

`make test` from the source tree is **not** shipped with the conda-forge binary, so the SOP step "run the built-in test cases" is satisfied by the literal `cpptraj --help` + `which sander` checks below. An end-to-end MD validation (tiny water box / ligand) is the queued next task — see [[Dev_Log]] entry of 2026-05-19.

## Env summary

| Item | Value |
|---|---|
| Env name | `prime-amber` |
| Prefix | `/opt/homebrew/Caskroom/miniforge/base/envs/prime-amber` |
| Python | 3.11.15 |
| AmberTools | **24.8** (build `cuda_None_nompi_py311h523f5e4_101`) |
| Sander banner | `Amber 24 SANDER 2024` |
| cpptraj | `V6.24.0 (AmberTools)` |
| PLIP | 3.0.0 (CLI: `plip`; Python module: `import plip`) |
| ParmEd | 4.3.1 |
| OpenBabel | 3.1.1 (PLIP dep, conda-resolved) |
| Arch check | `file $(which sander)` → `Mach-O 64-bit executable arm64` ✓ |
| Lockfile | `/Users/kevinzhou/Downloads/Single Particle/project-prime/env.lock.yml` |

## Exact commands run

```bash
# Pre-flight — confirm a native arm64 build exists, pick latest version
CONDA_SUBDIR=osx-arm64 mamba search -c conda-forge ambertools
# → AmberTools 24.8 confirmed (osx-arm64), py3.10/3.11/3.12/3.13 builds, nompi + mpich variants

# Single combined create + install (one solver run)
mamba create -n prime-amber -c conda-forge -y \
    python=3.11 'ambertools=24.8=*nompi*' plip

# Confirm arm64-native (not Rosetta x86_64)
conda activate prime-amber
file "$(which sander)"   # → arm64

# Lockfile
mamba env export -n prime-amber --no-builds \
    > /Users/kevinzhou/Downloads/Single\ Particle/project-prime/env.lock.yml
```

**Pin rationale:**
- `=24.8` — latest osx-arm64 build with confirmed Python 3.11 support. Pinning guards against a future regression auto-upgrading us.
- `*nompi*` — `mpich` MPI variants exist but are unnecessary on a single laptop and add deps. `nompi` is the lighter, sufficient choice for `sander` serial runs.
- Python 3.11 — broadly tested across conda-forge AmberTools builds. 3.12/3.13 builds also exist; revisit if a downstream library forces a bump.

## Verification (SOP intent)

```bash
conda activate prime-amber

which sander cpptraj tleap antechamber parmchk2 pdb4amber
# all → $CONDA_PREFIX/bin/<binary>

file "$(which sander)"
# → Mach-O 64-bit executable arm64

cpptraj --help     # literal SOP requirement — prints usage ✓
cpptraj --version  # → V6.24.0 (AmberTools)
tleap -h           # prints usage + leap search paths ✓
antechamber -h     # prints usage ✓

python -c "import plip; print(plip.__file__)"   # module loads ✓
plip -h | head -10                              # CLI confirms Version 3.0.0 ✓
```

**Note on `plip.__version__`:** PLIP 3.0.0 does not expose `__version__` on the module — the canonical version probe is the `plip -h` banner, not `plip.__version__`.

**Note on `sander -h`:** sander treats `-h` as an unknown flag (it expects `-O`/`-A` plus `-i mdin -o mdout` etc.), but it still prints its usage banner and writes "Amber 24 SANDER 2024" to the mdout file. That banner is the version probe.

## Shell environment

Shell is zsh (`~/.bashrc` does not exist on this machine). Conda init was already present in `~/.zshrc` (lines 24–37, from prior Miniforge install via Homebrew). **No rc-file edits were needed** — the SOP's "add to ~/.bashrc" step is a no-op on this machine. Activation:

```bash
conda activate prime-amber
```

## End-to-end smoke test — PASSED 2026-05-19

Two-leg validation at `project-prime/smoke-test/` (not `runs/` — that path is gitignored). Both legs run in ~42 s total on this Mac.

**Leg A — `aladip/` — alanine dipeptide in TIP3P water:** `tleap` build+solvate → `sander` minimize (1000 cyc) → `sander` heat 0→300 K (10 ps) → `sander` NVT 300 K (10 ps) → `cpptraj` rmsd + radgyr. Results: minimization energy dropped −4811 → −6694 kcal/mol; net charge 0.000; backbone RMSD stayed under 0.4 Å; radius of gyration steady ≈3.0 Å (matches alanine dipeptide); zero `NaN` in energy columns. ff14SB + TIP3P force fields.

**Leg B — `benzene/` — ligand parameterization chain:** `obabel` SMILES `c1ccccc1` → 3D → `antechamber` (GAFF2 atom types, AM1-BCC charges) → `parmchk2` (missing-parameter check) → `tleap` builds topology. Results: all 6 carbons typed `ca`, all 6 hydrogens typed `ha` (correct aromatic GAFF2 typing); AM1-BCC charges perfectly symmetric (C = −0.130, H = +0.130, ΣQ = 0); `frcmod` added one standard `X-X-ca-ha` improper torsion only.

This is the baseline the OpenClaw skills will reproduce — see [[Skill_Antechamber_LigandPrep]] for Leg B and [[Skill_Bounded_Recovery_AMBER]] for the kind of recovery logic that operates on top of Leg A's sander chain.

## Gotchas observed (none blocking)

1. `mamba search ... --subdir osx-arm64` is unsupported in mamba 2.5.0 — use `CONDA_SUBDIR=osx-arm64 mamba search ...` instead.
2. `plip.__version__` attribute does not exist in PLIP 3.0.0; use `plip -h` for version probing.
3. `sander -h` is "unknown flag" but still prints usage — sander's diagnostic-on-error path is the de facto help.

## Cross-links

- [[Skill_Antechamber_LigandPrep]] — the antechamber/parmchk2 binaries this env provides are the substrate for that skill.
- [[Skill_Bounded_Recovery_AMBER]] — bounded recovery operates on `sander` crashes; this env is the runtime that crash-recovery monitors.
- [[Infra_DPDispatcher]] — DPDispatcher in local-shell mode (`batch_type: "Shell"` + `LocalContext`) dispatches into this env's binaries.
- [[project-prime-status]] — Phase 2 step 1 closure point.
- [[Dev_Log]] — entry of 2026-05-19 logs this install.
