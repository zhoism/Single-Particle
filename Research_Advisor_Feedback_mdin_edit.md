---
tags: [project-prime, amber, mdin-edit, advisor-feedback, physical-realism, research]
type: research
status: addressed
created: 2026-06-22
---

# ✅ Advisor feedback on `mdin-edit` — what it means, and how the skill now handles it

**Origin:** Advisor review of the `mdin-edit` natural-language parameter editor, received
2026-06-22. Four points — none were bugs in what shipped; all are *physical-realism* and
*data-safety* refinements. This note records the feedback accurately (not verbatim),
explains the underlying MD physics for each point, and states exactly how the skill was
changed in response. Code landed in `project-prime/skills/mdin-edit/`; verification in
[[Dev_Log]] (2026-06-22 entry). Companion to [[Research_AMBER_Failure_Modes]] and the
[[md-param-check]] validator; the SOP §3 limits it leans on are in `Eval_Criteria.md`.

> **Packaged for the advisor (2026-06-27):** this explainer is distilled into a quick report +
> the whole current skill code in `deliverables-mdin-edit-advisor-20260627/`
> (`Advisor_Report_mdin_edit.md` + `mdin-edit/` snapshot at project-prime `5d500b0`).

The 10-stage chain referenced throughout (from [[phase3-advisor-demo]]):
`min1 → min2 → heat-1 → press-1 → heat-2 → press-2 → heat-3 → press-3 → relax → prod`.

---

## At a glance — what differed from our approach

None of the four were bugs in what shipped. The original `mdin-edit` was a deliberately
narrow, never-append, single-token numeric editor (project-prime `fd5ae2b`). The advisor's
feedback didn't ask us to abandon that discipline — it asked the editor to look at *more of
the surrounding namelist* before deciding an edit is safe. Three of the four changes make a
previously **file-blind** check **file-aware**; the fourth carves out the single, controlled
exception to "never append a line." Code landed in `246b06f`.

| # | Topic | What the editor did **before** | What it does **now** | The gap that closed |
|---|-------|--------------------------------|----------------------|---------------------|
| 1 | Temperature | A `temp0` edit coupled to **one** other token — the `&wt value2` ramp end — and only on heat stages. `tempi` was never touched. | Adds a third, mutually-exclusive branch: on a constant-T stage (relax/prod) `tempi` now tracks `temp0` (`tempi == temp0`). | Setting the prod target left `tempi` at its old value → the run started at one temperature and was dragged to another. |
| 2 | `dt` cap | One flat ceiling, `0 < dt ≤ 0.002 ps`, applied as a pure value check **regardless of SHAKE or temperature**. | Cap is read from the stage's own `ntc`/`ntf` (0.002 SHAKE-on / 0.001 SHAKE-off); plus a non-blocking advisory when `temp0 > 300` and `dt` sits at the cap. | A SHAKE-*off* stage could accept a 2 fs step that is only stable with SHAKE on. |
| 3 | Restraints | Could only **edit** an existing `restraint_wt` (and correctly skipped it where `ntr=0`). The engine never appends lines, so it **could not add or remove** restraints. | New `--enable-restraints` (`ntr=1` + `restraint_wt` + **inserts** a `restraintmask` line where absent) and `--disable-restraints` (`ntr=0`). | A stage with no `restraintmask` simply could not gain one through the skill. |
| 4 | `nstlim` | A plain bounds-checked replace (`nstlim > 0`), **blind** to `ntwx`/`ntpr`. | Computes + attaches the output schedule (frames, energy records) and warns on zero / sparse / non-multiple sampling; `--dry-run` previews it. | Shrinking `nstlim` below the write frequency gave a "successful" run with zero or near-zero frames and no signal. |

---

## 1. Temperature consistency across stages (`temp0` ↔ `tempi`, and the downstream stages)

