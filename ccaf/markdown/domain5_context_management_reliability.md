# Domain 5: Context Management & Reliability

> Claude Certified Architect – Foundations

> Exam Weight: 15% | Questions in Pool: 33

*Generated from the JSONL bank by `scripts/render_markdown.py` — do not edit by hand.*
*Private study material, assembled from mixed sources: not licensed for redistribution.*

---

**Q3.** Your agent achieves 55% first-contact resolution, well below the 80% target. Logs show it escalates straightforward cases while attempting to autonomously handle complex situations requiring policy exceptions. What's the most effective way to improve escalation calibration?

- **A)** Add explicit escalation criteria to your system prompt with few-shot examples demonstrating when to escalate versus resolve autonomously.
- **B)** Have the agent self-report a confidence score (1-10) before each response and automatically route requests to humans when confidence falls below a threshold.
- **C)** Deploy a separate classifier model trained on historical tickets to predict which requests need escalation before the main agent begins processing.
- **D)** Implement sentiment analysis to detect customer frustration levels and automatically escalate when negative sentiment exceeds a threshold.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Adding explicit escalation criteria with few-shot examples directly addresses the root cause: unclear decision boundaries. Option B fails because LLM self-reported confidence is poorly calibrated. Option C is over-engineered. Option D solves a different problem entirely.

</details>

---

**Q69.** A customer support agent is handling a complex billing dispute that spans 20+ turns. A customer mentioned early in the conversation that they were charged $847.50 on March 3rd for a service they cancelled on February 28th. Midway through the conversation, the agent references the charge as "the overcharge from last month" without the specific amount. The customer disputes the agent's understanding of the case. What context management technique would prevent this?

- **A)** Use `/compact` at the start of each conversation to summarize prior turns into a shorter representation.
- **B)** Extract transactional facts (amounts, dates, order numbers, statuses) into a persistent "case facts" block that is included at the beginning of every subsequent prompt in the conversation.
- **C)** Increase the model's context window by switching to a larger tier to retain the full conversation without summarization.
- **D)** Instruct the agent to re-read the full conversation history before each response.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Extracting precise transactional facts into a persistent "case facts" block ensures that specific numerical values, dates, and customer-stated details are explicitly available in every prompt turn rather than buried in growing conversation history. Progressive summarization risks condensing these details into vague references like "overcharge from last month." Option A's compaction is useful for context length management but can lose precision on transactional facts. Option C does not prevent progressive summarization and is not a reliable solution. Option D is not practical for long conversations and still does not prevent facts from being lost as context grows.

</details>

---

**Q70.** A multi-agent research pipeline aggregates findings from six subagents, each returning 800-1,200 tokens of raw tool output and reasoning. The synthesis agent receives all results in a single large message. The final report consistently omits or contradicts findings that appeared in the middle sections of the aggregated input. What is the most likely cause and the most effective mitigation?

- **A)** The subagents are returning conflicting information; add a deduplication step before synthesis.
- **B)** The synthesis agent is hitting its output token limit; increase `max_tokens` to allow a longer response.
- **C)** The "lost in the middle" effect causes models to reliably process content at the beginning and end of long inputs but miss middle sections. Mitigate by placing key findings summaries at the beginning of aggregated inputs and organizing sections with explicit headers.
- **D)** The synthesis agent's context window is exhausted; route some subagent outputs through a secondary summarization agent before passing to synthesis.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

The "lost in the middle" effect is a well-documented limitation where models attend less reliably to content in the middle of long inputs. Placing key findings at the beginning and using explicit section headers to organize the aggregated input significantly mitigates this effect. Option A addresses data consistency but not the positional attention problem. Option B addresses output length, not input attention. Option D adds pipeline complexity and may help with context length, but does not address the positional attention issue on its own.

</details>

---

**Q71.** A customer opens a support chat saying "I'd like to speak to a human please. I've been dealing with this billing issue for three weeks and I'm frustrated." The agent has already identified this as a standard billing adjustment that it can resolve in 2 steps using its available tools. Your agent responds by saying "I can help with that right away, let me pull up your account." and proceeds to investigate. The customer repeats their request for a human. What is wrong with this behavior and what should be corrected?

- **A)** The agent should honor an explicit customer request for a human agent immediately on first request, without attempting investigation first.
- **B)** The agent should detect negative sentiment and escalate once the frustration score exceeds a defined threshold.
- **C)** The agent should complete its investigation, present the proposed solution, and escalate only if the customer still insists afterward.
- **D)** The agent should apologize for the wait, then proceed with automated resolution since the case is within its capability.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

When a customer explicitly requests a human agent, that request must be honored immediately regardless of whether the agent believes it can resolve the issue. Proceeding with investigation after a clear escalation request violates the design principle documented in Task 5.2. Option B introduces sentiment scoring as a proxy, but the customer has already expressed an explicit preference. Sentiment analysis is irrelevant here. Option C delays honoring the request while investigation proceeds, which further frustrates the customer. Option D is the agent's current incorrect behavior: capability is not the deciding factor when a customer has made an explicit request.

</details>

---

**Q72.** Your web search subagent encounters a timeout while fetching results for a competitor analysis. The engineering team implements a change so the subagent catches the timeout internally and returns an empty result set with `status: "success"` and `results: []`. The coordinator receives this and the synthesis agent produces a report that is missing the competitive section entirely, with no indication anything went wrong. What is the problem with this approach?

- **A)** Silently returning an empty success result prevents the coordinator from making any recovery decision and allows incomplete work to pass as complete output.
- **B)** The synthesis agent should be responsible for detecting empty sections and re-triggering the search subagent directly.
- **C)** The coordinator should always validate that each subagent returned non-empty results before proceeding to synthesis.
- **D)** The timeout threshold should be increased so that the subagent does not time out before returning real results.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Silently suppressing errors by returning empty results as success is an explicitly documented anti-pattern. It removes the coordinator's ability to recover, retry, or annotate output with coverage gaps. Option B incorrectly shifts the recovery responsibility to the synthesis agent, which lacks the tools and context to re-run searches. Option C adds coordinator-level validation as a safeguard, but it does not address the root cause: the subagent is misrepresenting failure as success. Option D addresses the symptom (timeout threshold) rather than the error propagation design flaw.

