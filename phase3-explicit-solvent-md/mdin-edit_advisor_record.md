---
name: mdin-edit-advisor-record
description: "Record & summary for the advisor's parameter-editing task: a natural-language Agent Skill (mdin-edit) that changes one parameter in one stage (or a stage group) of the pre-prepared explicit-solvent AMBER mdin set, then submits the job — demonstrated end-to-end on the provided files, with each change logged and each mistake-avoidance mechanism proven live."
license: MIT
homepage: https://github.com/zhoism/Single-Particle
metadata: {"skill":"mdin-edit","skill_source":"project-prime/skills/mdin-edit","skill_commit":"7b89568","demonstrated":"2026-06-11","model":"google/gemini-3-flash-preview","inputs":"phase3-explicit-solvent-md (10-stage pmemd chain)","tasks":["understand-inputs","nl-edit","extend-temp0-cut-restraint","record-summary"],"verdict":"PASS"}
---

# mdin-edit — Advisor Task Record

**What this is.** The advisor asked for an Agent Skill that edits AMBER `mdin` parameters from natural language, then submits the job — and a summary of whether each change succeeds and how the skill avoids mistakes. This document records that, demonstrated end-to-end on the provided `phase3-explicit-solvent-md/` set on **2026-06-11**.

**How it was run.** The skill is `mdin-edit` (`project-prime/skills/mdin-edit`, commit `7b89568`). An OpenClaw agent (`google/gemini-3-flash-preview`) reads the English request and maps it to structured arguments; a deterministic Python wrapper does the actual edit — the LLM never writes the file. Every edit ran on a **copy** under `_demo-work/`; the 10 original `.in` files are byte-identical to their session-start checksums.

---

## The advisor's task (verbatim)

> 1. **Understand the input file structure** — go through the mdin files (min, heat, press, relax, prod) and key parameters like `dt`, `cut`, etc. (Amber26 §23.6).
> 2. **Modify parameters using an Agent Skill** — specify which stage and which parameter to modify in natural language (e.g. "set the time step to 0.001 ps in the first heating stage"), then submit the job.
> 3. **Extend** to: "set the target temperature to 310 K" (temp0 in all stages from the third onward — heat-3, press-3, relax, prod); "set the non-bond cutoff to 7.0 Å" (cut); "relax the positional restraints from 5.0 to 1.0 in a specific heating/pressurization stage" (restraint_wt).
> 4. **Record and summarize** — log whether each change succeeds and how the skill avoids mistakes (bounds checking, stage-aware targeting). The goal is a skill that edits correctly and predictably, no matter how many times it is used.

---

## Task 1 — Understanding the inputs (§23.6-grounded)

Chain order (`submit.sh`): `min1 → min2 → heat-1 → press-1 → heat-2 → press-2 → heat-3 → press-3 → relax → prod`. Heat/press interleave: heat to a target at constant volume (NVT), then pressurize at that temperature (NPT). Values below were read directly from the files.

| Stage | imin | dt | cut | temp0 | ntr·restraint_wt | `&wt` TEMP0 ramp |
|---|---|---|---|---|---|---|
| min1 | 1 | — | 9.0 | — | 1·5.0 | — |
| min2 | 1 | — | 9.0 | — | 0·0.0 | — |
| heat-1 | 0 | 0.002 | 9.0 | 100 | 1·5.0 | 5→100 |
| press-1 | 0 | 0.002 | 9.0 | 100 | 1·5.0 | — |
| heat-2 | 0 | 0.002 | 9.0 | 200 | 1·5.0 | 100→200 |
| press-2 | 0 | 0.002 | 9.0 | 200 | 1·5.0 | — |
| heat-3 | 0 | 0.002 | 9.0 | **300** | 1·5.0 | 200→**310** ⚠️ |
| press-3 | 0 | 0.002 | 9.0 | 300 | 1·5.0 | — |
| relax | 0 | 0.002 | 9.0 | 300 | 0·0.0 | — |
| prod | 0 | 0.002 | 9.0 | 300 | 0·0.0 | — |

