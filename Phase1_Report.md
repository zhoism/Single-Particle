---
tags: [report, phase-1, market-research, deliverable]
type: report
status: draft-for-review
date: 2026-05-19
---

# Phase 1 Report — US Market Research for OpenClaw Agent Skills (MD Simulation Context)

**Author:** Kevin Zhou
**Project:** Project Prime — Single Particle Agentic Workflow
**Date:** 2026-05-19

---

## Executive summary

I spent Phase 1 doing three things: clarifying what an "OpenClaw Agent Skill" actually is in the molecular-dynamics setting, mapping the US landscape of agent-based and adjacent automation in computational chemistry, and verifying my own work against primary sources. The headline takeaway is that the field is converging on a *decoupled hybrid* architecture — LLM reasoning sitting on top of a deterministic execution core — and that the niche Project Prime fills is autonomous, mathematically-bounded recovery from MD runtime failures, which is the one piece even the strongest commercial incumbents (Schrödinger, OpenEye) don't do. The substrate OpenClaw paper directly supports this with a methane-oxidation case study, which gives the project a real anchor instead of a hand-wave.

This report covers all five prompts from the brief in order. A short methodology note at the end documents the verification work that caught and corrected some early overclaims.

---

## 1. Clarifying the core concept — what "OpenClaw Agent Skills" means for MD

OpenClaw is an agent framework that deliberately separates **reasoning** from **execution**. The LLM is the brain; **skills** are the executable hands. A skill is a markdown-defined capability — a `skill.md` file with YAML frontmatter and Python or shell code underneath — that teaches the agent how to operate one specific tool, API, or protocol, and equally importantly, what its limits are.

For molecular dynamics, this separation matters a lot. MD pipelines are mission-critical and brittle: a single typo in `tleap` halts a topology build, a single bad parameter (`dt` set too high, non-bonded `cut` outside a valid range, SHAKE misconfigured) silently corrupts a multi-day run. You don't want an LLM hallucinating chemistry. You want it reasoning *over* a deterministic execution layer that refuses physically nonsensical inputs.

So an "OpenClaw Agent Skill for MD" is a *decomposed* capability — not one monolithic "do molecular dynamics" skill. The decomposition I'm working toward, building from the substrate paper's planning-skill / domain-skill split:

- **Setup / parameterization skill** — wraps `antechamber` and `tleap`. Given a ligand, it generates AM1-BCC charges, assigns GAFF atom types, and produces topology files. Handles the non-standard residues that crash `tleap` for human users.
- **Parameter-validation skill** — before any MD run, checks `mdin` parameters against physical-realism bounds (`dt ≤ 2fs`, valid non-bonded cutoffs, sane SHAKE constraints). Anything the LLM inferred is deterministically verified before execution.
- **HPC dispatch skill** — built on DPDispatcher in local-shell mode for day-1; the same interface scales later to Slurm/PBS/LSF if the project moves off-laptop.
- **Bounded recovery skill** — monitors `mdout` for crash signatures via regex (not LLM inference); on detection, applies a mathematically-bounded fix (lower `dt`, disable SHAKE temporarily, resume), then restores normal parameters once the system has stabilized.
- **Analysis skill** — wraps CPPTRAJ and PLIP for post-processing (trajectory analysis, protein–ligand interaction profiling).

The substrate paper (arXiv:2603.25522) supports this architecture explicitly. Its own words: *"Planning skills externalize task descriptions into executable task specifications; domain skills provide computational chemistry procedures."* It also directly supports **bounded recovery from runtime failures**, demonstrated in a methane-oxidation reactive-MD case study — which means the recovery skill above is paper-grounded, not just a project guess.

The LLM's job is not "run the simulation." It's: translate the scientist's natural-language goal into a structured workflow spec, route each stage to the appropriate deterministic skill, interpret error signals, and recover within hard mathematical limits.

---

## 2. Industry adoption — five US organizations in agent-based automation for computational chemistry

The first three are unambiguously agent-based. The last two are deterministic-workflow incumbents I included because mapping the contrast was essential to positioning the project — "what OpenClaw isn't" matters as much as what it is.

### 2.1 Johnson & Johnson — Mol Agent

J&J published Mol Agent in JCIM (2025) as a framework for autonomous ML over molecular datasets. It uses a three-part agent hierarchy: a **Manager Agent** that takes the user's prompt and routes it, a **Data Retrieval Agent** that handles preprocessing and standardization, and a **Model Training Agent** that executes the ML task and evaluates results. Communication between the LLM and tools goes through an MCP (Model Context Protocol) server. On their internal benchmarks Mol Agent matched or beat models hand-tuned by human ML engineers. This is the cleanest production example I found of an LLM agent automating a piece of the drug-discovery pipeline — and the multi-agent + MCP pattern transfers directly to MD automation.

