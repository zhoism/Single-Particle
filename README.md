# Single Particle — Project Prime (design vault)

The **design and context side** of *Project Prime — Single Particle Agentic
Workflow*: an internship project that uses the **OpenClaw** agent framework to
automate explicit-solvent **molecular dynamics in AMBER**. An LLM decides *what*
to run; hardened deterministic Python wrappers do *how* the science executes.

This repo is an **[Obsidian](https://obsidian.md) vault** — a graph of Markdown
notes, not runnable code. It holds the architecture decisions, prior-art
assessments, failure-mode research, and the development log behind the pipeline.
The *runnable* pipeline (the nine OpenClaw skills, the verification spine, the
pinned toolchain) lives in the companion repo:

> **Code:** [`zhoism/Single-Particle-pipeline`](https://github.com/zhoism/Single-Particle-pipeline)

## The thesis (decoupled hybrid agent)

Reasoning is deliberately separated from execution so a flaky or unconstrained
LLM can never corrupt mission-critical chemistry. The model is the front door;
the science is reproducible and bounded regardless of which model is behind it.
Reliability comes from **cheap deterministic proxy invariants** (`dt ≤ 2 fs`, net
charge ≈ 0, no NaN in the final energy block) — gates that are true when a step
worked and false when it broke — not from trusting the model. The notes here are
where those gates, and the decisions around them, get argued out and recorded.

## What's in here

A prefix taxonomy keeps the graph navigable (see [`CLAUDE.md`](CLAUDE.md) and
[`MAP.md`](MAP.md) for the full picture):

- **`Arch_*`** — architectural references (Recursion LOWE, J&J Mol Agent, the pipeline system).
- **`OpenClaw_*` / `Infra_*`** — framework mechanics and the execution layer (DPDispatcher, schedulers).
- **`Skill_*` / `Workflow_*`** — the design intent behind concrete pipeline skills and procedural loops.
- **`Design_*`** — cross-cutting principles (memory provenance, determinism spectrum, skill decomposition).
- **`Research_*`** — primary-source notes and tool assessments the distilled notes cite back to.
- **`Gap_*`** — open problems the vault has identified but not resolved (e.g. remote-HPC backend, gate coverage).
- **`Dev_Log.md`** — the reverse-chronological development trail; **`MAP.md`** — the at-a-glance done / in-flight / blocked index.

## Where the project stands

The local AMBER MD pipeline is **complete** — nine OpenClaw skills (ligand prep →
topology build → `pmemd` MD → CPPTRAJ analysis → PLIP profiling, plus a planning
layer, bounded crash-recovery, and a natural-language parameter editor), driven
end-to-end by an agent over CLI and Discord, running CPU-only on a local Mac.
The main open question is whether a production **remote HPC backend** ever
becomes available (`Gap_Remote_HPC_Backend`); local execution is the confirmed
current path.

## Scope / caveats

Internship / demo project. The deliverable is "an agent planned, ran, validated,
and recovered an MD run" — not publishable chemistry. Short-run MM-GBSA ΔG
figures referenced in these notes are illustrative **sanity numbers**, not
converged binding affinities: the *method* is verified, the *number* is not.

---

*Best read in Obsidian — the `[[wikilinks]]` and frontmatter form the knowledge
graph that ties the notes together. On GitHub they render as plain text.*
