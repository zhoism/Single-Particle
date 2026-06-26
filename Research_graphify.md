---
tags: [research, prior-art, claude-code, openclaw, knowledge-graph, tooling, steal-list, vault-meta]
type: research
status: prior-art-assessed
source: github.com/safishamsi/graphify (PyPI `graphifyy` v0.8.49, MIT, YC S26 / Penpax)
date: 2026-06-26
---

# Research note — `graphify` (safishamsi/graphify)

**Status:** 🟡 Prior-art assessed. Repo cloned + read at source level (README, `ARCHITECTURE.md`, `graphify/extract.py`, `graphify/llm.py`, `graphify/analyze.py`, `graphify/serve.py`, `graphify/export.py`, the `claw` skill). **Not** run against our private content — characterization below is from reading the actual extraction code, which is more precise than one run. Mature: 72.6k★, 836 commits, real `security.py` + threat model + CVE-pinned deps, MIT.

> safishamsi. *graphify* — "Type `/graphify` in your AI coding assistant and it maps your entire project — code, docs, PDFs, images, videos — into a knowledge graph you can query instead of grepping." GitHub / PyPI `graphifyy`.

## What it is

A Python CLI + AI-assistant **skill** that turns any folder into a **queryable knowledge graph**. Pipeline: `detect → extract → build_graph → cluster → analyze → report → export`. Outputs `graph.html` (interactive), `GRAPH_REPORT.md` (god nodes / surprising connections / suggested questions), `graph.json`, and — relevant to us — an **Obsidian vault** (one `.md` per node, YAML frontmatter, `[[wikilinks]]`, community tags, `.obsidian/graph.json`). Exposes an **MCP server** (`query_graph`, `get_node`, `get_neighbors`, `shortest_path`, `god_nodes`, `graph_stats`, `list_prs`/`get_pr_impact`/`triage_prs`; resources incl. `graphify://audit` = EXTRACTED/INFERRED/AMBIGUOUS breakdown).

Two facts make it unusually on-target for *this* project:
1. **Native OpenClaw skill** (`graphify claw install`) — one of very few external tools shipping an OpenClaw integration; touches our exact runtime. (Caveat: README says OpenClaw uses **sequential** extraction — parallel-subagent dispatch "still early" — so the build is slower there than on Claude Code; the MCP query path is unaffected.)
2. **It exports / understands Obsidian** — `extract_markdown` already parses `[[wikilinks]]` and `[text](./x.md)` into `references` edges and the heading tree into `contains` edges.

## The load-bearing architectural insight (resolves the vault tension)

graphify has **two separable layers**, and conflating them is the trap:

- **Deterministic structural layer** — `extract.py` header literally reads *"Deterministic structural extraction."* tree-sitter AST for code (36 grammars, **local, no API**) + pure line-parse for markdown structure + `[[wikilink]]`/`contains` edges. Every edge here is tagged `EXTRACTED`. **Zero edge invention; faithfully renders the graph that already exists.** `graphify extract` headless runs this.
- **LLM semantic layer** — `llm.py` (`extract_corpus_parallel`), driven by the `/graphify` skill via subagents. Adds `conceptually_related_to` / `shares_data_with` / `semantically_similar_to` edges + hyperedges, tagged `INFERRED` / `AMBIGUOUS`. **This is the edge-inventing part** that conflicts with the vault discipline.

So "point graphify at the vault" is not one action — it's two, with very different risk.

## Does it do our job? No.

Same shape as [[Research_amber_md_skill]] and [[Future_Work_Headroom_ContextCompression]]: useful adjacent tool, **none** of our substance. No deterministic execution gating ([[OpenClaw_Lobster_DAGs]]), no `check_amber` bounds, no MD physical-realism, no HPC dispatch ([[Gap_Remote_HPC_Backend]] untouched), no recovery ladder. It maps/retrieves over a corpus; it does not run or guard the pipeline. Orthogonal to the 9 skills, not competitive.

## Use-case 1 — OpenClaw runtime (the agent)

**Weak as a code-navigation layer.** Our agent's runtime job is to *drive* the MD pipeline over a **known 5-skill catalog** (md-planner's registry, [[Arch_Taskboard_Manifest]]) — it rarely needs to "understand a large codebase" at run time; that's a dev-time activity, and the repo is small. The `query_graph` mechanism (BFS from seed nodes, ~2000-token budgeted subgraph vs full-file reads) is real and is a sibling of the [[Future_Work_Headroom_ContextCompression]] idea (navigation/retrieval vs content-compression) — but there's little for it to navigate here yet.

