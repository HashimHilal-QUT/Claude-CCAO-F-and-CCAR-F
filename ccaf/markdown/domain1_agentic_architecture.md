# Domain 1: Agentic Architecture & Orchestration

> Claude Certified Architect – Foundations

> Exam Weight: 27% | Questions in Pool: 61

*Generated from the JSONL bank by `scripts/render_markdown.py` — do not edit by hand.*
*Private study material, assembled from mixed sources: not licensed for redistribution.*

---

**Q1.** Production data shows that in 12% of cases, your agent skips `get_customer` entirely and calls `lookup_order` using only the customer's stated name, occasionally leading to misidentified accounts and incorrect refunds. What change would most effectively address this reliability issue?

- **A)** Add a programmatic prerequisite that blocks `lookup_order` and `process_refund` calls until `get_customer` has returned a verified customer ID.
- **B)** Enhance the system prompt to state that customer verification via `get_customer` is mandatory before any order operations.
- **C)** Add few-shot examples showing the agent always calling `get_customer` first, even when customers volunteer order details.
- **D)** Implement a routing classifier that analyzes each request and enables only the subset of tools appropriate for that request type.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

When a specific tool sequence is required for critical business logic, programmatic enforcement provides deterministic guarantees that prompt-based approaches cannot. Options B and C rely on probabilistic LLM compliance. Option D addresses tool availability rather than tool ordering.

</details>

---

**Q7.** After running on "impact of AI on creative industries," each subagent completes successfully but the final reports cover only visual arts, missing music, writing, and film production. The coordinator decomposed the topic into: "AI in digital art creation," "AI in graphic design," and "AI in photography." What is the most likely root cause?

- **A)** The synthesis agent lacks instructions for identifying coverage gaps in the findings it receives from other agents.
- **B)** The document analysis agent is filtering out sources related to non-visual creative industries due to overly restrictive relevance criteria.
- **C)** The web search agent's queries are not comprehensive enough and need to be expanded to cover more creative industry sectors.
- **D)** The coordinator agent's task decomposition is too narrow, resulting in subagent assignments that don't cover all relevant domains.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

The coordinator's logs reveal the root cause directly: it decomposed "creative industries" into only visual arts subtasks. The subagents executed their assigned tasks correctly. The problem is what they were assigned.

</details>

---

**Q8.** The web search subagent times out while researching a complex topic. You need to design how this failure information flows back to the coordinator agent. Which error propagation approach best enables intelligent recovery?

- **A)** Return structured error context to the coordinator including the failure type, the attempted query, any partial results, and potential alternative approaches.
- **B)** Implement automatic retry logic with exponential backoff within the subagent, returning a generic "search unavailable" status only after all retries are exhausted.
- **C)** Catch the timeout within the subagent and return an empty result set marked as successful.
- **D)** Propagate the timeout exception directly to a top-level handler that terminates the entire research workflow.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Structured error context gives the coordinator the information it needs to make intelligent recovery decisions. Option B's generic status hides valuable context. Option C suppresses the error, preventing any recovery. Option D terminates the entire workflow unnecessarily.

</details>

---

**Q9.** The synthesis agent frequently needs to verify specific claims while combining findings. Currently, this creates 2-3 round trips per task, increasing latency by 40%. 85% of verifications are simple fact-checks; 15% require deeper investigation. What's the most effective approach to reduce overhead while maintaining reliability?

- **A)** Give the synthesis agent a scoped `verify_fact` tool for simple lookups, while complex verifications continue delegating to the web search agent through the coordinator.
- **B)** Have the synthesis agent accumulate all verification needs and return them as a batch to the coordinator at the end of its pass.
- **C)** Give the synthesis agent access to all web search tools so it can handle any verification need directly without round-trips.
- **D)** Have the web search agent proactively cache extra context around each source during initial research, anticipating what the synthesis agent might need to verify.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Option A applies the principle of least privilege by giving the synthesis agent only what it needs for the 85% common case while preserving the existing coordination pattern for complex cases. Option B creates blocking dependencies. Option C over-provisions the synthesis agent. Option D relies on speculative caching.

</details>

---

**Q13.** You are building a customer support agent using the Claude Agent SDK. The agent processes billing disputes by calling tools like `lookup_order`, `get_invoice`, and `process_refund`. A code review notes that after each tool call, your loop checks whether Claude's response text contains the phrase "I have completed" to decide whether to stop.

What is the primary problem with this loop termination approach?

- **A)** The agent will never terminate because `process_refund` always returns a success message that prevents "I have completed" from appearing.
- **B)** Relying on natural language signals in the assistant's text is unreliable; the correct approach is to inspect `stop_reason` and only terminate when it equals `"end_turn"`.
- **C)** The loop should terminate as soon as any tool call fails, since continuing after a failure will corrupt the conversation history.
- **D)** Checking response text is only valid in synchronous mode; you must use a callback handler for proper loop control in async contexts.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Inspecting `stop_reason` is the canonical method for agentic loop control: continue iterating when `stop_reason` is `"tool_use"`, stop when it is `"end_turn"`. Natural language phrases like "I have completed" are not reliable termination signals because Claude's phrasing varies across responses and prompt updates. Options A and C are based on incorrect assumptions about how tools interact with response text. Option D conflates asynchronous execution patterns with loop control logic.

</details>

---

**Q14.** A developer productivity agent investigates bug reports by calling `search_codebase`, `read_file`, and `run_tests`. During a code review, a colleague proposes adding an iteration cap: if the loop has not finished after 15 tool calls, terminate with a generic "investigation incomplete" response.

What is the correct characterization of this design?

- **A)** Iteration caps are the recommended primary stopping mechanism because they prevent runaway costs in production.
- **B)** Iteration caps are a reasonable safety boundary for long-running tasks but should not be the primary termination mechanism; `stop_reason: "end_turn"` remains the authoritative signal.
- **C)** The iteration cap should be replaced with a time-based timeout, since token counts are a more reliable measure of completion than iteration count.
- **D)** Iteration caps are unnecessary if the system prompt instructs the agent to always request only the minimum tools needed.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

The agentic loop should terminate primarily when `stop_reason` equals `"end_turn"`, which signals that the model has finished its task. An iteration cap can serve as a safety guardrail against runaway loops, but treating it as the primary stopping mechanism means the loop may cut off legitimate multi-step investigations. Options A and C misstate recommended practice. Option D conflates prompt-based guidance with loop control: even a well-prompted agent may legitimately need many tool calls for complex investigations.

</details>

---

**Q15.** Your multi-agent research system's agentic loop appends each tool result to the conversation history before sending the next request. A teammate suggests instead storing all tool results in a separate database and providing only a summary to the model at each iteration, rather than the full result.

Under what condition would this change most likely degrade agent performance?

- **A)** When the tool results contain binary data such as images or file attachments.
- **B)** When tools return results faster than 200ms, making history appending redundant.
- **C)** When the number of tool calls per session exceeds 10, since larger histories slow down the API.
- **D)** When the model needs to reason across multiple tool results simultaneously to determine its next action, since summaries may omit details required for that reasoning.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

The agentic loop depends on tool results being present in conversation history so the model can reason about what it has already discovered before deciding its next action. Summaries may omit field values, error codes, or conditional data the model needs to make correct decisions. Option A is a valid concern but not the primary performance risk for text-based research tasks. Options C and B are not recognized failure modes for this architecture.

</details>

---

**Q16.** Your multi-agent research system uses a coordinator that always routes every query through all four subagents (web search, document analysis, synthesis, and report generation) regardless of query complexity. For a simple factual question like "What year was the Anthropic API released?", the system takes 45 seconds and incurs unnecessary cost.

What design change most directly addresses this?

- **A)** Replace the coordinator with a static routing table that maps query keywords to specific subagent pipelines.
- **B)** Have each subagent evaluate its own relevance to the current query and self-select into or out of the pipeline.
- **C)** Design the coordinator to dynamically select which subagents to invoke based on query complexity and type, rather than always routing through the full pipeline.
- **D)** Reduce the number of subagents from four to two by merging web search and document analysis into a single "retrieval" agent.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

A coordinator that always runs the full pipeline regardless of query complexity wastes resources and adds latency for simple requests. The correct design is a coordinator that evaluates the query and selects only the subagents needed for that specific task. Option A replaces adaptive intelligence with a brittle keyword table. Option B distributes coordination logic across subagents, breaking the hub-and-spoke pattern and reducing observability. Option D reduces capability unnecessarily instead of improving routing logic.

</details>

---

**Q17.** A coordinator agent in your research system has delegated document analysis to a subagent. After the subagent finishes, the coordinator notices the findings are incomplete: the subagent covered only three of the five specified sources. The coordinator needs to get the remaining two sources analyzed.

What is the correct approach for re-delegating this work?

- **A)** Invoke the synthesis agent with the partial findings and instruct it to infer what the missing sources likely contain based on patterns from the three completed analyses.
- **B)** The coordinator should re-invoke the document analysis subagent with an explicit prompt specifying only the two missing sources, including the previously completed findings as context.
- **C)** Send all five sources again to a new document analysis subagent instance, which will re-analyze the three already-completed sources along with the two missing ones.
- **D)** Let the coordinator generate its own analysis of the remaining two sources directly, rather than spawning another subagent delegation.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

