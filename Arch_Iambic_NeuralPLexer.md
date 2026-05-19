---
tags: [architecture, competitor, ml-prediction, scoped-out, structure-prediction]
---
# Architecture: Iambic Therapeutics — NeuralPLexer2

**Core Concept:** A diffusion model that predicts 3D protein–ligand structures directly — positioned to *replace* traditional MD simulation rather than orchestrate it. Conceptually adjacent to AlphaFold; an ML-prediction approach, not an agentic-workflow approach.

**Why it's in the survey but deliberately scoped out:**
* Project Prime automates *running and recovering real MD/AMBER simulations* with an agent. NeuralPLexer2 sits in the orthogonal camp that argues you can skip the simulation and predict the answer.
* It has **no agent, no workflow orchestration, no recovery layer** — there is nothing here to borrow for an OpenClaw skill.
* Surveying it is still report-valuable: it shows Phase 1 consciously considered the "ML replaces MD" thesis and made a deliberate choice to stay in the MD-automation lane. That is a defensible scoping decision, not an oversight.

**One-line placement:** It is the far "remove the simulation entirely" pole on the [[Design_Determinism_Spectrum]] — useful as a boundary marker for the survey, not as a design input.

**Source:** User Phase 1 competitive-landscape research, 2026-05-18 (Round 2). Raw notes in [[Research_Phase1_Survey]].
