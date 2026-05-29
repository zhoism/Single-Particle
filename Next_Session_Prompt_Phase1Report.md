---
tags: [project-prime, phase-1, session-handoff]
type: handoff
status: ready
---
# Next Session Starter — Phase 1 Report (resume the competitor table)

> Created 2026-05-27. Paste the **first** code block into a fresh Claude Code session (run from
> the vault) to resume. The **second** code block is the Gemini intake prompt — give that to
> Gemini when you research a new tool, then paste Gemini's filled block back to Claude.
> Everything outside the code blocks is orientation for you (the human).

## Where the report stands (so you don't re-litigate it)
- `Phase1_Report.md` is at **rev. 6 — link-complete and submittable.** Matrix format, 3-bullet
  who/what/trend exec summary, **15 rows**, "What each tool solves — and how" section, materials
  scope-out block, trends, "Where Project Prime fits," consolidated Sources. `grep "LINK NEEDED"` → 0.
- Added since rev.3: **Aqemia** (MDFT analytical binding-ΔG, replace-the-sim) and **Espaloma**
  (Chodera/OpenFF GNN force-field parameterizer, prep tier). Evaluated → **NO row**: Exscientia
  (orthogonal accuracy/orchestration, now part of Recursion; kept a 1-line orthogonal note),
  Insilico Chemistry42 (orchestration tier, docking-scored, not MD; 1-line note in the orchestration
  bullet), "Cadence/OpenEye NNP-MM teardown" (fabrication + org-halo; OpenEye already = Orion row 7).
- Big-tech coverage is **comprehensive** (Microsoft AI2BMD/BioEmu, NVIDIA ALCHEMI-BMD/BCS, Google
  DeepMind GEMS). Memory `phase1-report-status` says returns went flat — **do not add tools just
  to add them.** Only add a new row if it's a genuinely distinct MD player/bottleneck; otherwise
  scope it out (materials / structure-only / infra) or leave it Dev_Log-only.
- Standing format + the recurring Gemini intake-error patterns live in memory `phase1-report-format`.
  **The verbose "teardown" format (no provenance tags) fabricated a fake auto-recovery feature
  TWICE (Exscientia, Cadence) — always Prime's niche. Use the hardened block below; reject teardowns.**

## Prompt to paste into Claude

```
We're resuming the Phase 1 market-research report for Project Prime. Read CLAUDE.md (both),
Project Prime.md, Dev_Log.md (top entries), project memory, and Phase1_Report.md before acting.

Current state: the report is rev. 6, competitor-matrix format, link-complete and submittable.
I want to keep refining the table. For any tool I bring you, I'll paste a Gemini intake block
(hardened format, provenance-tagged). Gemini now PROFILES the tool only — it does NOT compare to
Project Prime and does NOT volunteer recovery/error-handling claims. YOU own the Prime comparison.
Your job is to VERIFY and COMPRESS the block, not trust it:

- Re-check DOMAIN and links against the source yourself (WebFetch). Gemini has mislabeled
  domain/CAMP/bottleneck/org every prior round — the patterns are in memory phase1-report-format.
- If a block arrives in the verbose "teardown" format or with no PROVENANCE tags, treat it as
  suspect and verify hard — that format fabricated a fake auto-recovery feature twice.
- Apply the diagnostic "Does it run biomolecular MD?" but remember no-MD ≠ auto scope-out
  (replace-the-sim and prep-step rows exist). Default answer to "add this?" is NO unless it's a
  genuinely new player or bottleneck; otherwise scope-out one-liner or Dev_Log-only note.
- YOU assess VS-PRIME from verified facts, and YOU check recovery claims: any "autonomously
  mutates physics / re-queues a crashed run" claim is fabricated until a primary source shows it.
- Never fabricate a URL; flag UNVERIFIED and verify before placing.
- Keep scope honesty (e.g. J&J Mol Agent = ML/QSAR, Insilico Chemistry42 = docking-scored
  orchestration — not MD mechanics).

Before editing the report, reflect back: what you're treating as load-bearing vs. dropping from
Gemini's block, and whether the tool earns a row, a scope-out, or a Dev_Log-only no-add. Then proceed.

Thesis to preserve: "the field solves every MD bottleneck except autonomous runtime-failure
recovery, which is Project Prime's niche."
```

## Gemini intake prompt (give this to Gemini per tool)