The coordinator's role includes evaluating output for gaps and re-delegating targeted work to close those gaps. Re-invoking the subagent with only the unfinished sources and providing the completed findings as context is efficient and correct. Option A asks synthesis to fabricate content, which undermines report accuracy. Option C wastes resources by re-processing already-completed sources. Option D bypasses the coordinator-subagent architecture and ignores the subagent's specialization.

</details>

---

**Q18.** You are building a coordinator that delegates research tasks to subagents using the `Task` tool. When you test the system, the coordinator cannot invoke any subagents. Reviewing the coordinator's `AgentDefinition`, you notice the `allowedTools` field is set to `["web_search", "read_document"]`.

What is the most likely cause of the failure?

- **A)** The `Task` tool requires an explicit `subagent_endpoint` configuration before it can be invoked.
- **B)** The coordinator's system prompt does not include instructions to use the `Task` tool, so the model never attempts to call it.
- **C)** `"Task"` is not included in the coordinator's `allowedTools`, so it cannot spawn subagents.
- **D)** Subagent invocation requires the coordinator to be running in plan mode rather than direct execution mode.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

The `Task` tool is the mechanism for spawning subagents in the Claude Agent SDK. For a coordinator to invoke subagents, `"Task"` must be explicitly included in its `allowedTools`. Simply having other tools available does not grant subagent spawning capability. Option A describes a configuration parameter that does not exist. Option B conflates prompt instructions with capability gating: even a well-prompted coordinator cannot call a tool that is not in its allowed set. Option D conflates plan mode with subagent spawning.

</details>

---

**Q19.** Your multi-agent research system has a web search subagent that consistently returns findings without identifying which sources correspond to which claims. When the synthesis agent receives these findings, it cannot produce properly cited reports.

What is the correct fix during context passing from the web search subagent to the synthesis agent?

- **A)** Instruct the synthesis agent to run its own web searches to re-locate the original sources.
- **B)** Use structured data formats that separate claim content from metadata (source URLs, publication dates, page numbers) in the subagent's output, and include this structure when passing context to the synthesis agent.
- **C)** Have the coordinator concatenate all subagent outputs into a single text block before forwarding to synthesis, since synthesis will extract citations naturally.
- **D)** Configure the web search subagent to return only source URLs, and have the synthesis agent re-read each source to reconstruct the findings.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Structured data formats that separate content from metadata ensure that claim-source mappings survive the handoff between agents. When context is passed as unstructured text, citation information is easily lost. Option A introduces redundant work and potentially different search results. Option C risks losing the claim-source associations during concatenation. Option D is extremely inefficient and requires the synthesis agent to redo retrieval work.

</details>

---

**Q20.** A coordinator needs to research three independent subtopics in parallel: market trends, competitor analysis, and regulatory environment. Each requires a separate web search subagent. How should the coordinator spawn these subagents to maximize throughput?

- **A)** Spawn the subtopics sequentially: start the first subagent, wait for its result, then start the second, and so on, to avoid context conflicts.
- **B)** Emit all three `Task` tool calls in a single coordinator response, which allows the subagents to run in parallel.
- **C)** Route all three subtopics through a single subagent sequentially, sharing context between them to reduce total memory usage.
- **D)** Use a single subagent with three separate prompts in sequence, passing prior results as context for each subsequent prompt.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

The Claude Agent SDK supports parallel subagent execution by emitting multiple `Task` tool calls in a single coordinator response. This maximizes throughput for independent subtopics that do not depend on each other's results. Option A introduces unnecessary serial latency. Option C assumes a dependency that the question does not establish. Option D collapses three specialists into one sequential process, eliminating parallelism.

</details>

---

**Q21.** Your customer support agent handles account closure requests. The workflow requires: (1) verify customer identity via `get_customer`, (2) check for active subscriptions via `check_subscriptions`, (3) process closure via `close_account`. Production logs show the agent occasionally calls `close_account` before completing the identity verification step, resulting in unauthorized account closures.

A colleague suggests adding a system prompt instruction: "Always verify identity before closing accounts." What is the most effective approach?

- **A)** The system prompt instruction is sufficient because it explicitly describes the required order.
- **B)** Add few-shot examples showing the correct three-step sequence alongside the system prompt instruction.
- **C)** Implement a programmatic prerequisite that blocks `close_account` from executing until `get_customer` has returned a verified customer ID.
- **D)** Add a routing classifier that analyzes the request type and pre-selects the appropriate tools before the agent begins.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

When a tool ordering requirement has serious consequences (unauthorized account closures), programmatic enforcement provides deterministic guarantees. Prompt instructions have a non-zero failure rate even when explicit. Option A relies on probabilistic compliance, which the logs already show is insufficient. Option B improves the odds but still does not guarantee compliance. Option D addresses tool selection rather than ordering enforcement.

</details>

---

**Q22.** A customer contacts your support agent about three issues in a single message: a billing charge dispute, a missing order, and a request to update their email address. The agent processes these sequentially, taking 3-4 minutes per request. A senior architect suggests you redesign the handling approach.

What design change would most improve efficiency while maintaining accuracy?

- **A)** Instruct the agent to address only the highest-priority issue per conversation turn and ask the customer to submit separate tickets for the remaining issues.
- **B)** Decompose the three concerns into distinct investigation items and process each in parallel using shared customer context, then compile a unified response.
- **C)** Process the three issues sequentially but cache intermediate results so subsequent issues benefit from data already retrieved.
- **D)** Delegate all three issues to a single specialized "multi-issue" subagent that handles complex requests with multiple concerns.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

When a customer presents multiple independent concerns, decomposing them into parallel investigation items dramatically reduces latency. Each concern can be investigated simultaneously using the shared customer context already retrieved. Option A creates a poor customer experience and extra work for the customer. Option C improves caching but does not eliminate the serial bottleneck. Option D creates an undifferentiated subagent that doesn't reflect the coordinator-subagent specialization pattern.

</details>

---

**Q23.** Your customer support agent integrates with three backend MCP tools: a legacy billing system returning Unix timestamps, an order management system returning ISO 8601 dates, and a subscription service returning numeric status codes (1=active, 2=paused, 3=cancelled). The agent frequently misinterprets these heterogeneous formats when reasoning about customer records.

What is the most appropriate architectural fix?

- **A)** Update each backend system to return a uniform date and status format before the agent calls them.
- **B)** Add format conversion instructions to the system prompt explaining how to interpret each tool's output conventions.
- **C)** Implement `PostToolUse` hooks that intercept tool results from each source and normalize timestamps, dates, and status codes into a consistent format before the model processes them.
- **D)** Add a post-processing step after the agent produces its final response to re-format any dates and statuses that appear in the output.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

`PostToolUse` hooks are the correct mechanism for intercepting and transforming tool results before the model processes them. This ensures the model always sees normalized data regardless of backend heterogeneity. Option A requires backend changes that may not be feasible and introduces coupling. Option B relies on probabilistic compliance and adds token overhead. Option D applies normalization after the model has already reasoned on inconsistent data, which cannot repair any incorrect conclusions already made.

</details>

---

**Q24.** Your customer support agent has a policy: refunds above $500 require manager approval and must not be processed autonomously. Your system prompt states "Do not process refunds above $500 without manager approval." Production logs show this rule is violated in approximately 3% of cases.

What is the most effective way to guarantee compliance?

- **A)** Strengthen the system prompt language: "You are strictly forbidden from processing refunds above $500 without explicit manager approval under any circumstances."
- **B)** Add 10 few-shot examples in the system prompt, all demonstrating the agent requesting manager approval for high-value refunds.
- **C)** Implement a hook that intercepts outgoing `process_refund` tool calls, checks the refund amount, and blocks execution or redirects to the manager approval workflow when the amount exceeds $500.
- **D)** Implement a validation step that runs after `process_refund` completes and reverses any refunds that exceeded the threshold.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Business rules that require guaranteed compliance must be enforced programmatically, not through prompt instructions alone. A hook that intercepts `process_refund` calls before execution provides deterministic enforcement regardless of how the model interprets the system prompt. Options A and B both improve adherence probabilistically but cannot guarantee zero violations. Option D runs after the action has already been taken, which means the policy violation has already occurred.

</details>

---

**Q25.** A developer productivity agent has a `PostToolUse` hook that transforms raw Bash output. Currently the hook appends a formatted summary but also preserves the full raw output in the result passed to the model. Sessions exploring large codebases are hitting context limits faster than expected.

What change would most effectively reduce unnecessary context consumption from tool results?

- **A)** Disable the `PostToolUse` hook entirely and let the model process raw Bash output directly.
- **B)** Switch from `PostToolUse` hooks to pre-processing the Bash commands themselves to produce shorter output.
- **C)** Increase the model's `max_tokens` parameter to accommodate the additional context from both raw and formatted output.
- **D)** Modify the hook to return only the formatted summary to the model, trimming the verbose raw output rather than preserving it alongside the summary.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

`PostToolUse` hooks can trim verbose tool outputs to only the relevant data before the model processes them. Keeping both raw and summary output doubles the context consumption from each tool call. Modifying the hook to return only the formatted summary addresses the root cause directly. Option A removes normalization benefits. Option C increases output capacity but does not address the growing input context. Option B would require significant changes to tool invocation patterns and may not be feasible for all commands.

