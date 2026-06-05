---
tags: [research, prior-art, claude-code, skill, amber, md, competitor, steal-list]
type: research
status: prior-art-assessed
source: github.com/baifan-wang/skills (amber-md) + WeChat article 2026-06-03
date: 2026-06-04
---

# Research note — `amber-md` Claude Code skill (baifan-wang)

**Status:** 🟡 Prior-art assessed. Repo cloned + `SKILL.md` (320 lines) and `references/troubleshooting.md` read directly; WeChat walkthrough article (ferlich/Moubai123, 2026-06-03) read in full. Source PDF: `Weixin Official Accounts Platform.pdf` (Downloads).

> baifan-wang. *skills/amber-md* — "Amber 分子动力学模拟全流程助手." GitHub. Claude Code skill. Companion autodock skill in same repo.

## What it is

A **Claude Code skill** that automates the full protein–ligand explicit-solvent AMBER26 MD pipeline. NOT a one-system demo (the article undersold it) — `SKILL.md` handles **protein-ligand / pure-protein / protein-protein**, ff19SB/ff14SB, TIP3P/OPC, GAFF2, and emits **bash + Slurm + PBS** run scripts. Four-stage design with stage-routing-by-entry-state:

- **Stage 0** — fixed 6-question intake (charge, GPU/CPU, scheduler, duration, analyses, force field).
- **Stage 1** — antechamber/parmchk2/tleap. *LLM executes inline.*
- **Stage 2** — generates min×3 / heat / density / product `.in` + run script. *User runs the long job.*
- **Stage 3** — 10 cpptraj analyses + matplotlib plots. *LLM executes inline.*
- **Stage 4** — symptom→cause→fix lookup table (`troubleshooting.md`).

## Does this guy do our job? — verdict

**No.** He commoditized the **local single-machine happy path** (≈60%) and punted on all three of our actual differentiators (see [[CLAUDE]] three-layer thesis):

1. **Deterministic execution layer** — he has NONE. The LLM writes `leap.in` + every `mdin` inline and runs them; "guardrails" are prose in markdown. This is exactly the hallucination-in-mission-critical-chemistry risk our decoupled [[OpenClaw_Lobster_DAGs]] architecture exists to kill. He is structurally exposed to it.
2. **HPC grounding** — he generates a Slurm/PBS *script* and hands it to the user. No dispatch, no monitoring, no job-state-as-workflow-state, no remote backend. Untouched = [[Gap_Remote_HPC_Backend]]. He assumes you own the GPU box and babysit `bash run.sh`.
3. **Bounded recovery** — a reactive lookup table, not the automated bounded loop ([[Workflow_Error_Recovery_Loop]] / [[Skill_Bounded_Recovery_AMBER]]). Fixes are text advice ("reduce dt to 1fs"); human applies by hand. No retry counter, no checkpoint-resume.

Also no **PLIP** (MM-GBSA + cpptraj `hbond` only); Claude Code skill format won't drop into OpenClaw.

**Strategic implication:** the "automate local AMBER MD on one machine" framing of our project is now demonstrably trivial — *someone shipped it, well.* That was never our banked deliverable. The non-trivial value is the deterministic layer + HPC orchestration + bounded auto-recovery + PLIP. His existence **sharpens** scope rather than threatening it: adopt his happy-path as the commodity baseline, own everything above it. The seam where he says "now go run `bash run.sh` for 5 hours" is exactly where [[Infra_DPDispatcher]] dispatch-and-monitor plugs in.

## Steal list (validated heuristics — language/framework-agnostic)

Drop into [[Skill_Antechamber_LigandPrep]] / tleap / cpptraj skill references:

1. **Save `comp_dry.top` BEFORE `solvateoct`** — + sanity test (dry ≪ solvated, ~267K vs ~1.3M bytes) + save `protein.top` & `ligand.top` separately for MM-PBSA components. He gives the *verification test*, not just the rule.
2. **`-nc` net charge mandatory**, integer, ask user (confirms our antechamber gotcha).
3. **Residue-number conflict → renumber ligand** (his `sed 's/MOL A   6/.../'` is brittle — a place to *beat* him with a general fix).
4. **cpptraj footguns**: PCA = two calls (`diagmatrix`+`run`, then `projection` from evecs file); `cluster ... repout rep repframe` must be ONE command; `hbond` "no data" is not an error (report hydrophobic/π-π).
5. **Python parsing gotchas**: `evecs.dat` manual-parse (not `read_csv`); `summary.DENSITY` sometimes 1-col; cluster `summary.dat` header eats column names.
6. **Analysis preprocessing + relative-path convention**: `strip → center → image → rms` first; every module `parm ../../prep/comp_dry.top` + `trajin ../strip/strip.nc`.
7. **3-step minimization restraint ladder** (min1 solvent-only `restraint_wt=500` → min2 `+ !@H=` → min3 free `ntr=0`) — leaner than advisor's 11-stage chain; diff via `md-param-check` ([[Phase3_Taskboard_Manifest]]).
8. **`scripts/process_mdout.perl`** bundled — ready TEMP/DENSITY/ETOT extraction.

Design patterns worth adopting: **stage-routing-by-entry-state** (intake UX for [[Arch_Taskboard_Manifest]]); **pause-and-confirm per stage + explain WHY** (approval-gate fit).

**Do NOT steal:** his LLM-writes-everything-inline architecture; his "recovery = lookup table" story. Those are our differentiators.

## Cross-links

- Decision context: [[Research_El_Agente_Q]] (the other prior-art assessment; multi-agent scope banked).
- Open problem this validates: [[Gap_Remote_HPC_Backend]].
- Skills receiving the steal-list: [[Skill_Antechamber_LigandPrep]], [[Skill_Bounded_Recovery_AMBER]].
