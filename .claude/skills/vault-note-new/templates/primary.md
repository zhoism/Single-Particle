---
tags: [__TAG_1__, __TAG_2__, __TAG_3__]
---

# __NoteTitle__

> **Vault tier: __TIER__** — __anchor (paper / repo / official docs / advisor confirmation / our framing)__. __Verification method__ verified __YYYY-MM-DD__.

**Core Concept:** __One sentence on what this note encodes. Active voice. Domain language.__

## __First substantive section__

__Body. Use Memory Provenance labels inline where rules are stated:__

- *observed from source*: __raw data the agent literally reads__
- *confirmed by user*: __validated fact / deterministically verified rule__ (can drive execution)
- *inferred by model*: __LLM hypothesis__ (must be re-checked before acting)
- *imported from transcript*: __prior conversation state__ (treat as inferred until corroborated)

## __Second substantive section__

__Mechanism / how-it-works / what-this-means-for-our-agent.__

## Cross-links

- [[<existing-note-1>]] — __role__
- [[<existing-note-2>]] — __role__
- [[Dev_Log]] entry __YYYY-MM-DD__ — __role__ (only if this note distills a Dev_Log finding)

## Source

__Citation (paper DOI / arXiv abs / repo URL / official docs link / advisor conversation date).__

__If `🟡 design idea`:__ source is our reasoning — name the design conversation or the chain of vault notes that led here.
__If `⚪ aspirational`:__ explicitly state "no current implementation; recorded as a future direction."

## Tier badge reference

- **✅ Source-cited** — anchored to a paper, repo, official docs, or advisor confirmation. Has a real citation. The deterministic execution layer can act on `confirmed by user` and `observed from source` content here.
- **🟡 Design idea / our framing** — our own synthesis or framing. May be load-bearing for skill design, but is NOT paper-grounded. LLM execution must verify before acting.
- **⚪ Aspirational** — a direction we might pursue but haven't built. Do not let the deterministic layer consume this content.