</details>

---

**Q73.** An agent is performing a deep exploration of a 200,000-line legacy codebase to understand its payment processing flow. After approximately 90 minutes and dozens of file reads, the agent begins referencing "standard patterns in payment systems" rather than the specific classes and flows it found earlier, and its answers become inconsistent with findings from the first hour. What is the most likely cause and the best mitigation strategy?

- **A)** The agent has reached a rate limit; the fix is to add delays between tool calls to stay within limits.
- **B)** Context degradation: as the session grows, specific findings from early in the session compete with general knowledge and the agent's position-attention effects. Mitigate by having the agent maintain a scratchpad file recording key findings throughout the session.
- **C)** The legacy codebase's file structure is too complex for a single agent; break it into independent subsystems and run separate agents on each subsystem simultaneously.
- **D)** The agent is using the wrong tools; switching from `Read` to `Grep` for file exploration would reduce context consumption.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Context degradation in extended sessions is a known pattern: models start giving inconsistent answers and referencing general knowledge rather than specific findings discovered earlier. Having the agent maintain a scratchpad file that records key findings creates a persistent, explicit record that can be referenced and included in subsequent prompts, preventing specific details from being lost to context pressure. Option A misidentifies the cause as a rate limit. Option C adds parallelism but does not address the single-session degradation problem. Option D changes tooling but does not address context growth or degradation.

</details>

---

**Q74.** You are running a multi-phase codebase investigation using the Claude Agent SDK. After 45 minutes of exploration (reading files, tracing call chains, building a dependency map) you move into the second phase: identifying security vulnerabilities in the authentication module. You notice the agent is now describing the authentication module as "using standard JWT patterns" when earlier in the session it had found a custom token signing implementation. What technique would most effectively preserve key findings across these phase boundaries?

- **A)** Have the agent maintain a scratchpad file that records key findings after each phase, and reference that file at the start of subsequent phases rather than relying on conversation history.
- **B)** Use `/compact` before starting the second phase to free up context space and allow the agent to re-read files as needed.
- **C)** Restart the session with a fresh context at the start of each phase, passing a manual summary of what you found.
- **D)** Increase the `max_tokens` parameter so the model can hold more context without compressing earlier findings.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Scratchpad files are the recommended technique for persisting key findings across context boundaries when context degradation becomes apparent. The agent can write structured notes during exploration and read them back at phase boundaries, ensuring critical findings, like the custom token signing implementation, are not lost to context compression. Option B uses `/compact` to free up space, but this compresses conversation history and may lose the specific finding about the custom token signing. Option C is a valid but costly approach: restarting sessions loses the accumulated understanding and requires manual intervention. Option D is incorrect because `max_tokens` controls output length, not context window size, and would not prevent the degradation.

</details>

---

**Q75.** A structured data extraction system for insurance claims achieves 97% overall accuracy on a validation set. The team proposes automating the full workflow without human review. A colleague argues this aggregate metric masks important risks. What is the most important concern?

- **A)** 97% accuracy means 3% of claims will have errors, which could create legal liability if unchecked.
- **B)** Human review should always be retained regardless of accuracy metrics because automation of insurance decisions creates regulatory risk.
- **C)** The validation set may not be representative of production data volumes, so the 97% figure cannot be trusted.
- **D)** Aggregate accuracy metrics can mask poor performance on specific document types or fields. A claim type or field category with 85% accuracy would be hidden by strong performance elsewhere, and stratified analysis is needed before automating.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

The core risk is that aggregate metrics can hide poor performance on specific segments. A document type with 85% accuracy on a critical field like `claim_amount` would be masked by strong performance across other document types. Before automating, accuracy should be validated by document type and field segment to confirm consistent performance across all dimensions. Option A is a valid concern but describes the error rate, not the masking risk. Option C raises a data quality concern but is not the most important concern about the specific 97% figure. Option B makes a policy argument that does not engage with the analytical gap identified.

</details>

---

**Q76.** An extraction pipeline achieves high accuracy on average but the team wants to implement confidence-based routing: high-confidence extractions proceed automatically while low-confidence ones go to human review. A developer proposes using the model's stated confidence scores directly as the routing threshold. What is the critical flaw in this approach?

- **A)** Confidence scores add tokens to every response, increasing API costs unnecessarily.
- **B)** Model confidence scores must be calibrated against a labeled validation set to determine what score threshold actually corresponds to acceptable accuracy. Uncalibrated raw scores are not reliable predictors of extraction correctness.
- **C)** Confidence scores only work when the model outputs a single extraction; multi-field documents require a different approach.
- **D)** Routing on confidence scores creates two separate code paths that are harder to maintain than a single uniform review workflow.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

A model's raw confidence scores need calibration: without comparing stated confidence against actual correctness on a labeled validation set, there is no reliable mapping between a score of "0.85" and an acceptable error rate. Calibrating the threshold ensures that the routing cut-off corresponds to a known accuracy level. Option A is a minor operational concern, not a critical flaw. Option C is incorrect; confidence scores can be applied at the field level for multi-field documents. Option D is an engineering tradeoff, not a flaw in the confidence approach itself.

</details>

---

**Q77.** A research synthesis agent is combining findings from five subagents that searched different sources. The final report states that "AI adoption in healthcare reached 45% in 2024" but does not cite which source this came from. A reviewer cannot verify the claim because the subagents' individual outputs were not preserved. What structural change to the pipeline would prevent this provenance loss?

- **A)** Require the synthesis agent to add a generic "Sources consulted" section at the end of the report listing all sources accessed.
- **B)** Require subagents to output structured claim-source mappings (claim text, source URL, document name, relevant excerpt) and instruct the synthesis agent to preserve and merge these mappings into the final report rather than summarizing them away.
- **C)** Store all raw subagent outputs in a separate log file so they can be consulted if a claim needs verification.
- **D)** Add a post-synthesis review step where a separate agent checks each claim in the report against the raw subagent outputs.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

