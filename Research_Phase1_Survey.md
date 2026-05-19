---
tags:
  - research
  - market-survey
  - phase-1
  - openclaw
  - amber
type: research-source
status: in-progress
---

# Research: Phase 1 Market Survey (User Source Notes)

**Origin:** User-authored market research, imported 2026-05-14. This note is the *raw source* — refined distillations live in the `Arch_*`, `OpenClaw_*`, `Design_*`, `Skill_*` notes that cross-link below. Image embeds in the original (`![][image1]`) are not preserved; refer to the cited papers for figures.

---

## Defining the Objective: What are OpenClaw Agent Skills in MD context?

- LLMs are a brain; OpenClaw is a way for the brain to execute.
- A **skill** is a `skill.md` file that teaches an agent how to interact with a specific external tool, script, or API. For this project, we're teaching it how to run, debug, and analyze MD (and DFT-adjacent) code and results — translating the user's scientific goals into an executable.
- A monolithic skill is too broad. We decompose into subskills:
  - Setup skill
  - Parameter validation skill
  - HPC skill
  - Analysis skill

→ Distilled into [[Design_Skill_Decomposition]].

---

## Analysis of Industry Trends

### Johnson & Johnson — Mol Agent

**Summary**

The idea of a **Mol Agent**: it automates the work of a Machine Learning Engineer. It automates the process of testing algorithms or molecular features to see which is best for a dataset. It takes in a dataset of molecules and chemical structures, and spits out a trained PyTorch model that can predict future outcomes.

- Johnson & Johnson — biopharmaceutical company, AI agentic systems for autonomous drug discovery.
  - Replaces manual lab iterations, AI agents to identify potential drug candidates.
  - Determine optimal timing for certain chemical synthesis steps.
- Paper: https://pubs.acs.org/doi/pdf/10.1021/acs.jcim.5c01938
  - Developed by people at Johnson & Johnson.
  - **Mol Agent**: framework for AI systems to autonomously implement expert-level modeling for both classification & regression.
  - Features:
    - Converts raw molecular data into ML-understandable formats.
    - Generates 2D features, RDKit descriptors, molecular fingerprints.
      - Deep learning embeddings via bottleneck transformer.
    - 3D structure integration like affinity graphs and protein-ligand interaction fingerprints.
    - Model verification: partitions data so structurally related molecules aren't arbitrarily split between training and validation sets — prevents overfitting.
    - Model selection: "nested cross-validation" for unbiased optimal model & settings selection.
    - Ensemble methods: combine multiple simple algorithms into a bigger model for better performance.
    - Adjustable workload: "Cheap" vs "Medium" vs "Hard" for different tasks.
  - Performance was quite good on benchmarks — achieving equal if not better-performing models than those fine-tuned by humans.
  - 3-part hierarchy:
    - **Manager Agent** — takes user prompt, decides which specialized agent to call.
    - **Data Retrieval Agent** — handles dataset extraction, preprocessing, standardizing inputs.
    - **Model Training Agent** — executes ML tasks, evaluates performance.
  - Uses MCP server for standardized communication between LLM and API.

→ Distilled into [[Arch_JNJ_MolAgent]].

---

### Tippy — Artificial Inc.

**Summary**

This paper lays out a **multi-agent architecture** for drug discovery and lab automation. The agent hierarchy has a supervisor agent that shares context with the molecule agent, lab agent, analysis agent, and report agent. Above the supervisor agent is a guardrail agent that makes sure outputs aren't dangerous. It's a whole lab, automated.

This architecture makes heavy use of MCP servers, but also has other features. It's containerized with Docker and orchestrated by Kubernetes; each agent is in its own isolated environment. It uses Envoy Proxy for communication, and git-based tracking for version control.

*(Original figure not preserved on import — see paper Fig. 1.)*

*"Technical Implementation of Tippy: Multi-Agent Architecture and System Design for Drug Discovery Laboratory Automation"*
Paper: https://arxiv.org/pdf/2507.17852

- From Artificial Inc.
- More of a pure system-architecture blueprint for multi-agent frameworks.
- **Agent Hierarchy:**
  - **Supervisor Agent** — central brain, shares context across all agents.
  - **Molecule Agent** — computational chemist; converts molecules to SMILES, runs property predictions on GPUs, uses generative models.
  - **Lab Agent** — workflow engine; equipped with MCPs, interacts with laboratory hardware, starts experimental jobs, queries job statuses.
  - **Analysis Agent** — data science / statistical analysis.
  - **Report Agent** — documents processes; compiles experimental data and findings into Markdown and PDFs.
  - **Safety Guardrail Agent** — compliance monitor; no external tools, sits as a filtering layer to prevent harmful outputs.
