---
tags:
  - research
  - source-manifest
  - verification
  - notebooklm
  - phase-1
type: research-source
status: in-progress
---

# Research: Source Manifest & NotebookLM Verification Checklist

**Purpose:** This is the bridge between the [[Research_Phase1_Survey|distilled vault]] and the grounded primary sources living in **NotebookLM**. Each row names a source, where to find it, and *the specific vault claim it must verify or ground* — so NotebookLM is a targeted fact-checker for the report's load-bearing claims, not a pile of PDFs.

**The boundary (read this):** Claude Code (the vault assistant) **cannot see NotebookLM**. Workflow is one-directional refinement:

> NotebookLM verifies against primary source → *you* distill the precise finding → it flows back into the relevant vault note as a sharpened, cited claim.

This is exactly the loop run manually for the Schrödinger `-set` correction (2026-05-18). NotebookLM should make that loop *proactive* instead of luck-of-the-draw.

---

## Tier 1 — Report-critical (the report stakes credibility on these)

### 1. OpenClaw substrate paper — **VERIFIED 2026-05-19, MIXED RESULTS**
- **Ref (resolved):** *"Automating Computational Chemistry Workflows via OpenClaw and Domain-Specific Skills"* — arXiv:2603.25522
- **Status:** ☑ found ☑ uploaded ☑ verified — see verdicts below

**Verdicts (NotebookLM, 2026-05-19):**

| Vault claim | Verdict | Action taken |
|---|---|---|
| [[Arch_Taskboard_Manifest]] — planning-skill → executable-spec | **PARTIAL → CLOSED (design idea)** | Paper confirms the general planning-skill concept; specific terms (meta-prompting, lazy-load, validation-gating) are NOT in the paper. *Deliberate decision 2026-05-19:* not pursuing primary source — this is the standard plan-and-execute / planner-agent pattern. Demoted to 🟡 design idea; cite Plan-and-Solve / LangGraph / LangChain Plan-and-Execute in the report instead of "Taskboard Manifest." |
| [[OpenClaw_Lobster_DAGs]] — Lobster engine, LLM tasks, approval gates | **PARTIAL** | Lobster + `llm-task` + approvals confirmed; DAG-structure, "before agentic reasoning" layering, git-backed reversibility NOT in paper → caveat added |
| [[Infra_DPDispatcher]] — Slurm/PBS/LSF translation | **PARTIAL → RESOLVED** | Slurm/PBS/LSF/Bohrium + poke/monitor/download lifecycle confirmed by paper. Local-shell mode separately VERIFIED (2026-05-19) via DPDispatcher official docs: `batch_type: "Shell"` + `LocalContext`. Local-only plan unblocked. |
| [[Design_Memory_Provenance]] — provenance labels | **NOT STATED → RESOLVED** | Taxonomy not in paper; sourced separately 2026-05-19 to **OpenBrain** (memory-recipes repo for OpenClaw, via MindStudio article). Corrections applied: spelling Providence→Provenance; 3 labels → **4 labels** (added `imported from transcript`); cite changed from paper to OpenBrain. File renamed accordingly. |
| [[OpenClaw_Self_Evolution]] — MetaClaw, OpenClaw-RL | **NOT STATED → CLOSED (aspirational)** | Neither name appears in the paper; only `skill-creator` in GitHub commits. *Deliberate decision 2026-05-19:* not pursuing primary sources — demoted to ⚪ aspirational, kept as design inspiration only, out of report scope. |

**Paper-confirmed positive finds (added to vault, cite in report):**
- **Bounded recovery from runtime failures** is *explicitly* supported in the paper, with a **methane-oxidation reactive MD case study** as the demo. Added to [[Skill_Bounded_Recovery_AMBER]] as the strongest paper-cited element in the vault.
- `llm-task` plugin returns **JSON-only output validated against a JSON Schema** — concrete deterministic-output mechanism. Added to [[OpenClaw_Lobster_DAGs]]; strengthens stage-validation in [[Arch_Taskboard_Manifest]].
- DPDispatcher actively **pokes / monitors / downloads** — full execution lifecycle ownership. Added to [[Infra_DPDispatcher]].

**Open follow-ups — CLOSED 2026-05-19.** Row #1 is done. Resolutions:
- ✅ Bounded recovery + methane case study — paper-cited; quote in report.
- ✅ Lobster + `llm-task` + approval gates — paper-cited; DAG framing is ours, label honestly.
- ✅ DPDispatcher Slurm/PBS/LSF + poke/monitor/download — paper-cited.
- ✅ DPDispatcher local-shell — verified against DPDispatcher official docs.
- ✅ Memory Provenance — re-sourced to OpenBrain (4 labels, corrected spelling).
- 🟡 Taskboard Manifest — demoted to planner-agent design idea (not pursuing).
- ⚪ MetaClaw / OpenClaw-RL — demoted to aspirational (not pursuing).

**Decision logged:** unverified OpenClaw branding (MetaClaw, OpenClaw-RL, Taskboard Manifest, Lobster-as-DAG, git-backed reversibility) is not load-bearing for the report. We cite the *underlying patterns* from established literature (plan-and-execute, JSON-schema-validated agent outputs, etc.) and the *paper-confirmed* OpenClaw mechanics (Lobster engine, `llm-task`, approval gates, DPDispatcher lifecycle, bounded recovery). Tier badges enforce this discipline in every affected note.

