# Example: Fabrication caught by link resolution (STAR-MD, 2026-05-28)

Hardened/provenance-tagged Gemini block → fully fabricated source. Caught only by link-resolution-first.

## What came in (summarized)

Clean hardened-format block for **"STAR-MD (Spatio-Temporal Autoregressive Rollout for MD)"** — claimed ByteDance + Georgia Tech, SE(3)-equivariant causal diffusion transformer generating microsecond protein trajectories. Cited arXiv:2602.02128, stamped READ-directly. CAMP `replace-the-simulation`, benchmark ATLAS, an honest-looking DISCONFIRMING section.

## What verification found

**Resolve every link FIRST:**

- **arXiv:2602.02128 → HTTP 404.** A real arXiv `/abs/` page resolves even for obscure papers. 404 = ID doesn't exist.
- **Exact title "Spatio-Temporal Autoregressive Rollout for Molecular Dynamics" → zero hits** across Google Scholar / arXiv / generic web.
- **"STAR-MD" as a tool name → nothing in this space.**
- **Capability searches returned only the real analogues** the description was synthesized from: **Timewarp** (Microsoft), **MDGen** (Jing/Jaakkola), **BioEmu** (already a row). The ByteDance-MD-trajectory search returned only BioEmu (Microsoft, not ByteDance).

## Decision

**NO row, NO report edit.** Hallucinated source; per the never-place-unverified rule it cannot enter the report in any form. Hardening would *import* the misconception (no reader will ever see STAR-MD; rebutting it just plants the false architecture).

## The key lesson (banked as pattern #4)

**A fully hallucinated paper passed the clean hardened format.** Provenance tags stop field-level confabulation and fake recovery claims, but cannot vouch that the source *exists*. Gemini was handed a tool name and confabulated a plausible paper:

- Real benchmark (ATLAS).
- Plausible architecture buzzwords (SE(3)-equivariant, causal diffusion).
- An honest-looking DISCONFIRMING section.
- A 404 link stamped READ-directly.

**The lesson:** resolve the link FIRST. Link resolution is the single most reliable existence check, independent of format/provenance. This is why `intake-verify` Step 1 is link sweep before reading the body.

## What did NOT happen

- No matrix row.
- No "rejected" entry (would import the misconception).
- No thesis edit.
- Dev_Log entry logged the failure mode for next time.

## Takeaways for the skill

- **Hardened format ≠ verified.** Treat the format as a downstream check, not a substitute for link resolution.
- **arXiv 404 is definitive.** Real arXiv IDs resolve even for unindexed/obscure papers; 404 means the ID was never assigned.
- **If a hallucinated paper would refute the thesis if real, the absence of evidence is the report-side outcome.** The thesis is unchanged; the Dev_Log carries the audit trail.
