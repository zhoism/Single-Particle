---
tags: [project-prime, openclaw, session-handoff, report, walkthrough, teaching]
type: handoff
status: ready
created: 2026-06-10
---

Below is what we will do FIRST!!!! Get this done before we do ANYTHING ELSE in this .md file!!

Here's the pre-prepared complex demo (protein–ligand complex) for Phase 3 explicit-solvent MD simulation (zipped). Once your Amber + OpenClaw environment is ready, please work through the following:

Understand the input file structure – go through the provided mdin files (min, heat, press, relax, prod) and make sure you understand key parameters like dt, cut, etc. Refer to Section 23.6 “General minimization and dynamics parameters” in the Amber26 manual for detailed explanations of key parameters.


Modify parameters using an Agent Skill – write an OpenClaw Skill that lets you specify which stage and which parameter to modify in natural language (e.g., "set the time step to 0.001 ps in the first heating stage"), then submit the job.

Once that works, extend the Skill to handle instructions like:

• "set the target temperature to 310 K" — update temp0 in all stages from the third stage onward (i.e., heat-3.in, press-3.in, relax.in, prod.in)

• "set the non‑bond cutoff to 7.0 Å" — modify cut in the mdin file.

• "relax the positional restraints from 5.0 to 1.0 in a specific heating or pressurization stage." — reduce restraint_wt 

Record and summarize – log whether each parameter change succeeds and how the Skill avoids mistakes (e.g., bounds checking, stage‑aware file targeting). The goal is a Skill that modifies parameters correctly and predictably, no matter how many times it's used.




> **✅ ADVISOR "FIRST" TASK — DONE 2026-06-11.** The 4-part mdin parameter-editing task above was demonstrated end-to-end on the provided files and recorded. It is the existing `mdin-edit` skill (project-prime `7b89568`): all four edits — `dt→0.001` heat-1, `temp0→310` group:third-onward (with `&wt value2` coupling resolving the heat-3 mismatch), `cut→7.0` group:all, `restraint_wt 5.0→1.0` press-1 — were driven in natural language via `openclaw agent` and came out **byte-identical to the deterministic CLI**; `--submit` ran the fully-edited set **10/10 pmemd normal termination**; robustness proofs (out-of-bounds reject, caught wrong-stage mis-map, idempotency, wrong-param refusal) + both acceptance suites green; all 10 originals byte-identical to session start. **Deliverable:** `phase3-explicit-solvent-md/mdin-edit_advisor_record.md`. **Log:** `Dev_Log.md` 2026-06-11 entry. **→ A fresh session should SKIP the advisor task and start directly at the A→K teaching walkthrough below.**

# Next Session Starter — Report Walkthrough (intuitive teaching pass over the whole pipeline)

> Created 2026-06-10. **This is NOT a build session — the pipeline is feature-complete (nine green skills).** It is a *teaching* session whose product is **your own understanding**, so you (the user) can write the internship report yourself. The next-session agent walks you through the entire explicit-solvent MD pipeline as one intuitive flow of logic — for each step: the **theory** (plain-language), the **goal**, the **issues** that step has, and **how our architecture remedies them** — then you type a paragraph of your understanding, the agent verifies it, and you move on. It also explains the **architecture**, the **tests**, and **what a GREEN really means**. Paste the §The prompt to paste block into a fresh Claude Code session (run from the vault).




## What's already done (don't re-build — this session is about UNDERSTANDING + WRITING)

- **Nine deterministic-wrapper skills, all GREEN** under `project-prime/skills/`: `antechamber-ligandprep`, `tleap-build`, `amber-md-run`, `cpptraj-analysis`, `plip-profile`, `mdin-edit`, `pipeline-async`, `amber-recover` (Stage 8), `md-planner` (Stage 7). Full local AMBER MD happy path runs end-to-end; system-agnostic in code; NL-drivable; the planner runs the chain manifest-first. project-prime HEAD `7b89568` (master, local, not pushed).
- **A full-project multi-agent review (2026-06-10) passed** — verdict ALIGNED_WITH_CONCERNS; 3 code fixes landed (cpptraj graceful-fail, tleap residue gate, detector-authoritative recover hook). The engineering is sound and on-thesis.
- **The deliverable is "a working agent demo + a written report."** The demo half is proven; **the report half is what you write next.** This session loads your head with the accurate, intuitive material to write it well.

