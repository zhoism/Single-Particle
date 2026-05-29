---
tags: [report, market-research, deliverable]
type: report
status: for-advisor-review
date: 2026-05-28
companion: Market_Landscape_Summary.md
---

# AI in Molecular Dynamics — The Problem and the Techniques Solving It

**Author:** Kevin Zhou
**Date:** 2026-05-28

**Summary.** Molecular dynamics (MD) is the physics-based engine of computational drug discovery, but it is slow, costly, and prone to failure. The current wave of AI addresses this on three fronts: predicting MD's results directly to *skip the simulation*, building *smarter physics engines* that are both fast and accurate, and wrapping the pipeline in *AI agents* that plan and run it. Each front clears real bottlenecks, but none addresses the one that proves most disruptive in practice: a simulation that crashes mid-run with no operator present to intervene. That gap is the focus of this project.

---

## Part 1 — The problem

**What MD does.** A molecular-dynamics simulation takes a protein (often a drug target) and a candidate molecule, places them in a box of water, and steps forward in tiny time increments — roughly a femtosecond (a millionth of a billionth of a second) at a time — recalculating the forces on every atom at each step. Over enough steps, this reveals how the molecule moves, whether it remains bound, and how tightly it holds. That last quantity — **binding strength** — is the value drug discovery prioritizes most. MD is powerful because it is grounded in real physics rather than pattern-matching, but that grounding is also what makes it expensive and brittle. Six bottlenecks recur:

1. **Timescale / rare events.** The motions that matter biologically — a protein folding, a hidden ("cryptic") pocket opening — occur rarely and on timescales far longer than a feasible simulation can reach. A simulation may run for weeks without ever reaching the event of interest. Simulations are on th escale of femtoseconds, sometimes we want phenomena that are on the millisecond/second scale. This problem is the rare event sampling problem. 

2. **Accuracy vs. cost.** The most accurate way to compute the forces (quantum chemistry) is far too slow for anything protein-sized. The fast approximation in standard use (a *force field* — a fixed set of physics rules) is good but rough, and that roughness limits how far the result can be trusted.

3. **Throughput.** Drug discovery requires screening thousands to millions of candidate molecules. Running a full simulation for each, sequentially, does not scale.

4. **Setup brittleness.** Before a simulation can begin, the system must be prepared — assigning physics parameters to every atom and selecting sensible starting 3D shapes. This preparation is manual, intricate, and unforgiving: a single mis-typed atom or unusual chemical group causes the setup tools to reject the input or, worse, silently produce a configuration that destabilizes later.

5. **Binding affinity is expensive.** The single most valuable output — binding strength — requires especially heavy, careful sampling to compute rigorously, making it the costliest task MD is routinely asked to perform.

6. **Runtime fragility.** Even a correctly prepared run can crash mid-flight — a temperature spike, a numerical instability, a cluster timeout. At present this requires a person to notice the failure, read the logs, adjust a parameter, and restart. A failure outside working hours leaves the run idle until someone intervenes.

---

## Part 2 — The techniques attacking it

### Skip the simulation *(attacks #1 rare events, #5 affinity cost; pruning attacks #4 setup)*

**The idea:** rather than running a long simulation, train a deep-learning model on existing data to *predict the result directly* — the bound 3D structure, the range of shapes a protein takes, or the binding strength. 

A related approach uses a fast model to **prune** obviously poor candidate structures in advance, so that costly computation is spent only on promising candidates.


**How it works.** Most are *diffusion* models — the same family as image generators — trained on large structural databases, producing a physically plausible result in one pass rather than integrating a trajectory step by step. The distinguishing approach of each tool:

- **Iambic — NeuralPLexer2.** Predicts the *bound* protein–drug complex directly, and is **state-specific**: rather than one averaged structure, it can model the distinct functional states a protein switches between.

- **Microsoft — BioEmu.** Predicts not one structure but the protein's whole *equilibrium population* of shapes, so rare but important conformations (cryptic pockets, folding intermediates) emerge in a single pass rather than after a long simulation. The trade-off: it identifies which shapes exist and their relative populations, but not the order in which events occur (no kinetics).

- **Aqemia.** Notably avoids deep learning for the core calculation: rather than simulating thousands of water molecules, it solves a single liquid-physics equation for where water density settles around the molecule on a 3D grid, and reads binding strength directly from the result.

- **Isomorphic Labs — IsoDDE.** Distinct for its unification: a single model predicts structure, binding strength, and hidden pockets from sequence, and benchmarks its binding numbers against the gold-standard physics method (FEP+), reporting parity without requiring a crystal structure as a starting point.

