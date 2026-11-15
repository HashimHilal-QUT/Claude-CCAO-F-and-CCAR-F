# Domain 1 digest: Agentic Architecture and Orchestration (27%)

Items show a working system that now fails measurably and ask for the structural fix. Distractors fix a different problem. The exam rewards moving enforcement from prompt to code and punishes adding autonomy.

## 1.1 Agentic loops
- **Pattern:** branch on `stop_reason`. On `tool_use`, run every tool, append the assistant message, then one `tool_result` per `tool_use` id (matching id, results before any text), and continue. `end_turn` is the normal exit but only a candidate for success.
- **Truncation:** `max_tokens` means raise the limit or continue. `model_context_window_exceeded` means the window is full: compact or delegate, since raising max_tokens cannot help. Never parse either as finished.
- **Other values:** `pause_turn` (server-tool iteration limit) is a continuation, so send the content back. `refusal` is terminal: read `stop_details`, fall back or escalate, never loop.
- **Stateless API:** send the full history. Dropping the assistant `tool_use` message orphans the result, which is an API error.
- **Four guards:** turn cap, budget cap, no-progress detection (identical tool name plus arguments), and a code-evaluated acceptance check. The cap is a safety valve reporting "halted", never the primary stop.
- **SDK:** `max_turns` counts tool-use turns only. Check `ResultMessage.subtype` before reading `result`, which exists only on `success`.
- **Wrong:** parsing the model's words; breaking on the first text block (drops a pending tool call); raising the cap on a stuck loop.
- **Flip words:** "identical calls repeatedly" means no-progress detection. "Resolved without evidence" means an acceptance check. "Partial JSON" means truncation. "Stops mid-answer with a server tool" means pause_turn.

## 1.2 Coordinator and subagents
- **Topology:** a pipeline when steps and order are known; a single agent when each step depends on the last; a coordinator for independent, verbose subtasks. Test: does the next step depend on the previous result's content? A narrow agent inside one pipeline stage is often best.
- **Hub-and-spoke:** subagents never talk directly; routing through the coordinator gives observability and central error handling. The coordinator owns plan, budget and acceptance, combines results, and never re-reads what its workers read.
- **Siloed lanes:** a missing synthesis step, not a context or model problem.
- **Latency:** emit several subagent calls in one response; time equals the slowest branch. One call per turn is the "3x slower" anti-pattern.
- **Bounds:** `Agent` must be in `allowedTools` or delegation is denied. `maxBudgetUsd` covers the whole tree. Spawn depth defaults to 3; set it to 1 so workers cannot spawn workers. A capped run (`error_max_budget_usd`) is incomplete: report coverage, never "complete".

## 1.3 Invocation and context passing
- **Fresh context.** Crosses: the subagent's own prompt, the delegation string, project CLAUDE.md, tool definitions. Does not cross: parent history, tool results, parent system prompt.
- **Delegation is a work order:** paths, error text, repro, locked decisions, scope, return shape. Needing "as we discussed" means do not delegate.
- **Symptoms of missing context:** re-derived work, "can't find" files, context-unaware output. The fix is explicit injection, not more turns or a bigger model.
- **`description` is a routing rule,** not documentation. Patching the coordinator prompt is wrong.
- **Findings as structured objects,** never prose: content plus metadata (source_url, retrieved_at, confidence) and claim-to-source IDs the synthesis schema preserves. Prose drops attribution.
- **Conflicts:** record both claims, mark unresolved, escalate. Never pick silently.
- **Look-alikes:** `tools` restricts, `allowedTools` permits, skill `allowed-tools` pre-approves only, `readOnlyHint` is never authorization.

## 1.4 Enforcement and handoff
- **Prompt is a request, code a guarantee.** Ladder: withhold the tool, then `PreToolUse` deny, then a validated handoff record.
- **Prerequisite gate:** PreToolUse tracks session state and blocks tool B until tool A succeeds, with a `permissionDecisionReason` so the model escalates. Stronger prompts and few-shot examples are not guarantees.
- **Compaction** drops opening-prompt rules. CLAUDE.md, re-injected every request, gives persistence, not enforcement.
- **Handoff record:** run_id, completed and next_expected stage, gate with observed values and `evaluated_by: "code"`, artifact addresses plus checksum, `decisions_locked`, budget. The next stage refuses on mismatch.
- **Human handoff:** customer_id, issue, root cause, attempts, escalation reason, amount, next action. No transcript needed.

## 1.5 Hooks
- Run in your process, cost no tokens, cannot be argued with.
- **PreToolUse** runs before execution: block, or rewrite via `updatedInput` with `allow` or `ask`.
- **PostToolUse** runs before the model sees results: normalize (epochs, codes, cents, business meaning) and trim with `updatedToolOutput`, keeping a raw-output path.
- **Precedence:** deny, defer, ask, allow. Order does not matter.
- **Async hooks** cannot block or modify, so use them only for logging.
- **Wrong:** PostToolUse to prevent an action; decode tables in the prompt; async normalization.

## 1.6 Decomposition
- **Steps known upfront?** Yes: prompt chaining (reproducible, auditable). No: dynamic decomposition (investigations, migrations).
- **Split on** context volume, permission asymmetry, independent verification; keep whole when re-briefing costs as much as isolation saves.
- **Split by question, not territory;** never split refinement loops (cost up, quality flat); prefer wide over deep.

## 1.7 Sessions
- **Sessions persist conversation, not files;** resume restores beliefs.
- **Resume** when context is valid; state which files changed.
- **Fork** to compare alternatives from a costly baseline (new id, original untouched). Forks share files, so two forks on one checkout collide. Never fork for file updates.
- **Fresh start plus summary** when results are stale; frame findings as hypotheses.
- **Crash recovery:** not resume (session files are machine-local). Use a state record: status before and after each unit, bounded attempts, locked decisions, addresses, atomic writes.
