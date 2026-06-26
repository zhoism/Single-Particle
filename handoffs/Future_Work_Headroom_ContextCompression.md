---
tags: [project-prime, openclaw, future-work, context-compression, token-cost, observability]
type: future-work
status: candidate-not-started
created: 2026-06-24
---

🟡 **Assessed-and-banked external tool — candidate future work, deliberately not started.** Evaluated 2026-06-24 (adversarial multi-agent read of the actual tree, not the README). Headroom is a **context-compression layer for LLM agents**: it sits between the agent and the model and shrinks tool outputs / logs / file dumps / history before they reach the LLM (claimed 60–95% fewer tokens), with reversible retrieval (CCR). This note records the verdict, the OpenClaw-specific fit, and the **scoping rule** that must hold if we ever wire it in — so it doesn't get re-litigated. Companion to [[memory-system-options]] and [[amber-md-prior-art]] (same "assessed, deferred, don't re-open" discipline).

Repo: `github.com/headroomlabs-ai/headroom` (README/package metadata still say `chopratejas/headroom` — a stale rebrand, not a different project). Apache-2.0, PyPI `headroom-ai`, v0.27.0 Beta. ~163k LOC Python + 68k LOC Rust.

# Future work: route OpenClaw (and optionally Claude Code) tool-output through Headroom for token savings

## What it actually is (verified, not marketing)

