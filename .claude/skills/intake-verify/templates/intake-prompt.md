# Hardened intake prompt template (give this to Gemini)

This is the prompt format that minimizes field-level confabulation. Use it when asking Gemini to characterize a new tool/org for the Market Landscape report.

**Critical caveat:** this format does NOT prevent fabricated sources (STAR-MD). Always link-resolve before trusting any output of this prompt.

---

## The prompt

```
You are characterizing a tool/org for a competitor matrix in a market landscape report on AI-augmented molecular dynamics.

For the following candidate, output a structured block with the fields below. Tag every claim with one of:
  [READ-directly] — you have the primary source in your context and quoted it
  [INFERRED] — you reasoned from a related source but didn't read the specific claim
  [UNCERTAIN] — you're guessing or extrapolating

Required fields:
  TOOL: [name]
  ORG: [primary affiliated org — single org or short list, no halo]
  DOES-IT-RUN-MD: [yes / no / partial — explain]
  CAMP: [replace-the-simulation / engine-layer / prep-step / orchestration / infra]
  BOTTLENECK: [exactly which problem it addresses — e.g., binding affinity, conformer search, setup brittleness, rare-event sampling, runtime crash recovery]
  DOMAIN: [biomolecular / materials / mixed]
  MECHANISM: [one paragraph; cite the source]
  VS-PRIME: [orthogonal / overlapping / near-miss / direct-rival — and why]
  LIMIT: [physical or methodological constraint]

Required sub-sections:
  DISCONFIRMING-EVIDENCE: what would refute the load-bearing claim above
  UNCERTAINTIES: list every field you tagged [INFERRED] or [UNCERTAIN]
  LINKS: primary sources only. NO google.com/search wrappers. Each link is either a DOI, arXiv abs page, GitHub repo, or official product/docs page. Tag each link with [READ-directly] if you actually retrieved its content, [INFERRED] if you only know about it.

Candidate: [TOOL NAME / ORG NAME / PAPER TITLE]
```

---

## What this format prevents (and what it doesn't)

**Prevents (largely):**
- Field-level confabulation (CAMP/BOTTLENECK/DOMAIN swaps)
- Fabricated recovery claims (the DISCONFIRMING-EVIDENCE section forces self-criticism)
- Org-halo aggregation (single org or short list discipline)
- Wrapper links (explicit ban)

**Does NOT prevent:**
- **Fabricated sources** — Gemini can stamp a non-existent arXiv ID as READ-directly. STAR-MD passed this format on 2026-05-28. The link-resolves-first rule is the only defense.
- **Marketing self-description carried as mechanism** — homepage strings get treated as fact.
- **Subtle paper role-swaps** — the cited DOI exists, but its content doesn't match the description (Aqemia JCIM 0c00526 was FreeSolv, not biomolecular).

## After you receive the block

Run the `intake-verify` skill procedure (Steps 0–6). The block is INPUT to verification, not OUTPUT of a decision.
