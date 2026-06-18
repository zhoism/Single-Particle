---
tags: [report, summary, openclaw, amber, md-pipeline, architecture]
type: report
status: draft
created: 2026-06-17
---



## Implementation Summary 

A summary of what I've done! I'm still learning the overall landscape of Molecular Dynamics and AMBER Tools through this project, so I'll try to explain what in my own words my understanding of this work. The summary is focused on problems that arise in MD automation, and how the features we've created solve those problems. 

---

## 1. Executive summary

- What this is, an agent-driven pipeline, that takes a protein, and a small-molecule ligand from the raw structure, all the way to a binding-energy estimate, and a map of how the molecule binds. It's meant to be drivable through plain English, and our way of messaging this agent is through Discord, although this should be easily configurable. 

It works through nine self-contained 'skills' which are deterministic wrappers around the standard chemistry toolchain, with an agent that reasons over these skills. This format is to make sure the LLM doesn't touch certain parts that need perfect consistency. 

The most important thing to emphasize is that the LLM decides what to do, but never touches how the science will execute, instead using the wrappers that validate inputs and outputs through checking invariants, that can be checked very cheaply. 

The full pipeline seems to be fully functioning end-to-end on a real system.It takes in raw structure → parameterized ligand → solvated box → equilibration → production → analysis → binding energy → interaction fingerprint, launchable by natural language.

One thing to note for later is that I believe most MD simulations are ran through remote HPC clusters, which is something that needs to be done.

---

From my understanding, it seems the AMBER suite of tools is a very low-level tool, kind of like Assembly, which means that it requires a lot of babysitting and extra care. The expertise barrier is quite high, and the most annoying thing of all, is that many errors are silent, where the run completes, and produces garbage numbers, all from one small typo or mistake. 


### Brief review of the research phase

There were four groups ish that I was able to extract from the research phase, they are the following

1. **Remove the simulation entirely.** Replace physics-based MD with a learned surrogate model (e.g. Iambic / NeuralPLexer-style approaches). Fast, but you've swapped a mechanistic model for a statistical one. Out of scope for this project, but cool to see this field advance. 

2. **Remove the model; hard-code the pipeline.** A fixed, expert-built workflow with no agent in it (e.g. Schrödinger FEP-style pipelines). Reliable, but rigid — it does exactly and only what it was built to do. I do not have access to such pipelines, and they are probably quite sophisticated

3. **Remove the model; dynamic graph, no reasoning.** A workflow engine that can assemble steps dynamically but has no language-level reasoning (e.g. OpenEye Orion-style orchestration). These are pre-built dynamic workflows, but I also do not have access to these

4. **Reasoning *over* a deterministic core.** Keep a frozen, trustworthy execution layer; add a reasoning layer *on top* that decides what to run, never how the science executes. This is what we are trying to do, and we tried to take ideas from current industry trends. Johnson & Johnson has a Mol Agent, Artificla Inc has Tippy, Recursion has LOWE.

I'll get into what specifically we borrowed from them later, but we did not do agent swarms. Overall, the freedom for reasoning is actuall quite small. 

The idea is to have a system that borrows the determinism of approaches 2 and 3, and tries to integrate a reasoning layer around it, without giving up any determinism. 


## 3. core idea

**Agent is Decoupled**

The model is touched into the loop at only the decision points — *parse the user's intent, pick the skill, fill in the structured arguments, decide to launch* — and is structurally barred from everything else. It emits small, constrained instructions (e.g. "edit the production stage's temperature to 310"); a deterministic wrapper performs the actual work.

**The coverage line (the most important honest framing in the whole project).** The deterministic layer covers two layers of correctness completely and permanently, and a third not at all:

- **Covered, fully:** *mechanical* correctness, parameter bounds, cross-step invariants, known failure modes, and exact reproducibility. If a step ran, the wrapper can cheaply prove it ran *faithfully*.

- **Not covered, by design:** *scientific judgment* — whether the chosen method is appropriate, whether the sampling is converged, whether the force field is valid for this system, whether the question is even well-posed. I'm not a scientist who really has expertise in these tools, so I can't make judgments on that. My understanding for this whole project was that it is meant to reduce friction for AMBERtool users, but assumes that the users do have domain knowledege, and can interpret results and perform their own judgment.


