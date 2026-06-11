---
name: vault-note-new
description: Use when creating a new vault note (Arch_*, OpenClaw_*, Infra_*, Skill_*, Workflow_*, Design_*, Research_*, Gap_*, or connections/*). Triggers on "create a vault note", "new note for X", "add a Skill_ note", "gap for Y", or after a session reveals something the vault should encode. Enforces the vault's actual frontmatter discipline (NOT the parent Obsidian-network schema), the prefix taxonomy, the vocabulary check, and the tier-badge / [[wikilink]] / Memory-Provenance conventions.
---

# vault-note-new — typed vault note with correct frontmatter

This vault diverges from the parent `/Users/kevinzhou/Downloads/CLAUDE.md` Obsidian Knowledge Network schema. The project-level `CLAUDE.md` is the authoritative spec — read it before this skill if you're unsure. Practical reality:

- Frontmatter is **simple `tags:` + optional `type:` / `status:`**, NOT the parent's `extends/contradicts/fills-gap-in/related/confidence/worth-revisiting` block.
- Confidence is carried by **tier badges in the body** (`✅` source-cited / `🟡` design idea / `⚪` aspirational), NOT a `confidence:` field.
- Rule trust is carried by **Memory Provenance labels** in body content (`observed from source`, `confirmed by user`, `inferred by model`, `imported from transcript`).
- Typed edges from the parent schema are NOT enforced — `[[wikilinks]]` in prose are the actual graph.

## When to invoke

- User says "create a new vault note for X" / "add a Skill_ note for Y" / "gap for Z".
- A session reveals a new concept, architecture, technique, or unresolved question that should be retrievable later.
- An intake-verify pass concluded the report needed a new design-bullet that's substantial enough to deserve its own note.
- A new chemistry technique landed (e.g., a CPPTRAJ analysis pattern, a tleap idiom).

## When NOT to invoke

- The concept is one-shot. If it won't be linked from at least 2 other notes within a month, don't write it. (CLAUDE.md: "do not over-document.")
- The concept is already a note under a different name. Check first.
- The concept belongs in `vocabulary.md` (a single term + 1-line definition) rather than its own note.
- The concept is ephemeral session state — that goes in `Dev_Log.md`, not a note.

## Hard rules

1. **CHECK `vocabulary.md` BEFORE introducing any term.** Vocab drift silently breaks the graph. If the concept exists under a different name, use that name. If it's genuinely new, add it to `vocabulary.md` BEFORE using it elsewhere.
2. **Match the prefix taxonomy.** See `templates/prefix-guide.md`. Picking the wrong prefix means the note is harder to find via `Arch_*` / `Skill_*` glob searches.
3. **Tier badge goes at the top of the body.** Not in frontmatter (per project CLAUDE.md "do not add parallel confidence: frontmatter").
4. **Cross-link with `[[wikilinks]]`** to at least 2 other notes. Isolated notes are graph-dead.
5. **Don't fabricate cited claims.** Source-cited tier (`✅`) requires the actual citation (paper, repo, official docs). When in doubt, use `🟡 design idea`.
6. **For Gap notes:** `type: gap` + `status: open|partially-filled|filled` in frontmatter. The status field IS load-bearing — it's what `Gap_*` queries filter on.
7. **For connection notes:** lives in `connections/`, not at vault root. Has `type: connection` + `between: [a, b]` in frontmatter.

## Procedure

**Step 0 — Read context:**
- `templates/prefix-guide.md` — which prefix and where the note lives.
- `templates/primary.md` / `templates/gap.md` / `templates/connection.md` — the actual file skeletons.
- `vocabulary.md` — verify all terms used.
- Project `CLAUDE.md` (`/Users/kevinzhou/Downloads/Single Particle/Single Particle/CLAUDE.md`) — the canonical schema for THIS vault.

**Step 1 — Confirm the note's role.** Before scaffolding:
- What prefix? (`Arch_*` borrowed / `OpenClaw_*` mechanics / `Infra_*` execution-layer / `Skill_*` concrete skill / `Workflow_*` cross-cutting loop / `Design_*` cross-cutting principle / `Research_*` raw primary-source notes / `Gap_*` open problem / connection edge note.)
- Lives where? (vault root for most; `connections/<name>.md` for edge notes.)
- What 2+ existing notes will it link to? (If you can't name them, the note is premature.)
- Tier? (`✅` / `🟡` / `⚪`)

**Step 2 — Vocab check.** For every load-bearing term in the planned note:
- Grep `vocabulary.md` for the term.
- If present: use the canonical name.
- If absent + genuinely new: add to `vocabulary.md` first, then proceed.
- If a synonym exists: use the canonical synonym, link [[via wikilink]] if helpful.

**Step 3 — Stamp the template.** Copy `templates/primary.md` (or gap/connection) to the destination. Fill in:
- `tags: [...]` — short list (3–6), all-lowercase, kebab-case for multi-word.
- For primary: body sections (concept / how it works / source / cross-links).
- For gap: `status:`, `identified-from:`, `filled-by:` (initially empty), body sections (what / why / partial approaches).
- For connection: `between:`, `relationship:`, `confidence:`, `status:`, body sections (what / why-might-not-hold / what-it-implies).

**Step 4 — Tier badge + Memory Provenance.** At the top of the body:
- `> **Vault tier: ✅ Source-cited** — anchored to <citation>. <verification-method> verified YYYY-MM-DD.` (or 🟡/⚪)
- Apply Memory Provenance labels in body content where rules are stated — particularly important for `Skill_*` and `Workflow_*` notes that the deterministic execution layer might consume.

**Step 5 — Cross-link.** Insert `[[wikilinks]]` to:
- The note's parent concept (where applicable).
- Sibling notes that share structure (without inventing edges per the parent CLAUDE.md guidance — assert only obvious connections; speculative ones go in `connections/`).
- Source material in `Research_*` notes.

**Step 6 — Update `MAP.md` if applicable.** If `MAP.md` exists in the vault and has a topic section the new note belongs to, add a one-line pointer. (Check first — `MAP.md` is updated weekly, not per-session.)

## Anti-patterns

- Do NOT add a `confidence:` frontmatter field. Use the tier badge.
- Do NOT add `extends/contradicts/fills-gap-in/related` frontmatter blocks. The vault uses `[[wikilinks]]` in prose for typed edges.
- Do NOT invent a new prefix. The taxonomy is closed. If genuinely new category emerges, raise it explicitly with the user before adding.
- Do NOT write a note that doesn't link to anything. Isolated notes are graph-dead.
- Do NOT fabricate citations to reach `✅` tier. Step down to `🟡` if the source isn't verified.
- Do NOT use synonyms for vocab terms. ("Topology file" vs "prmtop" — pick the canonical one in vocabulary.md.)
- Do NOT duplicate Dev_Log content into a note. Dev_Log is chronological state; notes are timeless concepts.

## Cross-references

- Project `CLAUDE.md` — the canonical schema for THIS vault (overrides parent network spec).
- Vault `vocabulary.md` — controlled vocabulary; check before introducing terms.
- Vault `Design_Memory_Provenance.md` — the 4 provenance labels.
- Vault `Project Prime.md` — the canonical roadmap; the new note should fit somewhere in its phased framing.
