---
tags: [project-prime, openclaw, hermes-agent, session-handoff, research, evaluation, competitive-landscape]
type: handoff
status: consumed
created: 2026-06-11
consumed: 2026-06-27
---

# Next Session Starter — Hermes Agent: Research & Genuine Evaluation

> Created 2026-06-11 during a teaching/exploratory tangent. **This is a RESEARCH + EVALUATION session, not a build and not a migration.** Goal: genuinely evaluate **Hermes Agent** (Nous Research's open-source, self-hosted "OpenClaw alternative" agent framework, released ~Feb 2026) and decide, with evidence, *whether and where* it would couple with this project's OpenClaw + AMBER deterministic-wrapper pipeline. Product = a verdict + a vault note (and a decision on whether Hermes earns a row in the competitive-landscape section). Paste the §The prompt to paste block into a fresh Claude Code session (run from the vault).

## Why this session exists (the seed — don't re-derive)

A preliminary pass this session (2026-06-11) established the *framing*; the next session does the **genuine verification + evaluation** the framing demands. What we found at a glance (all **vendor/marketing + official-docs level — NOT independently verified**, which is precisely the next session's job):

- **What Hermes is:** same *category* as OpenClaw — model-agnostic agent gateway, skills, multi-channel front ends (Discord/Slack/CLI/Telegram/…), function-calling (the Hermes Function-Calling JSON-schema standard) + MCP. Marketed literally as "the OpenClaw alternative."
- **Its defining bet (the crux):** a **self-improving learning loop** — *"autonomous skill creation after complex tasks," "skills self-improve during use,"* agent-curated persistent memory, cross-session user modeling (Honcho), isolated subagents, FTS5 session search. This is the thing to verify hardest.
- **One genuine potential win for us:** first-class **local-LLM support** (Ollama / vLLM / llama.cpp / LM Studio). Since we already proved the LLM only does *cheap boundary work* (parse intent / pick skill), even a small local model suffices for the launch turn — which would **kill the 429 rate-limit dependency** that has repeatedly stalled the launch turn on free Gemini/Cerebras.

### The framing already worked out (use as the evaluation lens, then test it)

- **Determinism-spectrum placement:** Hermes sits at the *same pole as us* — "reasoning over a deterministic core" ([[Design_Determinism_Spectrum]]) — but leans hard toward the **self-evolution** side we deliberately *don't*. The sharp axis for the report: not "deterministic core: yes/no" (both say yes) but **"how much do you let the agent rewrite *itself*?"** Hermes bets on self-evolution; this project bets on a frozen, audited, reproducible core.
- **The firewall verdict (preliminary):** **front door = plausibly yes** (local model for the launch turn; persistent user model / memory — both touch only the boundary, never the science). **Engine room = no** — letting the learning loop auto-write/auto-mutate the chemistry wrappers reintroduces exactly the failure mode we engineered out: non-reproducible (skills change between runs, not in git), non-auditable (LLM-authored, unreviewed), and able to silently re-corrupt chemistry through code the LLM wrote (the gates exist to prevent this).
- **The one legitimately interesting coupling:** the learning loop feeding the **proposal** side of bounded recovery (accumulated "playbooks" for novel crash signatures) — but only as `inferred` proposals that *still pass `check_amber` + the bounded ladder* before any namelist is written. Better proposer inside propose-then-verify; never a trusted executable.
- **Collisions with banked decisions:** Hermes' isolated-subagent parallelism bumps the **max-3-named-agents** decision ([[multi-agent-scope]]); its self-evolving skills bump the **frozen-deterministic-core** thesis. Both are features we would deliberately *not* adopt — confirm that holds.

## Decisions banked — do NOT re-litigate

- **This is evaluation, NOT migration.** Do not port the pipeline to Hermes, do not edit `project-prime/` skills, do not touch `run_happy_path.sh`. The output is research + a verdict, not code. ([[feedback-verify-and-eval]] applies: deterministic-where-possible, then an honest verdict.)
- **The deterministic core stays frozen regardless.** The wrappers / `check_amber` / gates / byte-reproducibility are the thesis ([[Design_Determinism_Spectrum]], [[project-prime-status]]). Any Hermes feature that would let an LLM rewrite execution logic is out-of-bounds by design — the evaluation's job is to say so *with evidence*, not to relitigate the thesis.
- **Max 3 named agents** ([[multi-agent-scope]]) — Hermes' subagent swarm does not change this; skills absorb decomposition.
- **The LLM is model-agnostic and only does boundary work** — proven this project (Gemini ↔ Cerebras swap, identical science). A Hermes local-model launch turn is evaluated *within* that finding, not as a re-opening of it.
- **Precedent for this exact kind of session:** [[Research_El_Agente_Q]] (evaluate an external framework → bank a scope decision → memory `multi-agent-scope`). Match that format/rigor — verify claims, give a crisp ALIGNED / ALIGNED-WITH-CONCERNS / REJECT verdict, bank the decision, don't leave it open-ended.

## What's NOT done (deferred, non-blocking — this session resolves them)

- **No claim about Hermes is independently verified yet.** The learning-loop / auto-skills / persistent-memory descriptions are vendor + docs language. The single most load-bearing unknown: **does the loop edit literal skill *code*, or only higher-level skill *definitions*?** (Code-editing = strictly worse for our auditability/reproducibility argument.) Pin this down from the actual source.
- **No vault note exists for Hermes.** Decide on creating `Arch_Hermes_Agent.md` (or a `connections/` edge note vs [[OpenClaw_Self_Evolution]] / [[Design_Determinism_Spectrum]]) — Hermes is essentially "what if self-evolution were the *headline* feature," so it connects directly to the existing self-evolution note.
- **No decision on the competitive-landscape row.** Hermes may be a *better* landscape datapoint than Schrödinger/OpenEye (same pole, diverges on the self-rewrite knob). Decide whether it goes in the report's landscape section and draft the one-line positioning.

## The prompt to paste

```
Continuation of the Single Particle / OpenClaw + AMBER project. This is a RESEARCH + EVALUATION session (NOT a build, NOT a migration): genuinely evaluate Hermes Agent (Nous Research's open-source, self-hosted "OpenClaw alternative" agent framework, ~Feb 2026) and decide WITH EVIDENCE whether and where it would couple with our OpenClaw + AMBER deterministic-wrapper pipeline. The pipeline is feature-complete (nine green deterministic-wrapper skills); do NOT modify it.

Read these BEFORE acting (in this order):
- vault: Next_Session_Prompt_HermesAgent_Eval.md (THIS plan — the seed framing, the firewall verdict to test, the banked guards)
- vault: Design_Determinism_Spectrum (the spine — Hermes is "same pole, different bet on self-rewrite"); OpenClaw_Self_Evolution (the existing self-evolution note Hermes connects to); Eval_Criteria.md (the verdict discipline); Research_El_Agente_Q (the precedent: evaluate-a-framework → bank-a-scope-decision, match this rigor/format)
- memory: project-prime-status (CRITICAL — what the nine-skill pipeline is + the frozen-core thesis), multi-agent-scope (max 3 agents — Hermes subagents don't change it), feedback-verify-and-eval (verify don't self-attest; honest verdict), openclaw-canonical-paths (our current substrate facts, to contrast against Hermes)

Decisions banked, do NOT re-litigate:
- Evaluation only — no migration, no porting, no edits to project-prime/ or run_happy_path.sh.
- The deterministic core stays frozen; any Hermes feature that lets an LLM rewrite execution logic is out-of-bounds by design — say so WITH EVIDENCE, don't relitigate the thesis.
- Max 3 named agents; LLM is model-agnostic and only does boundary work (Gemini↔Cerebras proven).

Immediate sequence (evaluation ONLY):

1. VERIFY THE CLAIMS (the core of the session) — go to PRIMARY sources, not marketing:
   a. github.com/nousresearch/hermes-agent (source + docs) and the agentskills.io standard.
   b. Pin down THE load-bearing unknown: does the self-improving learning loop edit literal skill CODE, or only higher-level skill DEFINITIONS / prompts? Quote the mechanism.
   c. Confirm/refute: autonomous skill creation, skills self-improve during use, persistent cross-session memory + user model, isolated subagents, local-LLM support (Ollama/vLLM/llama.cpp), Hermes Function-Calling standard + MCP.
   d. For each claim: mark verified / vendor-only / refuted, with the source. (feedback-verify-and-eval — no self-attestation.)

2. EVALUATE THE COUPLING against the frozen-core thesis (use the firewall lens, then stress-test it):
   - Front door (launch-turn local model to kill 429s; persistent user model/memory): does the evidence support these as safe, science-untouching wins? Quantify the local-model-launch benefit.
   - Engine room (learning loop touching wrappers): confirm it is anti-thesis WITH the specifics from step 1b (reproducibility / auditability / silent-failure re-entry).
   - The interesting middle: learning loop as a PROPOSER for bounded recovery — only if its output stays `inferred` and passes check_amber + the bounded ladder. Assess feasibility honestly.
   - Re-confirm the collisions: subagent swarm vs multi-agent-scope; self-evolving skills vs frozen core.

3. SECOND-PASS ADVERSARIAL CHECK (Eval_Criteria step 4): spawn/think as a skeptic told to FIND where this evaluation is wrong — am I dismissing self-evolution too fast? is the local-model win overstated? is there a coupling I'm missing? Fix the analysis before the verdict.

4. VERDICT + RECORD:
   a. Crisp verdict: ALIGNED / ALIGNED-WITH-CONCERNS / REJECT-FOR-NOW, per coupling mode (front door vs engine room vs proposer-for-recovery), concerns named — match the Research_El_Agente_Q format.
   b. Create the vault note: Arch_Hermes_Agent.md (or a connections/ edge note to OpenClaw_Self_Evolution + Design_Determinism_Spectrum) — vault-note-new skill; check vocabulary.md first.
   c. Decide the competitive-landscape row: does Hermes go in the report's landscape section? If yes, draft the one-line positioning ("same pole, bets on self-rewrite where we freeze the core").
   d. devlog-append: log the session. If the decision is durable, bank a memory (memory-bank skill) — likely a `project` or `reference` entry, mirroring how multi-agent-scope was banked.

Stop conditions:
- If the source proves the learning loop is purely boundary/definition-level (never touches execution code) AND local-LLM support is real, the front-door coupling may be genuinely attractive — STOP and surface it to the user as a possible (opt-in, post-report) spike, do NOT start building it.
- If verifying the claims requires running/installing Hermes, STOP and ask — do not install a new agent framework without sign-off.

Scope-fence: RESEARCH + EVALUATION of Hermes Agent ONLY. Do NOT migrate, port, install, or modify any project-prime/ code. The deliverable is a verdict + a vault note, nothing executable.
```

## After the session — update this file

1. Flip frontmatter `status: ready` → `status: consumed`.
2. Add a footer: `## Outcome` — consumed YYYY-MM-DD, the verdict (per coupling mode), whether a vault note + landscape row were created, link to the [[Dev_Log]] entry and any banked memory.
3. If the evaluation spawns a follow-on (e.g., an opt-in local-model-launch spike), note the new handoff and flip this to `status: superseded` with a pointer.

## Cross-links

- [[Design_Determinism_Spectrum]] — the spine; Hermes is "same pole, different bet on self-rewrite."
- [[OpenClaw_Self_Evolution]] — the existing self-evolution note Hermes connects to most directly.
- [[Research_El_Agente_Q]] — the precedent: evaluate-a-framework → bank-a-scope-decision (→ memory `multi-agent-scope`). Match this rigor.
- [[Eval_Criteria]] — the verdict discipline (deterministic-where-possible → adversarial pass → honest verdict).
- memories: [[project-prime-status]], [[multi-agent-scope]], [[feedback-verify-and-eval]], [[openclaw-canonical-paths]].
- (No Dev_Log entry was written for the 2026-06-11 exploratory tangent that seeded this — the framing lives entirely in this handoff.)

## Outcome

**Consumed 2026-06-27.** Evaluation ran exactly as scoped (research only; project-prime untouched). Pre-run gate (user): start-focused-escalate + produce both Hermes-specific and durable category-level verdict.

- **Verdict, per coupling mode:** Gateway/multi-channel front-end **REJECT-FOR-NOW** · Front door (local launch-turn model + memory) **REJECT-FOR-NOW** · Engine room (self-evolving loop on wrappers) **REJECT (by design)** · Proposer-for-recovery **ALIGNED-WITH-CONCERNS (low priority)**.
- **Load-bearing finding (primary-source):** the autonomous self-improvement loop edits **`SKILL.md` Markdown definitions, not executable code**; literal code-evolution is a separate, offline, user-invoked, *not-yet-implemented* Phase-4 add-on. Second axis surfaced by the adversarial pass: Hermes' **default execution is LLM-mediated**, not frozen-wrapper.
- **The preliminary "front door = plausibly yes" did NOT hold:** the vault's own record deflated it — local-LLM was already dropped 2026-05-20 (Mac headroom), and the 429/503 pain it targeted was already fixed by the paid Google key. Revives only under a remote/GPU backend ([[Gap_Remote_HPC_Backend]]).
- **Vault note created:** [[Research_Hermes_Agent]] (source-cited). Datapoint + the self-mutation/execution-mediation 2-axis refinement added to [[Design_Determinism_Spectrum]]; `vocabulary.md` "Hermes Agent" entry added.
- **Competitive-landscape row: DECLINED with reason** — Hermes is a substrate peer of OpenClaw (attacks no MD bottleneck; OpenClaw itself isn't in the matrix). Value is positioning-contrast on the determinism spectrum, not a competitor row.
- **No follow-on spike triggered:** the stop-condition (loop is boundary-only AND local-LLM real → surface a front-door spike) did *not* fire, because local-LLM is hardware-blocked on the current box and the 429 motivation is already resolved. The Mode-4 proposer idea folds into the existing [[Future_Work_Proposer_Agent]] + [[Gap_Gate_Coverage]], not a new handoff.
- **Records:** [[Dev_Log]] 2026-06-27 entry; memory `project_prime_status` marker + `MEMORY.md` pointer.
