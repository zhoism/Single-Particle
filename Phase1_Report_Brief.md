---
tags: [report, phase-1, market-research, deliverable, brief]
type: report
status: draft-for-review
date: 2026-05-19
companion: Phase1_Report.md
---

# Phase 1 Report — Brief Version

**Kevin Zhou · 2026-05-19 · Project Prime**

*One-paragraph version: the field is converging on AI agents that **think** but don't **execute** — a separate deterministic engine actually runs the chemistry, and the LLM is allowed to reason only over the parts no one pre-scripted. Project Prime's niche is the one piece even the strongest commercial tools don't do: **autonomous, mathematically-bounded recovery** when a molecular-dynamics simulation crashes in the middle of the night.*

---

## 1. What "OpenClaw Agent Skills" means for MD

OpenClaw is an agent framework where the LLM does the thinking and small markdown-defined "skills" do the actual work — each skill teaches the agent how to operate one tool (like `tleap`, or AMBER's `sander`, or the HPC scheduler) safely. The split matters for molecular dynamics because the underlying software is extremely picky — one typo or bad parameter ruins a multi-day run, so you don't want the LLM inventing chemistry. Instead of one giant "do MD" capability, you break the work into focused skills: ligand setup, parameter validation, running the job, recovering from crashes, analyzing results. The LLM's job is to translate the scientist's natural-language goal into the right sequence of skill calls and to handle unexpected errors — never to invent chemistry parameters itself.

## 2. Five US organizations doing related work

I surveyed five US companies. Three are agent-based: **Johnson & Johnson's Mol Agent** (JCIM 2025) uses three coordinated AI agents to autonomously build ML models from molecular data; **Artificial Inc.'s Tippy** (arXiv:2507.17852) is a six-agent system that runs an entire drug lab, each agent containerized with a safety filter on top; and **Recursion's LOWE** lets scientists chain experiments in plain English and uses a "verifier" agent that tries to disprove its own conclusions before acting (this verifier pattern is what my error-recovery loop borrows from). The other two are deterministic incumbents I included to map the contrast: **Schrödinger's FEP+ and Multisim** run hard-coded pipelines that are very reliable but only auto-recover by restoring a checkpoint — parameter changes require a human to manually invoke a `-set` flag; **OpenEye's Orion** uses Python workflows with real runtime branching, but only handles the failures a developer pre-wrote an `if` for. The takeaway: the established players get reliability by removing the AI's freedom, and the agent-based players keep the AI but contain it — that's the niche Project Prime fits into.

## 3. Technology trends

A few patterns showed up everywhere. The biggest is **separating LLM reasoning from execution** — the LLM proposes, but a deterministic engine runs the chemistry, with the LLM's outputs forced into structured JSON instead of free-text replies. **Memory provenance** is becoming standard: every piece of information the agent holds gets tagged by where it came from (observed from a log, confirmed by the user, just guessed by the model, or imported from earlier conversation), and the agent isn't allowed to act on guesses until they're verified — this is from a project called OpenBrain that ships memory recipes alongside OpenClaw. **Bounded recovery** — letting the agent fix runtime crashes within hard mathematical limits rather than blindly restoring a checkpoint or letting the AI improvise — is the specific pattern Project Prime targets, and the OpenClaw paper directly validates it with a methane-oxidation case study.

## 4. User pain points and how OpenClaw addresses them

MD users complain about two things mainly. First, **force-field setup is brutal** — `tleap` (AMBER's topology tool) rejects anything with a typo, missing space, or non-standard ligand, and the error messages are useless, so users end up hand-editing PDB files atom by atom. Second, **simulations crash unpredictably at any hour** from temperature spikes or coordinate explosions, and the researcher has to manually parse log files, edit the config, lower the timestep, disable SHAKE, and restart — "constant babysitting," as one source put it. OpenClaw's answer is two skills: an **antechamber-wrapper skill** that auto-formats ligands and generates parameters (no human required for the brittle prep work), and a **bounded-recovery skill** that watches the log, detects crashes by regex, applies a pre-defined fix within hard limits, and resumes — so the researcher can actually sleep through the night.

## 5. Sources

Four buckets. **Primary papers**: the OpenClaw substrate paper (arXiv:2603.25522, NotebookLM-verified line-by-line), plus the agent-system papers from J&J (JCIM 2025), Artificial Inc. (arXiv:2507.17852), and Recursion (arXiv:2604.11661 + recursion.com/lowe). **Commercial product docs** for Schrödinger Multisim/FEP+ and OpenEye Orion, used for the deterministic-incumbent contrast. **Infrastructure docs**: DPDispatcher on GitHub (deepmodeling) for HPC dispatch, and OpenBrain memory-recipes for the four-label provenance system. **Background literature** on the plan-and-execute pattern (Plan-and-Solve, LangGraph) to ground the parts of the architecture that aren't OpenClaw-novel.

---

*Methodology in one sentence: my early notes had some overclaims (I'd attributed concepts to the OpenClaw paper that turned out to live in companion projects, and one term — "Memory Provenance" — I'd been spelling as "Providence" with the wrong label count) — NotebookLM verification caught all of it before this report, and the corrected facts are what's above.*

*Full version with detailed citations and per-organization deep-dives in [[Phase1_Report]].*