## How this session runs — the teaching protocol (do this, in order)

For **each step** in the §Pipeline walkthrough sequence below, the agent:
1. **Explains intuitively** — theory (what is physically happening, in plain language) → goal → the issues this step has → how *our* architecture (deterministic wrappers, reused `check_amber` bounds, validation gates, bounded recovery, the planner) specifically remedies those issues. Keep it an intuitive flow of logic, not a parameter dump.
2. **Stops and asks you to write a paragraph** of your own understanding of that step.
3. **Verifies your paragraph** — confirms what's right, corrects what's off, fills what's missing. Only then move to the next step.

After the stage walkthrough, the agent explains: **the architecture as a whole** (the four layers + the determinism spectrum), **the tests** (oracle / acceptance / mutation / adversarial review — what each kind proves), and **what GREEN really means** (the four-tier distinction below — this is the single most important conceptual point for the report). That is all — no new building.

## ⚠️ FIRST: the advisor's specific task — explain its significance + contextualize it

Before the stage walkthrough, open the session by unpacking the advisor's instruction. The user's advisor said specifically (verbatim below); the agent must **explain the significance of this task and contextualize it in the broader MD scheme** — why it matters, where it sits in the pipeline, what it proves or de-risks.

> **[PASTE THE ADVISOR'S 15-LINE INSTRUCTION HERE — it did not transmit into the handoff. Drop it in verbatim before pasting the prompt; the session opens by explaining its significance and situating it in the broader MD pipeline.]**

## Pipeline walkthrough sequence (the spine — teach in this order, one intuitive flow)

Each entry is an *anchor* for the agent (accurate hook + the headline issue + the remedy + the note to pull detail from). The agent expands each into a live, intuitive explanation tuned to the user's paragraph-back — it does NOT read these aloud.

**A. Ligand parameterization — `antechamber-ligandprep`** → [[Skill_Antechamber_LigandPrep]]
- *Intuition:* teach the small molecule to "speak AMBER" — assign GAFF2 atom types + AM1-BCC partial charges so it has a force-field description; output mol2 + frcmod.
- *Issue:* aromatic perception can silently break (obabel kekulization failure → mis-typed ring → corrupts every downstream energy). *Remedy:* H-present PDB routed to `antechamber -fi pdb -j 4`; fatal `AROMATIC_PERCEPTION_FAILED` gate; net-charge-sum + type-recognized checks. (This is the bug we caught — all prior ΔG ≈ −13 values were computed on the mis-typed ligand and are retracted; after the typing fix, ΔG is −17.18.)

**B. System assembly & solvation — `tleap-build`** → [[Skill_Tleap_Build]]
- *Intuition:* glue typed protein (ff19SB) + typed ligand into one system, save the *dry* complex, then solvate in a TIP3P octahedral water box and neutralize with counterions.
- *Issue:* save-order corruption — saving "dry" *after* solvation yields a dry file secretly full of water → cryptic atom-count mismatch downstream. *Remedy:* deterministic leap.in saves comp_dry BEFORE solvateoct; gates assert dry < solvated, protein+ligand == dry, system neutral, + the new non-standard-residue gate (a stray crystallographic metal can't sneak through).

**C. The equilibration ladder — minimization → heating → pressure/density — `amber-md-run`** → [[Skill_AMBER_MD_Run]]
- *Intuition:* the random-placed system would explode if run cold. **Minimize** (3 passes, relieve clashes) → **heat** 0→300 K (NVT, Langevin thermostat, weak restraints) → **density/pressure** equilibrate to 1 atm (NPT, Monte-Carlo barostat). Each step hands its restart to the next.
- *Issue (heat):* thermostat mismatch — `temp0` ramps but `&wt value2` stays fixed → the thermostat fights itself (the heat-3 bug). *Remedy:* generated namelists couple `temp0`↔`value2`; `dt ≤ 2 fs` with SHAKE (`ntc=2 ntf=2`); `cut∈[8,12]`; every namelist passed through `check_amber`; a crash detector watches each `.out`.

**D. Production MD — `amber-md-run`** → [[Skill_AMBER_MD_Run]]
- *Intuition:* restraints off; run free at 300 K / 1 atm; snapshot coordinates to a NetCDF trajectory. This is the raw data for all analysis. Longer run → more independent samples.
- *Issue:* a silent NaN (energy NaN but an exit-0 banner prints) can corrupt the whole trajectory. *Remedy:* deterministic post-run detector (NaN/Infinity sticky; SHAKE-fail; non-finite final block) → feeds Stage 8.

**E. Stability & ensemble analysis — RMSD/RMSF, clustering, PCA — `cpptraj-analysis`** → [[Skill_CPPTraj_Analysis]]
- *Intuition:* did the protein stay folded (RMSD flat)? which residues wiggle (RMSF)? what distinct poses exist (clustering → medoid frames)? what are the dominant motions (PCA)?
- *Issue:* atom-count mismatch (the Stage-3 bug) breaks cpptraj cryptically; hardcoded masks break on other systems; PCA in one cpptraj call silently produces empty eigenvectors. *Remedy:* strip with the matching topology; auto-detect masks from `RESIDUE_LABEL`; PCA as two calls (diagmatrix → projection); ≥12-analyses gate; graceful-fail envelope (the review fix) instead of a bare traceback.

**F. Binding free energy — MM-GBSA — `cpptraj-analysis`** → [[Skill_CPPTraj_Analysis]]
- *Intuition:* the headline number. ΔG_bind = ΔG_MM + ΔG_solv (GB electrostatics + SASA hydrophobic). Negative = favorable. MMPBSA.py over the trajectory using the dry complex + protein + ligand topologies from Stage 3.
- *Issue:* short MD → noisy ΔG; a mis-fit ligand charge silently corrupts it. *Remedy:* deterministic MMPBSA invocation (igb=5, saltcon=0.1); ΔG<0 gate; the upstream aromatic gate protects the inputs. **Honest caveat (carry into the report):** a single short-run ΔG is an *illustrative sanity fingerprint*, not a converged affinity — it wanders ±1–2 kcal/mol.

**G. Interaction fingerprint — PLIP — `plip-profile`** → [[Phase3_Taskboard_Manifest]], [[Next_Session_Prompt_Stage6_PLIP]]
- *Intuition:* MM-GBSA says *how much*; PLIP says *why* — the specific non-covalent contacts (hydrophobic, H-bond, π-stacking, salt bridge…) on a representative medoid frame.
- *Issue:* resname footgun — AMBER variant names (HIE/CYX/…) make PLIP invent *phantom* ligands while missing the real one. *Remedy:* deterministic resname normalization (HIE→HIS…); gates require the ligand hetid is found AND zero unmapped non-standard residues remain (`UNMAPPED_NONSTANDARD_RESIDUES` — the review-hardened catch-all). **Caveat:** single-frame medoid, not trajectory-occupancy (that's v2).

**H. NL parameter editing — `mdin-edit`** → [[Dev_Log]] 2026-06-08 entries, [[Phase3_Taskboard_Manifest]]
- *Intuition:* English ("set the production timestep to 1 fs") → a bounds-checked, idempotent, stage-aware edit of the right mdin namelist, with a self-check and change log.
- *Issue:* a careless editor appends/duplicates, breaks the `temp0`↔`value2` coupling, or writes an out-of-bounds value. *Remedy:* parse-replace (never append), bounds via vendored `check_amber`, auto-couples `temp0`↔`value2`, independent-parser self-check. (Hardened by a ~240k-assertion fuzz/mutation harness.)

**I. Bounded runtime recovery — `amber-recover` (Stage 8)** → [[Skill_Bounded_Recovery_AMBER]], [[Workflow_Error_Recovery_Loop]]
- *Intuition:* MD crashes (NaN, vlimit, SHAKE-fail). Instead of letting the LLM invent a fix, recover within hard math bounds: **Tier-1** restore last checkpoint, resume as-is (zero physics risk); **Tier-2** (only on re-crash) lower dt + SHAKE-off for a short stabilize window, then restore; **HALT** `needs_human` if bounds exhaust.
- *Issue:* silent NaN slips past a banner-only check; Tier-2 could over-mutate. *Remedy:* deterministic IEEE-non-finite (sticky) detector; every mutated namelist gated by `check_amber`; refuses to breach the dt-floor → HALTs. This is the **paper-cited differentiator** (arXiv:2603.25522 / LOWE-style falsification) — *cite it as an adopted discipline realized deterministically, not as novel research.*

**J. The planning layer — `md-planner` (Stage 7)** → [[Arch_Taskboard_Manifest]], [[Design_Determinism_Spectrum]]
- *Intuition:* the one place the LLM legitimately reasons — goal → a JSON **plan manifest** over the *known* skill catalog (which stages, what params, what order, how wired). The wrapper is then pure-deterministic: **validate** (G0–G6: known catalog, acyclic DAG, inputs satisfied, params in `check_amber` bounds, typed) → **compile** to byte-inspectable calls → **execute** stage-by-stage, HALT on failure (recovery stays Stage 8's).
- *Honest framing (load-bearing for the report):* 🟡 **our framing of the standard plan-and-execute pattern.** Cite Plan-and-Solve (Wang et al.) / LangGraph / LangChain. **Do NOT call it "Taskboard Manifest"** (vault brand) and do NOT call it a novel paper contribution.

**K. Async orchestration + Discord — `pipeline-async`** → [[Dev_Log]] 2026-06-09 (Discord e2e), [[Phase3_Taskboard_Manifest]]
- *Intuition:* @-mention the bot → it launches the full detached pipeline → live per-stage Discord pings (🚀🧪🧬⚛️📊✅) → final ΔG + RMSD plot. The LLM is touched *once* (deciding to launch); everything after runs without it.
- *Remedy/property:* notifications via LLM-free `openclaw message send` (fire even during a 429); the `RECOVER` hook authoritatively re-checks for silent-NaN rather than trusting the run's own flag.

## The architecture, the tests, and what GREEN really means (teach after the walkthrough)

**The four layers** (frame against the determinism spectrum — reasoning over a deterministic core):
1. **Planning (intent→manifest)** — `md-planner`; LLM reasons, wrapper validates/compiles/executes.
2. **Deterministic execution (core)** — the 9 wrappers; *zero* LLM/network/randomness inside any wrapper; every output is a JSON envelope `{ok, skill, outputs, validation, errors}`; bounds **reused** from `check_amber`, not invented.
3. **HPC grounding (deferred)** — local pmemd proven (`make test.serial` 212 pass); remote dispatch is [[Gap_Remote_HPC_Backend]], an `--engine` seam, **not built**.
4. **Resilience (bounded safety)** — `amber-recover` + the `RECOVER` hook; deterministic detect → bounded recover → HALT.

**The tests — what each kind actually proves:**
- *Oracle tests* — an **independent reimplementation** of the logic (e.g., the detector / validator), cross-checked on py3.9 + py3.11. Proves the engine isn't grading its own homework.
- *Acceptance tests* — real `pmemd`/`antechamber` runs on golden + unrelated + malformed inputs → asserts the envelope is right (golden ok, malformed `ok:false`).
- *Mutation/fuzz* — deliberately break the code/inputs and confirm the tests/gates catch it (mdin-edit: 8/8 mutants killed, ~240k assertions).
- *Adversarial 2nd-AI review* — an independent skeptic hunts silent-pass holes before "done" (caught a real HIGH bug in each recent session). This is the `Eval_Criteria.md` discipline.

**What a GREEN really means (the key conceptual point — four tiers):**
- A GREEN is a **passing deterministic gate / envelope-ok / bounds-satisfied artifact — NOT a claim of physical or biological correctness.**
- *Run-GREEN* (amber-md-run / planner execute): pmemd hit normal termination, no NaN, trajectory exists. ≠ the affinity is right (single-trajectory MM-GBSA noise is ±1–2 kcal/mol — see the −17.18/−17.6/−18.49 spread on the *same* system).
- *Analysis-GREEN* (cpptraj / PLIP): ≥12 analyses produced, ΔG<0, ligand found, zero phantoms. Certifies the analysis ran deterministically and is self-consistent — not that the number is biological ground truth.
- *Detector-GREEN* (amber-recover): a crash/silent-NaN was caught and the mutated params stayed in-bounds — not a guarantee recovery is numerically perfect.
- *Review-GREEN* (adversarial pass): the envelope is honest and the gates work as documented — not a proof of zero bugs.
- **The power of the thesis:** a silent failure (mis-typed aromatic, phantom ligand, out-of-bounds namelist pmemd happened to finish) *cannot* pass a GREEN — it trips a named gate (`AROMATIC_PERCEPTION_FAILED`, `UNMAPPED_NONSTANDARD_RESIDUES`, `ORIGINAL_NAMELIST_OUT_OF_BOUNDS`) and returns `ok:false`.

## Banked framing constraints for when YOU write the report (do NOT violate these)

- **No codename.** The work is "the OpenClaw + AMBER agentic pipeline" / "the project." **"Project Prime" must NOT appear** in any delivered report. ([[feedback-project-prime-name]])
- **Ruthless-editor format** ([[phase1-report-format]] / `Eval_Criteria.md`): tight exec summary, no fluff, every claim sourced (commit/run-id/file), every link resolves. Spine = [[Design_Determinism_Spectrum]] (reasoning over a deterministic core vs hard-coded incumbents).
- **Tier honesty (the four traps):**
  1. Planner = 🟡 *our framing* of plan-and-execute → cite Plan-and-Solve / LangGraph, NOT "Taskboard Manifest", NOT "novel."
  2. Bounded recovery = ✅ adopted discipline (Multisim / LOWE), paper-grounded (arXiv:2603.25522). The IP is the *deterministic wrapper realization + verified test suite*, not the concept.
  3. ΔG ≈ −17 = 🟡 illustrative sanity fingerprint, NOT a converged affinity. The real proof is correct aromatic typing + topology integrity + reproducibility + vdW-dominated decomposition.
  4. The decoupled-wrapper architecture = "one validated approach to keeping LLM output from corrupting chemistry," NOT "the only safe way."
- **Numbers to cite (honest):** ΔG −17.18 / −17.6 (two 20 ps 1L2Y runs, post-aromatic-fix); −17.94 (planner manifest-first *execute*, `--sim-ps 1` production — the 50 ps figure is only the dry-run *plan* assertion, not a run); 306 dry / 5986 solvated atoms; 12 analyses + ≥10 PNGs; nine ✓-ready skills. **Do NOT cite ΔG −13** (mis-typed ligand, retracted). **Do NOT claim** HPC dispatch is built, or arbitrary-ligand *live* proof (live runs were all 1L2Y; cross-system is code-level only — 3HTB was a scripted run, not agent-driven).

## Decisions banked — do NOT re-litigate

- This is a **teaching/writing** session, not a build. No new skills, no edits to `run_happy_path.sh`, no pushing. ([[feedback-autonomous-vault]] still applies to vault upkeep, but the report is the user's to author.)
- Max 3 named agents; no LLM inside any wrapper. ([[multi-agent-scope]], [[openclaw-canonical-paths]])
- Verify-and-eval discipline applies to any claim that goes in the report — ground it in committed code, don't self-attest. ([[feedback-verify-and-eval]])

## What's NOT done (deferred, non-blocking — post-report frontiers)

- **The report itself** — this session builds the understanding; you write it after (or in a following session).
- **[[Gap_Remote_HPC_Backend]]** — Scenario A (local) vs B (remote pmemd.cuda + Slurm via DPDispatcher); an advisor/design decision, no cluster yet.
- **Polish / v2** — registry per-key type tags; planner `--from-goal` (deliberately unbuilt — breaks the determinism thesis); per-frame PLIP occupancy. (Carried forward from the now-superseded `Next_Session_Prompt_HPCorPolish.md`.)

## The prompt to paste

```
Continuation of the Single Particle / OpenClaw + AMBER project. This is a TEACHING session, NOT a build — the pipeline is feature-complete (nine green deterministic-wrapper skills, project-prime HEAD 7b89568, master/local). Goal: walk ME (the user) through the ENTIRE explicit-solvent MD pipeline as one intuitive flow of logic, so I can write the internship report myself. Do NOT build, edit run_happy_path.sh, or push.

The teaching loop, for EACH step in the pipeline (in order A→K below): (1) explain it INTUITIVELY — theory in plain language → the goal → the issues that step has → how OUR architecture (deterministic wrappers, reused check_amber bounds, validation gates, bounded recovery, the planner) remedies those issues. Intuitive flow, not a parameter dump. (2) STOP and ask me to type a paragraph of my own understanding. (3) Verify my paragraph — confirm/correct/fill — then move on. After the walkthrough, explain: the architecture (four layers + the determinism spectrum), the tests (oracle / acceptance / mutation / adversarial review — what each proves), and WHAT A GREEN REALLY MEANS (the four-tier distinction: run / analysis / detector / review GREEN — a GREEN is a passing deterministic gate, NOT a claim of biological correctness). That is the whole session.

NOTE: the advisor's specific "FIRST" task (a natural-language mdin parameter-editor + submit) is ALREADY DONE — demonstrated end-to-end and recorded (see the ✅ banner at the top of this handoff + phase3-explicit-solvent-md/mdin-edit_advisor_record.md + Dev_Log 2026-06-11). Do NOT re-run it. When you reach step H (mdin-edit) you may briefly point at that record; otherwise go straight into the A→K walkthrough.

Read these BEFORE acting (the handoff has the full per-stage map + anchors):
- vault: Next_Session_Prompt_ReportWalkthrough.md (THIS session's plan — the pipeline sequence A→K, the GREEN-tier breakdown, the report framing constraints)
- vault: Design_Determinism_Spectrum (the spine), Arch_Pipeline_System.md (the system overview / report seed — note it's a 5-skill snapshot, refresh mentally to all 9), Eval_Criteria.md
- vault per-stage: Skill_Antechamber_LigandPrep, Skill_Tleap_Build, Skill_AMBER_MD_Run, Skill_CPPTraj_Analysis, Phase3_Taskboard_Manifest (PLIP/Stage6 + status), Skill_Bounded_Recovery_AMBER, Workflow_Error_Recovery_Loop, Arch_Taskboard_Manifest
- memory: project-prime-status (CRITICAL — nine skills, what's proven), feedback-project-prime-name (NO "Project Prime" codename in the report), phase1-report-format (ruthless-editor), feedback-verify-and-eval, antechamber-aromatic-kekulize-bug (the ΔG −13 retraction)

Pipeline sequence to teach (intuitive flow): A ligand parameterization (antechamber-ligandprep) → B system build & solvation (tleap-build) → C equilibration ladder: minimize→heat→pressure/density (amber-md-run) → D production MD (amber-md-run) → E stability/ensemble analysis: RMSD/RMSF, clustering, PCA (cpptraj-analysis) → F MM-GBSA binding free energy (cpptraj-analysis) → G PLIP interaction fingerprint (plip-profile) → H NL parameter editing (mdin-edit) → I bounded recovery (amber-recover) → J the planning layer (md-planner) → K async orchestration + Discord (pipeline-async).

Tier-honesty I MUST keep in the report (state these as we go): planner = our framing of plan-and-execute (cite Plan-and-Solve/LangGraph, NOT "Taskboard Manifest", not novel); bounded recovery = adopted discipline realized deterministically (arXiv:2603.25522), the IP is the wrapper + test suite; ΔG ≈ −17 is an illustrative sanity fingerprint NOT a converged affinity (don't cite the retracted −13); the architecture is "one validated approach," not "the only safe way"; HPC dispatch is NOT built; live agent runs were all 1L2Y (cross-system is code-level only).

Scope-fence: explanation + my-paragraph verification ONLY. Do NOT write the report for me, build anything, or modify code/pipeline. If I ask to start drafting the report, that's fine — but the default is: you teach, I write the understanding paragraphs, you verify.
```

## After the session — update this file

1. Flip frontmatter `status: ready` → `status: consumed`.
2. Add an `## Outcome` footer: consumed YYYY-MM-DD, 1-sentence outcome (which steps were walked, whether the report draft started), link to the [[Dev_Log]] entry.

## Cross-links

- `Next_Session_Prompt_HPCorPolish.md` (now `status: superseded`) — the prior frontier-choice handoff; the user picked the report path, which this handoff serves. HPC + polish frontiers carried forward above.
- [[Design_Determinism_Spectrum]] — the report spine. [[Arch_Pipeline_System]] — the system-overview seed (5-skill snapshot; refresh to 9).
- [[Eval_Criteria]] — the rubric the report is graded against.
- memories: [[project-prime-status]], [[feedback-project-prime-name]], [[phase1-report-format]], [[feedback-verify-and-eval]], [[antechamber-aromatic-kekulize-bug]].