</details>

---

**Q26.** You are building an automated code review system using Claude. The review must cover three aspects for every pull request: security vulnerabilities, style compliance, and performance implications. Each aspect has clear, defined criteria documented in your engineering handbook.

Which decomposition strategy is most appropriate?

- **A)** Dynamic adaptive decomposition: have the agent start by scanning the full PR and generate a review plan based on what it finds.
- **B)** Prompt chaining with sequential focused passes: one pass per review aspect (security, style, performance), each with dedicated criteria.
- **C)** A single comprehensive pass that examines all three aspects simultaneously to capture cross-cutting concerns.
- **D)** Spawn three fully independent agents without shared context, then merge their outputs in a final aggregation step.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

When a workflow has predictable, well-defined aspects that must each be covered, prompt chaining with sequential focused passes is the appropriate pattern. Each pass dedicates full attention to one concern rather than dividing attention across all three. Option A uses dynamic decomposition for a workflow whose structure is already known, adding unnecessary overhead. Option C suffers from the attention dilution problem that prompt chaining is designed to solve. Option D loses cross-file integration context by fully isolating the three agents.

</details>

---

**Q27.** An engineering team asks you to design a Claude-based system to investigate a production incident. The system must root-cause a bug that was introduced somewhere in the past two weeks across an unknown set of files and services. The scope of the investigation cannot be known in advance.

Which decomposition approach is most appropriate?

- **A)** Prompt chaining: design a fixed sequence of investigation steps (check logs, read configs, trace service calls) that the agent executes in order.
- **B)** Dynamic adaptive decomposition: the agent first maps the affected services and symptom timeline, then generates and prioritizes investigation subtasks based on what is discovered at each step.
- **C)** Split the investigation between two agents: one agent reads logs while the other reads source code, and they report findings independently to a human operator.
- **D)** Have the agent run a comprehensive search of all changed files in the past two weeks and produce a ranked list of candidates for manual review.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Open-ended investigation tasks with unknown scope require dynamic adaptive decomposition, where the agent builds its investigation plan based on intermediate findings rather than following a fixed sequence. A static prompt chain cannot adapt when the investigation reveals unexpected service dependencies or anomalous patterns. Option A is appropriate for predictable multi-aspect reviews, not exploratory investigations. Option C removes the coordinating intelligence and requires human intervention for synthesis. Option D is a single-pass heuristic that does not apply the model's reasoning capability.

</details>

---

**Q28.** A developer has been using Claude Code to investigate a legacy authentication service. After several hours, they have built up a detailed session with findings about the service's token validation logic. They need to step away and return tomorrow. Three core files in the authentication module will be modified overnight by another team.

What is the most reliable approach for resuming the investigation productively the next day?

- **A)** Resume the named session with `--resume <session-name>` and notify the agent about the specific files that were changed, so it can re-analyze those files in the context of its prior understanding.
- **B)** Start a completely new session each time, since stale tool results from the previous session make resumption unreliable for any scenario.
- **C)** Resume the named session without any notification about file changes; the agent will detect modifications automatically when it next reads those files.
- **D)** Use `fork_session` to create a branch of the current session before stepping away, then resume from the fork the next day.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

When resuming a session after code modifications, the correct approach is to use `--resume <session-name>` to continue the named session and explicitly inform the agent about which files changed so it can target re-analysis appropriately. Option B is overly conservative: starting fresh is appropriate when prior tool results are broadly stale, but when only a few known files changed, resumption with targeted context about those changes is more efficient. Option C is incorrect because the agent does not automatically detect file changes on resume. Option D misuses `fork_session`, which is designed for exploring divergent approaches from a shared baseline, not for session continuity across time gaps.

</details>

---

**Q29.** You are leading a research investigation using Claude Code. You have completed an initial analysis of a competitor's public API documentation and want to explore two divergent architectural approaches for your response strategy: one focused on feature parity, one focused on differentiation. You want both explorations to start from the same analysis baseline.

Which session management approach best fits this scenario?

- **A)** Run two separate new sessions, each with a copy of the analysis findings injected as context in the initial prompt.
- **B)** Use `--resume` to resume the current session twice in parallel, once for each exploration direction.
- **C)** Use `fork_session` to create two independent branches from the current session, then explore each approach in its respective branch.
- **D)** Continue in the same session, exploring one approach, then using `/compact` to clear context before exploring the second approach.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

`fork_session` is designed precisely for this scenario: creating independent branches from a shared analysis baseline to explore divergent approaches. Each branch inherits the common findings and can be explored independently without contaminating the other. Option A requires duplicating context and does not preserve the live session state. Option B describes a mechanism that does not work this way: `--resume` continues a single session sequentially, not in parallel branches. Option D uses `/compact` destructively, losing the baseline context needed for the second exploration.

</details>

---

**Q78.** Your support agent loop calls `messages.create`, checks `response.stop_reason`, executes any tools, and sends back `tool_result` blocks. In production, the loop occasionally exits after Claude calls `lookup_order` but before calling `process_refund` or replying to the customer. Logs show `stop_reason: "end_turn"` on those turns. What is the most likely root cause?

- **A)** The agent hit its `max_tokens` limit while composing the refund reasoning and silently truncated.
- **B)** A `PostToolUse` hook is rewriting the tool result and blocking the next turn.
- **C)** The agent loop is terminating correctly — `end_turn` means Claude produced a final natural-language answer for the user, so the model decided no further tool call was needed for that case.
- **D)** `stop_reason: "end_turn"` indicates a server-side timeout and the request should be retried.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** `end_turn` is the normal stop reason meaning Claude reached a natural stopping point and is not requesting another tool call. If the agent answered the customer instead of processing the refund, the model chose that path — the loop is behaving correctly; the prompt or tool description, not the loop, is the issue.

**Why A is Wrong:** `max_tokens` produces `stop_reason: "max_tokens"`, not `end_turn`; the two are distinct values and the logs show `end_turn`.
**Why B is Wrong:** `PostToolUse` runs after tool execution and cannot change `stop_reason`; it can only append `additionalContext` to conversation state.
**Why D is Wrong:** `end_turn` is a normal completion signal, not a timeout; Anthropic has no "retry end_turn" semantic.

**Pattern/Trap:** P10 Root Cause vs Symptom

</details>

---

**Q79.** Your research coordinator spawns three subagents via the Task/Agent tool for a market-analysis query. The coordinator has already gathered a list of 12 target companies and stored them in its conversation. Subagent 1 returns findings about only 3 of those companies; when asked why, its logs show it only "knew about" companies it inferred from the short task prompt. What is the correct fix?

- **A)** Serialize the full 12-company list into the `prompt` string passed to the Agent tool call, since subagents do not inherit the coordinator's conversation history.
- **B)** Switch the subagent to Opus so it has a larger effective context window.
- **C)** Increase the subagent's `maxTurns` so it can iterate longer and discover the remaining companies.
- **D)** Add a `PostToolUse` hook on the Agent tool that attaches the coordinator's transcript to the subagent input.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Per Anthropic's subagent docs, the only channel from parent to subagent is the Agent tool's `prompt` string. The subagent's context window starts fresh with no parent conversation; any data it needs (company list, file paths, prior decisions) must be explicitly included in that prompt.

**Why B is Wrong:** Context window size is irrelevant when the parent history was never passed; a larger window stays empty.
**Why C is Wrong:** More turns cannot reveal information the subagent never received; the constraint is missing input, not insufficient iteration.
**Why D is Wrong:** `PostToolUse` fires after the tool (subagent) has already executed and cannot inject data into the subagent's starting prompt.

**Pattern/Trap:** P6 Context Inheritance Misconception

</details>

---

**Q80.** Policy requires that `process_refund` never run for amounts above $500 without a manager-approval token. Currently the system prompt says "Never refund more than $500 without approval." A quarterly audit found 14 refunds of $500–$4,000 approved without tokens. Which change most reliably closes the gap?

- **A)** Strengthen the system prompt with bold, capitalized warnings and add three few-shot examples of correct refusals.
- **B)** Lower the agent's temperature to 0 to make refund decisions more deterministic.
- **C)** Have a second Claude instance review every refund decision before it executes and veto if it disagrees.
- **D)** Add a `PreToolUse` hook on `process_refund` that inspects `input.amount` and returns `permissionDecision: "deny"` when `amount > 500 && !input.approval_token`.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Hard financial thresholds belong in programmatic gates, not prompts. A `PreToolUse` hook can deterministically deny tool calls (precedence: deny > ask > allow) based on structured input fields before the tool ever executes, making the policy enforceable rather than persuasive.

**Why A is Wrong:** LLMs probabilistically violate prompt rules; strengthening prose cannot guarantee enforcement of a monetary policy.
**Why B is Wrong:** Lower temperature biases toward likely tokens but does not enforce any specific rule; the model can still emit a $2,000 refund tool call confidently.
**Why C is Wrong:** A reviewer LLM introduces its own error rate, doubles cost, and still relies on probabilistic judgment — the audit problem persists, only shifted.

**Pattern/Trap:** P1 Prompt vs Programmatic Enforcement

</details>

