---
tags: [architecture, competitor, fep, deterministic, ligand-prep, recovery]
---
# Architecture: Schrödinger FEP+ / Multisim

**Core Concept:** The *fully deterministic* end of the workflow-automation spectrum. Schrödinger achieves reliability not by reasoning carefully but by **removing the LLM entirely** — every step is a hard-coded, algorithmically validated pipeline tuned for its own FEP engine.

**What FEP+ is:** Free Energy Perturbation — a physics-based computational method for predicting binding affinity. `FEP+` is Schrödinger's drug-discovery-specific implementation.

**Key Features (and how each maps to Project Prime):**
* **FEP+ Pose Builder** — automatically handles ligand preparation, reference identification, and system setup. This is the deterministic mirror of our [[Skill_Antechamber_LigandPrep]]: same job (format ligands perfectly for the downstream engine), but a rigid hard-coded pipeline rather than an agent reasoning about non-standard residues. *Lesson: the happy path can and should be deterministic; reasoning is only warranted for the inputs that break the pipeline.*
* **De Novo Design via Active Learning FEP+** — iteratively trains an ML surrogate model on physics-based FEP+ data to triage novel chemical structures cheaply. This is the *deterministic, domain-specific analog* of [[OpenClaw_Self_Evolution]] — learning from accumulated simulation data, but via a fixed ML loop rather than an agent rewriting its own skills.
* **Multisim recovery** — automates sequential MD tasks. The precise behavior matters: its *automatic* retry on a crash (hardware failure / timeout) is a strictly **bitwise-accurate checkpoint-restore** — it resumes from the last `.cpt` with identical config and does **not** autonomously diagnose the physical state or mutate parameters (`dt`/SHAKE). Parameter mutation *is* supported, but only **human-in-the-loop**: a manual command-line restart with the `-set` flag (e.g. `-set "stage.[1]time=2.0"`) injects "workflow mutations" before resuming from the checkpoint. So the contrast with [[Skill_Bounded_Recovery_AMBER]] is precisely **autonomy**, not capability: OpenClaw computes and applies bounded parameter adjustments *automatically* in response to a crash; Multisim's automatic path is restore-only, and any mutation requires a human in the loop. (See that note's "Two recovery philosophies" section.)

**Why it matters for the report:** Schrödinger is the proof that the *deterministic execution core* is industry-validated — nobody hand-waves chemistry through an LLM. The gap it leaves is its strength inverted: a hard-coded pipeline cannot adapt to a system it wasn't pre-built for. That adaptation gap is OpenClaw's entire value proposition. See [[Design_Determinism_Spectrum]].

**Source:** User Phase 1 competitive-landscape research, 2026-05-18 (Round 2). Raw notes in [[Research_Phase1_Survey]].
