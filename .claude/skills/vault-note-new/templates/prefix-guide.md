# Prefix taxonomy guide

The vault uses filename prefixes to indicate role. Match this exactly — the taxonomy is closed.

| Prefix | Role | Location | Example |
|--------|------|----------|---------|
| `Arch_*` | Architectural reference — borrowed from external systems (LOWE, J&J Mol Agent, Tippy, Orion, Schrödinger FEP+) or internal planning concepts (Taskboard Manifest). | vault root | `Arch_Recursion_LOWE.md`, `Arch_Taskboard_Manifest.md` |
| `OpenClaw_*` | Mechanics of the OpenClaw framework itself — its primitives, plugins, paradigms. | vault root | `OpenClaw_Lobster_DAGs.md`, `OpenClaw_Self_Evolution.md`, `OpenClaw_CLI_Map.md` |
| `Infra_*` | Execution-layer infrastructure — DPDispatcher, HPC schedulers, AMBER install. | vault root | `Infra_DPDispatcher.md`, `Infra_AMBER_Install.md` |
| `Skill_*` | Concrete OpenClaw skill to be built. Each is a distinct chemistry / MD operation. | vault root | `Skill_Antechamber_LigandPrep.md`, `Skill_Bounded_Recovery_AMBER.md` |
| `Workflow_*` | Cross-cutting procedural loop. Spans multiple skills. | vault root | `Workflow_Error_Recovery_Loop.md` |
| `Design_*` | Cross-cutting design principle. Spans the whole agent's behavior. | vault root | `Design_Memory_Provenance.md`, `Design_Skill_Decomposition.md`, `Design_Determinism_Spectrum.md` |
| `Research_*` | Raw research materials and primary-source notes (Phase 1 market survey, paper assessments). `Arch_*`/`Skill_*`/`Design_*` notes are distilled from these; cross-link back. | vault root | `Research_Phase1_Survey.md`, `Research_El_Agente_Q.md`, `Research_Source_Manifest.md` |
| `Gap_*` | Open problem the vault has identified but not resolved. Frontmatter `status: open|partially-filled|filled`. | vault root | `Gap_Remote_HPC_Backend.md` |
| (no prefix) | Top-level vault entry points (`Project Prime.md`, `CLAUDE.md`, `MAP.md`, `vocabulary.md`, `Dev_Log.md`) + canonical report deliverables (`Market_Landscape_Report.md`, `Market_Landscape_Summary.md`, `Actionable_Recommendations.md`). | vault root | — |
| connections/ | Edge notes — uncertain or non-obvious connections between two existing notes. | `connections/<name>.md` | (no existing examples yet) |

## How to pick

**Is it about OpenClaw the framework?** → `OpenClaw_*`

**Is it about a specific chemistry / MD operation that becomes a skill?** → `Skill_*`

**Is it about a cross-cutting procedural pattern?** → `Workflow_*`

**Is it about a cross-cutting principle for HOW the agent thinks/behaves?** → `Design_*`

**Is it a reference to an external system / borrowed architecture?** → `Arch_*`

**Is it about HPC / install / dispatch / OS-level infrastructure?** → `Infra_*`

**Is it raw primary-source material (paper, market scan, transcript)?** → `Research_*`

**Is it an open problem that's identified but unresolved?** → `Gap_*`

**Is it an uncertain / speculative connection between two existing notes?** → `connections/<name>.md`

## Edge cases

- **"It's borrowed AND it's about OpenClaw mechanics."** Pick by source: paper-cited → `Arch_*`; OpenClaw-doc-cited → `OpenClaw_*`. Example: Lobster DAGs is `OpenClaw_Lobster_DAGs` because Lobster is OpenClaw's plugin; the Predict-Test-Falsify-Improve strict-verifier pattern is `Arch_Recursion_LOWE` because it's borrowed from LOWE.
- **"It's both a Workflow and a Skill."** A Skill is atomic (one chemistry op); a Workflow chains multiple. Bounded recovery is a Skill (`Skill_Bounded_Recovery_AMBER`); error-recovery-loop-around-many-skills is a Workflow (`Workflow_Error_Recovery_Loop`).
- **"It's a Design but it's super specific."** Design principles span the whole agent. If it only applies to one skill or one workflow, it belongs in that skill/workflow note as a section.
- **"It's a Research note but it's distilled."** No. If it's distilled, write the distilled `Arch_*` / `Skill_*` / `Design_*` and put the raw source in a sibling `Research_*` note (or extend an existing one). Cross-link.

## Naming convention within prefix

- `Arch_<Org>_<Tool>.md` — e.g., `Arch_Recursion_LOWE.md`, `Arch_JNJ_MolAgent.md`.
- `OpenClaw_<MechanismName>.md` — e.g., `OpenClaw_Lobster_DAGs.md`.
- `Infra_<System>_<Aspect>.md` — e.g., `Infra_AMBER_Install.md`.
- `Skill_<Operation>_<Scope>.md` — e.g., `Skill_Antechamber_LigandPrep.md`.
- `Workflow_<Pattern>.md` — e.g., `Workflow_Error_Recovery_Loop.md`.
- `Design_<Concept>.md` — e.g., `Design_Memory_Provenance.md`.
- `Research_<Topic>.md` — e.g., `Research_Phase1_Survey.md`.
- `Gap_<ProblemName>.md` — e.g., `Gap_Remote_HPC_Backend.md`.

Use TitleCase or Underscore_Separated. NOT kebab-case (vault convention; matches the existing files).