### 2.2 Artificial Inc. — Tippy

Artificial Inc. (San Francisco) published a system-architecture paper (arXiv:2507.17852) describing **Tippy**, a multi-agent platform for automating an entire drug-discovery laboratory. Its hierarchy is wider than J&J's: a **Supervisor Agent** shares context across **Molecule, Lab, Analysis, and Report** sub-agents, with a **Safety Guardrail Agent** sitting above them all as a compliance filter (the Guardrail notably has *no external tools* — its only job is to refuse unsafe outputs). The whole system is containerized: Docker + Kubernetes, one pod per agent, Envoy proxy for external communication, git-based tracking of every action. Tippy is less about chemistry mechanics and more about the *infrastructure pattern* for multi-agent lab automation. For Project Prime, the transferable ideas are MCP-as-bus and per-agent isolation.

### 2.3 Recursion Pharmaceuticals — LOWE

Recursion (Salt Lake City) built **LOWE** — LLM-Orchestrated Workflow Engine — as the central agentic brain sitting above the rest of their Recursion Operating System. Scientists chain dry-lab and wet-lab workflows in natural language. The piece I borrowed most heavily is LOWE's **strict-verifier loop**: sub-agents propose a hypothesis, then a separate *verifier* agent attempts to falsify it before any action is taken. This mirrors how scientists actually work — propose, try to disprove, refine — and it's the direct model behind the error-recovery loop I'm designing for AMBER crashes (predict the failure cause, test the conservative fix, falsify if the system re-crashes, improve). Recursion also uses "mechanistic action graphs" to represent biological knowledge for LLM consumption, which is interesting but less directly applicable to MD than the verifier pattern.

### 2.4 Schrödinger — FEP+ / Multisim *(deterministic incumbent)*

Schrödinger (NYC) is the established player in computational drug discovery and represents the *fully-deterministic-pipeline* end of the spectrum. **FEP+** (Free Energy Perturbation, drug-discovery flavor) automates ligand binding-affinity calculations end-to-end. Its **Pose Builder** handles ligand prep, reference identification, and system setup — the same job my antechamber skill targets — but as a rigid, hard-coded pipeline formatted for Schrödinger's own engine, not as an LLM reasoning autonomously. Their **Multisim** tool automates sequential MD runs and includes a built-in recovery mechanism that rolls back to the last `.cpt` checkpoint after a hardware failure or timeout.

A precision point worth getting right (a reviewer would pounce on the imprecise version): Multisim's *automatic* recovery is a bitwise-accurate checkpoint-restore — it never autonomously mutates physics. Parameter mutation *is* possible, but only **human-in-the-loop**, via a manual command-line `-set` flag (e.g. `-set "stage.[1]time=2.0"`). So the precise contrast between Multisim and what OpenClaw aims for is **autonomy**, not capability — Schrödinger requires a human to inject any parameter change after a crash; OpenClaw aims to do bounded autonomous mutation within mathematical limits.

### 2.5 OpenEye Scientific (now Cadence) — Orion

OpenEye's **Orion** (under Cadence since the 2022 acquisition) is a cloud-native workflow platform where compute units called **Cubes** are chained into Python workflows called **Floes**. Cubes evaluate data attributes *dynamically at runtime* — standard `if/else` Python routes each data item to a success port, failure port, or custom port (e.g. a `missing` port for molecules lacking a required property), based on the conditions of that data at that moment.

The precision point here matches the Schrödinger one (and again, the imprecise framing would get caught): Orion's branching is **not** rigid or pre-scripted in the sense of a fixed unbranching sequence — it's a live data stream with real conditional logic. The actual ceiling is **semantic reasoning**. A Cube can only branch on conditions a developer explicitly foresaw and coded an `if` for. Hand Orion a novel error log with no matching `if`, and it cannot reason its way to a fix. This is the precise gap OpenClaw aims to fill: keep Orion's deterministic-DAG substrate, but add an LLM reasoning layer *over* it for the unanticipated failure.

### Honorable mention — Iambic Therapeutics (scoped out)

