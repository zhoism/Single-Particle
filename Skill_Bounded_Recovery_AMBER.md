---
tags: [amber, error-handling, runtime, mdout, shake, dt]
---
# Skill: AMBER Bounded Runtime Recovery

> **Vault tier: ✅ Paper-cited (strongest in the vault)** — arXiv:2603.25522 *explicitly* supports "bounded recovery from runtime failures" and demonstrates it in a **methane-oxidation reactive MD case study**. NotebookLM-verified 2026-05-19. Quote this case study in the report when defending the bounded-recovery approach.
>
> **✅ BUILT 2026-06-10 — realized as the `amber-recover` skill** (project-prime `8a1e849`): deterministic mdout crash detector (NaN/Infinity sticky, SHAKE-fail, non-finite final block; transient overflow/finite-vlimit tolerated) → **Tier 1** checkpoint-restore as-is → **Tier 2** bounded dt-lower/SHAKE-off stabilize-then-restore (every mutated namelist re-gated by vendored `check_amber`) → bounded **HALT** `needs_human`. Wired into `run_happy_path.sh` via the opt-in, **detector-authoritative** `scripts/recover_hook.sh` (catches the silent NaN/Infinity-with-banner class amber-md-run's own check misses). See [[Dev_Log]] 2026-06-10 (cont.).

**The User Pain Point:** MD simulations require constant babysitting. They can crash at any time (e.g., massive temperature spikes, coordinate overflows). The researcher must manually parse the `mdout` file, diagnose the failure, and manually edit the `mdin` configuration to salvage the run.

**The OpenClaw Solution:**
A reactive detection and recovery skill governed by strict mathematical limits, *not* LLM hallucination.
* **Deterministic Detection:** The agent monitors the `mdout` file. The detection of runtime instability (e.g., coordinate overflow) is triggered deterministically via regex or log parsing, not by agentic reasoning.
* **Bounded Recovery:** The agent's reaction is strictly mathematically defined. 
    * *Example Protocol:* If a temperature spike crashes the system, the agent automatically applies a bounded fix: temporarily lower the integration time step (`dt`) to a highly conservative value and disable the "SHAKE" algorithm. 
    * Once the system stabilizes over a set number of steps, the agent resumes normal parameters.
* **Friction Reduced:** Eliminates manual log parsing and "babysitting" while ensuring the AI cannot invent physically impossible simulation parameters.

## Two recovery philosophies (2026-05-18)

The Round-2 survey surfaced a direct design counterpoint. Schrödinger's **Multisim** ([[Arch_Schrodinger_FEP]]) *can* mutate parameters — but only when a human manually restarts with the `-set` flag. Its **automatic** crash response is a bitwise-accurate checkpoint-restore with identical config; it never *autonomously* diagnoses instability or adjusts `dt`/SHAKE. The differentiator is therefore **autonomy**, not capability.

| | Multisim automatic path (Schrödinger) | Bounded parameter mutation (this skill) |
|---|---|---|
| On crash, who decides the fix? | Nobody — restore checkpoint as-is. Mutation only if a human manually restarts with `-set` | The agent, autonomously, within hard mathematical limits |
| Safety | Very high — automatic path changes no physics | Needs the mathematical-bounds guardrail to be defensible |
| Fixes root cause unattended? | **No** — physically unstable system just re-crashes from the checkpoint | Yes — conservative `dt` / SHAKE-off lets the system settle, no human needed |
| Industry default? | Yes | No (more ambitious) |

**Resulting design — tiered recovery (do both):**
1. **Tier 1 (safe, default):** on crash, restore the last good checkpoint and resume *as-is*. Handles transient hardware/timeout failures with zero physics risk.
2. **Tier 2 (escalation):** only if Tier 1 re-crashes at/near the same step does the agent apply the bounded parameter mutation (lower `dt`, disable SHAKE) within hard limits, then resume normal parameters once stable.

This makes the skill defensible against the "you're letting an AI change physics" critique: parameter mutation is the *escalation*, never the first move. See [[Design_Determinism_Spectrum]] for the positioning argument.

**Source:** User pain-point analysis in [[Research_Phase1_Survey]] (Runtime Instability section); recovery-philosophy contrast from Round-2 competitive research, 2026-05-18.