---
tags: [project-prime, graphify, knowledge-graph, reference-corpus, handoff, future-work]
type: next-session-prompt
status: candidate-decision-gated
created: 2026-06-26
---

# Handoff — graphify: the open questions to evaluate before any spike

🟡 **Decision-gated, to be called when ready.** The graphify assessment is complete ([[Research_graphify]] + memory [[graphify-assessment]]): **do not adopt it as a dependency.** What's left is a small set of *evaluation* questions to settle **before** running any spike — and they only become live when one of the next-step threads below is actually picked up. This file banks those questions so a fresh session can pick them up cleanly without re-deriving the assessment.

## Why this is parked (one paragraph)

graphify maps a folder into a queryable knowledge graph (two layers: a **deterministic structural** pass — tree-sitter AST + `[[wikilink]]`/heading parse, no-API, zero edge-invention; and an **LLM semantic** pass — `INFERRED`/`AMBIGUOUS` conceptual edges, the part that fights the vault's curation discipline). It does **not** do our job (no deterministic gating / `check_amber` / HPC dispatch). The connection-discovery use over the design `.md` notes is **moot now** — that's a research-phase activity and the build phase that justified it is over. graphify's ceiling for us is *retrieval/navigation for the human+agent doing the real work* — it never writes or tests a gate, builds a verifier, or makes a scientific judgment. So it's shelved with **two conditional triggers** that would reopen it.

## The three threads it could touch (the user's likely next steps)

1. **Index the reference corpus** (`Amber26.pdf` 1104pp + AMBER mailing-list archives + the upstream 66-skill library) into a queryable graph the OpenClaw agent hits at build/run time. *Cleanest fit* — clear of the deterministic path, pure reference retrieval. The user **likes this idea.**
2. **The 15-candidate gate backlog** ([[Research_AMBER_Failure_Modes]], P1=4/P2=7/P3=4). graphify helps *only* as the reference index for the per-gate manual lookups — and these are **precise-value lookups** (Table 4.1 radii map, exact tleap warning strings), which is the one thing a concept-graph is weakest at. It does **not** touch the actual work (writing+oracle-testing the deterministic check).
3. **The proposer agent** ([[Future_Work_Proposer_Agent]]). graphify is mostly *conceptual prior-art* — its `EXTRACTED` vs `INFERRED/AMBIGUOUS` firewall IS the propose-then-verify / [[Design_Memory_Provenance]] pattern. Its one possible *role* is as the backend for Phase-1a's "curated planner-context file" — but a hand-written context over the KNOWN 5-skill catalog is probably better/more auditable unless that corpus grows large.

## The questions to settle BEFORE any spike (the actual deliverable of this handoff)

**Q1 — the unifying question: how much reference material, and in which retrieval mode?**
- If you need **conceptual navigation** of a *large* corpus ("how do GB solvation, radii sets, and igb relate?") → graphify's graph is the right shape; thread 1 is worth a spike and incidentally serves 2 & 3.
- If you mostly need **precise lookups** from ~5 manual sections whose location you already know (the gate work) → the existing `amber26-pdf-section-map` jump-table + a simple full-text/RAG over the PDF is faster, and graphify is the **wrong tool**. **Honest lean banked: for the gate backlog specifically, steer away from graphify.**

**Q2 — is a knowledge-graph the right index shape, or would a lighter PDF-RAG win?** graphify builds a *concept graph*, not a vector store. Benchmark it against a plain RAG on a handful of real gate-lookup queries (e.g. "igb=5 radii requirement", "tleap cross-gap bond warning string") before committing. Decide on evidence, not on the tool being interesting.

**Q3 — extraction cost & scope.** A one-time LLM semantic pass over 1104 pages has a real (if modest, on `gemini-3-flash-preview`) token cost. If we do index it: structural pass is free; decide whether the semantic pass is worth it for a *reference* corpus (lower-stakes than the vault — INFERRED edges between manual sections are just navigation). Pin a graphify version (v0.x, 143 releases); leave the post-commit auto-rebuild hook OFF.

**Q4 — vault structural-only spike (separate, low-value-now).** A read-only/no-LLM `graphify extract` over the vault yields god-nodes (most-`[[wikilinked]]`), orphan notes, betweenness bridges. It's discipline-safe but **graph hygiene, not research** — and the anti-drift need it would serve is already covered by [[Definition_of_Done]] + the Stop-hook. Low priority; **NEVER let graphify write into vault notes.**

## Decisions already banked (don't re-litigate)

- **Don't adopt graphify as a dependency.** Assessed, shelved, two conditional triggers only.
- **The semantic layer is rejected as a writer/authority** over the vault; the only allowed form is human-gated candidate generation (machine proposes `inferred` → human ratifies into `connections/`), and we are **not** prioritizing that.
- **Reference-corpus indexing (thread 1)** is the strongest real use and the one the user wants — but gate it on Q1/Q2 first.
- **Conditional triggers that reopen the `query_graph` MCP nav layer:** Scenario B HPC lands ([[Gap_Remote_HPC_Backend]]) and project-prime grows past ~50 files; or a deliberate "give the agent a navigable Amber manual" capability decision.

## Prompt to paste (fresh session)

> I want to evaluate indexing our reference corpus (Amber26.pdf + AMBER mailing-list archives + the upstream 66-skill library) for the OpenClaw agent. Read `handoffs/Next_Session_Prompt_Graphify_ReferenceCorpus.md` and `Research_graphify.md` first. Before proposing anything, settle Q1 (conceptual-navigation vs precise-lookup — which do I actually need for [the gate backlog / the proposer-agent planner-context / general manual access]?) and Q2 (would a lighter PDF-RAG beat a graphify concept-graph on real gate-lookup queries — show me a small head-to-head). Don't run any spike until those are answered. graphify is NOT to be adopted as a dependency, and is NEVER to write into vault notes — see the banked decisions in the handoff.

## Cross-links
- [[Research_graphify]] — the full assessment (the *why*).
- [[graphify-assessment]] (memory) — the banked one-liner.
- [[Research_AMBER_Failure_Modes]] / [[Gap_Gate_Coverage]] — thread 2 (the gate backlog).
- [[Future_Work_Proposer_Agent]] — thread 3 (the proposer agent; has its own graphify-intersection section).
- [[Future_Work_Headroom_ContextCompression]] — sibling token/context tool (retrieval vs compression).
- `amber26-pdf-section-map` (memory) — the existing manual jump-table the index would replace/augment.
