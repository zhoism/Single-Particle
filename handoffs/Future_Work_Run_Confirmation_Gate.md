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

## What's already shipped (advisor #4) vs what this adds — SCOPE

The advisor's *literal* point-#4 ask — "present the output schedule for confirmation before applying" — is **already met, at the EDIT level**, by the shipped `mdin-edit` refinements (project-prime `246b06f`):
- editing `nstlim` emits an `output_schedule` (`trajectory_frames` / `energy_outputs` / `trajectory_off`) **plus** sparse/zero/uneven-sampling **warnings**, judged against the file's read-only `ntwx`/`ntpr`;
- `--dry-run` previews that whole envelope so you confirm **before the file is written**.

A real example (`--dry-run` editing `prod nstlim → 15000`): `"only 1 trajectory frame(s); very sparse sampling"` + `output_schedule.trajectory_frames: 1`. So a *bad single edit* is already caught.

**This note is the LAUNCH-level generalization** — surface that same schedule across the *entire resolved run* before the multi-hour sim kicks off, not one edit. It would **reuse the existing `output_schedule` machinery**, applied to the resolved run. Because the edit-level concern is already handled, this is **low-urgency** — it only bites on long, real production runs.

**Where the preview surfaces — as a user, where do you look?**
- **Terminal (direct CLI):** the `--dry-run` envelope is JSON on **stdout** — you read it right there (a `[prod.in] edited` marker goes to stderr). md-planner's `compile` likewise emits a byte-inspectable JSON plan.
- **Agent (`openclaw agent`):** the agent captures that JSON via `exec` and summarizes it in its chat reply ("heads up — 1 frame, very sparse").
- **Discord:** the detached pipeline already posts LLM-free progress to the `NOTIFY_CHANNEL`. What does NOT exist yet is a **human-readable preview posted there that waits for your "go"** — that posted-and-waits step is exactly what this gate adds.

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

## Sharpened approach (2026-06-27) — the "two homes" are a spectrum; pick Level 2 + TTY

- **Level 0 (exists):** a preview artifact already exists — `--dry-run` (edits) + md-planner's compiled plan.
- **Level 1 = home (1):** agent convention — show the plan, end the turn, wait for "go". ~Free; reliability rides on LLM discretion (a cheap model may skip it).
- **Level 2 = home (2):** `stage-run`/`confirm-run`. Even if the agent calls both back-to-back, you still get **no preview→launch drift, no launch-from-nothing, one auditable entry + a staleness check.** It does NOT force a human — but it stops *accidental/drifted* launches. **Same halt-and-reinvoke idiom as `needs_human` (mdin-edit) and amber-recover's bounded HALT** → architecturally consistent.
- **Level 3 (overkill):** a true human gate over Discord — `confirm-run` requires an approval **authored by a non-bot human Discord user**. The *token* alone isn't the security (the agent can read it); the **authorship** is — the agent posts only as the bot, so it can't forge a human-authored message. Needs inbound Discord reply-correlation, which isn't built.

**Why ironclad-over-the-agent is structurally impossible (the real reason, not just "not worth it"):** the agent runs with **raw shell via `exec` (sandbox off)**, so it can bypass *any* tool gate by running the launch command directly. No in-pipeline gate can deterministically stop a raw-shell agent; closing that would mean removing the agent's shell, which breaks the skill-execution model. Worst case is wasted *compute* (local, $0), so it's not worth it.

**Recommendation — approach pick essentially made: Level 2 + a TTY-guarded `--confirm`.** Level 2 gives the agent path every determinism available there (no drift / no accident / audit) and funnels well-behaved runs through one previewed entry; the TTY guard (`if stdin.isatty(): block for y/n; else proceed`) gives the **human-CLI path a real gate for free, without deadlocking** the automated callers. Skip Level 3. Build only when long production runs start.

## Why this does not reopen banked decisions

It does **not** reopen [[multi-agent-scope]] (no new agent — it shapes the existing agent's turn boundary, or adds two thin deterministic tools) and it does **not** contradict the `mdin-edit` "never blocks" contract — both options keep the skills non-interactive.

## Prompt to paste (fresh session, when you decide to start)

> Read [[Future_Work_Run_Confirmation_Gate]] (esp. the "Sharpened approach" section) and [[Definition_of_Done]]. Build the **Level 2 + TTY** confirm-before-launch: a `stage-run`/`confirm-run` handshake (`stage-run` writes a `pending_run.json` + posts the schedule preview, never launches; `confirm-run` reads it, hard-errors if missing/stale, launches exactly that spec) **plus** a TTY-guarded `--confirm` for the human-CLI path (`if stdin.isatty(): block; else proceed`). Build oracle-first: a `pending_run.json` round-trip oracle + a "confirm with nothing staged → hard error" + a "stale spec → refuse" test, before wiring into `pipeline-async`. Reuse mdin-edit's `output_schedule` machinery for the preview. Keep all skills non-interactive on the automated path; do NOT add a blocking prompt to the default path; do NOT build Level 3 (raw-shell `exec` makes ironclad-over-the-agent moot). Then apply the Definition-of-Done sync set.

## Related

- [[Research_Advisor_Feedback_mdin_edit]] — point #4 (the `nstlim`/output-schedule origin of this idea).
- [[Future_Work_Proposer_Agent]] — the other agent-layer candidate (propose-then-verify); sibling in scope discipline.
- [[Arch_Taskboard_Manifest]] / `md-planner` — the existing propose-then-validate pattern this extends to *launch*.