- **NVIDIA — ALCHEMI Conformer Search.** Optimized for throughput: it processes thousands of candidate shapes through a fast neural potential on a GPU simultaneously (10–100 ms each), ranking them by stability to discard unstable candidates before any simulation runs.

**The limit:** a model that predicts in one pass cannot capture the fine-grained motion real MD provides, and it becomes unreliable on molecules unlike those in its training data. These tools are best treated as a fast first pass that *feeds* physics-based MD, not a wholesale replacement.


### Smarter physics engines / ML force fields *(attacks #2 accuracy-vs-cost; helps #3 throughput, #4 setup)*

**The idea:** continue running real MD, but replace the rough physics rules with ones a model has learned from accurate quantum-chemistry data — delivering near-quantum accuracy at near-classical speed and closing the longstanding accuracy-vs-cost trade-off.

**How it works.** The model is trained on millions of high-accuracy quantum calculations/DFT until it can predict the forces on atoms almost as well as quantum chemistry, but fast enough to run a real trajectory. The distinguishing approach of each group:



- **Microsoft — AI2BMD.** Addresses the model's size limitation at **runtime**: it divides the protein into small overlapping fragments (capped dipeptides), computes accurate forces on each, and reassembles them at every step.

- **Google DeepMind — GEMS.** Addresses the same problem during **training** instead: it learns from both small molecules and quantum "chunks" extracted from large proteins, so it natively represents long-range structure and at runtime simulates the entire protein without reassembly (demonstrated on solvated proteins exceeding 25,000 atoms). The contrast with AI2BMD is instructive: AI2BMD fragments at runtime; GEMS fragments during training.

- **NVIDIA — ALCHEMI Batched MD.** Notably not a new model: it is a deployment container wrapping an existing learned potential (MACE), using GPU batching to run thousands of independent simulations at once — packaging applied to MD.

- **Chodera Lab — Espaloma.** Represents the molecule as a graph and uses a graph neural network to write the classical physics parameters directly onto each atom (node) and each bond/angle/torsion (edge), trained end-to-end by optimization against quantum data rather than retrieved from hand-written rule tables. A limitation: because it populates a *classical* force field, an unusual molecule can receive unphysical parameters that destabilize the simulation later — precisely the runtime failure this project's recovery layer is designed to catch.

**The limit:** this wave is still early. For routine protein–drug work, classical force fields remain the validated production standard, and the learned engines are not yet a drop-in replacement.



**Emerging — making the whole simulation differentiable.** A distinct research direction (Gangan et al., 2025) extends the principle behind Espaloma: it turns the *entire* MD loop into one differentiable function, so that an error in the final measured property can be back-propagated through thousands of timesteps to automatically tune the underlying force field — training the simulator itself like a neural network. Where Espaloma makes the *parameter-fitting* step differentiable, this makes the *whole trajectory* differentiable. To date it has been demonstrated only on **materials** (silicon/silica), not biomolecules, and it is memory-intensive (the entire timestep history must be held for the backward pass) — so it is currently an upstream *force-field-development* technique that warrants monitoring, not a drop-in for protein–drug MD.

### Agentic orchestration *(attacks the human-supervision burden across all of the above)*

**The idea:** use an LLM "agent" to translate a plain-language scientific goal into a validated, step-by-step workflow and run the pipeline — while deliberately keeping the LLM *out* of the physics math, so it cannot hallucinate chemistry.

**How it works.** The agent proposes the plan, but a separate deterministic engine executes the chemistry; the LLM's outputs are constrained to structured, schema-checked form rather than free text; information the agent holds is tagged by origin (observed vs. inferred) and it cannot act on inferences; high-risk steps pass through approval gates. The distinguishing approach of each:

- **Recursion — LOWE.** Its defining feature is a self-falsifying **verifier**: before acting on a conclusion, a separate agent attempts to disprove it (predict → test → falsify → improve) — the pattern this project's error-recovery loop adopts.
- **Johnson & Johnson — Mol Agent.** Distinct in that the agents do not merely run tools but autonomously build the ML property-prediction models themselves, coordinated as a three-agent hierarchy over a shared message bus (MCP).
- **Artificial Inc. — Tippy.** Characterized by isolation and a dedicated safety layer: one container per agent (Docker/Kubernetes), plus a separate tool-less "guardrail" agent that vets high-risk actions before execution.
- **PRISM / CADD-Agent (ZJUIQB).** A protein–ligand pipeline built on GROMACS — unifying ligand parameterization across force fields, system construction, enhanced sampling, multi-tier binding free energy estimation, and trajectory analysis — orchestrated by an agent through Claude Code and MCP. Its automated error handling is setup-stage (fixing GROMACS atom-naming and parameterization memory errors), not mid-run recovery; it is the closest in-domain analogue to this project's preparation and orchestration layers.

