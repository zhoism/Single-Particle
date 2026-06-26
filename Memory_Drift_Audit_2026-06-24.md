# Memory Drift Audit — 2026-06-24

A deep-dive pass over all 27 memory files + `MEMORY.md` index, cross-checked against each
other and against ground truth (project-prime + vault git state, live OpenClaw config).
Each item is a question for **you** to resolve. Grouped by confidence.

**Ground truth captured this pass (for reference):**
- project-prime HEAD = `246b06f` ("mdin-edit: address advisor feedback"), branch `main`,
  **ahead of `origin/main` by 2 unpushed commits** (`bda79f9`, `246b06f`).
  Chain: `7b89568 → 5647b0a → c951d38(README) → a166768(FEATURES.md, =origin/main) → bda79f9(packager) → 246b06f(advisor feedback)`.
- Live OpenClaw default model = `google/gemini-3-flash-preview`; fallback `gemini-3.1-pro-preview`;
  `cerebras/gpt-oss-120b` configured but **not** default. Google + Cerebras API keys both present.
- Vault repo HEAD = `764b0ee`, branch `main`, clean-tracked-and-pushed (untracked working files exist).

---

## A. Verified drift — memory disagrees with ground truth (likely just needs an OK to fix)

**A1 — `MEMORY.md` index is missing an entry for `llm_wiki_pattern.md`.**
The file exists on disk (`llm-wiki-pattern`, reference type, 2026-06-05) but has no line in the index.
Every other memory file is indexed.
→ *Add the missing index line?*

**A2 — project-prime HEAD pointer is stale in the index.**
`MEMORY.md` (project-prime line) ends with "project-prime HEAD now `5647b0a`". Ground truth HEAD = `246b06f`
(4 commits later). The `project_prime_status.md` *body* gets as far as `bda79f9` (2026-06-20) but no further.
→ *Update the index + status HEAD pointer to `246b06f`?*

**A3 — "Commit pending" for the advisor mdin-edit work is no longer true.**
`mdin_edit_advisor_feedback.md` (2026-06-22) ends "Commit pending in project-prime." It was committed as
`246b06f` (current HEAD). It is committed but **not pushed**.
→ *Update that memory to "committed `246b06f`, not yet pushed"?*

**A4 — `project_prime_status.md` frontmatter `description:` is dated "as of 2026-06-10".**
The body runs through 2026-06-20, and sibling memories carry facts to 2026-06-22/06-24. The description's
date stamp is ~10 days behind its own content.
→ *Bump the description date (and add the 06-20/06-22 milestones to it)?*

**A5 — Default-model phrasing in the status long-line reads "cerebras" first.**
The `project_prime_status.md` index line says "default model now `cerebras/gpt-oss-120b`" (2026-06-07 fragment)
and later "default model now `google/gemini-3-flash-preview`" (2026-06-09 fragment). Read in order it's correct
(Gemini is current, confirmed by live config), but the stale Cerebras phrase is still in the string and the
`headroom` memory already flagged it as "STALE drift."
→ *Confirm current default = `google/gemini-3-flash-preview` (paid) and scrub the lingering "default = cerebras" phrasing?*

---

## B. Possible mixups that could actively mislead — need your judgment

**B1 — A RETRACTED ΔG (−12.84) is still cited as a milestone result.**
Both the `MEMORY.md` index line *and* the `project_prime_status.md` body present
"Phase A … PROVEN end-to-end on FREE Cerebras (ΔG **−12.84**, $0)" (2026-06-07) as a result.
But `antechamber_aromatic_kekulize_bug.md` explicitly RETRACTS −12.84 / −13.11 / −13.29 (computed on the
mis-typed aromatic ligand, pre-2026-06-08 fix) and says "never cite them as the pipeline's result."
So the index/status cite a figure another memory says is invalid.
→ *Annotate/strike the −12.84 (and −13.x) figures in the status + index with a "(RETRACTED — see kekulize fix)" note?*

**B2 — "Canonical ΔG = −17.18" vs "ΔG is just a noisy sanity number."**
`antechamber_aromatic_kekulize_bug.md`: "the canonical number is **−17.18 kcal/mol (20 ps)**."
`project_prime_status.md`: "Single-trajectory MM-GBSA ΔG is a **sanity number** (run-to-run −17.18/−17.60/−18.49 = the noise)";
the skillbase proof (06-20) reports **−18.54** @100 ps; other runs −18.16/−18.63/−17.94; 3HTB −27.41.
These can both be "true," but calling −17.18 *canonical* while elsewhere treating ΔG as a ±1 sanity range is a
latent contradiction a future session could trip on.
→ *Pick one framing: keep −17.18 as the reference figure, or reframe to "≈ −17 to −18.6, sanity-only, not precise"?*

