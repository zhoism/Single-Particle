---
description: Evaluate the local AMBER MD happy path (Stages 2–5) end-to-end with deep QC
argument-hint: [sim_ps]
allowed-tools: Bash(source:*), Bash(cd:*), Bash(bash:*), Bash(python3:*), Bash(git:*), Bash(ls:*), Bash(grep:*), Read
---

# Evaluate the local AMBER MD happy path

Run a deterministic, agent-free QC pass over the Stage 2–5 pipeline (antechamber → tleap → MD → cpptraj) on the 1L2Y golden fixture, then independently verify the outputs against the baked-in correctness rules. This is evaluation only — **never loosen a validation gate to make a check pass; if a gate fails, STOP and report the cause.**

Production length: `$ARGUMENTS` ps if given, else default **20** ps (fast full chain, ~5 min).

## 1. Pre-flight

```bash
source /opt/homebrew/Caskroom/miniforge/base/envs/prime-amber/amber.sh && export PATH="$HOME/Downloads/pmemd26/bin:$AMBERHOME/bin:$PATH"
for b in tleap cpptraj pmemd MMPBSA.py antechamber parmchk2 pdb4amber; do printf "%-12s " "$b"; which "$b" || echo MISSING; done
git -C "/Users/kevinzhou/Downloads/Single Particle/project-prime" log --oneline -1
```

Confirm every binary resolves (pmemd from `~/Downloads/pmemd26/bin`) and HEAD is the expected Stages-3–5 commit. If a binary is MISSING, fix the env before continuing.

## 2. Run the happy path

```bash
source /opt/homebrew/Caskroom/miniforge/base/envs/prime-amber/amber.sh && export PATH="$HOME/Downloads/pmemd26/bin:$AMBERHOME/bin:$PATH"
cd "/Users/kevinzhou/Downloads/Single Particle/project-prime" && bash run_happy_path.sh ${ARGUMENTS:-20}
```

Expect: 4 `ok:true` envelopes (`s2..s5.json`), then `HAPPY PATH GREEN` with ≥12 analyses, ≥10 PNGs, and a negative MM-GBSA ΔG.

## 3. Independent output QC — do NOT trust the envelopes; verify the artifacts

Let `OUT="/Users/kevinzhou/Downloads/Single Particle/project-prime/happy-path-run"`.

- **tleap (Stage 3):** from `$OUT/s3.json` confirm `validation.dry_atoms < validation.solvated_atoms` and `protein_atoms + ligand_atoms == dry_atoms`. In the generated `leap.in` under `$OUT/build`, confirm `saveamberparm comp comp_dry.top …` appears **before** `solvateoct` (comp_dry-before-solvate rule).
- **MD (Stage 4) — independent md-param-check probe:**

  ```bash
  python3 "/Users/kevinzhou/Downloads/Single Particle/Single Particle/.claude/skills/md-param-check/checks/check_amber.py" "/Users/kevinzhou/Downloads/Single Particle/project-prime/happy-path-run/md/"
  ```

  Expect `VERDICT: PASS` (or WARN). A `FAIL` (dt>2fs, SHAKE incoherent, cut out of range, hardcoded foreign path) means the namelist generator regressed — STOP. Also eyeball `md/heat.in` (`temp0` == `&wt … value2`) and `md/product.in` (`ntp=1 barostat=2 iwrap=1`).
- **cpptraj (Stage 5):** from `$OUT/s5.json` confirm `outputs.produced` has ≥12 entries and `mmgbsa_dG_kcal_mol < 0`; confirm `$OUT/analysis` holds ≥10 non-zero PNGs, a PCA projection artifact (two-call rule) and a clustering representative (`repout`).

## 4. Report

Summarize: pre-flight result, the 4 envelope verdicts, ΔG value, analysis/PNG counts, the `check_amber.py` verdict, and any correctness-rule check that did not hold. A green run with a violated rule is a **FAIL** — surface it, don't bury it.

> Scope: this command is the local deterministic QC spine. It does **not** drive skills through the OpenClaw gateway (the live-agent-turn) or touch Discord — those are separate, model-dependent evaluations.
