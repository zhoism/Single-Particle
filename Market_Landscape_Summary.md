---
tags: [report, market-research, summary, deliverable, brief]
type: report
status: for-advisor-review
date: 2026-05-28
companion: Market_Landscape_Report.md
---

# AI in Molecular Dynamics — Short Summary

**Author:** Kevin Zhou
**Date:** 2026-05-28


The workhorse of computational chemistry and drug discovery is Molecular Dynamics, which has the constraint of being slow, expensive and fragile. The industry is attempting to remedy through 3 ways: skipping the simulation (using a deep-learning model that can directly predict the answer with near quantum-accuracy), which save a lot of time, smarter physics engines (using machine-learned force fields that achieve near DFT accuracy with normal MD speed), and agentic orchestration (LLM agents that plan adn run the entire MD pipeline).  Mature pipelines from Schrödinger and OpenEye are the reliable-but-rigid baseline all of this is improving on. This project focuses on automatically recovering when a simulation crashes in the middle of a run. 

| Category | Company | Tool | What it does (plain English) | MD scenario |
|---|---|---|---|---|
| **Skip the sim** | Iambic Therapeutics | NeuralPLexer2 | Uses a diffusion model to predict a protein–drug complex's bound 3D shape directly, skipping the simulation. It's state-specific, so it can model the distinct functional states a protein switches between rather than one averaged structure. | Structure prediction |
| **Skip the sim** | Microsoft Research | BioEmu | Predicts a protein's whole equilibrium population of shapes in a single pass, so rare-but-important conformations like cryptic pockets appear without a long simulation. It tells you which shapes exist and how common they are, but not the order events happen in. | Conformational sampling |
| **Skip the sim** | Aqemia | Analytical binding solver | Estimates binding strength without simulating water: it solves one liquid-physics equation for where water settles around the molecule on a 3D grid and reads the binding energy straight out. Fast enough for large screens. | Binding affinity (screening) |
| **Skip the sim** | Isomorphic Labs | IsoDDE | A single model that predicts structure, binding strength, and hidden pockets directly from sequence. It benchmarks its binding numbers against the gold-standard physics method (FEP+) and claims parity without needing a crystal structure to start from. | Structure + affinity + pockets |
| **Skip the sim** | NVIDIA | ALCHEMI Conformer Search | Rapidly ranks thousands of candidate 3D shapes by stability on a GPU (10–100 ms each) to prune the unstable ones before any real simulation runs. A fast pre-filter, not a dynamics engine. | Fast structure screening (prep) |
| **Smarter physics** | Microsoft Research | AI2BMD | Runs real MD with a machine-learned force field that hits near-quantum accuracy at simulation speed. To fit a whole protein, it chops it into small overlapping pieces at runtime, computes accurate forces on each, and stitches them back every step. | High-accuracy MD |
| **Smarter physics** | Google DeepMind | GEMS | Another machine-learned force field for proteins, engineered for large systems (>25k atoms). It solves the big-protein problem in training — learning from both small molecules and quantum "chunks" of large proteins — so at runtime it simulates the whole protein with no stitching. | Protein-scale high-accuracy MD |
| **Smarter physics** | NVIDIA | ALCHEMI Batched MD | Not a new model but a deployment container that wraps an existing learned force field (MACE) and uses GPU batching to run thousands of independent simulations at once. Packaging applied to MD, for high throughput. | High-throughput dynamics |
| **Smarter physics** | Chodera Lab / OpenFF | Espaloma | Replaces brittle, rule-based simulation setup: a graph neural network writes the classical physics parameters directly onto each atom and bond, trained end-to-end against quantum data. Caveat: an unusual molecule can get unphysical parameters that crash the run. | Force-field setup (prep) |
| **Agentic** | Recursion | LOWE | An LLM agent that turns plain-English goals into validated, staged workflows and runs them. Its signature is a self-falsifying verifier that actively tries to disprove its own conclusions before acting on them. | Workflow orchestration |
| **Agentic** | Johnson & Johnson | Mol Agent | A multi-agent system that doesn't just run tools but autonomously builds the ML property-prediction models itself, with a three-agent hierarchy coordinating over a shared message bus. | ML automation (MD-adjacent) |
| **Agentic** | Artificial Inc. | Tippy | Runs an entire automated drug-discovery lab as containerized agents (one per role), with a dedicated tool-less "guardrail" agent that vets high-risk actions before they execute. | Lab / workflow infrastructure |
| **Baseline** | Schrödinger | FEP+ | The rigorous gold standard for binding strength: it gradually "morphs" one molecule into another and measures the energy cost along the way. Fully automated end-to-end, but a fixed, validated pipeline with no autonomous reasoning. | Binding free energy / lead optimization |
| **Baseline** | Schrödinger | Multisim | Automates sequential MD stages and, on a crash, does a bitwise-exact restart from the last checkpoint. It never changes a physics parameter on its own — that requires a human passing a `-set` flag. | Pipeline automation + partial recovery |
| **Baseline** | OpenEye / Cadence | Orion | A cloud workflow engine that routes each molecule down success / failure / custom branches at runtime — but only down branches a developer pre-wrote an `if` for, so a genuinely novel error stalls. | High-throughput screening + routing |

**Also surveyed — out of scope (materials domain).** Excluded from the matrix as competitors (they target inorganic materials, not biomolecular MD), but several carry mechanisms that could transfer at the idea level:

- **Schrödinger MPNICE** — ML force field with learned long-range electrostatics; the charge-equilibration mechanism could carry directly to a biomolecular force field.
- **Differentiable atomistic simulation** — makes the entire MD loop differentiable to tune force-field parameters; domain-agnostic in principle.
- **Microsoft MatterSim** — a universal ("foundation") ML force field across the periodic table; the endpoint of moving past per-system parameterization.
- **Google DeepMind GNoME** — active-learning stability screening of candidate crystals; the screening-loop pattern maps to pre-filtering candidates before MD.
- **GENIUS** — an agentic framework with a finite-state error-recovery machine (materials/DFT, setup stage); the nearest published analogue to autonomous simulation recovery.

**Bottom line:** the three approaches increasingly overlap and feed one another — prediction models pre-filter candidates, ML-accelerated engines speed the runs, and agents orchestrate the pipeline — so the practical question for any pipeline is which combination fits the problem at hand.

---

*Full problem-and-techniques write-up, the complete matrix, and sources are in [[Market_Landscape_Report]].*
