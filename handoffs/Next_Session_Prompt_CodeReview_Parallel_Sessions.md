---
tags: [project-prime, code-review, quality-gate, session-handoff, parallel-sessions]
type: handoff
status: ready
created: 2026-06-27
scope: review-only
---

# Next Session — Independent code review of the 2026-06-27 parallel-session code

> **Small, focused review handoff.** Three sessions landed on 2026-06-27; **two shipped code** to `project-prime` and that code is the target. The **Hermes eval is OUT** (vault-only research, zero code) and so is the **graphify trial** (ran in an isolated throwaway corner — `project-prime` UNCHANGED). Each branch was adversarially reviewed *in-session* and merged — this is a **second, independent, fresh-eyes pass on the merged `main`**, which the per-branch reviews didn't see.

## Review surface (exact)

- **Repo:** `project-prime` (`github.com/zhoism/Single-Particle-pipeline`), local `../project-prime/`.
- **Range:** `b375f39..origin/main` (tip `fee1fbe`) — **6 commits, +935/−52, 15 files, 4 skills.**

```
2a6f05c  tleap-build: SOLVENT_NOT_ADDED + CROSS_GAP_SPURIOUS_BOND gates (P1, FATAL)   ← gates session
f188b79  plip-profile: require --nohydro in the PLIP argv (P1, determinism)            ← gates session
7582194  cpptraj-analysis: non-fatal GB_RADII_IGB_MISMATCH detector (P1)               ← gates session
174ca3f  mdin-edit: flip stale heat-3 coherence canary + correct docs                  ← mdin session
be656a4  mdin-edit: needs_human gate on pre-incoherent temp0/value2 (--couple/--keep)  ← mdin session
fee1fbe  Merge mdin-coherence-fix
```

## Look hardest at (highest-risk first)

1. **tleap-build's two new FATAL gates (`2a6f05c`)** — the load-bearing ones (FATAL = they can kill a real run).
   - `CROSS_GAP_SPURIOUS_BOND` is a **log-scrape** (`bond of N angstroms` > 3.0 Å). The vault's banked lesson is *structural > log-scrape* (the old `SYSTEM_NOT_NEUTRAL` was a vacuous log-scrape that silently stopped matching). Is the regex/threshold robust, and **can it false-fire on a legit production `leap.log`?** Is the committed `induced_cross_gap_leap_log.txt` fixture a faithful ground truth, or could gate+test be wrong together?
   - `SOLVENT_NOT_ADDED` (structural WAT-count ≥100) — correct count source; any false-fire on small/implicit-solvent systems?
2. **mdin-edit `needs_human` gate (`be656a4`)** — whole-batch **all-or-nothing HALT**, `--couple`/`--keep-value2` mutual exclusion, **temp0-only**, value2-only by design. Check the branch/flag/halt logic and that it writes nothing on HALT. The `174ca3f` canary flip also exposed a **py3.11 harness break** (`_read_raw` for `Path.read_text(newline=)`) — confirm py3.11+3.14 both clean. The known **parser-scope gap** (`d`-exponent / double-quoted `TEMP0` / non-finite) is banked as a *candidate* in `Gap_Gate_Coverage` — confirm it's genuinely pre-existing + validator-consistent, not a new regression.
3. **cpptraj-analysis `GB_RADII_IGB_MISMATCH` (`7582194`)** — intentionally **NON-FATAL** (the real `mbondi2` fix is deferred → `Next_Session_Prompt_GB_Radii_Fix`). Confirm the RADIUS_SET parse (last parenthetical) and that the detector can't false-fire or perturb MMPBSA output.
4. **plip-profile `--nohydro` (`f188b79`)** — determinism guard; confirm zero result regression on the real frames.
5. **Golden-path regression** — do any of these gates trip the real 1L2Y / 3HTB / 181L happy path? (In-session claim: GREEN, ΔG unchanged — verify, don't trust.)

## How to run it

The work is already on `main`, so materialize the range as one diff to feed `/code-review`:
```
cd ../project-prime
git switch -c review-scratch origin/main && git reset --soft b375f39   # 935 lines now staged vs base
/code-review high      # or: /code-review ultra   (deep multi-agent cloud pass)
git switch main && git branch -D review-scratch                        # discard scratch (main untouched)
```
Or just review `git diff b375f39 origin/main` directly with read-only subagents. Either is fine — the user said "code-review or just general review."

## Done =

A crisp **PASS / PASS-WITH-CONCERNS / FAIL** per [[Eval_Criteria]], findings ranked. **Fix any HIGH finding test-first** (red→green on that skill's oracle/`test_acceptance.sh`), commit + push to `project-prime` `main`, log in [[Dev_Log]]. If clean, say so plainly and note it — no busywork edits.

## Prompt to paste

```
Independent code review of the 2026-06-27 parallel-session code in the project-prime repo
(github.com/zhoism/Single-Particle-pipeline, local ../project-prime/). Review-only unless a
HIGH finding needs a test-first fix. SCOPE = the code-heavy work only:

  range: b375f39..origin/main (tip fee1fbe) — 6 commits, +935/-52, 4 skills
    2a6f05c tleap-build  SOLVENT_NOT_ADDED + CROSS_GAP_SPURIOUS_BOND (FATAL gates)
    f188b79 plip-profile --nohydro determinism guard
    7582194 cpptraj-analysis GB_RADII_IGB_MISMATCH (non-fatal detector)
    174ca3f + be656a4 mdin-edit  heat-3 canary flip + py3.11 fix + needs_human gate

OUT OF SCOPE: the Hermes eval (vault-only, no code) and the graphify trial (isolated corner,
project-prime unchanged). Each branch was already adversarially reviewed in-session and merged;
this is a fresh independent pass on the MERGED main.

Read handoffs/Next_Session_Prompt_CodeReview_Parallel_Sessions.md first (the per-commit risk list
+ the run recipe). Look hardest at: tleap-build's two new FATAL gates (esp. the CROSS_GAP log-scrape
false-fire risk — vault lesson is structural>log-scrape), the mdin-edit needs_human halt/flag logic
+ py3.11 cleanliness, the GB-radii non-fatal detector, and golden-path (1L2Y/3HTB/181L) regression.

Run /code-review (materialize the range via a review-scratch branch reset --soft to b375f39, per the
handoff), or review the diff range directly. Deliver PASS / PASS-WITH-CONCERNS / FAIL with ranked
findings; fix any HIGH test-first, commit+push, log in Dev_Log. Then flip this handoff to consumed.
```

## After the session
Flip `status: ready` → `consumed`, add a one-line `## Outcome` (verdict + any fixes/commits), drop it from the STATUS/README Ready lists into Consumed, and add a [[Dev_Log]] entry.
