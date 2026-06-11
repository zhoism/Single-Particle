# Example: marker entry (config / planning decision)

From Dev_Log.md, 2026-05-20. ~12 lines. A config decision with no implementation work to document.

```markdown
## 2026-05-20 — LLM provider decision: Google AI Studio only (Ollama dropped)

**Done today:**
- **Provider locked to Google AI Studio** for the agent's reasoning layer. Ollama / local-LLM paths are off the table — user's Mac doesn't have the headroom to host a usable-size model. User has **$300 AI Studio credits / 90-day window**, more than sufficient for the demo scope.
- Original 2026-05-14 plan (Ollama primary + AI Studio fallback) is superseded. [[project-prime-status]] memory updated; future skill designs target a single-provider (Gemini) API.

**State of the vault:** No vault content edits — this is a config / planning decision, captured in memory + Dev_Log only. Phase 2 step 3 (OpenClaw init + LLM wiring) is now simpler since the LLM half is single-provider.

**Next session:**
- OpenClaw distribution research (pip / npm / source?) → install → wire to AI Studio (Gemini Flash default, Gemini Pro for the few heavy-reasoning calls).
- Hello-world skill that dispatches a trivial shell command before pointing it at AMBER.

---
```

## What makes this a good marker entry

- **Headline tells the decision in one line.** Reader doesn't need to read the body to know what changed.
- **Body is 3 short paragraphs.** Decision + supersedes-what + state-of-vault.
- **"No vault content edits" stated explicitly.** Tells future-you not to look for an artifact.
- **Memory link `[[project-prime-status]]`** carries the actual state — the Dev_Log is the marker, the memory is the canonical state.
- **Next:** points at the unblocked sequence with concrete first step.

## Anti-pattern this avoids

- Doesn't explain *why* Ollama was originally chosen (the prior entry does that).
- Doesn't speculate about Gemini Flash vs Pro pricing in depth (that's a future entry's job if it becomes relevant).
- Doesn't claim work that wasn't done.
