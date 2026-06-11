---
name: devlog-append
description: Use at the end of a meaningful working session to append a Dev_Log entry. Triggers on "log this", "dev log entry", "session wrap-up", "log the session", or after a substantial deliverable has landed (stage complete, decision banked, report submitted, new failure mode caught). Output is a reverse-chronological entry at the top of Dev_Log.md following the project's marker+pointers (not duplicates) convention.
---

# devlog-append — structured Dev_Log entry

Project convention: `Dev_Log.md` at vault root, reverse-chronological (newest on top), each entry a **marker + pointers**, never a duplicate of the work. Per `dev_log_convention` memory.

## When to invoke

- User says "log this" / "dev log entry" / "log the session" / "wrap this up in the dev log".
- A stage in `Phase3_Taskboard_Manifest.md` flipped from PENDING to COMPLETE.
- A decision was banked (intake-verify ROW/NO call, architecture call like multi-agent scope).
- A new failure mode or pattern was caught (Discord token leaked, fabricated paper, recovery hallucination).
- A submission shipped (Phase 1 report, demo).

## When NOT to invoke

- Mid-session exploration with no concrete deliverable. The log records markers, not running commentary.
- Routine maintenance (typo fix, vocab cleanup) — fold into the next substantial entry.
- Re-litigation of a banked decision. Update the original entry's banked-decision pointer instead.

## Hard rules

1. **Marker + pointers, NOT duplicate.** The entry says *what was done* and *where the artifacts live*, not *the content of the artifacts*. If you find yourself copying full report text into the Dev_Log, stop — link to the report and quote one decisive sentence.
2. **Reverse-chronological insertion at the top.** New entry goes immediately after the `---` separator that follows the file's header preamble. Older entries flow downward.
3. **One headline emoji per entry.** Optional, but if used: single domain-relevant emoji at end of headline (🦞 OpenClaw, 🧪 chemistry, ✅ green, 🚩 issue caught, 📝 docs, ⚙️ setup, 🛡️ hardening).
4. **Cross-link with `[[wikilinks]]`** to vault notes and memories. The graph traversal that makes the log useful depends on these links existing.
5. **Convert relative dates to absolute.** "yesterday" → "2026-06-03". Memory + log entries get re-read months later.

## Procedure

**Step 0 — Read context:**
- Last 1–2 entries of `Dev_Log.md` (for tonal continuity and to confirm what's already logged).
- `templates/entry-skeleton.md` for structure.
- `examples/` for length calibration (marker / substantial / decision-banked).

**Step 1 — Identify the entry type.**
- **Marker** (~5–10 lines): a config/planning decision with no implementation. Example: 2026-05-20 LLM provider lock.
- **Substantial** (~30–60 lines): a multi-hour session with deliverables. Example: 2026-06-03 Stage 1 substrate verification.
- **Decision banked** (~20–40 lines): an architectural call with reasoning + "do not re-litigate" framing. Example: 2026-06-03 El Agente Q multi-agent scope.
- **Failure mode** (~15–40 lines): a caught pattern with a lesson. Example: 2026-05-28 STAR-MD fabrication.

**Step 2 — Draft using the skeleton.** Required sections:
- `## YYYY-MM-DD — <headline> <emoji>` (or `## YYYY-MM-DD (cont.) — ...` if continuing same calendar-day session)
- `**Context:**` — what triggered this entry, in 1–2 sentences.
- `**Done:** / **Verified:** / **Decision:**` — pick verbs by entry type.
- `**Artifacts:**` — list of files + memories touched, with `[[wikilinks]]`.
- `**Next:**` — what the next session picks up. Often a one-liner pointing at the next manifest stage.

**Step 3 — Length calibration.** Match length to weight:
- Don't bloat a config decision into 50 lines.
- Don't compress a thesis-touching decision into 8 lines.
- If unsure, err shorter — the log is a marker, not a summary-of-summary.

**Step 4 — Insert.** Find the top entry's `---` separator. Insert the new entry immediately after the header preamble's closing `---` and before the previous newest entry.

**Step 5 — Cross-link.** Every artifact mentioned gets a wikilink. Every memory updated gets a `[[memory-name]]`. Every vault note touched gets `[[note-name]]`.

## Headline emoji conventions (from existing entries)

- 🦞 OpenClaw work
- 🧪 chemistry / MD execution
- ✅ green / passed
- ⚙️ setup / config
- 📝 docs / writeup
- 📥 inputs received
- 🏁 phase closed
- 🚩 issue caught / red flag
- 🛡️ thesis hardened
- 🔧 fix / correction
- 📚 deep read / source study
- 📄 paper assessment
- ➕ added (matrix row, scope expansion)
- 🚫 NO-row / rejected
- 🔍 verification

Pick one. Don't stack.

## Anti-patterns

- Do NOT paste a full report section into the Dev_Log. Link + quote one decisive sentence.
- Do NOT re-state the body of a memory in the Dev_Log. Link to the memory.
- Do NOT write a Dev_Log entry per micro-step. One entry per session, or one per discrete deliverable if the session shipped multiple.
- Do NOT lose the "Next:" pointer. Even if next is "nothing scheduled," state that.
- Do NOT use future tense for what was done. "Did X" not "Will do X" — past tense for the body, future for the Next pointer only.

## Examples

- `examples/marker-entry.md` — short config/decision entry.
- `examples/substantial-entry.md` — multi-deliverable session.
- `examples/decision-banked-entry.md` — architectural call with "do not re-litigate" framing.

## Cross-references

- Memory `dev_log_convention` — the canonical convention (vault-root, reverse-chrono, markers + pointers).
- Vault `Dev_Log.md` — every prior entry as in-vivo exemplar.