The root cause of provenance loss is that summarization steps compress findings without preserving claim-to-source mappings. Requiring subagents to output structured mappings and instructing the synthesis agent to preserve and merge them ensures that each claim in the final report carries its source attribution through the pipeline. Option A produces a list of sources consulted but does not link individual claims to specific sources. Option C stores raw data as a fallback but does not integrate provenance into the report itself. Option D adds a verification step after the fact but does not prevent the structural provenance loss.

</details>

---

**Q205.** A support agent has been running for 47 turns with a customer disputing a charge. To stay under the context budget, the orchestration layer applies progressive summarization every 10 turns, replacing prior turns with a 200-token summary. On turn 48, the agent confidently tells the customer "we'll process your refund as discussed," but the most recent summary reads only "agent acknowledged dispute and discussed refund options with customer." The original turn-12 commitment was "refund of $147.83 to card ending 4412 within 3 business days." What is the most appropriate fix?

- **A)** Raise the summarization interval from every 10 turns to every 20 turns so more raw context is retained between compactions.
- **B)** Switch to a model with a larger context window so summarization is unnecessary for sessions under 100 turns.
- **C)** Maintain a persistent "case facts" block (refund amount, card last-4, promised timeline, ticket ID) that is extracted on first mention and re-injected verbatim into every prompt, separate from the rolling summary.
- **D)** Instruct the summarizer in its system prompt to "preserve all important details" before each compaction step.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Progressive summarization reliably loses transactional specifics — exact amounts, dates, account identifiers, and explicit commitments — because summarizers compress toward semantic gist. Extracting transactional facts into a structured block that bypasses summarization preserves them losslessly across the entire session.

**Why A is Wrong:** Less frequent summarization only delays the loss; once any summarization occurs, numerical specifics are still vulnerable. It also makes the eventual compaction more lossy because more must be condensed at once.
**Why B is Wrong:** Larger context windows exhibit the same recall degradation ("context rot") and do not address the structural problem that summaries discard transactional detail.
**Why D is Wrong:** A vague natural-language instruction like "preserve important details" is a prompt-only mitigation that fails unpredictably; the summarizer cannot reliably distinguish which numbers will matter on turn 48 when summarizing turn 12.

**Pattern/Trap:** P16 Progressive Summarization Risk; P1 Prompt vs Programmatic Enforcement

</details>

---

**Q206.** A lead research agent receives reports from six subagents and concatenates them (in order of completion) into a 78,000-token aggregated input before producing the final synthesis. Evaluation shows the synthesis reliably reflects subagent #1 (early in the input) and subagent #6 (late in the input), but routinely omits findings from subagents #3 and #4 — the middle of the aggregate. Which change most directly addresses this failure mode?

- **A)** Re-run the missing subagents to confirm their findings are reproducible before including them in the synthesis.
- **B)** Reduce each subagent's report to a 500-token summary so the aggregate fits in 25,000 tokens total.
- **C)** Have each subagent produce a structured "key findings" header (5–8 bullet claims with source IDs) and prepend all six headers to the top of the aggregated input, with full reports following.
- **D)** Sort subagent reports alphabetically by topic so position is deterministic across runs.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Models reliably attend to the beginning and end of long inputs but degrade in the middle. Hoisting compact key-findings headers to the top of the aggregate guarantees every subagent's claims occupy a high-recall position, while full reports remain available for grounding.

**Why A is Wrong:** Reproducibility is not the issue — the findings exist in the input but are positionally disadvantaged. Re-running wastes tokens and budget without changing the geometry that caused the omission.
**Why B is Wrong:** Aggressive compression risks dropping the same details the synthesis needs and does not eliminate the middle position; subagents #3 and #4 will still be middle in a smaller aggregate.
**Why D is Wrong:** Alphabetical ordering makes position deterministic but does not place high-signal content at boundary positions. Whichever topics fall in the middle still get under-attended.

**Pattern/Trap:** P17 Lost in the Middle

</details>

---

**Q207.** A support agent uses an `order_lookup` tool that returns 43 fields per order (line items, tax breakdowns, fulfillment events, internal warehouse codes, marketing attribution). The agent typically only needs 5 fields (order ID, status, total, ship date, tracking number). After 8 lookups in a session, tool results consume 31% of the context window, and the agent begins missing earlier conversation details. What is the best first remediation?

- **A)** Modify the tool wrapper to project only the 5 required fields by default, with a parameter to opt into the full schema when needed.
- **B)** Increase the model's context window tier and accept the higher per-call cost as the price of reliability.
- **C)** Add a system-prompt instruction telling the agent to "ignore irrelevant fields in tool results."
- **D)** After each tool call, run a separate Claude call to summarize the tool output into 200 tokens before appending it to context.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Tool-result accumulation is one of the largest sources of context bloat in agent systems. Trimming at the source — projecting only the relevant fields in the tool wrapper — eliminates the bloat deterministically before it ever enters context. This is a programmatic fix that scales linearly with calls.

**Why B is Wrong:** A larger window delays the symptom but compounds cost, and recall still degrades over long sessions ("context rot"). It treats the symptom rather than the root cause of irrelevant tokens.
**Why C is Wrong:** The model still pays attention cost on tokens it sees, regardless of instructions to ignore them. Prompt-only mitigations cannot reduce token consumption.
**Why D is Wrong:** A per-call summarization step adds latency and another LLM dependency that can itself drop critical fields like the tracking number; the verbose data was unnecessary in the first place.

**Pattern/Trap:** P10 Root Cause vs Symptom; P3 Over-Engineering Distractor

</details>

---

**Q208.** A team building a chat agent on the Messages API observes that on the second user turn, the assistant frequently "forgets" facts established in turn 1. Inspection shows the client sends only the most recent user message in each `messages` array, relying on the model's "memory." Which statement correctly characterizes the problem and fix?