**What the advisor said.** `tempi` is the *initial* temperature at the start of a stage;
`temp0` is the *reference* (target) temperature the thermostat holds the system at. The
temperature **ramp** happens only in the heat stages. So when you set the final target
(e.g. 310 K), every stage from the last heat stage onward must agree:

- `heat-3`: `temp0 = 310` (and its `&wt` ramp must end at 310 — see below)
- `press-3`: `temp0 = 310` (it *continues* at the target; it does not ramp further)
- `relax`, `prod`: these are **constant-temperature** stages — no ramp — so `tempi`
  **and** `temp0` must both be 310 (`tempi == temp0`).

**The physics.** During heating, the thermostat target is *driven* by the `&wt` weight-change
namelist (`nmropt=1`), which linearly ramps `TEMP0` from `value1` to `value2` over a step
window. So in a heat stage the "real" target is the ramped `&wt value2`, and `&cntrl temp0`
must equal that ramp end or the two disagree (this is the classic [[phase3-advisor-demo]]
heat-3 bug: `temp0=300` but `value2=310`). A *pressurization* stage holds the temperature
reached by the previous heat stage — it neither ramps nor restarts, so it just needs the
right `temp0`. A *constant-T* stage (relax, prod) has no ramp at all; if `tempi ≠ temp0` the
run would start at one temperature and be pulled to another, an avoidable thermal transient.

**How the skill handles it now.** Editing `temp0` is **coupled**, with two mutually-exclusive
cases detected from the file itself:
- **Heat stage** (has a `&wt TEMP0` ramp): also rewrite the ramp end `value2` (existing
  behavior). `tempi` is the ramp *start* and is deliberately **left alone**.
- **Constant-T stage** (`tempi` present, no `&wt` ramp, `nmropt≠1` → relax/prod): also rewrite
  `tempi` so `tempi == temp0`.
- **Pressurization stage** (`temp0`, no `tempi`, no ramp): just `temp0`.

