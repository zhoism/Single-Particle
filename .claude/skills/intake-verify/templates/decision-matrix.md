# Decision matrix — ROW / NO row / scope-out

## ROW (add to the matrix)

A row earns its place when **all three** hold:

1. **Genuinely new player.** Not a sub-tool of an org already in the matrix. (Exscientia → part of Recursion → LOWE already covers; not a new player.)
2. **Distinct mechanism.** Fills a cell that's structurally different from existing rows. ML-FF that pre-computes classical params (Espaloma) ≠ MLIP that integrates on-the-fly (AI2BMD/GEMS).
3. **Fills an empty cell.** Either a new bottleneck not yet owned, or a new approach to an owned bottleneck.

Bonus: reinforces or threatens the thesis in a load-bearing way. (IsoDDE = first matrix entry to benchmark DL affinity head-to-head vs FEP+ → sharpest "why run MD at all?" case.)

**Examples earned a row:**
- Aqemia, Espaloma, NVIDIA ALCHEMI-BMD/BCS, Google GEMS, Microsoft AI2BMD, Microsoft BioEmu, IsoDDE, PRISM/CADD-Agent, GENIUS.

## NO row (decline cleanly)

Default. Decline when **any** of these hold:

- **Existing row already covers the player.** Exscientia → Recursion/LOWE.
- **Distinguishing claim is unsubstantiated.** Cadence/OpenEye auto-recovery (fabricated); Insilico MD-as-reward (docking-scored, not MD).
- **The single new claim is fabricated** (link 404s, source non-existent). STAR-MD.
- **Tool is in a tier already represented 3+ times with the same mechanism.** Agentic orchestration (LOWE / J&J Mol Agent / Tippy) — adding a 4th LLM-orchestrator over docking adds no signal.
- **No load-bearing claim survives verification.** All fields drop to "not documented" / "marketing only."

**Hardening rule:** if the NO-row tool was close to a near-miss against our niche AND the misconception (autonomy gap, bounded recovery) is one a reader could independently arrive at, write a one-sentence inoculation into the report bullet that names the tool + the corrected reading. (Did this for Exscientia in the autonomy-gap bullet.)

**Anti-rule:** if the claim was fabricated AND the reader would never see the original block, do NOT import the rebuttal into the report. Rebutting an invisible claim imports the misconception. (This is the Exscientia 2026-05-27 first-pass mistake, corrected same day.)

## Scope-out (note the boundary)

Scope-out when the tool is **deliberately excluded** by a known boundary:

- **Materials domain.** MatterSim, MPNICE, GNoME, differentiable atomistic sim. Consolidated into the "Surveyed and excluded — materials-domain" subsection.
- **Adjacent tier explicitly out of scope.** Generative design platforms that are orchestration-not-MD (Insilico). One-line mention in the existing "orchestration, not MD mechanics" bullet — not a full scope-out row.
- **Pure structure-prediction without MD context.** ESMFold, AlphaFold pre-MD. Note in passing if a row already cites the relevant structure-prediction wave; otherwise omit.

**Rule:** scope-outs are not failures — they're deliberate boundary markers that show the survey was thorough. A clean scope-out section (with a one-paragraph rationale) is a stronger signal of rigor than a bloated matrix with off-domain rows.

## Trend (not a row, but a named pattern)

Sometimes the intake reveals a **trend**, not a specific tool worth including. Examples:
- Differentiable atomistic simulation (UCLA/DeepMind/OpenAI, JCTC 2025) — tool scoped out (materials), but the paradigm added as a Trends bullet.
- "Replace the simulation" — promoted to a named Dominant Trend at IsoDDE intake (covers BioEmu, Aqemia, NeuralPLexer2, IsoDDE).

**Rule:** trend additions don't need a matrix row, but they do need a Trends bullet + a cross-reference from at least one matrix row that exemplifies it.

## Decision audit trail

Whatever the decision, the Dev_Log entry must record:
1. The verification verdict per link (resolves / 404 / paywall / wrapper).
2. Pattern hits from `patterns/recurring-errors.md`.
3. The criterion (or criteria) the decision rests on.
4. Whether the thesis was touched (hardened, unchanged, threatened-and-rebutted).
5. Frontmatter `revision:` bump if the report was edited.

Without this trail, the decision can't be reproduced or challenged later.
