---
tags:
  - project-prime
  - vocabulary
type: controlled-vocabulary
status: living
---

# Controlled Vocabulary — Project Prime

**Purpose.** This is the canonical term list for the vault. Vocabulary drift — describing the same concept with different words across notes — silently breaks cross-note reasoning and `[[wikilink]]` traversal. Before introducing a new term for a concept, check here first. If the concept already exists under a name, use that name. If it is genuinely new, add it here before using it elsewhere.

This list is *adopted selectively* from the "Knowledge Network" CLAUDE.md pattern. The vault deliberately does **not** use that pattern's `confidence:` frontmatter or typed-edge schema — confidence is already carried by the existing systems below, and edges are plain `[[wikilinks]]`.

---

## Confidence & provenance (use the existing systems — do not invent new ones)

- **Tier badges** (note-level source confidence): `✅ paper/source-cited` · `🟡 design idea / our framing` · `⚪ aspirational`. Put the badge at the top of a note. See [[Dev_Log]] 2026-05-19 for when this discipline was established.
- **Memory Provenance** (rule-level execution trust, 4 labels): `observed`, `confirmed`, `inferred`, `imported from transcript`. Sourced to **OpenBrain** (not the OpenClaw paper). `inferred` output must be verified before execution; `imported from transcript` is treated as `inferred` by default. Canonical note: [[Design_Memory_Provenance]].

---

## Agent framework

- **OpenClaw** — the agent framework (lowercase-C "Claw"). Not "OpenClaude", not "Open Claw".
- **Lobster DAGs** / **Lobster engine** — OpenClaw's deterministic workflow engine. Canonical: [[OpenClaw_Lobster_DAGs]].
- **approval gates** — human-in-the-loop checkpoints in the Lobster engine.
- **llm-task** — OpenClaw's LLM-reasoning task primitive.
- **MetaClaw / OpenClaw-RL** — the self-evolution / RL direction. Tier ⚪ aspirational, out of report scope. Canonical: [[OpenClaw_Self_Evolution]].
- **Taskboard Manifest** — the lazy-loaded, stage-validated planning spec. A planner-agent design idea (plan-and-execute pattern), not OpenClaw-novel. Canonical: [[Arch_Taskboard_Manifest]].
- **decoupled hybrid agent** — the architecture: LLM reasoning separated from domain execution. Three layers: **planning**, **deterministic execution**, **HPC grounding**.

## Simulation engine & tooling

- **AMBER** — the MD suite. **AmberTools** (currently `24.8`) is the open toolset within it.
- **sander** — CPU MD engine (the one in use; CPU-only Mac).
- **pmemd.cuda** — GPU MD engine. Not available locally (no NVIDIA); relevant only under a remote GPU backend — see [[Gap_Remote_HPC_Backend]].
- **tleap** — system/topology builder. (Not "xleap", not "LEaP" in prose.)
- **antechamber** — ligand atom-typing + charge assignment.
- **parmchk2** — fills missing force-field parameters (frcmod).
- **pdb4amber** — PDB cleanup for AMBER.
- **CPPTRAJ** — trajectory analysis tool. Spelled all-caps for the tool; the binary is `cpptraj`.
- **obabel** (Open Babel) — SMILES→3D conversion in ligand prep.
- **PLIP** — Protein-Ligand Interaction Profiler (post-processing).
- **smoke test** — the fast env-sanity check at `project-prime/smoke-test/` (isolated protein-only + ligand-only legs). Not the real workflow.
- **golden path** — the canonical *end-to-end* reference recipe at `project-prime/golden-path/`: a real protein–ligand complex (the **T4 lysozyme L99A + benzene** positive control, PDB `181L`) driven through the entire pipeline (prep → build → MD → cpptraj → PLIP). This is the known-good recipe the OpenClaw skills automate; it is engine-agnostic (the `ENGINE` seam swaps `sander`↔`pmemd` for the HPC future — see [[Gap_Remote_HPC_Backend]]).

## Force fields & parameters

- **ff14SB** — protein force field.
- **GAFF2** — general AMBER force field for small molecules.
- **AM1-BCC** — semi-empirical charge method used by antechamber.
- **TIP3P** — explicit water model.

## MD physics parameters (hard limits are non-negotiable)

- **dt** — integration time step. Hard limit **`dt ≤ 2 fs`** (with SHAKE). On crash, lower it.
- **cut** — non-bonded cutoff distance.
- **SHAKE** — bond-length constraint enabling 2 fs steps.
- **mdin** — AMBER MD input file (the structure skills parse/modify).
- **minimization / heat / equilibration / production** — the standard MD stage sequence.
- **NVT** — constant-volume ensemble (`ntb=1, ntp=0`); used for heat and production here.
- **NPT** — constant-pressure ensemble (`ntb=2, ntp=1` + a **barostat**); the equilibration stage that settles solvent density. The **MC barostat** (`barostat=2`) is the one in use.
- **addions / neutralize** — tleap step adding counterions (Cl⁻/Na⁺) to bring net charge to 0 before MD.
- **RMSD / RMSF / RoG** — structural stability / residue flexibility / radius of gyration (CPPTRAJ outputs).

## HPC & dispatch

- **DPDispatcher** — job-dispatch layer. Canonical: [[Infra_DPDispatcher]].
- **LocalContext** + **`batch_type: "Shell"`** — DPDispatcher local-shell mode (current execution path; verified 2026-05-19).
- **Slurm / PBS** — remote HPC schedulers (relevant only under a remote backend — see [[Gap_Remote_HPC_Backend]]).

## Environment & providers

- **`prime-amber`** — the canonical conda env (AmberTools 24.8 + PLIP, osx-arm64 native). Activate before any AMBER binary.
- **conda / mamba** — env manager (mamba for solves).
- **Google AI Studio** — the agent's LLM provider (locked 2026-05-20). **Gemini Flash** = default; **Gemini Pro** = heavy-reasoning calls.
- **Ollama** — *deprecated term*: local-LLM path was dropped 2026-05-20 (insufficient Mac headroom). Do not propose Ollama paths.

## Note prefixes (taxonomy)

`Arch_` · `OpenClaw_` · `Infra_` · `Skill_` · `Workflow_` · `Design_` · `Research_` · `Phase_` (reports) · `Gap_` (open problems) · `Dev_Log` (chronological log) · `vocabulary.md` (this file). See CLAUDE.md for the role of each.