Three attach modes: **library** (`compress(messages)`), **proxy** (`headroom proxy`, point the agent's API base-URL at it, zero code change), **agent wrap** (`headroom wrap openclaw|claude|…`). The compression is genuinely content-aware engineering, not a wrapper:
- **SmartCrusher** (JSON) — ~12k lines of Rust; statistical field analysis, lossless table-compaction vs. lossy row-drop. REAL.
- **CodeCompressor** — real tree-sitter AST (Py/JS/TS/Go/Rust/Java), keeps signatures, compresses bodies. REAL.
- **CCR** — lossy-but-**reversible**: stores the original locally (SQLite/Redis, BLAKE3-keyed, TTL), leaves a marker, injects a `headroom_retrieve` tool so the model can pull the dropped detail back. REAL.
- **Kompress-base** (neural HF model) — exists but is **not** the default text path; `TextCrusher` (BM25 extractive, millisecond) is. The "6 algorithms" headline is inflated to ~4–5.
- Benchmark numbers (GSM8K ±0.000, 60–95% table) are **illustrative, not publicly reproducible** — need your own API keys + ~$3–5 + 30–45 min; not run in public CI (CI honestly *says* it skips them).

## Why it is OpenClaw-relevant (the real hook)

- Ships a first-class **OpenClaw integration**: `headroom wrap openclaw` installs it as a **ContextEngine plugin**, and there's a `headroom/providers/openclaw/` slice. Not a hypothetical bolt-on — it knows our framework (see [[openclaw-canonical-paths]]).
- Targets exactly our token offenders: **CPPTRAJ output, `mdout` blocks, PLIP 8-category interaction envelopes, `leap.log`** — verbose, repetitive, structured. The `amber-recover` mdout read and `md-planner` manifest validation skim large structured dumps for a few signals = the canonical "10,144 → 1,260 tokens, same FATAL found" case.

## The hard scoping rule (the reason this is *candidate*, not *planned*)

> **Compress only read-only observational content (logs, search results, post-analysis dumps). NEVER let it touch the deterministic-execution path — `mdin` files, charge blocks, anything gated by `check_amber` or byte-identical-edit guarantees.**

This maps cleanly onto our decoupled-hybrid architecture ([[Design_Determinism_Spectrum]], [[Design_Memory_Provenance]]): compress the **LLM-reasoning layer's inputs**, leave the **Lobster-DAG execution layer** untouched. A lossy compressor on the science path violates physical-realism non-negotiables (CLAUDE.md §6.3). This is the same boundary the [[Future_Work_Proposer_Agent]] note draws — reasoning on a leash, execution frozen.

## Urgency: moderate (we are on a PAID model)

Corrected 2026-06-24: current default is **paid `google/gemini-3-flash-preview`**, not free Cerebras (the old long-form status line had stale drift). So:
- **Input-token savings are now real money.** SmartCrusher/CodeCompressor/CCR reduce the tokens we *send* — provider-agnostic, applies to Gemini. At Gemini-Flash input rates the per-turn $ saved is still small (MD runs locally = $0 compute; agent-turns are cheap), but it's no longer zero. Value scales with **volume** (many turns) and **context-window pressure** on long recovery/planner loops — that's the dominant driver, not the per-turn cent.
- **Gemini caveat — the cache machinery mostly does NOT transfer.** Headroom's `frozen_message_count` / KV-cache-hot-zone invariant (and the position-0 bug-fix verified below) is **Anthropic/OpenAI-centric**. Gemini's caching model is different (implicit/explicit context caching), so CacheAligner's benefit — and the scariest risk I cleared — are largely moot for our setup. The provider-agnostic *input-reduction* is what we'd actually be buying.
- It's a **cost/context optimization, not a capability upgrade**, and it adds a new failure surface (CCR retrieval round-trips; lossy drop of the one line you needed — though their fidelity tests target this).

**Open integration question (check FIRST before any spike):** does Headroom's proxy sit cleanly in front of a **Gemini-backed OpenClaw gateway**? Its provider list is Anthropic/OpenAI/Bedrock-first; there is a `headroom/providers/gemini` slice but the proxy→Gemini-upstream path is **not yet verified end-to-end** for our `--gateway` config. This is the real blocker, not the cache fix.

## The one risk that was REAL and is now CLEARED (2026-06-24 verification)

Headroom's own `REALIGNMENT/` docs admit the flagship "IntelligentContext"/ICM strategy was **silently busting Anthropic's KV prompt cache** by dropping/mutating position-0 (system-prompt hot-zone) messages on every compression — i.e. it could *raise* effective cost while reporting "savings." **Verified FIXED in the current tree** (not just claimed): ICM/message-dropping is deleted; `CacheAligner` is detector-only (never mutates the system prompt); a `frozen_message_count` floor + SHA-256 byte-fidelity tests pin everything below it byte-stable (`crates/headroom-core/tests/live_zone_dispatch.rs::byte_fidelity_outside_compressed_block`, `tests/test_proxy_system_prompt_immutable.py`). This matters most for any agent doing many similar turns (us) — cache stability is the thing we'd care about.

## Remaining cautions before any spike

- **Output shaper OFF** (`HEADROOM_OUTPUT_SHAPER=0`): its "effort routing" downgrades model thinking-effort on turns it judges routine — don't let a third party govern reasoning on a turn that needed it.
- **Subscription auth-fingerprint leak**: their docs flag `X-Headroom-*` / `anthropic-beta` header mutation as a subscription-revocation risk (Phase F not yet live). N/A for our gateway/API-key setup, but **never wrap a Claude *subscription* session**.
- Measure **real provider cache-hit rate** before/after, not Headroom's self-reported number.
- ONNX runtime pulls from third-party `cdn.pyke.io` (escape hatch: `ORT_STRATEGY=system`); ~100 `unwrap()`/mutex-poison panics in Rust hot paths (fine in normal op, fragile on malformed input).

## Trigger to revisit

We are already on a paid model, so the gate is now **volume / context-window pressure**: a recovery or planner loop whose context window is filling, or enough agent-turns/day that input-token $ becomes non-trivial. First spike step: (0) **verify Headroom proxy ⇄ Gemini-backed OpenClaw gateway works at all** — this is the real prerequisite; (1) scoped proxy in front of **post-analysis content only** (PLIP/CPPTRAJ dumps), output-shaper off, deterministic path explicitly excluded; (2) measure tokens-saved on Gemini (not Headroom's self-report), since the Anthropic-centric cache-hit benefit won't apply here.

## See also

- [[openclaw-canonical-paths]] — exec tool, agent-loop envelope, ContextEngine surface
- [[multi-agent-scope]] · [[Future_Work_Proposer_Agent]] — same "reasoning on a leash, execution frozen" boundary
- [[memory-system-options]] · [[amber-md-prior-art]] — sibling assessed-and-deferred external tools
