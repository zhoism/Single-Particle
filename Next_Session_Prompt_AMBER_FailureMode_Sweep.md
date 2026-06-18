---
tags: [project-prime, openclaw, amber, gates, failure-modes, session-handoff, research, gap]
type: handoff
status: ready
created: 2026-06-12
---

# Next Session Starter — Systematic AMBER Failure-Mode Sweep → Gate Backlog

> Created 2026-06-12 during the report-walkthrough teaching session. **This is a RESEARCH + BACKLOG session, not a wholesale build.** Goal: do the *systematic* dive into AMBER's documented failure modes that we have **never done** — and turn it into a prioritized, reviewed backlog of candidate gates. Today the gate set is the union of (textbook physical-realism limits in `check_amber`) + (the handful of silent failures we personally crashed into or surfaced adversarially). That is **reactive + opportunistic, not systematic.** This session front-loads the field's *known* footguns instead of waiting to hit them. Product = a vault survey note + a gap note + a prioritized gate backlog. Paste the §The prompt to paste block into a fresh Claude Code session (run from the vault).

## Why this session exists (the seed — don't re-derive)

During the 2026-06-12 report walkthrough, the user asked the sharp question: *"Have we genuinely taken into account most of the field's accumulated knowledge? Have we even done a dive into AMBER's possible errors?"* Honest answer: **no.** The current gate set:

- **`check_amber` bounds** — real field knowledge, but the *shallow* end (dt ≤ 2 fs + SHAKE, non-bonded `cut` range, sane thermostat/barostat). Textbook, not subtle.
- **Reactively-encoded pitfalls** — aromatic kekulize ([[antechamber-aromatic-kekulize-bug]]), save-order (dry saved after solvation), `HIE/CYX` phantom-ligand resnames, `UNMAPPED_NONSTANDARD_RESIDUES`, NaN/Infinity/SHAKE-fail crash signatures. Found by **crashing into them** or by adversarial review — *then* encoded. Not from a survey.
- **Reference material we have but never mined** — the Amber26 manual ([[amber26-pdf-section-map]], "too big to whole-read"), the 66-skill upstream library ([[upstream-chemistry-skills-library]], "cite don't depend"). Neither systematically mined for failure modes.

**The gap:** there is a large, *documented* corpus of "ways AMBER silently does the wrong thing" — the AMBER mailing-list archives (the canonical repository), the manual's known-limitations sections, documented GAFF/antechamber mis-typing cases, common `tleap`/MMPBSA failures — and **our gate set is not derived from it.** This session closes that gap by surveying it and producing a backlog, so report claims can move from "we encode what we hit" toward "we systematically cover the field's known failure modes."

## Decisions banked — do NOT re-litigate

- **This is RESEARCH + a prioritized BACKLOG, not a build sprint.** Survey → catalogue → prioritize → (optionally) encode the top 1–3 *only if* each clears the full gate discipline below. Do NOT bulk-add unreviewed gates to the wrappers. The deliverable is the survey + backlog; encoding is a scoped follow-on.
- **The deterministic core stays frozen unless a gate earns its way in.** Every new gate must follow the same discipline as every existing one ([[Eval_Criteria]]): it is a **cheap deterministic proxy invariant** (true when the step worked, false when it broke — NOT a general "is the science correct" oracle, which cannot exist), it gets an **oracle/regression test**, it survives **adversarial review** (does it actually fire? does it false-alarm on valid runs? is it vacuous?), and it is **committed to git**. A candidate gate is `inferred` until it clears all four — never trusted on first proposal.
- **No auto-generated / self-evolving gates.** (Standing thesis — see [[Design_Determinism_Spectrum]] and the parallel [[Next_Session_Prompt_HermesAgent_Eval|Hermes eval]].) An LLM may *propose* candidate failure modes from the survey; it never *authors a trusted gate*. Faster discovery, same trust bar.
- **Honesty over coverage claims.** The whole point is to make the report claim *narrower and defensible*: "covers physical-realism limits + surveyed known failure modes, acknowledged-incomplete," NOT "encodes the field's accumulated knowledge." Do not overclaim completeness even after the sweep.

## What's NOT done (deferred, non-blocking — this session resolves them)

- **No systematic survey exists.** The AMBER mailing list, the manual's known-limitations, GAFF/antechamber mis-typing cases, common `tleap`/MMPBSA caveats have never been swept for failure modes.
- **No gap note exists** for gate-coverage incompleteness. Decide on `Gap_Gate_Coverage.md` (`status: open` → `partially-filled` after this session).
- **No backlog artifact.** Decide the vault note (`Research_AMBER_Failure_Modes.md` survey + a prioritized candidate-gate table: failure mode | how it manifests | silent-or-loud | proposed proxy invariant | which skill | priority | already-covered?).
- **No de-duplication against existing gates.** The session must first inventory the *current* gate set (from `check_amber` + each wrapper) so it proposes only genuinely new gates.

## The prompt to paste

