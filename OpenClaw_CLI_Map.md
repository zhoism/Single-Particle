---
title: "OpenClaw CLI Map"
type: reference
tags: [openclaw, cli, reference, day-3, substrate]
status: living
created: 2026-06-03
---

# OpenClaw CLI Map

**Status:** ✅ Primary-source-cited (local docs tree at `~/.nvm/versions/node/v24.14.1/lib/node_modules/openclaw/docs/` plus Day 1–3 empirical findings). This is the human-readable graph node consolidating what [[openclaw-canonical-paths]] memory captures for Claude sessions.

> **Read this when:** authoring a SKILL.md, debugging an agent run, choosing a tool name, or trying to remember whether the cooldown is per-profile or per-model. Use [[Phase3_Taskboard_Manifest]] for what we're building; use this note for how the substrate behaves.

---

## What OpenClaw actually is (the layered picture)

OpenClaw 2026.5.28 (`npm i -g openclaw@latest`, Node 24.x via nvm) is a **local agent runtime + gateway + tool registry + skill loader**. Four layers stack inside one Node process:

| Layer | What it does | Where it lives |
|---|---|---|
| **Gateway** | LaunchAgent daemon on `127.0.0.1:18789`. RPC surface. Owns auth profiles, sessions, channels (Discord/Slack/Telegram), and the agent runtime instance. | `~/Library/LaunchAgents/ai.openclaw.gateway.plist`; logs at `~/Library/Logs/openclaw/gateway.log` |
| **Agent runtime** | The agent-turn loop: intake → context → model call → tool calls → streaming → persistence. Runs **in-process** in the gateway. Tag in trace: `runner: "embedded"`. | source at `src/agents/embedded-agent-runner/` (in the installed pkg) |
| **Tool registry** | The fixed set of tools the agent can call: `exec`, `process`, `image`, `web`, `apply_patch`, etc. Plus optional plugin tools (`llm-task`, `lobster`). | `src/agents/agent-tools*.ts` |
| **Skill loader** | Discovers `SKILL.md` files across multiple roots, applies precedence, snapshots eligible skills into the system prompt at session start. | `src/agents/sessions/` |

OpenClaw is the **substrate** in our [[Phase3_Taskboard_Manifest]] architectural framing. The agent loop, tool registry, and skill loader are OpenClaw-owned; the planning/recovery layers and the chemistry skills are **our** contribution sitting on top.

---

## The agent loop — what actually happens in a turn

From `concepts/agent-loop.md`:

```
intake → context assembly → model inference → tool execution → streaming replies → persistence
```

For a `--json` agent turn, the trace records:

```
runId, status, summary,
result: {
  payloads:  [{ text, mediaUrl }],          ← final assistant message
  meta: {
    durationMs,
    agentMeta: { sessionId, sessionFile, provider, model,
                 contextTokens, usage, lastCallUsage, promptTokens, contextBudgetStatus },
    finalAssistantVisibleText,               ← the canonical final text
    finalAssistantRawText,                   ← pre-suppression
    toolSummary: { calls, tools, failures }, ← counts only (NOT args/stdout)
    executionTrace: { winnerProvider, winnerModel,
                      attempts: [{ provider, model, result, stage }],
                      fallbackUsed, runner: "embedded" },
    requestShaping: { authMode, thinking },
    completion: { stopReason, finishReason },
    stopReason
  }
}
```

Three things to internalize:

1. **The `--json` trace gives you summary counts + the final assistant text, not raw tool I/O.** If you need to know what the agent ran via `exec` and what stdout it got back, your wrapper has to log that itself. The substrate won't surface it.
2. **Sessions are persistent**. `sessionId` + `sessionFile` (`~/.openclaw/agents/main/sessions/<uuid>.jsonl`) survive across `openclaw agent` invocations. Subsequent calls with the same `--session-key` resume; without one, a new session.
3. **The default thinking level for `agent` is `minimal`** (verified in `requestShaping.thinking`). Override via `--thinking off|low|medium|high|...`. For Gemini, `/think adaptive` maps to Gemini's dynamic thinking.