So a single `--stage group:third-onward --param temp0 --value 310` now makes heat-3
(`temp0`+`value2`), press-3 (`temp0`), and relax/prod (`temp0`+`tempi`) all internally
consistent at 310 K. **Deferred:** a *cross-stage* advisory ("you set temp0 on some but not
all downstream stages") — it misfires on legitimate single-stage edits and can't see stages
outside the current selector, so the per-edit coupling (which already guarantees each edited
stage is internally consistent) is the chosen guardrail.

**Before → After.** *Before*, a `temp0` edit touched exactly one other token: the `&wt value2`
ramp end, and only on heat stages (`nmropt=1` with a TEMP0 ramp). On a constant-temperature
stage it wrote `temp0` alone — `tempi` kept its old value, so the run would *start* at one
temperature and be pulled to the new target, the avoidable thermal transient above. *After*,
a third mutually-exclusive branch detects the constant-T case (`tempi` present, **no** `&wt`
ramp, `nmropt≠1`) and rewrites `tempi` to match `temp0`, with its own independent self-check.
The `nmropt≠1` guard is what keeps it from firing on a half-disassembled heat stage whose ramp
was removed but whose `tempi` is still a ramp *start*. Heat-stage `tempi` and press stages stay
deliberately untouched — nothing that already worked changed.

---

## 2. `dt` must be coordinated with SHAKE (`ntc`/`ntf`) and with temperature

**What the advisor said.** From the Amber manual: with **SHAKE on** (`ntc=2, ntf=2`) the
maximum time step is **0.002 ps**; with **SHAKE off** (`ntc=1, ntf=1`) it drops to **0.001
ps**. Above 300 K the step should be reduced further. So `dt` should be coordinated with
`ntc`/`ntf` during editing, and a suggestion offered when `temp0 > 300`.

**The physics.** SHAKE constrains the fastest motions in the system (bonds to hydrogen). With
those frozen, a 2 fs step is stable; without SHAKE the X–H stretch (~10 fs period) must be
resolved, forcing ~1 fs. Temperature compounds this: hotter atoms move faster, travel further
per step, and a step that was fine at 300 K can produce anomalously high energies / blow-ups
at 310 K+. (Hydrogen Mass Repartitioning can buy up to ~4 fs by slowing H motion, but that
requires altering the topology and is **out of scope** for a parameter editor.)

**How the skill handles it now.** The `dt` hard cap is **context-aware**: the editor reads
`ntc`/`ntf` from the stage and rejects `OUT_OF_BOUNDS` if `dt` exceeds 0.002 (SHAKE on) or
0.001 (SHAKE off). The absolute global ceiling stays 0.002 (we don't do HMR). Separately, a
**non-blocking advisory** fires when, post-edit, `temp0 > 300` and `dt` is at the cap — it
suggests reducing `dt` but never blocks (same pattern as the deliberate `cut < 8 Å` warning).
The advisor's own 310 K example now correctly raises this advisory on heat-3/press-3/relax/prod.

**Before → After.** *Before*, `dt` was checked against a single flat ceiling — `0 < dt ≤ 0.002
ps` — a *pure value test* that never opened the file. A stage running SHAKE-off (`ntc/ntf ≠ 2`)
could therefore still accept a 2 fs step, which is only stable with SHAKE *on*; temperature was
ignored outright. *After*, the cap is read from the stage itself (0.002 ps with `ntc=2,ntf=2`,
else 0.001 ps) and an over-cap edit is rejected `OUT_OF_BOUNDS` with a message naming which
SHAKE state applied. The 0.002 value-level ceiling stays as the absolute global cap (we still
don't do HMR). The hot-`dt` advisory is wholly new — there was no temperature/`dt` interaction
check at all before.

---

## 3. Restraint transitions in **both** directions

**What the advisor said.** Skipping `restraint_wt` edits where `ntr=0` is correct. But the
skill should also handle *adding* restraints to a stage that has none, and *removing* them:
- **Add** restraints: set `ntr=1`, a user-supplied `restraint_wt`, **and** a user-supplied
  `restraintmask` (the user must provide the atom selection).
- **Remove** restraints: simpler — just set `ntr=0`.

**The physics.** Positional restraints pin chosen atoms to their reference coordinates with a
harmonic penalty. `ntr=1` turns them on; `restraint_wt` (kcal/mol·Å²) is the force constant;
`restraintmask` selects *which* atoms (e.g. `!:WAT,Cl-,K+,Na+ & !@H=` = solute heavy atoms,
letting solvent and hydrogens move). When `ntr=0`, `restraint_wt`/`restraintmask` are inert —
AMBER ignores them — so enabling restraints genuinely requires all three, and a stage that was
never restrained simply has **no `restraintmask` line at all**.

**How the skill handles it now.** Two dedicated modes (kept separate from the numeric
`--param` path so the core "never append" invariant is untouched everywhere else):
- `--enable-restraints --restraint-wt W --restraintmask "MASK"` → sets `ntr=1`, sets
  `restraint_wt`, and edits the `restraintmask` in place if it exists, **or inserts one line**
  (correct indentation + trailing-comma style) where the stage had none. This single,
  controlled insertion is the *only* place the skill adds a line.
- `--disable-restraints` → sets `ntr=0` only; the now-inert `restraint_wt`/`restraintmask` are
  left as-is (AMBER ignores them — matching the advisor's "just set `ntr=0`").

Both are idempotent, all-or-nothing, atomic, and self-checked. The mask is validated shallowly
(non-empty, ≤256 chars, and **no `"` / `'` / `/` / newline** — those bytes would corrupt the
namelist line or the namelist terminator; AMBER masks never need them). A found-during-review
gotcha: the vendored parser strips `! comments`, which would eat a mask that *starts* with `!`
— so the mask is read back through a dedicated quoted-value reader, not the generic parser.

**Before → After.** *Before*, the skill could only **edit** an existing `restraint_wt`, and it
correctly *skipped* that edit where `ntr=0` (restraints inactive) — but it had **no way to turn
restraints on or off**. The core engine never appends lines (its central invariant), so a stage
with no `restraintmask` line simply could not gain one, and there was no path to enable the
three coupled keys at once. *After*, two transactional modes do the multi-key change atomically.
`--enable-restraints` is the *single, controlled exception* to never-append: it inserts exactly
one `restraintmask` line — copying the file's own indentation, trailing-comma style and newline
flavour — and only when the stage lacks one, verified by a line-count self-check. `--disable-
restraints` just sets `ntr=0` and leaves the now-inert keys in place. The generic `--param` path
is untouched, so the never-append invariant still holds everywhere else; a `MODE_CONFLICT` guard
stops these modes from being mixed with a numeric `--param` edit in the same call.

---

## 4. `nstlim` vs the output frequency (`ntwx`/`ntpr`)

**What the advisor said.** After an `nstlim` edit you can end up with `nstlim < ntwx` or
`nstlim < ntpr` (zero or very sparse output), or `nstlim` only slightly above them — the run
won't crash, but the user may not realize they got no usable data. A soft warning when the
step count is too close to / below the output frequency is a good safety net. Best practice is
to align them (`nstlim % ntwx == 0`, same for `ntpr`) so the final interval isn't truncated.
Ideally the skill presents the resulting output schedule and lets the user confirm before
applying.

**The physics / data hygiene.** AMBER writes one trajectory frame every `ntwx` steps and one
energy record every `ntpr` steps. `trajectory_frames = nstlim // ntwx`. If `nstlim < ntwx` you
get **zero frames** — a "successful" run with no trajectory. A non-multiple leaves a runt final
interval. (Note `ntwx = 0` means the trajectory is intentionally **off** — the heat/press
stages do this — so that case must *not* warn.)

**How the skill handles it now.** After an `nstlim` edit the skill computes and **attaches the
output schedule** to the envelope (`nstlim`, `ntwx → trajectory_frames`, `ntpr → energy_outputs`,
plus a `trajectory_off` flag) and emits **non-blocking warnings** on zero frames, very sparse
(<10) frames, and non-multiple alignment — while staying silent when `ntwx = 0`. The advisor's
"present and confirm before applying" maps onto the skill's existing **`--dry-run`**: a dry-run
`nstlim` edit returns the same schedule + warnings *without writing*, so the user reviews the
schedule, then re-runs without `--dry-run` to commit. (The skill is non-interactive and
all-or-nothing; `--dry-run` is its review-before-commit mechanism.)

**Before → After.** *Before*, an `nstlim` edit was a plain bounds-checked replace (`nstlim > 0`)
that never read `ntwx`/`ntpr`. Shrinking `nstlim` below the write frequency therefore produced a
"successful" run with zero or near-zero trajectory frames — and *no signal* that anything was
wrong. *After*, the skill computes the resulting schedule (`trajectory_frames = nstlim // ntwx`,
energy records via `ntpr`, plus a `trajectory_off` flag), attaches it to the JSON envelope, and
raises non-blocking warnings on zero / very-sparse (<10) / non-multiple sampling — while staying
silent when `ntwx=0` (trajectory intentionally off on heat/press stages). `--dry-run` returns
the identical schedule *without writing*, which is how the advisor's "present and confirm before
applying" is satisfied within a non-interactive tool.

---

## Why this matters

Every one of these is the same lesson the skill was built on (cf.
[[antechamber-aromatic-kekulize-bug]]): a parameter edit that *looks* fine and passes every
gate can quietly produce wrong physics or no usable data. The fixes push more of that
judgment into deterministic, self-checked, oracle-tested code rather than leaving it to the
person (or LLM) issuing the edit. Verification — deterministic suite (oracle + acceptance +
~245k fuzz assertions + mutation 14/14), an adversarial second-AI review (3 latent
arbitrary-input bugs found and fixed), and a real `pmemd` edit→run smoke — is logged in
[[Dev_Log]].
