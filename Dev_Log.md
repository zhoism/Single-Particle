---
tags: [dev-log, project-prime, chronological]
type: log
---

# Dev Log — Project Prime

*Reverse-chronological session log (latest entry on top). Complements the topic-organized vault by giving a time-ordered "what was done when" trail. Each entry is a marker + pointers to artifacts, not a duplicate of the work itself.*

---

## 2026-05-19 — Phase 1 closed; transitioning to AMBER install

**Done today:**
- NotebookLM verification of the OpenClaw substrate paper (arXiv:2603.25522) caught real overclaims in the vault. Corrections propagated through every affected note. Strongest paper-cited element: **bounded recovery + methane-oxidation case study** — anchored in [[Skill_Bounded_Recovery_AMBER]].
- Memory Provenance properly sourced to **OpenBrain** (not the OpenClaw paper); renamed from "Providence" (propagated typo); corrected from 3 labels to **4** (added `imported from transcript`). Old file deleted; all wikilinks updated.
- DPDispatcher local-shell mode verified against DPDispatcher official docs (`batch_type: "Shell"` + `LocalContext`) — local-only execution plan unblocked.
- Demoted `Arch_Taskboard_Manifest` to a planner-agent design idea (it's the plan-and-execute pattern, not OpenClaw-novel); demoted `OpenClaw_Self_Evolution` (MetaClaw / OpenClaw-RL) to aspirational, out of report scope.
- Three-tier discipline now in effect across the vault: ✅ paper/source-cited · 🟡 design idea / our framing · ⚪ aspirational. Tier badges at the top of every affected note.
- Phase 1 report written in both full ([[Phase1_Report]]) and brief ([[Phase1_Report_Brief]]) versions.

**State of the vault:** Phase 1 is closed. Citation discipline is in place — the report cites *underlying patterns* from established literature for design choices that aren't OpenClaw-paper-novel, and the OpenClaw-paper-confirmed mechanics (Lobster engine, `llm-task`, approval gates, DPDispatcher lifecycle, bounded recovery) are clearly labeled. Nothing unverified is masquerading as paper-grounded.

**Next session — Phase 2 step 1: install AMBER + agent stack locally.**
- Hardware: macOS, CPU-only (no NVIDIA → no `pmemd.cuda`).
- Path: `conda install -c conda-forge ambertools` (gives `sander`, `tleap`, `antechamber`, `cpptraj`) + `pip install plip`.
- Validate end-to-end by hand on a tiny solvated ligand or small peptide *before* writing any skill — need a working baseline the agent will automate.
- Then `npm install -g openclaw@latest` and configure the LLM provider (clarify GCP credits vs. AI Studio first; Gemini Flash as primary; Ollama as offline fallback).

Continuation happens in a fresh chat to keep that session's context window short and fast for shell back-and-forth.
