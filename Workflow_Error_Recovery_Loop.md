---
tags: [workflow, error-handling, recovery, resilience]
---
# Workflow: Autonomous Error Recovery Loop

**Core Concept:** A bounded, state-driven recovery mechanism that allows the agent to respond to intermediate execution failures without fully derailing the workflow.

**Key Features:**
* **Log Inspection:** When execution does not reach a successful state, the agent parses standard output and error logs to identify the bottleneck.
* **Bounded Recovery Actions:** Depending on the stage, the framework can autonomously apply fixes such as:
    * Parameter repair (e.g., adjusting an unstable AMBER time step).
    * Retry execution.
    * Rollback to a previous safe state.
* **Halt Conditions:** If recovery conditions are not satisfied or the failure exceeds bounded limits, execution halts and requests human guidance, preventing unbounded deviation or wasted compute resources.

**Implementation Links:**
* The process of hypothesizing fixes and verifying them aligns with the scientific verification method described in [[Arch_Recursion_LOWE]].
* Execution logs are gathered directly from the cluster via [[Infra_DPDispatcher]].