---

**Q81.** An extraction pipeline processes PDFs and calls `messages.create` with `tool_use` forced via `tool_choice`. Roughly 3% of requests return `stop_reason: "max_tokens"` mid-way through a `tool_use` block, producing invalid JSON and downstream parse errors. Which response is correct?

- **A)** Treat `max_tokens` as equivalent to `end_turn` and parse whatever JSON was produced.
- **B)** Add a `PostToolUse` hook that repairs truncated JSON before it reaches the parser.
- **C)** Delete the partial tool_use block from the assistant turn and retry with the same parameters.
- **D)** Catch the error, re-issue the request with a higher `max_tokens`, and if the partial tool_use is still present, continue the conversation with a `tool_result` marked `is_error: true`.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** `max_tokens` means output was truncated; the partial `tool_use` is invalid and cannot be executed. The correct handling is to raise `max_tokens` (or tighten the schema) and, if a malformed tool_use remains, satisfy the API requirement that every `tool_use` needs a matching `tool_result` — marked as an error — so the conversation stays valid.

**Why A is Wrong:** `max_tokens` and `end_turn` are semantically different; treating them the same produces malformed outputs and silent data corruption.
**Why C is Wrong:** If you retain the assistant turn with a `tool_use` block but do not follow it with a `tool_result`, the API rejects the next request with `invalid_request_error`.
**Why B is Wrong:** `PostToolUse` fires after a tool executes; it cannot intercept an LLM output block that was truncated before a tool ever ran.

**Pattern/Trap:** P10 Root Cause vs Symptom

</details>

---

**Q82.** Your research coordinator decomposes queries into 3–10 parallel subagents. For a new query class ("summarize regulatory changes across 5 named jurisdictions"), a colleague proposes hard-coding the five subagent invocations in a script. Which decomposition strategy best fits?

- **A)** Dynamic orchestrator-worker decomposition so the coordinator decides at runtime how many subagents to spawn.
- **B)** Static prompt chaining (hard-coded sequence) because the five jurisdictions are known in advance and the subtasks are predictable.
- **C)** A single agent with a 200K context window that reads all jurisdictions sequentially.
- **D)** Evaluator-optimizer loop where one agent proposes summaries and another critiques until convergence.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** Anthropic's "Building effective agents" distinguishes static patterns (prompt chaining, parallelization) from dynamic orchestration. When subtasks are fixed and known in advance — five named jurisdictions — parallel prompt chaining is simpler, cheaper, and more predictable than dynamic orchestration.

**Why A is Wrong:** Dynamic decomposition is appropriate when subtasks cannot be predicted; here they can, so the extra orchestration overhead adds cost without benefit.
**Why C is Wrong:** Single-agent sequential reading foregoes parallelism for 5 independent jurisdictions and increases latency ~5x for no accuracy gain.
**Why D is Wrong:** Evaluator-optimizer addresses quality iteration on a single artifact, not breadth decomposition across independent jurisdictions.

**Pattern/Trap:** P3 Over-Engineering Distractor

</details>

---

**Q83.** A team shares a repo that defines two subagents via `.claude/agents/reviewer.md` and `.claude/agents/test-writer.md`. A developer committed `~/.claude/agents/reviewer.md` with different instructions on their laptop and wonders why teammates see different behavior. Which statement is correct?

- **A)** `~/.claude/agents/` is user-level and never shared via git; teammates only see `.claude/agents/` in the repo.
- **B)** User-level agents in `~/.claude/agents/` are automatically synced when the repo is cloned.
- **C)** `.claude/agents/` is gitignored by default; agents must be placed at `~/.claude/agents/` to be shared.
- **D)** Both locations are merged and the union is shared with teammates via Claude's cloud sync.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Anthropic's settings hierarchy places `.claude/agents/` at the project level (checked into version control, shared with the team) and `~/.claude/agents/` at the user level (personal, per-machine, not shared). The developer's user-level override is invisible to teammates by design.

**Why B is Wrong:** There is no automatic sync of `~/.claude/` across machines; that directory is private to each user.
**Why C is Wrong:** `.claude/settings.local.json` is gitignored by default, but `.claude/settings.json`, `.claude/agents/`, and `.claude/commands/` are the intended shared path.
**Why D is Wrong:** Claude Code does not operate a cloud-sync service for agents; shared config flows through git only.

**Pattern/Trap:** P15 Configuration Hierarchy

</details>

---

**Q84.** The support agent has `allowedTools: ["get_customer", "lookup_order", "process_refund", "escalate_to_human"]`. A user writes: "Please escalate this to a human — I want a supervisor now." Claude responds by apologizing and offering a $20 credit instead. Which change is most aligned with best practice?

- **A)** Add a system-prompt rule: "If the user requests escalation, call escalate_to_human immediately and do not offer alternatives."
- **B)** Remove `process_refund` from `allowedTools` so Claude cannot offer credits.
- **C)** Lower temperature to 0.
- **D)** Add a `PostToolUse` hook that rewrites credit offers into escalations.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Explicit escalation criteria belong in the agent's system prompt (and reinforced by the `escalate_to_human` tool description). Honoring a direct user request to escalate is a policy rule the model must follow; a clear, unambiguous instruction is the correct first step before adding programmatic enforcement.

**Why B is Wrong:** Removing `process_refund` breaks legitimate refund handling for every other case and does not teach the agent to escalate — it just narrows the menu.
**Why C is Wrong:** Temperature 0 does not teach escalation behavior; the model can still deterministically pick "offer credit" if that is the highest-likelihood path.
**Why D is Wrong:** `PostToolUse` cannot rewrite an assistant message that was never a tool call; credits here were conversational, not tool outputs.

**Pattern/Trap:** P20 Explicit Escalation Criteria

</details>

---

**Q85.** An architect designs an agent loop and insists the loop should also exit when `stop_reason == "pause_turn"`. In what situation is that stop reason emitted, and what is the correct handling?

- **A)** `pause_turn` means the user paused the session; the agent should halt until resumed.
- **B)** `pause_turn` is returned by server-executed tools (web_search, code_execution) when their internal iteration cap is hit; the client should resend the conversation including the paused assistant response to continue.
- **C)** `pause_turn` indicates rate limiting; the client should back off exponentially.
- **D)** `pause_turn` means Claude refused; treat it identically to `refusal`.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** `pause_turn` is specific to server-side tools like `web_search` and `code_execution`. When the internal server-side loop hits its step cap, the API emits `pause_turn`; the client continues by sending the conversation back (including the paused assistant turn) to resume execution.

**Why A is Wrong:** There is no user-pause mechanic that surfaces as `pause_turn`; that is an API-level signal, not a UI state.
**Why C is Wrong:** Rate limiting surfaces as HTTP 429 with retry headers, not as a `stop_reason`.
**Why D is Wrong:** `refusal` is its own distinct stop reason with different semantics (safety); conflating them loses error fidelity.

**Pattern/Trap:** P10 Root Cause vs Symptom

</details>

---

**Q86.** Your coordinator runs an 8-subagent research task. After all subagents return, the coordinator produces a final report. Average coordinator token usage is 180K tokens per run and the team wants to reduce it by 30%. Which approach preserves accuracy best?

- **A)** Instruct subagents to return compressed, structured findings (key facts, citations, confidence) rather than raw search dumps.
- **B)** Replace the coordinator model with Haiku to shrink the summary size.
- **C)** Move the coordinator to the Batch API.
- **D)** Run each subagent twice and majority-vote the outputs before returning to the coordinator.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Per Anthropic's multi-agent research engineering post, subagents should return compressed findings rather than raw tool output to keep coordinator context manageable. This is the primary lever for coordinator token reduction without accuracy loss, because the coordinator only needs synthesized results to do its job.

**Why B is Wrong:** Downgrading the coordinator model harms synthesis quality; the post notes coordinator capability is the single biggest predictor of final answer quality.
**Why C is Wrong:** Batch API is for high-latency asynchronous jobs; a user-facing research task cannot tolerate 24-hour batch windows.
**Why D is Wrong:** Duplicated subagent runs double token cost, the opposite of the goal, and consensus suppresses intermittent useful signal.

**Pattern/Trap:** P7 Batch API Latency Trap

</details>

---

**Q87.** A developer starts a debugging session at 9 AM, steps away, and resumes at 3 PM. She runs `claude --resume <session_id>`. The session's conversation history refers to files that have since been edited by a teammate on a different branch. Which is the best practice?

- **A)** Always resume; Claude tracks file state automatically and will detect mismatches.
- **B)** Use `fork_session` to get a clean state while keeping the original history.
- **C)** Resume only when the prior context is still valid; if the code has meaningfully diverged, start a fresh session to avoid stale assumptions poisoning the reasoning.
- **D)** Run `--resume` with `--clear-context` to reset tool results while keeping messages.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Sessions preserve the full transcript including prior tool results; if file contents have changed, the model's prior reasoning is built on stale data. A fresh session is appropriate when prior context is invalid, while `--resume` is for continuations where context remains accurate.

**Why A is Wrong:** The SDK does not automatically re-verify file state against old tool results; stale reads remain in the transcript as if current.
**Why B is Wrong:** `fork_session` copies existing state into a new session id; it does not clean stale file reads — it duplicates them.
**Why D is Wrong:** There is no `--clear-context` flag that selectively drops tool results while retaining messages.

