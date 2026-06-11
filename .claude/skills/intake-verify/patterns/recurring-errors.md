# Recurring intake-error patterns

Catalog of failure modes observed across Phase 1 intakes (2026-05-25 → 2026-05-28). Each entry: name, detection cue, what to do.

---

## 1. Org-halo aggregation

**Cue:** Block attributes a pile of OSS / academic papers to one commercial org. Multiple author affiliations crammed under a single "Org" field.

**Detection:** Pull the actual author list from each cited paper. Cross-check affiliations.

**Past hits:**
- **Cadence/OpenEye** (2026-05-27): claimed OpenMM 8 (Stanford Eastman), espaloma (Chodera), OpenFE (consortium), Sabanés Zariquiey JCIM 2024 (Acellera/Chodera). None are OpenEye.
- **Espaloma** (2026-05-27): block claimed "extensive Relay Therapeutics collaboration" — Relay not in author list, flagged unverified in the block's own UNCERTAINTIES.

**Action:** Trim org to actually-affiliated authors. Note dropped affiliations in Dev_Log.

---

## 2. Fabricated recovery (the thesis-threatening one)

**Cue:** Uncited "Actionable Takeaways" / "Architecture" / "State Management" paragraph claiming the tool does autonomous physics-mutation recovery (dt reduction, SHAKE toggle, velocity reinitialization, λ-window re-queue on crash). This is **our exact niche** — fabrication of it directly threatens the thesis.

**Detection:** Search the section header for "actionable" / "engineering takeaway" / "state management" / "recovery". If uncited, treat as Gemini's own advice to the reader, not the tool's behavior. Verify against actual product docs / GitHub issues — real auto-recovery would be a feature page or documented Lobster-style flow.

**Past hits:**
- **Exscientia** (2026-05-27): claimed BioSimSpace "catches the error, reduces the timestep, increments the Langevin seed, re-queues the crashed λ-window." Verified false against BioSimSpace docs + issue tracker (users hit crashes and fix manually).
- **Cadence/OpenEye** (2026-05-27): claimed orchestrator "adjusts state parameters (reduces dt, applies soft-core, re-initializes velocities)." Orion's documented behavior is `if/else` routing with explicit "novel error stalls" ceiling — already in matrix row 7.

**Action:** Drop the claim. If the tool would be a real near-miss without the fabrication, harden the relevant report bullet with a one-sentence inoculation naming the tool + "the auto-recovery claim could not be substantiated." If the tool is orthogonal to our niche even without the claim, no report edit (do not import the misconception).

---

## 3. Role-swap / paper-misattribution

**Cue:** Block cites a paper but describes a different paper's content. Or attributes a headline result to the wrong paper.

**Detection:** Pull the actual title + abstract of every cited DOI/arXiv. Does it match the block's description?

**Past hits:**
- **Aqemia** (2026-05-27): block implied JCIM 2020 (`0c00526`) was the biomolecular demo. Actual: that's the FreeSolv hydration paper (small-molecule physics); the biomolecular demo is arXiv:2109.03565 (COVID 3ClPro screen).
- **Cadence/OpenEye** (2026-05-27): "0.97→0.47 kcal/mol TYK2" attributed to Sabanés Zariquiey 2024. Actually Rufa et al. (Chodera) prior work.

**Action:** Correct the source labels in the Sources block. Note the swap in Dev_Log.

---

## 4. Fabricated source / non-existent paper

**Cue:** arXiv ID, DOI, or paper title that cannot be resolved.

**Detection:** WebFetch the URL. arXiv: a real ID returns the `/abs/` page even for obscure papers; 404 = ID doesn't exist. Title search: zero hits across Google Scholar / arXiv / DOI = fabrication. Cross-check author names — real authors have other findable work.

**Past hits:**
- **STAR-MD** (2026-05-28): arXiv:2602.02128 → 404. Title "Spatio-Temporal Autoregressive Rollout for Molecular Dynamics" → zero hits. Tool name → nothing in this space. The block was Gemini synthesizing a plausible paper from real analogues (Timewarp, MDGen, BioEmu).

**Action:** STOP. Default-NO. Write a fabrication Dev_Log entry. Do NOT add a "rejected" row to the matrix — the report should not import the misconception. **This is also the lesson that link-resolution must precede everything else** — STAR-MD passed the hardened-format provenance discipline because the link was stamped READ-directly without being checked.

---

## 5. Generative-platform MD-washing

