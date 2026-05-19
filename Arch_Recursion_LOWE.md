---
tags: [market-research, architecture, workflow-engine, verification]
---
# Architecture: Recursion Pharmaceuticals "LOWE"

**Core Concept:** An LLM-orchestrated workflow engine acting as the central brain for the Recursion OS, connecting to foundational models like Boltz-2 and SynFlowNet.

**Key Features to Borrow for OpenClaw:**
* **Planner-Executor Loop:** A central planner evaluates the current state of the project and invokes specific execute skills to move the project forward.
* **Mechanistic Action Graphs:** Used by the LLM to represent complex biological and chemical knowledge.
* **Strict Verifier Approach (Critical):** Simulates the scientific method.
    * Sub-agents retrieve knowledge and propose a hypothesis/parameter set.
    * A deterministic *Verifier Agent/Script* attempts to falsify the argument or parameters before any real compute is executed.
    * Applies a refining cycle: Predict -> Test -> Falsify -> Improve (highly applicable to error handling if a simulation crashes).

**Sources:**
- LOWE landing page — https://www.recursion.com/lowe
- Mechanistic-action-graph paper — https://arxiv.org/pdf/2604.11661
- Related VCR-Agent implementation — https://github.com/valence-labs/VCR-Agent
- Full raw notes in [[Research_Phase1_Survey]].