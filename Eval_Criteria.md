---
tags: [project-prime, process, evaluation, quality-gate]
type: process
status: active
created: 2026-06-10
---

# Evaluation Criteria — what "great" means before we ship

> The precise, per-artifact-type rubric for upcoming sessions. Format matches the project's existing **gate-list / "VERDICT PASS"** style (the Day-6 eval). Workflow established 2026-06-10 (memory [[feedback-verify-and-eval]]): **pre-run decision gate → deterministic gates → adversarial second-AI review per substantial deliverable.** Load this at session start; cite the relevant section before starting work, and run the matching gates before declaring done.

## The loop (every session)

1. **Pre-run decision gate.** Before committing compute or long/irreversible work, batch the **key decisions** into ONE `AskUserQuestion` checkpoint and get sign-off. Key = irreversible · costly/long-compute · multiple defensible options · affects scientific validity · scope-defining (target/system, parameters, branch-vs-master, definition of done). Mechanical/reversible steps stay autonomous.
2. **Define criteria up-front.** State the success criteria for THIS artifact (from the matching section below) and name the past example whose format you're matching, before starting.
3. **Deterministic gates first.** Run the objective, machine-checkable checks (test harness, byte-diff, `check_amber.py`, ΔG sanity, acceptance suite). These are necessary, not sufficient.
4. **Adversarial second-AI review per substantial deliverable.** Spawn an independent agent told to FIND FAULTS against these criteria, with the real artifacts (files/logs/diff) in hand, defaulting to skeptical. Fix high-severity findings before declaring done. This catches what gates can't (silent passes, missed scope, weak chemistry) — see [[antechamber-aromatic-kekulize-bug]].
5. **Record + verdict.** Commit (local), Dev_Log entry, memory/handoff updated. State an honest verdict: PASS / PASS-WITH-CONCERNS / FAIL, with the concerns named.

## Common spine — every deliverable

- ① **Deterministic gates pass** — the objective checks for this artifact type are green.
- ② **Independently verified** — re-derived by a second source (oracle / byte-diff) OR adversarially reviewed; not self-attested.
- ③ **Format-matched** — matches the established format of a named past example of its type.
- ④ **Scope complete** — nothing silently dropped; every deferral is named explicitly.
- ⑤ **Reversible + recorded** — committed (local, not pushed unless asked), logged in Dev_Log, memory/handoff updated.

## Per-type gates

### MD run (happy path / arbitrary target)
- 4/4 stage envelopes `ok:true` (antechamber → tleap → md-run → cpptraj).
- MM-GBSA ΔG **< 0** and in a sane range (single-trajectory ΔG is a *sanity number*, not a precise affinity — don't over-read it).
- ≥12 analyses produced, ≥10 PNGs.
- **Ligand chemistry sane:** aromatic ring carbons typed GAFF2 `ca` (H `ha`), NOT mis-typed non-aromatic; H present (never `--nohyd` a ligand); crystal/pocket coords preserved.
- **Physical realism:** dt ≤ 2 fs, SHAKE on, non-bonded `cut` in range, thermostat/barostat sane.
- Box/atom counts plausible for the system; no NaN/abnormal termination.

### Skill build (OpenClaw deterministic wrapper)
- `--dry-run` works + emits a JSON envelope; the LLM only picks the skill, the wrapper does the work.
- `test_acceptance.sh`: golden + unrelated/subset + **malformed → `ok:false` (graceful, not a crash)**.
- Deterministic — re-run is byte-identical / idempotent.
- Cross-python-version safe (engine runs under OpenClaw's conda py3.11, not just system py3.x).
- `SKILL.md` metadata is **single-line JSON**; inputs/outputs/gates documented.
- No hardcoded test case — handles any ligand/system.

### Report / writeup
- Every claim sourced; every link resolves.
- Ruthless-editor format (per [[phase1-report-format]]): tight exec summary, matrix discipline, fluff cut.
- No unverified assertions presented as fact; confidence/tier marked.

### Handoff / Dev_Log
- Format matches prior entries (reverse-chrono marker+pointers for Dev_Log; recap + pasteable prompt + scope-fence for handoffs).
- Banked decisions front-loaded; scope-fence visible without scrolling (handoffs).
- All `[[wikilinks]]` / memory references resolve by exact slug.
- Marker + pointers, not a duplicate of the work.

## Anti-patterns (these fail the rubric even if gates are green)
- Declaring "done" on self-attestation alone — no independent/adversarial check.
- Treating an LLM "looks good" as verification — deterministic gates come first; the LLM review is adversarial, on top.
- Silently narrowing scope (top-N, sampling, "skipped X") without saying so.
- Picking a key decision (target, parameters) unilaterally instead of the pre-run gate.
- Over-reading a single-trajectory ΔG as a real binding affinity.

## Cross-links
- memory [[feedback-verify-and-eval]] — the working practice this rubric operationalizes.
- memory [[feedback-autonomous-vault]] — the autonomy boundary (vault upkeep stays act-don't-ask; this gate is for key run/build decisions).
- memory [[antechamber-aromatic-kekulize-bug]] — why deterministic + adversarial verification matters here.
- `eval-happy-path` skill / `/eval-happy-path` — the deterministic MD-run gate, already automated.
