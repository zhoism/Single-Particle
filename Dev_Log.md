---
tags: [dev-log, project-prime, chronological]
type: log
---

# Dev Log — Project Prime

*Reverse-chronological session log (latest entry on top). Complements the topic-organized vault by giving a time-ordered "what was done when" trail. Each entry is a marker + pointers to artifacts, not a duplicate of the work itself.*

---

## 2026-06-03 (cont., branch) — El Agente Q paper assessed; multi-agent scope decided 📄🦞

**Context:** Side-branch session. User flagged arXiv:2505.02484v2 (Zou et al., Aspuru-Guzik group; "El Agente: An Autonomous Agent for Quantum Chemistry") asking whether its 22-agent hierarchical architecture transfers to Project Prime. Read pages 1–6 of the PDF directly; cross-checked against today's substrate findings.

**Their architecture:** 22 specialized LLM agents (top-level computational-chemistry planner → 3 module heads geometry/quantum/I/O → 18 specialists including 9 ORCA-block experts). Built on CoALA + Soar substrate. Hierarchical procedural memory; working memory with 4 components (global, agent-conversation, grounding-via-FS, long-term). Markov-style context filtering between levels. Jupyter-notebook action trace export. Reported >87% task success on university-level DFT exercises.

**Where it corroborates our discipline:** hierarchical context filtering, specialized-context-per-role, cybernetic feedback retries, action-trace audit, and grounding-via-filesystem all match what our wrapper architecture + [[Workflow_Error_Recovery_Loop]] + Dev_Log already do — typically with stricter LLM/deterministic separation. Strongest published peer for [[Arch_Taskboard_Manifest]] discipline.

**Where it doesn't transfer:** DFT inputs have 200+ flags across 50+ ORCA blocks with subtle cross-block constraints. AMBER `&cntrl` has ~30 keywords in 5 clusters; the [[phase3-advisor-demo]] 11-stage protocol already encodes best practices end-to-end. Their 9 block-expert agents map to **one** wrapper-internal namelist-heuristics dictionary for us. Also, each inter-agent call ≈ ~100s on Flash (Stage 1c empirical); 22-agent multi-hop = 8–16 min/task. Unusable for demo cadence.

**Architectural decision banked:** Project Prime stays at **max 3 named OpenClaw agents** — `main` (today) + future `planner` (when Stage 7 lands) + future `recovery` (when Stage 8 lands). Dynamic sub-agents only if we ever expand to high-throughput virtual screening (Stage 9+, out of current manifest scope). Skills already absorb most of El Agente's agent-side decomposition; pay the multi-agent latency cost only where there's genuine context-separation benefit (different model, different prompt, different thinking level).

**Worth borrowing later (not blocking):** their action-trace-to-Jupyter export as a future reproducibility deliverable; their imaginary-frequency-removal-agent as the conceptual pattern for our Stage 8 recovery sub-skills.

**Artifacts:**
- `Research_El_Agente_Q.md` — full source note with paper summary, architecture diagram, idea-by-idea evaluation, BibTeX.
- `OpenClaw_CLI_Map.md` — cross-link added in Related Notes pointing to the assessment.
- Memory `multi_agent_scope` — decision banked so future sessions don't re-litigate; MEMORY.md index updated.

**Next:** unchanged. Stage 2 (Skill_Antechamber_LigandPrep) is the next concrete work. Multi-agent expansion deferred until Stages 7/8 land and earn their way.

---

## 2026-06-03 (cont.) — Deep doc-read, upstream re-assessment, Stage 2 step 1 applied 📚🔧

**Context:** Same session as the Stage 1 entry below. After substrate verification landed (3/3 PASS), user requested deep familiarity with OpenClaw from primary sources before Stage 2 starts. Three deliverables shipped + step 1 of Stage 2 applied; no chemistry skill scaffolding yet.

**Deep-read of the LOCAL docs/ tree** at `~/.nvm/versions/node/v24.14.1/lib/node_modules/openclaw/docs/` — about 4000 lines across `concepts/{agent-loop, model-failover, retry}.md`, `tools/{exec, exec-approvals, skills, creating-skills, llm-task, lobster, thinking, loop-detection}.md`, `reference/prompt-caching.md`, `agent-runtime-architecture.md`, the bundled `skill-creator/SKILL.md`. Primary-source confirmation of every empirical Day 1–3 finding plus 8 non-obvious facts we hadn't surfaced: the 120s timeout is documented and configurable via `models.providers.<id>.timeoutSeconds`; cooldown is exponential 1m→5m→25m→1h; `metadata` MUST be single-line JSON in SKILL.md frontmatter (embedded parser quirk); `llm-task` plugin gives schema-validated JSON without retry loops; Lobster is linear pipelines not DAGs; 6 skill-loading precedence layers with extraDirs as the right registration path for git-tracked source; agent loop exposes rich plugin hooks (`before_tool_call`, `before_agent_reply`, etc.); OpenClaw has its own memory subsystem (`openclaw memory search/promote`).

**[[openclaw-canonical-paths]] memory rewritten** with 16 sections covering CLI essentials, agent-loop envelope, exec tool, SKILL.md authoring, skill loading + registration, model failover, idle timeout, optional plugins, loop detection, prompt caching, full dead-end catalog. Old Day 2 content preserved + extended. Human-readable companion shipped as vault note **`OpenClaw_CLI_Map.md`** (591 lines) with cross-links to manifest/dev-log/Skill_*/Design_*. Both are graph-aware (memory for Claude session priming; vault for human navigation).

**Upstream library re-assessment** (`computational-chemistry-agent-skills`) against today's substrate understanding — confirmed the paper user flagged ("Automating Computational Chemistry Workflows via OpenClaw and Domain-Specific Skills", Ding et al., arXiv:2603.25522) IS the OpenClaw substrate paper and our cloned repo IS its companion. We've already extracted the architectural lessons; the 4 additional patterns worth adopting now: (1) **iterative one-sub-task-at-a-time planning discipline** from their `agent-taskboard-manifest` skill — Stage 7 planner should adopt this interaction pattern, not just the validation-gate discipline; (2) **dry-run-before-submit** from `dpdisp-submit` — Stage 4 sander/pmemd wrapper should support `--dry-run` for Tier 2 recovery validation; (3) **`${ENV_VAR}` + envsubst** env-injection pattern — solves the path-mismatch portability gotcha [[phase3-advisor-demo]] hit; (4) the upstream **`.schema/skill-frontmatter.schema.json`** as our SKILL.md validation authority (with caveat: schema allows multi-line metadata, but OpenClaw embedded parser prefers single-line JSON; use single-line JSON for safety, validate against schema for portability). Market_Landscape_Report positioning thesis intact — Day 3 findings reinforce rather than contradict the runtime-failure-recovery niche claim.

**Stage 2 step 1 applied:** `skills.load.extraDirs` patched into `openclaw.json` via `openclaw config patch --file /tmp/openclaw-skills-extradir-patch.json5` — adds `/Users/kevinzhou/Downloads/Single Particle/project-prime/skills` as a skills root with `watch: true, watchDebounceMs: 250`. Gateway restarted. Verified via `openclaw config get skills.load`. Next: when SKILL.md lands in that dir, watcher picks it up without restart. **DO NOT re-apply this patch next session — it's persisted in `~/.openclaw/openclaw.json`.**

**Architectural intuition for Stage 2 (the carry-forward):** the manifest's "wrapper does the work, SKILL.md describes the goal" design isn't just preference — Day 3 made it triply load-bearing. (a) Latency: each LLM round-trip costs ~100s on Flash, so chains must be wrapper-internal. (b) Reliability: explicit "use N tool calls" wording triggers 120s idle stalls; SKILL.md prose must be goal-oriented. (c) Determinism: LLM out of the deterministic path = no hallucination corruption. The five-level scaling pattern is articulated in `OpenClaw_CLI_Map.md` §Stage 2 design intuition: Stages 2–6 are Level 0/1 atomic skills; Stage 7 is Level 2 (planner + deterministic executor — Python orchestrator preferred over Lobster for routine runs); Stage 8 is Level 3 (recovery — LLM as classifier within bounded action space + Lobster approval gate for Tier 2 mutation).

**Outstanding for next session ([[Next_Session_Prompt_OpenClaw_Day4]] starter prompt to be drafted):** scaffold `project-prime/skills/antechamber-ligandprep/` with SKILL.md (single-line JSON metadata, requires.bins = antechamber/parmchk2/obabel/pdb4amber, goal-oriented description), `scripts/wrapper.py` (obabel→antechamber→parmchk2 chain, `--dry-run` flag, returns JSON envelope), `references/` (adapted heuristics from upstream antechamber/SKILL.md with LGPL-3.0 attribution), `test_acceptance.sh` (golden-path benzene from PDB 181L + unrelated ligand + malformed input for error path). Acceptance per [[Phase3_Taskboard_Manifest]] Stage 2.

---

## 2026-06-03 — OpenClaw Phase 3 Stage 1 substrate verification: 3/3 PASS, two real design signals for Stage 2 🧪✅