- **A)** The Messages API maintains a hidden session cache keyed by API key; the team should pass a `session_id` header so prior turns are auto-loaded.
- **B)** The team should use the prompt-caching feature, which causes the API to retain prior turns server-side between calls.
- **C)** The model's context window is shared across recent calls from the same key, so adding a longer `system` prompt restating the facts will resolve the issue.
- **D)** The Messages API is stateless; every request must include the full prior conversation (all user and assistant turns) in the `messages` array, or earlier facts are not available to the model.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Anthropic's Messages API is stateless — the model only sees what is sent in the current request's `messages` array. The "memory" of a conversation is a client-side responsibility: the application must accumulate and resend prior turns.

**Why A is Wrong:** There is no `session_id` mechanism on the Messages API and no hidden server-side conversation cache keyed by API key. This option fabricates a feature.
**Why B is Wrong:** Prompt caching reduces cost and latency by caching token prefixes, but the client must still send those tokens in each request. Caching does not make the API stateful.
**Why C is Wrong:** Restating facts in the system prompt could partly help but is brittle and does not address that assistant turns (decisions, commitments, tool results) are also lost. The structural fix is sending full conversation history.

**Pattern/Trap:** P6 Context Inheritance Misconception

</details>

---

**Q209.** A customer writes: "This is the third time I've contacted you. I want to speak to a human agent now." The agent has full capability to issue the duplicate-shipment refund the customer is requesting and the policy clearly applies. What should the agent do?

- **A)** Acknowledge the frustration, issue the refund immediately since policy permits it, and only escalate if the customer remains dissatisfied after the resolution.
- **B)** Hand off to a human agent immediately, summarizing the case and the customer's explicit request, even though the agent could resolve it.
- **C)** Ask one more clarifying question to confirm the refund details before deciding whether to escalate or resolve.
- **D)** Issue the refund and send confirmation, noting in the ticket that the human-agent request was overridden because the issue was resolvable.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** An explicit customer request for a human agent is a hard escalation trigger that must be honored regardless of whether the agent could otherwise resolve the issue. Overriding an explicit request — even with a correct outcome — damages trust and violates a clear escalation criterion.

**Why A is Wrong:** Resolving despite an explicit human-agent request ignores a hard trigger. The "offer to resolve" pattern applies when the customer is frustrated but has not explicitly requested escalation.
**Why C is Wrong:** Asking another question delays handoff and ignores the explicit request, likely intensifying frustration. The trigger is unambiguous and a clarification is not warranted.
**Why D is Wrong:** "Overriding" an explicit human-agent request is the worst pattern: it disregards the customer's stated preference and creates a paper trail of policy violation, even when the outcome is correct.

**Pattern/Trap:** P20 Explicit Escalation Criteria

</details>

---

**Q210.** A team adds an automated escalation rule: if a sentiment classifier scores the customer's message below −0.6, the agent immediately routes to a human. Post-launch, escalation volume jumps 40%, but human agents report that 60% of escalated cases involved straightforward, in-policy issues the bot could have resolved. Meanwhile, several calmly worded but truly out-of-policy cases were not escalated. What is the underlying problem?

- **A)** Sentiment is a noisy proxy that correlates with frustration but not with whether the issue is resolvable; escalation should be driven by explicit criteria (human request, policy gap, inability to make progress) rather than emotional tone.
- **B)** The sentiment threshold is too aggressive at −0.6; lowering to −0.8 will fix the false positives.
- **C)** The sentiment classifier needs to be fine-tuned on customer-support transcripts to improve precision.
- **D)** Sentiment-based escalation works in principle but should be combined with a self-reported confidence score from the agent.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Sentiment measures emotional tone, which is orthogonal to whether a case is within agent capability. A frustrated customer with an in-policy refund should be served, not escalated; a polite customer asking for a policy exception must be escalated. Robust escalation uses explicit, observable criteria rather than affective signals.

**Why B is Wrong:** Tuning the threshold trades one error type for another but does not fix the categorical mismatch between sentiment and resolvability.
**Why C is Wrong:** A more accurate sentiment classifier still answers the wrong question. Improving classification of an irrelevant signal does not produce a correct escalation decision.
**Why D is Wrong:** Self-reported model confidence is itself unreliable as an escalation gate — models are often confidently wrong and uncertainly right. Layering two unreliable proxies does not produce a reliable trigger.

**Pattern/Trap:** P4 Sentiment/Confidence Trap; P20 Explicit Escalation Criteria

</details>

---

**Q211.** A customer asks the support agent to match a competitor's lower price on a TV. The agent's policy document covers price-matching against the company's own past prices and against authorized resellers, but is silent on third-party competitors. The agent confidently quotes a 12% discount based on what "seems consistent with the spirit of the policy." How should the agent's behavior be corrected?

- **A)** Add the competitor price-match scenario to the policy document so the agent has explicit guidance.
- **B)** Lower the agent's response temperature to 0 to reduce creative interpretation of policy.
- **C)** Update the system prompt with explicit escalation criteria, including "if a customer asks about a scenario the policy does not address, escalate to a human agent" plus 2–3 few-shot examples covering policy-gap cases.
- **D)** Instruct the agent to apply policies "conservatively" when there is uncertainty.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** The agent's failure was treating a policy gap as an interpretation problem. Explicit escalation criteria for policy gaps — paired with few-shot examples that demonstrate the boundary between covered and uncovered scenarios — give the model a concrete pattern to recognize.

**Why A is Wrong:** Expanding the policy is a separate business decision that may take weeks; meanwhile the agent will keep improvising on other gaps. The escalation pattern is the architectural fix and applies to all future gaps.
**Why B is Wrong:** Temperature 0 makes the wrong behavior deterministic, not correct. The model still lacks instruction that gaps require escalation rather than interpretation.
**Why D is Wrong:** "Conservatively" is vague and the model's notion of conservative may still produce a fabricated discount. Without explicit criteria and examples, the abstract instruction fails predictably.

**Pattern/Trap:** P20 Explicit Escalation Criteria; P1 Prompt vs Programmatic Enforcement

</details>

---

**Q212.** A customer provides only the name "Maria Garcia." The customer-lookup tool returns three matching accounts with different emails and order histories. The agent picks the account with the most recent order and proceeds to discuss it. Which response represents the correct pattern?