- **Infrastructure:**
  - Entire system containerized in Docker, orchestrated by Kubernetes — each agent isolated in its own pod.
  - Envoy Proxy for secure external user communication.
  - MCP Servers — critical for agents to interact with the APIs.
  - Git-based tracking — every change made by agents is tracked in git, so everything is version-controlled and reproducible.

→ Distilled into [[Arch_ArtificialInc_Tippy]].

---

### Recursion Pharmaceuticals — LOWE

LLM-orchestrated workflow engine known as **LOWE**, acting as the brain, connecting to their own foundational predictive models, **Boltz-2** and **SynFlowNet**.

- https://www.recursion.com/lowe
- https://arxiv.org/pdf/2604.11661
- https://github.com/valence-labs/VCR-Agent

Focus is on LOWE, the agentic architecture.

- LOWE is a central agentic brain for the entire Recursion Operating System.
  - Using natural language, scientists can chain together dry-lab and wet-lab workflows.
  - They have a "phenomap" it navigates through, calling tools to identify drug-target interactions, deploy models, predict properties, and finally schedule the most promising candidates for physical synthesis.
  - **Strict Verifier approach:** sub-agents retrieve grounded knowledge, construct an explanation, then a verifier agent attempts to falsify the argument to make sure it's right.
    - Simulates scientists: propose hypotheses → try to falsify → learn.
  - https://arxiv.org/pdf/2604.11661
    - The idea of **mechanistic action graphs** is used for LLMs to represent biological knowledge.
- **Ideas to borrow:**
  - **Planner-executor loop** — central planner agent evaluates project state, invokes an execute skill based on that state to move forward.
  - **Verifier skill** — agent that verifies things, particularly parameters. Before anything runs, it must synthesize parameters, where a deterministic script can verify them.
  - **MCP.**
  - The "refining" cycle of **predict → test → falsify → improve** applies to error handling: if the code crashes, invoke analysis, figure out why, and try again.

→ Distilled into [[Arch_Recursion_LOWE]].

---

## Automating Computational Chemistry Workflows via OpenClaw and Domain-Specific Skills

**Primary substrate paper for this project:** https://arxiv.org/pdf/2603.25522

### Core Architecture (the canonical 3-layer view)

The system is organized around three distinct layers that work together dynamically at runtime:

- **OpenClaw (Central Control)** — general-purpose agent that manages the session context, tracks state across long tasks, and supervises execution. The language model reasons over the user's goal, the loaded skills, and execution feedback to dictate the next action.
- **Agent Taskboard Manifest (Planning Skill)** — rather than giving the agent open-ended tool access, this skill acts as a meta-prompting layer. It translates natural-language goals into explicit, structured workflow specifications defining stage dependencies, inputs, outputs, and validation conditions. → [[Arch_Taskboard_Manifest]]
- **DPDispatcher (HPC Grounding Skill)** — translates the agent's intent into scheduler-compatible job descriptors (e.g., Slurm, PBS, LSF). Treats queueing, monitoring, and result collection as normal workflow states, bridging orchestration and remote cluster execution. → [[Infra_DPDispatcher]]

### OpenClaw Trends

- **Lobster Workflow** — introduces a deterministic layer for mission-critical automation, providing a "do this exactly" layer before agentic reasoning. Avoids the need for replanning.
- **Directed Acyclic Graphs (DAGs)** of tasks, where each task can be a shell command, an LLM invocation, or an approval gate.
  - Particularly suited for computational chemistry — geometry optimization, input file generation, and job submission often follow rigid protocols.
- **Approval gates** allow humans to intervene before performing high-risk actions.
  - State is maintained, so it's very reversible to go back.
  - Git version control underpins reversibility.

→ Distilled into [[OpenClaw_Lobster_DAGs]].

**Self-Evolution and RL**

- "Self-evolving" agents that improve through usage.
  - **MetaClaw** project — uses a "skill creator" skill to create new skills, which become active instantly and can adapt to the project as it works.
  - **RL** can fine-tune agent behavior in complex environments — **OpenClaw-RL** provides a fully asynchronous RL environment. Reads the conversation and uses next-state signals (successful submission, user correction) as training data.

→ Distilled into [[OpenClaw_Self_Evolution]].

**Agentic Reasoning Applied Over Contextualized Examples**

- In the context of setting up DFT/MD code and avoiding parameter errors, specific examples of a trend can serve as precedent. We wrap examples with agentic reasoning for good results.
  - **Taskflow & state** — save accumulated context even if a model call fails.
  - **Memory providence labels** — Observed, Confirmed, Inferred — to categorize examples.
  - **Lobster** for deterministic parts.
- Intuition: ground the agent's pattern matching in actual examples, but wrap it in agentic reasoning to critique, refine, and validate future work.

