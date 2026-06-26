# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Type

This is an **Obsidian vault**, not a code repository. There is no build system, test suite, or runtime. Files are Markdown notes with YAML frontmatter (tags, type, status) and Obsidian-style `[[wikilinks]]` between them. The `.obsidian/` directory holds Obsidian's local config (workspace, plugins, graph view).

When editing notes, preserve the frontmatter block and keep `[[wikilinks]]` intact — they form the knowledge graph that ties the vault together.

## Purpose: Project Prime

The vault is the design/context index for **Project Prime — Single Particle Agentic Workflow**: an internship project that uses the **OpenClaw** agent framework to automate explicit-solvent **Molecular Dynamics (MD)** simulations in **AMBER**, dispatched to HPC via **DPDispatcher**, with post-processing through **CPPTRAJ** and **PLIP**. `Project Prime.md` is the canonical entry point and lists the phased roadmap and SOPs.

The active deployment is **local (Scenario A)**: AMBER is compiled and installed locally (`pmemd` built from source) and the full MD pipeline runs CPU-only on the dev machine. The one open infrastructure question is whether a **remote production HPC backend** (Scenario B — API-driven dispatch to a Single Particle staging server) ever becomes available — tracked in `Gap_Remote_HPC_Backend`. Keep both scenarios as future-swap context, but treat local as the confirmed current path.

**Companion code repo:** the *runnable* pipeline lives in the sibling repo `../project-prime/` (GitHub `zhoism/Single-Particle-pipeline`); read its `CLAUDE.md` for the 9 skills, the run spine, and the pinned toolchain. This vault is the design side (`zhoism/Single-Particle`).

## Note Taxonomy (filename prefixes)

The vault uses a prefix convention to indicate the role of each note. Match it when creating new notes:

- `Arch_*` — Architectural references, often borrowed from external systems (Recursion LOWE, J&J Mol Agent, Artificial Inc. Tippy) or internal planning concepts (Taskboard Manifest).
- `OpenClaw_*` — Mechanics of the OpenClaw framework itself (Lobster DAGs, Self-Evolution/RL).
- `Infra_*` — Execution-layer infrastructure (DPDispatcher, HPC schedulers).
- `Skill_*` — Concrete OpenClaw skills to be built (e.g., Antechamber ligand prep, AMBER bounded recovery).
- `Workflow_*` — Cross-cutting procedural loops (error recovery).
- `Design_*` — Cross-cutting design principles (memory provenance, contextual reasoning, skill decomposition).
- `Research_*` — Raw research materials and primary-source notes (e.g., the user's Phase 1 market survey). The `Arch_*`/`Skill_*`/`Design_*` notes are *distilled* from these; cross-link back to the source.
- `Gap_*` — Open problems the vault has identified but not resolved (e.g., `Gap_Remote_HPC_Backend`). Frontmatter `status: open | partially-filled | filled`. Surface these when a question touches the unresolved area; they are where the interesting decisions still live.

**Session handoffs & future-work** (`Next_Session_Prompt_*`, `Future_Work_*`) live in the **`handoffs/`** folder (not at vault root) — see `handoffs/README.md` for the forward queue and per-file `status:`. New handoffs go there. Obsidian `[[wikilinks]]` resolve by filename, so the folder doesn't affect link traversal.

## Controlled Vocabulary

`vocabulary.md` is the canonical term list. **Before introducing a new term for an existing concept, check it first** — vocabulary drift silently breaks cross-note reasoning and `[[wikilink]]` traversal. If a concept already has a name, reuse it; if it is genuinely new, add it to `vocabulary.md` before using it elsewhere. Note confidence is carried by the existing **tier badges** (`✅`/`🟡`/`⚪`) and rule trust by **Memory Provenance** (4 labels) — do not add parallel `confidence:` frontmatter.

## Definition of Done (anti-drift)

The vault + auto-memory **are** the deliverable, so the main failure mode is **drift** — work happens but the record doesn't catch up. **Full discipline + the status-document inventory live in `Definition_of_Done.md`** (read it; this is the always-loaded summary).

A **substantive result** (a build, decision, assessment, failure-mode finding, report, gate fix, scope change — *not* a Q&A, typo, or read-only exploration) is **not done until, in one pass:**

1. **memory file** updated (+ `project_prime_status.md` for live state) **and** its **`MEMORY.md`** index pointer;
2. the **canonical vault note** per taxonomy, with **frontmatter `status:`/dates** refreshed on every note touched;
3. a **`Dev_Log.md`** entry (reverse-chron marker + pointers);
4. any **status field the result moved** — `Gap_*`/`handoffs/` `status:`, `Phase3_Taskboard_Manifest` stage state, `Project Prime.md` roadmap, and **`MAP.md`** if the high-level picture shifted;
5. **commit → independent review → push** (§4 below).

Don't ask whether to record it — just do it (extends [[feedback-autonomous-vault]]; pairs with [[feedback-sync-memory-status-docs]], [[dev-log-convention]], [[feedback-verify-and-eval]]). *Memory lives outside git — kept current by this discipline, never committed.*

**Commit → review → push** (scope: **both** this vault and the sibling `../project-prime/`, both private + solo so push is low-stakes and reversible): commit a completed result, then **review each commit independently before pushing it** — `/code-review` for the code repo; a frontmatter/`[[wikilink]]`/date/contradiction consistency pass for the vault — then push (`git push` is wired to prompt; that prompt is the review-gate moment). A deterministic user-scope **`Stop`-hook backstop** (`~/.claude/helpers/hook-handler.cjs`) nudges once if a session ends with uncommitted/un-logged/unpushed work in either repo — it can't write the updates, only catch the omission.

## Architectural Big Picture

The system is a **decoupled hybrid agent**: LLM reasoning is deliberately separated from domain execution to avoid hallucination in mission-critical chemistry steps. Three layers stack on top of each other:

1. **Planning layer** — `Arch_Taskboard_Manifest` enforces lazy-loaded, stage-validated workflow specs *before* any execution. The agent must translate scientific goals into explicit stage/input/output/validation specs.
2. **Deterministic execution layer** — `OpenClaw_Lobster_DAGs` runs the deterministic workflow engine with approval gates. The LLM is barred from this layer; it only executes `observed` and `confirmed` provenance-tagged rules (see `Design_Memory_Provenance` for the four-label discipline — `inferred` LLM output must be verified before execution, and `imported from transcript` is treated as inferred by default).
3. **HPC grounding layer** — `Infra_DPDispatcher` translates intent into Slurm/PBS job descriptors and treats queueing/monitoring as first-class workflow states.

Resilience cuts across all layers: `Workflow_Error_Recovery_Loop` + `Skill_Bounded_Recovery_AMBER` define bounded, mathematically-constrained recovery (e.g., crash → lower `dt`, disable SHAKE, resume) rather than letting the LLM invent fixes. The strict-verifier pattern from `Arch_Recursion_LOWE` (Predict → Test → Falsify → Improve) is the model.

## SOPs for Claude (from Project Prime.md §6)

1. **Plan first** using the `Arch_Taskboard_Manifest` concept — define stages, inputs, and validation conditions before writing execution logic.
2. **Default output format** for new skills is the OpenClaw `skill.md` format (Markdown/YAML + Python/Shell).
3. **Physical realism is non-negotiable** for MD parameters — enforce hard limits like `dt ≤ 2fs`, non-bonded `cut` ranges, SHAKE constraints.
4. **On errors**, check `Dev_Log.md` (if present) and apply the `Workflow_Error_Recovery_Loop` before proposing a fix.
5. **Write scalable skills** — handle any ligand/system, not a hardcoded test case.

## Developer Context

The developer is a CS major with a Physics minor, prior experience with data pipelines (PySPIDER / recursive sparse regression), and prefers tangible/design-oriented framing over abstract theory. Their role here is Integration & Automation Engineer — the work is about guardrails, logic, and UX over the simulation pipeline, not novel chemistry research.