**The limit:** orchestration makes pipelines easier to operate, but it does not by itself solve any MD physics — it organizes the work; it does not make the simulation faster or more accurate.

### The established baseline *(the reliable but rigid incumbents)*

These are mature, heavily validated pipelines — dependable but rigid: they follow fixed scripts and do not reason or adapt. They are the standard the three trends above seek to improve upon. Their distinguishing characteristics:

- **Schrödinger — FEP+.** The rigorous gold standard for binding strength: it gradually "morphs" one molecule into another and measures the energy cost along the way. Fully automated end-to-end, but a fixed, validated pipeline without autonomous reasoning.
- **Schrödinger — Multisim.** Its recovery behavior: on a crash it performs a bitwise-exact restart from the last checkpoint, but it never alters a physics parameter autonomously — that requires a human passing a `-set` flag.
- **OpenEye / Cadence — Orion.** Its distinguishing feature is genuine runtime branching: workflows route each molecule down success / failure / custom paths, but only along branches a developer has pre-coded with an `if`, so a genuinely novel error stalls.

---

## Part 3 — The unsolved piece, and the proposed approach *(attacks #6 runtime fragility)*

Every technique above speeds up, sharpens, or automates the **planning** of MD. None addresses the moment a running simulation actually **crashes** without a human present. The skip-the-sim and physics-engine tools run no trajectory to recover, so the problem does not arise for them; the agentic tools orchestrate but do not modify physics; and the incumbents only restart from a checkpoint — which simply re-crashes if the physics itself was unstable.

This is the gap the proposed system targets: **autonomous, mathematically-bounded recovery from MD runtime failures.** The approach is tiered, so that the safe move is always attempted first:

- **Tier 1 — safe checkpoint-restore.** For transient failures (hardware faults, cluster timeouts), resume from the last good checkpoint. Zero physics risk.
- **Tier 2 — bounded parameter mutation.** *Only* if Tier 1 re-crashes near the same step, the agent adjusts the simulation's physics within hard, pre-defined limits (timestep `dt ≤ 2 fs`, a valid interaction cutoff, SHAKE constraints enabled), then resumes.

The governing discipline is that **mutation is always the escalation, never the first move.** This answers a natural objection — that the system permits an AI to alter simulation physics. It does not improvise; it applies a small set of validated, mathematically-constrained fixes only after the safe option has failed. This allows the orchestration layer not only to plan and launch simulations but to keep them running unattended — the capability the rest of the field still delegates to manual intervention.

**Adjacent prior work (materials).** GENIUS (*Nature Communications Materials*, 2026) is the nearest published analogue: an agentic framework for first-principles materials simulation (Quantum ESPRESSO) with a finite-state error-recovery machine that autonomously repairs ~76% of failed runs. Its recovery operates at the *setup* stage — reading the program's error messages, regenerating a valid input file, and restarting from a clean template — rather than mutating the physics of a running trajectory, and it targets static DFT for inorganic materials (the authors note molecular dynamics as a possible future extension). It demonstrates the same autonomous-recovery concept applied to a different domain and failure mode.

---

## Surveyed and excluded (scope boundary)

For completeness, several systems were surveyed and deliberately left out of the matrix above.

**Materials-domain — excluded as competitors, but several carry transferable ideas.** These are materials / condensed-phase tools, so they are not biomolecular-MD competitors and do not belong in the matrix. But "excluded as a competitor" is not "irrelevant as an idea": several attack problems that also exist in biomolecular MD, and their *mechanisms* are not all domain-bound. The connections below are at the idea level — none has been demonstrated on biomolecules — and they range from deep (the mechanism transfers directly) to loose (only the pattern transfers).

