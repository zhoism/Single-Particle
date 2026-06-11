# Dev_Log entry skeleton

```markdown
## YYYY-MM-DD — <one-line headline> <single-emoji>

**Context:** <1–2 sentences on what triggered this entry. Reference the manifest stage / advisor ask / prior session continuation.>

**<Verb-section>:** <The substance. Bullets or short paragraphs.>
- <Bullet.>
- <Bullet, with [[wikilink]] to artifact.>

**[Optional: Verification:** <For intake/audit entries. Per-source verdict.>]

**[Optional: Decision:** <Banked decision with the criteria it rests on. Include "do not re-litigate" framing for architectural calls.>]

**Artifacts:**
- <File path or [[wikilink]] — one-line role.>
- <Memory `name` — what was updated.>
- <Or: explicit "no vault edits this session" if applicable.>

**Next:** <What the next session picks up. One sentence. Often a pointer to the next manifest stage or "<X> queued in [[Next_Session_Prompt_Y]].">

---
```

## Verb-section options

Pick the verb that matches the entry's purpose:

- **Done:** straightforward delivery (env installed, smoke test ran, report submitted).
- **Verified:** audit / inspection (install audit, intake verification).
- **Decision:** architectural call.
- **Found:** discovery (upstream library found, new failure mode).
- **Built:** new artifact created (golden path, scaffold).
- **Resolved:** prior open item closed (LLM auth resolved, Discord token rotated).
- **Banked:** architectural decision with re-litigation guard.

Most entries use 1–2 of these. Don't include all of them.

## The Context line

The Context line is the entry's hook. It should make the reader want to read the rest. Bad:

> Context: continued working on the project.

Good:

> Context: advisor handed off `phase3-explicit-solvent-md/` (pre-prepared complex MD demo) and `Amber26.pdf` (1104-page Amber 2026 reference manual). No execution yet — user explicitly scoped this session to bookkeeping + OpenClaw briefing prep.

It tells you what triggered the work, what was in scope, and what was deliberately out of scope.

## The Next line

The Next line points at the next concrete action. Bad:

> Next: continue.

Good:

> Next: Phase 3 Stage 1 (substrate verification — JSON output, bash tool, tool-chain tests). Also queued: write `OpenClaw_CLI_Map.md` vault note synthesizing today's CLI/intents/identity findings. Resume in `Next_Session_Prompt_OpenClaw_Day3.md`.

It names the action, optionally queues secondary items, and points at the handoff prompt if one exists.

## Length calibration

- Marker: ~5–10 lines. Single decision, no implementation.
- Substantial: ~30–60 lines. Multi-deliverable session.
- Decision banked: ~20–40 lines. The reasoning is the artifact.
- Failure mode: ~15–40 lines. Lesson must be extractable.

Err shorter when unsure. The log is a marker, not the work itself.
