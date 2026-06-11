# Example: decision-banked entry (architectural call with "do not re-litigate")

From Dev_Log.md, 2026-06-03 — El Agente Q paper assessment. ~30 lines. The reasoning *is* the artifact.

```markdown
## 2026-06-03 (cont., branch) — El Agente Q paper assessed; multi-agent scope decided 📄🦞

**Context:** Side-branch session. User flagged arXiv:2505.02484v2 (Zou et al., Aspuru-Guzik group; "El Agente: An Autonomous Agent for Quantum Chemistry") asking whether its 22-agent hierarchical architecture transfers to Project Prime. Read pages 1–6 of the PDF directly; cross-checked against today's substrate findings.

**Their architecture:** 22 specialized LLM agents (top-level computational-chemistry planner → 3 module heads geometry/quantum/I/O → 18 specialists including 9 ORCA-block experts). Built on CoALA + Soar substrate. Hierarchical procedural memory; working memory with 4 components (global, agent-conversation, grounding-via-FS, long-term). Markov-style context filtering between levels. Jupyter-notebook action trace export. Reported >87% task success on university-level DFT exercises.

**Where it corroborates our discipline:** hierarchical context filtering, specialized-context-per-role, cybernetic feedback retries, action-trace audit, and grounding-via-filesystem all match what our wrapper architecture + [[Workflow_Error_Recovery_Loop]] + Dev_Log already do — typically with stricter LLM/deterministic separation. Strongest published peer for [[Arch_Taskboard_Manifest]] discipline.

**Where it doesn't transfer:** DFT inputs have 200+ flags across 50+ ORCA blocks with subtle cross-block constraints. AMBER `&cntrl` has ~30 keywords in 5 clusters; the [[phase3-advisor-demo]] 11-stage protocol already encodes best practices end-to-end. Their 9 block-expert agents map to **one** wrapper-internal namelist-heuristics dictionary for us. Also, each inter-agent call ≈ ~100s on Flash (Stage 1c empirical); 22-agent multi-hop = 8–16 min/task. Unusable for demo cadence.

**Architectural decision banked:** Project Prime stays at **max 3 named OpenClaw agents** — `main` (today) + future `planner` (when Stage 7 lands) + future `recovery` (when Stage 8 lands). Dynamic sub-agents only if we ever expand to high-throughput virtual screening (Stage 9+, out of current manifest scope). Skills already absorb most of El Agente's agent-side decomposition; pay the multi-agent latency cost only where there's genuine context-separation benefit (different model, different prompt, different thinking level).

**Worth borrowing later (not blocking):** their action-trace-to-Jupyter export as a future reproducibility deliverable; their imaginary-frequency-removal-agent as the conceptual pattern for our Stage 8 recovery sub-skills.

**Artifacts:**
- `Research_El_Agente_Q.md` — full source note with paper summary, architecture diagram, idea-by-idea evaluation, BibTeX.
- `OpenClaw_CLI_Map.md` — cross-link added in Related Notes pointing to the assessment.
- Memory `multi_agent_scope` — decision banked so future sessions don't re-litigate; MEMORY.md index updated.

**Next:** unchanged. Stage 2 (Skill_Antechamber_LigandPrep) is the next concrete work. Multi-agent expansion deferred until Stages 7/8 land and earn their way.

---
```

## What makes this a good decision-banked entry

- **Headline names the decision.** "multi-agent scope decided" — no need to read further to know what landed.
- **"Their architecture" / "Where it corroborates" / "Where it doesn't transfer" structure** mirrors how the reasoning actually went. Reader can follow the case.
- **The decision is bolded and crisp.** "max 3 named OpenClaw agents" + the named conditions for revisiting (Stages 7, 8, 9+).
- **"Worth borrowing later" carries the future hooks** without committing to them now.
- **The memory `multi_agent_scope` is named** — future sessions can find the banked decision.
- **"Do not re-litigate" framing implicit** in the memory description + the "Next: unchanged" — signals that this is settled.

## When to write this type vs a substantial entry

Decision-banked when:
- The output is the *decision*, not new files or stage transitions.
- The reasoning needs to be preserved so future-you doesn't re-litigate.
- A memory is being created or updated specifically to bank the decision.

Substantial when:
- Multiple concrete deliverables shipped.
- A stage flipped.
- A failure mode was caught + corrected.

A session can warrant both — write two separate entries (the 2026-06-03 day has 3, including this one).
