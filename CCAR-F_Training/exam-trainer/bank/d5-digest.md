# Domain 5: Context Management and Reliability (15%), grounding digest

Domain 5 tests telling apart failures that look alike from outside, and fixing the cause rather than the symptom. The trap is usually a global fix: a bigger window, a retry, a higher threshold, more sources. When two designs are equally reliable, the credited answer spends fewer tokens, review hours, or round trips.

## 5.1 Preserving critical information in long interactions
- **Facts.** The API is stateless: the whole context is re-read every turn. Everything counts against it: system prompt, messages, tool results, tool definitions, thinking. Quality degrades silently as the window fills.
- **Correct.**
  - Keep a compact **case-facts block** (IDs, amounts, dates, policy thresholds) pinned at the top and refreshed each turn. It holds tool-verified values only, never customer claims.
  - Trim verbose tool output *before* it piles up, with a post-tool hook, and keep a **path to the raw output**.
  - Layout: facts at the top, trimmed results in the middle, a one-line constraint recap plus the question last. Middle material is used least reliably ("lost in the middle", a tendency).
- **Pick the strategy.** Trim bulky output. Summarize when the reasoning path matters. Save to disk anything that must stay word-for-word. Start a **fresh session with a handoff brief** when the phase changed or the history is more contradiction than context. Anything missing from the brief is lost, and prior findings go in as hypotheses.
- **Wrong.** A bigger window. More output tokens. Trusting summaries or compaction to keep numbers, which degrade first. Clearing with no record. Raising the compaction trigger or disabling compaction. Putting documents after the question.
- **Words that flip the answer.** "auditable later" means a raw-output path. "tool corrected the customer" means verified-only facts. "keeps reverting" means a fresh brief.

## 5.2 Escalation and ambiguity
- **Valid triggers** are checkable:
  - An **explicit request for a human**: escalate at once, with no attempt to resolve, no asking why, no portal.
  - A **policy gap**: no rule matches, or the playbooks conflict.
  - **Genuinely stuck** after reasonable attempts.
  - The hard tier: safety or legal risk, irreversible or money-moving actions.
  - Evaluate in order, take the first match, and record the rule ID.
- **Invalid triggers.** Sentiment alone, complexity alone, self-reported confidence, "escalate if unsure", quotas. Over-escalation leads reviewers to rubber-stamp.
- **Ambiguity.** If exactly one required field is missing and the customer can supply it, ask **one** question, then re-evaluate. A second ambiguity escalates. Never guess and never interrogate. If the ambiguity is in the *policy*, don't ask the customer: **abstain** as `policy_gap`, attach the playbooks, and review weekly. Send no holding reply implying resolution. Resolve covered cases even if the customer is angry.

## 5.3 Error propagation
- **Correct.** Subagents return structured results, never prose:
  - `status: partial`, what completed, and `failures`, each with unit, `error_class`, `error_code`, `retryable`, `retry_would_help_if`, attempts, and evidence.
  - Coverage counts, plus a `claim_scope` saying unexamined units are not clean.
  - Reuse the tool layer's transient/business/permission values, with detail in `error_code`.
  - Make failure distinguishable from an empty result (`is_error`).
- **Routing.** Transient: bounded retry. Business: change plan. Permission: escalate. Non-retryable is never retried. Keep partial results.
- **Coordinator.** Carry the gap into **human-facing** output: "11 of 13, these two unexamined". Stopping short is laundering.
- **Wrong.** Empty results reported as success. Retrying a 403. A higher retry cap. A confidence downgrade instead of naming the gap. The coordinator redoing subagent work. Per-agent error labels.

## 5.4 Large codebase exploration
- **Correct.**
  - Search first (paths and line numbers), read matched ranges only, follow one level of callers.
  - Keep identifiers in context, not file bodies (just-in-time retrieval). The reference map shows the blast radius.
  - Delegate wide sweeps to a subagent or forked skill whose context is discarded.
  - The **return contract** matters most: files, line ranges, finding, catching test, what was unexamined.
- **Wrong.** Reading whole files or directories. Preloading by recency. Concatenating the repo. Moving files after the question. Batches that can't see each other. "Looks mostly fine" returns. The coordinator re-reading. A bigger subagent model.

## 5.5 Human review and calibration
- **Facts.** Stated confidence is a claim until measured:
  - Calibrate on a **labelled sample**: accuracy per confidence bucket, **per document type**.
  - Set thresholds to a **stated target error rate**, and re-measure when inputs change.
  - The mapping is usually monotonic but compressed, and differs by type.
  - **Segment** accuracy with volumes, because an aggregate hides a failing low-volume type.
- **Designs.**
  - Review everything when regulated, new, or unlabelled; this also builds the labels.
  - Stratified sampling audits items the threshold passed. It detects stale thresholds and fits a fixed capacity.
  - Calibrated thresholds gate individual items.
  - Run all three, with a feedback loop.
- **Wrong.** Intuitive thresholds. Aggregate accuracy. A higher global threshold. Average stated confidence as the error rate. Self-justification. Agreement among runs (shared blind spots agree). Sampling alone for regulated output.

## 5.6 Provenance and multi-source uncertainty
- **The four parts.** Claim-to-source mapping (claims and sources arrays sharing `source_id`, with quote and locator, not a bibliography). Temporal handling (`retrieved_at` plus effective date). Conflict annotation. Coverage gaps.
- **Rule.** A step that consumes structured findings and outputs only prose breaks the chain, so render prose from the arrays. Conflicts with no tie-breaker give both claims, a conflict object, `conflicted_unresolved`, and the named human decision, escalated to the coordinator.
- **Platform.** Citations on documents return `cited_text` plus a page or character location. Tool results need your own provenance record.
- **Wrong.** Newest source wins. Majority vote. Averaging. Confidence instead of sources. "According to sources" wording.
