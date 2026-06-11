# Example: substantial handoff (OpenClaw Day 4, 2026-06-03)

Reference: vault `Next_Session_Prompt_OpenClaw_Day4.md`. ~200 lines.

## What it does well

- **Headline includes day number + phase.** "Next Session Starter — OpenClaw Phase Day 4" — fresh chat immediately knows the thread.

- **Quoted callout summarizes the previous day in one paragraph + tells the user what to do with the file.** No ambiguity about whether to read or paste.

- **Day 3 recap is bulleted with explicit "don't re-do" callouts.**
  > **Stage 2 step 1 DONE.** `skills.load.extraDirs` patched into `~/.openclaw/openclaw.json` registering `project-prime/skills/` with watcher on. **Do NOT re-apply.** Verify with `openclaw config get skills.load`.

  The pattern `**Do NOT re-apply.**` is visually loud and unambiguous. Future-you scans for it.

- **Architectural decisions banked section is its own subsection** with explicit memory references:
  > Wrapper-internal chaining (1 exec call per skill turn, NOT agent-orchestrated sub-steps) — see [[openclaw-canonical-paths]] §6 latency analysis + `OpenClaw_CLI_Map.md` §Stage 2 design intuition.

  Names the canonical memory + the vault note + the specific section.

- **"What's NOT done (deferred)" section** keeps open items visible without conflating them with the work-to-do.

- **The pasteable prompt is in a fenced code block, separated from the recap.** The user knows what to copy.

- **Inside the prompt: memory references are exact slug names**, not paraphrases:
  > - memory: openclaw-canonical-paths (CRITICAL — 16 sections, load-bearing CLI/runtime facts including SKILL.md authoring §8 and skill loading §9)
  > - memory: project-prime-status, openclaw-install-state, openclaw-vertex-gap, ...

  The fresh chat can grep these exact slugs in `MEMORY.md` and load the files directly.

- **Reading order is explicit and prioritized.** "Read these vault notes + memories BEFORE acting (in this order)" — not just a list, an ordering with a reason.

- **Immediate sequence is numbered + sub-stepped + time-estimated.**
  > 1. PRE-FLIGHT — confirm Day 3 state still holds (5 min):
  >    a. openclaw gateway status (running, write-capable)
  >    b. openclaw config get skills.load (should return extraDirs + watch + debounce)
  >    c. openclaw models status | grep cooldown (should NOT show cooldown)

  Each sub-step says what to check AND what the expected pass condition looks like.

- **Scope-fence at multiple levels:**
  > Immediate sequence (Stage 2 — DO NOT extend scope to Stage 3+):

  In the prompt header AND repeated in the section title.

- **Closing checklist:** the prompt tells the next session what to do BEFORE ending — log the session, write the next handoff, update the manifest. No hand-waving.

## Anti-patterns this avoided

- Doesn't inline the contents of `openclaw-canonical-paths` memory. Just points at it.
- Doesn't re-state the project vision.
- Doesn't use relative dates.
- Doesn't bury the don't-re-do items.

## Length rationale

Day 4 starter is ~200 lines because:
- Day 3 shipped THREE banked decisions (multi-agent scope, wrapper-internal-chaining, 4 upstream patterns to adopt).
- Day 3 had a non-trivial config patch persisted (extraDirs).
- Stage 2 work is multi-step (scaffold + populate + test + validate + log).
- This is the first time the project-prime/skills/ directory is being actively used.

A trivial day boundary would warrant a 30-line handoff. A trivial scope change might not warrant a handoff at all (update the prior one in place).

## When NOT to mimic this length

- If only one banked decision: trim to ~50 lines.
- If only one work item: trim preflight + work to a single numbered sequence.
- If no environmental state needs to ride forward: skip the preflight section entirely.

Err short. The handoff is a starter, not a manual.