**Parameter meanings (Amber26 §23.6).** `imin=1` = minimization (no `dt`/thermostat — editing those there is invalid). `dt` = integration step (ps); SHAKE (`ntc=2,ntf=2`) caps it at **2 fs**. `cut` = real-space non-bonded cutoff (Å); under PME the long-range electrostatics are handled in reciprocal space, so a 7 Å cut is aggressive but valid. `temp0` = target temperature, but during heating the thermostat follows the ramped `&wt TEMP0 value2`, so **`temp0` must equal the ramp end**. `ntr=1`+`restraint_wt` pin solute heavy atoms (mask `!:WAT,Cl-,K+,Na+ & !@H=`) through min/heat/press, then release for relax/prod.

⚠️ **The heat-3 footgun:** `temp0=300` but the ramp ends at `310` — a 10 K disagreement. The advisor's "set temp to 310 from the third stage onward" resolves it, and the skill's `temp0↔value2` coupling guarantees they cannot silently drift apart again (see edit b).

A fuller §23.6 write-up lives at `project-prime/skills/mdin-edit/references/mdin-params.md`.

---

## Tasks 2 + 3 — The four edits (natural-language driven, verified)

Each edit was issued to the agent in the advisor's English (no `--stage/--param/--value` supplied — that mapping is what's under test), and the agent's result was **byte-compared to a deterministic CLI baseline**. All four matched byte-for-byte.

| # | Natural-language instruction | Agent-resolved command | Result | NL == CLI |
|---|---|---|---|---|
| a | "set the time step to 0.001 ps in the first heating stage" | `--stage heat-1 --param dt --value 0.001` | `heat-1.in`: `dt 0.002→0.001` (one line) | ✔ byte-identical |
| b | "set the target temperature to 310 K in all stages from the third stage onward" | `--stage group:third-onward --param temp0 --value 310` | `heat-3, press-3, relax, prod`: `temp0 300→310`; on `heat-3` the `&wt value2` is coupled to 310 — **mismatch resolved**; `heat-1/press-1` untouched | ✔ byte-identical |
| c | "set the non-bond cutoff to 7.0 Å across all stages" | `--stage group:all --param cut --value 7.0` | all 10 files `cut 9.0→7.0`; advisory **WARN** (7.0 < 8 Å solvent floor) but `ok:true` | ✔ byte-identical |
| d | "relax the positional restraints from 5.0 to 1.0 in the first pressurization stage" | `--stage press-1 --param restraint_wt --value 1.0` | `press-1.in`: `restraint_wt 5.0→1.0`; `restraintmask` line intact | ✔ byte-identical |

**Read-back before every edit.** Each NL edit (and each CLI baseline) was previewed with `--dry-run`, which prints the exact file(s), `namelist.param`, and `old→new` it *would* write — the "I am about to change `dt` in `heat-1` — correct?" gate the advisor's review asked for — before anything is written. Every applied change is appended to `<md-dir>/mdin-edit.log` (`{timestamp, file, namelist.param, old → new}`).

### Submit ("then submit the job")

All four edits were applied to a single copy, then run with `--submit --reduce-nstlim 120`: the wrapper rewrites the advisor's hard-coded `AMBERHOME` to the local toolchain on its own scratch, reduces the step count, and runs the full `min1…prod` chain restart-chained.

- **10 / 10 stages reached normal termination** (`rc=0`, no "Terminated Abnormally", non-empty `.rst7`), final `prod.rst7` produced.
- The working directory was **not mutated** (scratch-only).
- This proves the fully-edited set is **runnable** — a **Run-GREEN**, *not* a scientific result (120 steps is a smoke, not the 10 ns production protocol; see Limitations).

---

## Task 4 — How the skill avoids mistakes (proven live)

The skill's guarantees (`SKILL.md` §"Guarantees", `references/heuristics.md`) were each demonstrated, not just asserted:

| Mechanism | What it prevents | Proof |
|---|---|---|
| **Hard bounds, reject-before-write** | An out-of-range value reaching a file | `temp0→600` → `ok:false OUT_OF_BOUNDS` (`0 < temp0 ≤ 400 K`); file byte-identical |
| **Byte-compare vs intended baseline** | A *mis-mapped but in-bounds* edit ("perfectly wrong") | A valid `dt=0.001` deliberately placed in `heat-2` instead of `heat-1` — the byte-compare to the intended baseline **failed loudly**, catching it |
| **`--dry-run` read-back** | Editing the wrong thing unseen | Every edit previewed the resolved file/param/old→new before writing |
| **Idempotent parse-replace** | Drift / duplication on re-runs | Re-running an applied edit → `status:"unchanged"`, byte-identical (no-op) |
| **Stage-aware targeting** | Appending a param where it doesn't belong | `dt` on `min1` (a minimizer) → `ok:false PARAM_NOT_FOUND`, nothing appended |
| **`temp0 ↔ &wt value2` coupling** | The thermostat target silently disagreeing with the ramp end | heat-3 `temp0` and `value2` both 310 after edit b — the documented footgun resolved |
| **Advisory validation + deliberate WARN** | Silently accepting *or* silently blocking a borderline value | `cut=7.0` accepted with a transparent "below 8 Å floor" WARN (PME covers long-range), `ok:true` |
| **Post-edit self-check + atomic write** | A half-written or wrong-span edit reaching disk | re-parse-and-assert before `os.replace`; all-or-nothing batch |

