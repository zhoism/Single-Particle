---
tags: [project-prime, openclaw, amber, gates, mdin-edit, restart, ntx, irest, session-handoff, encoding]
type: handoff
status: ready
created: 2026-06-24
supersedes: Gap_ntx_irest_restart_topology  # this handoff replaces that gap note (content folded in below)
---

# Next Session Starter — Encode the `ntx`↔`irest` restart-coherence gate

> Created 2026-06-24 (drift-audit follow-on). This **replaces** the old `Gap_ntx_irest_restart_topology` note — the gap analysis is folded into §Background below, and this file makes it session-actionable. **This is an ENCODING session** (turn a known verifier hole into a real, tested, committed deterministic gate), the focused sibling of [[Next_Session_Prompt_AMBER_Gate_Encoding]] — split out because the rule table + a contested editor-feature scope-tension make it meatier than a one-line backlog gate.
>
> **⚠️ FIRST ACTION OF THE SESSION: do NOT start coding. Ask the four §Open questions via one `AskUserQuestion` gate ([[feedback-verify-and-eval]]), then proceed on the answers.** Recommended answers are marked, but they are the user's call. Paste the §The prompt to paste block into a fresh Claude Code session (run from the vault).

---

## Background — what this is (folded in from the retired gap note)

**`ntx` / `irest` semantics** (`observed from source`, Amber26 §23.6):
- **`ntx`** = what AMBER reads from the start-coordinate file. `ntx=1` = coordinates only → velocities are *invented* (Maxwell–Boltzmann at `tempi`). `ntx=5` = coordinates **+ velocities** (inherited from the prior stage → `tempi` ignored at runtime). Velocity-reading values are `ntx ∈ {4,5,6,7}` (5 is the modern standard; 4/6/7 are legacy unformatted variants).
- **`irest`** = `0` new run (clock at step 0) / `1` restart (continue the step counter). A restart **needs** velocities, so `irest=1` is only legal with a velocity-reading `ntx`. **`irest=1, ntx=1` is an illegal pair — AMBER aborts.**
- In the advisor demo set ([[phase3-advisor-demo]]): heat stages = `ntx=1`/`irest=0` (fresh velocities); press/relax/prod = `ntx=5`/`irest=1` (inherited). All coherent.

**The gap is three distinct things — one settled, two open:**
- ✅ **Settled (already correct, no action):** `mdin-edit`'s constant-T `temp0`↔`tempi` coupling is deliberately `ntx`-agnostic (keys on ramp-absence + `nmropt≠1` + `tempi` present, never on `ntx`; `wrapper.py:490`). So an already-`ntx=1` stage gets the matching `tempi` written — genuinely runtime-correct.
- 🟥 **OPEN #1 — no coherence gate (THIS SESSION).** The validator has **zero** `ntx`/`irest` awareness. An illegal `irest=1, ntx=1` file **passes every gate we have**, however it was produced. A latent correctness hole in the safety boundary the whole pipeline leans on ([[Design_Determinism_Spectrum]]) — independent of any editing feature, cheap to close, uncontested.
- 🟡 **OPEN #2/#3 — editor can't flip restart mode + re-thermalization is unguarded (DEFERRED).** `ntx`/`irest` aren't in `mdin-edit`'s editable set; flipping a stage is a coupled-pair transaction (precedent: §3 `--enable/--disable-restraints` in [[Research_Advisor_Feedback_mdin_edit]]). **Decision 2026-06-22 (`confirmed by user`): document-only, defer** — restart *topology* is arguably planner-layer ([[Arch_Taskboard_Manifest]]), not a within-protocol tweak. Stays deferred unless Q1 says otherwise.

---

## ⛳ Open questions — ASK THESE FIRST (one `AskUserQuestion` gate)