- **A)** Use a heuristic — most recent order, highest lifetime value, or closest geographic match — to pick the most likely account, since asking for clarification creates friction.
- **B)** Pick any of the three accounts and proceed; if the customer corrects, the agent can switch accounts mid-conversation.
- **C)** Escalate immediately to a human agent because account ambiguity is inherently outside agent capability.
- **D)** Ask the customer for an additional identifier (email, order number, last 4 of payment method, ZIP code) to disambiguate before discussing any account-specific information.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Multiple matches create a real ambiguity that no heuristic can safely resolve, because acting on the wrong account exposes account-specific information to a different customer — a privacy and security failure. The correct pattern is requesting one additional identifier, which costs one turn but eliminates ambiguity deterministically.

**Why A is Wrong:** Heuristic selection optimizes for friction at the expense of correctness and privacy. "Most recent order" can easily be the wrong Maria Garcia, and the agent will reveal her details to the wrong person.
**Why B is Wrong:** Speaking about one account before disambiguation leaks information about that account to a person who may not be its owner. Mid-conversation correction does not undo the disclosure.
**Why C is Wrong:** Disambiguation by asking for one more identifier is well within agent capability and does not require human escalation. Escalating here over-uses scarce human capacity.

**Pattern/Trap:** P20 Explicit Escalation Criteria; P11 Scoped Access / Least Privilege

</details>

---

**Q213.** A research subagent's web-search tool intermittently fails. The subagent currently catches all exceptions and returns the string `"search unavailable"` to the lead agent. Downstream, the lead agent cannot distinguish a transient network blip (worth retrying) from an authentication failure (needs config fix) from a query that simply returned zero results. Reports come back with unexplained gaps. What is the right error contract?

- **A)** Have the subagent suppress the error entirely and return an empty result list, so the lead agent treats failures as "no findings."
- **B)** Replace the search tool with a more reliable provider so error-handling logic becomes unnecessary.
- **C)** Have each subagent independently retry up to 50 times with exponential backoff before reporting any failure.
- **D)** Return a structured error object including `failure_type` (timeout / auth / rate_limit / empty_result), `attempted_query`, `partial_results` if any, and `suggested_alternatives`, so the lead agent can decide whether to retry, reroute, or annotate.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Generic error strings collapse meaningfully different failure modes into one opaque signal, destroying information the orchestrator needs to act intelligently. A structured error context — failure type, what was attempted, any partial results, suggested alternatives — lets the lead agent route transient failures to retry, surface configuration failures to operators, and treat genuine empty results as legitimate findings.

**Why A is Wrong:** Conflating failures with empty results is a silent-suppression anti-pattern: the report will look complete but is missing data the user assumes was searched.
**Why C is Wrong:** Aggressive retry without classification wastes budget on permanent failures (auth, malformed query) and delays the lead agent's ability to adapt.
**Why B is Wrong:** No provider is perfectly reliable, so error handling cannot be eliminated. This treats the tool as the root cause when the architectural defect is the error contract itself.

**Pattern/Trap:** P10 Root Cause vs Symptom

</details>

---

**Q214.** A subagent calls a document-retrieval API that has a 2% transient timeout rate. Currently, every timeout is propagated up to the lead agent, which then must decide whether to retry, reroute, or fail. Retries from the lead level cost one full round-trip of LLM reasoning each. How should error handling be redesigned?

- **A)** The subagent should locally retry transient failures (timeouts, 5xx) with exponential backoff up to a small bounded limit, propagating to the lead agent only unrecoverable errors with a description of what was attempted and what failed.
- **B)** The lead agent should retry every error it receives once, regardless of failure type, since most errors at this scale are transient.
- **C)** The subagent should treat every timeout as a permanent failure and immediately propagate, since retries hide real problems.
- **D)** Add a third-tier "retry agent" between subagent and lead whose sole responsibility is retry orchestration.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** The principle is local recovery for recoverable errors, structured propagation for unrecoverable ones. Subagents are closer to the failure and can retry transient issues cheaply, without consuming lead-agent reasoning tokens. When propagation is necessary, the lead agent receives a structured account of attempts and final failure mode so it can make an informed routing decision.

**Why B is Wrong:** Blind lead-level retry of every error wastes LLM budget on permanent failures and conflates retryable with non-retryable.
**Why C is Wrong:** Propagating every timeout floods the lead with noise and makes the system brittle to normal network jitter. A 2% transient rate is exactly the case bounded local retry was designed for.
**Why D is Wrong:** A separate retry agent adds an LLM-mediated hop for what is a deterministic concern. Retry belongs in the data path as code, not as a third agent.

**Pattern/Trap:** P3 Over-Engineering Distractor; P13 Retry Futility

</details>

---

**Q215.** A research orchestrator queries an internal knowledge base via a `kb_search` subagent. For one query, the subagent returns `{"results": []}`. The orchestrator treats this identically to "search failed" and re-issues the query through a different subagent, then a third, accumulating cost without progress. Which design correction addresses the root issue?

- **A)** Configure the orchestrator to never retry searches, since the first answer is usually correct.
- **B)** Have `kb_search` retry internally until at least one result is returned, then propagate.
- **C)** Introduce a confidence score on every search result and only re-query when confidence is below 0.7.
- **D)** Have `kb_search` distinguish in its return value between an access failure (timeout, auth, malformed) and a successful query that returned zero matches, so the orchestrator can treat them differently.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Zero results from a successful query is a valid finding ("the KB does not contain this") and should not trigger retry. An access failure is a retryable problem with the channel, not the data. Conflating the two leads to wasted retries on real empty results and missed retries on real failures. The fix is at the contract level — the subagent must report which case occurred.

**Why A is Wrong:** Never retrying makes the system fragile to genuine transient failures. The defect is conflation, not retry itself.
**Why B is Wrong:** Forcing the subagent to keep searching until it finds something will hallucinate or loosen queries until a result appears, corrupting the research.
**Why C is Wrong:** A confidence score on results does not distinguish "no documents matched" from "search service unreachable." It addresses a different problem.

**Pattern/Trap:** P10 Root Cause vs Symptom

</details>

---

