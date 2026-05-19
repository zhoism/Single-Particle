---
tags: [market-research, architecture, multi-agent, lab-automation]
---
# Architecture: Artificial Inc. "Tippy"

**Core Concept:** A comprehensive multi-agent blueprint for end-to-end drug discovery and laboratory automation.

**Agent Hierarchy (6-Part):**
1.  **Supervisor Agent:** Central brain; maintains and shares context across all sub-agents.
2.  **Molecule Agent:** The computational chemist. Converts molecules to SMILES, runs GPU property predictions, and utilizes generative models.
3.  **Lab Agent:** The workflow engine. Uses MCPs to interact with lab hardware, start jobs, and query status.
4.  **Analysis Agent:** Handles data science and statistical analysis.
5.  **Report Agent:** Compiles experimental data into Markdown and PDFs.
6.  **Safety Guardrail Agent:** A compliance monitor with no external tools. Sits at the top to filter harmful/dangerous outputs.

**Infrastructure:**
* **Containerization:** Fully Dockerized and orchestrated by Kubernetes (each agent isolated in a pod).
* **Networking:** Envoy Proxy used for secure communication.
* **Communication:** Heavy reliance on MCP Servers.
* **State Management:** Git-based tracking for all agent changes to ensure reproducibility.

- > **Related Architecture:** The Supervisor Agent here functions similarly to the Planner-Executor Loop in [[Arch_Recursion_LOWE]].

**Source:** *"Technical Implementation of Tippy: Multi-Agent Architecture and System Design for Drug Discovery Laboratory Automation"* — https://arxiv.org/pdf/2507.17852 (full raw notes in [[Research_Phase1_Survey]]).