---
tags: [project-prime, gap, force-field, machine-learning, future-work]
type: gap
status: open
created: 2026-06-17
---

🟡 **Design idea / our framing — open gap, captured 2026-06-17** from a user question during the post-report maintenance pass ("would ML force fields help — are they any better than antechamber/GAFF2, or still a growing field?"). Not a planned build; a banked open question.

# Gap: Machine-learned force fields vs. the classical GAFF2/AM1-BCC core

## What the gap is

The pipeline parameterizes ligands with **GAFF2 + AM1-BCC** via [[Skill_Antechamber_LigandPrep|antechamber]] — a fixed-functional-form classical force field. **Machine-learned force fields (MLFFs)** are a fast-moving alternative the project has never evaluated. Open question: would any MLFF flavor improve our deliverable (automated solvated protein–ligand MM-GBSA), and at what cost to the architecture?

## The three flavors (do not conflate)

1. **Full NN potentials** (ANI-2x, MACE-OFF, AIMNet2) — learn the PES from QM. More accurate on small-molecule energetics, but **10²–10⁴× MM cost** → impractical for our solvated boxes (~6k+ atoms, ns sampling).
2. **ML/MM hybrids** — ligand (or active site) on the MLFF, protein+water classical. Where the field is genuinely moving for binding; tooling still research-grade.
3. **ML parameterization** (espaloma-style) — a graph-NN assigns *classical-form* charges/torsions; output is a normal `prmtop` at normal MM cost. **The architecture-preserving option.**

## The honest assessment (2026-06-17)

- MLFFs *are* better at QM-accuracy for isolated small molecules, and the field is maturing fast (foundation models 2023–2025). But **our accuracy ceiling is MM-GBSA's end-point / implicit-solvent approximations, not GAFF's torsions** — a better force field improves the wrong link if the goal is better ΔG.
- **Tension with the project thesis (the interesting part):** our value-add is *cheap deterministic proxy-invariant gates* (integer charge, discrete aromatic atom-types, atom-count arithmetic). A full NN potential **has no atom types to gate** and fails silently via **out-of-distribution extrapolation** — the honest "gate" becomes uncertainty / OOD detection, which is hard to make cheap + deterministic. So a full MLFF partially dissolves what makes the pipeline trustworthy. This is the real reason it isn't a clean swap.

## What it implies if pursued

- **Do NOT** adopt full MLFF MD now (cost + immature tooling + breaks the gate model).
- **DO** treat **ML parameterization (espaloma)** as the scoped experiment: cheap, architecture-preserving (still emits a gate-inspectable `prmtop`), upgrades GAFF's genuine weak spot (ligand charges/torsions). It is a swap at the ligand-prep skill, not an architecture change — the [[Design_Skill_Decomposition|skill boundary]] is force-field-agnostic by construction.
- A deeper open question worth a gate-discipline pass: **what is the cheap deterministic gate-equivalent for an OOD MLFF prediction?** Ties directly to the systematic-coverage discipline of the [[Next_Session_Prompt_AMBER_FailureMode_Sweep|failure-mode sweep]].

## Distinct from

[[Arch_Iambic_NeuralPLexer]] — that is the *replace-the-simulation* surrogate pole on the [[Design_Determinism_Spectrum]]; this gap is about a *better force field inside* the physics-based simulation. Different axis — don't collapse them.
