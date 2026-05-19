---
tags: [design, synthesis, positioning, thesis, phase-1]
---
# Design: The Determinism ↔ Reasoning Spectrum (Project Prime's Positioning Thesis)

**Why this note exists:** Every system in the Phase 1 survey can be placed on one axis — *how much of the workflow do you trust an LLM to reason about vs. hard-code away?* This axis **is** Project Prime's thesis. Use this as the spine of the internship report's "competitive landscape" section.

## The spectrum

| Pole | Systems | How it gets reliability | What it can't do |
|---|---|---|---|
| **Remove the simulation** | Iambic [[Arch_Iambic_NeuralPLexer]] | ML predicts the answer; no MD run at all | Can't ground a result in actual physics; not a workflow at all |
| **Remove the LLM (hard-coded pipeline)** | Schrödinger [[Arch_Schrodinger_FEP]] | Algorithmic pipeline tuned for one engine; automatic recovery is checkpoint-restore only (mutation needs a human via `-set`) | Can't adapt to systems it wasn't pre-built for; can't autonomously fix an unstable run |
| **Remove the LLM (dynamic DAG, no reasoning)** | OpenEye [[Arch_OpenEye_Orion]] | Cubes branch dynamically at runtime — but only on conditions a developer coded an `if` for | Can't *reason* about a failure nobody anticipated |
| **Reasoning *over* a deterministic core** | OpenClaw / Project Prime; also J&J [[Arch_JNJ_MolAgent]], Tippy [[Arch_ArtificialInc_Tippy]], Recursion [[Arch_Recursion_LOWE]] | Deterministic execution for mission-critical steps ([[OpenClaw_Lobster_DAGs]], [[Skill_Bounded_Recovery_AMBER]]) + LLM reasoning for the novel/unstructured parts | Reasoning must be bounded & verified or it hallucinates chemistry |

## The argument the report should make

1. **The deterministic core is not optional and not novel — it's industry-validated.** Schrödinger and OpenEye prove nobody trustworthy hand-waves chemistry through an LLM. Project Prime adopting Lobster DAGs + bounded recovery is *aligning with the field*, not deviating from it.
2. **The gap every hard-coded competitor leaves is the same, and it is specifically about *autonomous semantic reasoning*, not branching or static-ness.** Schrödinger's Multisim *can* mutate parameters and Orion's Cubes *do* branch dynamically at runtime — neither is a rigid unbranching script. The real ceiling: Multisim only mutates physics when a human manually injects it (`-set`); Orion only branches on a condition a developer foresaw and coded. Hand either a novel failure with no human and no pre-written `if`, and there is no path to a fix. Phrase it in the report as "cannot *autonomously reason* about the unanticipated," never as "static" or "can't branch" — a reviewer who knows these tools will pounce on the imprecise version.
3. **OpenClaw's bet is to fill exactly that gap** — keep determinism for the rigid 95% (file gen, job submission, the happy ligand path), spend LLM reasoning *only* on the unstructured 5%: a non-standard ligand `tleap` rejects, a crash signature no one scripted. The [[Design_Memory_Provenance]] four-label discipline (`observed`/`confirmed`/`inferred`/`imported from transcript`) and the [[Workflow_Error_Recovery_Loop]] are the guardrails that keep that reasoning honest.
4. **Therefore Project Prime is not "yet another agent" — it is the answer to a specific, demonstrated gap** in the deterministic-automation incumbents.

## Design implications already actioned

- **Tiered recovery** (from the Schrödinger Multisim contrast): safe checkpoint-restore first, bounded parameter mutation only on re-crash. Folded into [[Skill_Bounded_Recovery_AMBER]].
- **Defaults-as-guardrail UX** (from OpenEye's pre-configured-but-modifiable model): [[Arch_Taskboard_Manifest]] should ship validated default specs that the user can override, not a black box.
- **Surrogate learning is a known pattern** (Schrödinger Active Learning FEP+): a deterministic analog of [[OpenClaw_Self_Evolution]] — note it exists, but it's out of Project Prime's day-1 scope.

**Source:** Synthesis of Phase 1 Round 2 competitive research, 2026-05-18. Raw notes in [[Research_Phase1_Survey]].
