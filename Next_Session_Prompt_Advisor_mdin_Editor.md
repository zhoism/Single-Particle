---
tags: [project-prime, openclaw, session-handoff, advisor-task, mdin-editor, plan]
type: handoff
status: consumed
created: 2026-06-08
---

# Onboarding + Plan — the advisor's MD-parameter-editor Skill

> **This file is both your onboarding AND your plan.** It is written for a FRESH Claude Code chat (no memory of prior sessions), run from the vault. It exists because the advisor set a specific task — a natural-language **parameter-editing** OpenClaw Skill over his pre-prepared mdin files — and **we have not built it yet** (we built an adjacent *generate-and-run* pipeline instead). This document onboards you to the system, states the task and the honest gap, gives you the demo files' ground truth, and lays out the build plan. Read §1–§6, then execute. A condensed paste-ready block is in §7.

> **✅ OUTCOME (consumed 2026-06-08):** Built the deterministic core — new OpenClaw skill `project-prime/skills/mdin-edit/` (✓ ready), committed `fd5ae2b`. Idempotent, bounds-checked, stage-aware parse-replace with `temp0`↔`&wt value2` coupling (fixes the heat-3 bug), atomic write + post-edit self-check, and a change log; validation logic vendored from `md-param-check`. §23.6 write-up (Task 1) in `references/mdin-params.md`; "how mistakes are avoided" summary (Task 4) in SKILL.md. `test_acceptance.sh` 11 cases (file-byte assertions, not `ok:true`) green incl. all four advisor examples (dt→0.001 heat-1; temp0→310 third-onward; cut→7.0; restraint_wt→1.0). **Deferred (decided with user):** the `--submit` reduced-`nstlim` smoke (Stage D) + the live `openclaw agent` NL drive (Stage F). See [[Dev_Log]] 2026-06-08 (cont. 2).

---

## 1. Onboarding — the system you're joining

**Project ("Project Prime"):** an internship build — an **agentic AMBER molecular-dynamics pipeline**. A **decoupled hybrid agent**: an LLM (reached via a Discord bot or the CLI) decides *what* to run; **hardened deterministic Python wrappers** (OpenClaw "skills") do *how* the science executes. The LLM never writes chemistry — it picks a skill and fills its arguments; the wrapper does the work and validates its own output. Full system overview: **`Arch_Pipeline_System.md`** (read it first).

**Why this discipline matters (cautionary tale, read it):** last session we caught a *silent* science bug — a ligand was mis-typed non-aromatic because a tool (OpenBabel) failed quietly and the wrapper trusted it; **every validation gate passed**. Lesson banked in memory `[[antechamber-aromatic-kekulize-bug]]`: **never trust `ok:true` — inspect the actual files; verify thoroughly.** This task is *all about* not making silent mistakes, so internalize it.

**Where everything lives:**
- **Code repo:** `/Users/kevinzhou/Downloads/Single Particle/project-prime/` (git, branch `master`). Skills in `skills/<name>/`; shared scripts in `scripts/`; the agent-free spine `run_happy_path.sh`.
- **Vault (docs):** `/Users/kevinzhou/Downloads/Single Particle/Single Particle/` (git, branch `main`) — design notes, `Dev_Log.md`, this file.
- **Toolchain:** the `prime-amber` conda env (AmberTools 24.8) + locally-built **pmemd 26**. Activate for any AMBER work:
  ```bash
  source /opt/homebrew/Caskroom/miniforge/base/envs/prime-amber/amber.sh
  export PATH="$HOME/Downloads/pmemd26/bin:$AMBERHOME/bin:$PATH"
  # or: source project-prime/scripts/env.sh   (the canonical bootstrap)
  ```
- **OpenClaw:** 2026.5.28; gateway LaunchAgent on `127.0.0.1:18789`; default model `cerebras/gpt-oss-120b` (free). Skills under `project-prime/skills/` **auto-register** via the `skills.load.extraDirs` config (watcher on). Shell tool is `exec` (not `bash`). Prompt the agent in **goals, not tool topology** (topology prompts trigger idle stalls).

**The 5 existing skills (the PATTERN to copy):** `antechamber-ligandprep`, `tleap-build`, `amber-md-run`, `cpptraj-analysis`, `pipeline-async`. Each = a `SKILL.md` (single-line JSON `metadata`, goal-oriented body) + `scripts/wrapper.py` (with `--dry-run` + one JSON envelope) + `references/heuristics.md` + `test_acceptance.sh` (golden + unrelated + malformed). **Open `antechamber-ligandprep/` as your template.**