**Pattern/Trap:** P18 Fresh Session vs Resume

</details>

---

**Q88.** A CI pipeline runs Claude Code non-interactively with `-p` to auto-fix lint warnings. The team wants to prevent Claude from ever writing to `node_modules/` or `.env*` files. Which configuration reliably enforces this?

- **A)** A `PreToolUse` hook matching `Write|Edit` that inspects the target path and returns `permissionDecision: "deny"` for forbidden paths.
- **B)** A system prompt directive: "Never edit node_modules or .env files."
- **C)** A `Notification` hook that warns the user when forbidden paths are touched.
- **D)** A `PermissionRequest` hook to pop up a confirmation dialog.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** `PreToolUse` hooks fire before the tool executes and can deterministically deny based on `updatedInput` inspection; deny precedence overrides allowlists. This is the correct programmatic gate for path-based access control in automated/non-interactive contexts.

**Why B is Wrong:** Prompts cannot guarantee path-level enforcement against a probabilistic model, especially across thousands of CI runs.
**Why C is Wrong:** `Notification` hooks are informational and fire after actions are taken; they do not block.
**Why D is Wrong:** `PermissionRequest` hooks do not fire in non-interactive (`-p`) mode; Anthropic's docs explicitly direct users to `PreToolUse` for automated decisions.

**Pattern/Trap:** P1 Prompt vs Programmatic Enforcement

</details>

---

**Q89.** You define a subagent with `AgentDefinition` fields including `description` and `prompt`. Other developers notice Claude is not routing relevant queries to this subagent. Which field is most commonly the root cause?

- **A)** `prompt` — it needs to be longer to give Claude more to work with.
- **B)** `tools` — subagents cannot be invoked unless `tools` is empty.
- **C)** `description` — it is used by the coordinator to auto-route to this subagent; vague or missing descriptions prevent delegation.
- **D)** `model` — routing requires an explicit `model` override.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** The `description` field is the routing signal the orchestrator reads to decide "when to use this agent." If it is vague, missing, or overlaps with other agents, automatic delegation fails; explicit invocation ("use the X agent") can still work but auto-routing is description-driven.

**Why A is Wrong:** `prompt` is the subagent's system prompt (internal instructions); it does not affect whether the coordinator chooses the subagent.
**Why B is Wrong:** Empty `tools` is not required for invocation; it just restricts what the subagent can do once invoked.
**Why D is Wrong:** `model` is optional; routing works fine with the default inherited model.

**Pattern/Trap:** P5 Tool Description Primacy

</details>

---

**Q90.** A Claude Code agent completes a multi-step refactor. Your project defines `PreToolUse` hooks that gate `Write` and `Bash`. A new subagent you defined also writes files but the hooks do not run when that subagent writes. Why?

- **A)** Subagents inherit parent hooks automatically, so the hooks are running but failing silently.
- **B)** Hooks must be redefined inside each `AgentDefinition.hooks` field or they do not apply.
- **C)** `PreToolUse` hooks only fire for the top-level agent; subagent tool calls bypass them entirely.
- **D)** `PreToolUse` hooks configured via `settingSources: ["project"]` in the parent SDK options apply to the entire session tree, including subagents, provided the subagent's tool calls happen in the same process.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Hooks configured through SDK options or project settings apply to tool calls made during the session, including those originating from subagents running in the same SDK process, because subagent tool calls flow through the same SDK interception layer. Ensure `settingSources` loads `"project"` so `.claude/settings.json` hooks take effect.

**Why A is Wrong:** Hooks are not "silently failing"; Anthropic's docs show hook errors surface in `hook_feedback` or `tool_result` content, not silently.
**Why B is Wrong:** `AgentDefinition` has no `hooks` field; hooks are configured at the session level, not per AgentDefinition.
**Why C is Wrong:** Subagent tool calls do fire `PreToolUse`; the common bug is forgetting to include `settingSources` so the hook file never loads at all.

**Pattern/Trap:** P10 Root Cause vs Symptom

</details>

---

**Q91.** You extract invoices into a schema with required fields `invoice_number`, `total`, `vendor_tax_id`. About 12% of source PDFs omit the tax ID. Current schema marks all three as required; Claude is fabricating plausible tax IDs when absent. Which fix is best?

- **A)** Add a system prompt: "Do not hallucinate."
- **B)** Re-run extractions that produce tax IDs through a second review agent.
- **C)** Change the schema to make `vendor_tax_id` nullable and instruct the model to emit `null` when not present in the source.
- **D)** Lower temperature to 0 so outputs become deterministic.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Required fields with absent source data structurally push the model toward fabrication because the schema demands a value. Making the field nullable and instructing explicit `null`-on-absence aligns the schema with reality and eliminates the incentive to invent data.

**Why A is Wrong:** Generic "do not hallucinate" prompts do not fix a structural contradiction where the schema demands a value the source lacks.
**Why B is Wrong:** A reviewer agent cannot verify a tax ID it also cannot see in the source; it faces the same information gap.
**Why D is Wrong:** Temperature 0 makes fabrication deterministic, not accurate; the model can consistently produce the same wrong tax ID.

**Pattern/Trap:** P14 Nullable Field Prevention

</details>

---

**Q92.** Your agent's `get_customer` MCP tool description reads: "Gets customer." The agent calls it unnecessarily (including for anonymous FAQ questions), driving up costs by 40%. What should you try first?

- **A)** Add a classifier LLM in front of the agent to decide whether customer lookup is needed.
- **B)** Rewrite the tool description to specify when to use it: "Retrieves authenticated customer record. Only call when the user has provided an order ID, email, or account number AND the task requires personal account data."
- **C)** Remove `get_customer` from `allowedTools` and let the agent ask the user for details directly.
- **D)** Reduce the main model from Sonnet to Haiku to make calls cheaper.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** Tool selection is primarily driven by the tool description. Rewriting it with crisp preconditions is the lowest-effort, highest-leverage fix and the first intervention Anthropic recommends before adding classifiers or new components.

**Why A is Wrong:** A classifier LLM is an over-engineered addition that duplicates the LLM's native routing capability; descriptions are the correct lever.
**Why C is Wrong:** Removing the tool breaks legitimate customer lookups; the problem is over-use, not existence.
**Why D is Wrong:** Model downgrade may degrade quality across all tasks and does not address the misrouting cause.

**Pattern/Trap:** P5 Tool Description Primacy, P2 First Step Proportionality

</details>

---

**Q93.** A developer is mid-refactor at turn 47 and wants to explore an alternative database choice without losing the current work. Which command supports this best?

- **A)** `claude --resume <session_id>` and edit the last message.
- **B)** `claude --new` to start fresh, then paste relevant context manually.
- **C)** `claude --resume <session_id> --fork-session` so the new session clones the transcript up to the current point, leaving the original session intact.
- **D)** `claude --resume <session_id> --bypass-permissions` to freely change tools.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** `fork_session` combined with `--resume` clones the session state into a new session id so the developer can branch into the alternative database path while preserving the original session for continuation. This is the canonical "what if" branching pattern.

**Why A is Wrong:** Resuming and editing modifies the single session history and loses the original path the team may want to keep.
**Why B is Wrong:** Starting fresh loses prior reasoning and forces manual recovery, which risks omissions.
**Why D is Wrong:** `--bypass-permissions` has nothing to do with branching; it disables permission checks.

**Pattern/Trap:** P18 Fresh Session vs Resume

</details>

---

**Q94.** The team proposes giving subagents access to the `Agent` tool so they can spawn sub-subagents. What is the documented behavior and recommendation?

- **A)** Recursive Agent spawning is supported and recommended for deep research trees.
- **B)** Sub-subagents are allowed but inherit the root coordinator's conversation history.
- **C)** Subagents inherit the `Agent` tool by default; removing it requires `disallowedTools: ["Agent"]`.
- **D)** Subagents can technically include `Agent` in `tools`, but Anthropic explicitly recommends against it; sub-subagent spawning is unsupported and can cause runaway token usage.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Per Anthropic's subagent documentation, subagents should not spawn their own subagents. Including `Agent` in a subagent's `tools` is discouraged because it enables uncontrolled fan-out, blows token budgets, and makes failure modes opaque.

**Why A is Wrong:** Anthropic's docs explicitly caution against recursive spawning; the multi-agent research post describes a two-level hub-and-spoke, not arbitrary depth.
**Why C is Wrong:** Subagents do not receive `Agent` in inherited tools when they have no way to spawn; the default for subagents excludes Agent to prevent recursion.
**Why B is Wrong:** Even if spawning were allowed, sub-subagents would not inherit the root's history — the only channel is the prompt string.

**Pattern/Trap:** P3 Over-Engineering Distractor

</details>

---

**Q95.** Aggregate agent resolution rate is 92%. Product leadership is happy until a segment analysis shows refund cases resolve at 63% while FAQ cases resolve at 98%. What is the correct architectural response?