Iambic Therapeutics (San Diego) developed **NeuralPLexer2**, a diffusion model that predicts 3D protein-ligand structures directly — essentially the "skip the simulation, predict the answer" camp, adjacent to AlphaFold. I surveyed it for completeness but consciously scoped it out: it isn't an agentic workflow system, there's no orchestration or recovery layer to learn from. It marks the boundary of the competitive landscape (replace the simulation entirely) but doesn't transfer techniques into Project Prime.

---

## 3. Technology trends — what's emerging around OpenClaw Agent Skills

Across the systems I surveyed, the same handful of patterns kept showing up.

**Decoupled hybrid agents.** The strongest trend by far is the *deliberate separation* of LLM reasoning from domain execution. Schrödinger and OpenEye remove the LLM from execution entirely; J&J, Tippy, LOWE, and OpenClaw keep the LLM in the loop but contain it. The OpenClaw paper enforces this via **Lobster** (its deterministic workflow engine) and an `llm-task` plugin that requires LLM outputs to be JSON validated against an explicit JSON Schema. "Structured outputs over free text" is becoming the default for any mission-critical agent step.

**Approval gates and human-in-the-loop checkpoints.** OpenClaw bakes approval gates into Lobster ("put approvals before any side-effecting step" is paper-cited verbatim). Tippy's Safety Guardrail is the same idea at higher altitude. The trend is that "high-risk action" is treated as a workflow state with its own gate, not as a vibe.

**Workflow lifecycle ownership.** DPDispatcher doesn't just submit jobs — it actively **pokes (monitors) until completion and downloads result files**. Treating queueing / monitoring / result-collection as first-class workflow states, rather than ad-hoc shell scripts, is a pattern shared between DPDispatcher and Orion. This is how heterogeneous backends (Slurm, PBS, LSF, local shell) become interchangeable from the agent's perspective.

**Memory provenance / belief grounding.** OpenBrain — an open-source memory-recipes companion project to OpenClaw that I discovered mid-Phase 1 — introduces a four-label memory provenance system. Every piece of memory is tagged `observed from source`, `inferred by model`, `confirmed by user`, or `imported from transcript`. The deterministic execution layer is only allowed to act on `observed` + `confirmed`; `inferred` memory is quarantined until verified, and `imported from transcript` is treated as inferred by default until corroborated. This kind of provenance discipline is appearing across the agent space as the practical answer to "how do we stop hallucinations from being treated as facts."

**Cross-platform / cross-backend dispatch.** DPDispatcher supports `LocalContext`, `LazyLocalContext`, `SSHContext`, `OpenAPIContext`, and `HDFSContext`. The same skill logic targets a laptop shell or a remote supercomputer interchangeably. This is essential for my situation specifically — I must develop locally on a Mac (no NVIDIA GPU, no Amber `pmemd.cuda` license), but the work has to stay portable to GPU clusters later.

