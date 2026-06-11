---
name: intake-verify
description: Use when the user pastes a Gemini-generated intake block, teardown, or candidate tool/org for the Market Landscape report and wants a verify-and-decide pass. Triggers on phrases like "evaluate X", "intake for Y", "should this go in the matrix", or any block containing CAMP/BOTTLENECK/DOMAIN/DOES-IT-RUN-MD tags. Output is a ROW / NO-row / scope-out decision with sources verified.
---

# intake-verify — Gemini intake → matrix decision

The single most-repeated task in the vault (≥15 intake passes between 2026-05-25 and 2026-05-28). Each pass costs ~30min and the failure mode is silent: a fabricated claim, an unresolved link, or an org-halo aggregation that slips through poisons the report.

## When to invoke

- User pastes a block with fields like `DOES-IT-RUN-MD`, `CAMP`, `BOTTLENECK`, `DOMAIN`, `VS-PRIME`, `LIMIT`, `LINKS`.
- User says "evaluate X for the matrix" / "intake for Y" / "should we add Z to the report".
- A new tool / org / paper is being weighed against `Market_Landscape_Report.md`.

## Hard rules (do not skip)

1. **Resolve every link FIRST, before reading the rest of the block.** This is the single most reliable existence check. STAR-MD (2026-05-28) was a fully hallucinated paper that passed the hardened-format provenance discipline because the link was stamped READ-directly without being resolved. arXiv IDs that don't exist return HTTP 404; real ones resolve even when obscure.
2. **Default-NO discipline.** A row earns its place; absence is the default. New row only if (a) genuinely new player, (b) distinct mechanism, (c) fills an empty cell. Scope-out for materials / non-MD / off-domain.
3. **Never trust an uncited claim that matches our niche.** A block claiming the tool does "autonomous physics-mutation recovery" or "dt reduction on crash" is the highest-priority fabrication check — it's our exact thesis-threatening pattern (Exscientia, Cadence/OpenEye).
4. **Treat google.com/search wrapper links as forbidden.** Resolve to the primary source (DOI, arXiv abs page, repo) or reject.

## Procedure

**Step 0 — Read context:**
- `patterns/recurring-errors.md` — the 9+ recurring intake-error patterns with detection cues.
- `templates/decision-matrix.md` — ROW / NO-row / scope-out criteria.
- Current `Market_Landscape_Report.md` matrix — to avoid re-adding existing rows.

**Step 1 — Link resolution sweep.** WebFetch every URL in the block. Record verdict per link: `resolves / 404 / paywall / wrapper`. If the load-bearing source URL 404s → STOP, default-NO, write a fabrication Dev_Log entry (template in `examples/star-md-fabrication.md`).

**Step 2 — Pattern scan.** For each of the patterns in `patterns/recurring-errors.md`, flag any match in the block. Common hits: org-halo aggregation, fabricated recovery, role-swap, fabricated source, MD-washing, materials mislabel.

**Step 3 — Verify load-bearing fields.** For each of `DOES-IT-RUN-MD`, `CAMP`, `BOTTLENECK`, `DOMAIN`: confirm against the actual paper / repo / docs. The block's own `DISCONFIRMING-EVIDENCE` and `UNCERTAINTIES` sections often hand you the answer — read them first.

**Step 4 — Decision.** Apply `templates/decision-matrix.md`:
- **ROW** → write matrix row + Sources sub-block + bump frontmatter `revision:` + Dev_Log entry.
- **NO row** → Dev_Log entry explaining the call; if it could be misread as a near-miss to our niche, harden the relevant report bullet with a one-sentence inoculation.
- **Scope-out** → consolidate into the "Surveyed and excluded" section if materials-domain; one-line mention in an existing bullet if redundant (orchestration-not-MD pattern).

**Step 5 — Write the artifacts.** Use:
- `templates/matrix-row.md` — exact row format.
- `templates/sources-block.md` — Sources sub-block format with verified-on date.
- `templates/devlog-decision.md` — short Dev_Log entry for the decision.

**Step 6 — Update memory if a new pattern emerged.** Add to `phase1-report-format` memory only if the failure mode is genuinely new (not already in `patterns/recurring-errors.md`).

## Output format

Single response with three clearly-labeled sections:
1. **Verification result** — per-link verdict, pattern hits, field corrections.
2. **Decision** — ROW / NO-row / scope-out, with the criteria each call rests on.
3. **Artifacts** — exact text to insert into `Market_Landscape_Report.md` + Dev_Log entry text, ready to paste.

## Anti-patterns

- Do NOT write the decision before resolving links. The link-first rule exists because Gemini will confabulate plausible architecture around a fake source.
- Do NOT carry a tool's marketing self-description as evidence. "Generative AI and deep physics" on a homepage is not a mechanism claim.
- Do NOT add a row just because the block looks well-formatted. Hardened/provenance-tagged blocks can still wrap fabricated sources (STAR-MD).
- Do NOT rebut a fabricated claim in the report body. If the claim was never published, the reader never sees it — rebutting it just imports the misconception (see Exscientia 2026-05-27 first-pass mistake, corrected same day).
- Do NOT trust org attribution on collaborative-author papers. Org-halo aggregation (Cadence/OpenEye claiming Stanford/Chodera work) is the #1 silent failure.

## Cross-references

- Memory `phase1_report_format` — recurring intake patterns, hardened intake template, the 9 failure modes.
- Memory `phase1_report_status` — what's already in the canonical reports; what was deleted.
- Vault `Market_Landscape_Report.md` — current matrix; the source of truth.
- Vault `Actionable_Recommendations.md` — positioning logic for ROW vs scope-out calls.
- Dev_Log entries 2026-05-25 → 2026-05-28 — worked examples of every decision type.