```
Continuation of the Single Particle / OpenClaw + AMBER project. This is a RESEARCH + BACKLOG session (NOT a build sprint, NOT a migration): do the systematic dive into AMBER's documented failure modes that we have never done, and turn it into a prioritized, reviewed backlog of candidate gates. The pipeline is feature-complete (nine green deterministic-wrapper skills); do NOT modify it wholesale.

Read these BEFORE acting (in this order):
- vault: Next_Session_Prompt_AMBER_FailureMode_Sweep.md (THIS plan — the seed, the gate discipline, the banked guards)
- vault: Eval_Criteria.md (the gate discipline: proxy invariant → oracle test → adversarial review → commit); Design_Determinism_Spectrum (why gates matter + why we never auto-generate them); amber26-pdf-section-map memory (the manual jump-table — LEaP/Antechamber/sander/pmemd sections)
- memory: project-prime-status (the nine skills + what each gate currently is), antechamber-aromatic-kekulize-bug (the canonical silent-failure → gate example — the template for what a good gate looks like), upstream-chemistry-skills-library (66 read-only SKILL.md files to mine for encoded pitfalls), feedback-verify-and-eval (verify, don't self-attest)
- check vocabulary.md before introducing any new term.

Decisions banked, do NOT re-litigate:
- Research + prioritized backlog only. Encode AT MOST the top 1-3 candidates, and ONLY if each clears the full discipline (proxy invariant + oracle test + adversarial review + git commit). Do NOT bulk-add unreviewed gates.
- The deterministic core stays frozen; a gate is `inferred` until it clears all four discipline steps. No auto-generated / self-evolving gates — the LLM proposes candidates, never authors a trusted gate.
- Honesty over coverage: the goal is a NARROWER, defensible report claim, not "we cover everything."

Immediate sequence:

1. INVENTORY THE CURRENT GATE SET (so we don't propose duplicates). Read check_amber + each wrapper's gates; list every gate we already have, by skill. One table.

2. SYSTEMATIC SWEEP (the core) — go to PRIMARY sources for documented AMBER failure modes, per pipeline stage:
   a. antechamber / GAFF parameterization — documented mis-typing cases, charge-fitting failures, aromaticity/protonation pitfalls.
   b. tleap build / solvation — common silent corruptions (atom naming, missing params, save-order, box/ion issues).
   c. pmemd/sander run — instability signatures beyond NaN (vlimit, SHAKE failures, ewald errors, restart/coordinate issues).
   d. cpptraj / MMPBSA analysis — atom-count/mask mismatches, igb/saltcon caveats, single-trajectory ΔG misuse.
   e. PLIP / post-processing — resname footguns (already partly covered — confirm scope).
   Sources: the Amber26 manual known-limitations sections, the AMBER mailing-list archives (the canonical footgun repository), the upstream 66-skill library, documented GAFF/antechamber issues. For EACH failure mode found: does it manifest silently or loudly? what cheap deterministic proxy invariant would catch it? which skill owns it? is it already covered?

3. PRIORITIZE — rank candidates by (silent > loud) × (likelihood) × (cheap-to-check). Silent failures that pass current gates are top priority (that is the whole thesis — see antechamber-aromatic-kekulize-bug).

4. SECOND-PASS ADVERSARIAL CHECK (Eval_Criteria step 4): for the top candidates, a skeptic asks — would this proxy actually fire on the real failure? would it false-alarm on valid runs? is it vacuous (looks like a check, never triggers)? Drop the ones that don't survive.

5. RECORD:
   a. Create Research_AMBER_Failure_Modes.md — the survey + a prioritized candidate-gate table (failure mode | manifests silent/loud | proposed proxy invariant | owning skill | priority | already-covered).
   b. Create/Update Gap_Gate_Coverage.md (status: open → partially-filled) — the coverage gap is now surveyed, not closed.
   c. OPTIONALLY encode the top 1-3 (only if each clears proxy + oracle test + adversarial review); commit local.
   d. devlog-append; if durable, update project-prime-status memory with the survey outcome + the narrower defensible report claim.

Stop conditions:
- If encoding a candidate would require touching run_happy_path.sh or restructuring a wrapper, STOP and surface it — wire-in is a separate scoped decision.
- If the sweep surfaces a CURRENTLY-SHIPPING silent failure (a gate we thought existed but doesn't, or one that's vacuous), STOP and flag it loudly — that is a correctness issue, not a backlog item.

Scope-fence: SURVEY + PRIORITIZED BACKLOG of AMBER failure modes ONLY. Encode at most the top 1-3, fully disciplined. Do NOT bulk-add gates, do NOT modify run_happy_path.sh, do NOT auto-generate gates, do NOT push.
```

## After the session — update this file

1. Flip frontmatter `status: ready` → `status: consumed`.
2. Add a `## Outcome` footer: consumed YYYY-MM-DD, how many failure modes surveyed, how many genuinely-new candidate gates found, how many encoded (if any), link to `Research_AMBER_Failure_Modes.md` + `Gap_Gate_Coverage.md` + the [[Dev_Log]] entry.
3. If encoding the top candidates spawns a wire-in decision, note the follow-on handoff.

## Cross-links

- [[Eval_Criteria]] — the gate discipline (proxy invariant → oracle test → adversarial review → commit) every candidate must clear.
- [[Design_Determinism_Spectrum]] — why gates matter, and why we never auto-generate them.
- [[antechamber-aromatic-kekulize-bug]] — the canonical silent-failure → gate example; the template for a good gate.
- [[amber26-pdf-section-map]] — the manual jump-table the sweep mines.
- [[upstream-chemistry-skills-library]] — 66 read-only skills to mine for encoded pitfalls.
- memories: [[project-prime-status]], [[feedback-verify-and-eval]].
- Sibling research handoff: [[Next_Session_Prompt_HermesAgent_Eval]] (same "propose-then-verify, never auto-author" discipline).
