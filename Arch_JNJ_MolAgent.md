---
tags: [market-research, architecture, machine-learning, mol-agent]
---

**Implementation Link:** To build the Strict Verifier without LLM hallucination, we must use the deterministic routing outlined in [[OpenClaw_Lobster_DAGs]].
# Architecture: J&J Mol Agent

**Core Concept:** Automates the role of a Machine Learning Engineer. Tests algorithms/features to find the best fit for molecular datasets and outputs trained PyTorch models for prediction.

**Key Features:**
* **Data Translation:** Converts raw molecular data into ML formats (2D features, RDKit descriptors, molecular fingerprints via bottleneck transformer).
* **3D Integration:** Uses affinity graphs and protein-ligand interaction fingerprints.
* **Model Verification:** Partitions data rigorously to prevent overfitting (ensures structurally related molecules aren't arbitrarily split). Uses "nested cross-validation" for unbiased model selection.
* **Ensemble Methods:** Combines simple algorithms into higher-performing mega-models.
* **Adjustable Workloads:** Tasks can be scaled (Cheap vs. Medium vs. Hard).

**Agent Hierarchy (3-Part):**
1.  **Manager Agent:** Parses user prompt and routes to specialized agents.
2.  **Data Retrieval Agent:** Extracts datasets, preprocesses, and standardizes inputs.
3.  **Model Training Agent:** Executes ML tasks and evaluates performance via MCP servers.

- > **Future Implementation:** The model evaluation strategies here could provide the reward signals needed for the reinforcement learning loops described in [[OpenClaw_Self_Evolution]].

**Source:** *J. Chem. Inf. Model.* paper — https://pubs.acs.org/doi/pdf/10.1021/acs.jcim.5c01938 (full raw notes in [[Research_Phase1_Survey]]).