**Q1 — Scope.** Just the coherence GATE (#1), or also the editor toggle (#2)?
- **(a) Gate only** ✅ *recommended* — correctness hole, uncontested, independent of the design debate.
- (b) Gate + `--set-restart`/`--set-fresh-start` editor toggle — bigger; reopens the "should `mdin-edit` own restart topology vs. planner-layer" scope-tension.
- (c) Gate + toggle + re-thermalization advisory (#3) — full sweep.

**Q2 — `imin` scoping.** Fire on minimization stages (`imin=1`)?
- **(a) Dynamics-only (`imin=0`)** ✅ *recommended* — `irest` is moot in minimization.
- (b) All stages.

**Q3 — `ntx` legality set for `irest=1`.** The gate treats which `ntx` as legal-with-restart?
- **(a) `{4,5,6,7}` permissive** ✅ *recommended* — all velocity-reading values are valid restart; don't false-fire on legitimate (if legacy) files.
- (b) `{5}` strict — only the modern value; warn on deprecated 4/6/7.

**Q4 — Severity + reach.** How loud, and which copies get it?
- **(a) Hard-fail (`ok:false`) in the canonical source + all 3 vendored copies** ✅ *recommended* — matches existing bounds discipline + the `5647b0a` template.
- (b) Hard-fail, canonical `md-param-check` source only (let the next vendor-sync propagate).
- (c) Warn-only.

> Also note up-front (not a question — the correct behavior): the gate **must apply AMBER defaults** (`ntx`→1, `irest`→0, `imin`→0) so a namelist that *omits* `ntx` under `irest=1` is still caught; and it must **NOT** fire on the legal reverse case `ntx=5, irest=0` (reading velocities but restarting the clock fresh is allowed).

---

## The work — oracle-first, on the recommended (gate-only) path

Adapt if Q1≠(a). The template to copy is the neutrality fix: commit **`5647b0a`** + test `skills/tleap-build/tests/test_neutrality_gate.py` — read that diff first; this gate takes the exact same shape (structural namelist parse → fixture oracle → no-false-alarm regression → adversarial review → commit + push).

**Code surface (pinned this session — saves you the recon):**
- **Canonical validator:** `.claude/skills/md-param-check/checks/check_amber.py` (the `md-param-check` Claude Code skill, in the *vault* `.claude/`, not project-prime).
- **3 vendored copies in project-prime:** `skills/{md-planner,amber-recover,mdin-edit}/scripts/check_amber_vendored.py`.
- **⚠️ they are NOT in sync:** `md-planner` + `amber-recover` are byte-identical (`91fcd543…`); **`mdin-edit`'s has DIVERGED (`dd5f581f…`)** — it carries the advisor refinements. So you **cannot** blind-copy the source over mdin-edit's copy — **hand-add** the new function there, or it clobbers the advisor work (`246b06f`). Re-vendor md-planner/amber-recover by copy is fine.

**Steps:**
1. **Pin the rule** as the oracle (write it as the test's ground truth, independent reimpl — don't reuse the gate's own code):
   - Parse `imin`/`irest`/`ntx` from each `&cntrl`; apply defaults (0/0/1).
   - **Fires** ⇔ `imin==0 AND irest==1 AND ntx ∉ {4,5,6,7}` → `ok:false`, code e.g. `RESTART_NTX_INCOHERENT` (names the stage + the offending pair).
   - **Legal (no fire):** `irest==0` (any ntx) · `irest==1, ntx∈{4,5,6,7}` · `imin==1` (per Q2) · `ntx==5, irest==0`.
2. **Implement** the function in the canonical `check_amber.py`; wire into its namelist `validate` path. Propagate per Q4 (default: copy to md-planner/amber-recover, hand-merge into mdin-edit).
3. **Oracle test** (`py3.9 + py3.11`, the project's two interpreters): fixture matrix of legal + illegal `(imin,irest,ntx)` incl. omitted-key defaults; assert fires exactly on the illegal set, never on legal.
4. **No-false-alarm regression:** run the gate over **every real production mdin in the repo** (the `phase3-explicit-solvent-md/` set + any generated namelists) → **0 false-alarms** (all real stages are coherent). A gate that reddens a known-good file is wrong.
5. **Adversarial second-AI review** ([[feedback-verify-and-eval]]) — independent agent told to find faults against the criteria, with the real files in hand. Fix high-severity before declaring done.
6. **Commit + push** (`git push origin main` — the repo has a remote now, HEAD `246b06f`).
7. **Close-out:** update [[Gap_Gate_Coverage]] (this coherence gate → encoded), append a [[Dev_Log]] entry, and if #2/#3 stayed deferred, note the residual open gap there (so the knowledge the retired gap note held isn't lost).

---

## Success criteria (define up-front; mirror the `5647b0a` template)
- Oracle green on **py3.9 + py3.11**.
- Acceptance proves the illegal `irest=1, ntx=1` (and the default-omitted variant) is **caught**, and all legal combos pass — including the `ntx=5, irest=0` non-fire.
- **0 false-alarms** over every real GREEN mdin in the repo.
- Adversarial review → PASS (high-severity fixed).
- Committed **and pushed**; `mdin-edit`'s divergent copy not clobbered.

## Decisions banked — do NOT re-litigate
- **Frozen core stays frozen.** Add to the validator's `validate` path; do **not** touch `run_happy_path.sh`; do not restructure a wrapper (STOP-and-surface if it'd need wire-in).
- **Structural namelist parse, not log-scrape** — the banked lesson from `SYSTEM_NOT_NEUTRAL` ([[Research_AMBER_Failure_Modes]]); `ntx`/`irest` read straight from `&cntrl`.
- **The reverse case is legal** (`ntx=5, irest=0`) — don't over-fire.
- **#2 editor toggle + #3 advisory stay DEFERRED** unless Q1 reopens them — the 2026-06-22 document-only decision holds; restart topology is arguably planner-layer.
- A gate is `inferred` until it clears the full discipline ([[Eval_Criteria]]): proxy → oracle/regression → adversarial review → commit+push.

## NOT in scope (explicitly)
- Building `--set-restart` / `--set-fresh-start` editing (that's #2 — only if Q1 says so).
- The `ntx=1`-needs-`tempi` cold-start advisory (that's #3 / the editor side, softer than the hard coherence gate).
- Touching `mdin-edit`'s temp/restraint logic — the advisor work (`246b06f`) is done and verified; this session only ADDS the coherence check to the shared validator.

---

## The prompt to paste

```
Dedicated session: encode the ntx↔irest restart-coherence gate. Read
handoffs/Next_Session_Prompt_ntx_irest_CoherenceGate.md in full first.

FIRST, before any coding, ask me the four Open questions in that handoff as ONE
AskUserQuestion gate (scope / imin-scoping / ntx legality set / severity+reach),
recommended option first. Then proceed on my answers.

On the recommended (gate-only) path: copy the 5647b0a neutrality-gate shape —
add a structural ntx/irest coherence check to .claude/skills/md-param-check/checks/
check_amber.py and the 3 vendored copies (mdin-edit's has DIVERGED — hand-merge,
don't clobber). Fires iff imin==0 AND irest==1 AND ntx not in {4,5,6,7}; apply
AMBER defaults (ntx=1/irest=0/imin=0); do NOT fire on ntx=5,irest=0. Then:
independent oracle (py3.9+3.11), 0-false-alarm regression over every real mdin in
the repo, adversarial review, commit + push. Close out Gap_Gate_Coverage + Dev_Log.
```
