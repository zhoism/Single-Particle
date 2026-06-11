---
tags: [project-prime, <topic>, session-handoff, <day-or-stage-tag>]
type: handoff
status: ready
created: YYYY-MM-DD
---

# Next Session Starter — <Topic> <Day N+1 / Stage N>

> Created YYYY-MM-DD at end of <previous day/stage>. <One-line summary of what completed.> <Next stage> starts at <specific work item>. Paste the code block in the §The prompt to paste section into a fresh Claude Code session (run from the vault).

## Day N recap (what's done — don't re-discover)

- **<Item 1>** — <one-line summary with link to artifact / Dev_Log / memory>.
- **<Item 2>** — <ditto>.
- **<Item 3 done DON'T REDO>** — <particularly important DO-NOT-REPEAT items, e.g., a config patch applied>.

## Decisions banked — do NOT re-litigate

- **<Decision 1>** — <one-line statement>; see [[<memory or note>]] for the full reasoning.
- **<Decision 2>** — <ditto>.

## What's NOT done (deferred, non-blocking)

- **<Open item 1>** — <why deferred>. Re-evaluate after <trigger>.
- **<Open item 2>** — <ditto>.

## The prompt to paste

```
Continuation of <topic> — <Day N+1 / Stage N>. <One-line state summary>.

Today's work: <scope-fenced description of the immediate task>.

Read these vault notes + memories BEFORE acting (in this order):

- memory: <name-1> (CRITICAL — <reason>)
- memory: <name-2>, <name-3>, <name-4>
- vault: <Dev_Log.md (specific entry-range), Phase3_Taskboard_Manifest.md (Stage N section), <other relevant notes>>

Decisions banked, do NOT re-litigate:
- <Decision 1, one line>
- <Decision 2, one line>

Immediate sequence (<scope-fence>: only this scope):

1. PRE-FLIGHT — confirm yesterday's state still holds (~5 min):
   a. <env / config sanity check 1>
   b. <env / config sanity check 2>
   c. <env / config sanity check 3>

2. <First substantive step>:
   - <Sub-step 1>
   - <Sub-step 2>

3. <Second substantive step>:
   - <Sub-step 1>
   - <Sub-step 2>

4. CLOSING (do these before ending):
   a. Update Phase3_Taskboard_Manifest.md stage status.
   b. devlog-append skill: log the session.
   c. next-session-prompt skill: write Day N+2 / Stage N+1 starter (or note that none is needed).

Stop conditions:
- If <blocker condition>, STOP and ask the user before extending scope.
- If preflight shows <unexpected state>, do NOT proceed — investigate why state diverged.

Scope-fence: <Topic> <Day N+1 / Stage N> ONLY. Do NOT extend to <next stage / topic>.
```

## After the session — update this file

When the next session consumes this handoff:
1. Flip frontmatter `status: ready` → `status: consumed`.
2. Add a footer: `## Outcome\n\nConsumed YYYY-MM-DD by Day N+1 session. Outcome summary: <1-sentence>. See [[Dev_Log]] entry YYYY-MM-DD.`
3. If the handoff was superseded mid-day (e.g., scope changed), flip to `status: superseded` with a pointer to whatever replaces it.

## Cross-links

- [[Dev_Log]] entry YYYY-MM-DD — the session that produced this handoff
- [[Phase3_Taskboard_Manifest]] — the manifest stage this handoff serves
- <any other relevant cross-links>
