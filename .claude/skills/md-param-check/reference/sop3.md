# SOP §3 — Physical Realism Hard Limits

From project `CLAUDE.md`: "Physical realism is non-negotiable for MD parameters — enforce hard limits like `dt ≤ 2fs`, non-bonded `cut` ranges, SHAKE constraints."

## Why these are non-negotiable

The LLM reasoning layer can suggest plausible-looking parameters that are physically wrong. Real-world consequences:

- `dt = 0.004` "to run faster" → SHAKE breaks, energy drifts, simulation blows up. The LLM doesn't know this from prose alone.
- `cut = 6.0` "for speed" → too short for PME error cancellation in explicit solvent, electrostatics wrong, ensemble corrupted.
- SHAKE off with `dt = 0.002` → bond-stretching modes integrated unstably, NaN within picoseconds.

These are the runtime crashes `Skill_Bounded_Recovery_AMBER` is supposed to fix. Best to not cause them in the first place.

## The limits

### `dt` (integration timestep)

- **With SHAKE (`ntc=2, ntf=2`)**: hard cap `dt ≤ 0.002` ps (2 fs).
- **Without SHAKE**: hard cap `dt ≤ 0.001` ps (1 fs).
- Why: SHAKE freezes the highest-frequency bonds (X–H stretch, ~10 fs period). With SHAKE, the next-fastest mode (heavy-atom bond stretch, ~30 fs period) sets the stability ceiling at 2 fs. Without SHAKE, the X–H stretch sets the ceiling at 1 fs.

### `cut` (non-bonded cutoff, Å)

- **Explicit solvent (water box)**: `8.0 ≤ cut ≤ 12.0`. Advisor demo uses 9.0.
- Why: too short → PME long-range correction breaks down; too long → wasted compute, no accuracy gain.

### SHAKE constraints

- `ntc=2, ntf=2` — bonds involving H constrained AND skipped in force evaluation. The standard.
- `ntc=2, ntf=1` — bonds constrained but force still computed. Wastes compute; inconsistent.
- `ntc=1, ntf=1` — no SHAKE. Requires `dt ≤ 0.001`.
- `ntc=3, ntf=3` — all bonds. Rarely used (overconstrains).

### Langevin thermostat (`ntt=3`)

- `gamma_ln` typically in `[1, 5]` ps⁻¹. Advisor demo uses 2.0.
- Lower (e.g., 0.1) → weak coupling, slow thermalization.
- Higher (e.g., 10) → overdamped, can affect dynamics.
- `ig = -1` for randomized seed (default best practice).

### Barostat (when `ntp=1`)

- `barostat=2` — Monte Carlo barostat, standard for explicit-solvent NPT.
- `barostat=1` — Berendsen, deprecated for production (incorrect fluctuations).
- `taup = 2.0` ps — relaxation time. Advisor demo standard.

### Restraint mask

- Must be valid AMBER atom-mask syntax (see Amber26.pdf ch.25 p.509).
- Advisor demo: `!:WAT,Cl-,K+,Na+ & !@H=` — everything that is NOT water/counter-ion AND NOT hydrogen, i.e., heavy atoms of protein + ligand.
- `!` = negate; `:` = residue name match; `@` = atom name match; `=` = wildcard.

### Production trajectory hygiene

- `iwrap=1` for `nstlim` above ~1M steps — wraps coordinates back into the box to prevent diffusion artifacts in the saved trajectory.
- `ioutfm=1` — NetCDF binary trajectory (vs `0` = ASCII). Faster I/O, smaller files.
- Trajectory cadence (`ntwx`) typically 10k–50k steps for routine production (every 20–100 ps).

## What the validator does NOT check

These need a domain-specific extension (out of scope for the default validator):

- QM/MM (`ifqnt=1`) — different parameter envelope.
- λ-windows / REMD — multiple coupled inputs, ensemble-level checks.
- Free energy with bond-breaking — SHAKE not applicable.
- Implicit solvent (`igb`) — `cut` rules differ.
- Steered MD (`jar=1`) — additional pulling parameters.

When you hit these, escalate to manual review against Amber26.pdf section §23.6 (sander keywords) + the relevant feature chapter.

## Source

- Project `CLAUDE.md` §3 (the SOP itself).
- Amber26.pdf §23.6 — sander keyword source-of-truth, p.429.
- Amber26.pdf §24.3 — pmemd-specific deviations from sander, p.499.
- Amber26.pdf ch.25 — atom mask syntax, p.509.
- `phase3_advisor_demo` memory — the canonical 11-stage exemplar.