- **Microsoft MatterSim** — a universal ML force field for inorganic crystals across the periodic table. *Transferable idea (moderate):* the foundation-model force-field ambition — one broadly pre-trained potential instead of per-system parameterization. Pushed to biomolecules, that is the endpoint of the AI2BMD/GEMS trajectory, and it could eventually erode the brittle per-ligand atom-typing this project's prep skill exists to handle. https://arxiv.org/abs/2405.04967 · https://github.com/microsoft/mattersim
- **Schrödinger MPNICE** — an ML force field whose differentiator is *iterative charge equilibration* for long-range electrostatics (liquids, crystals, organometallics). *Transferable idea (deep — the strongest here):* long-range electrostatics is a central problem in biomolecular MD too (solvent and ion screening), and a learned charge-equilibration scheme is mechanism-level applicable to a biomolecular ML force field — the same gap GEMS addresses. Only the training domain differs. https://arxiv.org/abs/2505.06462
- **Differentiable atomistic simulation** (UCLA / DeepMind / OpenAI) — makes the *entire* MD loop differentiable to optimize force-field parameters by back-propagation through the trajectory (the technique flagged in Part 2; demonstrated on Si/SiO₂). *Transferable idea (deep):* the method is domain-agnostic in principle — the same machinery could tune a biomolecular force field (ff14SB/GAFF) against experimental observables. The barrier is practical (the whole trajectory must be held in memory for the backward pass), not conceptual. https://doi.org/10.1021/acs.jctc.4c01784
- **Google DeepMind GNoME** — a GNN that predicts the static stability of hypothesized inorganic crystals inside an active-learning loop (≈2.2M predicted, ~380k stable). *Transferable idea (loose):* the *loop pattern* — cheaply predict which candidates are viable, run the expensive calculation only on the survivors, feed results back to retrain — maps onto a pre-filter for proposed ligands, poses, or mutants upstream of MD, cutting wasted runs. The crossover is the screening loop, not the model itself: crystal lattice stability and biomolecular conformational stability are different physics. https://www.nature.com/articles/s41586-023-06735-9 · https://github.com/google-deepmind/materials_discovery

**Adjacent biomolecular tools (excluded with reason).**
- **Exscientia** — its relative binding free energy pipeline (ML/MM end-state corrections around classical AMBER/GROMACS) is an orthogonal *accuracy* play, not a recovery or orchestration one; now part of Recursion. https://doi.org/10.1021/acs.jctc.4c01427
- **Insilico Medicine — Chemistry42** — a generative-design platform whose reward loop is driven by *docking* plus ligand-based/ADMET scoring, not explicit-solvent MD; it sits in the agentic-orchestration tier rather than MD mechanics. https://doi.org/10.1021/acs.jcim.2c01191

**Background (methodology, not a competitor).**
- Zhu et al., *Enhanced Sampling in the Age of Machine Learning*, *Chem. Rev.* (2025) — the in-MD route to rare-event sampling (learned collective variables, neural biasing potentials), contrasting with the skip-the-simulation emulators above. https://doi.org/10.1021/acs.chemrev.5c00700

---

## Reference table

| Category | Company | Tool | What it does (plain English) | MD scenario |
|---|---|---|---|---|
| **Skip the sim** | Iambic Therapeutics | NeuralPLexer2 | Predicts a protein–drug complex's 3D shape directly | Structure prediction |
| **Skip the sim** | Microsoft Research | BioEmu | Predicts the full range of shapes a protein flexes through | Conformational sampling |
| **Skip the sim** | Aqemia | Analytical binding solver | Estimates binding strength analytically, with no trajectory | Binding affinity (screening) |
| **Skip the sim** | Isomorphic Labs | IsoDDE | Predicts structure, binding strength, and hidden pockets from sequence | Structure + affinity + pockets |
| **Skip the sim** | NVIDIA | ALCHEMI Conformer Search | Rapidly ranks candidate 3D shapes to prune unstable ones before simulating | Fast structure screening (prep) |
| **Smarter physics** | Microsoft Research | AI2BMD | Quantum-level accuracy at simulation speed, for proteins | High-accuracy MD |
| **Smarter physics** | Google DeepMind | GEMS | Same idea, engineered for large proteins (>25k atoms) | Protein-scale high-accuracy MD |
| **Smarter physics** | NVIDIA | ALCHEMI Batched MD | Runs thousands of learned-physics simulations in parallel on GPUs | High-throughput dynamics |
| **Smarter physics** | Chodera Lab / OpenFF | Espaloma | Uses ML to auto-set a simulation's physics parameters, replacing a brittle step | Force-field setup (prep) |
| **Agentic** | Recursion | LOWE | Turns plain-English goals into validated workflows; checks its own work | Workflow orchestration |
| **Agentic** | Johnson & Johnson | Mol Agent | Multi-agent system that auto-builds property-prediction models | ML automation (MD-adjacent) |
| **Agentic** | Artificial Inc. | Tippy | Containerized multi-agent platform running an automated lab | Lab / workflow infrastructure |
| **Agentic** | ZJUIQB | PRISM / CADD-Agent | GROMACS protein–ligand pipeline (parameterization, sampling, binding free energy) orchestrated via Claude Code + MCP; setup-stage error fixes, not runtime recovery | Protein–ligand MD orchestration |
| **Baseline** | Schrödinger | FEP+ | Mature automated pipeline for accurate binding-strength prediction | Binding free energy / lead optimization |
| **Baseline** | Schrödinger | Multisim | Automates MD stages; restarts from a checkpoint after a crash (no physics change) | Pipeline automation + partial recovery |
| **Baseline** | OpenEye / Cadence | Orion | Routes around *known* failures via pre-coded rules | High-throughput screening + routing |