**Regression suites (re-run this session, both green):** `test_acceptance.sh` — 12/12 cases (malformed, golden, idempotency, out-of-bounds, wrong-param, group temp0 + coupling, cut WARN, restraint_wt + ntr=0 skip). `tests/submit_acceptance.sh` — `--submit` dry-run + real run (10/10 normal termination, `--md-dir` untouched).

---

## Limitations (honest)

- **Residual mis-map risk.** The hard bounds catch an out-of-*range* value, but they cannot catch a *mis-mapped-but-in-bounds* edit (a valid `dt` in the wrong stage). The defenses are the `--dry-run` read-back and the byte-compare to an intended baseline (both demonstrated above); in production NL use, surfacing the read-back to a human before committing is the right gate. Note a naïve "assert temp0 ∈ 200–500 K" guard would be **wrong here** — `heat-1` legitimately targets 5 K and ramps up, so a 200 K floor would reject the real heating stages; the correct envelope is the existing `0 < temp0 ≤ 400 K`.
- **Scale.** The stage map and `group:*` selectors are hard-coded to this 10-stage chain, and `--submit` runs the stages serially. For 100+ files or branched workflows this editor is the wrong tool — that is the job of a planning layer (arbitrary stage graphs) and remote dispatch (queue a long chain to a cluster rather than smoke it locally), which are separate, not-yet-built components.
- **Run-GREEN ≠ science.** A green `--submit` means pmemd executed the edited files to normal termination with no NaN. It is not a claim that the simulation is physically converged.

---

## Reproduce

```bash
WRAP="project-prime/skills/mdin-edit/scripts/wrapper.py"
CP="phase3-explicit-solvent-md/_demo-work/<a-copy>"     # always operate on a COPY

# the four edits (each previewable with --dry-run first)
python3 "$WRAP" --md-dir "$CP" --stage heat-1            --param dt           --value 0.001
python3 "$WRAP" --md-dir "$CP" --stage group:third-onward --param temp0        --value 310
python3 "$WRAP" --md-dir "$CP" --stage group:all          --param cut          --value 7.0
python3 "$WRAP" --md-dir "$CP" --stage press-1            --param restraint_wt --value 1.0

# submit the edited set (reduced-step smoke)
python3 "$WRAP" --md-dir "$CP" --submit --reduce-nstlim 120

# natural-language drive (one exec call → wrapper.py)
openclaw agent --agent main --json --message \
  "The mdin set is in <dir>. Using the mdin-edit skill, set the time step to 0.001 ps in the first heating stage."

# suites
bash project-prime/skills/mdin-edit/test_acceptance.sh
bash project-prime/skills/mdin-edit/tests/submit_acceptance.sh
```

## Evidence ledger

- Skill: `project-prime/skills/mdin-edit` @ `7b89568`. Engine: `scripts/wrapper.py` (pure-Python, stdlib only). Validation bounds vendored from `check_amber`.
- NL drive: `google/gemini-3-flash-preview` via the local OpenClaw gateway; 5–16 s / turn. All four agent edits byte-identical to the CLI baselines.
- Submit: 10/10 stages normal termination, final `prod.rst7`, `--md-dir` unmutated.
- Suites: `test_acceptance.sh` 12/12; `tests/submit_acceptance.sh` dry-run + real run green.
- Integrity: all 10 original `.in` files byte-identical to session start; edits confined to `_demo-work/`.

**Verdict: PASS** — the skill modifies `dt`, `temp0` (with ramp coupling), `cut`, and `restraint_wt` from natural language, stage-aware and bounds-checked, idempotently, and the edited set runs; mistake-avoidance mechanisms demonstrated, limitations stated.
