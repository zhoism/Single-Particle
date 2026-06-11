# Example: substantial entry (multi-deliverable session)

From Dev_Log.md, 2026-06-03 — Stage 1 substrate verification. ~50 lines. Multi-hour session with deliverables in 3 directions.

```markdown
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
```

## What makes this a good substantial entry

- **Headline carries the headline result + the *secondary* outcome.** "3/3 PASS, two real design signals for Stage 2." Reader knows the immediate verdict AND why this matters downstream.
- **Each probe gets its own bolded sub-headline** (`1a`, `1b`, `1c`) with the verdict up front, then the details.
- **Numbered findings + numbered design signals.** Easy to reference in future entries ("the 311s signal from 2026-06-03").
- **Operational gotchas captured inline** with the diagnostic command (`openclaw models status | grep cooldown`) — future-you can act on them without re-deriving.
- **Artifacts section lists where things live**, doesn't repeat what they contain.
- **Manifest line** flips the stage status — explicit state transition.
- **Stage 0 cleanup mentioned** but flagged "deferred, non-blocking" — open items don't get lost.
- **Next:** is two sentences — what's the next action + what carry-forward design signal still applies.

## Anti-patterns this avoids

- Doesn't paste the full transcript of any of the 3 probes.
- Doesn't speculate about what Stage 2 design will look like in detail — that's Stage 2's entry's job.
- Doesn't conflate the design-signal findings (forward-looking) with the substrate findings (backward-looking) — separates them.