### What an agent turn round-trip looks like (latency)

A turn with N tool calls is roughly:

```
model_call_0 (decide + emit tool call 1)
exec_call_1
model_call_1 (read result + emit tool call 2)
exec_call_2
...
model_call_N (synthesize + emit final text)
```

So N tool calls → **N+1 LLM round-trips**. Each round-trip pays Gemini Flash first-token latency (variable: 10s on a good day, ~100s under load). Empirically (1c attempt 4, 2 exec calls, default thinking minimal): **311s total wall time**. Per-call token work is cheap (`lastCallUsage` showed 719 new input tokens against 16,226 cache hits); the wall time is dominated by API latency per round-trip.

**The design implication is large** — see [[#Stage 2 design intuition]] below.

---

## The `exec` tool — what we use to shell out

From `tools/exec.md`. **The shell tool is named `exec`**, not `bash`. Tool trace records `tools: ["exec"]`.

### Default behavior (no custom config)

| Setting | Default | Effect |
|---|---|---|
| `host` | `auto` → resolves to `gateway` (sandbox is off by default) | Runs on the host machine, not in a container |
| `security` | `full` | No allowlist enforcement |
| `ask` | `off` | No approval prompts |
| `timeout` | `tools.exec.timeoutSec` = 1800s (30 min) | Per-call override via `timeout` param; `timeout: 0` disables |
| `yieldMs` | 10000 | Auto-backgrounds at 10s unless `background: true` set immediately |

That's "YOLO mode" from the defaults. **`exec` is a mutating shell** — can create, delete, modify files anywhere the user can. Disabling other filesystem tools (`write`, `edit`, `apply_patch`) doesn't make it read-only. Day 1b empirically confirmed: bash-equivalent task ran without any approval prompts.

### Configurable knobs that matter for us

- `tools.exec.host`: `auto`|`sandbox`|`gateway`|`node` — not a hostname.
- `tools.exec.mode`: `deny`|`allowlist`|`ask`|`auto`|`full`. `auto` runs deterministic allowlist matches directly, then routes remaining through OpenClaw's auto reviewer before asking a human.
- `tools.exec.pathPrepend`: list of dirs prepended to PATH (gateway and sandbox only — `env.PATH` overrides are REJECTED for host exec).
- `tools.exec.safeBins`: stdin-only safe binaries (do not add interpreters here).
- `tools.exec.strictInlineEval`: when true, `python -c`, `node -e`, etc. require explicit approval.
- `tools.deny: ["exec"]` to hard-disable. `tools.allow: [...]` to enable allowlist mode.

### Companion tools

- **`process`** — manages long-running/backgrounded exec sessions: `poll`, `send-keys`, `paste`, `submit`. Useful for tmux-style interactions.
- **`apply_patch`** — sub-tool for structured multi-file edits. OpenAI/Codex only; not relevant for Gemini.

### Approvals system

Configured in `~/.openclaw/exec-approvals.json`. Two interfaces:
- `openclaw approvals {get|set|allowlist}` — manage rules.
- `openclaw exec-policy {show|set|preset}` — preset shortcuts: `yolo`, `cautious`, `deny-all`.

We're effectively in `yolo` posture and that's appropriate for trusted local skill development. When Stage 8 (recovery skill) lands, we may want `cautious` with explicit allow rules for the chemistry binaries.

---

## SKILL.md authoring — the spec

From `tools/skills.md`, `tools/creating-skills.md`, and the bundled `skill-creator/SKILL.md` (the meta-skill written by OpenClaw authors).

### Skill folder shape

```
<skill-name>/
  SKILL.md
  scripts/      optional deterministic helpers (this is where our wrapper.py lives)
  references/   optional docs loaded only when needed
  assets/       optional output resources/templates
  agents/       optional UI metadata
```

### Minimum SKILL.md

```markdown
---
name: antechamber-ligandprep
description: "Parameterize a single ligand for AMBER MD via antechamber→parmchk2→tleap-ready outputs."
---

# antechamber-ligandprep

Use when the user needs ligand parameters (.mol2 + .frcmod) for an AMBER simulation.

## Workflow

1. Invoke `{baseDir}/scripts/wrapper.py --input <path> --output <dir> [--res-name <name>] [--net-charge <n>]`.
2. Read the JSON result. On `success: true`, the paths under `outputs` are ready for tleap.
3. On failure, surface the `errors` array verbatim.
```

### Frontmatter fields

**Required:**
- `name` — kebab-case slug, lowercase letters/digits/hyphens. Matches the slash command.
- `description` — quoted, one-line, trigger-relevant. Noun phrase preferred.

**Optional top-level:**
- `homepage`, `license`, `compatibility` (free-text)
- `user-invocable: true` (default) — exposes as `/<name>` slash command
- `disable-model-invocation: false` (default) — when true, keeps skill out of model prompt but still runnable as explicit slash command
- `command-dispatch: "tool"` + `command-tool: "<name>"` + `command-arg-mode: "raw"` — slash command dispatches direct to a tool, bypassing the model
- `allowed-tools: [...]` — accepted by local OpenClaw skills

**The `metadata` field is special — it MUST be single-line JSON.** The embedded parser only handles single-line keys for `metadata`. So:

```yaml
metadata: { "openclaw": { "requires": { "bins": ["antechamber", "parmchk2", "obabel"], "env": ["AMBERHOME"] }, "os": ["darwin"] } }
```

NOT multi-line YAML. This is a load-bearing parser quirk; the upstream `~/Downloads/Single Particle/upstream-reference/.../antechamber/SKILL.md` violates this (uses multi-line YAML metadata) — OpenClaw's parser may or may not accept it.

### `metadata.openclaw.requires` gating

These fields filter at load time — if the requirement isn't met, the skill is silently skipped (not loaded into the prompt):

- `bins: ["antechamber", "parmchk2"]` — ALL must exist on PATH.
- `anyBins: ["pmemd", "sander"]` — at least one must exist.
- `env: ["AMBERHOME"]` — env var must exist or be in config.
- `config: ["plugins.entries.foo.enabled"]` — openclaw.json paths must be truthy.

Plus `os: ["darwin"]` for platform filter, `always: true` to skip all gating, `emoji`, `primaryEnv`, `install: [{...}]` for installer hints.

### `{baseDir}` placeholder

Use in the SKILL.md body to reference paths inside the skill folder. OpenClaw substitutes the absolute folder path at runtime. Example: `{baseDir}/scripts/wrapper.py`.

### Hard rules from skill-creator/SKILL.md (authoritative)

- Keep SKILL.md **lean** — "Codex is already capable"; don't teach the model how to be an AI.
- **Trigger-critical facts only in `description`**.
- Quote frontmatter `description`.
- Move long examples/docs to `references/`; scripts to `scripts/`; templates to `assets/`.
- **No extra README/changelog/setup docs** inside a skill unless they're actual task references.
- Validate YAML frontmatter after edits.

### Token cost of a skill in the system prompt

Formula: 195 base (if ≥1 skill loaded) + 97 per skill + length of name/description/location strings. Roughly ~24 tokens per skill plus your field lengths. Lean descriptions help; verbose `description` text shows up in every turn.

---

## Skill loading — where they live, precedence, registration

### Skill roots, highest precedence first

| # | Source | Path |
|---|---|---|
| 1 | Workspace skills | `<workspace>/skills` |
| 2 | Project agent skills | `<workspace>/.agents/skills` |
| 3 | Personal agent skills | `~/.agents/skills` |
| 4 | Managed/local skills | `~/.openclaw/skills` |
| 5 | Bundled | shipped with `openclaw` npm pkg |
| 6 | Extra dirs | `skills.load.extraDirs` config |

For our `main` agent, `<workspace>` = `~/.openclaw/workspace/`. Same-name conflict resolves to the highest source.

### Where Project Prime skills should live

**Runnable code lives under `/Users/kevinzhou/Downloads/Single Particle/project-prime/`** per [[CLAUDE.md]] — git-tracked separately from the vault. So our skills are at:

```
/Users/kevinzhou/Downloads/Single Particle/project-prime/skills/<skill-name>/
  SKILL.md
  scripts/wrapper.py
  references/
  test_acceptance.sh
```

Three options to make OpenClaw discover them:

| Option | Mechanism | Pros | Cons |
|---|---|---|---|
| **`skills.load.extraDirs`** ✅ | Add path in `openclaw.json` | Source-of-truth stays in git, no copies, lowest precedence is fine absent conflicts | Lowest precedence — bundled with same name would win |
| `openclaw skills install <path> --as <slug>` | Copies into workspace | Standard install path | Breaks git ownership — copy diverges from source |
| Symlink workspace → project-prime/skills | Requires `skills.load.allowSymlinkTargets` | Source stays in git | Symlink resolution can be fragile across machines |

**Recommended: `skills.load.extraDirs`** for our case. Patch shape:

```json5
{
  skills: {
    load: {
      extraDirs: ["/Users/kevinzhou/Downloads/Single Particle/project-prime/skills"],
      watch: true,
      watchDebounceMs: 250
    }
  }
}
```

`watch: true` picks up SKILL.md changes mid-session (otherwise: gateway restart or `/new` for next session).

### Per-agent allowlist

```json5
{ agents: { defaults: { skills: ["antechamber-ligandprep", "tleap-build", "sander-run"] } } }
```

If `agents.defaults.skills` is omitted, all eligible skills are available. If set, it's an allowlist. Per-agent `agents.list[].skills: [...]` is the final set for that agent (does NOT merge with defaults). Empty list = no skills.

---

## Model failover + auth cooldown — real semantics

From `concepts/model-failover.md`. Two-stage failure handling:

1. **Auth-profile rotation** within the current provider.
2. **Model fallback** to next configured model in `agents.defaults.model.fallbacks`.

### Cooldown is per auth-profile, exponential

When a profile fails on an auth/rate-limit error (or a timeout that looks like rate limiting), the profile is marked in cooldown:

```
1 min → 5 min → 25 min → 1 hour (cap)
```

Stored in `~/.openclaw/agents/main/agent/auth-state.json` under `usageStats.<provider:profile>.cooldownUntil`. Cooldown CAN be model-scoped (`cooldownModel`), meaning a sibling model on the same provider may still try — but our case has one auth profile shared between Flash and Pro, so a Flash cooldown blocks both.

### What "looks like rate limiting"

Broader than 429: includes "Too many concurrent requests", "ThrottlingException", "resource exhausted", "weekly/monthly limit reached", and **the model idle timeout we saw in 1c**. Format/invalid-request errors are TERMINAL — no retry.

### Empirical 2026-06-03

When Flash hits a 120s idle timeout, the AI Studio profile goes into 1-minute cooldown that also blocks Pro fallback (single key, both models). Diagnostics: `openclaw models status | grep cooldown` shows `[cooldown 1m]` next to the profile. Wait ≥60s before retry.

### Billing failures

Separate path: profile marked `disabled`, 5h → 24h backoff. Not what we hit, but good to know.

### Pinned profile

Sticky per-session until session reset, compaction, or cooldown. `/model <name>@<profileId>` for explicit user pinning (strict, no auto-fallback if it fails).

---

## Model idle timeout — THE 120s

From `concepts/agent-loop.md`:

> OpenClaw aborts a model request when no response chunks arrive before the idle window. ... Otherwise OpenClaw uses `agents.defaults.timeoutSeconds` when configured, capped at **120s by default**.

Configurable per-provider via `models.providers.<provider>.timeoutSeconds` to extend for slow self-hosted providers. We could raise it for Gemini if we expect long-chain agent turns:

```json5
{ models: { providers: { google: { timeoutSeconds: 240 } } } }
```

But the right answer for our project is NOT to extend the timeout; it's to make wrappers do the chaining (see [[#Stage 2 design intuition]]).

---

## Optional plugin tools — `llm-task` and `lobster`

### `llm-task` (from `tools/llm-task.md`)

JSON-only LLM call with optional JSON-Schema validation. Returns `details.json` containing parsed (and schema-validated when `schema` is set) output. Params: `prompt`, `input`, `schema`, `provider`, `model`, `thinking`, `authProfileId`, `temperature`, `maxTokens`, `timeoutMs`.

Enable:

```json5
{
  plugins: { entries: { "llm-task": { enabled: true } } },
  tools: { alsoAllow: ["llm-task"] }
}
```

**Use case in Project Prime:** Stage 7 planner. Right now, our Stage 1a test confirmed Gemini reliably emits valid JSON when prompted with "no fences, no prose" — but the planner needs schema-validated output. `llm-task` gives us schema validation without writing a retry loop.

### `lobster` (from `tools/lobster.md`)

Workflow shell — typed pipelines of tool calls with built-in approval gates and resume tokens. Runs in-process inside the gateway in embedded mode. Pipelines are **linear with conditional branching**, NOT DAGs — the vault's [[OpenClaw_Lobster_DAGs]] note overstates this; the 🟡 tier badge correctly flags the inference.

Workflow files (`.lobster`):

```yaml
name: inbox-triage
steps:
  - id: collect
    command: inbox list --json
  - id: categorize
    command: inbox categorize --json
    stdin: $collect.stdout
  - id: approve
    command: inbox apply --approve
    stdin: $categorize.stdout
    approval: required
  - id: execute
    command: inbox apply --execute
    stdin: $categorize.stdout
    condition: $approve.approved
```

**Limitation**: embedded Lobster's `openclaw.invoke` for nested tool calls is not currently reliable. Standalone Lobster CLI works.

**Use case in Project Prime:** Stage 8 (recovery skill, [[Skill_Bounded_Recovery_AMBER]]) — Tier 1 (checkpoint-restore) → Tier 2 (bounded parameter mutation with approval) is a natural Lobster workflow. For Stages 2–6 (deterministic prep/run/analysis), direct wrappers are simpler.

---

## Prompt caching — what the cache hits in our traces mean

From `reference/prompt-caching.md`. The system prompt is split at an internal **cache-prefix boundary**:

- **Stable prefix** above the boundary: tool definitions, skills metadata, stable workspace files.
- **Volatile suffix** below: `HEARTBEAT.md`, timestamps, per-turn metadata.

Changes above don't bust the prefix; changes below don't bust the suffix.

**For Google AI Studio direct API**: cache hits surface as `usage.cacheRead`. When `cacheRetention` is configured on a Gemini model, OpenClaw auto-creates/reuses/refreshes `cachedContents` resources for the system prompt. Our 1b/1c traces showed `cacheRead=16226` against `input=719` new tokens — the cache is already warm on a working session.

Configure:

```json5
{
  agents: {
    defaults: {
      models: {
        "google/gemini-3-flash-preview": { params: { cacheRetention: "long" } }
      }
    }
  }
}
```

Not urgent for our project (chemistry skills run infrequently, not bursty) but worth knowing for the Day 4+ work.

---

## Loop detection — off by default for flagship models

From `tools/loop-detection.md`. Two cooperating guards under `tools.loopDetection`:

1. **Rolling-history detector** (`enabled`) — default `false`. Watches for repeated `(tool, args)` patterns. Recommended for smaller models; flagship Gemini doesn't need it.
2. **Post-compaction guard** (`postCompactionGuard`) — default `true` unless master is explicitly `false`. Arms after a compaction-retry; aborts the run on the same `(tool, args, result)` triple within `windowSize: 3`. Error name: `compaction_loop_persisted`.

Knobs: `historySize` (30), `warningThreshold` (10), `criticalThreshold` (20), `unknownToolThreshold` (10), `globalCircuitBreakerThreshold` (30).

We've never hit a loop in our 3 substrate tests. If Stage 2+ starts looping, raise thresholds or disable specific detectors before disabling the whole guard.

---

## The CLI surface we actually use

About 50 top-level commands ship. The subset that matters for skill development:

**Inference + agent:**
- `openclaw infer model run --gateway --json --prompt "..."` — one-shot inference, no agent loop.
- `openclaw agent --agent main --message "..." --json [--thinking <level>] [--session-key <key>] [--timeout <sec>]` — full agent turn.
- `openclaw infer model list` — model catalog.

**Skills:**
- `openclaw skills list` — what's loaded for the current workspace.
- `openclaw skills info <slug>` — detail on a specific skill.
- `openclaw skills check` — show ready/missing-requirements.
- `openclaw skills install <slug>|git:<ref>|./path --as <slug> [--global]` — install (copies).
- `openclaw skills verify <slug>` — verify against ClawHub.
- `openclaw skills update --all` — update ClawHub-tracked installs.

**Models + auth:**
- `openclaw models status` — auth profile health (cooldown, etc.).
- `openclaw models auth paste-api-key --provider google` — wire a key.
- `openclaw models set <provider/model>` — set default.
- `openclaw models fallbacks add <provider/model>` — add fallback.

**Gateway + diagnostics:**
- `openclaw gateway status` / `restart` / `run --force`.
- `openclaw doctor [--fix|--repair|--generate-gateway-token]`.
- `openclaw status` — gateway, channel, model, recent session.
- `openclaw health` — detailed health.
- `openclaw logs` — tail gateway logs.

**Config:**
- `openclaw config get <path>` — single field read (use this instead of cat'ing openclaw.json).
- `openclaw config set <path> <value>` — set field.
- `openclaw config patch --file foo.json5` — bulk patch.
- `openclaw config schema` — JSON Schema for the whole config.
- `openclaw config validate` — sanity-check.

**Approvals + exec policy:**
- `openclaw approvals get|set|allowlist`.
- `openclaw exec-policy show|set|preset {yolo|cautious|deny-all}`.

**Sessions + memory + transcripts:**
- `openclaw sessions list --agent main`.
- `openclaw memory status|search|index|promote`.
- `openclaw transcripts list|show|path`.

**Channels:**
- `openclaw channels status --probe`.
- `openclaw channels capabilities --channel <id>`.
- `openclaw channels add` / `login`.

**Docs:**
- `openclaw docs <query>` — first-resort doc lookup against `docs.openclaw.ai`.

---

## Failure-mode catalog — dead-ends and traps from Day 1–3

| Symptom | Real cause | Fix / avoid |
|---|---|---|
| `Unknown model: google/gemini-2.5-flash` | google provider plugin only catalogs `gemini-3-flash-preview` / `gemini-3.1-pro-preview` in 2026.5.28 | Pin to one of the two cataloged names |
| `Unknown model` when running `infer model run` without `--gateway` | `--local` path requires duplicating model in `models.providers.google.models[]` user config | Always use `--gateway` for inference |
| Bot silent in Discord server | `groupPolicy: "allowlist"` + empty `guilds: {}` = ignore everything | Patch `channels.discord.guilds.<GUILD_ID>` with `requireMention: true` + `users: [...]` |
| `config set` rejects `channels.discord.intents.messageContent` | Hard-coded by OpenClaw; not user-configurable | Ignore the `intents:content=limited` probe label — it's a tier name, not a defect |
| `Vertex auth` paths silently fail with no errors | No `google-vertex` provider plugin in 2026.5.28 | Use AI Studio path (`google/*`); see [[openclaw-vertex-gap]] |
| Agent stalls forever then errors `LLM idle timeout (120s)` | Model didn't stream any chunks for 120s — usually because prompt prescribed tool-call topology, triggering long deliberation | Phrase prompts as goals not topology; let wrapper enforce call sequence |
| Fallback to Pro fails with `No available auth profile for google (all in cooldown)` | Flash idle-timeout cooled the shared AI Studio auth profile for ~60s; both Flash and Pro use same profile | Wait ≥60s. Check `openclaw models status \| grep cooldown` |
| Wanted to read raw exec args/stdout from `--json` trace | Substrate only exposes `toolSummary.calls/tools/failures` + `finalAssistantVisibleText` | Capture inside the wrapper itself; surface via final reply if needed |
| `openclaw models test` not found | Doesn't exist as a verb | Use `openclaw infer model run --gateway --prompt "x"` |
| `openclaw chat "<prompt>"` returns TUI | `chat` is a TUI alias only | Use `openclaw infer model run` for one-shot |
| Reaching for `bash` as tool name | It's `exec` | Use `exec`. Trace records `toolSummary.tools: ["exec"]` |
| Treating Lobster as DAG | Linear pipelines with conditional branching, not DAGs | Use as workflow shell; for true graphs, write a deterministic Python orchestrator |

---

## Stage 2 design intuition (the load-bearing payoff)

What all this means for [[Skill_Antechamber_LigandPrep]] (Phase 3 Stage 2 of the [[Phase3_Taskboard_Manifest]]):

### 1. The wrapper does the work, the SKILL.md describes the goal

Empirical: Stage 1c showed 311s wall time for 2 exec calls because each LLM round-trip costs ~100s. A real antechamber chain (`obabel → antechamber → parmchk2`) is 3 commands. If the agent orchestrates them: 4 round-trips × 100s = ~7 min for a 5-second compute job.

Architecture: **one exec call per skill turn**. The wrapper script runs the full chain internally as ordinary Python subprocesses (milliseconds apart) and returns ONE JSON envelope. The agent makes one tool call, gets one result, formulates one reply. Total LLM round-trips per skill turn: 2 (decide + report).

This isn't just performance — it's also alignment with the "lobster-like discipline" the project's [[Actionable_Recommendations]] §1 calls out. The LLM stays outside the deterministic path.

### 2. SKILL.md prose: goal-oriented, not topology-prescriptive

Stage 1c also showed that explicit "use N separate tool calls" triggers Flash to enter long deliberation that exceeds the 120s idle timeout. SKILL.md prose should say what the user can achieve, not how the agent should sequence tool calls.

Good:

> Use when the user needs ligand parameters (.mol2 + .frcmod) for an AMBER simulation. Invoke `{baseDir}/scripts/wrapper.py --input <path> --output <dir>`.

Bad:

> First call exec with obabel to convert SMILES. Then call exec again with antechamber. Then call exec a third time with parmchk2.

### 3. Wrapper returns one JSON envelope that the agent forwards mostly verbatim

The wrapper's output should be JSON the agent can interpret without thinking hard:

```json
{
  "success": true,
  "outputs": { "mol2": "...", "frcmod": "..." },
  "atom_types": ["ca", "ha"],
  "net_charge": 0.0,
  "errors": []
}
```

On `success: false`, the agent surfaces `errors` verbatim. No interpretation. The wrapper owns all error analysis; the LLM is a router.

### 4. Frontmatter

Use single-line JSON for `metadata`, kebab-case `name`, quoted noun-phrase `description`. Concrete starter:

```yaml
---
name: antechamber-ligandprep
description: "Parameterize one ligand for AMBER MD: input file → GAFF2 .mol2 + .frcmod."
license: MIT
metadata: { "openclaw": { "requires": { "bins": ["antechamber", "parmchk2", "obabel", "pdb4amber"], "env": ["AMBERHOME"] }, "os": ["darwin"] } }
---
```

### 5. Skill registration

Add `/Users/kevinzhou/Downloads/Single Particle/project-prime/skills` to `skills.load.extraDirs` in `openclaw.json`. Set `skills.load.watch: true` so iterating on SKILL.md doesn't require gateway restart. Verify with `openclaw skills list | grep antechamber`.

### 6. Acceptance test shape (per the manifest)

`project-prime/skills/antechamber-ligandprep/test_acceptance.sh`:

- Golden-path benzene from PDB 181L (the validated fixture).
- An unrelated ligand (e.g., methane from a fresh small-mol PDB).
- A malformed PDB to exercise the wrapper's error path.

Both successes plus the clean error exit are the validation gate per [[Arch_Taskboard_Manifest]] discipline.

### 7. What this stage does NOT need

- llm-task plugin — overkill until Stage 7 planner needs schema validation.
- Lobster workflow — overkill until Stage 8 recovery needs approval gates.
- Subagents — single-skill turn, no parallel work.
- Loop detection tuning — Gemini Flash doesn't loop on simple chains.
- Prompt caching tuning — sparse invocation, cache will be cold most of the time anyway.

---

## Related vault notes

- [[Phase3_Taskboard_Manifest]] — Stage 1 ✅ complete; Stage 2 design rides on this note.
- [[Dev_Log]] — chronological record; 2026-06-03 entry has the Stage 1 results.
- [[Research_El_Agente_Q]] — 2026-06-03 paper-cited assessment of the El Agente Q 22-agent DFT architecture, with banked architectural decision: Project Prime stays at max 3 named agents (`main` + future `planner` + future `recovery`), NOT a swarm. Skills absorb most of multi-agent's decomposition value at a fraction of the latency cost.
- [[Actionable_Recommendations]] §1 BUILD/INTEGRATE/ADOPT triage — the "lobster-like discipline" cited here.
- [[Arch_Taskboard_Manifest]] — the discipline this substrate enables.
- [[Skill_Antechamber_LigandPrep]] (vault sketch) — supersedes when Stage 2 lands.
- [[Skill_Bounded_Recovery_AMBER]] — Stage 8; Lobster relevance noted above.
- [[OpenClaw_Lobster_DAGs]] — 🟡 framing overstates DAG; this note's §Optional plugin tools corrects.
- [[Infra_DPDispatcher]] — local Shell+LocalContext mode; orthogonal to the substrate questions but relevant for Stage 4.
- [[openclaw-canonical-paths]] (memory) — load-bearing CLI facts for Claude session priming.
- [[openclaw-install-state]] (memory) — install + config snapshot.
- [[upstream-chemistry-skills-library]] (memory) — the reference library at `~/Downloads/Single Particle/upstream-reference/`.

---

## Source citations (primary)

All facts above derive from one of:

- Local docs: `~/.nvm/versions/node/v24.14.1/lib/node_modules/openclaw/docs/{agent-runtime-architecture.md, AGENTS.md, concepts/agent-loop.md, concepts/model-failover.md, concepts/retry.md, concepts/compaction.md, tools/exec.md, tools/exec-approvals.md, tools/skills.md, tools/creating-skills.md, tools/llm-task.md, tools/lobster.md, tools/thinking.md, tools/loop-detection.md, reference/prompt-caching.md}`.
- Bundled meta-skill: `~/.nvm/versions/node/v24.14.1/lib/node_modules/openclaw/skills/skill-creator/SKILL.md`.
- CLI surface: `openclaw <subcommand> --help` outputs.
- Empirical Day 1–3: dev log entries on 2026-06-01, 2026-06-02, 2026-06-03; substrate-verification transcripts at `project-prime/runs/substrate-verification/`.

Live docs at `docs.openclaw.ai` were not consulted in this pass; the local docs are version-pinned to 2026.5.28 and authoritative for the installed CLI. Revisit when upgrading.