**Q216.** A team's subagents wrap all tool calls in `try/except Exception: pass` blocks because "we don't want one bad search to crash the whole research run." After three weeks in production, the team notices reports occasionally cite sources that do not exist, and one report claimed comprehensive coverage of a topic when in fact 4 of 7 subagents had silently failed. What pattern is this and how should it be fixed?

- **A)** The subagents need higher timeout values so fewer exceptions occur.
- **B)** The lead agent should run a self-review pass after synthesis to catch any inconsistencies.
- **C)** Silent error suppression is an anti-pattern; subagents should propagate structured error context (failure type, attempted operation, partial results) and the lead agent should annotate the final report with coverage information distinguishing well-supported findings from gap areas.
- **D)** Switch to a single-agent architecture so there are no subagent failures to suppress.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Silently suppressing errors makes failures invisible to the orchestrator and to users, producing reports that overstate coverage. The correct pattern combines structured error propagation with explicit coverage annotations on the final report, so users see what was researched well, what was attempted but failed, and what remains a gap.

**Why A is Wrong:** Longer timeouts reduce one failure mode but do not address the structural defect of suppressing whatever errors do occur.
**Why B is Wrong:** Self-review by the same model that produced the synthesis is unreliable and cannot detect missing data — the model has no way to know what 4 failed subagents would have found.
**Why D is Wrong:** Removing parallelism trades throughput and quality for an avoidable problem. Subagent architectures are correct; suppressing their errors is the defect.

**Pattern/Trap:** P19 Self-Review Limitation

</details>

---

**Q217.** A developer is using Claude Code to refactor a 180-file Java service. Around the 90-minute mark, Claude begins giving inconsistent answers about which classes implement a given interface, sometimes referencing "typical Spring patterns" rather than the specific classes it had identified earlier. The developer's first instinct is to upgrade to a model with a 1M-token context window. What is the better remediation?

- **A)** Restart the session from scratch and re-explore the codebase, since context-window upgrades only delay the problem.
- **B)** Maintain a scratchpad file (e.g., `claude-progress.md`) that records key findings — interface implementers, file paths, conventions discovered — and have Claude reference it for subsequent questions, optionally using `/compact` with custom instructions to preserve those findings.
- **C)** Increase the temperature so the model relies less on memorized patterns and more on the codebase.
- **D)** Have the developer manually re-paste the full file list at the start of every prompt.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** Context degradation in long Claude Code sessions ("context rot") is structural — recall decreases as token count grows even within a window's limits. Persisting key findings to a scratchpad file that survives compactions, and using `/compact` with custom instructions to preserve specific facts, addresses the root cause regardless of window size.

**Why A is Wrong:** A blank restart loses all prior exploration work. A scratchpad allows resuming with the high-signal findings already captured, which is far more efficient.
**Why C is Wrong:** Temperature does not control reliance on memorized patterns versus context. The model defaulted to "typical patterns" because specific findings degraded, not because of sampling stochasticity.
**Why D is Wrong:** Manual re-pasting reintroduces the same volume of low-signal tokens that caused degradation. The fix is condensing key findings, not re-injecting raw content.

**Pattern/Trap:** P8 Larger Context Window Fallacy

</details>

---

**Q218.** During a 4-hour Claude Code session migrating a database schema, the IDE crashes and the session is lost. The developer had been tracking progress informally in chat. To make future crashes recoverable, which design is best?

- **A)** Periodically have Claude write a structured state manifest (completed steps, pending steps, modified files, commands run, key decisions, unresolved questions) to a project file; on resume, start a fresh session and have Claude load the manifest as its first action.
- **B)** Disable auto-save in the IDE so partial state is never persisted in a corrupted form.
- **C)** Keep one extremely long session open indefinitely and never close the IDE, treating session continuity as the recovery strategy.
- **D)** On crash, attempt to restore the previous session's exact context window from disk cache and resume mid-thought.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Crash recovery for long agent sessions is best implemented as structured state export — a manifest the agent can read into a fresh session to bootstrap. This is more robust than session restoration because manifests are smaller, human-readable, and not subject to corruption of token-level state.

**Why B is Wrong:** Disabling auto-save addresses one symptom and prevents the manifest pattern itself, since the manifest needs to be persisted regularly.
**Why C is Wrong:** Indefinite sessions accumulate context degradation and are still vulnerable to crashes. Session continuity is not a recovery strategy; it is the absence of one.
**Why D is Wrong:** Restoring exact context window state is fragile and ties recovery to internal model state that may not be portable across versions. Manifests are the durable abstraction.

**Pattern/Trap:** P18 Fresh Session vs Resume

</details>

---

**Q219.** A Claude Code agent is asked to "find all callers of `processPayment` and assess whether each handles the new `RetryableException`." Naive execution would have the main agent grep, open dozens of files, read each, and accumulate ~60K tokens of source code in its context before any analysis. Which approach best preserves the main agent's context for the higher-level decision?

- **A)** Run the entire exploration in the main agent but ask it to be terse in its narration.
- **B)** Use prompt caching on the file reads so the tokens cost less and become acceptable.
- **C)** Spawn a subagent for the exploration phase whose sole task is to grep, read, and return a structured list of `{file, line, handles_retryable: bool, evidence}`; the main agent receives only that summary, not the raw file contents.
- **D)** Read all files into the main context first, then ask the agent to summarize them in place to free up tokens.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Subagent delegation is Anthropic's core pattern for context isolation: the subagent burns its own context window on verbose exploration and returns a compact, structured result. The main agent's context stays focused on coordination and higher-level reasoning.

**Why A is Wrong:** Terseness in narration does not reduce the tokens consumed by file reads themselves — those still enter context. The structural problem is unaddressed.
**Why B is Wrong:** Prompt caching reduces cost and latency on repeat reads but does not reduce the in-context token footprint. The main agent still pays the attention cost on cached tokens.
**Why D is Wrong:** In-context summarization happens after the tokens have already been read, and the summarization step itself can drop critical evidence. Avoiding the bloat at all (via subagent isolation) is strictly better.

**Pattern/Trap:** P3 Over-Engineering Distractor

</details>

---