**READ FIRST (memories + notes):** `project-prime-status`, `openclaw-canonical-paths`, `phase3-advisor-demo`, `amber26-pdf-section-map`, `antechamber-aromatic-kekulize-bug`, `dev-log-convention`; vault `Arch_Pipeline_System.md`, `Phase3_Taskboard_Manifest.md`.

**Tooling you have (Claude Code skills):** `skill-scaffold` (bootstraps a new OpenClaw skill dir — use it to create the new skill), `md-param-check` (a **validator** for AMBER `.in` files — already encodes the bounds + the heat-3 `temp0`==`&wt value2` rule; **reuse its logic, don't rewrite it**), `devlog-append`, `next-session-prompt`, `vault-note-new`.

---

## 2. The task (your advisor's actual assignment)

Operate on a **pre-prepared protein–ligand complex** (provided, see §3) and:

1. **Understand the input files** — go through the mdin files (min, heat, press, relax, prod); understand `dt`, `cut`, etc. Reference **Amber26 manual §23.6 "General minimization and dynamics parameters."** (Amber26.pdf is at the vault root; §23 sander starts ~p425 — see memory `amber26-pdf-section-map`.)
2. **Write an OpenClaw Skill** that lets you specify, **in natural language**, *which stage* and *which parameter* to modify (e.g. *"set the time step to 0.001 ps in the first heating stage"*), then **submit the job**.
3. **Extend the Skill** to handle:
   - *"set the target temperature to 310 K"* → update `temp0` in **all stages from the third onward** (the advisor names them: `heat-3.in`, `press-3.in`, `relax.in`, `prod.in`).
   - *"set the non-bond cutoff to 7.0 Å"* → modify `cut`.
   - *"relax the positional restraints from 5.0 to 1.0 in a specific heating or pressurization stage"* → reduce `restraint_wt`.
4. **Record & summarize** — log whether each change succeeds and how the Skill **avoids mistakes** (bounds checking, stage-aware file targeting). **Goal: a Skill that modifies parameters correctly and predictably, no matter how many times it's used.**

### Honest assessment of where we are (do not skip)

| Sub-task | Status | Why |
|---|---|---|
| 1. Understand mdin (+ §23.6) | 🟡 partial | We analyzed the demo (found the heat-3 bug) but produced no §23.6-grounded write-up. **§3 below gives you the ground truth to finish it.** |
| 2. NL parameter-**edit** skill + submit | 🔴 **not built** | Our `amber-md-run` *generates its own* `min/heat/density/product` chain — it does **not** edit the advisor's existing files, and takes no NL parameter edits. **This is a NEW skill.** |
| 3. The three extensions | 🔴 not built | depends on #2 |
| 4. Record + bounds + predictability | 🟡 partial | The bounds-checking *engine* exists (`md-param-check`) but only **validates**; it is not wired into a **modifier**, and there is no change-log/idempotency. |

**Bottom line: build a new OpenClaw skill (`mdin-edit`) that EDITS the advisor's files. Reuse the wrapper pattern + the `md-param-check` validation logic. Do not extend `amber-md-run` (wrong tool — it generates, doesn't edit).**

---

## 3. The demo — ground truth (the files you operate on)

**Location:** `phase3-explicit-solvent-md/` (also `phase3-explicit-solvent-md.zip`) at the vault root. Contains `complex.parm7`, `complex.rst7`, `complex.pdb`, `submit.sh`, and **10 mdin files**. **Do NOT edit the originals in place** — copy to a working dir (or back up) so edits are reproducible and the advisor's set stays pristine.

**Chain order (from `submit.sh`, restart-coords chained `-c <prev>.rst7`):**
`min1 → min2 → heat-1 → press-1 → heat-2 → press-2 → heat-3 → press-3 → relax → prod` (heat/press are **interleaved**: heat to T, then pressurize at T).

