---
tags: [project-prime, openclaw, session-handoff]
type: handoff
status: ready
---
# Next Session Starter — OpenClaw Phase

> Created 2026-05-24 at the close of the AMBER phase. Paste the block below into a fresh Claude Code session (run from the vault) to begin Phase 3. Everything outside the code block is orientation for you (the human); the code block is the actual prompt.

## What's already done (so you don't re-litigate it)
- **AMBER fully wrapped.** Prep/analysis = conda env `prime-amber` (AmberTools 24.8). MD engines = locally-compiled `pmemd` + `pmemd.MPI` at `~/Downloads/pmemd26/bin/`, both passing `make test.serial`/`test.parallel`. Auto-loaded via `amber.sh` in `~/.zshrc`. Recipe + gotchas in memory `pmemd-local-build`, Dev_Log 2026-05-22.
- **Golden path validated** — T4 lysozyme L99A + benzene (`181L`), full `pdb4amber → antechamber → tleap → sander → cpptraj → PLIP`. This is the known-good recipe the OpenClaw skills will automate.
- `pmemd.cuda` is N/A on this Mac (no NVIDIA) → production GPU stays the open `Gap_Remote_HPC_Backend` question, not a blocker.

## The prompt to paste

```
We're starting the OpenClaw phase of Project Prime (Phase 3). The AMBER side is fully
wrapped — read CLAUDE.md, Project Prime.md, Dev_Log.md (top entries), and project memory
before acting, then help me install and wire OpenClaw.

Hard constraints (from project memory — do not violate):
- Everything is LOCAL. No remote cluster. DPDispatcher, if used at all, runs in
  batch_type:"Shell" + LocalContext mode.
- LLM provider is Google AI Studio (Gemini) ONLY — not Ollama/local LLMs (this Mac can't
  host them), not Anthropic/OpenAI. ~$300 AI Studio credits, 90-day window. Default to
  Gemini Flash; use Gemini Pro only when complexity genuinely warrants the cost.
- Runnable code lives in ../project-prime/ (sibling to the vault), git on master, no
  commits yet. New skills go there in skill.md format (Markdown/YAML + Python/Shell).
  New design notes go in the vault first, matching the Arch_/OpenClaw_/Infra_/Skill_/
  Workflow_/Design_ taxonomy.
- Architecture discipline: the LLM is BARRED from the deterministic execution layer
  (Lobster DAGs + approval gates). Physical realism is non-negotiable (dt <= 2fs, etc.).
  Use bounded recovery, never freeform fixes. See Design_Determinism_Spectrum,
  Design_Memory_Provenance, OpenClaw_Lobster_DAGs, Workflow_Error_Recovery_Loop.

Immediate goals, in order:
1. Determine what "OpenClaw" actually is as installable software and how to install it
   locally. The vault notes are sourced from arXiv:2603.25522 + docs.openclaw.ai, and
   several framings (Lobster-as-DAG, MetaClaw/OpenClaw-RL) are UNVERIFIED design ideas,
   not confirmed product features — installing the real thing should ground them. Start
   with docs.openclaw.ai and the OpenClaw GitHub. CONFIRM the install method before
   running anything.
2. Wire the Gemini (AI Studio) API key into OpenClaw and verify a basic llm-task returns
   JSON-schema-validated output.
3. Verify OpenClaw can execute a basic local shell command (the deterministic substrate).
4. Then begin wrapping golden-path Stage 2 as the first real skill —
   Skill_Antechamber_LigandPrep (its acceptance test IS golden-path Stage 2). Keep it
   system-agnostic (any ligand, not hardcoded benzene).

Open decisions to surface rather than assume:
- Is there an internal Single Particle skill.md template, or do we use the public
  OpenClaw docs format?
- Where does the Gemini API key live / how should it be stored (not committed)?

Plan first, Taskboard-Manifest style: define stages, inputs, and validation conditions
before writing any execution logic.
```

## Likely first friction points (forewarned)
- **Does OpenClaw install cleanly at all?** This is the first real test of the framework, not just the vault's reading of it. Budget the session for discovery, not just execution.
- **Gemini API key handling** — must stay out of git (the vault already gitignores plugin `data.json` for the same reason; mirror that discipline in `../project-prime/`).
- **skill.md format** may differ from the vault's sketches once you see the real docs — treat existing `Skill_*` notes as design intent, not spec.
