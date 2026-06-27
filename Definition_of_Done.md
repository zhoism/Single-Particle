---
tags: [project-prime, process, meta, definition-of-done]
type: process
status: active
---

# Definition of Done

*Vault-root meta-doc (joins [[Dev_Log]], `vocabulary.md`, [[MAP]], `CLAUDE.md`). The canonical, finite list of what "update all status documents" means, so it's a checklist rather than a vibe. Why this exists: the vault + auto-memory **are** the deliverable, so the main failure mode is **drift** — work happens but the record doesn't catch up. The 2026-06-24 drift-audit and 2026-06-19 re-assessment together caught ~26 such inconsistencies. Banked rule: [[feedback-sync-memory-status-docs]]; pairs with [[feedback-verify-and-eval]] + [[dev-log-convention]] + [[feedback-autonomous-vault]].*

---

## 1. What triggers a full sync

A **substantive result** — anything that changes project state:

✅ **Triggers** — a build/skill landed · a decision banked · an assessment/teardown · a failure-mode finding · a report drafted · a gate fixed · a scope change.

🚫 **Does not trigger** — a question answered · a typo/formatting fix · read-only exploration · work that was started then abandoned.

When in doubt, treat it as substantive. A no-op Dev_Log entry is cheaper than silent drift.

---

## 2. The sync set (do these in ONE pass, per result)

Not done until all of these that apply are current — same pass as the work, not an afterthought:

1. **Memory file** — write/update the relevant file in `~/.claude/projects/-Users-kevinzhou-Downloads-Single-Particle-Single-Particle/memory/` (and `project_prime_status.md` for live project state). *Outside git — kept current by discipline, never committed.*
2. **MEMORY.md index** — add/update the one-line pointer for any memory file touched.
3. **Canonical vault note** — the topical note per the [[CLAUDE]] taxonomy (`Research_*`/`Gap_*`/`Design_*`/`Arch_*`/…). Update **frontmatter `status:` + dates** on every note touched, not just the body.
4. **[[Dev_Log]] entry** — reverse-chron marker + pointers (not a duplicate of the work). See [[dev-log-convention]].
5. **Status fields that the result moved** — `Gap_*` `status:`, `handoffs/` `status:`, `Phase3_Taskboard_Manifest` stage state, `Project Prime.md` roadmap if scope changed.
6. **[[MAP]]** — refresh done/in-flight/blocked if the result changed the high-level picture (otherwise leave for the weekly pass).
7. **Commit → review → push** (§4).

---

## 3. Status-document inventory (the source of truth for "what tracks state")

| Doc | Path | Tracks | Cadence |
|---|---|---|---|
| Auto-memory files + index | `~/.claude/projects/…/memory/*.md` + `MEMORY.md` | durable facts / decisions | per result (outside git) |
| `project_prime_status.md` | memory dir | long-form live project state | per result |
| [[Dev_Log]] | vault root | time-ordered session trail | per session |
| [[MAP]] | vault root | high-level done / in-flight / blocked | weekly + on big shifts |
| `Project Prime.md` | vault root | canonical roadmap entry point | on scope change |
| `Gap_*.md` | vault | open problems + `status:` | on change |
| `handoffs/README.md` + `Next_Session_Prompt_*` / `Future_Work_*` | `handoffs/` | forward queue + `status:` | on change |
| `Phase3_Taskboard_Manifest.md` | vault | stage build state | on stage change |
| Reports / audits (`Implementation_Summary_*`, `Market_Landscape_*`) | vault | deliverable snapshots | ad-hoc |
| `vocabulary.md` | vault root | controlled term list | when a new term appears |
| project-prime `Dev_Log` / `README` / `FEATURES.md` / skill `references/` | `../project-prime/` | code-side state | per code result |

---

## 4. Commit → review → push protocol

Scope: **both repos** — the vault (`zhoism/Single-Particle`) and the code repo `../project-prime/` (`zhoism/Single-Particle-pipeline`). Both private + solo, so push is low-stakes and reversible — but every commit gets one independent review before its push.

1. **Commit** when a substantive result is complete and its sync set is landed. Don't push in the same breath.
2. **Review each commit independently before pushing it** (the [[feedback-verify-and-eval]] discipline):
   - **Code repo** → `/code-review` on the commit diff; fix-or-accept the findings.
   - **Vault** → a consistency pass on the diff: frontmatter `status:`/dates correct, `[[wikilinks]]` resolve, no contradiction introduced vs other notes, no stale claim (commit hash / model / ΔG) reintroduced.
3. **Push** after review. (`git push` is wired to prompt in `~/.claude/settings.json` — that prompt is the review-gate moment.)

Git is reversible: a bad push is fixable. The gate is about catching drift, not gatekeeping.

---

## 5. Cadence checklists

**Per result** — the sync set (§2) + commit/review/push (§4).

**Weekly**
- [ ] Refresh [[MAP]] (done / in-flight / blocked).
- [ ] Review `Gap_*` with `status: open` — has anything filled them?
- [ ] Scan `handoffs/README.md` — are the `status:` fields still accurate?
- [ ] Check `vocabulary.md` for drift (same concept under two names).
- [ ] Update the "Current focus" framing wherever it lives.

**Monthly**
- [ ] Prune notes with no inbound `[[wikilinks]]` that connect to nothing.
- [ ] Revisit `worth-revisiting: true` notes.
- [ ] Spot-check frontmatter dates vs body content; spot-check memory `description:` vs body for staleness.
- [ ] Confirm memory commit-hash / model / ΔG claims still match ground truth.

---

## 6. The Stop-nudge backstop (deterministic)

A user-scope `Stop` hook (`~/.claude/helpers/hook-handler.cjs`, wired in `settings.json`; recorded in [[claude-harness-statusline-hooks]]) is the safety net. A `SessionStart` hook snapshots each repo's `HEAD` + working-tree at session start (keyed by `session_id`); on stop, if **this session** left work that's uncommitted or unpushed in either tracked repo — **or**, in the vault, a commit lacking a `Dev_Log.md` entry — it **blocks the stop** with a short checklist. It compares against the session-start baseline, so the repo's chronic pre-existing dirt does **not** trigger it. Unpushed counts commits not on the tracking branch, or (for a no-upstream feature branch) not on `origin/main` — so review-before-push is caught even before a branch's first push.

It can't *write* the updates — only judgment can — but it won't let a session end with the bookkeeping silently undone. It's deliberately conservative and **dismissible** — it re-blocks at most **once per stop attempt**: a trivial commit that doesn't warrant the full sync is waved through by simply stopping again (`stop_hook_active` is honored, so a second stop always proceeds). No hard push block — review-before-push stays a discipline, reinforced by the nudge surfacing unpushed commits.
