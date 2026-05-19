---
tags: [openclaw, skills, planning, decomposition, design]
---
# Design: Skill Decomposition

**Core Concept:** A monolithic "run MD simulation" skill is too broad to be debuggable, testable, or composable. Skills should decompose into the natural stages of the workflow, each independently testable and chainable through OpenClaw's planning layer.

**Mental Model (from the user's market survey):**
- The **LLM** is the brain (reasoning over goals, context, and execution feedback).
- **OpenClaw** is the way the brain executes — it loads skills, tracks state, and dispatches calls.
- A **skill** is a `skill.md` file that teaches the agent how to interact with a specific external tool, script, or API. For Project Prime, that means teaching it how to run, debug, and analyze MD code and results — translating the user's scientific goals into an executable plan.

**Canonical Subskill Set:**

1. **Setup skill** — system prep, force-field parameterization, topology generation. Handles the `tleap` / `antechamber` pain points and the non-standard-residue problem. See [[Skill_Antechamber_LigandPrep]].
2. **Parameter validation skill** — deterministically check `mdin` parameters against physical-realism bounds (`dt ≤ 2fs`, non-bonded `cut` in valid range, SHAKE constraints). LLM-Inferred parameters get validated *before* execution. See [[Design_Memory_Provenance]] for the four-label provenance discipline (`observed` / `confirmed` / `inferred` / `imported from transcript`).
3. **HPC dispatch skill** — translate validated inputs into job descriptors via [[Infra_DPDispatcher]]; manage queueing, monitoring, and result collection as first-class workflow states.
4. **Analysis skill** — invoke CPPTRAJ and PLIP post-trajectory; emit RMSD/RMSF plots, hydrogen-bond timelines, and interaction diagrams.

**How the layers stack:**

The [[Arch_Taskboard_Manifest]] planner glues subskills together. The user's natural-language goal becomes an explicit DAG of subskill invocations with validation conditions between each. [[OpenClaw_Lobster_DAGs]] runs the DAG deterministically; the LLM only re-enters when an *Inferred* decision is needed.

**Why this matters:**

- Each subskill has a clear input/output contract → it's unit-testable in isolation.
- Failures localize to a stage (setup vs. validation vs. dispatch vs. analysis) → recovery via [[Workflow_Error_Recovery_Loop]] can act with the right scope.
- New skills (e.g. a future "membrane builder") slot in without rewriting the orchestration layer — they just register against the manifest.

**Source:** Opening framing in [[Research_Phase1_Survey]].
