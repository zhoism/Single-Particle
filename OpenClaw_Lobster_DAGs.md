---
tags: [openclaw, dag, deterministic-workflow, safety]
---
# OpenClaw Mechanics: Deterministic Workflows & DAGs

> **Vault tier: 🟡 Mixed** — arXiv:2603.25522 confirms **Lobster as a workflow engine** with the `llm-task` plugin (JSON-Schema-validated output) and approval gates. The vault's claims that Lobster is specifically a **DAG**, sits **strictly before agentic reasoning** as a layered architecture, and is **git-backed for reversibility** are NOT in the paper. Treat the "DAG" framing as ours, not the paper's. NotebookLM-verified 2026-05-19.

**Core Concept:** Moving beyond pure LLM reasoning by introducing strict, rigid layers for mission-critical automation.

**Key Implementations:**
* **The Lobster Workflow:** Introduces a deterministic layer before agentic reasoning. This tells the system "do this exactly," preventing the AI from hallucinating during rigid protocols and avoiding the need for replanning.
* **Directed Acyclic Graphs (DAGs):** Tasks are structured as DAGs. A task can be a shell command, an LLM invocation, or an approval gate. This is perfect for computational chemistry, where input file generation and job submission follow strict rules.
* **Approval Gates:** Mandatory pauses in the workflow allowing human intervention before high-risk actions (like cluster submission). Maintains state via Git version control, making it easily reversible.

**External analog & contrast:** OpenEye's Orion ([[Arch_OpenEye_Orion]]) is the same DAG primitive built *without* an LLM. Its branches are *not* static — Cubes evaluate conditions dynamically at runtime — but they can only branch on what a developer foresaw and coded an `if` for. It validates the substrate and exposes its ceiling: the gap is **semantic reasoning**, not static wiring. OpenClaw's differentiator is reasoning *over* this deterministic layer to handle the failure nobody coded for. See [[Design_Determinism_Spectrum]].

## Source — verified breakdown (2026-05-19 via NotebookLM, arXiv:2603.25522)

- **Paper-confirmed:** Lobster is a workflow engine; the `llm-task` plugin integrates LLM invocations into it; approval steps before side-effecting actions are an explicit recommended pattern. Quote: *"llm-task is an optional plugin tool that runs a JSON-only LLM task... This is ideal for workflow engines like Lobster..."* and *"Put approvals before any side-effecting step..."*
- **Paper-confirmed positive find (add to report):** the `llm-task` plugin returns **JSON-only** output that can be optionally validated against a **JSON Schema** — a concrete deterministic-output mechanism strengthening the stage-validation claim in [[Arch_Taskboard_Manifest]].
- **Unverified vs the substrate paper — re-source required:** That Lobster is structured explicitly as a **DAG**, that it sits **strictly before agentic reasoning** as a layered architecture, and that **reversibility is git-backed** — none of these specific claims appear in the paper. Likely in OpenClaw documentation. Until re-verified, the report should describe Lobster more conservatively as "a deterministic workflow engine with approval gates and JSON-validated LLM tasks." See [[Research_Source_Manifest]] row #1.