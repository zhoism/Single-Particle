# Matrix row template

The Market Landscape Report matrix uses this row format:

```
| [Org] | [Tool] | [Exact MD Scenario] | [Link] |
```

## Field rules

- **Org**: single org or trimmed short list. No halo. If a paper has authors from 3+ affiliations, name the primary one (first/last author institution) and acknowledge collaborators in the Sources block, NOT in the row.
- **Tool**: the specific named product/package/method. Not the umbrella platform. "AI2BMD" not "Microsoft Research." "ALCHEMI-BCS" not "NVIDIA ALCHEMI suite."
- **Exact MD Scenario**: one sentence with the **mechanism**, the **bottleneck**, and the **stage of MD** it touches. Active-voice verbs. Example: "ML-force-field engine that swaps the GAFF/antechamber rule-based atom-typing with a GNN to remove setup brittleness." Avoid marketing buzzwords ("AI-driven", "deep physics").
- **Link**: a single primary source — official product page, peer-reviewed paper, or GitHub repo. WebFetch-verified. No google.com wrappers.

## Examples (from `Market_Landscape_Report.md`)

```
| Microsoft Research + GHDDI | AI2BMD | ML-FF (ViSNet GNN) ab initio-accuracy biomolecular MD; binding ΔG, protein-folding ΔG/Tm, pKa, NMR ³J. Engine-layer. | [Nature 2024](https://doi.org/10.1038/s41586-024-08127-z) |

| Chodera Lab (MSKCC) / Open Force Field | Espaloma | GNN replaces rule-based GAFF/antechamber atom-typing to remove setup brittleness; emits classical MM params, not forces at runtime. Prep-step. | [Chem. Sci. 2024](https://doi.org/10.1039/D4SC00690A) |

| Isomorphic Labs (Alphabet/DeepMind) | IsoDDE | AlphaFold-3-lineage DL engine — predicts structure / affinity / pockets directly from sequence, no trajectory. Benchmarks DL affinity head-to-head vs FEP+ (Pearson 0.85 vs 0.78). Replace-the-sim. | [Tech report Feb 2026](https://www.isomorphiclabs.com/...) |
```

## Where to insert

Group by CAMP:
1. **Replace-the-simulation**: NeuralPLexer2, BioEmu, Aqemia, IsoDDE
2. **Engine-layer**: AI2BMD, GEMS, ALCHEMI-BMD
3. **Prep-step**: ALCHEMI-BCS, Espaloma
4. **Orchestration / agentic**: LOWE, J&J Mol Agent, Tippy, Multisim, Orion, PRISM/CADD-Agent, GENIUS
5. **Deterministic incumbent**: FEP+

Insert into the matching cluster; do not just append at the bottom. Re-cluster only if the new row genuinely creates a new CAMP.

## Frontmatter bump

After every row add (or row removal), bump `revision:` in the report frontmatter by 1. Note the change in the Dev_Log entry.
