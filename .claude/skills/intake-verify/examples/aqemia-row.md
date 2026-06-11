# Example: ROW with field corrections (Aqemia, 2026-05-27)

Verbose Gemini intake → clean ROW after correcting a paper role-swap.

## What came in (summarized)

Block claimed: Aqemia runs Molecular Density Functional Theory (MDFT) for binding affinity prediction. Cited JCIM 2020 (`0c00526`) as the biomolecular demo. Speculative `VS-PRIME: Prime generates Aqemia's relaxed input conformation`.

## What verification found

- **DOES-IT-RUN-MD: no** — confirmed. MDFT = classical DFT-of-liquids (HNC closure on the molecular Ornstein–Zernike equation), 3D-grid functional minimization. No trajectory.
- **Paper role-swap caught.** JCIM 2020 `0c00526` is actually *FreeSolv hydration free energies via MDFT* (small-molecule physics). The **biomolecular** demo the block was describing is arXiv:2109.03565 (*COVID-19 drug repositioning via absolute binding free energy*, 1,400 FDA drugs vs SARS-CoV-2 3ClPro). Sources block re-labeled each correctly.
- **Marketing-only homepage**: aqemia.com generic ("generative AI and deep physics") — kept as org link, not as mechanism evidence.
- **Dropped speculative VS-PRIME claim.** Block's own UNCERTAINTIES admitted unclear whether Aqemia even does MD relaxation. Replaced with "static-conformation blindness is Prime's dynamic regime; complementary, not rival."
- **Dropped generative-loop architecture** (RL/GFlowNets black box) — off-lens for the matrix.

## Decision

**ROW — earned.** Three criteria:
1. Genuinely new player.
2. Distinct mechanism — only "replace-the-sim" approach aimed at binding affinity. (FEP+ computes ΔG via MD; BioEmu/NeuralPLexer don't compute ΔG at all.)
3. Fills an empty cell.

Bonus: reinforces thesis — third "remove the simulation" play that does zero runtime-failure recovery.

## What got written

- Matrix row after NeuralPLexer2 (replace-the-sim cluster).
- Problem-centric "binding affinity without the trajectory" bullet.
- Added to "remove the simulation" positioning line (structure / ensemble / binding ΔG).
- Sources sub-block, 3 links verified 2026-05-27.
- Frontmatter `revision: 4`.
- Thesis intact.

## Takeaways for the skill

- **Role-swap caught only by reading the cited paper's actual title.** The DOI resolved, the page loaded, but the content didn't match the block's description. Pattern #3 in the catalog.
- **Speculative VS-PRIME fields are routine and should usually be dropped.** Replace with a defensible orthogonality statement.
- **"No MD" ≠ scope-out.** It's the CAMP, not a disqualifier.