**Q220.** A developer's Claude Code session is approaching the auto-compaction threshold. They are mid-way through implementing API changes and want to ensure the compaction preserves the specific endpoints modified, the new request schemas, and the open TODO items, while it is acceptable to discard exploratory tangents and earlier discussion of unrelated files. What is the best action?

- **A)** Run `/clear` to fully reset the context and re-explain the task from memory.
- **B)** Wait for auto-compaction to trigger with default behavior, since auto-compaction is generally well-tuned.
- **C)** Run `/compact Focus on the API endpoints modified, new request schemas, and remaining TODO items` before auto-compaction triggers.
- **D)** Switch to a fresh session and copy the relevant parts manually from the prior session into the new one.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** `/compact` accepts custom instructions that direct the summarizer toward the specific facts the developer needs preserved. Running it proactively — before auto-compaction's default behavior fires — guarantees the right details survive while exploratory content is discarded.

**Why A is Wrong:** `/clear` discards everything, including the API changes still in flight. It is appropriate between unrelated tasks, not mid-implementation.
**Why B is Wrong:** Default auto-compaction may discard endpoint-specific details since it has no signal that those particular facts matter more than others. Custom instructions are the available control.
**Why D is Wrong:** Manual copy-paste is brittle and time-consuming, and it often misses dependencies (helper functions, decisions). The platform offers `/compact` precisely so this manual work is not necessary.

**Pattern/Trap:** P16 Progressive Summarization Risk

</details>

---

**Q221.** An invoice-extraction system reports 97% overall accuracy on a held-out validation set of 10,000 invoices. The product team is satisfied. A customer using the system for international suppliers later reports widespread errors on VAT-line extraction. Investigation reveals: the validation set was 92% domestic invoices (where accuracy is 98.5%), 8% international (where accuracy on the VAT field is 71%). What measurement change is needed?

- **A)** Increase the validation set size from 10,000 to 50,000 to make the aggregate metric more reliable.
- **B)** Stratify accuracy measurement by document type (domestic vs international, plus other meaningful segments) and by field, with stratum sample sizes large enough to detect failure modes; route the field-level metrics — not the aggregate — to the production dashboard.
- **C)** Replace the aggregate accuracy metric with a single F1 score, which handles imbalanced classes better.
- **D)** Continue using aggregate accuracy but add a customer-feedback channel to surface field-level issues retroactively.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** A 97% aggregate metric masked a 71% failure rate on a specific field within a specific document subtype. Aggregate metrics weighted by population frequency systematically hide poor performance on minority segments. Stratified measurement — by document type and by field — surfaces these failure modes before customers do.

**Why A is Wrong:** Larger samples make the aggregate more precise, not more informative. A 50,000-invoice aggregate of 97% will still hide the 71% international VAT subgroup.
**Why C is Wrong:** F1 addresses class imbalance in a single classification task; it does not address segment-level differences across document types and field types.
**Why D is Wrong:** Customer feedback is a slow, lagging signal that surfaces failures only after revenue impact. Stratified offline measurement should detect them before deployment.

**Pattern/Trap:** P12 Aggregate Metric Masking

</details>

---

**Q222.** A team monitors extraction error rates in production by reviewing a sample of outputs every week. They currently sample 200 random outputs uniformly. The volume is dominated by one document type (85%), and rare document types are almost never sampled — but rare types are where novel errors typically appear first. What sampling change best supports both error-rate measurement and novel-pattern detection?

- **A)** Use stratified random sampling across document types, with each stratum sampled in proportion that ensures statistical power for that stratum (often oversampling rare types relative to their natural frequency, then reweighting for the global error-rate estimate).
- **B)** Increase the uniform sample to 2,000 per week so rare types are sampled by chance.
- **C)** Switch to sampling only the rarest document types, since common types are well understood.
- **D)** Have Claude self-flag outputs it is uncertain about and review only those.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Stratified sampling with per-stratum allocation ensures that every meaningful document segment receives enough samples to compute a reliable per-stratum error rate and to surface novel failure patterns. Reweighting by stratum frequency then recovers an unbiased global estimate.

**Why B is Wrong:** Even at 2,000 samples, a document type at 0.5% frequency would only contribute ~10 samples — too few for reliable per-stratum estimates and still likely to miss novel patterns.
**Why C is Wrong:** Sampling only rare types loses error-rate visibility on the common types that drive most volume and revenue. Both ends matter; stratification covers both.
**Why D is Wrong:** Self-flagged uncertainty is an unreliable proxy — models are often confidently wrong on novel patterns precisely because the model has no internal signal that the pattern is novel.

**Pattern/Trap:** P12 Aggregate Metric Masking; P4 Sentiment/Confidence Trap

</details>

---

**Q223.** An extraction pipeline outputs values for 12 fields per document. Stakeholders need a human review workflow that catches likely errors without reviewing every document. The team has labeled validation data per field and observes that field-level confidence scores from the model, after calibration on the validation set, correlate well with field-level error rates. What is the right human-review design?

- **A)** Send every document to human review, since extraction is too important to trust.
- **B)** Send a fixed 10% of documents to human review, randomly sampled.
- **C)** Send documents whose overall (document-level) confidence score falls below 0.85 to review.
- **D)** Compute calibrated confidence per field; route any extraction to review if any field falls below its field-specific threshold or if multiple sources within the document contradict each other; document-level confidence is not used as the routing signal.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Field-level confidence calibrated against labeled data lets thresholds be set per field according to that field's risk profile. Document-level scores average over fields and mask one bad field among eleven good ones — the same masking pathology as aggregate accuracy. Adding contradiction detection catches errors confidence alone misses.

**Why A is Wrong:** 100% review eliminates the value of automation. The point is to spend human attention where it provides the most marginal value.
**Why B is Wrong:** Random sampling treats every document equally regardless of likely error, missing the bulk of high-risk extractions while wasting reviewer time on obvious low-risk ones.
**Why C is Wrong:** Document-level confidence at 0.85 hides field-specific risk. A document where 11 fields are highly confident and 1 critical field is uncertain may still score above 0.85 overall, escaping review.

**Pattern/Trap:** P12 Aggregate Metric Masking