**Context:** Day 3 of OpenClaw. Stage 1 of [[Phase3_Taskboard_Manifest]] — three substrate probes (structured JSON output, bash tool execution, multi-tool chain) against the gateway-routed `google/gemini-3-flash-preview` substrate. No skills built; no chemistry yet. The exercise was capability verification before Stage 2 design decisions ride on assumptions about the substrate.

**1a — Structured JSON output: 3/3 PASS clean.** Three difficulty-graded clinical-extraction prompts (flat 3-field, nested objects, array field) all returned parseable JSON, correct schemas, correct types, no markdown fences. Envelope shape is canonical: `{ok, capability, transport, provider, model, attempts, outputs:[{text, mediaUrl}]}` — inner LLM payload lives in `outputs[0].text` and is a JSON-string when the prompt demands it. **Stage 7 planner can rely on `--json` + a "no fences, no prose" prompt suffix** without a schema-validation retry loop for simple shapes.

**1b — Bash tool execution: PASS.** Prompt: "list the 5 newest files in ~/Downloads." Agent emitted **one tool call to a tool named `exec`** (NOT `bash` — this is a canonical-paths correction; [[openclaw-canonical-paths]] needs updating). 0 failures. Agent's reply enumerated the 5 paths in identical order to `ls -ta ~/Downloads/ | head -5` (including `.DS_Store` — the prompt didn't exclude hidden files, so the agent correctly included it). No hallucination — every path matches reality.

**1c — Multi-tool chain: PASS, but only after 3 failures and a prompt softening.** Strict prompt ("use separate bash tool calls — one to identify, one to measure") triggered **Flash 120s LLM-idle-stream timeout repeatedly** (attempts 1, 2, 3 — including with `--thinking minimal`). Each Flash failure puts the AI Studio auth profile into a 1-minute cooldown that ALSO blocks the Pro fallback (auth profile is per-provider, not per-model). Attempt 4 (cooldown cleared, instruction softened to natural phrasing) succeeded: **2 exec calls, 0 failures, 311s duration.** Final reply named `.DS_Store` at `40K` — the agent could only know the filename from call #1, so the chain carried state correctly into call #2. Size discrepancy reconciled: file is 40,964 bytes → 40K (logical bytes/1024) or 44K (`du -h` allocated blocks); both correct readings.

**Three substrate findings for [[openclaw-canonical-paths]] (memory update next session):**
1. The shell tool is named **`exec`**, not `bash`. Prompts and skill docs should reference `exec`.
2. `--json` mode surfaces `toolSummary.calls/tools/failures` + `finalAssistantVisibleText` but **does NOT expose raw exec args or stdout**. Skills that need to log exact tool I/O must do it inside the wrapper, not rely on the agent trace.
3. AI Studio auth-profile cooldown is **per-provider** — a Flash idle-timeout takes Pro out of rotation for ~1 minute. Fallback chains within the same provider don't add resilience against this failure mode.

**Two design signals for Stage 2 (antechamber-ligandprep):**
- **Latency budget**: a 2-step chain at default thinking took 311s. Real chemistry skills with 5–10 stages cannot afford 5min per turn. Either (a) bundle the whole skill into one `exec` call from a Python wrapper (the architecture the manifest already calls for — "lobster-like" hardened-deterministic discipline), or (b) tune `--thinking off` for routing turns and reserve thinking for genuinely hard decisions. Option (a) is the right call; this confirms the design.
- **Strict-instruction triggers stall**: explicit "use N tool calls" demands push Flash into a long-deliberation state that the gateway kills at 120s. SKILL.md prose should describe the goal, NOT prescribe the tool-call topology. Wrappers enforce the topology deterministically.

**Operational note** (the cooldown gotcha): after a Flash idle timeout, wait ≥60s before retrying or the auth profile blocks even Pro. `openclaw models status | grep cooldown` is the fastest diagnostic. **Did NOT need to touch `openclaw approvals`** — bash/exec is in-profile under `tools.profile: "coding"` and fires without prompting.

