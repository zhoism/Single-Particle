---
tags: [amber, tleap, antechamber, parameterization, force-field]
---
# Skill: Antechamber & Ligand Parameterization

**The User Pain Point:** Force field parameterization is highly sensitive to naming conventions. The `tleap` compiler is incredibly unforgiving—minor typos, missing spaces, or non-standard residues/custom ligands cause complete compiler halts. Manual `.pdb` editing and command-line parameter generation is tedious and error-prone.

**The OpenClaw Solution:**
An autonomous `antechamber` skill designed to bypass human formatting errors. 
* **Execution:** When `tleap` flags a missing parameter or non-standard residue, this skill is invoked.
* **Capabilities:** It autonomously processes the new ligand, generates AM1-BCC charges, assigns GAFF (General AMBER Force Field) atom types, and compiles the topology files. 
* **Friction Reduced:** Completely eliminates the need for the user to manually open and format `.pdb` files, acting as a deterministic text-formatter and parameter generator.

**Acceptance test:** the **golden path** (`project-prime/golden-path/`, validated 2026-05-21) Stage 2 exercises this exact chain — `obabel +H → antechamber (GAFF2 + AM1-BCC) → parmchk2` — but now on a ligand pulled from a *real crystal structure* (benzene from PDB `181L`) and fed into a combined protein–ligand `tleap` build, not in isolation. That run also surfaced a downstream integration bug this skill should guard against: AMBER's protonation-variant residue names (`HIE/HID/HIP`, `CYX`, …) must be normalized back to standard PDB names before PLIP, or PLIP misreads them as phantom ligands. See [[Dev_Log]] 2026-05-21.

**Source:** User pain-point analysis in [[Research_Phase1_Survey]] (Force Field Parameterization section).