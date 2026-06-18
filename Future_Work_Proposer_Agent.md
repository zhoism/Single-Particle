---
tags: [project-prime, openclaw, future-work, architecture, agentic-reasoning]
type: future-work
status: candidate-not-started
created: 2026-06-12
---

🟡 **Design idea / our framing — candidate future work, deliberately not started.** Captured 2026-06-12 during the report-walkthrough session (Kevin's proposal). This is an opt-in expansion path, not a planned build. It does **not** reopen [[multi-agent-scope]] (that banked decision rejected a *swarm*; this is a single supervisory agent) — but starting it would be a deliberate decision, gated by the limit named below.

# Future work: an outer proposer-agent around the frozen deterministic core

## The idea

Wrap the existing nine-skill deterministic pipeline with **one** standing supervisory agent that can **propose** new things, **make decisions**, **supply inputs**, and **test its own ideas** — but can never *insert* anything into execution directly. Every proposal it makes is barred by the deterministic wrappers (`check_amber` bounds, the validation gates, the bounded-recovery ladder) before it can touch the science. A **propose-then-verify** loop, generalized.

This is not a new pattern for the project — it is the generalization of two things already built:
- the **planner** ([[md-planner]] / [[Arch_Taskboard_Manifest]]) — proposes a workflow plan; gates G0–G6 validate before any skill runs;
- the **recovery proposer** ([[Workflow_Error_Recovery_Loop]] / [[Skill_Bounded_Recovery_AMBER]]) — proposes crash fixes; `check_amber` + the bounded ladder bar anything out of bounds.

The extension: turn that one-shot pattern into a **standing exploratory loop** — propose variants → run them through the frozen pipeline → look at results → propose again.

## Why it is thesis-aligned (not the rejected swarm)

A single supervisory agent in a verify loop ≠ the El Agente Q topology (many named specialist agents with execution authority) rejected in [[multi-agent-scope]]. The reasoning here stays on the **boundary** side of the coverage line ([[Design_Determinism_Spectrum]]) — proposing and driving, never executing science unverified. It is "reasoning on a leash," extended one notch.

## The hard limit (the reason this is *candidate*, not *planned*)

> **In a propose-then-verify architecture, the agent can safely explore exactly as far as the verifier can check — and no further. Capability is gated by *verification*, not by *reasoning*. The bottleneck is the oracle, not the brain.**

The safety argument ("the wrappers bar it") is only as strong as what the wrappers can *catch*. The deterministic layer covers the **mechanical / bounds layer completely** and the **scientific-judgment layer not at all**:
- out-of-bounds proposal (`dt = 5 fs`) → caught, safe;
- **in-bounds-but-scientifically-wrong** proposal (a legal parameter combo that is physically inappropriate; the wrong pocket; a valid-but-incorrect protonation state) → **passes every gate**, returns a confident green *wrong* answer. No gate for "is this good science" exists cheaply.

Second-order limit: to let it "test its ideas," you need to **score** them. For mechanical questions there is a real verifier (did it run? in bounds? crash?). For scientific quality there is **no ground-truth oracle** — only proxies (ΔG more negative, lower variance, faster convergence). An agent optimizing a proxy will **reward-hack** it (settings that make ΔG look great and mean nothing).

## What it *can* safely expand (where a real verifier or defensible proxy exists)

- **Parameter exploration / DOE** — propose `cut` / equilibration-length / ion-concentration variants; pipeline is the verifier; agent only drives.
- **Convergence monitoring** — "ΔG still drifting → propose extending production." Proxy = variance/drift.
- **Adaptive analysis selection** — choose which cpptraj analyses to run from what it sees.
- **Generalized recovery / triage** — diagnose *why* a gate failed, propose a targeted fix (smarter [[Skill_Bounded_Recovery_AMBER]]).

## What it *fundamentally cannot* do (no matter how capable the model)

- Verify scientific **appropriateness** or **correctness** of an in-bounds proposal.
- Judge **convergence / sampling adequacy** as truth (only as a proxy).
- Replace **human scientific judgment** on whether the question is well-posed.

## The reframe for the report (and for any future build)

"How much can we expand?" has a precise answer: **as much as we can expand the verifier.** Growing safe capability is therefore *not* "add a smarter agent" — it is "**build a verifier (or defensible proxy) for the thing you want it to reason about.**" Where you can build that check, the agent can roam; where you can't (is the science *correct*), it cannot, because nothing can bar a wrong-but-legal proposal. This is a feature: capability grows through auditable, reproducible checks rather than trust in a black box.

## If/when this is picked up

- Decide it deliberately — it is opt-in and intersects [[multi-agent-scope]] (confirm: single supervisory agent, not a swarm).
- Scope the **first verifier to extend** before scoping the agent (oracle-first, per the reframe above).
- Every proposal + decision must be logged as an auditable artifact (the planner manifest is the precedent) to preserve the frozen-core reproducibility guarantee.
- Keep all agent output `inferred` ([[Design_Memory_Provenance]]) until a deterministic check clears it.

## Related smaller idea — a curated planner-context file (captured 2026-06-17)

A lighter, orthogonal addition surfaced during the report walkthrough: give [[md-planner]] a **curated context `.md`** beyond the per-skill `SKILL.md` + registry — worked goal→manifest examples, domain notes (e.g. equilibration length vs system size), common-pitfall hints. It would raise the *quality* of the LLM's drafted manifests (fewer rejected plans, smarter defaults). **Key caveat (thesis-aligned):** context improves the *proposal* only, never the *trust* — the G0–G6 validator gates stay exactly as strict regardless of how good the context is. Context and validation are orthogonal: context makes the agent propose better, gates make the system safe regardless. Low-risk to build precisely because it cannot weaken the guarantee. Not started; noted as a clean, opt-in addition.

## Related smaller idea — a natural-language gloss on the recovery diagnostic (captured 2026-06-17)

Concrete, narrow extension to [[Skill_Bounded_Recovery_AMBER]] / `amber-recover`: emit **both** outputs from the crash detector — (1) the existing **raw deterministic dict** (`crashed`, `classification`, `signatures`, `crash_nstep`, `vlimit_clamps`, `final_block_finite`, `rc`) exactly as-is, **plus** (2) an LLM-written **natural-language gloss** alongside it ("crashed at step ~41k on a SHAKE failure → looks like a too-large timestep; bounded Tier-2 stabilization applies; if it recurs, check the ligand parameterization upstream").

**Firewall constraints (must hold or it breaks the thesis):**
- The gloss is **additive, never a replacement** — the raw dict stays the authoritative, byte-stable, oracle-tested artifact.
- The gloss **must not drive routing** — Tier-1/Tier-2/HALT keys off the deterministic `classification`/`signatures` only; the prose is advisory-to-human, downstream of the decision.
- The gloss is `inferred` ([[Design_Memory_Provenance]]) and clearly labelled non-reproducible; the oracle test covers the dict, **never** the prose (you can't oracle-test a paragraph).
- It stays on the **propose-to-a-human** side of the firewall — same discipline as the proposer idea above.

Small to build (one LLM call over the existing dict, output into a separate envelope field). Not started.

## Cross-links

- [[Design_Determinism_Spectrum]] — the spine; this stays on the boundary pole.
- [[multi-agent-scope]] (memory) — the banked swarm rejection this does *not* reopen.
- [[md-planner]] / [[Arch_Taskboard_Manifest]], [[Workflow_Error_Recovery_Loop]] / [[Skill_Bounded_Recovery_AMBER]] — the one-shot propose-then-verify patterns this generalizes.
- [[Gap_Remote_HPC_Backend]] — sibling open direction.