**Cue:** Generative design platform (RL-scored ligand generation, docking-scored reward) claiming to be "physics-based" or to "run MD as the reward function." The single distinguishing claim is `DOES-IT-RUN-MD: yes` and the bottleneck is `workflow orchestration` or `binding affinity`.

**Detection:** Read the actual reward function from the cited paper / docs. Is it docking + ADMET + ligand-based scoring? Or is there a real MD/FEP loop with trajectory integration?

**Past hits:**
- **Insilico Chemistry42** (2026-05-27): JCIM 2023 — 42 generative algorithms + RL scoring; reward is docking + ligand-based, not MD/FEP. Block's own DISCONFIRMING-EVIDENCE predicted exactly this.

**Action:** NO row. One-line mention in the existing "orchestration, not MD mechanics" bullet (generative-design platform, docking-scored reward, not MD). Do not promote to scope-out.

---

## 6. Materials-domain mislabel

**Cue:** Block fields `DOMAIN: biomolecular` but the cited paper is materials science (crystals, polymers, batteries, OLED, inorganic).

**Detection:** Read the paper title + first paragraph. Materials-science venues (Chem. Mater., npj Comput. Mater., the "Materials Science" division of Schrödinger's product line, GNoME's crystal stability) are tells.

**Past hits:**
- **MatterSim** (2026-05-25): universal ML-FF for inorganic materials. Scoped out.
- **MPNICE** (2026-05-25): arXiv:2505.06462 = liquid + materials properties; Schrödinger Materials Science suite. Block claimed "built to drive Desmond / drug-discovery MD" — false. Scoped out.
- **GNoME** (2026-05-25): crystal stability discovery GNN. Scoped out.
- **Differentiable atomistic simulation** (2026-05-25): JCTC 2025 = Si/SiO₂ elastic constants, phonons. Trend added; tool scoped out.

**Action:** Scope-out into the consolidated "Surveyed and excluded — materials-domain" subsection. Do NOT add as a matrix row. (Domain gate is hard.)

---

## 7. google.com/search wrapper links

**Cue:** Cited URL is a google.com/search?q=... wrapper instead of a primary source.

**Detection:** Look at the URL host. `google.com/search`, `scholar.google.com/scholar?q=...`, `duckduckgo.com/?q=...` — all wrappers.

**Past hits:**
- **Insilico Chemistry42** (2026-05-27): three links were google.com/search wrappers. Replaced with verified DOIs.

**Action:** Reject the wrapper. Resolve to the primary source (DOI, arXiv abs, repo, official product page). If you can't find the primary source, treat as `LINK MISSING` and apply pattern #4 if the block claim is load-bearing.

---

## 8. Rare-event sampling mislabel

**Cue:** Block labels `BOTTLENECK: rare-event sampling` for a tool that does conformer search / static minimization / structural prep.

**Detection:** Read the cited paper. Rare-event sampling = dynamic barrier-crossing (BioEmu emulates equilibrium ensembles; enhanced sampling stays in MD with biasing). Conformer search = finds static minima (BCS via AIMNet2).

**Past hits:**
- **NVIDIA ALCHEMI-BCS** (2026-05-25): block said "rare-event sampling." Actual: conformer search / structural prep at 10–100ms per conformer.

**Action:** Correct the bottleneck label in the row. Note the swap in Dev_Log.

---

## 9. Replace-the-sim vs engine-layer confusion

**Cue:** Block labels `CAMP: replace-the-simulation` for a tool that runs real MD with ML-derived forces.

**Detection:** Does the tool emit a trajectory? If yes, it's engine-layer (ML-FF that integrates forward), not replace-the-sim. Replace-the-sim emits structures / ensembles / ΔG without integration.

**Past hits:**
- **Google DeepMind GEMS** (2026-05-25): block labeled "replace-the-simulation." Actual: runs MD; ML provides forces. Engine-layer. Direct rival to AI2BMD.

**Action:** Correct CAMP label. Update positioning text (rivals AI2BMD, not BioEmu / NeuralPLexer / Aqemia).

---

## Process discipline

- Link-resolution-first is non-negotiable. Patterns 4 and 7 are unreachable if you read the body before resolving the URLs.
- The block's own `UNCERTAINTIES` and `DISCONFIRMING-EVIDENCE` sections are gold — they often flag the exact field the block is weakest on. Read them before the load-bearing claims.
- Hardened/provenance-tagged blocks reduce field-level confabulation but cannot vouch that the source exists. The format is a downstream check, not a substitute for link resolution.
- Default-NO. ROW only earns its place against the three criteria in `templates/decision-matrix.md`.
