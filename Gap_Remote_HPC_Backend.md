---
tags:
  - project-prime
  - gap
type: gap
status: open
identified-from:
  - "[[Project Prime]]"
  - "[[Infra_DPDispatcher]]"
---

# 🟡 Gap: Is there a production remote HPC backend, or is everything local-shell?

> Gap note (adopted from the Knowledge Network pattern). `status: open` = identified but unresolved. Surface this when a question touches GPU execution, Slurm/PBS, or "where will this actually run at scale."

## What the gap is

`Project Prime.md` §3 flags an unconfirmed infrastructure question — the original Scenario A vs. Scenario B fork:

- **Scenario A (local/raw):** AMBER compiled/installed locally; agent dispatches to the local machine.
- **Scenario B (pre-configured):** a remote Single Particle staging server / HPC cluster exists; agent dispatches jobs via API.

**Current resolved-so-far state:** development proceeds **local** — `prime-amber` conda env on a CPU-only Mac, `sander` (no `pmemd.cuda`), DPDispatcher in `LocalContext` + `batch_type: "Shell"` (verified 2026-05-19). So the *demo path* is local.

**User decision (2026-05-21): Scenario A confirmed for now.** The user explicitly chose to **stay local and treat HPC as a future swap**, not build remote dispatch yet. Crucially, this is not a constraint we're working around — it's the *correct* division of labor: a cluster (if one ever appears) provides `pmemd`/`pmemd.cuda` as a `module load amber`, so we never compile AMBER on it. The deliverable that bakes this in is the [[Project Prime]] **golden path** (`project-prime/golden-path/`, validated 2026-05-21 on the T4 lysozyme L99A + benzene complex, PDB `181L`): all MD goes through one engine-agnostic `run_md()`/`ENGINE` seam, so the eventual Scenario-B switch is `ENGINE=pmemd.cuda` + a DPDispatcher `SSHContext`, with **zero changes to the recipe files**. The recipe is therefore swap-ready by construction.

**What is still open:** whether a production remote backend (the "Single Particle staging server") ever becomes available, and if so, when. That single fact determines whether the `pmemd.cuda` / Slurm-PBS / `SSHContext` code paths ever get built, or remain dead branches.

## Why it matters

- It decides whether [[Infra_DPDispatcher]]'s remote-context and the GPU engine (`pmemd.cuda`) are in scope or YAGNI.
- It changes the physics envelope: GPU MD enables far larger systems / longer trajectories than CPU `sander` on a laptop — which changes what the post-processing skills ([[Skill_Antechamber_LigandPrep]], CPPTRAJ/PLIP automation) must scale to.
- It affects skill design *now*: skills should be written so the execution context is swappable (local ↔ remote) rather than hardcoding `LocalContext`.

## Partial approaches already in the vault

- **Local path is proven:** [[Infra_AMBER_Install]] (env + smoke test) + DPDispatcher local-shell mode verified — Scenario A is unblocked end-to-end.
- DPDispatcher is *designed* to abstract local vs. remote (context objects), so the seam exists; it just hasn't been exercised against a real cluster.

## What would fill this gap

A confirmation from Single Particle on whether a remote cluster/staging server is provisioned for this internship, with access details (scheduler type, GPU availability, auth). Until then: build local, keep the dispatch context swappable, do not invest in Slurm-specific logic.
