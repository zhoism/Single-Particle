# Canonical 11-stage advisor recipe

Source: `phase3-explicit-solvent-md/` (advisor handoff 2026-06-01). Per `phase3_advisor_demo` memory.

## Stage sequence

```
min1 → min2 → heat-1 → press-1 → heat-2 → press-2 → heat-3 → press-3 → relax → prod
```

Plus implicit Stage 0: `tleap` builds `complex.parm7` + `complex.rst7` from PDB + ligand frcmod/lib.

## Per-stage shape (the rule envelope the validator enforces)

| Stage | imin | ntx | irest | nstlim | dt | ntr | mask released | ntp | barostat | tempi → temp0 | nmropt |
|-------|------|-----|-------|--------|-----|-----|--------------|------|----------|----------------|--------|
| min1 | 1 | — | — | — | — | 1 | no (heavy restraint) | 0 | — | — | 0 |
| min2 | 1 | — | — | — | — | 1 | no (lighter) | 0 | — | — | 0 |
| heat-1 | 0 | 1 | 0 | 50000 | 0.002 | 1 | no | 0 | 2 (cosmetic) | tempi=0 → 100 (&wt) | 1 |
| press-1 | 0 | 5 | 1 | 50000 | 0.002 | 1 | no | 1 | 2 (MC) | 100 | 0 |
| heat-2 | 0 | 5 | 1 | 50000 | 0.002 | 1 | no | 0 | 2 (cosmetic) | tempi=100 → 200 (&wt) | 1 |
| press-2 | 0 | 5 | 1 | 50000 | 0.002 | 1 | no | 1 | 2 (MC) | 200 | 0 |
| heat-3 | 0 | 5 | 1 | 50000 | 0.002 | 1 | no | 0 | 2 (cosmetic) | tempi=200 → 310 (&wt) | 1 |
| press-3 | 0 | 5 | 1 | 50000 | 0.002 | 1 | no | 1 | 2 (MC) | 300 | 0 |
| relax | 0 | 5 | 1 | 5,000,000 | 0.002 | 0 | YES | 1 | 2 (MC) | 300 | 0 |
| prod | 0 | 5 | 1 | 5,000,000 | 0.002 | 0 | YES | 1 | 2 (MC) | 300 | 0 |

## Restraints

- `restraintmask = "!:WAT,Cl-,K+,Na+ & !@H="` — everything that is not water or counter-ion or hydrogen, i.e., the heavy atoms of protein + ligand.
- `restraint_wt = 5.0` kcal/mol/Å² through heat/press cycles.
- Released at `relax` (`ntr=0, restraint_wt=0`).

## Common settings (constant across non-min stages)

- `dt = 0.002` ps (2 fs, matches SHAKE)
- `cut = 9.0` Å (explicit solvent non-bonded cutoff)
- `ntc = 2, ntf = 2` (SHAKE on bonds-to-H)
- `ntt = 3, gamma_ln = 2.0, ig = -1` (Langevin thermostat)
- `pres0 = 1.0, taup = 2.0` (MC barostat reference)

## Production output cadence

- `ntpr = 10000` (energy log every 10k steps = every 20 ps at dt=0.002)
- `ntwx = 10000` (trajectory write every 20 ps)
- `ntwr = 10000` (restart write every 20 ps)
- `ioutfm = 1` (NetCDF binary trajectory)
- 5,000,000 steps × 0.002 ps = **10 ns production**

## Submit chain

`pmemd -O -i <stage>.in -p complex.parm7 -c <prev>.rst7 -ref <prev>.rst7 -o <stage>.out -r <stage>.rst7 -x <stage>.nc -inf <stage>.info`

(min stages drop `-x`; min1 uses `complex.rst7` as both `-c` and `-ref`.)

## Known issues in the advisor handoff

Both flagged by the validator on actual `phase3-explicit-solvent-md/` files:

1. **`heat-3.in`**: `&cntrl temp0=300.0` but `&wt TEMP0 value2=310.0`. Langevin follows the &wt-set TEMP0 → system ramps to 310 K. Author intent unclear; confirm.
2. **`submit.sh`**: `AMBERHOME=/Application/software/Amber26/pmemd26` — advisor's machine. Local pmemd is at `~/Downloads/pmemd26/`. Replace with `AMBERHOME` from env or `which pmemd` resolution before running.

Bonus catch: `prod.in` has `iwrap=0` with `nstlim=5,000,000`. Set `iwrap=1` for long production to prevent trajectory diffusion artifacts.
