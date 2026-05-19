---
tags: [architecture, competitor, dag, deterministic, conditional-logic, cloud]
---
# Architecture: OpenEye Orion

**Core Concept:** A cloud-native, **hard-coded DAG** platform. Compute units (cubes) are chained into directed acyclic workflows. This is the closest external analog to [[OpenClaw_Lobster_DAGs]] — but it is the *deterministic* version of that idea: the DAG is authored by a human, not reasoned about by an agent.

**Key Features:**
* **DAG of chained compute units** — same structural primitive as OpenClaw's Lobster DAGs (a node = a unit of work, edges = dependencies).
* **Pre-configured + modifiable** — ships validated default workflows, but power users can edit the graph to optimize. *This is a UX pattern worth stealing for [[Arch_Taskboard_Manifest]]: ship stage-validated default specs, allow override — defaults are the guardrail, not a cage.*
* **Automatic parallelism** — non-sequential nodes run in parallel to save wall-clock time. A scheduling optimization Lobster DAGs should adopt where the dependency graph allows.
* **Conditional logic / branching** — workflows (Floes) stream data through Python compute units (Cubes) that evaluate data attributes **at runtime**. Standard `if/else` inside a Cube dynamically routes each item to a success, failure, or custom port (e.g. a `missing` port for molecules lacking a required property) based on the data *at that moment*. This is **not** a rigid, unbranching sequence — it is a live, dynamically-evaluated data stream. The real ceiling is narrower and more interesting: **semantic reasoning**. A Cube can only branch on conditions a developer explicitly foresaw, coded an `if` for, and wired to a recovery task.

**The decisive contrast (precise version):** Orion's branching is dynamic, but it cannot *reason*. It evaluates conditions via explicit Python a human wrote, so it handles exactly the failures that human anticipated — no more. Hand it a novel crash signature with no matching `if`, and there is no code path to reason its way out. OpenClaw's bet is that an LLM reasoning layer *over* a deterministic DAG can read the unfamiliar error logs, diagnose the unanticipated failure (the [[Workflow_Error_Recovery_Loop]] / predict→test→falsify→improve cycle from [[Arch_Recursion_LOWE]]), and then act within bounded, deterministic limits. Orion proves the dynamic-DAG substrate works; it also proves why even a dynamic DAG is insufficient for "fails at 3am in a way nobody coded an `if` for." The gap is *semantic*, not *static*.

**Why it matters for the report:** Orion is the strongest argument that DAGs are the right execution substrate *and* the clearest illustration of the static-DAG ceiling OpenClaw is built to break. See [[Design_Determinism_Spectrum]].

**Source:** User Phase 1 competitive-landscape research, 2026-05-18 (Round 2). Raw notes in [[Research_Phase1_Survey]].
