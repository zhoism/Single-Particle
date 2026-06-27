---
tags: [project-prime, housekeeping, gitignore, run-output, convention, session-handoff]
type: handoff
status: candidate
created: 2026-06-26
---

# Next Session Starter — Route all run-output under `runs/` (durable git-noise prevention)

> Created 2026-06-26 during the housekeeping pass that cleared the *symptom* (project-prime `b375f39`). This is the **durable prevention**, deferred to its own session because it edits executable run scripts and needs a verifying pipeline re-run — non-trivial. Decision-gated / low-urgency: do it when the run-output noise next bothers you, or before onboarding anyone to the repo.

## Background — why git-noise builds up (root cause)

The project-prime tree had accreted **384 untracked files** across many demo runs. Two stacked causes:

- **The `.gitignore` is type-based, not location-based.** It ignores file *types* (`*.nc`, `*.prmtop`, `*.out`, `*.pdb`…) but the only ignored *directory* is `runs/*`. Demo runs were written to ad-hoc **top-level** dirs (`regression-1L2Y/`, `new-target-run/`, `stage6-wire-test/`…) that escaped the `runs/` ignore; their binaries got ignored by type, but stray text/metadata (`README`, `.err`, `.status`, `.json` envelopes, `_renum.txt`, `_sslink`) had no matching rule and piled up.
- **The DoD discipline manages *tracked* files, not the *untracked* tree.** "Stage explicit files by path, never `git add -A`" is correct for concurrency safety, but nothing ever reconciles untracked accumulation, and the Stop-hook nudges on uncommitted/unpushed (not untracked). So the noise grew silently — and *hid* genuinely-forgotten content (the golden-path/smoke-test recipe fixtures, now committed in `b375f39`).

## The work — enforce the convention the repo is already half-built for

`runs/*` is **already ignored** (`!runs/.gitkeep` whitelisted; `.gitkeep` now committed in `b375f39`). The fix is to make every run *write* there:

1. **`run_happy_path.sh`** — confirmed this session: it has **no `runs/`/OUTDIR default** (greps clean). Add a default output root under `runs/<name>/` (keep any existing positional `OUTDIR` override). STOP-and-surface if it would change a tracked test's expected path.
2. **The async pipeline** (`pipeline-async` / `pipeline-async-run-*`) — point its output root under `runs/` too (the `pipeline-async-run-*/` ignore can then retire, or stay as belt-and-suspenders).
3. **Test wire-ins** — any acceptance/smoke test that writes a top-level dir → redirect under `runs/`.
4. **Re-verify** — a full happy-path re-run must stay GREEN *and* produce a quiet `git status` (that's the acceptance criterion).
5. **CLAUDE.md maintenance rhythm** — add one line to the Monthly list: *"reconcile the project-prime untracked tree — gitignore run scratch, commit forgotten fixtures."* Cheap insurance for whatever escapes the convention.

## Decisions banked — do NOT re-litigate

- **Location-based (route under `runs/`) over pattern-globs.** Least fragile — the infra already exists; globs (`*-run/`) need per-scheme upkeep and risk swallowing a legit future dir.
- **Frozen core stays frozen.** Changing *where* runs write must NOT change pipeline behavior or break a green run — verify with a re-run before committing. STOP-and-surface if a wrapper needs restructuring.
- **The symptom is already cleared** (`b375f39`): 5 run-output trees + 2 stray artifacts ignored, `runs/.gitkeep` / `docs/.gitkeep` activated, 17 forgotten recipe fixtures committed. This session is *prevention*, not cleanup.

## The prompt to paste

```
Durable fix for project-prime run-output git-noise. Read
handoffs/Next_Session_Prompt_RunOutput_Convention.md in full first.

Goal: every demo/run writes under the already-ignored runs/<name>/ instead of ad-hoc
top-level dirs, so `git status` stays quiet by construction. run_happy_path.sh has NO
OUTDIR default today (verified) — add a runs/-rooted default (keep the positional
override); do the same for the async pipeline + any test that writes a top-level dir.
Frozen core: this changes WHERE runs write, never pipeline behavior — re-run the full
happy path GREEN and confirm a quiet git status as the acceptance test before committing.
Add one Monthly line to CLAUDE.md: reconcile the untracked tree. Then DoD sync + push.

Today's symptom tidy already landed (b375f39); this is prevention, not cleanup.
```

## Cross-links

- [[Definition_of_Done]] — the discipline whose untracked-tree blind spot this closes.
- [[claude-harness-statusline-hooks]] — the Stop-hook (nudges on uncommitted/unpushed, not untracked).
- [[Dev_Log]] entry 2026-06-26 (cont. 5) — the housekeeping session that cleared the symptom + banked this.
