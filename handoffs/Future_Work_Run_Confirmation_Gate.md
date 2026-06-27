---
tags: [project-prime, openclaw, future-work, discord, ux, agentic-reasoning]
type: future-work
status: candidate-not-started
created: 2026-06-26
---

🟡 **Design decision / our framing — candidate future work, deliberately not started.** Banked 2026-06-26 during a conceptual session walking the advisor's `mdin-edit` feedback (point #4: `nstlim` vs output frequency) and the broader "never silently make a data-quality-compromising change" principle. This is an opt-in UX expansion; **starting it is a deliberate decision gated by the approach pick below.** No code was written.

# Future work: a confirm-before-launch gate for agent/Discord-driven runs

## The idea

Before an agent-driven MD run actually kicks off (and burns compute), present the resulting plan/schedule to the user and require an explicit **"go"** — so a bad `nstlim`/sampling choice (or any costly mistake) is caught *before* the simulation, not after it completes with unusable data. This generalizes the advisor's point-#4 request ("present the output schedule for confirmation before applying") from a single edit to the **launch** of a whole run.

## The decision banked (the hard part)

**Do NOT implement this as a literal blocking `Proceed?` prompt inside a skill** (e.g. an `input()` in `mdin-edit`'s default path, or in `run_happy_path` / `pipeline-async`). In this stack a blocking read on stdin would **deadlock** every non-interactive caller:

- the agent calling skills via the `exec` tool (no interactive stdin → stalls to the 120 s idle timeout),
- the **detached Discord pipeline** (`pipeline-async`, no human at a keyboard),
- `md-planner`'s executor, which chains the wrappers directly,
- `--submit` smoke (subprocess-calls the wrapper across a min1→prod chain),
- the **~240k-assertion test harness**, which runs the wrappers thousands of times.

The skill contract is "a pure, non-blocking, deterministic transform that reports what it did." **Interactivity belongs at the agent/human layer, not inside the deterministic tool** — same decoupled-agent seam the whole project is built on. Note `--dry-run` is *already* a non-blocking confirm-before-apply (preview → commit), so the advisor's point-#4 intent is met today; this note is about the **launch** UX, not the edit UX.

## Two viable homes (pick one — this is the gate)

1. **Agent/conversation layer (recommended, no skill change).** On a run request the agent runs the relevant `--dry-run`, posts the schedule to Discord, **ends its turn without launching**, and treats your next message ("go") as approval before launching. Interactivity lives where it belongs. *Cost:* the gate's reliability rides on LLM discretion — a terse/cheap model could skip it. Low effort (a `SKILL.md` / system-prompt instruction).

2. **Staged-spec two-tool handshake (robust).** Split the launch:
   - `stage-run` — computes the schedule (reusing the existing dry-run machinery), writes a `pending_run.json` (the exact resolved command + timestamp), posts the preview. **Never launches.**
   - `confirm-run` — deterministically reads `pending_run.json`, hard-errors if nothing is staged / it's stale, else launches exactly that spec.

   Buys: no parameter drift between preview and launch, an auditable single launch entry point, no launch-by-accident. *Residual gap (honest):* the agent could `stage`-then-`confirm` without truly waiting — closing that fully would need `confirm-run` to verify a human approval it can't see from Discord; not worth it for a solo demo. Moderate, contained effort + a couple of tests.

**Ironclad** (deterministically impossible to launch without human sign-off) is explicitly **out of scope** — the only expensive step (the simulation) is already behind the agent, and a wrongly-launched run costs compute, not safety.

## Why this does not reopen banked decisions

It does **not** reopen [[multi-agent-scope]] (no new agent — it shapes the existing agent's turn boundary, or adds two thin deterministic tools) and it does **not** contradict the `mdin-edit` "never blocks" contract — both options keep the skills non-interactive.

## Prompt to paste (fresh session, when you decide to start)

> Read [[Future_Work_Run_Confirmation_Gate]] and [[Definition_of_Done]]. Decide between (1) the agent-layer conversational gate and (2) the staged-spec `stage-run`/`confirm-run` handshake for confirm-before-launch on Discord/agent-driven MD runs. If (2), build oracle-first (a `pending_run.json` round-trip oracle + a "confirm with nothing staged → hard error" test) before wiring it into `pipeline-async`. Keep all skills non-interactive; do not add a blocking prompt to the default path. Then apply the Definition-of-Done sync set.

## Related

- [[Research_Advisor_Feedback_mdin_edit]] — point #4 (the `nstlim`/output-schedule origin of this idea).
- [[Future_Work_Proposer_Agent]] — the other agent-layer candidate (propose-then-verify); sibling in scope discipline.
- [[Arch_Taskboard_Manifest]] / `md-planner` — the existing propose-then-validate pattern this extends to *launch*.