**Proxy-invariant gates (how the "covered" part is actually achieved).** 
You can't check if something is correct, but we can just write some cheap checks for things a known failure violates. Charges sum to an integer, atom counts add up, aromatic atoms receive aromatic atom-types, energies are finite, residue names map to known residues. These gates basically just yell and scream when we have failures like this, and essentially make "silent failures" that would have ruined the run, "loud"

---

## 4. The pipeline, feature by feature

This is my learned intuition of the AMBER pipeline, along with features we've created, so pardon maybe a lack of scientific correctness

### A. Ligand parameterization 

Simulations requires assigning a molecule a force field, which are values that describe atom's charges and overall just behavior for the simulation. The standard chemical building blocks, like the amino acids, nucleotides, water, and common ions, all have been painstakingly parameterized over decades into validated force field values, a trusted table of values.

However, drug-candidate ligands are arbitrary organic molecules that have not been pre-parameterized, and must be generated. That's why we have GAFF2, which is a general force field to handle this, and AM1-BCC, which does charges. **antechamber** assigns GAFF2 atom types, and computes charges for new molecule. 

- **Problem.** 
Traditionally, the scientist runs antechamber by hand at terminal, choosing all flags, looking at output, and debugging by themselves. A lot of things can go wrong, and it's not an error type of wrong, it's just garbage Force fields. 

 The classic case: an aromatic ring that the tooling fails to recognize as aromatic gets the wrong atom types and loses a ring hydrogen — yet every downstream step runs cleanly on the broken parameters.


- **How it's solved.** The wrapper enforces invariants the scientist would otherwise have to track: total charge must sum to a near-integer, aromatic ring atoms must receieve aromatic atom-types, hydrogens are never stripped from a ligand. I actually got screwed over by an aromatic failure in the early stages. But we remove the doubt out of antechamber, and make sure we parameterize the ligand properly. 


### B. System build and solvation

- **Problem.** The simulation needs the protein-ligand complex placed in a box of water with neutralizing ions — a realistic "wet" environment. But a later analysis step needs the *dry* structure (no water), and the order in which files are saved determines whether you still have a clean dry copy. Get the order wrong and you've silently lost it.

- **How it's solved.** The wrapper fixes the save order so the dry structure is always preserved, and checks that atom counts are internally consistent (the solvated system must equal the dry system plus the water and ions actually added). These checks are very simple and seem trivial, but goes a long way

For the demo system this is roughly **306 atoms dry → ~5,990 atoms solvated**; the wrapper verifies that arithmetic rather than trusting it.

### C. Equilibration ladder — *easing the system to life without it exploding*

- **Problem.** A freshly built system holds enormous artificial potential energy (atoms slightly overlapping, awkward geometries). Starting full dynamics immediately tears it apart. The fix is a careful ladder: energy-minimize, then warm up gradually, then bring pressure to a realistic value. 

The issue is that warming up uses **two different temperature settings** — the thermostat's target and a separate scheduling target — and if they disagree, the system is being pulled toward two temperatures at once. Nothing complains.

- **How it's solved.** The wrapper treats the two temperature settings as **coupled**: set one, and it fixes the other automatically, so the inconsistency cannot be introduced by hand.

More broadly, every parameter in the ladder is checked against hard physical bounds (integration timestep ≤ 2 fs, sane non-bonded cutoff, sane thermostat/barostat).

This check again is really trivial, it's just making sure two values are the same. It makes me wonder why AMBER doesn't do this natively, but I've learned that AMBER is very low-level and doesn't safe guard these types of things.


### D. Production MD — *the actual simulation*

- **Problem.** Production runs thousands of tiny time-steps, one after another. It can quietly diverge into nonsense — energies blowing up to infinity — and keep producing output the whole time, with no warning to the user.

- **How it's solved.** The wrapper checks the run's health rigorously rather than trusting it to completion, watching for the numerical signatures of divergence (non-finite energies, integrator failures) while *tolerating* the harmless transient warnings that occur in healthy runs — over-sensitivity would be its own failure. 

