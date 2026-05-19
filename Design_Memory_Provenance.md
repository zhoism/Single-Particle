---
tags: [memory, state-management, reasoning, provenance-labels, openbrain]
---
# Design: Memory Provenance & Contextual Reasoning

> **Vault tier: ✅ Source-cited** — anchored to the **OpenBrain** memory-recipes project (the actual home of this mechanism), *not* the OpenClaw substrate paper. NotebookLM-verified 2026-05-19.

**Core Concept:** Tag every memory item with where it came from, so the deterministic execution layer can refuse to act on un-verified beliefs. Stops LLM hypotheses from being mistaken for facts.

**The four provenance labels (OpenBrain, exact set):**

| Label | Meaning | Example | Can drive execution? |
|---|---|---|---|
| `observed from source` | Raw data the agent literally read from a log / file / tool output | "`mdout` says crashed at step 500" | ✅ Yes |
| `confirmed by user` | A fact the user validated, or a rule deterministically verified | "SHAKE requires `dt ≤ 2fs`" | ✅ Yes |
| `inferred by model` | An LLM hypothesis | "the crash might be from a missing GAFF type" | ❌ No — must be re-checked before acting |
| `imported from transcript` | Context lifted in from prior conversation / session state | "earlier we agreed the test ligand is benzamidine" | ⚠️ Treat as inferred until corroborated |

*Source quote (OpenBrain via MindStudio):* "OpenBrain's memory provenance system ships with exactly four labels: observed from source, inferred by model, confirmed by user, imported from transcript." And on inferred: "you might want to re-check it before acting on it... an agent that confidently recommends a rollback based on a half-remembered inference is worse than no recommendation at all."

**Operating discipline for Project Prime:**
- The deterministic execution layer (`Lobster` engine, [[OpenClaw_Lobster_DAGs]]) acts only on `observed` + `confirmed`.
- `inferred` is quarantined — it can guide reasoning but cannot trigger side-effecting actions until promoted (by user confirmation or deterministic verification).
- `imported from transcript` is treated as `inferred` by default until corroborated by an `observed` source — transcripts can carry stale assumptions forward.

**Why this matters for the recovery skill:** [[Skill_Bounded_Recovery_AMBER]] is exactly the kind of side-effecting action that must be gated on `observed` evidence (the crash signature parsed from `mdout`) plus `confirmed` rules (the bounded-mutation limits) — never on a raw `inferred` LLM diagnosis.

## History note (2026-05-19)

Earlier vault drafts called this **"Memory Providence"** with **three** labels (Observed / Confirmed / Inferred) and attributed it to arXiv:2603.25522. Three corrections from NotebookLM verification:
1. The term is **Provenance**, not Providence (the original was a propagated typo; one MindStudio blog also typo'd it as "providence-rich recall").
2. There are **four** labels, not three — we were missing `imported from transcript`.
3. The real source is **OpenBrain** (open-source memory-recipes for OpenClaw), not the substrate paper.

**Source:** OpenBrain memory-recipes (via MindStudio article); NotebookLM-verified 2026-05-19. Companion to [[Research_Phase1_Survey]] and [[Research_Source_Manifest]].