→ Distilled into [[Design_Memory_Provenance]] *(renamed 2026-05-19 — was "Providence", a propagated typo; verified via NotebookLM to be 4 labels, not 3, with `imported from transcript` as the missing fourth; real source is OpenBrain, not the OpenClaw paper)*.

---

# User Pain Points

## Force Field Parameterization

- Everything is highly sensitive to naming conventions.
- When attempting to build systems with **non-standard** residues or anything not in standard libraries, there is no easy conversion to the AMBER library. When attempting to do so, the compiler often halts because force-field parameters are missing.
  - **tleap**, the compiler, fails to recognize custom ligands or non-standard residues, often requiring manual command-line tools like **antechamber** to generate missing parameters.
  - Often have to manually open `.pdb` coordinate files and rename atoms.
  - tleap is extremely unforgiving — any typos, missing spaces, or mismatches cause errors that can be hard to trace.
- **Ideas for OpenClaw:**
  - **Antechamber skill** — autonomously processes new ligands and generates everything necessary: AM1-BCC charges, GAFF atom types, and topology files. Much less risk of misplaced spaces.

→ Distilled into [[Skill_Antechamber_LigandPrep]].

## Runtime Instability

- If a simulation crashes due to a massive temperature spike or coordinate overflow, the researcher must manually find that in the `mdout` file, diagnose the failure, manually edit the `mdin` configuration, disable the **SHAKE** algorithm, and lower the integration step `dt`.
  - In essence, simulations require constant babysitting and can fail at any time, even while you're sleeping.
- **OpenClaw addressing:**
  - Use an agent to detect AMBER coordinate crash and use a **bounded recovery** to adjust failed parameters and everything else that comes with it. Can temporarily set `dt` to a conservative value before resuming normal parameters.
  - **"Bounded recovery"** means a mathematically defined correction, not an agentic-reasoned correction (which may be hallucinated). The agent is bounded in how it's allowed to react.
  - Detection of runtime instability is **deterministic** — it does not rely on agentic reasoning.

→ Distilled into [[Skill_Bounded_Recovery_AMBER]] and [[Workflow_Error_Recovery_Loop]].

---

# Round 2 — Competitive Landscape Expansion (2026-05-18)

Deterministic-automation incumbents and adjacent ML approaches, surveyed to position Project Prime. Synthesis lives in [[Design_Determinism_Spectrum]].

## Schrödinger — FEP+ / Multisim

- Highly optimized **deterministic** workflow automation. FEP = Free Energy Perturbation (binding-affinity computation); FEP+ is the drug-discovery implementation.
- **FEP+ Pose Builder** — auto ligand prep, reference ID, setup. Mirrors the antechamber/structure skills but is a *hard-coded algorithmic pipeline* formatting for Schrödinger's own FEP engine — no agentic reasoning.
- **De Novo Design** — uses *Active Learning FEP+*: iteratively trains an ML model on physics-based FEP+ data to evaluate novel structures.
- **Multisim** — automates sequential MD; on crash from hardware failure/timeout, recovers from the last checkpoint (`.cpt`). Standard IT failsafe — **does not alter physical parameters** if the system becomes unstable.
  - *Precision (2026-05-18, user verification):* the *automatic* retry is a bitwise-accurate checkpoint-restore and never autonomously mutates physics. Multisim **can** apply parameter mutations, but only via a **manual** command-line restart with the `-set` flag (e.g. `-set "stage.[1]time=2.0"`). The contrast with our skill is **autonomy**, not capability.

→ Distilled into [[Arch_Schrodinger_FEP]].

## OpenEye — Orion

- Cloud-native **DAG** system: compute units chained into guided workflows. Pre-configured workflows provided, but the graph is modifiable for further optimization.
- Non-sequential nodes run in **parallel**. Strong **conditional logic** — DAG splits into success/failure pathways leading to next steps or error handling.
- "Hard-coded": handling a new error means scripting it into the DAG yourself.
  - *Precision (2026-05-18, user verification):* Floes stream data through Python Cubes that evaluate conditions **dynamically at runtime** (`if/else` → success / failure / custom ports). Not a rigid unbranching script. The true limit is **semantic reasoning**: a Cube only branches on what a developer foresaw and coded. Frame the gap as "can't autonomously reason about the unanticipated," not "static."

→ Distilled into [[Arch_OpenEye_Orion]].

## Iambic Therapeutics — NeuralPLexer2

- A diffusion model predicting 3D structures, meant to *replace* traditional MD. Similar to AlphaFold. Not an agentic workflow — deliberately scoped out.

→ Distilled into [[Arch_Iambic_NeuralPLexer]] (boundary marker only).
