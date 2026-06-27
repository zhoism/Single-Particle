---
tags: [project-prime, mdin-edit, future-work, flexibility, arbitrary-inputs]
type: future-work
status: candidate-not-started
created: 2026-06-26
---

🟡 **Scope-expansion candidate — deliberately not started.** Banked 2026-06-26 during the mdin-edit coherence-fix discussion. This is the "make `mdin-edit` flexible enough to edit *any* mdin set, not just the advisor's" idea. No code written.

# Future work: mdin-edit for arbitrary mdin shapes

## The idea

Today `mdin-edit` is a parameter editor for **the advisor's specific pre-prepared set**. To make it edit **arbitrary / pipeline-generated** mdin sets, it needs to stop assuming that one set's shape.

## The two hardcoded assumptions to lift

1. **Stage names are hardcoded** — the advisor's `min1, min2, heat-1..3, press-1..3, relax, prod`. The wrapper, the oracle's `STAGES`/`GROUPS` tables, and `group:third-onward`/`group:all` are all keyed to these exact names. An arbitrary set (different stage count/names, or pipeline-generated files) won't map. Needs **stage-name-agnostic discovery** — classify each `*.in` by its *contents* (min vs heat vs press vs prod via `imin`/`nmropt`/`ntb`/`ntp`/`&wt`), not its filename; let selectors be content-derived.
2. **Single `TEMP0` ramp card per stage** — `wrapper.py:183 temp0_wt_span` returns the **first** `&wt` block with `type='TEMP0'`; the coupling rewrites that card's `value2`. A **multi-card / piecewise** schedule (ramp → hold → ramp) breaks this: you'd want the **FINAL** card's `value2` to equal `temp0`, while **intermediate** cards' `value2` legitimately differ (they're waypoints — a `temp0 ≠ value2` is *correct* there). Needs multi-card handling: find the final TEMP0 card, couple that one, leave intermediates.

## Why it matters — "build AND use" inputs

The user wants the system flexible: *"able to build inputs, able to use created inputs."* The build side already exists — `tleap-build` + `amber-md-run` + `md-planner` **generate** leap/mdin for arbitrary targets (proven on 1L2Y / 3HTB / 181L). This note is the **consume** side: letting `mdin-edit` operate on those generated sets (or any hand-built set), not only the advisor's hand-shaped one. Closing this makes the param-editor as system-agnostic as the generators already are.

## Decisions banked (don't re-litigate)

- **Not the current coherence-fix session's scope** — [[Next_Session_Prompt_mdin_edit_CoherenceFix]] explicitly fences multi-card out. Do that first; this is the follow-on.
- **`temp0 ≠ value2` is legitimate for intermediate multi-card waypoints** — so the `needs_human` confirm gate (added in the coherence-fix session) must NOT fire on intermediate cards once multi-card lands; only on the final card / single-card incoherence. Keep that in mind when this is built.
- **Stays a deterministic, non-interactive wrapper** — same contract as today (no `input()`; `needs_human` envelope for ambiguity).

## Open questions to settle before starting

- Is there a real second mdin set to test against, or do we synthesize one? (Hermetic fixtures either way — see the coherence-fix handoff's Option-A principle.)
- Does content-based stage classification need to be exact, or is a "best-effort + `needs_human` on ambiguity" classifier acceptable?
- Scope: just temperature/restraint params on arbitrary shapes, or the full editable set?

## Prompt to paste (fresh session, when you decide to start)

```
Read Future_Work_mdin_edit_Arbitrary_Shapes and Definition_of_Done. Goal: make mdin-edit edit ARBITRARY mdin sets, not just the advisor's. Two lifts: (1) stage-name-agnostic discovery — classify each *.in by contents (imin/nmropt/ntb/ntp/&wt), not filename; (2) multi-card TEMP0 — couple the FINAL TEMP0 card's value2 to temp0, leave intermediate waypoints (temp0 != value2 is legitimate there). Build oracle-first / test-first with HERMETIC synthetic fixtures (never depend on the live demo). Keep the wrapper non-interactive (needs_human envelope). Do NOT let the needs_human coherence gate fire on intermediate multi-card waypoints. Then apply the Definition-of-Done sync set.
```

## Related

- [[Next_Session_Prompt_mdin_edit_CoherenceFix]] — do this first; it fences multi-card out.
- [[Next_Session_Prompt_mdin_edit_Whitelist]] — the other mdin-edit expansion (editable-param set); sibling scope.
- memory [[phase3-advisor-demo]] — the advisor's single set this skill was originally shaped to.