- **A)** Celebrate the 92% and move on — aggregate is acceptable.
- **B)** Investigate the refund segment specifically; aggregate accuracy is masking a poorly performing subpath that likely needs its own tool, hook, or subagent.
- **C)** Retrain the model on more FAQ data to further lift the easier segment.
- **D)** Increase temperature to encourage more creative refund solutions.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** Aggregate metrics frequently mask segment-specific failure modes. A 35-point gap indicates a structural issue in the refund path (tool design, policy enforcement, decomposition) that requires targeted investigation, not aggregate optimism.

**Why A is Wrong:** Ignoring segment gaps means refund users experience near-coin-flip support quality while leadership reports success.
**Why C is Wrong:** Retraining on the strong segment widens the gap; it does not address the weak segment.
**Why D is Wrong:** Higher temperature reduces determinism on a policy-heavy task, worsening refund accuracy.

**Pattern/Trap:** P12 Aggregate Metric Masking

</details>

---

**Q96.** The coordinator returns its final report, but key numerical findings in the middle of the 12,000-token synthesis get dropped when downstream summarization runs. What is the most effective mitigation at the coordinator output stage?

- **A)** Progressively summarize multiple times to tighten the report.
- **B)** Use a larger-context model and let it summarize.
- **C)** Position the most critical findings, numbers, and dates at the beginning and end of the report; avoid burying them in the middle to mitigate "lost in the middle" effects.
- **D)** Encode the findings as base64 so the summarizer cannot drop them.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** The well-documented "lost in the middle" phenomenon means models attend less to content placed midway through long contexts. Front-loading and back-loading critical findings preserves them through downstream processing far more reliably than any encoding trick.

**Why A is Wrong:** Progressive summarization degrades precision on numbers and dates with each pass; it compounds the problem.
**Why B is Wrong:** Larger context does not improve attention quality in the middle; the failure mode persists regardless of window size.
**Why D is Wrong:** Base64 obscures the content from the model entirely, preventing any useful summarization; it is not a serious mitigation.

**Pattern/Trap:** P17 Lost in the Middle, P16 Progressive Summarization Risk

</details>

---

**Q97.** Your extraction agent occasionally emits dates in `MM/DD/YYYY` when source documents use ISO format and vice versa, producing 6% downstream parse failures. Which approach uses Agent SDK hooks most appropriately?

- **A)** A `PostToolUse` hook on the extraction tool that normalizes all dates to ISO 8601 before the result enters downstream storage.
- **B)** A `PreToolUse` hook that rewrites the user prompt.
- **C)** A `Notification` hook that pings Slack on each inconsistency.
- **D)** Add a system prompt saying "always use ISO format."

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** `PostToolUse` is designed for data normalization and side-effects after tool execution; it can append normalized values or transform tool output into conversation-visible `additionalContext`. Deterministic normalization at that layer fixes format drift without re-prompting.

**Why B is Wrong:** `PreToolUse` runs before execution and rewriting the user prompt does not deterministically normalize output format.
**Why C is Wrong:** Notifying Slack records the problem but does not fix it; data still flows in mixed formats.
**Why D is Wrong:** Prompt instructions for formatting are probabilistically followed; 6% deviation is consistent with that weakness.

**Pattern/Trap:** P1 Prompt vs Programmatic Enforcement

</details>

---

**Q98.** An agent loop receives `stop_reason: "refusal"`. Which handling is correct?

- **A)** Retry the same prompt — refusals are usually transient.
- **B)** Treat it as a terminal state: exit the loop and surface an appropriate message; do not resubmit tool results because there is no tool_use block to satisfy.
- **C)** Continue the loop with an empty `tool_result`.
- **D)** Escalate to a more capable model automatically.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** `refusal` indicates Claude declined to respond due to safety constraints. It is a terminal stop reason with no tool_use to satisfy; the correct handling is to exit, log, and surface a user-appropriate message (or route to a human/policy flow), not retry blindly.

**Why A is Wrong:** Refusals are policy-driven, not transient; retrying the identical prompt typically yields the same result and wastes spend.
**Why C is Wrong:** There is no `tool_use` block to match, so sending a `tool_result` produces `invalid_request_error`.
**Why D is Wrong:** Automatic model-escalation on refusals is an attempt to evade safety controls; it is neither a recommended nor reliable pattern.

**Pattern/Trap:** P10 Root Cause vs Symptom

</details>

---