**Per-stage parameter map (your §23.6 write-up + the skill's stage→file knowledge):**

| Stage | File | Ensemble | Key params | Restraint | temp0 / ramp |
|---|---|---|---|---|---|
| Min 1 | `min1.in` | minimization | `imin=1, maxcyc=10000, cut=9` | `ntr=1, restraint_wt=5.0` | — (no dt/temp0) |
| Min 2 | `min2.in` | minimization | `imin=1, maxcyc=10000, cut=9` | `ntr=0` (none) | — |
| Heat 1 | `heat-1.in` | NVT (`ntb=1,ntp=0`) | `dt=0.002, cut=9, ntt=3` | `restraint_wt=5.0` | `temp0=100`; `&wt` 5→100 (`nmropt=1`) |
| Heat 2 | `heat-2.in` | NVT | same | `5.0` | `temp0=200`; `&wt` 100→200 |
| Heat 3 | `heat-3.in` | NVT | same | `5.0` | `temp0=300`; **`&wt` 200→`value2=310`** ⚠️ |
| Press 1 | `press-1.in` | NPT (`ntb=2,ntp=1,barostat=2,pres0=1`) | `dt=0.002, cut=9` | `5.0` | `temp0=100` (no `&wt`) |
| Press 2 | `press-2.in` | NPT | same | `5.0` | `temp0=200` |
| Press 3 | `press-3.in` | NPT | same | `5.0` | `temp0=300` |
| Relax | `relax.in` | NPT | `nstlim=500000, dt=0.002` | `ntr=0` (none) | `temp0=300` |
| Prod | `prod.in` | NPT | `nstlim=5000000 (10 ns), dt=0.002` | `ntr=0` (none) | `temp0=300` |

**Param presence (the skill must know this for stage-aware targeting):**
- `dt`, `temp0`: all 8 MD stages (NOT min1/min2). `cut`: all 10. `restraint_wt`: min1 + heat-1/2/3 + press-1/2/3 (7 stages; absent in min2/relax/prod). `&wt` TEMP0 ramp: heat-1/2/3 only.

**⚠️ The known bug (and why the advisor's task #3 is clever):** `heat-3.in` has `temp0=300` in `&cntrl` but its `&wt` ramp ends at `value2=310` — inconsistent. The advisor's *"set temp0 to 310 from the third stage onward"* would **align** heat-3's `temp0` with its existing `&wt=310` (fixing it). **So when your skill sets `temp0` in a heat stage with `nmropt=1`, it must also keep the `&wt value2` consistent** — that is exactly the "avoid mistakes / stage-aware" sophistication being tested.

**`submit.sh` portability:** it hardcodes `AMBERHOME=/Application/software/Amber26/pmemd26` (the **advisor's** machine). Your submit path must **adapt this** to the local pmemd26 (`~/Downloads/pmemd26` / the `prime-amber` env). The hardcoded-AMBERHOME anti-pattern is called out in `[[phase3-advisor-demo]]`.

---

## 4. The plan — build the `mdin-edit` OpenClaw skill

**Design (consistent with the architecture):** the **agent** parses the NL → invokes `mdin-edit` with **structured args**; the **wrapper** does the deterministic, bounds-checked edit + validation + logging. (LLM out of the edit path.) The advisor's *"a Skill that lets you specify in NL"* = agent(NL) + skill(edit).

**Skill interface** (`project-prime/skills/mdin-edit/scripts/wrapper.py`):
`--stage <heat-1|press-3|relax|prod|min1|... | group:third-onward | group:all>` · `--param <dt|cut|temp0|restraint_wt|nstlim|...>` · `--value <number>` · `--workdir <copy of the demo>` · `--dry-run` · (later) `--submit`.

Build in stages; **verify each by inspecting the edited file, not just the envelope.**

- **Stage A — Task 1 deliverable.** Write a short **§23.6-grounded write-up** of the mdin params per stage (use the table above; cite Amber26 §23.6 for `dt`, `cut`, `ntt`, `ntp`, `ntr`/`restraint_wt`, `nmropt`/`&wt`). Put it in `skills/mdin-edit/references/mdin-params.md` (and optionally a vault `Arch_*`/`OpenClaw_*` note). This *is* deliverable #1.
- **Stage B — Task 2 (core skill).** `skill-scaffold` a new `mdin-edit` skill. wrapper.py:
  1. **Resolve `--stage` → file(s)** via an explicit map (incl. groups `third-onward` = `{heat-3,press-3,relax,prod}` and `all`).
  2. **Param applicability check** — refuse `dt`/`temp0` on `min1/min2`; refuse `restraint_wt` where `ntr=0`; clear error if the param/namelist isn't present.
  3. **Bounds check** — `0 < dt ≤ 0.002` (SHAKE on), `cut` ~`6–12`, `0 < temp0 ≤ ~400`, `restraint_wt ≥ 0`, `nstlim > 0`. Reject out-of-bounds with a coded error.
  4. **Idempotent edit** — parse-and-replace the value inside the correct `&cntrl` namelist via regex (preserve comments/formatting); **never blind-append**. Re-running the same edit must yield a byte-identical file.
  5. **`&wt` consistency** — if editing `temp0` in a `nmropt=1` heat stage, update `&wt value2` to match (or flag). Handles the heat-3 case.
  6. **Post-edit validation** — run the `md-param-check` logic over the edited file; fail if it now violates a rule.
  7. **Change log** — append `{timestamp, file, param, old→new}` to `mdin-edit.log` (the "record" requirement) and return it in the JSON envelope.
  8. **`--dry-run`** prints the planned edit + validation without writing.
  - **Acceptance (`test_acceptance.sh`):** the advisor's example *"dt → 0.001 in the first heating stage"* (→ `heat-1.in`); **idempotency** (run twice → identical); **out-of-bounds rejected** (`dt=0.01` → error); **wrong-param-for-stage rejected** (`dt` on `min1` → error).
- **Stage C — Task 3 (the three extensions).** Add + test:
  - `temp0 = 310`, `--stage group:third-onward` → edits `heat-3, press-3, relax, prod`; **heat-3 also gets `&wt value2=310`** (assert it). Verify heat-1/2 and press-1/2 are **untouched**.
  - `cut = 7.0`, `--stage group:all` (or a named stage) → edits `cut` everywhere; assert.
  - `restraint_wt 5.0 → 1.0`, `--stage <heat-N|press-N>` → assert only that stage changed.
- **Stage D — submit path.** Add `--submit` (or a sibling script): copy `submit.sh`, **rewrite AMBERHOME** to the local toolchain, run the chain on `complex.parm7/.rst7`. **Full `prod` is 10 ns — far too long locally**; provide a **reduced-`nstlim` smoke** (e.g. temporarily small `nstlim`) to *prove* the submit works without a multi-hour run. Log it.
- **Stage E — Task 4 (record + summarize).** Confirm the guarantees with tests: every advisor example succeeds + is logged; each edit is **idempotent** (double-run diff = empty); bounds + stage-aware + `&wt` guards all fire on bad input. Write the summary (what each change does, how mistakes are avoided).
- **Stage F — NL through the agent.** Drive the skill via `openclaw agent` (or Discord) with **goal-phrased** prompts ("set the timestep to 0.001 in the first heating stage"); confirm the agent maps NL → the right `--stage/--param/--value`. (Optional: expose via `pipeline-async`-style Discord.)
- **Stage G — record.** `devlog-append` entry; update `Phase3_Taskboard_Manifest.md`; update memory `project-prime-status`; flip this starter to `consumed` with an Outcome.

---

## 5. Decisions banked / guards (don't re-litigate or trip)

- **Agent parses NL; wrapper does the deterministic edit.** Don't put parsing logic the LLM should do into the wrapper, and don't let the LLM edit files directly.
- **Work on a COPY; never destroy the advisor's originals.** Idempotent **parse-replace** edits only — never append.
- **Stage-awareness is the whole point:** refuse a param that doesn't belong in a stage (`dt` in `min`); `group:third-onward` = exactly `{heat-3, press-3, relax, prod}` (NOT heat-1/2 or press-1/2).
- **`&wt` consistency** for `temp0` in `nmropt=1` heat stages (the heat-3 trap).
- **Reuse `md-param-check` validation** (bounds + heat-3 rule) — it's a *Claude Code* validator; your new `mdin-edit` is an *OpenClaw* skill in `project-prime/skills/`. Different things; reuse the *logic*.
- **VERIFY THOROUGHLY** (the aromatic-bug lesson): inspect edited files, diff double-runs, don't trust `ok:true`.
- **submit:** adapt AMBERHOME; reduced-`nstlim` smoke for the proof (don't kick off a 10 ns run).
- **Bounds defaults:** `dt ≤ 2 fs` with SHAKE; `cut` 6–12 Å; `temp0` 0–~400 K; `restraint_wt ≥ 0`. Cite Amber26 §23.6 for the physics.

---

## 6. Definition of done (what "accomplished" means)

✅ A new **OpenClaw skill `mdin-edit`**, agent-invocable in **natural language**, that:
1. edits a named param in a named stage of the advisor's mdin files, with **bounds checking** + **stage-aware file targeting** + **`&wt` consistency** + a **change log**;
2. handles the advisor's four examples (dt-in-heat-1; temp0→310 from third-onward; cut→7.0; restraint_wt→1.0);
3. is **idempotent/predictable** (re-running any edit is byte-identical) — proven by acceptance tests incl. negative cases;
4. can **submit** the chain locally (adapted AMBERHOME, reduced-nstlim smoke);
5. ships with the **§23.6 write-up** (Task 1) and a **recorded summary** (Task 4);
6. is committed + logged (Dev_Log, manifest, memory).

---

## 7. The prompt to paste (condensed, self-contained)

```
New session — Project Prime (agentic AMBER MD pipeline). Today: build the advisor's MD-parameter-EDITOR OpenClaw skill. We have NOT built this yet (our amber-md-run GENERATES namelists; the advisor wants to EDIT his pre-prepared mdin files via natural language). Full onboarding + plan: vault file Next_Session_Prompt_Advisor_mdin_Editor.md — READ IT, plus Arch_Pipeline_System.md.

Read first: memories project-prime-status, openclaw-canonical-paths, phase3-advisor-demo, amber26-pdf-section-map, antechamber-aromatic-kekulize-bug (cautionary: verify thoroughly, don't trust ok:true), dev-log-convention. Vault: Arch_Pipeline_System.md, Phase3_Taskboard_Manifest.md, Amber26.pdf §23.6.

The demo (DON'T edit originals — copy first): phase3-explicit-solvent-md/ — complex.parm7/.rst7 + 10 mdin files (min1,min2,heat-1/2/3,press-1/2/3,relax,prod) + submit.sh. Chain order min1→min2→heat-1→press-1→heat-2→press-2→heat-3→press-3→relax→prod. Known bug: heat-3 temp0=300 vs &wt value2=310. submit.sh AMBERHOME is the advisor's path — adapt to local pmemd26.

Toolchain: source /opt/homebrew/Caskroom/miniforge/base/envs/prime-amber/amber.sh && export PATH="$HOME/Downloads/pmemd26/bin:$AMBERHOME/bin:$PATH" (or source project-prime/scripts/env.sh).

Plan (see §4 of the vault file for detail): A) §23.6-grounded write-up of the mdin params (Task 1 deliverable). B) skill-scaffold a new OpenClaw skill `mdin-edit` in project-prime/skills/ (template: skills/antechamber-ligandprep): stage→file resolution (incl. groups third-onward={heat-3,press-3,relax,prod}, all), param-applicability check, BOUNDS check (dt≤0.002+SHAKE, cut 6-12, temp0 0-~400, restraint_wt≥0), IDEMPOTENT parse-replace edit (never append), &wt-value2 consistency for temp0 in nmropt=1 heat stages, post-edit md-param-check validation, a change log, JSON envelope, --dry-run; acceptance test = advisor's "dt→0.001 in first heating stage" + idempotency(double-run identical) + out-of-bounds rejected + wrong-param-for-stage rejected. C) extend to the 3 cases (temp0→310 third-onward incl. heat-3 &wt; cut→7.0; restraint_wt→1.0). D) submit path (adapt AMBERHOME; reduced-nstlim smoke — prod is 10 ns, too long). E) record/summarize (Task 4). F) drive via openclaw agent in NL (goal-phrased). G) devlog + manifest + memory.

Guards: agent parses NL, wrapper does the deterministic edit; work on a COPY; reuse md-param-check's validation logic (don't rewrite); refuse params that don't belong in a stage (dt in min); VERIFY by inspecting edited files + diffing double-runs (the aromatic-bug lesson). Definition of done: §6 of the vault file.

Suggest entering plan mode to confirm the skill design, then build stage by stage with verification.
```

---

## Cross-links
- `Arch_Pipeline_System.md` — the system you're extending.
- `[[phase3-advisor-demo]]`, `[[amber26-pdf-section-map]]`, `[[antechamber-aromatic-kekulize-bug]]`, `[[openclaw-canonical-paths]]`, `[[project-prime-status]]` — memories.
- `Phase3_Taskboard_Manifest.md` — this becomes a new manifest entry (a parameter-editor skill alongside the Stage 2–5 generators).
- Supersedes the PLIP focus in `[[Next_Session_Prompt_OpenClaw_Day9]]` — the advisor's task is the priority.