### 2. Johnson & Johnson — Mol Agent
- **Ref:** ACS JCIM — https://pubs.acs.org/doi/pdf/10.1021/acs.jcim.5c01938
- **Grounds:** [[Arch_JNJ_MolAgent]] — 3-part hierarchy (Manager / Data Retrieval / Model Training agents), nested cross-validation, structural-split anti-overfitting, MCP for LLM↔API
- **Verify specifically:** the exact agent names/roles and the "nested cross-validation" claim — these are concrete and easy to misquote
- **Status:** ☐ found ☐ uploaded ☐ verified

### 3. Tippy — Artificial Inc.
- **Ref:** *"Technical Implementation of Tippy…"* — arXiv:2507.17852
- **Grounds:** [[Arch_ArtificialInc_Tippy]] — Supervisor/Molecule/Lab/Analysis/Report/Guardrail agent hierarchy; Docker + Kubernetes per-agent isolation; Envoy proxy; git-based change tracking
- **Verify specifically:** that the Guardrail agent has *no external tools* and sits purely as a filter (we assert this)
- **Status:** ☐ found ☐ uploaded ☐ verified

### 4. Recursion — LOWE
- **Refs:** https://www.recursion.com/lowe · arXiv:2604.11661 · https://github.com/valence-labs/VCR-Agent
- **Grounds:** [[Arch_Recursion_LOWE]] — planner-executor loop, **strict verifier** (predict→test→falsify→improve), mechanistic action graphs, phenomap navigation
- **Verify specifically:** the strict-verifier falsification loop — it's the model for [[Workflow_Error_Recovery_Loop]], so the report leans on it hard
- **Status:** ☐ found ☐ uploaded ☐ verified

### 5. Schrödinger — Multisim / FEP+
- **Where:** Schrödinger's own product documentation (Multisim CLI docs, FEP+ docs) — *not* a paper. Search "Schrödinger Multisim -set flag", "FEP+ Pose Builder", "Active Learning FEP+"
- **Grounds:** [[Arch_Schrodinger_FEP]] and the "Two recovery philosophies" section of [[Skill_Bounded_Recovery_AMBER]]
- **Verify specifically — this is the one a reviewer will pounce on:**
  - Automatic retry = bitwise checkpoint-restore, **no autonomous physics mutation**
  - `-set` flag (e.g. `-set "stage.[1]time=2.0"`) exists and is **manual / human-in-the-loop only**
  - Therefore the contrast is *autonomy*, not capability
- **Status:** ☐ found ☐ uploaded ☐ verified

### 6. OpenEye / Cadence — Orion
- **Where:** OpenEye Orion / Floe documentation. Search "OpenEye Floe Cube ports", "Orion success failure port"
- **Grounds:** [[Arch_OpenEye_Orion]] and the analog/contrast lines in [[OpenClaw_Lobster_DAGs]] and [[Design_Determinism_Spectrum]]
- **Verify specifically:** Cubes evaluate conditions **dynamically at runtime** (`if/else` → success/failure/custom ports). The gap is **semantic reasoning**, not "static." Do NOT let the report say "static" or "can't branch."
- **Status:** ☐ found ☐ uploaded ☐ verified

---

## Tier 2 — Boundary / supporting (cite if used, low effort)

### 7. Iambic — NeuralPLexer2
- **Where:** Iambic Therapeutics preprint/site for NeuralPLexer2
- **Grounds:** [[Arch_Iambic_NeuralPLexer]] — diffusion structure prediction, "replaces MD." Only needed as the scoped-out boundary marker on the [[Design_Determinism_Spectrum]]. One citation, no deep verification.
- **Status:** ☐ found ☐ uploaded ☐ verified

### 8. OpenClaw framework docs (mechanics, not a paper)
- **Where:** docs.openclaw.ai, github.com/openclaw/openclaw
- **Grounds:** the local-setup plan (install, skills dir, LLM fallback chain). Useful for the *implementation* chapter, not the competitive section.
- **Status:** ☐ found ☐ uploaded ☐ verified

---

## Source-integrity risks (confront these early)

- **arXiv:2603.25522 and arXiv:2604.11661 — RESOLVED 2026-05-18.** User searched both IDs; they resolve correctly to the claimed papers. This risk is retired. Citations in the vault stand as-is. *(Historical fallback procedure kept below in case a later doc-version or DOI is found to mismatch.)* If any ID is ever found to 404 or resolve to an unrelated paper:
  1. Do **not** cite the placeholder ID in the report.
  2. Re-find the real paper by title/authors and update the `**Source:**` line in every note that cites it (grep the vault for `2603.25522` / `2604.11661`).
  3. Flag it in `Dev_Log` (once it exists) — a broken substrate citation is a project-level risk, not a footnote.
- **Schrödinger/OpenEye are docs, not papers** — version matters. Note the doc version/date you verified against; their behavior can change between releases.

## Definition of done

A row is ✅ only when: source located → uploaded to NotebookLM → the *specific* claim above confirmed against it → any correction distilled back into the linked vault note with an updated `**Source:**` line.

**Source:** Verification scaffold for Phase 1 sources, created 2026-05-18. Companion to [[Research_Phase1_Survey]] and [[Design_Determinism_Spectrum]].