</details>

---

**Q224.** A multi-agent research system synthesizes findings from five subagents into a final report. Each subagent currently returns a free-text prose summary. The final report frequently states claims without traceable sources, and post-hoc citation attempts often hallucinate URLs. What change to subagent output most directly preserves provenance through synthesis?

- **A)** Add a final "citation agent" that reads the report and re-derives citations from web search.
- **B)** Have each subagent return a free-text summary plus a list of URLs it consulted, appended at the end.
- **C)** Have each subagent return structured `claim → source` mappings (claim text, source URL, document name, supporting excerpt) that are preserved through the synthesis prompt and rendered into citations in the final report.
- **D)** Have the lead agent ask the user to verify each claim manually after the report is produced.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Provenance is preserved by carrying claim-source bindings as structured data through every stage, not by attempting to recover them after synthesis. When each subagent returns explicit `(claim, source, excerpt)` tuples and the synthesis prompt is designed to retain those bindings, the final report can render grounded citations.

**Why A is Wrong:** Post-hoc citation re-derivation is exactly what produces hallucinated URLs — the citation agent has no ground truth for which source actually supported a claim and must guess.
**Why B is Wrong:** A bare URL list at the end of a prose summary loses the binding between specific claims and specific sources. The synthesizer cannot tell which URL backs which sentence.
**Why D is Wrong:** Pushing verification to the user destroys the value of the system and does not address the architectural defect; provenance should be machine-tracked.

**Pattern/Trap:** P10 Root Cause vs Symptom

</details>

---

**Q225.** Two subagents return conflicting statistics on the same question: the World Bank reports 7.2% for 2023, the IMF reports 6.8% for 2023. The synthesis prompt is currently told to "produce a coherent answer." The final report quotes "approximately 7%" without attribution to either source. A reviewer flags this as misleading. What is the right pattern?

- **A)** Have the synthesis prompt pick the source with higher historical accuracy and quote only that figure.
- **B)** Drop both figures from the report and replace with a qualitative phrase like "around 7%."
- **C)** Average the two figures and present the mean as the consensus value.
- **D)** Annotate the conflict explicitly in the final report ("World Bank reports 7.2%; IMF reports 6.8%; sources differ on methodology") and surface the divergence to the reader rather than collapsing it into a midpoint.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Conflicting credible sources on the same quantity reflect real uncertainty — often methodological — that the user needs visibility into. Annotating the conflict with attribution preserves the information that two reputable bodies disagree, which is itself a finding. Arbitrary selection, averaging, or qualitative softening all fabricate a false consensus and erase real epistemic signal.

**Why A is Wrong:** "Higher historical accuracy" is rarely available, often domain-dependent, and silently picks one number over another without showing the user the disagreement exists.
**Why C is Wrong:** Averaging two methodologically different estimates produces a number neither source endorses and obscures the disagreement. It manufactures false precision.
**Why B is Wrong:** Replacing a precise but contested figure with a vague qualitative phrase reduces information content without resolving the conflict, and still hides the divergence from the reader.

**Pattern/Trap:** P9 Consensus Review Fallacy

</details>

---

**Q226.** A research synthesis report flags a "contradiction" between two sources: Source X says "smartphone penetration is 78%" and Source Y says "smartphone penetration is 91%." Investigation shows Source X is from 2019 and Source Y is from 2024 — both correct for their time. The system has no awareness of this. What design change prevents this misinterpretation?

- **A)** Require each subagent's structured output to include `publication_date` and `data_collection_date` per claim, and instruct the synthesis prompt to treat differing temporal coverage as different facts rather than as contradictions.
- **B)** Drop the older source whenever two sources disagree numerically, since the newer is presumed correct.
- **C)** Add a disclaimer at the top of every report stating that all figures may be outdated.
- **D)** Have the synthesis model use its training-data knowledge of typical timeframes to guess which source is more recent.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Temporal metadata is critical for synthesis: two figures from different years are not in contradiction — they describe different points in time. Requiring publication and data-collection dates as structured fields on every claim lets the synthesizer represent "78% in 2019, 91% in 2024" as a time series rather than as a conflict.

**Why B is Wrong:** Dropping the older source loses historical trend information and makes assumptions ("newer is correct") that are not always true.
**Why C is Wrong:** A blanket disclaimer does not help the user reason about specific figures and does not prevent the system from labeling time-shifted measurements as contradictions.
**Why D is Wrong:** Guessing dates from training-data priors is unreliable and can be confidently wrong. Dates are observable metadata that should be captured at extraction, not inferred at synthesis.

**Pattern/Trap:** P10 Root Cause vs Symptom

</details>

---

**Q227.** A reporting system aggregates three content types into a single output: financial figures (12 metrics across 4 quarters), news developments (7 narrative items), and technical specifications (a list of 15 named parameters). The current implementation renders all three as flowing prose, and users complain that financial comparisons are hard to follow and technical specs are easy to misread. What is the best fix?

- **A)** Render everything as a single flat bulleted list with one bullet per item.
- **B)** Apply heavier prose with more transition sentences so the financial and technical sections feel less abrupt.
- **C)** Use a single Markdown table for the entire report with three columns (financial / news / technical).
- **D)** Render each content type in the structure that fits it: financial figures as a table (quarters as columns, metrics as rows), news developments as prose paragraphs, and technical specifications as a structured list with parameter names bolded.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Different content types have different optimal renderings: tabular data is read best as tables, narrative news is read best as prose, and named-parameter lists are read best as structured lists. Content-type-appropriate rendering is a final-stage formatting decision driven by the data, not a single uniform style.

**Why A is Wrong:** Flat bullets destroy the row/column structure of financial data and the narrative flow of news. Uniform rendering is what the question is critiquing, not solving.
**Why B is Wrong:** Heavier prose worsens the financial-comparison problem (numbers get harder to scan when buried in sentences) and adds noise to technical specs.
**Why C is Wrong:** A three-column shared table forces incompatible content types into the same grid; news paragraphs do not align row-wise with financial metrics or technical parameters.

**Pattern/Trap:** P3 Over-Engineering Distractor

</details>

---
