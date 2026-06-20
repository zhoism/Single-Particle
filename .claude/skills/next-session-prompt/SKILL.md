---
name: next-session-prompt
description: Use to generate a Next_Session_Prompt_*.md handoff file in the vault's `handoffs/` folder when the current session has substantial state that the next fresh-chat session must pick up cleanly. Triggers on "write a handoff prompt", "next session prompt", "wrap into a starter", "Day N+1 prompt", or naturally at session end when the next session will be in a fresh chat. Output is a paste-ready vault note containing recap + pasteable prompt + decision-banked guards.
---

# next-session-prompt — fresh-chat handoff scaffold

Convention: each phase has a starter prompt in the vault's **`handoffs/`** folder (`handoffs/Next_Session_Prompt_<Topic>_<DayN>.md`) to be pasted into a fresh Claude Code session. The prompt minimizes rediscovery, preserves banked decisions, and points at the right vault notes / memories to load first.

Existing exemplars:
- `Next_Session_Prompt_OpenClaw.md` (Day 1 entry — substrate setup)
- `Next_Session_Prompt_OpenClaw_Day4.md` (Day 4 entry — Stage 2 work, comprehensive 200+ lines)
- `Next_Session_Prompt_Phase1Report.md` (report-side context)

## When to invoke

- Current session is wrapping with substantial banked state that a fresh chat would re-derive.
- A natural day boundary (OpenClaw Day N → Day N+1, Phase 2 → Phase 3).
- A discrete deliverable just landed (Stage 1 complete, report submitted) and the next stage starts cold.
- The user asks "write a handoff prompt" / "set up the next session" / "starter for tomorrow".

## When NOT to invoke

- The next session is a continuation of the same chat. No handoff needed.
- No state changed — last session's prompt still applies. Update it in place if minor; rewrite only if substantial.
- The session was exploratory with no banked outcome. There's nothing to hand off.

## Hard rules

1. **Lead with what NOT to re-litigate.** Banked decisions belong at the top, not buried. Future-you will skim — front-load the don't-re-do list.
2. **Memory references by exact name, not paraphrase.** "Read `openclaw_canonical_paths` memory" not "read the OpenClaw memory." Slug matching matters.
3. **Pre-flight sequence first.** The fresh chat doesn't know what state should still hold from yesterday. First N steps are environmental sanity checks; only then real work.
4. **Scope-fence the immediate task.** "Stage 2 only — DO NOT extend to Stage 3+." Without this, sessions sprawl.
5. **Pasteable prompt in a code fence.** Separated cleanly from the recap. The user copies the fenced block into the new chat; the recap stays in the vault.
6. **Frontmatter `status: ready` flip.** When the next session starts, flip to `status: consumed`. Tracks whether the handoff was actually used.
7. **Cross-link the handoff in the relevant Dev_Log entry's `Next:` line.**

## Procedure

**Step 0 — Read context:**
- `templates/skeleton.md` — the file structure.
- `examples/day4-exemplar.md` — what a substantial handoff looks like.
- Most recent Dev_Log entries (today's + yesterday's) — the state to encode.
- Existing `Next_Session_Prompt_*.md` for this thread — supersede if applicable.

**Step 1 — Determine handoff scope.** Before drafting:
- What phase / topic? (OpenClaw, Phase1Report, Phase3-stage-N)
- What's the next session's day-number or stage-number?
- What banked decisions must not be re-litigated?
- What state from this session must still hold tomorrow? (config patches applied, env activated, etc.)

**Step 2 — Draft using the skeleton.** Required sections:
- Frontmatter (tags, type: handoff, status: ready, created: YYYY-MM-DD).
- `# Next Session Starter — <Topic> <DayN>` headline.
- Quoted callout summarizing what's done + how to use this file.
- `## Day N-1 recap (what's done — don't re-discover)` — bullet list of completed work.
- `## Decisions banked — do NOT re-litigate` — explicit guard list.
- `## What's NOT done (deferred, non-blocking)` — open items that future-you should know exist.
- `## The prompt to paste` — fenced code block with the actual prompt.
- `## After the session — update this file` — instructions for closing the loop.

**Step 3 — Compose the pasteable prompt.** The fenced block must include:
- One-line orientation: "Continuation of <topic> — <DayN>. <one-line state summary>."
- Today's work scope, with the scope-fence.
- Memory + vault notes to load, in order, with one-line reason for each.
- Immediate sequence — numbered preflight + work steps.
- Decisions-banked reference (point at the section above).
- A "stop conditions" line so the session knows when to write the next handoff.

**Step 4 — Place file.** In the `handoffs/` folder, name `handoffs/Next_Session_Prompt_<Topic>_<DayN>.md` (kebab-case `_DayN` suffix). Then add a one-line entry for it under the right status heading in `handoffs/README.md` (the forward-queue index).

**Step 5 — Cross-link.** Update the Dev_Log entry's `Next:` line to point at the new prompt file.

**Step 6 — Update any prior handoff.** If a `Day N-1` prompt is still `status: ready` and is now superseded, flip its frontmatter to `status: superseded` with a one-line pointer to the new file.

## Length calibration

- **Short handoff** (~30–50 lines): one banked decision, one work item. Example: 2026-05-24 OpenClaw Day 1 starter.
- **Substantial handoff** (~100–200 lines): multiple banked decisions, multi-step preflight, multi-step work. Example: 2026-06-03 OpenClaw Day 4 starter.

Err short. The recap section is for re-skimming; the pasteable prompt is for the fresh chat. Both can grow tomorrow if today's work shipped substantial banked state.

## Anti-patterns

- Do NOT inline the contents of memories or vault notes. Reference by name. The fresh chat will load them itself.
- Do NOT use relative dates ("yesterday", "last session"). Absolute: "2026-06-03".
- Do NOT re-state the project's vision / CLAUDE.md / SOP. The fresh chat loads those automatically.
- Do NOT write a handoff every session. Most session ends → just a Dev_Log entry. Only when state genuinely needs to ride forward.
- Do NOT bury the scope-fence. "Stage 2 only — DO NOT extend" must be visible without scrolling.
- Do NOT delete the prior handoff. Flip it to `status: superseded` and add a pointer. The graph of handoffs is part of the audit trail.

## Cross-references

- Vault `Next_Session_Prompt_OpenClaw_Day4.md` — the comprehensive exemplar.
- Vault `Next_Session_Prompt_OpenClaw.md` — the short exemplar.
- Memory `dev_log_convention` — the Dev_Log Next: line is where the handoff is linked from.
- Memory `openclaw_canonical_paths` — exemplar of the kind of state-encoding a handoff points to.
