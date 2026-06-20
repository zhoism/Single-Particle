---
tags: [project-prime, amber, gates, failure-modes, research, gap]
type: research
status: survey-complete
created: 2026-06-19
---

✅ **Source-cited survey** (Amber26 manual + AMBER mailing-list archives + the upstream 66-skill library + the live wrapper code). Produced 2026-06-19 by the systematic failure-mode sweep called for in [[Next_Session_Prompt_AMBER_FailureMode_Sweep]]. This is the **first systematic** dive into AMBER's documented footguns — the prior gate set was reactive (textbook `check_amber` limits + the handful we crashed into). **Honest scope:** this surveys *known* failure modes per pipeline stage and turns them into a reviewed, prioritized **candidate-gate backlog**. It does **not** claim completeness, and (per the discipline) **no gates were encoded** — every candidate is `inferred` until it clears proxy-invariant + oracle-test + adversarial-review + commit ([[Eval_Criteria]]). Method: 5 per-stage finders (38 candidates) → adversarial verifiers → 15 kept (P1=4 / P2=7 / P3=4), 23 dropped.

# AMBER failure-mode survey → prioritized candidate-gate backlog

## 🚩 CONFIRMED CURRENTLY-SHIPPING DEFECT — `SYSTEM_NOT_NEUTRAL` is a dead gate

