---
tags: [openclaw, aspirational, self-evolution, design-idea]
---
# OpenClaw Mechanics: Self-Evolution and RL (aspirational)

> **Vault tier: ⚪ Aspirational — design inspiration only, not load-bearing.** "MetaClaw" and "OpenClaw-RL" as named mechanisms are NOT in arXiv:2603.25522 (NotebookLM-verified 2026-05-19); the only paper-adjacent evidence is a `skill-creator` reference in the OpenClaw GitHub commit history. May be elaborated in OpenClaw docs or OpenBrain-style satellite repos (cf. [[Design_Memory_Provenance]]). **Not chasing primary sources for Project Prime — out of scope for the demo + report.**

## The core idea (kept as inspiration)

- A **skill-creator** skill that writes new skills which become active instantly — the agent adapts to novel project requirements on the fly.
- An asynchronous RL loop using conversation state changes (successful submission, user correction) as training signal — fine-tune future behavior from accumulated runs.

## Deterministic analog (worth a sentence in the report)

Schrödinger's *Active Learning FEP+* ([[Arch_Schrodinger_FEP]]) achieves the "improves through usage" outcome via a fixed ML loop trained on physics data — same goal, opposite mechanism. Mention in the competitive section; out of day-1 scope.

**Source:** Inspirational, not load-bearing. General "self-evolving agents" concept is broadly attested in agent literature; specific OpenClaw branding (MetaClaw, OpenClaw-RL) is not verified against any primary source.