```
You are preparing a research intake block on ONE tool/model for a US market-research report on
agentic molecular-dynamics (MD) automation. Your output goes to another system (Claude) that
VERIFIES every claim against primary sources and decides what to keep — so do NOT pre-compress
into tidy conclusions, and do NOT editorialize. Give evidence per field, flag every uncertainty.
A hedge I can act on beats a confident claim I have to unwind.

HARD RULES (breaking any of these wastes a full verification round):
1. Output ONLY the fields below, in this structure. Do NOT add an "Engineering Takeaways,"
   "Architectural Patterns," "Tooling to Evaluate," or any advice/synthesis/recommendation
   section. Describe the tool; do not design, prescribe, or extrapolate.
2. PROVENANCE is mandatory on EVERY field: READ-directly (you saw it stated in the cited source)
   or INFERRED (you reasoned it). Unmarked-inferred is a failure. When unsure, mark INFERRED.
3. Do NOT describe any crash-recovery, error-handling, auto-restart, self-healing, or
   parameter-mutation behavior UNLESS the primary source explicitly documents it — then quote the
   exact sentence and mark READ-directly. A workflow engine that can re-queue or restart a node is
   NOT autonomous physics-mutation recovery; do not infer one from the other. Default to "not
   documented." (Do NOT compare the tool to any other project — just report what it does.)
4. ORG = the actual author affiliations / project owner from the cited paper or repo. Do NOT
   bundle ecosystem or open-source components (e.g. OpenMM, espaloma, ANI-2x, OpenFE, BioSimSpace)
   under a commercial vendor unless that vendor authored the work. If it's a community / academic /
   consortium project, say so.
5. LINKS: direct working URLs only — primary literature (DOI) first, then official page. NO
   google.com/search?q= or other search-engine wrappers, NO empty parens. If you can't produce a
   real URL, write UNVERIFIED.

Tool to research: <NAME>

Fields (give value + evidence for each):

ORG:        (actual author affiliations / owner — see rule 4)
TOOL:
ONE-LINE:   what it is, plainly

DOMAIN:     biomolecular drug-discovery MD | materials/condensed-phase | other
  DOMAIN-EVIDENCE: name the actual systems the paper/docs DEMONSTRATE on (e.g. "crambin, 25k-atom
  solvated protein" vs "Si/SiO2 crystals, Li liquids"). Judge by what is SHOWN, not what the
  vendor usually sells. Inorganic crystals / liquids / batteries / organometallics = materials.

DOES-IT-RUN-MD:  yes/no + one sentence. Integrates a real trajectory, or predicts a structure /
  ensemble / force-field parameters directly? The single most decisive call.

CAMP:       engine-layer (computes forces, integrates a real trajectory) | replace-the-simulation
  (outputs structures/ensembles WITHOUT integrating) | prep-step (parameterization / conformer
  prep that feeds an engine) | infra/orchestration (deploy/scale/workflow)
  CAMP-EVIDENCE: the specific mechanism that justifies the label.

BOTTLENECK: one of — rare-event/conformational sampling | accuracy-vs-cost | throughput/trajectory
  -generation | binding-affinity | setup/force-field brittleness | skip-the-simulation | workflow
  orchestration. (Conformer search = static minima, NOT rare-event sampling. Rare-event = dynamic
  barrier-crossing only.)

PROBLEM-&-HOW:  3–5 sentences — the specific problem, the mechanism that solves it, the key
  LIMIT/failure mode (include the limit even if the vendor doesn't).

MD-SCENARIO:  precise industry term(s) (binding free energy, lead optimization, high-throughput
  screening, stability prediction, force-field parameterization, ...)

DEMONSTRATED vs CLAIMED:  split explicitly — what the primary source SHOWS vs what press/marketing
  asserts. Flag any gap.

RECOVERY/ERROR-HANDLING:  per rule 3 — quote documented error-handling verbatim if any, else write
  "not documented." Do not speculate.

LINKS:      (see rule 5)

PROVENANCE: per field, mark READ-directly vs INFERRED.

UNCERTAINTIES:  bullets — what you couldn't verify, what's ambiguous, where sources disagree.

DISCONFIRMING-EVIDENCE:  what would make your DOMAIN / CAMP / BOTTLENECK calls wrong; state the
  plausible alternative reading.

If the "tool" is actually a review/survey (no single tool), say so — it's a background citation,
not a competitor row.
```

## Notes
- **What changed 2026-05-27 (v2 of this prompt):** dropped `VS-PRIME` from Gemini's job — that
  field primed it to confabulate recovery features (fabricated twice). Gemini now profiles only;
  Claude owns the Prime comparison and the recovery check. Added hard rules: no teardown/"takeaways"
  synthesis sections, mandatory provenance, recovery-behavior is documented-or-"not documented,"
  no org-halo bundling of OSS under a vendor, no search-wrapper links. Added `prep-step` to CAMP.
- This supersedes the shorter hardened intake-block in memory `phase1-report-format`; the recurring
  intake-error patterns there still apply (now 8, incl. fabricated-recovery + OSS-aggregation halo).
- If you decide the report is truly final, this handoff can be deleted — but keep the Gemini
  prompt (move it into the format memory) since it's reusable for any future market write-up.
