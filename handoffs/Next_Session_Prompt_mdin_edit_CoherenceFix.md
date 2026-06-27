---
tags: [project-prime, mdin-edit, session-handoff, coherence-fix, needs-human]
type: handoff
status: ready
created: 2026-06-26
---

# Next Session Starter — mdin-edit coherence fix + needs_human confirm

> Created 2026-06-26 after the heat-3 typo was resolved (the vault demo is now coherent `300/300`). `mdin-edit`'s test suite has exactly **one** failing guard, plus a confirm-gate enhancement to add. Two phases: **Phase 1** unblocks the tests (small surface), **Phase 2** adds the `needs_human` gate the user wants to run with. Paste the block in §The prompt to paste into a fresh Claude Code session (run from the vault). EXECUTION handoff — split out because the originating session's context was high.

## Recap (what's done — don't re-discover)

- **heat-3 resolved** — `phase3-explicit-solvent-md/heat-3.in` is coherent `temp0=300 / &wt value2=300` (vault commit `51e15c1`). The advisor's original `value2=310` was a **typo**, confirmed by the user — NOT a deliberate fixture. Memory [[phase3-advisor-demo]] already corrected.
- **Repos clean** — both on `main`, pushed. **project-prime advanced `79b0a43`→`b375f39`** (2026-06-26 housekeeping: gitignored ad-hoc run-output + committed forgotten golden-path/smoke-test recipe fixtures — `git status` is now **clean**, *not* the 384-untracked noise earlier sessions saw). The audit branch merged (`fb6c1a9`) + was deleted. `mdin-edit` itself is UNCHANGED. *(vault HEAD also advanced this session — `git log` for the latest.)*
- **Diagnosis was verified by RUNNING (not trusting the Dev_Log)** — `test_acceptance.sh`: all 14 cases PASS (it edits `temp0→310`, the coupling forces `value2→310`, and asserts the END state, so it's robust to the demo). `oracle_selftest.py`: 21 pass / **1 fail**. The single failure is `tests/oracle.py:339-342` `_verify_ground_truth` — it asserts "the famous heat-3 mismatch must still be there" and raises `GROUND-TRUTH DRIFT` when `temp0==value2`. It's a drift-canary that fired correctly.
- **Blast radius** — that guard is consumed at module scope by `tests/mutation_test.py:32` and `tests/fuzz_mdin_edit.py:156` (`GT = O.load_ground_truth()`), so BOTH crash at startup too. Fixing the one guard unblocks all three.
- **needs_human** — the pattern is shipping in `amber-recover/scripts/wrapper.py` (10 uses); `mdin-edit` does NOT have it (its envelope is only `ok`/`errors`/`warnings`/`verdict`). Phase 2 ports it, doesn't invent it.

## ⚠️ Concurrency heads-up (added 2026-06-26)

This session edits `skills/mdin-edit/tests/oracle.py` + docs. The **`ntx_irest` encoding handoff also touches `skills/mdin-edit/`** (its diverged `scripts/check_amber_vendored.py`) — *different files, same dir / repo / branch*. If the two run concurrently: **isolate this one in a project-prime `git worktree`** on its own branch, stage only mdin-edit files by path, and **serialize the memory writes** — a `git worktree` does **not** isolate memory (`project_prime_status.md` lives outside git at a fixed path, so concurrent writes clobber). Run solo? Just work on `main`.

## Decisions banked — do NOT re-litigate

- **Demo stays coherent `300/300`** — do NOT reintroduce the `300/310` mismatch to "fix" the tests. The fix is in the tests/docs, not the demo.
- **Flip the guard, don't delete it** — `oracle.py:339-342` is a working anti-drift canary. Change its expectation (must be COHERENT), keep the protection.
- **`needs_human` envelope, NOT an interactive prompt** — Discord is send-only; a mid-job blocking read would deadlock the `exec` tool / detached pipeline / `md-planner` / the ~240k-assertion harness. Same call as [[Future_Work_Run_Confirmation_Gate]]. The human re-invokes with a flag; the notifier just relays the message.
- **Hermetic tests own their fixtures** — the root cause was a test depending on the external mutable demo file. Demonstrate "repair a mismatch" with a SYNTHETIC in-test fixture (`oracle_selftest.py`'s `CNTRL` constant, lines 47-63, is already one).
- **Single `TEMP0` card per stage is current scope** — `wrapper.py:183 temp0_wt_span` returns the first card. Multi-card is [[Future_Work_mdin_edit_Arbitrary_Shapes]], not this session.

## What's NOT done (deferred, non-blocking)

- **mdin-edit for arbitrary mdin shapes** — stage-name-agnostic + multi-card `TEMP0`. Separate [[Future_Work_mdin_edit_Arbitrary_Shapes]] (candidate).
- **`--couple` / `--keep-value2` CLI flags** — new surface added in Phase 2; document them in `SKILL.md`.

## The prompt to paste

```
Continuation of mdin-edit — coherence fix + needs_human confirm. heat-3 is now coherent 300/300 (advisor's 310 was a typo); the test suite has ONE failing guard plus a confirm-gate to add. Two phases, build test-first.

Read these BEFORE acting (in order):
- vault: handoffs/Next_Session_Prompt_mdin_edit_CoherenceFix.md (this handoff — the full plan + banked decisions)
- vault: Definition_of_Done.md (the sync set you'll apply at the end)
- memory: phase3-advisor-demo (the heat-3 typo resolution), mdin_edit_advisor_feedback
- code: project-prime/skills/mdin-edit/tests/oracle.py (the guard), tests/oracle_selftest.py, test_acceptance.sh; and amber-recover/scripts/wrapper.py (the needs_human pattern to PORT)

Decisions banked, do NOT re-litigate (see this handoff's "Decisions banked" section):
- Demo stays coherent 300/300 — do NOT reintroduce the mismatch.
- Flip the oracle.py guard, don't delete it (anti-drift canary).
- needs_human envelope, never an interactive/blocking prompt.
- Hermetic test fixtures; single TEMP0 card per stage is current scope.

Immediate sequence (mdin-edit ONLY — do NOT touch other skills):

1. PRE-FLIGHT (~5 min):
   a. Both repos clean + on main + pushed: git -C <vault> status, git -C <project-prime> status.
   b. Reproduce the failure (prime-amber python): run tests/oracle_selftest.py → expect 21 pass / 1 fail (GROUND-TRUTH DRIFT: heat-3 ... already equal). Run bash test_acceptance.sh → expect all 14 PASS.
   c. Confirm heat-3.in is 300/300 in the vault demo (grep temp0/value2 phase3-explicit-solvent-md/heat-3.in).

2. PHASE 1 — unblock (test-first, small surface):
   a. FLIP oracle.py:339-342: change the "heat-3 must be MISMATCHED (temp0 != value2)" assertion to "must be COHERENT (temp0 == value2)" with a clear comment. Re-run oracle_selftest + mutation_test + fuzz (prime-amber python) → all green.
   b. Add a HERMETIC repair-demonstration: a synthetic in-test fixture with temp0=300, value2=310, edit temp0→310, assert the engine couples value2→310 (repairs it). Owns its input; never reads the demo. (oracle_selftest.py's CNTRL is the model.)
   c. FIX DOCS — rewrite the false "advisor wanted 310" narrative to "the 310 was a typo; heat-3 is coherent 200→300; mdin-edit keeps temp0/value2 coherent on edit": references/mdin-params.md:32,97-103, SKILL.md:70-78,247, tests/README.md:70.

3. PHASE 2 — add the needs_human confirm gate (PORT from amber-recover):
   - When editing temp0 and &wt value2 was ALREADY incoherent (pre-existing mismatch): do NOT silently auto-couple. Emit a needs_human envelope, write NOTHING, require re-invocation with --couple (set value2 to match) or --keep-value2 (preserve the mismatch).
   - When value2 was already coherent: keep coupling silently (no ambiguity).
   - Write oracle/acceptance cases first: pre-existing-mismatch → needs_human (no write); --couple → coheres; --keep-value2 → temp0 only; coherent-start → silent couple. Then implement. Document --couple/--keep-value2 in SKILL.md.
   - Adversarial review (Definition_of_Done §4 / feedback-verify-and-eval) before committing.

4. CLOSING (Definition_of_Done sync set):
   a. Phase3_Taskboard_Manifest.md if stage state moved; MAP.md.
   b. devlog-append skill: log the session.
   c. memory: update mdin_edit_advisor_feedback / project_prime_status + MEMORY.md pointer.
   d. commit (stage only mdin-edit files by path; never git add -A) → independent review → push, BOTH repos as applicable.
   e. Flip THIS handoff frontmatter status: ready → consumed; add an Outcome footer.

Stop conditions:
- If flipping the guard does NOT make mutation_test + fuzz green, STOP — there's a second dependency; investigate before proceeding.
- If Phase 2's needs_human would require touching the multi-card path, STOP — that's out of scope (Future_Work_mdin_edit_Arbitrary_Shapes).

Scope-fence: mdin-edit ONLY. Do NOT extend to arbitrary mdin shapes, the editable-param whitelist, or other skills.
```

## After the session — update this file

1. Flip frontmatter `status: ready` → `status: consumed`.
2. Add: `## Outcome\n\nConsumed YYYY-MM-DD. <1-sentence outcome>. See [[Dev_Log]] entry YYYY-MM-DD.`
3. If only Phase 1 shipped (Phase 2 deferred), flip to `status: partially-consumed` and note what remains.

## Cross-links

- [[Dev_Log]] entry 2026-06-26 — the session that produced this handoff (the mdin-edit design discussion + code verification).
- [[Future_Work_mdin_edit_Arbitrary_Shapes]] — the deferred multi-card / stage-name-agnostic expansion.
- [[Future_Work_Run_Confirmation_Gate]] — the sibling "interactivity belongs at the agent layer, not in the skill" decision.
- [[Research_Advisor_Feedback_mdin_edit]] · memory [[phase3-advisor-demo]] · [[mdin-edit-advisor-feedback]].