I haven't quite done this now, but right now the system checks the outputs only AFTER the simulation completes. I want it to periodically check the simulation while it still runs; the example ligand you gave me ran in a short amount of time so it didn't seem necessary. It's labelled as future work.

### E. Stability and ensemble analysis — *condensing thousands of frame*

- **Problem.** A production run is thousands of snapshots. Raw, they're unusable. You need summary statistics — how much the structure drifts, which parts are flexible, what conformations it visits. The analysis is only valid if it's run against the 
**correct topology** (the matching description of which atom is which). Use the wrong one and the analysis silently mis-reads the trajectory.

- **How it's solved.** The wrapper pins the analysis to the right topology and verifies the match before running, then produces the standard battery — structural drift, per-residue flexibility, clustering, and dimensional reduction. A run yields on the order of **12 analyses and 10+ figures**. 

Once more, this seems really trivial, but there are no guardrails.

### F. Binding free energy (MM-GBSA) 


- **Problem.**  (not really a problem that we can solve)

The quantity we want is the binding energy, which takes some math to solve for. Accuracy, for MD, cannot be guranteed, and this is a limit of science.

- **How it's solved — and what it deliberately does *not* claim.** 
All we can do is again, make sure our inputs are not corrupted, and that the arithmetic is done correctly. So this layer just performs sanity checks, it's assumed that user understand the limitations of MD. 

Across runs of the demo system the estimate lands around **−17 to −18 kcal/mol** (e.g. −17.18, −17.6, and −17.94 from a planner-driven run)


### G. Interaction fingerprint (PLIP) — *how it binds*

PLIP seems to be a tool outside of AMBER, meaning it's not natively compatible with the AMBERtools suite. PLIP is important as it tells you not just how strongly something binds, but how. I don't know too much about this, but my understanding is that it's an important analysis tool. 

- **Problem.** 
The issue is that the naming conventions differ from AMBER to PLIP, just a result of being from different software. It's a pretty simple issue, but results in phantom extra ligands, which causes issues

- **How it's solved.** 
We just create a thin translation layer that normalizes the residue names into standard PLIP format, before handing it off. We create a "loud" gate for this to catch it before we let anything through. 

### H. Natural-language parameter editing — *steering safely in plain English*

- **Problem.** Changing how a run behaves means editing those delicate, interdependent parameter files by hand — easy to break and mess up, easy to break a coupling, like the two temperature coupling

- **How it's solved.** 
The model translates an English request into commands, through the LLM. Our wrapper is called "mdin-edit" and the LLM has basically three slots to fill, where the wrapper does everything else.]

  mdin-edit --md-dir <dir> --stage <which> --param <what> --value <new>

There are 3 slots, 

first is -stage, which is the stage at which the simulation is at (energy minimization, heating, pressurization, and relaxing stages). 

second is -param, so the parameter inside the namelist that we are modifying. As of now, there are only five parameters within the namelist, dt (integration step), temp0 (target temperature), restraint_wt (restraint weight), nstlim (number of steps), and cut (non-bonded cutoff). This is of course an incomplete set of parameters, but are the ones we've "proven" in the sense that we can modify them **safely**, taking into account everything else that relates to it. This namelist is incomplete, and will need to be expanded

-value is simply the new value

There is a failure vocabulary, a set of known failures we catch, with hierarchcial layers. Layer 1 is malformed requests, layer 2 is whether something is applicable to a stage, and layer 3 is checking the output to make sure it's correct. There's a separate non-fatal track, with Warnings. 


### I. Bounded recovery — *handling crashes without inventing fixes*

- **Problem.** MD runs crash; that's normal. We don't just blindly letting the LLM read the error and propose a fix, that would reintroduce unverified, unrepeatable chemistyr decisions at bad timing

- **How it's solved.** 
A deterministic detector distinguishes a real crash from harmless noise. It climbs a **fixed, bounded ladder** of pre-defined, physically-legal responses.


First is to address external/transient errors, say a timeout, node failure, or wall-clock limit. The fix is simple, jump back to last checkpoint and resume

Second is numerical instability, with like NAN_Energy or SHAKE, which softens the dynamics (every change here must be verified by check_amber), so that the run doesn't propose anything outside of physical bounds.