**B3 — Is project-prime supposed to be pushed right now?**
Memory's narrative is "PUBLISHED to a private repo" (2026-06-19), which reads as "synced." Ground truth: `main`
is **2 commits ahead of `origin/main`** (`bda79f9` packager + `246b06f` advisor feedback are local-only).
→ *Intentional (keep local until you say push), or should those two be pushed — and should memory record the "ahead-by-N, not yet pushed" state explicitly?*

---

## C. Softer / lower-priority drifts (flagging for completeness)

**C1 — "Execution finalized 2026-06-11 → phase transition to writing the report," yet code work continued.**
After the 06-11 "execution complete" declaration, real code landed: `5647b0a` (gate fix, 06-19),
`bda79f9` (packager, 06-20), `246b06f` (advisor refinements, 06-22). Not a hard contradiction (these are
follow-on/advisor asks), but the "execution → writing" phase framing is muddier than the 06-11 entry implies.
→ *Leave as-is (follow-ons don't reopen "execution"), or note that advisor-driven refinements continued post-06-11?*

**C2 — Legacy engine/force-field phrasings still live in dated memory entries.**
Early entries say the MD engine is `sander` (2026-05-14/19) and mention `GAFF`; the live skill uses `pmemd`
and `GAFF2` (the 2026-06-19 vault reassessment fixed the *vault notes*, and `vocabulary.md` now says pmemd).
The memory entries are dated/historical so they're not "wrong," but read out of order they mislead.
→ *Worth a one-line "superseded: live default is pmemd/GAFF2" pointer on the early entries, or leave dated?*

**C3 — Two recent vault artifacts aren't reflected in any memory.**
New untracked files exist that no memory mentions: `Gap_ntx_irest_restart_topology.md` (a new gap note) and
`deliverables-skillbase-20260620.zip` (memory describes the deliverable as a *directory* `deliverables-skillbase-20260620/`,
not a `.zip`). Possibly just not-yet-recorded, not drift.
→ *Should `project_prime_status.md` pick up the new gap note / the zip, or are these intentionally out-of-memory?*

**C4 — Stale "outstanding" cleanups — still outstanding?**
`discord_token_leaked.md` + the status Stage-0 line list gateway-token rotation + plaintext-secrets migration
as "still outstanding (low priority)." These are weeks old.
→ *Still outstanding, or done and the memory should be closed?*

---

---

## Resolution log — 2026-06-24

**A — ALL APPLIED to memory.**
- A1 ✅ `llm_wiki_pattern.md` added to `MEMORY.md` index (after the memory-system-options line).
- A2 ✅ HEAD pointer `5647b0a` → `246b06f` (+ full commit chain) in index and status.
- A3 ✅ `mdin_edit_advisor_feedback.md` "Commit pending" → "Committed `246b06f`; pushed to origin/main 2026-06-24."
- A4 ✅ status frontmatter date `2026-06-10` → `2026-06-24` + 06-22/06-24 milestones appended.
- A5 ✅ stale "default = cerebras" annotated SUPERSEDED in index + body; live default confirmed `google/gemini-3-flash-preview`.

**B — resolved per your calls.**
- B1 ✅ **Confirmed −12.84 = the garbage run** (2026-06-07 Cerebras overnight, computed on the pre-fix mis-typed aromatic indole; retraction list in `antechamber_aromatic_kekulize_bug.md`). Annotated "RETRACTED, do-not-cite" in index + body.
- B2 ✅ Per you (separate runs of the same system, treated as equal because close): reframed the antechamber memory from "canonical −17.18" → "sanity number, run-to-run ≈ −17 to −18.6, cite the range not one figure."
- B3 ✅ Per you (it's in the private repo): the 2 local-only commits (`bda79f9`, `246b06f`) were **pushed** to `origin/main` 2026-06-24 — project-prime now fully synced (0 ahead). Secret-scanned clean first.

**C — addressed 2026-06-24.**
- C1/C2 ✅ left as-is (dated/historical; current-state lines already say the truth).
- C3 ✅ the `Gap_ntx_irest_restart_topology` note was **replaced by a ready handoff** `handoffs/Next_Session_Prompt_ntx_irest_CoherenceGate.md` (gate-only scope recommended; opens by asking 4 questions). All inbound links repointed (Gap_Gate_Coverage + both memory files + this file).
- C4 ✅ verified live — all 3 hygiene items genuinely still outstanding (`plaintext=4` secrets, `plugins.allow` unset); memory was accurate, updated with the precise state. Migration offered, not done (needs explicit OK — touches live auth).

### Notes
- Items I could verify against ground truth (A2/A3/A5, the HEAD chain, the default model) are **resolved facts** —
  the only open question there is whether/how to rewrite the memory.
- Items in **B** are genuine judgment calls (which figure/framing is "truth").
- I did **not** edit any memory this pass — per your ask, this is the question list. Tell me which to apply and I'll fix them.
