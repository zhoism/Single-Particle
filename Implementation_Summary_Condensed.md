---
tags: [report, summary, openclaw, amber, md-pipeline, architecture]
type: report
status: draft
created: 2026-06-17
condensed-from: Implementation_Summary_Report.md
---

## Implementation Summary — Condensed

A short version of the full report. Same honest framing, less prose.

---

### 1. What this is

An agent-driven pipeline that takes a protein + a small-molecule ligand from raw structure all the way to a binding-energy estimate and a map of how the molecule binds — drivable in plain English (we use Discord, but it's configurable). It runs end-to-end on a real system today.

It's built from **nine self-contained "skills"**: deterministic wrappers around the standard chemistry toolchain (AMBER, antechamber, CPPTRAJ, PLIP), with an LLM that reasons *over* them. The one line to remember: **the LLM decides *what* to do; it never touches *how* the science executes.** AMBER is a low-level tool that needs constant babysitting, and its worst failures are *silent* — a run completes and returns garbage from one small mistake. The wrappers exist to make silent failures loud.

---

### 2. The core idea — reasoning over a frozen core

The research phase showed four families of approach: (1) replace MD with a learned surrogate, (2) hard-code an expert pipeline with no agent, (3) a dynamic workflow engine with no reasoning, (4) **reasoning layered over a deterministic core**. We do (4) — borrowing the determinism of (2)/(3) and adding a thin reasoning layer, taking cues from J&J's Mol Agent, Artificial Inc.'s Tippy, and Recursion's LOWE. No agent swarms; the freedom given to reasoning is deliberately small.

**The coverage line (the most important honest framing):**
- **Covered, fully and permanently:** mechanical correctness — parameter bounds, cross-step invariants, known failure modes, exact reproducibility. If a step ran, the wrapper can cheaply prove it ran *faithfully*.
- **Not covered, by design:** scientific judgment — method appropriateness, convergence, force-field validity, whether the question is well-posed. The tool reduces friction for users who already have domain expertise; it does not replace it.

**How "covered" is achieved — proxy-invariant gates.** You can't cheaply check correctness, but you *can* cheaply check things a known failure violates: charges sum to an integer, atom counts add up, aromatic atoms get aromatic types, energies stay finite, residue names map to known residues. The gates yell when these break.

---

### 3. The nine skills (one line each)

| | Skill | Problem it guards against |
|---|---|---|
| A | **Ligand parameterization** (antechamber/GAFF2/AM1-BCC) | Mis-typed aromatic ring / stripped H → garbage force field that runs cleanly. Enforces integer charge, aromatic types, never strips ligand H. |
| B | **System build + solvation** | Wrong file-save order silently loses the dry structure; atom-count drift. Pins save order; verifies dry + water + ions = solvated (~306 → ~5,990 atoms on the demo). |
| C | **Equilibration ladder** | Two temperature settings (thermostat vs. schedule) can silently disagree. Treats them as *coupled*; enforces dt ≤ 2 fs, sane cutoff/thermostat/barostat. |
| D | **Production MD** | Run can diverge to infinite energy and keep emitting output. Checks for non-finite energies / integrator failure while tolerating harmless transient warnings. |
| E | **Stability + ensemble analysis** (CPPTRAJ) | Analysis run against the wrong topology silently mis-reads the trajectory. Pins + verifies topology, then produces ~12 analyses / 10+ figures. |
| F | **Binding free energy (MM-GBSA)** | Accuracy is a limit of the science, not solvable. Only sanity-checks inputs + arithmetic. Demo lands ~−17 to −18 kcal/mol — a fingerprint, not a measured affinity. |
| G | **Interaction fingerprint (PLIP)** | AMBER↔PLIP naming mismatch creates phantom ligands. Thin residue-name normalization layer with a loud gate. |
| H | **NL parameter editing (`mdin-edit`)** | Hand-editing interdependent param files breaks couplings. LLM fills 3 slots (`--stage --param --value`); wrapper does the rest. 5 params proven safe; 3-layer failure vocabulary + non-fatal warnings. |
| I | **Bounded recovery (`amber-recover`)** | Letting the LLM invent crash fixes reintroduces unverified chemistry. Deterministic detector → fixed ladder: (1) transient → resume from checkpoint; (2) numerical instability → soften dynamics, every change verified by check_amber; (3) structural issue → HALT + diagnosis for a human. |
| J | **Planning layer (`md-planner`)** | A flawed plan pushed to execution ruins everything. Plan = inspectable manifest over the known catalog; treated as *untrusted*; must pass 7 gates (skills exist, DAG acyclic, inputs satisfied, typed params…) before compile + run. Reports all failures at once. |

Plus **K — async orchestration + Discord:** runs launch *detached* (survive disconnection) and stream *live per-step* notifications; you can start a run by @-mentioning the bot.

---

### 4. Architecture in four layers

1. **Planning (J)** — goal → validated stage-by-stage spec *before* anything runs.
2. **Deterministic execution (A–H)** — the frozen core; every action self-validates inputs/outputs; the model is barred here.
3. **Resilience (I)** — bounded, math-constrained recovery cutting across all layers, with an honest halt at the bounds.
4. **Operations / grounding (K)** — detached execution + live notification today; remote-HPC dispatch is the designed-for-but-unbuilt extension.

---

### 5. What "verified" / "green" actually means

Verification is **layered**, no single check trusted: **gates** (cheap proxy invariants) → **oracle tests** (independent re-implementations cross-checking wrappers across Python versions; the param editor alone hit ~hundreds of thousands of fuzz assertions and caught 5 engine bug classes pre-ship) → **adversarial second-AI review** (a fresh agent told to *find faults* on each deliverable).

**A green is the passing of a deterministic gate — never a claim of physical/biological correctness.** Four flavors recur, and conflating them over-reads the results:
- **Run-green** — executed to completion without numerical failure (≠ good science).
- **Analysis-green** — outputs produced over the correct topology (≠ converged/sampled).
- **Detector-green** — no fatal crash signature (≠ physically meaningful).
- **Review-green** — adversarial review found no fault (= "no fault found," not "correct").

Each green certifies a *faithful mechanical computation of the system as specified.* Whether that was the right system, and whether it converged, stays the scientist's call.

**Explicitly NOT claimed:** more-accurate MM-GBSA than the method allows; any judgment of appropriateness/convergence/force-field validity; cluster execution (not built); live agent-driven runs beyond the demo system (1L2Y) — the second system (3HTB) was driven end-to-end at the *scripted* level only.

---

### 6. Future work

- **Remote HPC backend (the big one)** — runs are detached but local; Slurm/PBS dispatch with queueing/monitoring as first-class states is designed-for but unbuilt. Layer K is the on-ramp.
- **Mid-run watchdog** — recovery is currently post-hoc; tail a live production run and apply crash-detection at intervals. Reuses the detector; valuable at HPC scale.
- **Systematic failure-mode survey** — move the gate set from "what we hit" toward "surveyed known failures," mining manuals/mailing lists into a reviewed gate backlog.
- **A single supervisory proposer-agent** — generalize propose-then-verify: propose sweeps / run-extensions / analysis choices, always gated by the wrappers. Capability gated by verification, not reasoning.
- **Curated planner-context file** — better goal→plan examples raise proposal quality only; validator stays strict.
- **Self-hosted local model for the launch turn** — the model only does cheap boundary work, so a small local model could remove the API rate-limit dependency.
- **Semantic memory layer** — deferred until the core was stable; revisit now.

---

### 7. Where the ideas came from

The contributions are the **deterministic wrappers, the gate discipline, and the verified tests** — not the high-level patterns, which are adopted/attributed:

| Element | Inspiration |
|---|---|
| Strict-verifier loop; reasoning over a deterministic core | Recursion **LOWE** |
| Reasoning layered over a trustworthy execution core | **J&J Mol Agent**, **Artificial Inc. Tippy** |
| Planning layer (propose → validate → execute) | **Plan-and-Solve**, **LangGraph** (established pattern, applied — not novel) |
| Bounded, math-constrained crash recovery | **Multisim / LOWE** recovery discipline (realized deterministically) |
| ≤ 3 named agents, no swarm | Lessons from evaluating **El Agente Q** — skills absorb most decomposition value at a fraction of the cost |

The model is **model-agnostic and does boundary work only** — swapping vendors left the science identical, exactly as the decoupled design predicts.

---

*Condensed draft for internal use. Numbers and scope are conservative; nothing here is a converged scientific result. Full detail in `Implementation_Summary_Report.md`.*