The Third is a structural/setup issue. This is when it HALTS and calls for human help. Fixing this would require changing the science, which this step cannont do. It returns a diagnosis, which is basically a dictionary of the values, with no LLM involvement. I'm thinking of using an LLM to add a kind of "english language gloss" over these values to make it a bit more friendly.


### J. Planning layer — *turning a goal into a validated workflow*

- **Problem.** A scientist thinks in goals ("get me the binding energy and how it binds"), not in skills. Something must translate a goal into the right ordered sequence with its dependencies respected. If a model pushes a plan with a flawed step to execution, everything will turn to garbage

- **How it's solved.** 
We use a plan as an explicit, inspectable manifest over our known skill catalog, using a deterministic validator which by default, treats the plan as *untrusted*. Every skill must exist, the dependency graph must be valid (acyclic), and every step's inputs are actually produced by earlier steps, along with valid parameters. Only after passing this inspection does it get compiled into a byte-inspectable execution and run. It must pass through 7 gates before anything runs; the validator checks every gate and reports all failures at once, rather than stopping at the first.


### K. Async orchestration and Discord 
- **Problem.** Real runs take hours. A foreground job holds your terminal hostage and dies if your connection drops; a job that only reports at the very end leaves you blind for hours.

- **How it's solved.** The pipeline launches **detached** (it survives disconnection) and streams **live per-step notifications over Discord** — you can even start the whole run by @-mentioning the bot. You dispatch it and get a running play-by-play on your phone. 

---

## 5. The architecture in layers

The features above stack into four conceptual layers:

1. **Planning layer (J).** Translates scientific goals into validated, stage-by-stage workflow specifications *before* anything executes.

2. **Deterministic execution layer (A–H).** The frozen core: every scientific action runs through a wrapper that validates its own inputs and outputs. The model is barred from this layer.

3. **Resilience (I), cutting across all layers.** Bounded, mathematically-constrained recovery instead of model-invented fixes — and an honest halt when the bounds are reached.

4. **Operations / grounding layer (K).** Detached execution and live notification today; remote-HPC dispatch is the designed-for-but-unbuilt extension here.

---

## 6. What "verified" means — and what a "green" actually is

This is the single most important conceptual point for anyone reading the results, so it gets its own section.

### The layered defense

No single check is trusted to prove correctness. Verification is layered:

- **Gates** — the cheap proxy invariants in each wrapper. They catch the *known* failure modes.

- **Oracle tests** — independent re-implementations of several wrappers' logic (the parameter editor, planner, interaction profiler, and crash detector), run across multiple Python versions, that cross-check the wrapper's output. (For the parameter editor alone this reached on the order of hundreds of thousands of fuzz/matrix assertions and found five distinct engine bug classes *before* anything shipped.)

- **Adversarial second-AI review** — for each substantial deliverable, an independent agent is told to *find faults*, defaulting to skeptical, with the real artifacts in hand. Every time we make something new to this pipeline, we run an AI agent to find faults. This is more of just claude code spawning fresh subagents to make sure things are right. We could definitely invest some more time into doing more of these, but these AI reviews have caught stuff for me


### The four flavors of "green" — and what none of them claim

A **green is the passing of a deterministic gate. It is never a claim of physical or biological correctness.** Four distinct greens recur, and conflating them is the easiest way to over-read the results:

- **Run-green** — the simulation executed to completion without numerical failure. Says nothing about whether the run was good science.

- **Analysis-green** — the analysis produced its outputs over the correct topology. Does not mean the ensemble is converged or sufficiently sampled.

- **Detector-green** — the crash detector found no fatal signature; the run is mechanically stable. Does not mean it is physically meaningful.

- **Review-green** — the adversarial review found no faults against the criteria. Means "no fault found," not "correct."

In every case, the green certifies a *faithful mechanical computation of the system as specified.* Whether that system was the right thing to simulate, and whether the result has converged enough to trust, remains the scientist's call. The pipeline is scrupulously honest about this boundary, and the report should be too.

