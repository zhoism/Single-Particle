---
tags:
  - #active
  - #internship
  - #openclaw
  - #computational-chemistry
  - #amber
  - #project-prime
type: context-index
status: in-progress
---

# 🎯 Project Prime: Single Particle Agentic Workflow

## 1. Core Mission
Develop an "Agentic Workflow" using the OpenClaw AI framework to automate and reduce user friction in executing explicit-solvent Molecular Dynamics (MD) simulations. The project bridges computational chemistry with AI-driven orchestration, transforming natural language requests into executable HPC tasks, parameter validations, and data visualizations.

## 2. Agentic Architecture Scope (Knowledge Graph)
This project implements a decoupled, hybrid OpenClaw architecture. Instead of hardcoding procedures into the LLM, we separate general reasoning from domain execution.
**Architectural References:**
* **Workflow Planning:** [[Arch_Taskboard_Manifest]] (Enforces lazy-loading and explicit stage validation before execution).
* **Deterministic Execution:** [[OpenClaw_Lobster_DAGs]] (Rigid DAGs for strict protocols), [[OpenClaw_Self_Evolution]].
* **HPC Grounding:** [[Infra_DPDispatcher]] (Translates agent intent into Slurm/PBS job descriptors).
* **Resilience & Verification:** [[Workflow_Error_Recovery_Loop]], [[Arch_Recursion_LOWE]], [[Arch_ArtificialInc_Tippy]].
* **Data Translation:** [[Arch_JNJ_MolAgent]].

## 3. Developer Context (For Claude via MCP)
* **Background:** The developer is a Computer Science major with a minor in Physics. They have prior experience with data pipelines (e.g., recursive sparse regression via PySPIDER) and prefer tangible, design-oriented problem-solving over purely abstract theory. 
* **Role:** Integration & Automation Engineer. The focus is on building robust logic, guardrails, and UX for the simulation pipeline.
* **Infrastructure (RESOLVED 2026-05-21):** Scenario A (local) is the confirmed active path — AMBER is compiled/installed locally (Phase 2 ✅). The remaining open question is whether a production *remote* backend ever becomes available — tracked in [[Gap_Remote_HPC_Backend]]. Both scenarios are kept as future-swap context:
    1.  *Scenario A (Local/Raw):* Troubleshooting dependency hell (gcc, cmake, CUDA) and compiling AMBER from source.
    2.  *Scenario B (Pre-configured):* Writing API-driven OpenClaw skills that dispatch jobs to a remote Single Particle staging server.

## 4. The Tech Stack
* **Agent Framework:** OpenClaw (Local deployment, skills defined via Markdown/YAML and Python/Shell scripts).
* **Simulation Engine:** AMBER (specifically `sander` or `pmemd.cuda` for explicit solvent MD).
* **HPC Interface:** DPDispatcher (for remote cluster job submission and state tracking).
* **Data Analysis:** CPPTRAJ (native AMBER trajectory analysis) and PLIP (Protein-Ligand Interaction Profiler).
* **Environment:** Bash, Python, Slurm (potential cluster execution).

---

## 5. Phased Execution Roadmap

> **⚠️ This roadmap banner is a 2026-05-23 snapshot — for LIVE status see [[Phase3_Taskboard_Manifest]] + memory `project-prime-status`.** As of 2026-06-10 Phase 3 is essentially DONE: **9 OpenClaw skills built** (antechamber-ligandprep, tleap-build, amber-md-run, cpptraj-analysis, plip-profile, mdin-edit, pipeline-async, amber-recover, md-planner), the full local AMBER MD happy path is GREEN end-to-end, and both the bounded-recovery (Stage 8) and planner (Stage 7) layers are built. The Phase-4 PLIP deliverable is also done. Only [[Gap_Remote_HPC_Backend]] and the written report remain.
>
> **Status (2026-05-23, original):** Phase 1 ✅ done · Phase 2 ✅ done (AMBER fully wrapped — AmberTools 24.8 via conda + `pmemd`/`pmemd.MPI` built from source locally and test-suite-passing; see [[Dev_Log]] 2026-05-22) · **Phase 3 → NEXT: install OpenClaw + wire Gemini, then build skills.** · Phase 4 pending. Golden path (T4L L99A + benzene, `181L`) is the validated known-good recipe the skills will automate.

### Phase 1: Technical Market Research (Agentic AI)
* **Objective:** Survey the landscape of OpenClaw and multi-agent systems in U.S. pharma/biotech.
* **Focus:** Usage patterns, hybrid automation (LLMs + standardized calculators like ASE), and proving ROI by reducing "boilerplate friction" in biomolecular simulations.

### Phase 2: Environment Setup & Agent Configuration
* **Objective:** Establish the foundational pipeline between OpenClaw and AMBER.
* **Tasks:**
    * ✅ Resolve system dependencies (gcc@11, cmake, open-mpi) and configure environment variables (`amber.sh` in `~/.zshrc`).
    * ✅ Install and verify AMBER core modules — AmberTools 24.8 via conda + `pmemd`/`pmemd.MPI` from source; `make test.serial`/`test.parallel` pass.
    * ⏭️ **NEXT:** Initialize OpenClaw and verify it can execute basic local commands + a Gemini-backed `llm-task`.

### Phase 3: Skill-Based Explicit Solvent MD (The Logic)
* **Objective:** Build OpenClaw Skills to control simulation behavior dynamically.
* **Tasks:**
    * Teach the Agent to parse and modify the `mdin` input file structure.
    * **Physics Guardrails:** Implement logic checks for parameters like `cut` (non-bonded cutoff) and `dt` (time step, explicitly enforcing limits like 2fs).
    * Automate the job submission workflow.

### Phase 4: Automated Post-Processing & Visualization
* **Objective:** Translate massive trajectory files into digestible insights.
* **Tasks:**
    * **CPPTRAJ Integration:** Automate the calculation of RMSD (structural stability) and RMSF (residue flexibility).
    * **PLIP Integration:** Automate extraction of non-covalent interactions (hydrogen bonds, π-π stacking, salt bridges).
    * **Output:** Format the data into automated, visual reports (heatmaps, network graphs, bar charts) directly returned by the Agent.

---

## 6. Standard Operating Procedures for Claude
When assisting with this project, Claude should:
1. **Plan First:** Always refer to the [[Arch_Taskboard_Manifest]] concept to define stages, inputs, and validation conditions *before* writing execution logic.
2. **Format:** Default to writing modular, well-documented OpenClaw skills (`skill.md` format).
3. **Accuracy:** Maintain strict physical realism regarding computational chemistry parameters.
4. **Troubleshooting:** If encountering a system error, check the `Dev_Log.md` (if available) and apply the [[Workflow_Error_Recovery_Loop]] logic before suggesting a fix.
5. **Scalability:** Prioritize scalable logic (e.g., writing a skill that handles *any* ligand, not just a hardcoded test case).