---

## Sources

*All links verified 2026-05-25 → 28.*

**Skip the simulation**
- Iambic NeuralPLexer2 — *Nature Machine Intelligence* (2024): https://www.nature.com/articles/s42256-024-00792-z · vendor: https://www.iambic.ai/post/np2
- Microsoft BioEmu — *Science* (2025): https://doi.org/10.1126/science.adv9817 · repo: https://github.com/microsoft/bioemu
- Aqemia — biomolecular application (1,400 FDA drugs vs SARS-CoV-2 3ClPro), arXiv:2109.03565: https://arxiv.org/abs/2109.03565 · foundational physics (FreeSolv hydration), *JCIM* (2020): https://doi.org/10.1021/acs.jcim.0c00526 · https://www.aqemia.com/
- Isomorphic Labs IsoDDE — technical report (Feb 2026): https://storage.googleapis.com/isomorphiclabs-website-public-artifacts/isodde_technical_report.pdf · announcement: https://www.isomorphiclabs.com/articles/the-isomorphic-labs-drug-design-engine-unlocks-a-new-frontier
- NVIDIA ALCHEMI Conformer Search — ALCHEMI blog: https://developer.nvidia.com/blog/faster-chemistry-and-materials-discovery-with-ai-powered-simulations-using-nvidia-alchemi/

**Smarter physics engines / ML force fields**
- Microsoft AI2BMD — *Nature* (2024): https://doi.org/10.1038/s41586-024-08127-z · repo: https://github.com/microsoft/AI2BMD
- Google DeepMind GEMS — *Science Advances* (2024): https://doi.org/10.1126/sciadv.adn7397 · publication page: https://deepmind.google/research/publications/88551/
- NVIDIA ALCHEMI Batched MD — NIM docs: https://docs.nvidia.com/nim/alchemi/alchemi-bmd/latest/overview.html · container: https://catalog.ngc.nvidia.com/orgs/nim/teams/nvidia/containers/alchemi-bmd
- Chodera Lab / OpenFF Espaloma — *Chemical Science* (2024): https://doi.org/10.1039/D4SC00690A · original method: https://arxiv.org/abs/2010.01196 · repo: https://github.com/choderalab/espaloma

**Emerging — differentiable simulation**
- Differentiable atomistic simulation — Gangan et al., *JCTC* (2025): https://doi.org/10.1021/acs.jctc.4c01784 (demonstrated on Si/SiO₂ materials, not biomolecules — an upstream force-field-development technique).

**Agentic orchestration**
- Recursion LOWE — https://www.recursion.com/lowe · companion paper: https://arxiv.org/abs/2604.11661
- Johnson & Johnson Mol Agent — *JCIM* (2025): https://pubs.acs.org/doi/pdf/10.1021/acs.jcim.5c01938
- Artificial Inc. Tippy — https://arxiv.org/abs/2507.17852
- PRISM / CADD-Agent (ZJUIQB) — *bioRxiv* (2026): https://www.biorxiv.org/content/10.64898/2026.04.02.716083v1 · repo: https://github.com/AIB001/PRISM

**Established baseline**
- Schrödinger FEP+ — https://www.schrodinger.com/platform/products/fep/
- Schrödinger Multisim — https://learn.schrodinger.com/public/python_api/2022-1/api/schrodinger.application.desmond.multisimstartup.html
- OpenEye / Cadence Orion — https://www.eyesopen.com/orion/platform

**Adjacent — autonomous recovery (materials domain)**
- GENIUS — *Nature Communications Materials* (2026): https://www.nature.com/articles/s43246-026-01167-0 · arXiv:2512.06404: https://arxiv.org/abs/2512.06404 (Quantum ESPRESSO / DFT; finite-state setup-error recovery; MD noted as future work).

**Substrate (agentic framework + bounded-recovery case study)**
- OpenClaw — https://arxiv.org/abs/2603.25522 (planning/execution split, approval gates, bounded recovery with a methane-oxidation case study).
