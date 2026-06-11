# Dev_Log entry template for an intake decision

Insert at the top of `Dev_Log.md` (reverse-chronological).

## Format

```markdown
## YYYY-MM-DD — [Tool] [decision verb] [emoji]

**Context:** Gemini intake for [Tool] ([format: hardened-with-provenance / verbose-teardown / loose]). [One sentence on what made this intake worth dev-logging — e.g., "third recovery-fabrication this week" or "first matrix entry to benchmark X."]

**Verification:**
- [Per-link verdict: resolves / 404 / paywall / wrapper, with the corrected source if applicable.]
- [Pattern hits from patterns/recurring-errors.md, named explicitly.]
- [Load-bearing field corrections, with the cited source.]

**Decision — [ROW / NO row / scope-out / one-line mention]:**
[Which of the three matrix criteria the decision rests on. For NO row: which criterion failed. For scope-out: which boundary applies.]

**Done:** [What was edited in the report, with frontmatter revision bump if applicable.] [If thesis was hardened: which bullet, what was added.] [If no edit: state explicitly "no report edit, thesis untouched."]

**[New pattern, if any]:** [Description of the new failure mode, banked into patterns/recurring-errors.md OR phase1-report-format memory.]
```

## Real examples from Dev_Log

**ROW** (Espaloma, 2026-05-27):
> Verified mechanism + links against arXiv, the `choderalab/espaloma` repo, and the Chem Sci 2024 paper.
> Verified (load-bearing, kept): DOES-IT-RUN-MD: no — confirmed (two independent sources)...
> Corrected/dropped: ORG: dropped unverified "extensive Relay Therapeutics collaboration"...
> Decision — earns a ROW: "no MD" ≠ scope-out (BCS is also a no-MD prep step and is a row). Espaloma fills the empty setup/force-field-brittleness cell via a distinct mechanism...
> Done: matrix row after NVIDIA BCS (prep-tier); "force-field setup brittleness" problem bullet; prep-tier sentence in "Where Project Prime fits"...

**NO row + hardening** (Exscientia, 2026-05-27):
> The danger: an uncited "Actionable Engineering Takeaways" paragraph claimed Exscientia's orchestrator "catches the error, reduces the timestep, increments the Langevin seed, and re-queues the crashed λ-window" — i.e. Prime's exact niche.
> Verification: Claim unsubstantiated. No evidence in Exscientia's papers or BioSimSpace docs/changelog/GitHub issues...
> Decision — NO row (default-NO discipline holds on all three counts)...
> Done: banked point (3) as a one-sentence hardening of the "open gap — autonomy" bullet...

**Fabrication** (STAR-MD, 2026-05-28):
> Verification — does not exist in any findable form:
> - arXiv 2602.02128 → HTTP 404 (a real /abs/ page resolves even for obscure papers; 404 = ID doesn't exist).
> - Exact title → zero hits...
> Decision — NO row, NO report edit. Hallucinated/unverifiable source...
> New failure mode (important): a fully hallucinated paper passed the clean hardened format...
> Lesson: resolve the link FIRST.

## Length

Match the entry length to the decision weight. Routine ROW: ~10–15 lines. Routine NO row: ~6–10 lines. Fabrication or thesis-touching decision: write the full pattern + lesson at length so the next iteration of the report process learns from it.