### What the pipeline does *not* claim
- It does not make MM-GBSA more accurate than the method permits; the ~−17 to −18 kcal/mol figure is a sanity fingerprint, not a measured affinity.
- It does not judge scientific appropriateness, convergence, or force-field validity.
- It does not run on a cluster yet (see future work).
- Live, agent-driven runs to date were all on the demo system (1L2Y); a second system (3HTB) was driven end-to-end at the *scripted* level, not via the live agent. These two facts are kept distinct deliberately.

---

## 7. Future work

- **Remote HPC backend (the big one).** Today, runs are detached but execute locally. Dispatching to a Slurm/PBS cluster queue — treating queueing and monitoring as first-class workflow states — is designed-for but unbuilt. The async/notification layer (K) is the on-ramp.

- **Mid-stage / mid-run recovery (the watchdog).** Current recovery is **post-hoc**: it acts on a stage's log *after* the run finishes or crashes. A mid-run watchdog would tail a long production run *while it executes*, applying the same crash-detection logic at intervals so a doomed run can be caught and recovered (or halted) before wasting hours of compute. It reuses the existing detector; the new part is the continuous-monitoring loop. Buys little at demo scale, but is genuinely valuable at the long-run / HPC scale — so it pairs naturally with the remote-backend item above. **Not built.**

- **Systematic failure-mode survey → gate backlog.** The current gate set is the union of textbook physical limits and the handful of silent failures we personally hit or surfaced adversarially — *reactive*, not systematic. A planned research pass would mine the field's documented footguns (manual known-limitations, mailing-list archives, documented mis-typing cases) into a prioritized, reviewed backlog of candidate gates — so the coverage claim can move from "we encode what we hit" toward "we cover surveyed known failure modes," while staying honestly incomplete.

- **A single supervisory proposer-agent.** 

Generalize the propose-then-verify pattern (already used by the planner and recovery) into one standing agent that proposes parameter sweeps, convergence-driven run extensions, and adaptive analysis choices — *never* inserting anything into execution directly; every proposal still barred by the wrappers.

The agent can iterate, propose something, run it through the frozen pipeline, and try again if it comes back bad. But not just failure, it can be proactive, running sweeps (cut at 8, 9, and 10) or extend runs, or pick analyses. It can "explore the space" essentially

The limit of this is that the agent **can only propose things that can be verified.** Capability is gated by verification, not by reasoning.

- **A curated planner-context file.** Worked goal→plan examples and domain hints to raise the *quality* of proposed plans — with the standing caveat that better context improves the proposal only, never the trust (the validator stays equally strict).


- **Evaluate a self-hosted local model for the launch turn.** Since the model only does cheap boundary work, even a small local model could drive the launch — which would remove the external-API rate-limit dependency that has periodically stalled runs. (Tied to an evaluation of Hermes Agent as an alternative substrate; research, not migration.)

- **Semantic memory layer.** Deferred until the core was stable; to be revisited now that it is.

---

## 8. Where the architecture's ideas came from

The contributions here are the *deterministic wrappers, the gate discipline, and the verified tests* — not the high-level patterns, which are adopted and adapted from prior work and attributed accordingly:

| Element | Inspiration |
|---|---|
| Strict-verifier loop (predict → test → falsify → improve); reasoning over a deterministic core | Recursion's **LOWE** philosophy |
| Same architectural pole — reasoning layered over a trustworthy execution core | **J&J molecular agent**, **Artificial Inc. Tippy** |
| Planning layer (model proposes a plan; a runtime validates and executes it) | **Plan-and-Solve** prompting (Wang et al.) and **LangGraph**-style graph execution — an established pattern, applied here; not a novel concept |
| Bounded, mathematically-constrained crash recovery | The **Multisim / LOWE** recovery discipline (realized here deterministically; the contribution is the wrapper + verified tests, not the idea) |
| Deliberate restraint to ≤ 3 named agents rather than a large specialist swarm | Lessons from evaluating **El Agente Q**'s multi-agent topology — skills absorb most of the decomposition value at a fraction of the latency and coordination cost |

A note on the language model itself: it is **model-agnostic and does boundary work only** — swapping the underlying model (across vendors) was verified to leave the science identical, which is exactly what the decoupled design predicts.

---

*Draft for internal use / internship writeup. Numbers and scope statements are deliberately conservative; nothing here should be cited as a converged scientific result.*