> This is a **correctness finding, not a backlog item** (the sweep's STOP condition). Flagged loudly, then **FIXED this session** (project-prime `5647b0a`) after the user asked to proceed — see the resolution below. Verified independently across all 13 production `leap.log`s — not taken on the agent's word.

`tleap-build/scripts/wrapper.py` intends to gate post-neutralization charge:
```python
m = re.search(r"unperturbed charge:\s*(-?\d+\.\d+)", s)   # parse_leap_log
...
if rc is not None and abs(rc) > 0.5:                       # validate
    errors.append(f"SYSTEM_NOT_NEUTRAL: residual charge {rc} after addions2")
```
**What actually happens** (measured, 2026-06-19):
- On **every real skill run** (13/13 production `*/build/tleap-build-run/leap.log`), the regex matches **nothing** → `residual_charge = None` → **the gate never fires.** It is **vacuous on 100% of the production path.**
- The only logs where it *does* match are non-skill hand-runs (`golden-path/leap.log` → captures `Total unperturbed charge: 8.000000`). There the captured value is the **pre-neutralization** complex charge (the line precedes `addions2`), so the gate would **false-fire `SYSTEM_NOT_NEUTRAL` on a perfectly valid charged protein.**

**Net:** the gate provides **zero** neutrality protection on the shipping pipeline, and is actively wrong when it triggers. **Do not "just fix the regex"** — capturing `Total unperturbed charge:` would make it flag every charged protein (e.g. golden-path's +8) as non-neutral and break GREEN runs.
**Resolution — IMPLEMENTED 2026-06-19 (project-prime `5647b0a`, master, local-only, not pushed).** Neutrality is now computed structurally from the **prmtop CHARGE block** of `comp_oct.top` — new `prmtop_net_charge()` helper: sum ÷ 18.2223 → net charge in e, fire `SYSTEM_NOT_NEUTRAL` when `abs > 0.5`. Phrasing/path-independent; measures the *actual* built system rather than scraping a log. The misleading `residual_charge` log-parse was removed; the envelope now exposes `net_charge_e`. Verified: oracle (neutral/+2/−1/+0.3/+0.6/malformed) + regression over **all 48 real `comp_oct.top` builds** (worst |net| 1e-6 e → 0 false-alarms), green under py3.11 (conda) + py3.14 (system); live `validate()` on the 1L2Y GREEN build emits `net_charge_e` and does not false-fire. `run_happy_path.sh` untouched. Test: `skills/tleap-build/tests/test_neutrality_gate.py`.

---

## How the current gate set was characterised (dedup baseline)

The sweep first inventoried the ~80 existing deterministic gates (in `check_amber` + each of the 9 wrappers) so it would propose only genuinely new checks. Summary of the *existing* coverage: physical-realism limits (dt/SHAKE/cut/thermostat/barostat), antechamber output sanity (charge sum, untyped atoms, frcmod ATTN, `AROMATIC_PERCEPTION_FAILED`), tleap structural invariants (atom counts, dry<solvated, component sum, residue-identity), MD crash signatures (`amber-md-run` post-scan + `amber-recover`'s NaN/Inf/SHAKE/box/overflow detector), planner G0–G6, and PLIP resname/phantom guards. Full table: see the sweep transcript + the gate-inventory recon in [[Dev_Log]] 2026-06-19.

## Prioritized candidate-gate backlog (15 kept)

Priority = (silent > loud) × likelihood × cheap-to-check. **P1 = silent AND likely AND cheap.** Every candidate was adversarially checked for *would-it-actually-fire / false-alarm / vacuous* before being kept.

### P1 — encode first (each still pending the full discipline)

| # | Failure mode | Stage / skill | Silent? | Proposed proxy invariant | Note from adversarial review |
|---|---|---|---|---|---|
| 1 | **GB radii ↔ igb mismatch** — `cpptraj-analysis` hardcodes `igb=5` but tleap saves prmtops with default `mbondi` radii; Amber26 Table 4.1 says igb=5 *requires* `mbondi2`. Solvation term silently computed under wrong radii. | cpptraj-analysis (root cause in tleap-build) | yes (ΔG stays negative, fires on **every** run today) | grep prmtop `%FLAG RADIUS_SET`; assert it matches igb via Table 4.1 map (igb 1→mbondi, 2\|5→mbondi2, 7→bondi, 8→mbondi3). | Verified against real prmtops: they read "modified Bondi radii (mbondi)". Discrete internal-consistency invariant, not a science oracle. True fix is upstream (`set default PBRadii mbondi2` in tleap) — touches the build, so STOP-and-surface. |
| 2 | **`SOLVENT_NOT_ADDED` (zero waters)** — `solvateoct` adds ~0 waters yet a few neutralizing ions push `oct>dry`, so the existing dry<solvated gate passes; explicit-solvent MD runs in vacuum. | tleap-build | yes | assert WAT count in `comp_oct.top` RESIDUE_LABEL ≥ floor (≥100; real runs are 1890–8290) **and** `solvent_residues_added > 0`. | Prmtop-WAT-count is the load-bearing half (the log-regex half shares the brittleness that killed SYSTEM_NOT_NEUTRAL). Cleanest/safest new gate; addresses a known hole. |
| 3 | **`CROSS_GAP_SPURIOUS_BOND`** — a missing-residue gap / chain break without a TER card makes tleap bond across the gap (>100 Å bond), emitted only as a `WARNING` that `parse_leap_log` drops (it keeps only ERROR/FATAL). | tleap-build | yes | scan `leap.log` for `bond of\s+([0-9.]+)\s+angstroms`; assert no captured length > ~3.0 Å. | Common on raw/fetched crystal PDBs (the arbitrary-target path). Caveat: it scrapes tleap's *own* warning — a log-scraper, not a geometry oracle; bound needs tuning. |
| 4 | **PLIP non-deterministic re-protonation** — wrapper calls PLIP without `--nohydro`; PLIP strips tleap's H and re-adds via non-deterministic OpenBabel, breaking the skill's advertised byte-identical determinism and able to flip H-bond/salt-bridge calls. | plip-profile | yes | (a) hard-assert `--nohydro` is in the PLIP argv (tleap H are authoritative); (b) run PLIP twice on a fixed frame, require identical `totals.by_type`. | The argv assertion fires on today's code and is zero-false-alarm. The twice-run-diff half over-triggers until `--nohydro` lands. Trade-off: `--nohydro` shifts trust to OpenBabel bond perception — a real decision, not free. |

### P2 — useful, but louder / rarer / needs tuning (7)

| Failure mode | Stage | Proxy invariant (with the review's caveat) |
|---|---|---|
| **SQM SCF non-convergence with output emitted** — sqm exits 0 after a partial/failed AM1 SCF; charges meaningless but sum rounds to `-nc`. | antechamber | parse `sqm.out` for `Calculation Completed` + finite final SCF block; **anchor on the LAST block** — do NOT ban every "Unable to achieve self consistency" (benign mid-minimization warnings are normal). |
| **Wrong/odd multiplicity default** — `-m` defaults to singlet; an odd-electron inventory under enforced singlet is electronically impossible. | antechamber | assert `(ΣZ − nc)` is EVEN when `-m=1`. Fires only on the H-present-PDB / mol2 passthrough paths (obabel paths auto-saturate). Closed-shell ions stay EVEN → low false-alarm. |
| **Missing-H / wrong protonation state** — under-protonated carboxylate/amine typed silently. | antechamber | primary detector = grep antechamber log for `assigned bond types may be wrong` / acdoctor `unfilled valence`; valence-sum cross-check **only for neutral ligands** (carboxylates false-alarm the naive version). |
| **Missing heavy atoms rebuilt from internal coords** — disordered side-chain tips rebuilt into clashing rotamers; NATOM matches template so gates stay green. | tleap-build | non-fatal FINDING: count `Added missing heavy atom` for **side-chain** atoms only (exclude OXT/terminal completions — real GREEN runs already emit one OXT add) + surface `Close contact` warnings. As written (count==0) it would red-flag the project's own GREEN builds. |
| **Water-model ↔ box mismatch** — wrapper hardcodes `TIP3PBOX` regardless of `--water`; a non-tip3p `--water` silently builds a tip3p box. | tleap-build | derive box token from `--water` via a fixed map; assert the leap.in box matches. Dormant today (nothing passes non-tip3p) but `--water` is agent-exposed via the planner registry. Better fix: derive box from `--water` (removes the bug). |
| **MMPBSA finite-avg with non-finite std-dev** — partial-frame corruption gives a finite ΔG with `nan`/`****` std-dev; only gate is `dG<0`. | cpptraj-analysis | extend the DELTA-TOTAL regex to capture 3 cols; assert avg **and** std-dev finite. **Drop** the `stddev > k·|avg|` magnitude heuristic (false-alarms on legit near-zero-ΔG / short-trajectory runs — it's a disguised science oracle). |
| **Backbone-medoid not binding-pose representative** — medoid picked on `@CA,C,N` only; ligand can be mid-drift while backbone is at the fold average. | plip-profile | non-fatal note: pocket-fit, then no-fit ligand-heavy RMSD of the chosen frame vs ligand-average ≤ ~2× median per-frame. Must best-fit on protein (else measures tumbling). Threshold arbitrary → note, never fatal. |

### P3 — marginal / defense-in-depth / rare in scope (4)

`UNSUPPORTED_ELEMENT` pre-scan vs the GAFF allowlist (metals/B already loud via acdoctor-fatal; this is earlier/clearer UX) · `BURIED_COUNTERION` geometric check (addions2 shell algorithm structurally disfavors burial; expensive, false-alarm tail on surface ions) · `autoimage`-before-`strip` reorder + Rg-jump detector (marginal on the compact systems this pipeline runs) · multi-ligand / duplicate-same-resname site silently dropped (the distinct-resname cases are already caught by `UNMAPPED_NONSTANDARD_RESIDUES`; only the same-resname-duplicate sliver is novel).

## Dropped (recorded so they are not re-discovered) — 23 total; the instructive 5

- **INCORRECT_CONNECTIVITY_PERCEPTION** — same-atom-count wrong-bond-order typing needs a real correctness oracle (RDKit/obabel canonical perception), not an atom/bond count diff; the count-diff residual is redundant with `AROMATIC_PERCEPTION_FAILED`.
- **NONSTOICHIOMETRIC_NET_CHARGE vs sqm target** — "assert sqm Mulliken == requested `-nc`" is a **tautology** (sqm constrains the wavefunction to `qmcharge=-nc`); the wrong-`-nc` failure is invisible to any check reading only pipeline outputs.
- **PARMCHK2 zero-barrier placeholder without ATTN** — the zero value and the `ATTN` tag are the same line; already caught by the ATTN gate; empirically vacuous (0 ATTN, 0 populated BOND/ANGLE blocks across 31 real frcmods); dihedral clause false-alarms on legit zero-barrier Fourier terms.
- **AM1-BCC geometry-dependent spurious H-bonds** — a conformer-quality "is-the-science-correct" oracle (out of scope); rerouted to a `maxcyc=0` heuristic in `antechamber-ligandprep/references/heuristics.md` for future charged flexible ligands.
- **DISULFIDE_BOND_OMITTED** — **empirically false**: pdb4amber writes S-S CONECT by default and the wrapper never passes `--no-conect`; a live test confirmed the disulfide forms correctly with zero explicit `bond` lines. The proposed "count bond lines" proxy would false-fire on every disulfide protein.

The dropped set is itself a result: it shows the gate line where a *defensible deterministic proxy* exists vs. where only a *(non-existent) science-correctness oracle* would do — the boundary [[Design_Determinism_Spectrum]] predicts and [[Future_Work_Proposer_Agent]] formalizes ("capability is gated by the verifier, not the reasoning").

## Honest, defensible coverage claim (for the report)

> The pipeline encodes the **physical-realism hard limits** (`check_amber`) plus a **surveyed set of documented AMBER failure modes** across antechamber/tleap/pmemd/MMPBSA/PLIP — with a reviewed, prioritized backlog of the remainder and an **acknowledged-incomplete** posture. It does **not** claim to encode the field's full accumulated knowledge. One existing gate (`SYSTEM_NOT_NEUTRAL`) was found **non-functional** and has since been **repaired** (structural prmtop check, project-prime `5647b0a`).

## Cross-links
- [[Gap_Gate_Coverage]] — the coverage gap this survey partially fills (now `partially-filled`).
- [[Next_Session_Prompt_AMBER_FailureMode_Sweep]] — the handoff that scoped this (now `consumed`).
- [[Eval_Criteria]] — the proxy-invariant → oracle-test → adversarial-review → commit discipline every candidate must clear before encoding.
- [[Design_Determinism_Spectrum]] — why these are gates (cheap deterministic proxies), and why a "is the science correct" oracle is out of scope.
- [[antechamber-aromatic-kekulize-bug]] — the canonical silent-failure→gate template this survey generalizes.
- [[Future_Work_Proposer_Agent]] — "capability is gated by the verifier" — this backlog *is* expanding the verifier.