**The one genuinely novel runtime angle:** graphify ingests **PDFs + docs** into the queryable graph. The 1104-page `Amber26.pdf` is exactly the kind of corpus we already keep a manual section-map for (see memory `amber26-pdf-section-map`). Indexing it (and the mailing-list/manual material behind [[Research_AMBER_Failure_Modes]]) into a graph the agent can `query_graph` at run time is the strongest OpenClaw-runtime use I can find — and it stays clear of the deterministic path entirely (pure reference retrieval).

## Use-case 2 — current Claude-Code dev setup

### (a) The vault (`Single-Particle`)
**Structural-only render = faithful, free, aligned.** Run `graphify extract` (no LLM) over the vault and the analysis is pure *measurement of the existing graph*: `god_nodes` = most-`[[wikilinked]]` notes; isolated-node detection = **orphan notes** (maps exactly onto the monthly "prune notes that connect to nothing" rhythm); `surprising_connections` via edge-betweenness = real bridge notes ranked, **no invention**. This is 100%-discipline-safe and is the best fit.

**LLM-semantic layer = candidate generator ONLY, never a writer.** Its `INFERRED`/`AMBIGUOUS` conceptual edges are precisely the vault's *"candidate connections go in `connections/` as hypotheses, not into existing notes as assertions."* If ever used, its output is mined by hand → ratified into `connections/` → the rest discarded. **Never let graphify write into vault notes** — auto-edges degrade a hand-curated graph, and "plausible ≠ meaningful" is the whole point.

### (b) project-prime code repo (`Single-Particle-pipeline`)
Local AST map of the 9 wrappers + run spine + shell + SKILL.md/JSON is **free** (no API) and a fine navigation aid — but the repo is small enough (vault's own rule: programmatic traversal earns its keep at ~50+ files) that value is marginal **now**. Re-evaluate if [[Gap_Remote_HPC_Backend]] (Scenario B) lands and the repo grows.

## Steal-list (ideas, not the dependency)

- The **`EXTRACTED / INFERRED / AMBIGUOUS`** edge taxonomy is independent convergent prior-art for our [[Design_Memory_Provenance]] four-label model and the "edges are hypotheses until ratified" stance — worth citing as external validation that the design is sound.
- **`god_nodes` + `surprising_connections` (betweenness) + isolated-node detection** is a clean articulation of what `connections/` and the (currently absent) MAP.md do by hand — a candidate for a tiny home-grown structural analyzer over the vault even if we never adopt graphify.
- **Hyperedges** (3+ nodes in one shared concept) are a structure the vault lacks but arguably wants (e.g. "the 3 layers of the decoupled hybrid agent" is one hyperedge, not 3 pairwise edges).

## Adversarial flags (if ever wired in)

- v0.x, 143 releases, fast-moving → **pin a version**.
- The post-commit **auto-rebuild hook** is noisy/surprising → leave it **off**.
- LLM semantic pass costs tokens on docs (negligible per-turn on `google/gemini-3-flash-preview`, vault is small) → scope any run to **code/markdown structural** only unless deliberately generating candidates.
- Third-party YC startup tool sending content to an LLM API → for the vault, structural/no-LLM keeps content local; the semantic pass would ship note prose to the model.

## Verdict

**Don't adopt as a dependency now.** Neither surface clears the bar: the agent doesn't navigate a big codebase at run time, the code repo is small, and the vault's curation discipline is hostile to auto-edges. **Two scoped, aligned uses worth banking:**
1. **Structural-only candidate-connection spike over the vault** (read-only, no-LLM, free): god-nodes + orphan list + betweenness bridges → hand-ratify any worthy un-encoded edges into `connections/`. Fits the documented maintenance rhythm; lowest risk, highest fit.
2. **Watch for Scenario B** — if remote HPC lands and project-prime grows past ~50 files, revisit the OpenClaw `query_graph` MCP layer (sibling to [[Future_Work_Headroom_ContextCompression]]). Separately, indexing `Amber26.pdf` into a queryable graph is the one novel runtime use that needs no growth trigger.

Sibling to [[Research_amber_md_skill]], [[Future_Work_Headroom_ContextCompression]], and the `memory-system-options` / `llm-wiki-pattern` assessments — **assessed, deferred, don't re-open** the "should we just adopt it" question; the two scoped spikes above are the only live threads.
