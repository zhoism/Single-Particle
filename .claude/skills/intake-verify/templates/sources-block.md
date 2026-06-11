# Sources block template

Every matrix row gets a Sources sub-block in the Report's Sources section.

## Format

```
### [Tool] ([Org])

- **[Title]** — [Venue Year, DOI/arXiv ID] · [link, WebFetch-verified YYYY-MM-DD] — [one-line role: the mechanism evidence / the demo paper / the org page / the schema docs]
- ...

[Caveats, if any — peer-review status, self-reported, architecture undisclosed, OOD-degrading, materials side, etc.]
```

## Rules

1. **Every link is WebFetch-verified.** Date-stamp the verification.
2. **Each link gets a one-line role.** Mechanism source vs demo paper vs org page vs schema docs vs review reference. The reader can tell what each link does for the claim.
3. **Caveats live in the sub-block, not the matrix row.** Self-reported / not-peer-reviewed / architecture-undisclosed / OOD-degrading — note them honestly.
4. **Org-halo trimmed.** If a paper has authors from 3+ orgs and the matrix row names a primary one, the Sources block can acknowledge collaborators in the caveat — but do not list them as the "org" of the row.

## Example (from `Market_Landscape_Report.md`, Espaloma)

```
### Espaloma (Chodera Lab / Open Force Field)

- **Machine-learned molecular mechanics force fields from large-scale quantum chemical data** (espaloma-0.3) — Chem. Sci. 2024, [10.1039/D4SC00690A](https://doi.org/10.1039/D4SC00690A) · verified 2026-05-27 — peer-reviewed mechanism source.
- **End-to-End Differentiable MM Force Field Construction** — arXiv:2010.01196 · verified 2026-05-27 — original method paper.
- **choderalab/espaloma** — [GitHub](https://github.com/choderalab/espaloma) · verified 2026-05-27 — code home.

Caveat: paper claims Relay Therapeutics collaboration; not in author list of D4SC00690A (Asahi Kasei Pharma is the named industry partner). Org carried as Chodera Lab / OpenFF.
```

## Failure-mode citations

For NO-row decisions where the report was hardened, the inoculation bullet's citation goes in a "Defensibility" sub-block (or equivalent), not the per-tool Sources. Example (Exscientia hardening, in the autonomy-gap bullet):

> "...e.g., Exscientia's BioSimSpace orchestration layer, where the autonomous-recovery claim could not be substantiated against the project's docs or issue tracker (verified 2026-05-27)."

The citation is the verification act, not a primary source — the absence of evidence is itself the citation.