**Skill marketplaces and portable capabilities.** Across the broader agent ecosystem (Claude Code skills, OpenAI custom GPTs, LangChain Hub, OpenClaw's `~/.openclaw/skills/` convention), the trend is toward small, markdown-defined, version-controlled capabilities you install per-project. The *skill* is becoming the unit of reuse rather than the entire agent.

**Bounded recovery as a design pattern.** Worth separating this out because it's where Project Prime actually differentiates. The OpenClaw paper explicitly supports "bounded recovery from runtime failures" and demonstrates it in the methane-oxidation reactive-MD case study. "Bounded" means mathematically constrained — not "LLM picks a new parameter" but "agent applies a pre-defined mutation within hard limits." That is precisely the gap between Schrödinger's automatic checkpoint-restore (which doesn't actually fix unstable physics) and a free-form LLM agent (which would hallucinate a fix). It sits between the two, and the paper validates that this is a real and useful design point.

---

## 4. User pain points — and how OpenClaw addresses each

Pulled from the primary-source pain-point literature in the survey and from my own initial experiments with AMBER.

### 4.1 Force-field parameterization brittleness

`tleap`, the AMBER topology compiler, is **extremely** unforgiving. Any typo, missing whitespace, or atom-name mismatch in a `.pdb` file halts the build. Non-standard residues and custom ligands aren't in the standard AMBER libraries, so the compiler errors out asking for parameters that don't exist. Users have to drop to the command line, run `antechamber` to generate AM1-BCC charges and assign GAFF atom types, and then manually edit `.pdb` files to align with AMBER's expected naming conventions — often opening individual atom records and renaming them by hand. The error messages are notoriously cryptic.

**OpenClaw's approach:** an **Antechamber skill** that autonomously processes the incoming ligand — generates AM1-BCC charges, assigns GAFF atom types, formats the `.pdb` correctly, and produces clean topology files. The skill is a deterministic text-formatter and parameter generator. The LLM doesn't *invent* parameters (that would be the failure mode); it just routes the ligand into the skill's deterministic pipeline.

### 4.2 Runtime instability and crash babysitting

Explicit-solvent MD simulations crash, often unpredictably, from temperature spikes, coordinate overflows, and constraint violations. When this happens, the researcher has to manually parse the `mdout` log file, identify the crash signature, edit the `mdin` configuration (lower `dt`, disable SHAKE, sometimes adjust nonbonded cutoffs), and restart. As one of the source notes put it: *"simulations require constant babysitting and can fail at any time, even while you're sleeping."*

**OpenClaw's approach — the Bounded Recovery skill.** This is the strongest paper-cited element of the project. The agent monitors `mdout` deterministically (regex / log-parsing, not LLM reasoning) for crash signatures. On detection, it applies a *mathematically bounded* fix: temporarily lower `dt` to a conservative value, disable SHAKE, let the system stabilize for a set number of steps, then restore normal parameters. "Bounded" means hard limits — the agent cannot pick a `dt` outside a pre-defined safe range. The OpenClaw paper demonstrates this with the methane-oxidation reactive-MD case study; that's the precedent I'll cite when defending the design.

**Tiered design to address the safety critique.** Schrödinger's industry-default is checkpoint-restore only (never touch physics automatically), which is safer but doesn't fix root cause — a physically unstable system just re-crashes from the checkpoint. OpenClaw's mutation approach is more ambitious and therefore needs a guardrail. My answer is **tiered recovery**: Tier 1 is safe checkpoint-restore (handles transient hardware/timeout failures with zero physics risk); Tier 2 escalation is bounded parameter mutation, but only if Tier 1 re-crashes near the same step. So parameter mutation is always the *escalation*, never the first move — this makes the skill defensible against the "you're letting an AI change physics" critique.

### 4.3 Workflow brittleness in deterministic incumbents

Schrödinger's hard-coded FEP+ pipeline works perfectly *for the systems it was pre-built for*. Orion's Cubes branch beautifully *on conditions a developer foresaw*. Neither handles a novel failure or a non-standard input.

**OpenClaw's approach:** the LLM reasoning layer sits *over* a deterministic core. The deterministic part stays — file generation, job submission, the happy path — because the field has proven that's how you get reliability. The LLM is only spent on the unstructured 5%: a non-standard ligand `tleap` rejects, a crash signature no one anticipated.

### 4.4 The autonomy gap

Schrödinger Multisim *can* mutate parameters but only via a human running `-set` on a manual restart. OpenEye Orion *can* route around failures but only if a developer pre-wrote the `if`. Both leave the same gap: a failure that no human is around to intervene on, and no developer anticipated, sits stuck.

**OpenClaw's approach:** autonomous bounded reasoning. The LLM diagnoses unfamiliar error logs (within the verifier loop borrowed from Recursion LOWE), proposes a fix, the deterministic layer verifies the fix is within mathematical limits, and the action proceeds. No human required for the common cases; humans are reserved for genuinely novel decisions via approval gates.

---

## 5. Information source list

Organized by tier and annotated with what I used each for. Sources marked **(NotebookLM-verified)** were uploaded into NotebookLM and fact-checked against specific vault claims; everything else was cited from direct reading.

### 5.1 Primary literature — OpenClaw substrate

- **arXiv:2603.25522** — *"Automating Computational Chemistry Workflows via OpenClaw and Domain-Specific Skills."* **(NotebookLM-verified, 2026-05-19.)** Confirms: planning-skill / domain-skill split; Lobster as a workflow engine with the `llm-task` plugin and approval gates; DPDispatcher Slurm/PBS/LSF/Bohrium translation + poke-monitor-download lifecycle; **bounded recovery from runtime failures with the methane-oxidation reactive-MD case study**.

### 5.2 Primary literature — competitive agent systems

- **pubs.acs.org/doi/pdf/10.1021/acs.jcim.5c01938** — J&J *Mol Agent*, JCIM. Three-part agent hierarchy + MCP server.
- **arXiv:2507.17852** — Artificial Inc., *"Technical Implementation of Tippy: Multi-Agent Architecture and System Design for Drug Discovery Laboratory Automation."* Six-agent hierarchy with Safety Guardrail; Docker + Kubernetes per-agent isolation.
- **arXiv:2604.11661** — Recursion / LOWE companion paper on mechanistic action graphs.
- **https://www.recursion.com/lowe** — Recursion's official LOWE landing page.
- **https://github.com/valence-labs/VCR-Agent** — verifier-loop reference implementation; useful for the predict→test→falsify→improve pattern.

### 5.3 Commercial product documentation — deterministic incumbents

- **Schrödinger Multisim documentation** — `-set` flag (e.g. `-set "stage.[1]time=2.0"`) confirmed as the manual workflow-mutation interface; automatic recovery is checkpoint-restore only.
- **Schrödinger FEP+ documentation** — Pose Builder behavior, De Novo Design via Active Learning FEP+.
- **OpenEye / Cadence Orion documentation** — Floes (Python workflows) and Cubes (compute units with runtime conditional logic via standard `if/else` on data attributes; success / failure / custom ports).

### 5.4 Infrastructure documentation

- **docs.deepmodeling.com/projects/dpdispatcher/en/latest/machine.html** — DPDispatcher machine parameters; confirms `batch_type: "Shell"` for local execution.
- **docs.deepmodeling.com/projects/dpdispatcher/en/latest/context.html** — DPDispatcher supported contexts (`LocalContext`, `LazyLocalContext`, `OpenAPIContext`, `HDFSContext`, `SSHContext`).
- **github.com/deepmodeling/dpdispatcher** — source repository and getting-started guide.

### 5.5 Companion / memory-recipes literature

- **OpenBrain memory-recipes** (via MindStudio article; **NotebookLM-verified**). Source of the four-label memory provenance taxonomy (`observed from source` / `inferred by model` / `confirmed by user` / `imported from transcript`). An earlier draft of my notes had this as "Memory Providence" with three labels — both errors are now corrected.

### 5.6 Scoped out (mentioned, not central)

- **Iambic Therapeutics — NeuralPLexer2** — diffusion-based protein-ligand structure prediction. Surveyed as the "ML replaces MD" boundary marker; deliberately out of scope for an MD-automation project.

### 5.7 Established agent-systems literature (cited for design patterns, not chemistry-specific)

These ground the patterns the report relies on so I don't over-claim OpenClaw novelty for things that are well-attested elsewhere.

- **Plan-and-Solve prompting** (Wang et al.) — the established planner-agent pattern.
- **LangGraph / AutoGen / LangChain Plan-and-Execute** — production implementations of plan-and-execute that the planner skill draws from.

---

## Methodology note — how Phase 1 actually evolved

Phase 1 went through three rounds of revision, each forced by something I encountered.

**Round 1 — initial survey.** I read the primary sources and distilled them into vault notes. This produced solid coverage of the three agent systems (J&J Mol Agent, Tippy, Recursion LOWE) and the OpenClaw substrate paper.

**Round 2 — competitive landscape expansion.** I added the deterministic incumbents (Schrödinger FEP+/Multisim, OpenEye Orion) and the scoped-out boundary case (Iambic NeuralPLexer2). This is where the analytical thesis crystallized: systems get reliability by *removing the LLM* (Schrödinger, OpenEye), *removing the simulation* (Iambic), or — like OpenClaw — by *bounding the LLM's role to autonomous semantic reasoning over a deterministic core*. Two precise corrections from this round are worth flagging because they were the kind of thing a reviewer would catch: Schrödinger Multisim *can* mutate parameters (via the manual `-set` flag), so the contrast is autonomy, not capability; and Orion *does* branch dynamically at runtime (via Python Cubes with `if/else` on data attributes), so the contrast is semantic reasoning, not static-versus-dynamic.

**Round 3 — NotebookLM verification.** I uploaded the OpenClaw substrate paper into NotebookLM and systematically fact-checked the vault against it. This caught real overclaims: I had been attributing things to the paper that the paper didn't actually say. The biggest catches: "Memory Providence" was a propagated typo (the real term is **Provenance**), the taxonomy has **four** labels not three (we were missing `imported from transcript`), and the real source is **OpenBrain**, not the OpenClaw paper. Also, "Lobster as a DAG" and "git-backed reversibility" are not in the paper — those are vault framing. And DPDispatcher local-shell mode is not mentioned in the paper, but I separately verified it exists in DPDispatcher's own documentation (`batch_type: "Shell"` + `LocalContext`), which unblocks the local-only execution plan.

The vault now uses a three-tier discipline — paper-cited (✅), design idea / our framing (🟡), aspirational (⚪) — so for Phase 2 onward, what's load-bearing for the report stays cleanly separated from what's design opinion.

---

*End of Phase 1 Report.*
