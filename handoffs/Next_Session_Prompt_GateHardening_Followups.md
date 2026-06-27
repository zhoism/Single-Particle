---
tags: [project-prime, code-review, gates, test-quality, session-handoff]
type: handoff
status: ready
created: 2026-06-27
scope: non-blocking-hardening
---

# Next Session — Gate-hardening follow-ups from the 2026-06-27 independent code review

> **Non-blocking.** The 2026-06-27 second-pass review of the gate work
> (project-prime `b375f39..fee1fbe`, 4 skills) returned **PASS** — zero HIGH, zero MED,
> all 14 surviving findings LOW/INFO (see [[Next_Session_Prompt_CodeReview_Parallel_Sessions]]
> Outcome + [[Dev_Log]] 2026-06-27). Nothing here gates a merge; these are durability /
> test-quality / doc-accuracy nits worth a small focused pass. **All are in passing code** —
> each task is test-first, `RED→GREEN` on that skill's oracle, then commit→review→push.

## Why these exist (the through-line)

The review's recurring theme: a couple of the new gates are **pinned only against synthetic
fixtures** and one FATAL gate is a **log-scrape that fails OPEN** — i.e. a future teLeap/AMBER
format drift could silently neuter a gate *in the safe direction*, which is exactly the class
(`SYSTEM_NOT_NEUTRAL` shipped vacuous) [[Gap_Gate_Coverage]] exists to fight. None false-fire
today (empirically re-verified: 0 `bond of` in 17 real leap.logs; water 1890–8290 in 47 real
`comp_oct.top` ≫ floor 100). These tasks make the PASS *durable*.

## Tasks (each independently shippable; ranked)

1. **`mdin-edit` — close the mutation-test hole on the `needs_human` halt (LOW, highest value).**
   The new coherence gate has thorough *acceptance* coverage (cases 5d–5k, no-write asserted by
   `diff`), but **no mutation mutant** and every current mutation-slice fixture is now coherent —
   so a mutant that deletes `if pre_mismatch and couple_mode is None: return needs_human`
   (`skills/mdin-edit/scripts/wrapper.py:497`) would **survive** the mutation suite. Add a
   pre-mismatched synthetic slice fixture to `tests/mutation_test.py` + a halt-deletion mutant so
   the suite kills it. This is the most safety-critical new code; make its coverage match its
   importance.

2. **`tleap-build` — `CROSS_GAP_SPURIOUS_BOND` durability (LOW) + `\b` anchor (INFO).**
   It is a log-scrape that **fails open** on a teLeap reword of `"There is a bond of N angstroms"`
   (`wrapper.py:291-294, 404-411`). Currently correct (real-fixture canary `test_parse_leap_log_real_fixture`
   pins the format; oracle 72/72). Preferred hardening: compute bond lengths **structurally** from
   the prmtop `BONDS_*` block + the `.crd` coords (the "structural > log-scrape" lesson) and keep
   the log-scrape as a secondary signal; otherwise keep the canary as the durability guard. Trivial
   adjacent nit: anchor the regex `\bbond of` so it can't match `"rebond of 9.9 angstroms"`
   (defensive only — no real line triggers it; re-run the oracle to confirm the `[4.084]` fixture
   still captures).

3. **`cpptraj-analysis` — commit a real-format `prmtop` fixture for `prmtop_radius_set` (LOW) +
   trim a wrong comment (INFO).** The radius-set parser is pinned only against *synthetic*
   `RADIUS_SET` lines (`tests/test_engine.py`), so a future AMBER prmtop-layout drift could make the
   regex return `None` and **silently stop the detector firing** (safe direction). Add a **small
   committed** real-format prmtop excerpt fixture (NOT a pointer to `golden-path/.../comp_dry.top` —
   that's gitignored). Also fix the inaccurate code comment at `wrapper.py:69-71`: it claims
   `mbondi3` carries a parenthetical `(Bondi2)` aside, but the real line
   `"ArgH and AspGluO modified Bondi2 radii (mbondi3)"` has **Bondi2 unparenthesized** — only
   `mbondi2`'s `H(N)` is a genuine multi-paren case (the last-paren logic is correct regardless).

4. **`plip-profile` — re-scope the "zero regression" claim (INFO, doc/verification).** "Identical
   interaction counts with vs without `--nohydro`" is an **empirical 2-frame result** (1L2Y + 3HTB
   medoids), not a static invariant — by the code's own mechanism, switching to tleap-H *can*
   legitimately shift H-bond calls vs the pre-`f188b79` baseline on **other** targets (this is more
   physically correct, and the path is non-fatal, so it's not a bug). Scope the wording in
   `wrapper.py:386-393` to the two tested frames and re-confirm when a new-target baseline is first
   set. (Optional same-file nits: the salt-bridge comment overstates H-geometry sensitivity; the
   `build_plip_cmd` post-build missing-flag guard is provably dead — harmless backstop, the real
   tripwire is `test_build_plip_cmd`'s tuple-equality assert.)

5. **`mdin-edit` — correct the parser-scope wording in `references/mdin-params.md` (INFO, doc).**
   Lines ~119–121 mischaracterize the [[Gap_Gate_Coverage]] parser-scope gap: a `d`-exponent
   `value2` actually **trips** the gate (it does not "fall through ungated"), and the vendored
   `check_amber` validator **reads double-quoted `"TEMP0"` while the gate does not** (the validator
   is *broader*, not "same scope"). The Gap note already states this accurately — align the doc to
   it. Pure doc; zero production impact (advisor format is single-quoted plain-decimal).

6. **Test-infra hygiene (INFO).** The mdin mutation/acceptance harness hardcodes bare `python3` and
   a persistent shared scratch dir, which produced one non-reproducible baseline flake under an
   interpreter mix during the review. Pin the interpreter (conda py3.11) and isolate scratch per
   run.

## Done =
Each task `RED→GREEN` on its skill's oracle/`test_acceptance.sh`, committed (one commit per skill is
fine), `/code-review`'d, pushed to `project-prime` `main`, with a [[Dev_Log]] marker. Tasks 1–3 are
the ones with real durability value; 4–6 are accuracy/hygiene. Flip this handoff `status: ready →
consumed` with an Outcome line when done.

## Prompt to paste

```
Gate-hardening follow-ups from the 2026-06-27 code review (PASS, no blockers) in the project-prime
repo (github.com/zhoism/Single-Particle-pipeline, local ../project-prime/). Read
handoffs/Next_Session_Prompt_GateHardening_Followups.md for the full task list + locations. These
are LOW/INFO durability + test-quality + doc-accuracy nits on PASSING code — test-first each one
(RED→GREEN on the skill's oracle), commit per skill, /code-review, push, Dev_Log. Priority order:
(1) add a pre-mismatched mutation mutant so a deleted needs_human halt is killed; (2) tleap CROSS_GAP
structural-or-canary durability + \b regex anchor; (3) commit a real-format prmtop fixture for
cpptraj prmtop_radius_set + fix the mbondi3 comment; (4) re-scope plip "zero regression" wording;
(5) correct mdin-params.md parser-scope wording; (6) pin the test interpreter + isolate scratch.
Then flip this handoff to consumed.
```