**Artifacts:** 35 files in `project-prime/runs/substrate-verification/` (cmd/out/stderr/verdict per case, plus 1c's 4 attempts and a baseline_ls snapshot). All four `.verdict.txt` files report PASS. Transcripts gitignored — they capture point-in-time substrate behavior, not source.

**Manifest:** [[Phase3_Taskboard_Manifest]] Stage 1 flipped from PENDING to COMPLETE.

**Stage 0 cleanup** still outstanding from Day 2 (gateway token rotation, plaintext-secrets migration, plugin allowlist hygiene) — non-blocking, deferred.

**Next:** Confirm Stage 2 scope before starting. The latency signal above changes nothing in the manifest's planned design (one wrapper.py per skill, SKILL.md describes goals not topology) — it just validates that the design was already correct. Optional vault note `OpenClaw_CLI_Map.md` queued; design decision = include `exec`-not-`bash` correction + cooldown gotcha + 311s observation.

---

## 2026-06-02 — OpenClaw Stage 0 unblocked: AI Studio key works, default model swap, Discord wiring, persona side-quest ⚙️✅

**Context:** Day 2 of OpenClaw setup. Goal: clear Day 1's UNRESOLVED LLM auth + security debt + get the bot actually responsive. All three landed.

**LLM auth resolved:**
- AI Studio key (`AQ.<~53chars>` format — newer Google AI Studio key style, NOT the legacy `AIzaSy<33chars>`) curl-verified against `generativelanguage.googleapis.com/v1beta/models?key=$KEY` → returns model list including gemini-2.5-flash + 2.5-pro + 2.0-flash. **Format is fine** — user's account is on the newer enrollment.
- Wired into OpenClaw via `openclaw models auth paste-api-key --provider google`. `models status` shows `api_key=1` for `google`. Cosmetic "Missing auth" warning ignored (counts OAuth specifically, not API keys).
- BUT first smoke test failed: `Unknown model: google/gemini-2.5-flash`. Root cause: the **OpenClaw 2026.5.28 `google` provider plugin only catalogs `gemini-3-flash-preview` and `gemini-3.1-pro-preview`** — verified via `infer model providers` + `infer model list`. Not a tier/key issue — plugin catalog limit.
- Swapped default + fallback to cataloged models: `openclaw models set google/gemini-3-flash-preview` + `openclaw models fallbacks add google/gemini-3.1-pro-preview` (removed stale `gemini-2.5-pro` fallback).
- Final twist: `infer model run` defaults to `--local` which fails with the same `Unknown model` UNLESS the model is duplicated into `models.providers.google.models[]` in user config. **`--gateway` uses the catalog directly and just works.** End-to-end smoke test passed: `openclaw infer model run --prompt "ok" --gateway` returns Gemini's response. All real work routes through the gateway anyway, so `--local` is irrelevant.

**Discord:**
- Token rotated at discord.com/developers/applications → Bot → Reset Token; `openclaw config set channels.discord.token "<new>"` + gateway restart. `channels status --probe` confirms `connected, transport:just now, bot:@Single Particle, token:config, works`.
- `intents:content=limited` is a LABEL, not a defect — OpenClaw's word for "under 100 servers, no Discord verification needed, fully functional." Confirmed in gateway logs: *"Discord Message Content Intent is limited; bots under 100 servers can use it without verification."* The `channels.discord.intents` schema accepts only `presence`, `guildMembers`, `voiceStates` — there is **no `messageContent` field**.
- Bot was in server but silent because `groupPolicy: "allowlist"` + empty `guilds: {}` = ignore everything. Patched config with server `1511130058306228311` + user `370013420013223937` under `channels.discord.guilds`, `requireMention: true`. After restart, `@Single Particle <msg>` in any channel of that server reaches OpenClaw and routes through Gemini. **First @ working: confirmed end-to-end.**

**Bonus side-quest — persona experiment:**
- Discovered the agent workspace already has stock-template identity files: `~/.openclaw/workspace/{IDENTITY.md, SOUL.md, BOOTSTRAP.md, AGENTS.md, USER.md, TOOLS.md, HEARTBEAT.md}`. The bot's "Hey, I just came online — who am I?" first-message script came verbatim from `BOOTSTRAP.md`.
- Wrote a temporary joke persona (Haibin Peng — adult gay Chinese guy, bad flirt, suggestive-not-explicit, "out of character" escape hatch in SOUL). Snapshot taken at `~/.openclaw/snapshots/pre-persona-20260602-234723.json` + the three workspace files. Tested 3–4 messages in Discord, reverted cleanly via one-line `cp` chain + gateway restart. Workspace files back to stock — bot will re-run BOOTSTRAP conversation on next message (correct pre-persona behavior).

**Decisions logged (do not re-litigate):**
- All real OpenClaw inference (skills, agent turns) goes through **`--gateway`**, not `--local`. Local mode requires duplicating the catalog into user config — not worth it.
- Default model is **`google/gemini-3-flash-preview`** with `gemini-3.1-pro-preview` fallback. Skills + tests pin to these names.
- For inference smoke tests, use `openclaw infer model run --prompt "..." --gateway` — there is **no `openclaw models test` verb**.
- New canonical-CLI memory created: [[openclaw-canonical-paths]] — read FIRST in new OpenClaw sessions to skip rediscovery.

**Stage 0 cleanup outstanding (non-blocking, low priority):**
- Gateway token rotation — `openclaw doctor --generate-gateway-token` (loopback-only).
- Plaintext secrets migration — `openclaw secrets configure` + `apply` + `audit --check`.
- Plugin allowlist hygiene — `plugins.allow` is empty; logs warn discovered non-bundled plugins may auto-load.

**Next:** Phase 3 Stage 1 (substrate verification — JSON output, bash tool, tool-chain tests). Also queued: write `OpenClaw_CLI_Map.md` vault note synthesizing today's CLI/intents/identity findings. Resume in `Next_Session_Prompt_OpenClaw_Day3.md`.

---

## 2026-06-01 (evening) — OpenClaw substrate installed; upstream library found; LLM auth blocked 🦞

**Context:** First OpenClaw session — install + provider auth attempt. Substrate is in; LLM auth path is unresolved; upstream library discovered (not in prior research).

**Substrate (working):**
- OpenClaw **2026.5.28** installed via `npm install -g openclaw@latest` (Node 24.14.1 via nvm, no sudo needed). Gateway running as LaunchAgent at `~/Library/LaunchAgents/ai.openclaw.gateway.plist`, loopback `127.0.0.1:18789`, token auth, dashboard at `http://127.0.0.1:18789`.
- Config at `~/.openclaw/openclaw.json`, workspace `~/.openclaw/workspace`, per-agent auth store `~/.openclaw/agents/main/agent/auth-profiles.json`.
- `openclaw doctor` clean except cosmetic warnings (nvm Node, plaintext secrets in config, no command-owner, 42 unused bundled skills now disabled).
- gcloud + ADC installed and minting tokens (`brew install --cask google-cloud-sdk` → `gcloud auth application-default login` → `set-quota-project`).

**Upstream library DISCOVERED — not in any prior research pass:**
- `jinzhezenggroup/computational-chemistry-agent-skills` (LGPL-3.0) is the paper authors' open code repo — the actual code home of arXiv:2603.25522. **Research_Source_Manifest verified only the paper, never reached the code library.** Cloned read-only to `~/Downloads/Single Particle/upstream-reference/` (sibling to vault + project-prime).
- 66 SKILL.md files across `molecular-dynamics/`, `quantum-chemistry/`, `agent-workflow/`, `tools/`, etc. Their `molecular-dynamics/antechamber/SKILL.md` is 12.7 KB of instruction text + parameter heuristics (zero deterministic code — pure "LLM constructs the call" pattern). Their `tools/dpdisp-submit/SKILL.md` is 12 KB of DPDispatcher patterns. Their `agent-workflow/agent-taskboard-manifest/SKILL.md` is the upstream of our planning-layer design (wraps third-party `light-cyan/AgentTaskboardManifest`).
- **Contribution boundary now sharper**: their skills are *documentation-skills* (LLM-as-CLI-constructor); ours will be *hardened-deterministic-skills* (LLM picks the skill, the wrapper script does the work). That contrast IS the "lobster-like" disciplinary distinction `Actionable_Recommendations.md` already named.
- `.schema/skill-frontmatter.schema.json` is the authoritative SKILL.md schema — use when authoring our own.

**LLM auth — UNRESOLVED, multiple dead-ends:**
- **Vertex-Gemini is broken in OpenClaw 2026.5.28.** No provider plugin claims `google-vertex/*`; stock extensions list shows `anthropic-vertex` (Claude only) but no `google-vertex`. `openclaw models auth login --provider google-vertex` → "No provider plugins found." Model catalog entry `google-vertex/gemini-2.5-flash` is orphaned. Configure wizard for "Google Vertex" provider silently writes no credential. ADC tokens are minting fine on the GCP side — OpenClaw just has no plugin to consume them.
- **AI Studio path tried but credential format suspect.** Generated AI Studio key against project `single-XXXXXX`; key prefix is `AQ.Ab8R...` not the canonical `AIzaSy...`. Wired into OpenClaw via `models auth paste-api-key --provider google`. Smoke test failed with `Unknown model: google/gemini-2.5-flash (model_not_found)` for BOTH Flash and Pro despite the catalog showing both with `Auth: yes`. Could be (a) wrong credential type pasted, (b) free-tier model access limitation, or (c) Google API rejecting the key. **Direct curl verification of the key against `generativelanguage.googleapis.com/v1beta/models` is the definitive next step — deferred to tomorrow.**
- **$300 GCP credit EXCLUSION verified** (user's prior memory was correct). As of March 2026 the free trial credit is explicitly excluded from AI Studio Gemini API usage. Vertex remains credit-eligible but Vertex is broken in OpenClaw — credit-eligibility is moot until OpenClaw ships a Vertex-Gemini plugin. Pragmatic call: accept ~$1–10 out-of-pocket AI Studio dev cost in the interim; the credit is preserved for non-AI-Studio GCP services.

**Security debt — address tomorrow before resuming skill work:**
- **Discord bot token was pasted into the assistant's chat context** during config inspection. Rotate at discord.com/developers/applications → Bot → Reset Token → `openclaw config set channels.discord.token "<new>"` + gateway restart.
- Gateway token (loopback-only, blast-radius minimal) also leaked; rotate with `openclaw doctor --generate-gateway-token` for hygiene.
- `openclaw doctor` confirms `openclaw.json` stores secrets in plaintext. Migration: `openclaw secrets configure`; defer until after Discord rotation.

**Decisions logged (will not be re-litigated tomorrow):**
- **Upstream reuse strategy**: clone as read-only reference (done); BUILD our own hardened skills per `Actionable_Recommendations.md` §1 ("Build: ligand-prep skill" + recovery + planning). Borrow their instruction text + parameter heuristics into our SKILL.md bodies; do NOT depend on their package at runtime.
- **Gemini key storage**: NOT in `~/.zshrc`, NOT in `project-prime/.env`. Lives in OpenClaw's per-agent auth store `~/.openclaw/agents/main/agent/auth-profiles.json` (outside project tree, can't be `git add`ed).
- **Discord channel + chat-channel skills**: out of scope for skill dev. Already configured but the `coding` tool profile strips `message`; doctor warnings about missing messaging tools are non-blocking and being ignored.

**Next:** Phase 3 stages captured as `Phase3_Taskboard_Manifest.md` (Stage 0 LLM auth resolution → Stage 1 substrate verification → Stage 2 first skill `Skill_Antechamber_LigandPrep`). Resume sequence in `Next_Session_Prompt_OpenClaw_Day2.md`. First action tomorrow: curl-verify a regenerated AI Studio key BEFORE any OpenClaw config touches.

---

## 2026-06-01 — Phase 3 inputs received from advisor; pre-OpenClaw orientation 📥

**Context:** advisor handed off `phase3-explicit-solvent-md/` (pre-prepared complex MD demo) and `Amber26.pdf` (1104-page Amber 2026 reference manual). No execution yet — user explicitly scoped this session to bookkeeping + OpenClaw briefing prep.

**Demo shape (canonical recipe the OpenClaw skill chain must reproduce):** 11 sequential `pmemd` stages — `min1 → min2 → heat-1 → press-1 → heat-2 → press-2 → heat-3 → press-3 → relax → prod` — Langevin thermostat (`ntt=3, gamma_ln=2.0`), MC barostat (`barostat=2`), SHAKE on (`ntc=2, ntf=2`), `dt=0.002`, `cut=9.0`, restraint mask `!:WAT,Cl-,K+,Na+ & !@H=` released only at relax. Production = 10 ns (`nstlim=5,000,000`). Details in memory [[phase3-advisor-demo]].

**Two gotchas to fix before any local run:**
1. `submit.sh` exports `AMBERHOME=/Application/software/Amber26/pmemd26` — advisor's path, not ours (local `pmemd` is `~/Downloads/pmemd26/`). The wrapping skill should resolve `pmemd` from PATH instead of hardcoding.
2. `heat-3.in`: `cntrl temp0=300.0` but `&wt value2=310.0` — Langevin follows TEMP0 (set by &wt), so system ramps to 310 K then would clamp toward 300 K if extended. Minor; flag to advisor next conversation.

**Manual coverage check:** Amber26.pdf section map saved in memory [[amber26-pdf-section-map]] for targeted reads — sander §23.6 (p.429) is the keyword source-of-truth, pmemd §24.3 (p.499) for engine overrides, atom-mask syntax in ch.25 (p.509) for parsing the restraint masks.

**Next:** brief user on OpenClaw (what it is as installable software, vault's verified vs. unverified claims, install entry point), then move into the [[Next_Session_Prompt_OpenClaw]] flow.

---

## 2026-05-28 — Market research consolidated into "Market Landscape" reports → SUBMITTED to advisor 📝✅

**Context:** advisor wanted a high-level, plain-language read on where AI is taking MD. Reframed the Phase-1 survey into a clean supervisor-facing set (three trends: skip-the-sim / ML force fields / agentic orchestration) and **dropped the "Project Prime" codename** per user (see [[feedback-project-prime-name]]). **Submitted 2026-05-28.**

**Artifacts (canonical going forward):**
- `Market_Landscape_Summary.md` — short: intro + 15-row table + out-of-scope materials bullets + neutral bottom line.
- `Market_Landscape_Report.md` — long, problem-first: 6 MD bottlenecks → per-tool techniques → recovery; full table; **"Surveyed and excluded (scope boundary)"** section; Sources.
- `Actionable_Recommendations.md` — build/integrate/adopt triage + infra decision + positioning + next steps.

**Also this session:**
- **Deleted `Phase1_Report.md` + `Phase1_Report_Brief.md`** (git-tracked, recoverable); unique content migrated into the Report's scope-boundary section — materials scope-outs (MatterSim / MPNICE / GNoME / differentiable-sim), Exscientia, Insilico Chemistry42, Zhu et al. review.
- **Added two web-verified tools:** PRISM/CADD-Agent (in-domain agentic GROMACS pipeline via Claude Code + MCP → matrix row) and GENIUS (*Nature Comms Materials* 2026; Quantum ESPRESSO/DFT finite-state *setup*-error recovery, materials → recovery-adjacent note). TopoMAS = materials, surveyed but not added.
- Per user, **removed the "nobody does bounded recovery" defensibility claim** from the summary (info-gathering > defensible claim). Niche context: OpenClaw already demonstrated bounded recovery (methane-oxidation) and GENIUS published finite-state sim recovery (materials/setup) → honest niche narrowed to runtime physics-instability recovery for explicit-solvent biomolecular MD. Same claim still present in the Report + Actionable (user editing those).

**Next:** OpenClaw install + LLM (Gemini) wiring — starter prompt at `Next_Session_Prompt_OpenClaw.md`.

---

## 2026-05-28 — "STAR-MD" rejected as a fabricated/unverifiable paper 🚩

**Context:** intake for "STAR-MD (Spatio-Temporal Autoregressive Rollout for MD)" — ByteDance + Georgia Tech, claimed SE(3)-equivariant causal diffusion transformer generating microsecond protein trajectories (replace-the-sim, ATLAS benchmark). Arrived in the **clean hardened format** with provenance tags; LINKS marked READ-directly.

**Verification — does not exist in any findable form:**
- arXiv `2602.02128` → **HTTP 404** (a real /abs/ page resolves even for obscure papers; 404 = ID doesn't exist).
- Exact title "Spatio-Temporal Autoregressive Rollout for Molecular Dynamics" → zero hits.
- "STAR-MD" tool name → nothing in this space.
- Capability searches returned only the **real analogues** the description was synthesized from: **Timewarp** (Microsoft), **MDGen** (Jing/Jaakkola), **BioEmu** (already a row). The ByteDance-MD-trajectory search returned only BioEmu (Microsoft, not ByteDance).

**Decision — NO row, NO report edit.** Hallucinated/unverifiable source; per the never-place-unverified rule it cannot enter the report in any form.

**New failure mode (important):** a **fully hallucinated paper** passed the clean hardened format — provenance tags stop field-level confabulation and fake recovery claims, but cannot vouch that the *source exists*. Gemini was handed a tool name and confabulated a plausible paper (real benchmark ATLAS, plausible architecture buzzwords, even an honest-looking DISCONFIRMING section), then stamped the dead link READ-directly. **Lesson: resolve the link FIRST; link resolution is the single most reliable existence check, independent of format/provenance.** Logged as pattern #9 in [[phase1-report-format]]. Thesis/report untouched. (If a real generative-trajectory representative is ever wanted, the genuine options are MDGen / Timewarp — but replace-the-sim is already a named trend with 5 rows, so default-NO holds.)

---

## 2026-05-27 — Isomorphic Labs IsoDDE added as matrix row + "skip the simulation" promoted to a named trend (rev. 7) ➕

**Context:** first intake on the **new hardened (provenance-tagged) Gemini prompt** — and it shows: clean fields, recovery = "not documented," no teardown. IsoDDE = Isomorphic Labs Drug Design Engine (Alphabet/DeepMind), tech report released Feb 10 2026.

**Verified (PDF was binary/un-extractable; confirmed via report title + multiple secondary sources):**
- DOES-IT-RUN-MD **no** / CAMP **replace-the-simulation** — confirmed; AlphaFold-3-lineage DL engine, predicts structure/affinity/pockets directly from sequence, no trajectory.
- Demonstrated: ~2× AlphaFold 3 cofolding (hardest Runs N' Poses subset); beats AF3/Boltz-2 on antibody–antigen (CDR-H3); 1.5× P2Rank AUPRC on pockets; CRBN thalidomide + cryptic allosteric site from sequence (RMSD 0.12/0.33 Å).

**Intake correction (in IsoDDE's favor):** block filed "exceeds FEP" under CLAIMED (marketing). Actually **benchmarked** — Pearson 0.85 vs FEP+ 0.78 (FEP+ 4 set), 0.73 vs 0.72 (OpenFE), no crystal needed. Carried WITH caveats: self-reported / not peer-reviewed, architecture undisclosed, "in some settings," OpenFE margin ≈ tie, no third-party validation, static + OOD-degrading.

**Decisions:**
1. **ROW** — marquee new player (most prominent replace-the-sim company) and the first matrix entry to benchmark DL affinity head-to-head vs FEP+ and report parity/edge — the sharpest "why run MD at all?" case. Reinforces thesis (no trajectory → no runtime recovery). Placed after Aqemia in the replace-the-sim cluster.
2. **Promoted "replace the simulation" to a named Dominant Trend** (per user's "this is a trend" call) — NeuralPLexer2 (structure) / BioEmu (ensemble) / Aqemia (ΔG) / IsoDDE (all three) are now a recognized wave, distinct from ML-force-field engines (AI2BMD/GEMS) that still integrate. Ties the cluster together + restates Prime's orthogonality.

**Done:** matrix row 16; "unified oracle" problem bullet (with caveats); updated "remove the simulation" positioning line; new Trends bullet; Sources sub-block (2 links verified, peer-review caveat); frontmatter `revision: 7`. Thesis intact.

---

## 2026-05-27 — "Cadence Molecular Science" NNP/MM teardown evaluated → NO row (fabrication + org-halo) 🚫

**Context:** verbose teardown (no provenance tags) framing Cadence/OpenEye as architecting a unified "AI-driven MD platform" (NNP/MM in the integration loop, espaloma, OpenMM, OpenFE, ATM). Same format as the Exscientia trap. User flagged it as "extremely similar to what I've seen before" — correct.

**Two failure modes, both confirmed by verification:**
1. **Fabricated recovery (pattern #6, 2nd instance):** "Actionable Engineering Takeaways → State Management" claims the orchestrator "adjusts state parameters (reduces dt, applies soft-core, re-initializes velocities) and resubmits" the crashed node = Prime's exact niche, uncited. Orion's *real* documented behavior (already in the report's row 7) is pre-coded `if/else` routing with the explicit ceiling "a novel error with no matching `if` stalls" — which already rebuts this.
2. **Org-halo aggregation (pattern #1, expanded):** attributes a pile of academic/consortium OSS to "Cadence/OpenEye contributors":
   - **OpenMM 8** (JPCB 2024, arXiv:2310.03121) — authors Eastman (**Stanford**), Chodera, Markland, De Fabritiis; **no OpenEye affiliation**.
   - **"Enhancing Protein–Ligand Binding Affinity Predictions Using NNPs"** (JCIM 2024, `10.1021/acs.jcim.3c02031`) — Sabanés Zariquiey, Galvelis, Gallicchio, **Chodera, Markland, De Fabritiis** (Acellera/Chodera/ATM); **not OpenEye**. The "0.97→0.47 kcal/mol TYK2" headline is **Rufa et al.** (Chodera) prior work — misattributed.
   - **espaloma** — Chodera/OpenFF (verified this session); already its own matrix row, not OpenEye.
   - **OpenFE** — OMSF-hosted pre-competitive consortium (~15 pharma), not an OpenEye product.

**Decision — NO row, NO report edit.** OpenEye/Cadence is already matrix row 7 (Orion); the "new" material is fabricated (recovery) or belongs to Stanford/Chodera/De Fabritiis/consortium, not Cadence. Row 7 is accurate as-is and already inoculated against the recovery claim via its `if/else`-ceiling wording. Logged + patterns reinforced in [[phase1-report-format]]. Thesis untouched.

---

## 2026-05-27 — Insilico Chemistry42 evaluated → NO row (orchestration tier, not MD) 🚫

**Context:** Gemini intake for **Insilico Medicine / Chemistry42** (generative AI + claimed MD active-learning loop). Verified the decisive `DOES-IT-RUN-MD: Yes` claim — it does **not** hold.

**Verification:**
- **GENTRL/DDR1** (*Nature Biotech* 2019, `10.1038/s41587-019-0224-x`): GENTRL optimizes synthetic feasibility / novelty / activity; binding mode "derived from **docking** simulations" (PDB 3ZOS). No MD. Block's "demonstrated in a solvated environment" = embellishment.
- **Chemistry42** (*JCIM* 2023, `10.1021/acs.jcim.2c01191`): 42 generative algorithms + RL scoring/reward loop + med-chem filters. Reward battery is **docking + ligand-based/ADMET scoring**, not explicit-solvent MD/FEP. No MD/FEP/OpenMM/Desmond as the reward mechanism. The block's own DISCONFIRMING-EVIDENCE predicted exactly this ("if it primarily uses static docking and calls it physics-based, DOES-IT-RUN-MD would be a no").
- **Links were google.com/search wrappers** (forbidden pattern, rule #3) → clean DOIs verified above.

**Decision — NO row.** Insilico Chemistry42 is in the **agentic-orchestration tier already represented 3× (LOWE, J&J Mol Agent, Artificial Tippy)** — generative design + docking/ML scoring, *not MD mechanics* (the Mol Agent honesty note exactly). `BOTTLENECK: workflow orchestration` is already covered; the one distinguishing claim (MD-as-reward) is unsupported → default-NO. Per user follow-up ("just keep a quick note"), added a **one-line mention** to the existing "orchestration, not MD mechanics" bullet (generative-design platform, docking-scored reward, not MD) — NOT a matrix row or materials scope-out. Logged to memory + new pattern (generative-platform "MD-washing": docking-scored RL loop billed as running MD). Thesis untouched.

---

## 2026-05-27 — Exscientia re-run with corrected intake → recharacterized as orthogonal 🔧

**Follow-up to the entry below.** User re-submitted Exscientia in the proper hardened format — the fabricated auto-recovery claim is **gone**; the block now self-classifies honestly: DOES-IT-RUN-MD **yes** (classical AMBER/GROMACS; ML only as prep torsion-fitting or post end-state correction), CAMP **infra/orchestration**, BOTTLENECK **accuracy-vs-cost**, VS-PRIME **orthogonal** (even ships a clean DISCONFIRMING quote). Confirms the prior NO-row call on independent grounds (bottleneck already owned: accuracy-vs-cost→AI2BMD/GEMS, RBFE→FEP+, parameterization→Espaloma; org now part of Recursion).

**Report fix:** the first pass (below) had put a *defensive rebuttal* of the auto-recovery claim into the "open gap — autonomy" bullet. With the honest read, Exscientia is orthogonal — not a recovery near-miss like Multisim/Orion — so that placement was a category mismatch rebutting a claim the reader never sees. **Removed it, restored the clean Multisim+Orion autonomy-gap pair, and added one correctly-categorized orthogonal-accuracy line** in the "Where Project Prime fits" engine/prep grouping, citing JCTC 2025 (`4c01427`)'s finding that well-fit classical torsions match heavier ML/MM end-state corrections (MAE 0.8–0.9 kcal/mol) at lower cost. Still NO row. Thesis intact. (Frontmatter `revision: 6` note updated in place rather than bumping — nothing was submitted between the two same-day passes.)

---

## 2026-05-27 — Phase 1 report: Exscientia evaluated → NO row; thesis hardened (rev. 6) 🛡️

**Context:** Gemini intake for **Exscientia** — but in the *verbose teardown* format, **no provenance tags**, and containing a thesis-threatening claim. Scrutinized hard before touching the report.

**The danger:** an uncited "Actionable Engineering Takeaways" paragraph claimed Exscientia's orchestrator "catches the error, reduces the timestep, increments the Langevin seed, and re-queues the crashed λ-window" — i.e. **Prime's exact niche** (autonomous bounded physics-mutation recovery). If true, it refutes the report's thesis.

**Verification:**
- **Claim unsubstantiated.** No evidence in Exscientia's papers or BioSimSpace docs/changelog/GitHub issues of autonomous crash→param-mutation→re-queue. It's Gemini's own *architectural advice to the reader* (the section literally lists "Open-Source Tooling to Evaluate"), not an Exscientia feature. BioSimSpace is an interoperability/process layer; users hit crashes and fix them manually (per its issue tracker).
- **Real papers exist, neither about recovery:** JCTC 2025 21(2):967 (`10.1021/acs.jctc.4c01427`) = ML/MM end-state corrections (ANI-2x/AIMNet2) for RBFE accuracy; JCIM 2024 (`10.1021/acs.jcim.4c00220`) = active-learning triage (GP + Chemprop) — largely a **University of Edinburgh (Mey lab)** paper w/ Exscientia co-authors (org-halo trim).
- **Org context:** Recursion **completed its acquisition of Exscientia 2024-11-20** (SEC 6-K confirmed). Exscientia is now part of Recursion, which already holds the LOWE row.

**Decision — NO row** (default-NO discipline holds on all three counts): (1) no new bottleneck — its MD work spreads across already-owned cells (binding affinity→FEP+, AL triage→LOWE, NNP correction/torsion fitting→Espaloma + MLIP engines); (2) not a new player — now part of Recursion; (3) its standout claim, once corrected, is a **third instance of the autonomy gap** (orchestrate/restart/triage, but don't autonomously mutate physics) alongside Multisim and Orion.

**Done:** banked point (3) as a one-sentence hardening of the "open gap — autonomy" bullet in *Where Project Prime fits* — names Exscientia/BioSimSpace and explicitly states the auto-recovery claim could not be substantiated (inoculates the thesis against the exact misconception). NO matrix row, NO scope-out row (not materials — it's a deliberate redundancy no-add). Frontmatter `revision: 6`. New fabrication pattern logged in [[phase1-report-format]]: **fabricated recovery-feature / uncited-takeaways spoof of Prime's niche.** Thesis intact and strengthened.

---

## 2026-05-27 — Phase 1 report: Espaloma added as matrix row (rev. 5) ➕

**Context:** verify-and-compress pass on a Gemini intake block for **Espaloma** (Chodera Lab / OpenFF). Verified mechanism + links against arXiv, the `choderalab/espaloma` repo, and the Chem Sci 2024 paper.

**Verified (load-bearing, kept):**
- **DOES-IT-RUN-MD: no — confirmed** (two independent sources). Output is an OpenMM `System` (`openmm_system_from_graph`), not a trajectory; a standard engine integrates. Crucial distinction from the MLIP engine rows (AI2BMD/GEMS compute forces on-the-fly; Espaloma pre-computes **classical** MM parameters).
- **CAMP prep-step / force-field generator** + **BOTTLENECK setup/force-field brittleness** — confirmed (GNN replaces rule-based GAFF/antechamber atom-typing).
- **DOMAIN biomolecular** — confirmed (small molecules, peptides, nucleic acids; binding free energies).
- LIMIT (classical form → no bond-breaking; OOD graph → unphysical force constants → blow-up) — physically sound; OOD-instability is INFERRED in the block so phrased as *can*, not documented.

**Corrected/dropped:**
- **ORG: dropped unverified "extensive Relay Therapeutics collaboration/utilization."** Chem Sci `D4SC00690A` authors = MSKCC (Chodera) + Asahi Kasei Pharma; Relay not in author list and flagged unverified in the block's own UNCERTAINTIES. Row org = **Chodera Lab (MSKCC) / Open Force Field**; Relay noted as unverified in Sources.

**Link verification:** D4SC00690A = *Machine-learned molecular mechanics force fields from large-scale quantum chemical data* (espaloma-0.3, Takaba et al., Chem. Sci. 2024) ✅ · arXiv:2010.01196 = *End-to-End Differentiable MM Force Field Construction* (Wang/Chodera, original method) ✅ · github.com/choderalab/espaloma ✅.

**Decision — earns a ROW:** "no MD" ≠ scope-out (BCS is also a no-MD prep step and is a row). Espaloma fills the empty **setup/force-field-brittleness** cell via a distinct mechanism (ML → *classical* MM params, unlike MLIP engines), from a prominent player. Most Prime-adjacent tool yet: ML alternative to Prime's antechamber/tleap ligand-prep skill, AND its OOD failures manufacture exactly the runtime explosions Prime's recovery catches → reinforces the thesis (setup brittleness gets solved; runtime-failure recovery stays unowned). New recurring pattern logged in [[phase1-report-format]]: unverified org-collaboration halo (Relay).

**Done:** matrix row after NVIDIA BCS (prep-tier); "force-field setup brittleness" problem bullet; prep-tier sentence in "Where Project Prime fits" (feeder-not-rival framing); Sources sub-block (3 links, verified); frontmatter `revision: 5`. Thesis intact.

---

## 2026-05-27 — Phase 1 report: Aqemia added as matrix row (rev. 4) ➕

**Context:** verify-and-compress pass on a Gemini intake block for **Aqemia** (generative + MDFT platform). Re-checked domain/mechanism/links against the sources via WebFetch/WebSearch rather than trusting the block.

**Verified (load-bearing, kept):**
- **DOES-IT-RUN-MD: no — confirmed.** MDFT = classical DFT-of-liquids (HNC closure on the molecular Ornstein–Zernike equation), a 3D-grid functional minimization; no trajectory integration.
- **CAMP replace-the-simulation — confirmed.** Same boundary camp as BioEmu/NeuralPLexer2 (already rows). "No MD" ≠ scope-out here; the materials scope-outs are excluded for *domain*, not for skipping MD.
- **BOTTLENECK binding-affinity / HTVS — confirmed** (arXiv COVID paper).
- **DOMAIN biomolecular — confirmed** (3ClPro protease screen). Passes the domain gate.
- LIMIT (static input conformation → blind to flexibility/induced-fit) — physically sound; the reason it doesn't threaten Prime's niche.

**Intake errors caught:**
- **Paper role-swap.** Block implied JCIM `0c00526` was the applied biomolecular demo. Actual: JCIM 2020 = *FreeSolv hydration free energies via MDFT* (small-molecule **physics**, within 1 kcal/mol @ ~2 cpu·min/mol); the **biomolecular** evidence is arXiv:2109.03565 (*COVID-19 drug repositioning via absolute binding free energy*, 1,400 FDA drugs vs SARS-CoV-2 3ClPro). Sources block now labels each correctly.
- aqemia.com is marketing-only ("generative AI and deep physics") — kept as the org link, not as mechanism evidence.

**Dropped from the block:** the speculative `VS-PRIME` "Prime generates Aqemia's relaxed input conformation" (intake's own UNCERTAINTIES admit it's unclear they even do MD relaxation) → replaced with the defensible "static-conformation blindness *is* Prime's dynamic regime; complementary, not rival." Also dropped the generative-loop architecture (RL/GFlowNets black box) as off-lens.

**Decision — earns a ROW (not scope-out):** genuinely new *player* + distinct *mechanism* filling an empty cell — the only "replace-the-sim" approach aimed at **binding affinity** (FEP+ computes ΔG *via* MD; BioEmu→ensembles, NeuralPLexer→structures; none compute binding ΔG without a trajectory). Reinforces the thesis: a third "remove the simulation" play that does zero runtime-failure recovery.

**Done:** matrix row after NeuralPLexer2; problem-centric "binding affinity without the trajectory" bullet; added to the "remove the simulation" positioning line (structure / ensemble / binding ΔG); Sources sub-block (3 links, verified 2026-05-27); frontmatter `revision: 4`. Thesis intact.

---

## 2026-05-26 — Phase 1 report link-complete; submittable ✅

**Context:** re-reviewed advisor feedback against the current [[Phase1_Report]] (rev. 2). The matrix format, 3-bullet who/what/trend exec summary, Microsoft (AI2BMD, BioEmu), NVIDIA (ALCHEMI-BMD/BCS) and DeepMind (GEMS) were all already in place — the only remaining bounce risk was the advisor's hard "every tool needs a working link" rule.

**Done today:**
- Filled the **4 `⟨LINK NEEDED⟩`** rows (WebSearch-verified, official/primary), in both the matrix and the Sources block: **FEP+** (`schrodinger.com/platform/products/fep/`), **Multisim** (official Schrödinger Python API `multisimstartup` page — documents the `-set` mutation flag the report's framing leans on), **Orion** (`eyesopen.com/orion/platform`), **NeuralPLexer** (peer-reviewed *Nature Machine Intelligence* 2024, DOI `10.1038/s42256-024-00792-z`, + Iambic NP2 blog for the v2 specifics; report cites "NeuralPLexer2" but the load-bearing link is the original-method paper).
- Removed the stale "links to fill" note in Sources; bumped frontmatter `revision: 3`. `grep "LINK NEEDED"` → 0 matches.
- **"Major tech players" ask resolved as links-only** (user decision): big-tech MD coverage (Microsoft / NVIDIA / DeepMind) is already comprehensive per memory `phase1-report-status` ("returns went flat"). Considered but did **not** add — NVIDIA BioNeMo (umbrella over the existing ALCHEMI rows), Meta ESMFold, AWS (Orion's host) — all either already represented by ALCHEMI or adjacent/structure/infra, not biomolecular MD.

**State:** report is submittable. No outstanding link gaps.

---

## 2026-05-25 — Phase 1 report restructured to competitor-matrix format (advisor feedback) 📝

**Context:** advisor reviewed v1 of [[Phase1_Report]] — wants it tighter and more actionable: add **Microsoft + NVIDIA**, give every org an **exact MD scenario** in a table, ensure **every tool has a working link**, and convert the exec summary to who/what/dominant-trend bullets.

**Done today:**
- Rewrote `Phase1_Report.md` (rev. 2) into the matrix format: 3-bullet exec summary, a `[Org] | [Tool] | [Exact MD Scenario] | [Link]` competitor matrix, condensed trends + positioning, consolidated sources. Cut the round-by-round methodology narrative (it lives here in the Dev_Log instead).
- Added clearly-marked **placeholder rows for NVIDIA + Microsoft** (candidates flagged unverified: NVIDIA→BioNeMo/NIM, MS→Azure Quantum Elements/MatterGen/MatterSim) — slots for the user's in-progress research.
- Flagged **4 missing links** (Schrödinger FEP+, Multisim, OpenEye Orion, Iambic NeuralPLexer2) as `⟨LINK NEEDED⟩` rather than fabricating URLs.
- Honesty note baked into the matrix: J&J Mol Agent and Tippy are adjacent (ML / infra), not MD mechanics — mapped as such.

**Microsoft row filled (same session):** **AI2BMD** (Microsoft Research + GHDDI) — ML-force-field (ViSNet GNN) ab initio-accuracy biomolecular MD; binding free energy / lead optimization, protein-folding ΔG/Tm, pKa, NMR ³J. Sourced to *Nature* 2024 (`10.1038/s41586-024-08127-z`), *Nat. Commun.* 2024 ViSNet paper, bioRxiv 2023, and the `github.com/microsoft/AI2BMD` repo. Framed as an **engine-layer** play (swaps the force field, not the orchestrator) → a candidate to run behind Prime's `ENGINE` seam, and notably depends on AmberTools for PDB prep (same substrate Prime automates).

**NVIDIA row filled + MatterSim scoped out (same session):**
- **NVIDIA → ALCHEMI Batched MD (BMD) NIM** — GPU-batched ML-interatomic-potential (MACE/AIMNet2/TensorNet) MD packaged as a deployable microservice. **Links WebFetch-verified** (docs page resolves, confirms drug-discovery + high-throughput use cases). Framed as engine-layer + the clearest "microservices" evidence for the dominant-trend bullet; defense caveat noted (MLIPs aren't standard explicit-solvent protein–ligand FF). Dropped the unverifiable `nvalchemi-toolkit` GitHub link.
- **Microsoft MatterSim → scoped out** as a boundary marker (universal ML-FF for *inorganic materials*, out of biomolecular-MD domain; cf. Iambic on the other boundary). User chose scope-out over a matrix row.
- **ML-enhanced-sampling review (Zhu et al., *Chem. Rev.* 2025, arXiv:2509.04291) → background citation, NOT a matrix row.** It's a methodology *review*, not a competitor tool — no `TOOL` to place. Verified + added as Sources "Background" + one contrast sentence in the BioEmu entry: two ML routes to the rare-event bottleneck — BioEmu skips MD and emulates equilibrium; enhanced sampling stays in MD with learned CVs + neural biasing potentials. Orthogonal methodology Prime could run, not a competitor.
- **Schrödinger MPNICE → scoped out** (materials). User asked if arXiv:2505.06462 was in the vault — it was not; verified + assessed. Paper title = *Efficient Long-Range ML Force Fields for **Liquid and Materials Properties*** (Weber et al.); product page = Schrödinger **Materials Science** suite (batteries/polymers/OLED, 89 elements, OPLS4/5). Engine-layer ML-FF (charge-equilibration for long-range electrostatics) but **materials domain**, so scoped out (4th materials item). **Caught an intake overclaim:** the block's "built to drive Desmond / drug-discovery MD" is NOT supported by the paper or product page — MPNICE is materials-side. Kept as a datapoint that the ML-FF wave reached the deterministic incumbents.
- **Google DeepMind GNoME → scoped out** (materials). Crystal-stability discovery GNN (2.2M predicted, ~380k stable, *Nature* 2023) — **doubly out of scope**: materials domain *and* not an MD engine (static discovery, upstream of any sim). Triggered **consolidation** of the three materials-domain scope-outs (MatterSim, differentiable-sim, GNoME) into one "Scoped out — materials-domain" subsection + one sources block, with an explicit rationale (turns scattered omissions into a deliberate, defensible boundary for the advisor).
- **Differentiable atomistic simulation (UCLA/DeepMind/OpenAI, JCTC 2025) → new TREND, scoped-out tool.** User flagged it as "a different trend." Verified (pubmed) = **materials domain** (Si/SiO₂ elastic constants, phonons), so per the MatterSim discipline it's NOT a biomolecular-MD matrix row — but the *paradigm* (make the whole MD loop differentiable → backprop macroscopic-property error → gradient-optimize FF params) is a genuine emerging trend, added as a "Differentiable simulation" bullet in Trends. **Corrected intake bottleneck** from "setup/force-field brittleness" to force-field **parameterization/optimization** (microscopic→macroscopic gap), distinct from tleap/antechamber setup brittleness.
- **Google DeepMind GEMS → matrix row** (links WebFetch-verified; DeepMind page confirms title + *Sci. Adv.* 2024). **Corrected TWO intake fields:** CAMP `replace-the-simulation → engine-layer` (GEMS runs real MD, computing forces for integration — it does *not* skip the sim like BioEmu; it's a direct ML-FF rival to AI2BMD), and BOTTLENECK `rare-event sampling → accuracy-vs-cost` (its problem is the MLIP long-range blind spot on large proteins, same as AI2BMD). Report draws the sharp AI2BMD-vs-GEMS contrast: fragmentation at **runtime** (AI2BMD, stitch forces) vs at **training** (GEMS, learn from top-down DFT chunks, no stitching).
- **NVIDIA ALCHEMI-BCS → matrix row** (links WebFetch-verified; DOI = the AIMNet2 *Chem. Sci.* paper). Companion NIM to BMD: BCS does high-throughput **conformer search** (static energy minima via AIMNet2 + GPU batching, 10–100 ms/conformer), BMD does the dynamics → BCS→BMD = an ALCHEMI prep→dynamics pipeline. **Corrected the intake's bottleneck label** from "rare-event sampling" to "conformer search / structural prep" — rare-event sampling is dynamic barrier-crossing (BioEmu); conformer search finds static minima. Sources block consolidated to "ALCHEMI suite (BMD + BCS)".
- **Microsoft BioEmu → matrix row** (links WebFetch-verified) — generative diffusion model that emulates protein equilibrium ensembles *without* MD integration; the "skip the MD" boundary alongside Iambic. Positioned as the sharpest "why run MD at all?" challenge, but complementary (emulates equilibrium distribution, not kinetics/pathways/explicit-solvent detail; training-distribution-bound) → a fast pre-filter feeding physically-grounded MD, not a replacement. Microsoft now appears 3× across distinct camps: AI2BMD (engine-layer), BioEmu (replace-the-sim), MatterSim (scoped out, materials).

**Next on the report:** only the **4 commercial-doc link gaps** remain (Schrödinger FEP+/Multisim, OpenEye Orion, Iambic NeuralPLexer2); fill + verify each resolves before submission. New report format is the standing convention (see memory `phase1-report-format`).

---

## 2026-05-24 — AMBER phase closed; OpenClaw handoff prepared 🏁

**Marker (no new build work).** Reviewed the pmemd test results in depth and declared the **AMBER side of Project Prime fully wrapped**: prep/analysis via conda AmberTools 24.8, MD via locally-compiled `pmemd`/`pmemd.MPI` (both test-suites green), golden-path recipe validated. The single non-ignored test diff was traced and explained — `kmmd/kmmd_pmemd_gb`, `RESTRAINT 1.1976` (ours) vs `1.2006` (ref) at NSTEP 100; `EELEC`/`EGB` bit-match — i.e. expected cross-compiler floating-point drift in a niche GPU-targeted ML-bias feature, not a build defect.

**Handoff created:** `Next_Session_Prompt_OpenClaw.md` (vault root) — a pasteable starter prompt to open the OpenClaw phase. Status markers added to `Project Prime.md` §5 roadmap; memory `project-prime-status` updated.

**Next session:** install OpenClaw + wire Gemini (AI Studio), verify a local shell step + a JSON-schema `llm-task`, then wrap golden-path Stage 2 as [[Skill_Antechamber_LigandPrep]] (system-agnostic).

---

## 2026-05-22 — pmemd built from source locally + `make test.serial` ✅

**Context:** mentor directed a local from-source **pmemd** build (`make test.serial`), reopening the source-build path that the 2026-05-21 audit had deferred to the cluster. See [[Gap_Remote_HPC_Backend]].

**Done today:**
- Installed `gcc@11` (→ `gfortran-11`, GCC 11.5.0) and `gpatch` (+ `/opt/homebrew/bin/patch` symlink) per ambermd.org/InstMacOS.php prereqs. The machine's default `gfortran` is **15.1 — too new** for Amber, so 11 is required.
- Source = **`pmemd26.tar.bz2`** (Amber26, registration-gated free academic download; MD5 verified). It's **self-contained `PMEMD_ONLY`** — separate from the conda AmberTools 24.8 that still runs tleap/cpptraj. Extracted to `~/Downloads/pmemd26_src/`.
- Built with the bundled macOS `run_cmake` (CLANG + Apple Accelerate, MPI/CUDA off, tests on). **Compiler gotcha:** `COMPILER=CLANG` hardcodes the Fortran exe to literal `gfortran` (would grab GCC-15) — fixed with a PATH shim `build/compiler_shim/gfortran → gfortran-11`. Configure confirmed `Fortran: GNU 11.5.0`. `make install` clean → `pmemd: Version 26.0` at `~/Downloads/pmemd26/`.
- **`make test.serial`: 212 comparisons passed, 0 errors.** 6 diffs — 5 Amber-flagged `(ignored)`, 1 trivial (`kmmd/kmmd_pmemd_gb` RESTRAINT 1.20 vs 1.19, gfortran-11 roundoff in a niche enhanced-sampling feature; irrelevant to explicit-solvent MD). The `make … Error 2 (ignored)` is Amber's normal Makefile behavior.

- **MPI build added (same session, per instructor "if a compiled MPI version is available, run `make test.parallel`"):** `brew install open-mpi` (5.0.9) → separate `build_mpi/` configure with `-DMPI=TRUE` into the *same* prefix, producing **`pmemd.MPI`** (Version 26.0) alongside the serial `pmemd`. **`make test.parallel` (`mpirun -np 4`): 197 comparisons passed, 0 errors, 0 MPI aborts** — same single trivial `kmmd_pmemd_gb` roundoff. Version-mismatch risk (Open MPI's Fortran `.mod` built by gfortran-15 vs our gfortran-11) did **not** bite: pmemd uses `mpif.h` (plain text), not the `use mpi` module; `OMPI_FC=gfortran-11` set as a safety override. (The log's many "exceptions are signalling: IEEE_INVALID_FLAG" lines are benign FP notes, not crashes.)

**Usage note:** PMEMD_ONLY build → `amber.sh` exports **`PMEMDHOME`** (not `AMBERHOME`); `make test.serial` runs from `$PMEMDHOME`, not the build dir. For parallel: `export DO_PARALLEL='mpirun -np 4'` then `make test.parallel`. Recipe + shim details in memory `pmemd-local-build`.

**Caveat for mentor:** this is **v26**, newer than the conda AmberTools 24.8 (GetAmber only offers v26 now). prmtop format is stable 24→26, so it runs existing topologies — flag if 24-matched was intended.

---

## 2026-05-21 — AMBER audit + golden-path protein–ligand pipeline (real complex) ✅

**Context:** user wanted to "completely set up AMBER … all the tleap and other things," suspecting missing components. Audited the install first.

**Done today:**
- **Install audit — AmberTools 24.8 in `prime-amber` is complete, nothing missing.** Verified all binaries (`sander`, `tleap`/`teLeap`, `antechamber`, `parmchk2`, `pdb4amber`, `cpptraj`, `sqm`, `reduce`, `mdgx`, `MMPBSA.py`, `packmol`, `parmed`), `AMBERHOME` exported on activation, and the full force-field/leaprc library (ff14SB/ff19SB, gaff/gaff2, all water models, DNA/RNA/lipid/GLYCAM + parm/frcmod). `pmemd` is *correctly* absent: conda-forge ships only `sander`; `pmemd`/`pmemd.cuda` is a cluster `module load`, never compiled locally.
- **Scenario A confirmed by user** — stay local with `sander`, HPC is a future swap. Recorded in [[Gap_Remote_HPC_Backend]] (still `status: open` long-term, but the near-term decision is settled).
- **Built the `golden path`** at `project-prime/golden-path/` — the first *real* protein–ligand complex run end-to-end, vs. the isolated smoke-test legs. System: **T4 lysozyme L99A + benzene (PDB `181L`)**, the textbook positive control (benzene reuses the proven GAFF2/AM1-BCC params; ALA99 is the L99A cavity mutation). Pipeline: `pdb4amber` clean → `obabel/antechamber/parmchk2` ligand → `tleap` combine + solvate TIP3P + **addions neutralize** (8 Cl⁻, 24,553 atoms) → `sander` **minimize → heat NVT → equilibrate NPT → produce** → `cpptraj` (RMSD/RMSF/ligand-RMSD/frame export) → **PLIP** (first-ever end-to-end interaction run).
- **Results, validated:** production held **299.87 K avg**; backbone RMSD 0.61 Å (stable fold); per-residue RMSF 0.23–0.62 Å (textbook: termini/loops flexible, core rigid); benzene RMSD 2.84 Å (rattles in the roomy cavity, stays bound). **PLIP correctly fingerprinted the cavity** — 6 hydrophobic contacts: LEU84, VAL87, ALA99, VAL111, LEU118, PHE153. Wall time ~16 min CPU (first uninterrupted run; a later confirmation run's clock was inflated by laptop sleep — disregard that figure).
- **Two real integration bugs found & fixed** (the kind of guardrail work that's the actual job): (1) added a **production-temperature assertion** to `run.sh` — "no NaN" alone would have green-lit a thermostat collapse; (2) cpptraj writes AMBER protonation-variant resnames (`HIE/CYX/…`) that **PLIP misreads as phantom ligands** — `analyze.cpptraj` now normalizes them to standard PDB names, and `run.sh` asserts only `BNZ` is detected. Cross-linked from [[Skill_Antechamber_LigandPrep]].
- **HPC-swap seam baked in:** all MD goes through one `run_md()`/`ENGINE` wrapper; Scenario B = `ENGINE=pmemd.cuda` + a DPDispatcher `SSHContext`, **no recipe-file changes**.
- Vocabulary updated (NPT/barostat/addions, `smoke test`, `golden path`); `.gitignore` extended so generated artifacts stay untracked while recipe files (`.leap/.in/.cpptraj/.sh`) are tracked.

**State of the vault:** The golden path is the new canonical known-good recipe that the OpenClaw skills will automate (supersedes the smoke-test as the reference; smoke-test stays as the fast env check). Phase 2 AMBER work is done end-to-end on a realistic system.

**Next session:** OpenClaw install + Gemini (AI Studio) wiring; then wrap the golden-path stages as OpenClaw skills, starting with [[Skill_Antechamber_LigandPrep]] (golden-path Stage 2 is its acceptance test).

---

## 2026-05-20 — LLM provider decision: Google AI Studio only (Ollama dropped)

**Done today:**
- **Provider locked to Google AI Studio** for the agent's reasoning layer. Ollama / local-LLM paths are off the table — user's Mac doesn't have the headroom to host a usable-size model. User has **$300 AI Studio credits / 90-day window**, more than sufficient for the demo scope.
- Original 2026-05-14 plan (Ollama primary + AI Studio fallback) is superseded. [[project-prime-status]] memory updated; future skill designs target a single-provider (Gemini) API.

**State of the vault:** No vault content edits — this is a config / planning decision, captured in memory + Dev_Log only. Phase 2 step 3 (OpenClaw init + LLM wiring) is now simpler since the LLM half is single-provider.

**Next session:**
- OpenClaw distribution research (pip / npm / source?) → install → wire to AI Studio (Gemini Flash default, Gemini Pro for the few heavy-reasoning calls).
- Hello-world skill that dispatches a trivial shell command before pointing it at AMBER.

---

## 2026-05-19 (cont. 2) — End-to-end AMBER smoke test PASSED ✅

**Done today:**
- Built a two-leg smoke test at `project-prime/smoke-test/`. Total wall time: **42 s** (Leg A 40 s, Leg B 2 s) on this Mac CPU.
- **Leg A — alanine dipeptide MD (`aladip/`):** field-standard hello-world, `tleap → sander minimize → sander heat (0→300 K, 10 ps) → sander NVT (10 ps) → cpptraj`. Force fields: ff14SB + TIP3P. ~1500-2000 atoms. Results sensible: minimization energy −4811 → −6694 kcal/mol, RMSD < 0.4 Å throughout, RoG steady ~3.0 Å, no NaN. Asserts that `dt = 2 fs + SHAKE` (Project Prime hard rule) ran clean.
- **Leg B — benzene ligand prep (`benzene/`):** `obabel "c1ccccc1" → antechamber (GAFF2 + AM1-BCC) → parmchk2 → tleap load test`. All 6 C atoms typed `ca`, all 6 H atoms `ha`; charges symmetric C=−0.130 / H=+0.130, sum 0; one trivial improper-torsion frcmod entry. Catches the antechamber/sqm failure mode flagged in [[Skill_Antechamber_LigandPrep]].
- Wrapped both legs in `run.sh` with hard assertions (no `NaN` in sander outputs, non-empty `.nc`, all expected dat files present). Recipe-style inputs (`.leap`, `.in`, `.cpptraj`, `.sh`) live in `smoke-test/` at project-prime root (NOT `runs/*` which is fully gitignored); generated `.nc`/`.rst`/etc. still ignored by extension.
- Updated [[Infra_AMBER_Install]] with the smoke-test section (replaces the prior "deferred" placeholder).

**State of the vault:** Phase 2 step 1 fully closed — install **and** end-to-end validation both green. The `prime-amber` env can now be treated as a known-good substrate. The smoke-test directory is the canonical baseline that OpenClaw skills will eventually replicate programmatically.

**Next session:**
- **OpenClaw install** + LLM provider wiring (Ollama primary, Gemini Flash fallback) per `Project Prime.md` Phase 2 step 4.
- Start sketching the first real skill — probably the `Antechamber` skill (Leg B becomes its acceptance test).

---

## 2026-05-19 (cont.) — Phase 2 step 1: AMBER installed locally ✅

**Done today:**
- Confirmed conda-forge ships a native osx-arm64 build of **AmberTools 24.8** (`CONDA_SUBDIR=osx-arm64 mamba search …`). Picked the `nompi` py3.11 variant — lighter than `mpich`, sufficient for serial `sander` on a single laptop.
- Created conda env **`prime-amber`** with a single combined solve: `mamba create -n prime-amber -c conda-forge -y python=3.11 'ambertools=24.8=*nompi*' plip`. One solver run, ~minutes wall-time.
- Verified arm64-native (not Rosetta): `file $(which sander)` → `Mach-O 64-bit executable arm64`.
- SOP exit conditions met: `which sander` resolves under `$CONDA_PREFIX/bin/`, `cpptraj --help` prints usage. Also verified `tleap`, `antechamber`, `parmchk2`, `pdb4amber`, and PLIP 3.0.0 (`plip -h`).
- Exported `mamba env export --no-builds → project-prime/env.lock.yml` (119 lines) for reproducibility.
- Documented in [[Infra_AMBER_Install]]: env summary table, exact commands, pin rationale, verification block, three small gotchas (mamba `--subdir` syntax, missing `plip.__version__`, sander `-h` quirk).

**State of the vault:** Phase 2 step 1 closed. `prime-amber` env is the canonical local MD runtime — every future skill that touches AMBER binaries should `conda activate prime-amber` first. SOP's "edit `~/.bashrc`" step was a no-op because shell is zsh and conda init was already in `~/.zshrc` from the prior Homebrew Miniforge install.

**Next session:**
- **End-to-end MD validation** — tiny TIP3P water box (and ideally an `antechamber`+`parmchk2` ligand leg on a trivial molecule like benzene) in `project-prime/runs/smoke-test/`. Catches the AmbiguousAtomType / sqm-failure modes that are the #1 real breakage when antechamber later runs in agent context (see [[Skill_Antechamber_LigandPrep]]).
- After that: OpenClaw install (`npm install -g openclaw@latest`) + LLM provider wiring (Ollama primary, Gemini Flash fallback).

---

## 2026-05-19 — Phase 1 closed; transitioning to AMBER install

**Done today:**
- NotebookLM verification of the OpenClaw substrate paper (arXiv:2603.25522) caught real overclaims in the vault. Corrections propagated through every affected note. Strongest paper-cited element: **bounded recovery + methane-oxidation case study** — anchored in [[Skill_Bounded_Recovery_AMBER]].
- Memory Provenance properly sourced to **OpenBrain** (not the OpenClaw paper); renamed from "Providence" (propagated typo); corrected from 3 labels to **4** (added `imported from transcript`). Old file deleted; all wikilinks updated.
- DPDispatcher local-shell mode verified against DPDispatcher official docs (`batch_type: "Shell"` + `LocalContext`) — local-only execution plan unblocked.
- Demoted `Arch_Taskboard_Manifest` to a planner-agent design idea (it's the plan-and-execute pattern, not OpenClaw-novel); demoted `OpenClaw_Self_Evolution` (MetaClaw / OpenClaw-RL) to aspirational, out of report scope.
- Three-tier discipline now in effect across the vault: ✅ paper/source-cited · 🟡 design idea / our framing · ⚪ aspirational. Tier badges at the top of every affected note.
- Phase 1 report written in both full ([[Phase1_Report]]) and brief ([[Phase1_Report_Brief]]) versions.

**State of the vault:** Phase 1 is closed. Citation discipline is in place — the report cites *underlying patterns* from established literature for design choices that aren't OpenClaw-paper-novel, and the OpenClaw-paper-confirmed mechanics (Lobster engine, `llm-task`, approval gates, DPDispatcher lifecycle, bounded recovery) are clearly labeled. Nothing unverified is masquerading as paper-grounded.

**Next session — Phase 2 step 1: install AMBER + agent stack locally.**
- Hardware: macOS, CPU-only (no NVIDIA → no `pmemd.cuda`).
- Path: `conda install -c conda-forge ambertools` (gives `sander`, `tleap`, `antechamber`, `cpptraj`) + `pip install plip`.
- Validate end-to-end by hand on a tiny solvated ligand or small peptide *before* writing any skill — need a working baseline the agent will automate.
- Then `npm install -g openclaw@latest` and configure the LLM provider (clarify GCP credits vs. AI Studio first; Gemini Flash as primary; Ollama as offline fallback).

Continuation happens in a fresh chat to keep that session's context window short and fast for shell back-and-forth.
