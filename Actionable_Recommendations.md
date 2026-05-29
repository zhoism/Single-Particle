---
tags: [report, market-research, actionable, deliverable]
type: report
status: for-advisor-review
date: 2026-05-28
companions: [Market_Landscape_Summary.md, Market_Landscape_Report.md]
---

# Actionable Recommendations: Build Strategy and Competitive Positioning

**Author:** Kevin Zhou
**Date:** 2026-05-28

## Executive summary

The market survey supports a clear strategy: build selectively, integrate broadly, and differentiate on a single capability. Classical MD remains the default engine; external engines and prediction models are integrated behind swappable interfaces; proven agent-architecture patterns are adopted from existing tools; and in-house development concentrates on the one capability absent from the field — autonomous, mathematically-bounded recovery from mid-run simulation failures. The approach is positioned on two points: it escalates rather than improvises, and it keeps physics-based MD — which prediction models cannot fully replace — runnable without supervision.

---

## 1. Recommendation triage: build, integrate, or adopt

The survey indicates that most of the required capability already exists and should be integrated or adopted rather than rebuilt; only a small core warrants in-house development.

| Bucket | Source / capability | Recommended action | Rationale |
|---|---|---|---|
| **Build** | Tiered recovery skill (checkpoint-restore → bounded mutation) | Build in-house — primary differentiator | The sole MD bottleneck unaddressed by the field; the project's central contribution. |
| **Build** | Ligand-prep skill (antechamber/tleap automation) | Build in-house | Setup brittleness is a primary user pain point; the skill must generalize to any ligand rather than a fixed test case. |
| **Build** | Planning/manifest layer with validation gates | Build in-house | Defines stage/input/output/validation specifications before execution — the guardrail layer the LLM is prevented from corrupting. |
| **Integrate** | ML force-field engines (Microsoft AI2BMD, DeepMind GEMS) | Integrate behind the swappable `ENGINE` interface; optional | Near-quantum accuracy, but classical force fields (ff14SB/GAFF) remain the default, as ML potentials are not yet production-standard for explicit-solvent protein–ligand MD. AI2BMD uses AmberTools preparation already automated here. |
| **Integrate** | NVIDIA ALCHEMI (Batched MD + Conformer Search) | Integrate as throughput / preparation microservices | Batched dynamics and a fast conformer pre-filter; the container/microservice packaging aligns with the system's architecture. |
| **Integrate** | Espaloma (Chodera/OpenFF) | Integrate as an optional ML parameterizer | An alternative to rule-based atom-typing, and a documented source of the out-of-distribution failures the recovery layer is designed to catch. |
| **Integrate** | Skip-the-sim predictors (BioEmu, NeuralPLexer2, IsoDDE, Aqemia) | Integrate as optional upstream pre-filters | Inexpensive prediction first; commit to costly MD only on promising candidates. They feed the pipeline rather than replace it. |
| **Adopt** | Verifier loop (Recursion LOWE) | Adopt the pattern | Predict → test → falsify → improve is the model for how recovery verifies a fix before resuming. |
| **Adopt** | Guardrail agent (Artificial Tippy) | Adopt the pattern | A tool-less safety agent gating high-risk actions corresponds to the system's approval gates. |
| **Adopt** | 4-label memory provenance (OpenBrain) | Adopt the discipline | Only `observed`/`confirmed` beliefs are execution-trusted; `inferred` LLM output is verified before it can act. |
| **Adopt** | Checkpoint-restore (Schrödinger Multisim) | Adopt as Tier 1 | A bitwise-exact safe restart is already proven by an incumbent; it serves as the always-first recovery step. |
| **Adopt** | Conditional routing (OpenEye Orion) | Adopt and extend | Branching on success/failure as in Orion's workflows, extended beyond pre-coded conditions — the point of differentiation. |

In summary, in-house development concentrates on the recovery core, the preparation skill, and the planning layer. All remaining capability is supplied either by integrating an external engine or predictor behind a defined interface, or by adopting a pattern an existing tool has already validated.

---

## 2. Infrastructure decision and recommendation

A single infrastructure question remains open: whether a production remote HPC backend will be available (Scenario A, local-only, versus Scenario B, a remote staging server). For development this is settled — local execution — but the production answer determines whether GPU, scheduler, and remote-dispatch code paths are ever built.

**Recommendation:** continue local development, keep the engine and dispatch context swappable, and defer scheduler-specific (Slurm/PBS) logic until a remote backend is confirmed. This is already structurally in place: the validated golden path routes all MD through a single engine-agnostic interface, so a switch to Scenario B reduces to selecting a GPU engine and a remote dispatch context, with no change to the recipe files.

**Open question:** confirmation from Single Particle as to whether a remote cluster is provisioned, including scheduler type, GPU availability, and authentication.

---


## 3. Positioning and differentiation

- **Controlled, not autonomous, modification of physics.** A natural concern is that the system permits an AI to alter simulation physics. The design escalates rather than improvises: Tier 1 (a safe checkpoint-restart) is always attempted first; Tier 2 activates only if Tier 1 fails again, and modifies parameters strictly within fixed mathematical bounds (`dt ≤ 2 fs`, a valid interaction cutoff, SHAKE enabled). Modification is an escalation of last resort, grounded in the OpenClaw methane-oxidation case study and the falsification loop demonstrated by Recursion's LOWE.
- **Complementary to, not replaced by, prediction.** Prediction models function as fast oracles that feed MD; they cannot resolve kinetics, pathways, or induced-fit dynamics, and become unreliable on unfamiliar molecules. The proposed system makes the physics-based MD they cannot replace runnable without supervision.
- **A genuinely unoccupied position.** No surveyed tool provides autonomous runtime-failure recovery: incumbents restart from a checkpoint (Multisim) or route around pre-coded failures (Orion); prediction models run no trajectory to recover; and agentic tools orchestrate without modifying physics. The field addresses every MD bottleneck except this one.