**Q99.** A developer proposes consolidating four tools (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`) into a single `support_action` tool with a `type` parameter to "simplify" the tool list. What is the trade-off most relevant here?

- **A)** Consolidation improves accuracy because Claude picks one tool name.
- **B)** The Agent SDK requires at most three tools, so consolidation is mandatory.
- **C)** Consolidation typically degrades tool-selection accuracy and hides preconditions better expressed in per-tool descriptions and schemas; four well-described tools are generally preferable.
- **D)** Consolidation reduces latency proportional to the number of tools removed.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Tool selection is description-driven; distinct tools with precise descriptions and schemas give Claude the clearest routing signal. Collapsing tools into a typed dispatcher erases description-level precision and schema validation per action, degrading selection accuracy and raising error rates.

**Why A is Wrong:** Selection accuracy depends on description quality, not the number of tools on the menu; one vaguely described tool is worse than four precisely described ones.
**Why B is Wrong:** There is no such limit; Claude regularly uses dozens of tools.
**Why D is Wrong:** Latency is driven by turns and token count; tool count is not a major factor.

**Pattern/Trap:** P3 Over-Engineering Distractor, P5 Tool Description Primacy

</details>

---

**Q100.** Your coordinator spawns a synthesis subagent whose job is to combine earlier subagent outputs and produce a final report. The coordinator currently asks that same synthesis subagent to also self-review its report for accuracy. Quality is mediocre. Which change is most effective?

- **A)** Delegate the review to an independent, separately-instantiated reviewer subagent rather than having the author self-review.
- **B)** Tell the synthesis agent to "be more critical."
- **C)** Run the synthesis subagent three times and majority-vote the outputs.
- **D)** Have the coordinator review by reading the report aloud in its response.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Self-review by the same instance tends to reinforce the author's assumptions rather than catch them. An independent reviewer subagent with a distinct system prompt provides adversarial critique and catches errors the author is biased against seeing.

**Why B is Wrong:** "Be more critical" is a prompt tweak that does not overcome the structural bias of same-instance self-review.
**Why C is Wrong:** Majority voting on the same model/prompt suppresses intermittent but correct minority signals; it masks rare bugs rather than revealing them.
**Why D is Wrong:** The coordinator reading text aloud adds no evaluative capability and does not constitute independent review.

**Pattern/Trap:** P19 Self-Review Limitation, P9 Consensus Review Fallacy

</details>

---

**Q101.** A CI job runs Claude Code to triage failing tests. The team wants runtime limits: no more than 25 turns per job. Where should this be enforced?

- **A)** Include the limit in the system prompt.
- **B)** Configure a `Stop` hook that counts turns internally.
- **C)** Manually abort after 25 turns via a shell timer.
- **D)** Set `maxTurns` in the `ClaudeAgentOptions` (or `AgentDefinition` if run as a subagent) so the loop terminates automatically at the programmatic boundary.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** `maxTurns` is a first-class SDK option that bounds the agent loop deterministically. It is the correct programmatic lever for turn limits and does not depend on prompt adherence or external timing races.

**Why A is Wrong:** Prompt-level turn limits are not enforced; the model does not track turns reliably.
**Why B is Wrong:** `Stop` hooks fire when a turn ends; they do not provide a cleaner mechanism than the built-in `maxTurns` option.
**Why C is Wrong:** A shell timer on wall-clock time is a crude proxy; a slow single turn can burn the budget while a fast 30-turn job runs fine.

**Pattern/Trap:** P1 Prompt vs Programmatic Enforcement

</details>

---

**Q102.** Your agent handles refunds. After refund processing, the workflow must also (a) send a confirmation email and (b) update CRM. Currently the system prompt instructs Claude to "remember to always send email and update CRM after a refund." In production, one of these steps is missed in 9% of cases. Which is the best fix?

- **A)** Add the two steps as bullet points to the system prompt in bold.
- **B)** Deploy a second Claude agent to audit completed refunds weekly.
- **C)** Have the agent apologize to the user and retry.
- **D)** Implement a structured handoff: make `process_refund` return a `next_actions` array, and enforce via a `PostToolUse` hook that queues required follow-ups (`send_confirmation_email`, `update_crm`) or blocks finalization until they complete.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Multi-step workflow enforcement needs programmatic prerequisites and structured handoff, not prompt reminders. Encoding the follow-up obligations into tool output contracts and gate hooks makes completion verifiable rather than hoped-for.

**Why A is Wrong:** Bullet points and bolding do not make a rule programmatically enforceable; 9% drift is consistent with prompt-only controls.
**Why C is Wrong:** Apologies do not prevent the next omission; they convert a reliability issue into a customer-experience issue.
**Why B is Wrong:** Weekly audits catch problems after the fact and do not prevent missed steps in the moment.

**Pattern/Trap:** P1 Prompt vs Programmatic Enforcement

</details>

---

**Q103.** A colleague proposes an "orchestrator-workers" multi-agent design for a coding task that requires editing three tightly-coupled files across the repo. Anthropic's own guidance on this pattern suggests:

- **A)** Orchestrator-workers is ideal because each file can be edited in parallel.
- **B)** Use three independent sessions and manually merge.
- **C)** Orchestrator-workers always outperforms single-agent by ~90%.
- **D)** Multi-agent architectures are poorly suited to tasks requiring shared context or tight inter-agent dependencies, such as most coding tasks with cross-file coupling; a single agent is usually preferable.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Anthropic's multi-agent research engineering post explicitly notes that multi-agent systems are poorly suited to tasks requiring shared context or tight dependencies, and that most coding tasks fall into this category. A single agent retains holistic view of cross-file coupling.

**Why A is Wrong:** Parallel edits across tightly-coupled files produce merge conflicts and inconsistent changes; parallelism is inappropriate where dependencies are tight.
**Why B is Wrong:** Independent sessions plus manual merge is the exact anti-pattern the pattern guidance warns against.
**Why C is Wrong:** The ~90% figure is specific to breadth-first research queries on Anthropic's internal eval, not a universal result; it does not apply to coding.

**Pattern/Trap:** P3 Over-Engineering Distractor

</details>

---

**Q104.** Two `PreToolUse` hooks are registered on `Write`. Hook A always returns `{permissionDecision: "allow", updatedInput: {...pathA}}`; Hook B returns `{permissionDecision: "allow", updatedInput: {...pathB}}`. Which statement best describes SDK behavior?

- **A)** Hooks run sequentially in registration order and the first result wins.
- **B)** Conflicts cause the tool call to be denied automatically.
- **C)** Both inputs are merged field-wise.
- **D)** Hooks run in parallel; when multiple return `updatedInput`, the last one to finish wins and order is non-deterministic. Avoid multiple writers to the same field.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Per Anthropic's hook docs, `PreToolUse` hooks execute in parallel; when several return `updatedInput`, the last to complete wins, which is non-deterministic. The documented guidance is to avoid having multiple hooks write the same input fields.

**Why A is Wrong:** Registration order is not preserved; parallel execution means "first" is meaningless in the sequential sense.
**Why B is Wrong:** There is no automatic conflict-deny; only an explicit `deny` decision blocks the call, and deny beats allow.
**Why C is Wrong:** The SDK does not do field-wise merging of `updatedInput`; last-writer-wins is a whole-object overwrite.

**Pattern/Trap:** P1 Prompt vs Programmatic Enforcement

</details>

---

**Q105.** A developer wants a pre-commit guardrail: before Claude runs `git commit`, a Python script should validate that no `console.log` statements were added. Which mechanism is most appropriate?

- **A)** A `PreToolUse` hook matching `Bash` with a command hook that inspects the pending command and greps the staged diff, denying if a `console.log` is found.
- **B)** A `PostToolUse` hook that warns after the commit completes.
- **C)** A system prompt rule that says "do not commit console.log statements."
- **D)** Turn off the `Bash` tool and require the developer to commit manually.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Pre-commit validation is a classic `PreToolUse` use case: intercept before the tool runs, inspect arguments and repo state, return `deny` if the policy fails. Matching on the `Bash` tool name and running a shell command hook is the canonical pattern in Anthropic's hook guide.

**Why B is Wrong:** `PostToolUse` cannot block the commit; it only sees results after execution and cannot undo them.
**Why C is Wrong:** Prompt rules are probabilistic and do not enforce deterministic pre-commit gates.
**Why D is Wrong:** Disabling Bash removes useful functionality broadly instead of narrowly enforcing the specific rule.

**Pattern/Trap:** P1 Prompt vs Programmatic Enforcement

</details>

---

**Q106.** The agent reports `confidence: 0.94` in its final message when resolving refund cases. Correlating with audit outcomes, refunds labeled "high confidence" have only a 71% correctness rate while low-confidence refunds have 68%. The team wants to use the confidence score to auto-approve. What is the best assessment?

- **A)** 0.94 confidence is reliable; auto-approve above 0.9.
- **B)** Use a second LLM to re-grade the confidence score before using it as a gate.
- **C)** The issue is a temperature problem; setting temperature to 0 will fix calibration.
- **D)** LLM self-reported confidence is typically poorly calibrated. The near-identical correctness across bands indicates the signal has limited discriminative value; do not use it as a gating threshold without calibration and independent validation.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Self-reported confidence from LLMs is a well-documented calibration failure mode. The 71% vs 68% split shows the score is not meaningfully predictive of correctness; using it as an auto-approval gate would produce incorrect approvals near the claimed "high confidence" rate.

**Why A is Wrong:** The empirical data contradicts the assumption; 71% correctness is not acceptable for auto-approval of refunds.
**Why B is Wrong:** A second LLM inherits the same calibration weakness; stacking self-reports does not produce a well-calibrated number.
**Why C is Wrong:** Temperature affects output variability, not the calibration of a model's self-reported score; the miscalibration would persist.

**Pattern/Trap:** P4 Sentiment/Confidence Trap

</details>

---

**Q107.** Your coordinator invokes a `web_researcher` subagent with only the prompt "Research recent trends." The subagent returns generic, unfocused findings. Which decomposition improvement is most impactful?

- **A)** Switch the subagent to Opus.
- **B)** Provide a detailed subagent brief in the prompt: objective, output format, tool/source guidance, scope boundaries, and success criteria — per Anthropic's multi-agent research system guidance.
- **C)** Increase `maxTurns` from 10 to 30.
- **D)** Add two more web-search subagents in parallel.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** Anthropic's engineering post on multi-agent research emphasizes that detailed delegation instructions — clear objective, output format, tool/source guidance, and task boundaries — are the single highest-leverage lever for subagent quality. Vague prompts produce vague work regardless of model or parallelism.

**Why A is Wrong:** Opus cannot infer the missing brief; the model upgrade pays for capability on a mis-specified task.
**Why C is Wrong:** More turns expand generic output without improving direction.
**Why D is Wrong:** Adding parallel subagents with the same vague brief multiplies the cost of generic output.

**Pattern/Trap:** P5 Tool Description Primacy, P2 First Step Proportionality

</details>

---

**Q108.** Two tools are currently separated by role: `get_customer_basic` for agents and `get_customer_full` for managers. About 80% of refund cases require only name + order history, which is in `basic`. However, some legitimate refund flows need `full`. The team debates least-privilege design. Which option best balances security and functionality?

- **A)** Give all agents `get_customer_full` and rely on prompts to restrict use.
- **B)** Remove `get_customer_full` entirely; agents should ask managers manually for every case.
- **C)** Keep `get_customer_basic` as the default for agents with a scoped, purpose-restricted `get_customer_full` callable only via a tool whose `PreToolUse` hook enforces justification capture and refund-case verification.
- **D)** Merge both tools into one and let Claude decide which fields to request.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Least privilege with a scoped cross-role tool for legitimate exceptions is the canonical pattern: default narrow access, provide a gated escalation path for real needs, enforce via programmatic hook rather than trust. This preserves security without breaking the 20% of legitimate flows.

**Why A is Wrong:** Prompts cannot guarantee restriction; exposing full data broadly violates least privilege and creates compliance risk.
**Why B is Wrong:** Blanket removal blocks 20% of legitimate work and forces human bottlenecks on routine cases.
**Why D is Wrong:** Collapsing tools removes the enforcement seam; Claude's "decision" is not a security boundary.

**Pattern/Trap:** P11 Scoped Access / Least Privilege

</details>

---

**Q109.** A flaky integration test passes on 3 of 5 re-runs. The agent is configured to "retry on failure up to 5 times and report the consensus result." The bug being masked is an intermittent race condition. What is the architectural problem?

- **A)** Five retries is not enough; increase to ten.
- **B)** The retries should use the Batch API.
- **C)** Switch to a larger model to improve reliability.
- **D)** Consensus-on-retry masks intermittent bugs rather than surfacing them. The CI agent should flag any failure, not vote it away; retry-and-consensus suppresses exactly the signal engineers need.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Taking consensus over reruns for a probabilistic test suppresses intermittent failures — the most important class of bug to detect. The correct CI posture is fail-on-any-failure with diagnostics, not majority-vote.

**Why A is Wrong:** More retries increase the probability of hiding the bug; a 30% flake rate vanishes quickly under majority voting.
**Why B is Wrong:** Batch API introduces latency unsuitable for CI and does not address the consensus-masking problem.
**Why C is Wrong:** The issue is in the test subject (race condition), not model capability; no model choice changes CI consensus semantics.

**Pattern/Trap:** P9 Consensus Review Fallacy

</details>

---

**Q110.** A required field `ein` (US Employer Identification Number) is absent from 40% of source invoices. The team tries retrying the extraction up to 3 times hoping to get a valid EIN. After retry logic went live, the EIN population rate rose to 97%. A sample audit shows most of the newly-populated EINs are fabricated. What went wrong?

- **A)** The retry count is insufficient; 5 retries would produce cleaner outputs.
- **B)** The temperature is too low; raise it to encourage diverse retry outputs.
- **C)** Retrying does not help when the information is absent from the source; the field should be made nullable and schema/prompt explicitly instructed to return `null` when absent. The rising "success rate" is a hallucination indicator, not improvement.
- **D)** The extractor should pull EINs from an external database automatically.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** When source data is absent, no amount of retrying can recover the missing value; what it does produce is increasingly confident fabrication across retries. Making the schema nullable and explicitly instructing `null`-on-absence is the correct structural fix.

**Why A is Wrong:** More retries amplify fabrication, making the audit failure worse; population rate is a misleading success metric.
**Why B is Wrong:** Higher temperature increases fabrication variability, not accuracy; it makes the problem worse.
**Why D is Wrong:** Silent automatic external enrichment is a material scope change that introduces its own correctness and privacy issues; it is not a fix to the extraction itself.

**Pattern/Trap:** P13 Retry Futility, P14 Nullable Field Prevention

</details>

---

**Q111.** You enable a `SubagentStop` hook to log per-subagent token usage. It fires reliably. A developer also wants a `SubagentStart` hook to inject a common style guide into every subagent. Which is correct?

- **A)** The style guide should be added to the coordinator's system prompt so subagents "inherit" it.
- **B)** Place the style guide in `~/.claude/CLAUDE.md` to force per-subagent inheritance from the user home.
- **C)** Use a `Notification` hook to display the style guide in the UI.
- **D)** Add the style guide to each `AgentDefinition.prompt` (and/or via `SubagentStart` where supported) because subagents do not inherit the parent's system prompt.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Subagents do not inherit the parent's system prompt; the documented injection points are the subagent's own `AgentDefinition.prompt` (and optionally `SubagentStart` where available). Putting the guide there ensures every subagent receives it.

**Why A is Wrong:** Parent system prompts are invisible to subagents by design; the guide would never reach them.
**Why B is Wrong:** User-level `CLAUDE.md` at `~/.claude/` is personal and not loaded into subagents unless settings explicitly wire it in; project-level `CLAUDE.md` is more appropriate but still not automatic for every subagent context.
**Why C is Wrong:** `Notification` hooks are UI-facing and do not enter subagent context.

**Pattern/Trap:** P6 Context Inheritance Misconception

</details>

---

**Q112.** A developer designs a long-running refactor agent and wants to handle crashes gracefully. Which session strategy best supports reliable recovery?

- **A)** Persist the `session_id` returned in the SDK's init message; on crash, invoke `--resume <session_id>` to reload the full transcript and continue from the last state.
- **B)** Serialize the entire conversation to a local JSON file and rebuild it manually on recovery.
- **C)** Rely on memory-only sessions and re-prompt on crash.
- **D)** Always start a fresh session after any crash to avoid stale state.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Sessions persist to `~/.claude/projects/<cwd>/*.jsonl` automatically; `--resume <session_id>` reloads the full transcript including prior tool results, enabling clean recovery. Capturing the `session_id` from `system:init` is the canonical recovery pattern.

**Why B is Wrong:** Manual JSON serialization duplicates what the SDK already does automatically and risks schema drift.
**Why C is Wrong:** Memory-only sessions lose all context on crash, forcing expensive re-prompting and rework.
**Why D is Wrong:** Starting fresh throws away valid context; resume is the correct default when the prior context is still valid.

**Pattern/Trap:** P18 Fresh Session vs Resume

</details>

---

**Q113.** Your agent's `allowedTools` includes MCP-namespaced tools like `mcp__billing__process_refund`. A `PreToolUse` hook is configured with `matcher: "process_refund"`. It never fires. Why?

- **A)** MCP tools cannot be hooked.
- **B)** Hooks must be registered before the MCP server starts.
- **C)** The matcher is a regex against the full tool name, which is `mcp__billing__process_refund`; use a pattern like `mcp__billing__process_refund` or `.*process_refund.*` to match MCP-namespaced names.
- **D)** `PreToolUse` hooks do not support MCP.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Hook matchers are regex strings applied to the full tool name. MCP tools have names in the form `mcp__<server>__<action>`, so a bare `process_refund` pattern does not match. Using the full prefixed name or a wildcard pattern works.

**Why A is Wrong:** MCP tools are absolutely hookable; only the matcher pattern is at fault.
**Why B is Wrong:** There is no ordering requirement between hook registration and MCP server startup; the SDK handles tool discovery.
**Why D is Wrong:** `PreToolUse` works uniformly across built-in and MCP tools.

**Pattern/Trap:** P10 Root Cause vs Symptom

</details>

---

**Q114.** A coordinator synthesizes four subagent outputs. To keep the final context small, the developer recursively summarizes the synthesis three times before presenting to the user. Leadership complains key numbers have shifted: a "$2.3M savings" reported by a subagent appears as "~$2M" in the final output. What is happening?

- **A)** The subagent reported the wrong number originally.
- **B)** A `PostToolUse` hook is truncating numbers.
- **C)** Progressive (iterative) summarization is a known risk: each pass loses precision on numbers and dates. Preserve numeric precision by carrying through verbatim quotes or structured fields rather than re-summarizing.
- **D)** Temperature is too high; setting it to 0 will preserve numbers.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Progressive summarization compounds precision loss; numbers and dates drift under repeated compression because the model rounds or abstracts them for readability. Preservation requires carrying specific facts through as structured data or verbatim quotes, not re-summarizing.

**Why A is Wrong:** The subagent's original number ($2.3M) was correct; the loss happened at the synthesis compression stage.
**Why B is Wrong:** `PostToolUse` is not automatically truncating numbers; this is a prompt-side summarization artifact.
**Why D is Wrong:** Temperature 0 does not prevent summarization-induced rounding; the model still abstracts during compression.

**Pattern/Trap:** P16 Progressive Summarization Risk

</details>

---

**Q115.** A developer defines an agent with no `allowedTools`. They try to delegate via the Agent (Task) tool and find that subagents never spawn. What is the fix?

- **A)** `Agent` (or `Task`) must be included in the parent's `allowedTools` to enable subagent spawning; without it, the tool is not available and delegation silently no-ops.
- **B)** Subagents always spawn; the developer must be misreading logs.
- **C)** Reduce `maxTurns` so the model runs out of room and is forced to delegate.
- **D)** Move the subagent definition to `~/.claude/agents/`.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Per Anthropic's subagent docs, the `Agent` tool (or its prior name `Task`) must appear in the parent session's `allowedTools` or the tool is not exposed to the model, so no delegation can occur. This is the most common silent-failure cause.

**Why B is Wrong:** Delegation can silently fail without any error when the Agent tool is omitted; logs will simply show no `tool_use: Agent` blocks.
**Why C is Wrong:** `maxTurns` does not affect tool availability; running out of turns terminates the loop without enabling missing tools.
**Why D is Wrong:** Relocating the agent file does not solve the allowedTools omission; the parent still cannot emit the Agent tool call.

**Pattern/Trap:** P10 Root Cause vs Symptom

</details>

---

**Q116.** The team asks: should the main Sonnet-based support agent also perform nightly data summarization of closed tickets? Nightly summarization is offline, tolerant of latency, and batchable. Which architecture recommendation fits?

- **A)** Run nightly summarization in the live support agent loop to reuse infrastructure.
- **B)** Route nightly summarization through a Claude Code CLI for developer-style task management.
- **C)** Skip summarization; tickets are already logged.
- **D)** Run nightly summarization through the Anthropic Batch API since the workload is asynchronous, latency-tolerant, and cost-sensitive; reserve the live agent for user-facing, blocking flows.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Batch API is designed for asynchronous, high-volume, latency-tolerant jobs at reduced cost. Nightly ticket summarization is a textbook fit: it does not block a user, can run with hours of latency, and benefits from batch cost economics. The live agent stays focused on real-time blocking flows.

**Why A is Wrong:** Interleaving nightly bulk work into the live agent risks latency spikes for real users and conflates very different SLOs.
**Why B is Wrong:** Claude Code CLI is optimized for developer-interactive coding workflows, not scheduled bulk summarization.
**Why C is Wrong:** Skipping summarization loses analytical value leadership requested; logs are raw, not insight.

**Pattern/Trap:** P7 Batch API Latency Trap (applied correctly here — Batch is right for this non-blocking flow)

</details>

---

**Q117.** An architect observes a pattern across agent failures: whenever subagent output passes through the coordinator, specific structured facts (order IDs, amounts, timestamps) are sometimes dropped. Several fixes are proposed. Which is the best durable architecture for preserving structured facts end-to-end?

- **A)** Increase coordinator context window to 1M tokens.
- **B)** Ask the coordinator to "double-check" all numbers in its prose output.
- **C)** Add a `PreToolUse` hook that rewrites coordinator prose.
- **D)** Have subagents return structured JSON (not prose) to the coordinator, and have the coordinator treat those fields as immutable pass-through values in the final report rather than re-describing them in prose.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Structured JSON handoff between subagents and coordinator preserves precise facts by construction; treating those fields as immutable pass-through data in the final output prevents prose-layer re-description from drifting numbers or losing IDs. This is the canonical structured-handoff pattern.

**Why A is Wrong:** A larger context window does not address "lost in the middle" attention quality or progressive-summarization drift; more room is not more precision.
**Why B is Wrong:** Asking the coordinator to self-check prose is weak self-review and does not prevent drift deterministically.
**Why C is Wrong:** `PreToolUse` fires on tool calls, not on coordinator prose generation; there is no tool call to intercept at that stage.

**Pattern/Trap:** P8 Larger Context Window Fallacy, P19 Self-Review Limitation

</details>

---
