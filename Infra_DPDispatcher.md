---
tags: [infrastructure, hpc, dpdispatcher, slurm, execution]
---
# Infrastructure: DPDispatcher Execution Grounding

> **Vault tier: ✅ Paper-cited + docs-verified** — arXiv:2603.25522 confirms Slurm/PBS/LSF/Bohrium translation + full poke/monitor/download lifecycle. Local-shell mode (`batch_type: "Shell"` + `LocalContext`) verified against DPDispatcher official docs 2026-05-19. The local-only plan is unblocked.

**Core Concept:** The bridge between the OpenClaw agent's reasoning and the heterogeneous High-Performance Computing (HPC) environments (e.g., Slurm, PBS, LSF).

**Key Features:**
* **Scheduler Adaptation:** Translates agent intent into valid job descriptors, handling machine settings, resource requests, and file-transfer specifications.
* **Unified State Tracking:** Treats queueing, waiting, monitoring, and result collection as normal workflow states within the OpenClaw control loop, rather than relying on ad-hoc shell scripts.
* **Cross-Backend Grounding:** Shields the core agent from having to memorize specific scheduler syntax, allowing the same logic to target local shell execution or remote supercomputers interchangeably.

**Implementation Links:**
* If DPDispatcher detects a failed job state on the cluster, it triggers the recovery protocols outlined in [[Workflow_Error_Recovery_Loop]].

## Source — verified breakdown (2026-05-19 via NotebookLM, arXiv:2603.25522)

- **Paper-confirmed:** DPDispatcher generates HPC scheduler job input scripts for **Slurm / PBS / LSF / Bohrium**, submits them, and **monitors ("pokes") until jobs finish, then downloads result files** — full lifecycle ownership, not just submission. Quote: *"DPDispatcher is a Python package used to generate HPC...scheduler systems (Slurm/PBS/LSF/Bohrium) jobs input scripts, submit them...and poke until they finish."*
- **Paper-confirmed positive find:** the *poke + download* lifecycle is paper-attested — add to the report as DPDispatcher's distinctive value vs. ad-hoc shell scripts.
- **Verified separately (2026-05-19 via DPDispatcher official docs):** **Local-shell execution mode exists and is well-supported.** Configuration: `batch_type: "Shell"` + `context_type: "local"` (`LocalContext`), with `queue_name` typically empty. `LocalContext` runs in the local server in a separate working directory, symlinking input files in and copying outputs back. Supported context types include `LocalContext`, `LazyLocalContext`, `OpenAPIContext`, `HDFSContext`, `SSHContext`. *Source:* DPDispatcher docs ([machine](https://docs.deepmodeling.com/projects/dpdispatcher/en/latest/machine.html), [context](https://docs.deepmodeling.com/projects/dpdispatcher/en/latest/context.html), [getting-started](https://github.com/deepmodeling/dpdispatcher/blob/master/doc/getting-started.md)). The local-only plan is unblocked — proceed.

> **Local-only deployment note (2026-05-14, verified 2026-05-19):** Project Prime runs everything locally — no remote Slurm/PBS/LSF cluster. Day-1 config: `batch_type: "Shell"` + `LocalContext`. The cross-backend grounding DPDispatcher offers (Slurm/PBS/LSF/Bohrium/SSH) is forward-looking insurance if the project ever moves off the Mac, not day-1 scope.