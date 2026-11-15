# Domain 4: Prompt Engineering & Structured Outputs

> Claude Certified Architect – Foundations

> Exam Weight: 20% | Questions in Pool: 46

*Generated from the JSONL bank by `scripts/render_markdown.py` — do not edit by hand.*
*Private study material, assembled from mixed sources: not licensed for redistribution.*

---

**Q11.** Your team wants to reduce API costs. Two workflows: (1) a blocking pre-merge check that must complete before developers can merge, and (2) a technical debt report generated overnight for review the next morning. Your manager proposes switching both to the Message Batches API for 50% cost savings. How should you evaluate this proposal?

- **A)** Use batch processing for the technical debt reports only; keep real-time calls for pre-merge checks.
- **B)** Switch both workflows to batch processing with status polling to check for completion.
- **C)** Keep real-time calls for both workflows to avoid batch result ordering issues.
- **D)** Switch both to batch processing with a timeout fallback to real-time if batches take too long.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

The Message Batches API has up to 24-hour processing times with no guaranteed latency SLA. This makes it unsuitable for blocking pre-merge checks but ideal for overnight batch jobs. Option B is wrong because relying on "often faster" completion isn't acceptable for blocking workflows. Option C reflects a misconception: batch results can be correlated using `custom_id` fields.

</details>

---

**Q12.** A pull request modifies 14 files across the stock tracking module. Your single-pass review produces inconsistent results: detailed feedback for some files, superficial comments for others, obvious bugs missed, and contradictory feedback. How should you restructure the review?

- **A)** Split into focused passes: analyze each file individually for local issues, then run a separate integration-focused pass examining cross-file data flow.
- **B)** Require developers to split large PRs into smaller submissions of 3-4 files before the automated review runs.
- **C)** Switch to a higher-tier model with a larger context window to give all 14 files adequate attention in one pass.
- **D)** Run three independent review passes on the full PR and only flag issues that appear in at least two of the three runs.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Splitting reviews into focused passes directly addresses attention dilution. Option B shifts burden to developers without improving the system. Option C misunderstands that larger context windows don't solve attention quality issues. Option D would suppress detection of real bugs by requiring consensus on issues that may only be caught intermittently.

</details>

---

**Q55.** A CI code review prompt flags 60% of pull requests for "potential security vulnerabilities." Developers have stopped reading the reports because nearly all flags are false positives on standard input validation patterns they consider acceptable. Adding "only report high-confidence findings" to the prompt has had no measurable effect. What is the most effective next step?

- **A)** Replace the security review prompt with a rule-based static analysis tool that has zero false positives.
- **B)** Temporarily disable the security category and add explicit criteria defining which patterns constitute a reportable vulnerability versus acceptable practice, with concrete code examples for each.
- **C)** Increase the review model to a larger tier to improve its judgment on security issues.
- **D)** Add a post-processing confidence threshold: discard any finding where Claude rates its own confidence below 80%.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

General instructions like "only report high-confidence findings" fail to reduce false positives because they do not define what counts as a positive. Temporarily disabling the noisy category restores developer trust immediately while explicit criteria with examples give Claude the specificity needed to distinguish real issues from acceptable patterns. Option A abandons the AI-based review entirely rather than fixing it. Option C is unlikely to change false positive rates when the root cause is imprecise criteria. Option D relies on self-reported confidence scores, which are poorly calibrated for LLMs.

</details>

---

**Q56.** A Claude-based pull request reviewer raises "magic number" warnings on every numeric literal in the codebase, including well-understood constants like HTTP status codes and standard buffer sizes. Developers want magic numbers flagged only when they appear in business logic with no explanation. How should the prompt be updated?

- **A)** Add an instruction to "use good judgment about whether numbers are truly magic numbers."
- **B)** Add a severity field to findings and instruct Claude to omit any finding with severity "low."
- **C)** Define explicit criteria: flag numeric literals that appear in business logic calculations with no accompanying comment or named constant; exclude HTTP status codes, standard buffer sizes, and any value documented in a comment.
- **D)** Provide a list of allowed numeric values that should never be flagged.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Explicit, specific criteria that define what to report and what to exclude are far more effective than general guidance or exclusion lists. Describing the precise conditions that make a number "magic" gives Claude a clear decision rule rather than requiring inference. Option A is the kind of vague instruction that causes the problem in the first place. Option B introduces a severity layer that does not address the underlying definitional problem. Option D would require maintaining an incomplete and fragile list that does not generalize to new values.

</details>

---

**Q57.** A Claude-based code reviewer is generating inconsistent feedback on documentation quality: sometimes flagging missing docstrings for private helper functions, sometimes not; sometimes requiring full parameter descriptions, sometimes accepting one-line summaries. The team wants consistent, predictable documentation feedback on public API functions only. Which change most directly addresses the inconsistency?

- **A)** Instruct Claude to "apply documentation standards consistently and carefully."
- **B)** Define explicit documentation criteria: public API functions must have a docstring with a one-sentence summary, parameter descriptions, and return value description; private functions are excluded from documentation checks.
- **C)** Run three parallel review instances and accept feedback that appears in at least two of the three.
- **D)** Restrict the review prompt to only one concern at a time, alternating between security, documentation, and style in separate runs.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Explicit criteria that specify exactly what is required, for which functions, and at what level of detail eliminate the ambiguity that causes inconsistency. Without a clear definition of "documented," Claude must infer the threshold each time, leading to variable results. Option A is the type of general instruction that already produces the problem. Option C adds overhead and suppresses legitimate feedback that may only appear in one instance. Option D separates concerns but does not fix the definition of what counts as adequate documentation.

</details>

---

**Q58.** A team uses Claude to generate code review comments for pull requests. The comments are technically accurate but vary widely in format: some include file paths and line numbers, others are vague summaries, some use bullet points, and others write prose paragraphs. Developers want a consistent, actionable format: file path, line number, issue description, suggested fix. What is the most effective way to achieve this?

- **A)** Add a format specification to the system prompt listing the required fields.
- **B)** Provide 2-4 few-shot examples in the prompt showing the exact desired output format for different types of issues, including file path, line number, issue description, and suggested fix.
- **C)** Use `--output-format json` and parse the results in a post-processing step to normalize format.
- **D)** Ask Claude to self-review its output and reformat any comment that does not match the required structure.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Few-shot examples demonstrating the exact desired output format are the most effective technique for achieving consistently formatted output when detailed instructions alone produce inconsistent results. Seeing concrete examples of the format makes the requirement unambiguous. Option A is a format specification that has likely already been tried given the problem description. Option C introduces parsing complexity and does not ensure consistent generation. Option D adds a round-trip that may still produce inconsistent intermediate output.

</details>

---

**Q59.** A structured data extraction system is extracting contract clauses from legal documents. The model handles standard clauses well but consistently misclassifies ambiguous clauses that could fit two or more categories, such as a clause that contains both termination conditions and force majeure language. What few-shot prompting approach is most effective for improving accuracy on these edge cases?

- **A)** Add more few-shot examples of standard, unambiguous clauses to reinforce the classification schema overall.
- **B)** Add a confidence score field and route all low-confidence classifications to human review without attempting to improve the model's judgment.
- **C)** Switch from classification to extraction: ask Claude to extract the clause text without categorizing it, then apply a rule-based classifier.
- **D)** Create targeted few-shot examples that specifically demonstrate ambiguous-case handling: showing the reasoning for why a clause with both termination and force majeure language belongs to one category and not the other.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

Targeted few-shot examples for ambiguous scenarios that show the reasoning behind the classification decision are the most effective technique for improving handling of edge cases. Standard examples do not teach the model how to handle cases that span category boundaries. Option A reinforces behavior that already works rather than addressing the gap. Option C sidesteps the classification problem rather than solving it. Option B is a reasonable operational safeguard but does not improve model accuracy.

</details>

---

**Q60.** A document extraction system uses Claude to pull financial figures from quarterly earnings reports. The reports have varied formats: some use tables, some use inline prose, some use both. Extraction accuracy for tabular data is high (94%) but prose-only documents show only 72% accuracy. What is the most targeted approach to improve prose extraction accuracy?

- **A)** Increase the system prompt's emphasis on accuracy with stronger language and more detailed instructions.
- **B)** Add few-shot examples specifically showing correct extraction from prose-formatted documents, including cases where numbers appear in sentence form rather than tables.
- **C)** Pre-process all documents to convert prose financial data into table format before sending to Claude.
- **D)** Use a separate prompt for prose documents that instructs Claude to first identify all sentences containing numbers, then extract figures from those sentences only.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Few-shot examples demonstrating correct extraction from documents with varied formats directly address the accuracy gap on prose documents. The model already generalizes well to tabular data; the gap is in prose, and targeted examples for that format close the gap most efficiently. Option A relies on emphasis, which does not resolve structural pattern differences. Option C requires reliable pre-processing of arbitrarily structured prose, which is non-trivial. Option D adds complexity and may miss numbers that are discussed without appearing in sentences Claude isolates.

</details>

---

**Q61.** Your extraction pipeline uses a prompt that requests JSON output with a code block. In production, approximately 3% of responses have JSON syntax errors: missing commas, unescaped characters, or truncated objects. These errors break your downstream parser and require manual reprocessing. What is the most reliable way to eliminate JSON syntax errors?

- **A)** Add a validation step that re-runs the prompt if the output fails JSON parsing, up to 3 retries.
- **B)** Switch to tool use with a defined JSON schema as the input parameter; extract structured data from the `tool_use` response block.
- **C)** Add an instruction to the prompt: "Your response must be valid JSON. Double-check for syntax errors before responding."
- **D)** Use a regex post-processor to fix the most common syntax errors before passing output to the parser.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Tool use with a JSON schema guarantees schema-compliant structured output by construction, eliminating syntax errors entirely. The model populates the tool call's input parameters according to the schema rather than generating free-text JSON. Option A reduces the frequency of failures but does not eliminate syntax errors. Option C relies on model self-checking, which does not provide the deterministic guarantee that tool use provides. Option D is a fragile workaround that cannot handle all syntax error patterns.

</details>

---

**Q62.** Your structured data extraction pipeline processes invoices. You have two extraction tools: `extract_invoice_schema` and `extract_receipt_schema`. For each document, you do not know in advance which type it is. After switching to `tool_choice: "auto"`, you observe that 30% of the time the model returns a text description of what it found rather than calling either tool. What is the correct fix?

- **A)** Set `tool_choice: "any"` to guarantee the model calls one of the available extraction tools without specifying which one.
- **B)** Set `tool_choice: {"type": "tool", "name": "extract_invoice_schema"}` to always call a specific tool.
- **C)** Add a system prompt instruction: "Always call one of the extraction tools and never return text."
- **D)** Merge both schemas into a single `extract_document_schema` tool with an optional `document_type` field.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

`tool_choice: "any"` guarantees the model calls a tool rather than returning conversational text, without requiring you to specify which tool. This is exactly the documented use case when you have multiple valid tools and want to ensure one is called. Option B forces a specific tool, which defeats the purpose when you do not know the document type in advance. Option C is a prompt-based approach with probabilistic compliance, which already failed as evidenced by the 30% text response rate. Option D is a valid architectural change but requires more engineering effort than a single configuration change.

</details>

---

**Q63.** An invoice extraction pipeline uses tool use with a strict JSON schema. After validation, 8% of extracted invoices fail a business rule check: the sum of line item amounts does not equal the `total_amount` field. These are semantic errors, not schema syntax errors. The invoices are well-formed documents with no missing data. How should you implement the retry loop?

- **A)** Retry up to 3 times with the same prompt; schema-compliant extraction will converge on a valid answer with additional attempts.
- **B)** Add a `calculated_total` field to the schema and populate it with the sum of line items in post-processing, then use the calculated total as the canonical value.
- **C)** Flag all invoices with this error as missing data and route them directly to human review without retry.
- **D)** On failure, append the original document, the failed extraction, and the specific validation error ("line items sum to X but total_amount is Y") to the follow-up prompt for model self-correction.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

Retry-with-error-feedback works by giving the model the specific discrepancy it needs to self-correct. Since the invoices are well-formed and the data is present, the model has the information it needs to fix the arithmetic alignment on retry. Option A retries without feedback and is unlikely to improve results since the model will reproduce the same error. Option C routes to human review prematurely when a retry with feedback could resolve the issue. Option B silently replaces the model's extracted total with a calculated value, which could propagate errors if the line items themselves were extracted incorrectly.

</details>

---

**Q64.** A CI code review pipeline is generating false positive findings at a high rate. The team wants to understand which specific code constructs are being flagged incorrectly so they can refine the prompt. The current findings output only includes `file`, `line`, and `description`. What schema change would best enable systematic false positive analysis?

- **A)** Add a `confidence` field (0-100) to each finding so the team can filter by confidence threshold.
- **B)** Add a `detected_pattern` field to each finding that records the specific code construct or pattern that triggered the finding.
- **C)** Add a `category` field so findings can be grouped by issue type for aggregate analysis.
- **D)** Add an `is_false_positive` boolean field and instruct Claude to self-label its own false positives.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

The `detected_pattern` field directly captures what code construct triggered each finding, enabling the team to identify which patterns produce the most false positives and update prompt criteria accordingly. Option A provides confidence scores but does not identify what prompted the finding. Option C allows grouping but not pattern-level debugging. Option D asks Claude to self-identify its own false positives, which is unreliable since the model cannot accurately distinguish true from false positives without ground truth.

</details>

---

**Q65.** A compliance team runs a weekly audit that analyzes 50,000 contract documents for regulatory clauses. The audit results are reviewed by a compliance analyst every Monday morning. The team is considering the Message Batches API. A colleague raises a concern: "What if a batch fails partway through the 50,000 documents?" How should partial batch failures be handled?

- **A)** Always resubmit the entire batch; tracking partial failures adds implementation complexity.
- **B)** Set a shorter processing window timeout to force faster completion and reduce the risk of partial failures.
- **C)** Use the `custom_id` field to correlate each request with its response, identify which documents returned error responses, and resubmit only those documents in a new batch.
- **D)** Switch to real-time API calls with retry logic; the batch API is not suitable for mission-critical compliance workloads.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

The `custom_id` field is specifically designed for correlating batch request and response pairs, enabling teams to identify which documents failed and resubmit only those, avoiding the cost of reprocessing the entire batch. Option A wastes 50% cost savings by reprocessing successful documents. Option B misunderstands the batch API; processing windows are managed by Anthropic and cannot be shortened on demand. Option D is overly conservative: the batch API is appropriate for non-blocking, latency-tolerant compliance audits, which this workflow is.

</details>

---

**Q66.** A developer generates a 300-line module using Claude Code in one session, then asks the same session to review the code for bugs. The review returns "looks good" with minor style suggestions but misses two logic errors that a colleague catches in manual review. What is the most likely cause, and what architectural change addresses it?

- **A)** The context window was too large; the fix is to limit code generation to smaller chunks so the review has less to process.
- **B)** The reviewing instance retains reasoning context from generation, making it less likely to question its own decisions. Use a second independent Claude instance without the generation context to perform the review.
- **C)** The review prompt was too vague; adding more explicit review criteria to the same session would catch the missed errors.
- **D)** The model tier used for generation is more capable than the one used for review; switching both to the same tier resolves the quality gap.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Self-review limitation is a known pattern: when a model retains the reasoning context from code generation, it is less likely to identify errors in its own output. An independent review instance without the generator's context approaches the code without prior assumptions and catches issues the generating instance would overlook. Option A addresses context length, not reasoning context bias. Option C might improve detection of certain categories of issues but does not address the fundamental self-review limitation. Option D addresses model selection, not the structural problem of reviewing one's own output.

</details>

---

**Q67.** A financial document extraction pipeline is failing on the "guarantor address" field for a set of loan summaries. After 3 retry attempts with error feedback, the field still extracts as null. Each retry prompt includes the original document and the validation error. What should you investigate before scheduling further retries?

- **A)** Increase the retry limit from 3 to 5, since complex field extraction may require more attempts to converge.
- **B)** Check whether the guarantor address is actually present in the loan summary document, or whether the document only references it by directing the reader to an external exhibit.
- **C)** Switch to a larger model tier for the retry attempts, since the current model may lack the reasoning capacity for this field.
- **D)** Restructure the schema to make the guarantor address field optional, allowing the pipeline to proceed when the field cannot be extracted.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Retries are only effective when the information needed to satisfy the validation is present in the document. A loan summary that references guarantor details in an external exhibit does not contain the address. No number of retries will extract information that is not in the input. Before adding retry cycles, validate that the target field is actually present in the source document. Option A adds more retries without diagnosing why the existing retries are failing. Option C may improve performance on difficult extractions but does not address absence of data. Option D removes the validation rather than diagnosing the root cause.

</details>

---

**Q68.** A developer builds a code generation pipeline where Claude generates a 200-line module, and then the same session reviews the generated code for correctness. The review returns only minor style suggestions and misses a logic error in the error handling path. A second developer reviewing the code manually finds the bug immediately. What architectural change would make the review phase more effective?

- **A)** Add more explicit review criteria to the generation session's system prompt to help it catch logic errors.
- **B)** Switch to a larger model tier for the review step to improve reasoning quality.
- **C)** Run the review immediately after generation before any other tool calls accumulate in the context window.
- **D)** Use a second independent Claude instance without the generation context to perform the review, since the generating instance retains reasoning context that makes it less likely to question its own decisions.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

When a model reviews code it generated in the same session, it retains the reasoning context from generation and is less likely to identify errors in its own output. An independent review instance approaches the code without prior assumptions and catches issues the generating instance overlooks. This is the documented rationale for multi-instance review architectures. Option A improves the review prompt but does not address the fundamental self-review limitation. Option C manages context length but does not remove the generator's retained reasoning bias. Option B improves general capability but does not change the structural problem of a model reviewing its own work.

</details>

---

**Q175.** A code-review bot built on Claude Sonnet 4.5 produces ~38% false-positive findings on pull requests. Developers have begun marking the bot's comments as "noise" and ignoring entire review threads. The team's first instinct is to add the line "Be conservative and only flag high-confidence issues" to the system prompt. After deploying that change, the false-positive rate is unchanged but recall on real bugs dropped ~22%. What is the most effective next step?

- **A)** Replace the conservative-tone instruction with an explicit severity rubric defining each level with one-sentence criteria plus 1–2 concrete code examples per level, and an explicit "Do NOT report" exclusion list.
- **B)** Add `temperature=0` and increase `max_tokens` so the model has more room to deliberate before committing to a finding.
- **C)** Route the bot's output through a second Claude instance asked "Is this finding important?" and drop anything it marks unimportant.
- **D)** Switch to Claude Opus 4.5 because larger models are inherently more conservative about flagging issues.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Vague adverbial instructions ("be conservative", "high-confidence") are subjective thresholds the model interprets idiosyncratically. Anthropic's prompt-engineering guidance prescribes replacing such instructions with explicit, observable criteria plus concrete examples — a severity rubric with behavioral definitions and exclusion lists converts subjective judgment into checkable rules.

**Why B is Wrong:** Temperature and token budget do not address criterion ambiguity; the model already finds the issues, the problem is which findings get reported.
**Why C is Wrong:** A second self-review instance with the same vague criterion inherits the same ambiguity and adds latency and cost without fixing the root cause.
**Why D is Wrong:** Larger models are not inherently "more conservative"; they follow vague instructions even more faithfully, often worsening the recall regression.

**Pattern/Trap:** P10 Root Cause vs Symptom; P20 Explicit Escalation Criteria

</details>

---

**Q176.** A medical-records extraction pipeline uses a JSON schema with a required `dosage_mg` field of type `number`. The source documents include free-text notes like "about a teaspoon" or "patient unsure". The model is fabricating numeric values when the dose is non-numeric or missing, producing plausibly wrong outputs that pass schema validation. What is the correct schema-level fix?

- **A)** Add a regex pattern constraint to `dosage_mg` to reject obviously fabricated round numbers like 5 or 10.
- **B)** Move `dosage_mg` out of `required` and add an `extraction_notes` string for the model to explain itself in.
- **C)** Change `dosage_mg` to type `["number", "null"]`, keep it `required`, and add a description: "Return null if no confirmed numeric dose appears in the source. Do not estimate or convert informal measurements."
- **D)** Add a post-validation Python check that re-prompts the model whenever `dosage_mg` looks suspicious.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Anthropic's hallucination-reduction guidance maps to schema design: give the model a structurally honest way to say "I don't know." A nullable-but-required field paired with a description prohibiting estimation is the canonical pattern — the model can return `null` instead of inventing a number.

**Why A is Wrong:** Regex on numbers cannot distinguish a fabricated value from a real one; "5 mg" is a perfectly valid real dose.
**Why B is Wrong:** Optional-and-omitted forces every consumer to handle missing-key vs null-value vs present-value, and `extraction_notes` doesn't suppress fabrication — it just adds a side channel.
**Why D is Wrong:** Post-hoc retries can't conjure information that isn't in the source; this is retry futility bolted onto the wrong layer.

**Pattern/Trap:** P14 Nullable Field Prevention; P1 Prompt vs Programmatic Enforcement

</details>

---

**Q177.** A code-review system flags TODO comments and descriptive comments ("// returns user object") as bugs while routinely missing comments that no longer match the code's behavior (e.g., "// retries 3 times" above a function that retries 5). The team has tried adding "Don't flag harmless comments" to the prompt with no improvement. What is the most reliable fix?

- **A)** Increase the system prompt detail to enumerate every harmless comment style (TODO, FIXME, NOTE, descriptive, license headers, etc.) with negative phrasing.
- **B)** Add 3–4 few-shot examples showing pairs of (acceptable comment → no flag, with reasoning) and (misleading comment → flag, with reasoning), each wrapped in `<example>` tags.
- **C)** Lower `temperature` to 0 so the model is more deterministic in its flagging decisions.
- **D)** Switch the review tool to a tool with `tool_choice: "any"` so the model is forced to produce structured output.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** Anthropic recommends 3–5 diverse few-shot examples specifically for boundary cases where a verbal rule cannot capture the distinction. The (acceptable vs. genuine-issue) pair pattern teaches the model the boundary between near-identical surface forms — this is the canonical fix for false-positive misclassification on subtle semantic categories.

**Why A is Wrong:** Negative enumerations multiply contradictions and Anthropic explicitly recommends "replace don't-do-this with do-this"; the model still cannot distinguish *misleading* from *descriptive* without examples.
**Why C is Wrong:** Determinism doesn't fix a categorization the model cannot make; it just makes the wrong answer reproducible.
**Why D is Wrong:** `tool_choice: "any"` enforces output shape, not classification correctness — a perfectly-shaped wrong answer is still wrong.

**Pattern/Trap:** P1 Prompt vs Programmatic Enforcement; P3 Over-Engineering Distractor

</details>

---

**Q178.** An invoice-extraction service uses a tool with `strict: true` and a JSON schema enforcing `line_items: array`, `subtotal: number`, `tax: number`, `total: number`. Schema validation passes 100% of the time but ~9% of invoices have a `total` that does not equal `sum(line_items.amount) + tax`. The schema enforcement is working correctly. What is the root cause and best mitigation?

- **A)** Strict schemas are misconfigured — add a `multipleOf: 0.01` constraint to all numeric fields.
- **B)** The model is rounding inconsistently — set `temperature=0` and the totals will balance.
- **C)** Strict mode is failing — open a support ticket with Anthropic about constrained-decoding accuracy.
- **D)** Strict mode is working correctly but only eliminates syntax errors, not semantic errors; add a `calculated_total` field the model must compute from line items, then post-validate `calculated_total == subtotal + tax` and retry with the discrepancy as feedback.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Constrained decoding guarantees the output *shape* but not its *meaning*; cross-field arithmetic invariants are out of scope for the schema grammar. Anthropic's documented mitigation is a self-verification idiom: force the model to emit its own re-computed total alongside the stated total so a downstream validator can compare and feed any discrepancy back as a retry.

**Why A is Wrong:** `multipleOf` constrains decimal precision, not arithmetic consistency between fields.
**Why B is Wrong:** Temperature affects sampling variance, not the model's choice of whether to ground numbers in source arithmetic.
**Why C is Wrong:** Anthropic's docs are explicit that strict mode guarantees format adherence, not semantic correctness — there is no bug to file.

**Pattern/Trap:** P1 Prompt vs Programmatic Enforcement; P3 Over-Engineering Distractor

</details>

---

**Q179.** A team needs to extract product attributes from 80,000 supplier PDFs nightly. Their SLA is "results available within 30 hours of file arrival." They currently use the synchronous Messages API at 1× pricing. What batching strategy meets the SLA at minimum cost?

- **A)** Submit one batch of all 80,000 documents per night and rely on the 24-hour processing window.
- **B)** Submit batches every 4 hours, since worst-case latency = 4h queue wait + 24h processing ceiling = 28h ≤ 30h SLA.
- **C)** Submit batches every 6 hours to amortize overhead; 6h + 24h = 30h exactly meets the SLA.
- **D)** Use the synchronous API with parallel workers — Batch API can't meet SLAs under 36h.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** The 24-hour figure is a processing *target/ceiling*, not an SLA, so worst-case end-to-end latency is `submit_interval + 24h`. For a 30h SLA, a 4-hour cadence yields 28h worst case with 2h of headroom for queue depth and operational variance, while still capturing the 50% batch discount.

**Why A is Wrong:** A once-nightly submission gives zero margin: a file arriving 1 minute after submission waits ~24h before its batch starts, then up to 24h to process, blowing the SLA.
**Why C is Wrong:** Exactly hitting the SLA leaves zero headroom for the documented "processing may be slowed based on demand" warning and the no-SLA caveat.
**Why D is Wrong:** Batch easily meets a 30h SLA at half the cost; abandoning batch for synchronous is over-correction.

**Pattern/Trap:** P7 Batch API Latency Trap

</details>

---

**Q180.** A code-review platform runs the same Claude prompt twice on every PR — first to generate findings, then in the same conversation appending "Now critically review your findings and remove any that are incorrect." The team reports that this self-review barely changes the output. Why?

- **A)** The same instance retains the reasoning context, prior assumptions, and biases that produced the original findings — it tends to defend rather than reverse its prior output, so genuine independent review requires a fresh API invocation with no inherited context.
- **B)** Self-review needs `extended thinking` enabled; once thinking blocks are added, the second pass becomes adversarial.
- **C)** Self-review only works after at least 3 turns of conversation history — two turns is not enough for the model to distance itself.
- **D)** The system prompt is missing the `<self_review>` XML tag that Anthropic requires for adversarial evaluation.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** This is the canonical self-review limitation: a model in the same conversation sees its own prior reasoning and is biased toward consistency with it. Independent review requires an independent invocation — fresh context window, no prior assistant turns from the generator — ideally with a different system prompt scoping it to disprove the prior findings.

**Why B is Wrong:** Extended thinking improves single-pass reasoning depth but produces the same biased perspective; it is not a substitute for independent review.
**Why C is Wrong:** There is no turn-count threshold; the bias is structural to context inheritance, not a function of conversation length.
**Why D is Wrong:** No such required tag exists in Anthropic's documentation; the answer fabricates an API contract.

**Pattern/Trap:** P19 Self-Review Limitation; P6 Context Inheritance Misconception

</details>

---

**Q181.** An engineer is designing a tool definition for extracting customer-complaint categories. The current schema has `category: enum["billing", "technical", "account"]`. Customer-success has identified ~6% of complaints don't fit any of these and the model currently misclassifies them into the closest existing value. What's the cleanest schema design?

- **A)** Add 12 more enum values to cover edge cases discovered in production logs.
- **B)** Remove the enum constraint and let the model emit any category string as free text.
- **C)** Add `"other"` to the enum and a sibling field `category_other_detail: ["string", "null"]` with a description: "If category is 'other', describe the actual category in 3–8 words; otherwise null."
- **D)** Keep the current 3-value enum and add a confidence score so downstream logic can route low-confidence cases to humans.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** The "enum + other + detail" pattern preserves the enum's downstream tractability (typed routing, dashboards, aggregation) while giving the model a structurally honest escape valve for novel cases. It eliminates the misclassification-into-nearest-enum failure mode without flattening the entire taxonomy into free text.

**Why A is Wrong:** Expanding the enum to 15 values trades one classification problem for a harder one and still won't cover the long tail.
**Why B is Wrong:** Free text destroys the downstream typed pipeline (routing, aggregation, dashboards) and makes near-duplicate categories proliferate.
**Why D is Wrong:** Confidence scores from LLMs are notoriously poorly calibrated and don't solve the underlying "model has no way to express 'doesn't fit'" problem.

**Pattern/Trap:** P4 Sentiment/Confidence Trap; P14 Nullable Field Prevention

</details>

---

**Q182.** A support agent uses three tools: `get_account_status`, `lookup_billing_history`, and `escalate_to_human`. Logs show that for ambiguous escalation-worthy cases, the model occasionally returns a natural-language reply ("I'd recommend escalating this to a human") instead of calling `escalate_to_human`. The team wants to guarantee a tool call on these cases. Which configuration change is most appropriate?

- **A)** Set `tool_choice: {"type": "tool", "name": "escalate_to_human"}` for all turns to force escalation.
- **B)** Remove the natural-language fallback by setting `max_tokens: 1` so the model can't produce a text reply.
- **C)** Add the line "You MUST call a tool, never reply in text" to the system prompt; `tool_choice` defaults are sufficient.
- **D)** Set `tool_choice: "any"` on the API call, which forces the model to call one of the available tools but lets it choose which.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** `tool_choice: "any"` is exactly the documented option for "model must call a tool but can pick which one" — perfect for cases where the model should always take a structured action but the choice between tools is data-dependent. Forcing a specific tool would route every call to `escalate_to_human`, even when account lookup is the right action.

**Why A is Wrong:** Forcing `escalate_to_human` on every turn would escalate every conversation, including ones where the model should call `get_account_status` first.
**Why C is Wrong:** Prompt-level enforcement of tool use is unreliable; `tool_choice: "auto"` (the default with tools provided) explicitly allows text responses regardless of prompt instructions.
**Why B is Wrong:** `max_tokens: 1` would truncate tool-use blocks too, breaking the API call entirely.

**Pattern/Trap:** P1 Prompt vs Programmatic Enforcement; P15 Configuration Hierarchy

</details>

---

**Q183.** An extraction pipeline retries failed schema validations up to 3 times, appending the validator error to the prompt each retry. Metrics show that 91% of "missing required field" failures retry to success, but 87% of "value not found in source document" failures retry to failure or fabrication. What architectural change is most appropriate?

- **A)** Increase the retry budget to 5 — most failures are recoverable with more attempts.
- **B)** Lower temperature on retries from 0.3 to 0 to make the model more deterministic.
- **C)** Add an extended-thinking step before each retry so the model reasons more carefully.
- **D)** Differentiate transient/format errors (retry with feedback) from data-absence errors (return null and log) — fabrication failures indicate retry futility because the information isn't in the source.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Retries succeed when the model has the information but produced a malformed shape; they are futile when the information is genuinely absent from the source — additional attempts only generate more confidently-wrong fabrications. The correct pattern combines structured error differentiation with nullable schema fields and explicit "return null if absent" instructions.

**Why A is Wrong:** Adding retries to a futile retry loop multiplies cost and latency without raising success rate; the 87% failure rate signals the loop is the wrong tool.
**Why B is Wrong:** Determinism cannot conjure information that isn't in the source — it just locks in one fabrication instead of varying them.
**Why C is Wrong:** Extended thinking improves reasoning over available evidence; it doesn't create evidence the source lacks.

**Pattern/Trap:** P13 Retry Futility; P10 Root Cause vs Symptom

</details>

---

**Q184.** A team's code-review system runs three parallel Claude instances with the same prompt and reports a finding only when ≥2 agents agree. After three months, the false-positive rate has dropped to ~12% but a recurring class of bugs (off-by-one in pagination handlers) is still missed by all three reviewers in 30% of cases. Why is consensus failing here?

- **A)** Three reviewers is too few — five-agent consensus is needed for off-by-one detection.
- **B)** Consensus voting introduces majority bias; the system should use unanimous-only flagging.
- **C)** Identical prompts across instances mean shared training-data priors and identical blind spots produce *correlated* errors, not independent confirmation. The fix is specialized agents with non-overlapping mandates plus a cross-file integration pass.
- **D)** Pagination bugs require domain-specific tools that consensus voting cannot substitute for.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** N-instance unanimous agreement under the same prompt is *correlated* error, not independent confirmation — the instances share the same framing, the same training-data blind spots, and the same priors. Anthropic's Code Review architecture mitigates this with specialized agents (each scoped to a different failure mode) plus a cross-file integration pass.

**Why A is Wrong:** More copies of the same biased reviewer don't add independence; the marginal correlation remains.
**Why B is Wrong:** Tightening to unanimous voting reduces false positives but worsens recall on exactly the case described — all three reviewers share the blind spot.
**Why D is Wrong:** Specialized prompts handle this without external tools; the limitation is prompt diversity, not tool availability.

**Pattern/Trap:** P9 Consensus Review Fallacy; P19 Self-Review Limitation

</details>

---

**Q185.** A team submits a 60,000-document batch at 9 PM. At 6 AM the next morning they discover the prompt referenced the wrong field name (`invoice_total` instead of `total_amount`) and ~40% of outputs will be wrong. The `processing_status` is still `in_progress` with most requests not yet executed. What is the correct operational response?

- **A)** Cancel the batch (since most work is still queued), fix the prompt, and resubmit a new batch with the corrected prompt; the Batches API has no in-flight prompt update endpoint.
- **B)** Let the batch complete, then PATCH the prompt via the batch update endpoint and re-process affected requests.
- **C)** Submit a parallel correction batch with the fixed prompt and merge the results when both finish.
- **D)** Open a support ticket with Anthropic asking them to update the in-flight prompt.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** The Batches API has no PATCH/update endpoint — once submitted, prompts cannot be modified. Cancellation is the correct operational response when most work is still queued; completing 60,000 known-bad outputs and then reprocessing would double cost. The key lesson is that **prompt refinement must happen before batch submission** because async validation gives no mid-flight feedback.

**Why B is Wrong:** No batch update/PATCH endpoint exists in the Anthropic API; this option fabricates a capability that does not exist.
**Why C is Wrong:** Submitting a parallel batch doubles cost and consumes rate-limit capacity for a batch whose results will be discarded.
**Why D is Wrong:** Anthropic Support cannot modify the contents of an in-flight batch — this is a structural API limitation, not a permissions issue.

**Pattern/Trap:** P7 Batch API Latency Trap; P15 Configuration Hierarchy

</details>

---

**Q186.** A research orchestrator dispatches sub-tasks to specialist agents and parses their natural-language responses with regex to populate a planning data structure. Parse failures (~14%) cause cascading task-graph corruption. The team is debating fixes. What is the most reliable approach?

- **A)** Add stricter regex with more fallback patterns to handle the 14% of edge cases.
- **B)** Define each sub-task response as a JSON tool with a typed schema (`findings`, `confidence`, `next_steps`, `unresolved_questions`) and call it with `tool_choice: "any"` so every specialist returns schema-compliant structured output the orchestrator can consume directly.
- **C)** Add a second LLM pass that converts the natural-language response to JSON, with retries on parse failure.
- **D)** Increase the specialist agents' `max_tokens` so their responses are more complete and parseable.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** Tool-use with a JSON schema and `tool_choice: "any"` is Anthropic's most reliable mechanism for guaranteed schema-compliant output — the model is trained on the tool-use contract and the output is constrained at the decoder level. Eliminating the natural-language → regex layer entirely removes the 14% failure mode rather than patching it.

**Why A is Wrong:** Regex fragility against open-ended LLM output is the root cause; more regex compounds the problem.
**Why C is Wrong:** A second LLM pass to convert NL → JSON adds latency, cost, and a new failure mode while not eliminating the original brittleness.
**Why D is Wrong:** Token budget doesn't make natural language deterministically parseable; longer responses can be *less* parseable.

**Pattern/Trap:** P1 Prompt vs Programmatic Enforcement; P5 Tool Description Primacy

</details>

---

**Q187.** A team is designing a tool definition for medical-claim extraction. They've drafted a one-sentence description: "Extracts diagnosis codes from clinical notes." The tool is occasionally called when a billing tool would be correct, and it occasionally fabricates ICD-10 codes for vague symptoms. What is Anthropic's recommended fix?

- **A)** Add few-shot routing examples to the system prompt so the model learns when to call this tool vs. the billing tool.
- **B)** Add a regex post-validator that rejects fabricated ICD-10 codes.
- **C)** Lower temperature to 0 to reduce fabrication.
- **D)** Expand the tool description to 3–4+ sentences covering what the tool does, when it should be used, when it should NOT be used, what each parameter means, and important caveats including "return an empty array if no confirmed diagnosis is documented."

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Anthropic's tool-use best practices state that the **tool description is by far the most important factor** in tool performance — recommended length is at least 3–4 sentences covering purpose, scope, exclusions, parameter semantics, and caveats. The description (not surrounding prompts or routing examples) is what the model uses to disambiguate similar tools and constrain fabrication.

**Why A is Wrong:** Few-shot routing examples paper over a tool-description problem; Anthropic's guidance is to fix descriptions first because examples consume tokens and cannot disambiguate inherently overlapping tools.
**Why B is Wrong:** Post-validation catches malformed codes but cannot tell whether a syntactically valid code was actually documented in the note.
**Why C is Wrong:** Temperature reduces sampling variance, not the model's choice of whether to invent an ICD-10 from vague text.

**Pattern/Trap:** P5 Tool Description Primacy; P3 Over-Engineering Distractor

</details>

---

**Q188.** A code-review architecture analyzes each file in isolation, then aggregates findings. A recent bug — a parameter renamed in one file but still referenced under the old name in three caller files — was missed by every per-file reviewer. Each reviewer's local analysis was correct in isolation. What architectural change closes this gap?

- **A)** Add a "shared blind spot" verification agent whose only job is to check the per-file findings against each other.
- **B)** Increase the per-file reviewers' `max_tokens` so they consider more context.
- **C)** Add a cross-file integration pass: an agent receives the union of related files in its context window and looks for problems visible only across files (renamed parameters, unused arguments, type mismatches between caller and callee).
- **D)** Run five identical reviewers per file and require unanimous agreement before flagging.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Per-file passes find local bugs cheaply and in parallel, but cross-file issues like renamed parameters, type mismatches at call sites, and silent semantic drift are visible **only when multiple files share a context window**. The documented architecture pairs per-file local analysis with a cross-file integration pass.

**Why A is Wrong:** A meta-reviewer of per-file findings still has only the per-file findings as input — it cannot detect issues that no per-file reviewer surfaced.
**Why B is Wrong:** More tokens per file doesn't bring other files into context; the issue is which files are in scope, not how much room each gets.
**Why D is Wrong:** N copies of the same per-file reviewer share the per-file blind spot — consensus on file-local context cannot manifest cross-file information.

**Pattern/Trap:** P9 Consensus Review Fallacy; P17 Lost in the Middle

</details>

---

**Q189.** A pipeline extracts shipment data into a schema with 22 fields. Three fields (`hazmat_class`, `customs_value`, `consignee_tax_id`) are present in only ~30% of source documents. The current schema marks them all `required: true`. The model is fabricating values for these fields when they're absent. What is the best schema redesign?

- **A)** Remove the three sparse fields from `required` and from the schema entirely; consumers can derive them downstream.
- **B)** Add a `missing_fields: array` and require the model to list any field it couldn't extract.
- **C)** Keep them in the schema but remove from `required`, and change types to `["string", "null"]` (or appropriate type union with null), with descriptions instructing the model to return null when not documented and never to infer or estimate.
- **D)** Run extraction twice and accept only fields that match across both runs.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Nullable typing combined with explicit "return null if not documented" descriptions gives the model a structurally honest path for absent data — the field remains documented and consistently shaped for downstream consumers, but the model is no longer cornered into fabrication.

**Why A is Wrong:** Removing the fields entirely loses signal when they *are* present and pushes the absence-handling problem to consumers without solving it.
**Why B is Wrong:** A side-channel `missing_fields` array is unstructured and doesn't prevent fabrication in the primary fields when the model "thinks" it found something.
**Why D is Wrong:** Duplicate extraction doubles cost and latency for a problem the schema can solve cleanly; Best-of-N is a verification pattern, not a replacement for nullable design.

**Pattern/Trap:** P14 Nullable Field Prevention; P13 Retry Futility

</details>

---

**Q190.** A team enables `extended thinking` on a Claude review agent with `tool_choice: {"type": "tool", "name": "submit_review"}` to force structured output. The API call returns an error. What is the correct interpretation?

- **A)** Forced tool selection (`tool_choice: "any"` or `tool_choice: {"type": "tool", ...}`) is incompatible with extended thinking; only `auto` and `none` are supported. Switch to `tool_choice: "auto"` and instruct the model in a user message to call `submit_review`.
- **B)** Extended thinking requires `temperature: 1`; setting it to 0 (the team's default) caused the error.
- **C)** Extended thinking requires the tool name to be prefixed with `thinking_`.
- **D)** The error is a transient API issue — retry with exponential backoff.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Anthropic's documentation explicitly lists this incompatibility: extended thinking works only with `tool_choice: "auto"` and `tool_choice: "none"`. The documented workaround is to use `auto` and place a user-message instruction directing the model to call the desired tool — the model will comply in practice and you retain extended thinking.

**Why B is Wrong:** Temperature requirements for extended thinking concern values, not the choice of `tool_choice` mode; the error here is structural.
**Why C is Wrong:** No naming convention requirement exists in the API; the option is fabricated.
**Why D is Wrong:** This is a deterministic configuration error, not a transient one — retries will fail identically.

**Pattern/Trap:** P15 Configuration Hierarchy; P3 Over-Engineering Distractor

</details>

---

**Q191.** A team is benchmarking three approaches to producing JSON output from Claude for a contract-review tool: (1) prompt-only ("Respond with JSON matching this schema..."), (2) tool use with `strict: true` and `tool_choice: "any"`, (3) tool use with `strict: false`. Schema-validity rates over 10,000 calls are 94.1%, 100%, and 99.4% respectively. The team wants to choose option 1 because it's "simpler". What is the right rebuttal?

- **A)** Prompt-only achieves 94.1% which is sufficient; the 5.9% can be retried.
- **B)** Tool use with `strict: false` at 99.4% is the best balance because strict mode adds latency.
- **C)** Switch to prompt-only with `temperature: 0` — it will reach 100% validity.
- **D)** Tool use with strict schemas + `tool_choice: "any"` is Anthropic's most reliable structured-output mechanism, with constrained decoding mathematically guaranteeing schema compliance; the simplicity argument is false economy because the 5.9% syntactic failure rate creates downstream fragility that exceeds the integration overhead of tool use.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Anthropic explicitly documents tool use with strict schemas as the most reliable approach. Constrained decoding makes syntactic compliance a mathematical guarantee, not a probability — eliminating the entire class of malformed-JSON errors. A 5.9% failure rate at 10,000 calls is 590 broken integrations per run.

**Why A is Wrong:** A 5.9% failure rate at 10,000 calls is 590 broken integrations per run — not a tail-risk to be papered over with retries.
**Why B is Wrong:** Strict mode does not measurably increase latency; the 0.6% gap represents real production failures, and `strict: true` is the recommended default.
**Why C is Wrong:** `temperature: 0` reduces variance but does not guarantee schema compliance — that requires constrained decoding, which only the tool-use path provides.

**Pattern/Trap:** P1 Prompt vs Programmatic Enforcement; P12 Aggregate Metric Masking

</details>

---

**Q192.** A team's PR-review system is showing a pattern: on long PRs (>800 lines changed), the model frequently dismisses real issues in the *middle* of the diff as "intentional" while flagging issues at the start and end accurately. They've tried adding "review every line equally carefully" to the prompt with no effect. What is the most effective architectural fix?

- **A)** Add a `detected_pattern` field to the output schema for the model to self-report dismissal patterns.
- **B)** Increase `max_tokens` so the model has more room to discuss middle-of-diff issues.
- **C)** Split long diffs into smaller chunks (per-file or per-hunk) reviewed by independent per-file agents, then a cross-file integration pass — addressing the lost-in-the-middle effect through architecture rather than prompt instructions.
- **D)** Switch to a model with a larger context window and include the entire repository.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Lost-in-the-middle is a documented attention-distribution effect that prompt instructions cannot reliably correct; the architectural remedy is to keep each pass's scope small enough that no content lands in the under-attended middle. Independent per-file agents plus a cross-file integration pass is Anthropic's documented pattern for exactly this regime.

**Why A is Wrong:** A `detected_pattern` field is a useful logging idiom for offline analysis but doesn't change the within-call attention distribution that caused the dismissals.
**Why B is Wrong:** More output tokens don't redistribute input attention; the bias is in how the model attends to the input, not how much output it can produce.
**Why D is Wrong:** Larger context windows make the lost-in-the-middle effect *worse*, not better, by enlarging the under-attended region.

**Pattern/Trap:** P17 Lost in the Middle; P8 Larger Context Window Fallacy

</details>

---

**Q193.** A team wants to extract structured data from documents and is debating between (a) prompt-only with `"Respond in JSON"`, (b) tool use with `tool_choice: "auto"`, and (c) tool use with `tool_choice: "any"`. With option (b), they observe ~7% of responses contain natural-language preamble before the tool call or a text-only response. What's happening?

- **A)** Tool definitions are missing required fields — fix the schema and the preambles will stop.
- **B)** `tool_choice: "auto"` allows the model to either call a tool OR respond in text — this is documented behavior. To guarantee a tool call, use `tool_choice: "any"` or `tool_choice: {"type": "tool", "name": "..."}`.
- **C)** The 7% rate indicates a temperature that is too high; setting `temperature: 0` will eliminate it.
- **D)** The tool descriptions are too short; expanding them will force tool use.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** `tool_choice: "auto"` is the default-with-tools and explicitly permits the model to either call a tool or respond in text — Anthropic's docs note Claude can be over-eager *or* under-eager about tool calls in this mode. To guarantee a tool call, use `"any"` (any of the provided tools) or a forced specific tool.

**Why A is Wrong:** The behavior is the documented contract of `auto`, not a schema bug.
**Why C is Wrong:** Temperature affects sampling variance, not the auto-vs-required choice axis controlled by `tool_choice`.
**Why D is Wrong:** Tool descriptions are extremely important for *which* tool is called, but they don't override the `tool_choice: "auto"` permission to respond in text.

**Pattern/Trap:** P15 Configuration Hierarchy; P5 Tool Description Primacy

</details>

---

**Q194.** A support agent escalates conversations to humans inconsistently. The system prompt says "Escalate when the customer is frustrated or the issue is complex." Sentiment-analysis logs show the model escalates 8% of conversations, but human auditors say the *correct* escalation rate should be ~22%. What is the most reliable fix?

- **A)** Replace the vague criteria with explicit, observable triggers: "Escalate when ANY of: (1) customer has used a refund/cancel/lawsuit keyword; (2) the issue has been re-opened ≥2 times; (3) the resolution requires changes the available tools cannot perform; (4) customer explicitly requests a human." Provide 3 few-shot examples covering edge cases.
- **B)** Lower the sentiment threshold for "frustrated" so more conversations meet the bar.
- **C)** Add a confidence score to the escalate decision and escalate when confidence > 0.7.
- **D)** Run a second Claude instance asking "Should this be escalated?" and OR the two decisions.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** "Frustrated" and "complex" are subjective adverbial criteria that the model maps to its own internal cutoff inconsistently. Anthropic's guidance is to replace them with explicit, observable, testable conditions. Concrete triggers plus a small set of few-shot examples for boundary cases convert subjective judgment into checkable rules.

**Why B is Wrong:** Sentiment-classifier threshold tuning treats the symptom; the root cause is the criterion itself being vague, not its threshold.
**Why C is Wrong:** Self-reported confidence from LLMs is poorly calibrated; this just adds another vague subjective scalar.
**Why D is Wrong:** Two instances with the same vague criterion produce correlated errors, not independent confirmation; OR-ing decisions inflates false positives without fixing the criterion.

**Pattern/Trap:** P20 Explicit Escalation Criteria; P4 Sentiment/Confidence Trap

</details>

---

**Q195.** An extraction system reports an aggregate accuracy of 96% across 50,000 invoices in a nightly batch. Finance flags that on the ~3,200 international invoices the accuracy is only 71%. The aggregate metric had been masking a domain-specific failure. What is the most appropriate response?

- **A)** The 96% aggregate is acceptable; international invoices are an edge case.
- **B)** Add `temperature: 0` to make extraction more deterministic across all invoices.
- **C)** Switch to a more capable model for the entire pipeline.
- **D)** Segment evaluation by document subtype (domestic vs. international, by country, by currency), build targeted few-shot examples for international cases, and re-evaluate the segment-level metrics; aggregate metrics mask domain-specific failure.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Aggregate accuracy hides systematic failures on minority slices — a 96% global rate is consistent with disastrous performance on a 6% subset. The documented response pattern is segment-level evaluation, identification of the failing slice's specific characteristics, and targeted few-shot examples for the underrepresented case.

**Why A is Wrong:** A 71% accuracy is unacceptably low for production finance data regardless of slice size; "edge case" reasoning normalizes systematic failures.
**Why B is Wrong:** Determinism doesn't improve accuracy on a domain the model is mishandling; it locks in the wrong answer.
**Why C is Wrong:** Upgrading the model for all 50,000 invoices is wasteful when 94% of the volume is already extracted correctly; targeted few-shot is the proportional fix.

**Pattern/Trap:** P12 Aggregate Metric Masking; P2 First Step Proportionality

</details>

---

**Q196.** A team is designing a self-correction validation pattern for invoice extraction. They want the model to detect its own arithmetic inconsistencies. Which schema design best implements this?

- **A)** Add a `confidence: number` field and reject any extraction with confidence < 0.9.
- **B)** Add `stated_total` (verbatim from document) and `calculated_total` (model-computed from line items) plus a `conflict_detected: boolean` field the model must set to true when the values disagree; downstream code validates the boolean and triggers retry-with-feedback or human review when set.
- **C)** Add a `notes: string` field where the model can mention any concerns it has.
- **D)** Add an `extraction_quality: enum["high", "medium", "low"]` field and route low-quality extractions to humans.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**Why Correct:** Anthropic's documented self-verification pattern is to **force the model to compare its own output against the source** and surface the comparison as structured fields. Dual-extraction (stated vs calculated) plus an explicit `conflict_detected` boolean creates an auditable invariant that downstream code can check; this is far more reliable than soft confidence fields because the comparison is mechanical, not subjective.

**Why A is Wrong:** Self-reported confidence from LLMs is poorly calibrated; rejecting on confidence < 0.9 will simultaneously discard correct extractions and accept fabrications labeled "high confidence."
**Why C is Wrong:** Free-text `notes` is unstructured and unparseable, so downstream code cannot mechanically act on it.
**Why D is Wrong:** A 3-level qualitative enum is just confidence-binning under a different name and shares the same calibration problem.

**Pattern/Trap:** P4 Sentiment/Confidence Trap; P14 Nullable Field Prevention

</details>

---

**Q197.** A research orchestrator runs three specialist agents in parallel and synthesizes their findings. The team observes that when all three agree, the synthesis is correct ~96% of the time, but when even one agent dissents the synthesis is correct only ~58% of the time. The team wants to use unanimous agreement as a green-light signal. What is the most accurate critique?

- **A)** Three agents is too few; expand to seven to make consensus more reliable.
- **B)** Unanimous agreement should override any dissent; the dissenter is the noise.
- **C)** If all three agents share the same prompt and same model, unanimous agreement is *correlated* confirmation, not independent — when they share a blind spot, all three are wrong together. The 96% figure is calibrated against the kinds of cases where this prompt happens to work; deploy it as a heuristic for human-review triage, not as a correctness guarantee.
- **D)** Unanimous agreement is fine; just track which agents disagree most often and remove them.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** N agents with the same prompt share the same training-data priors and the same blind spots, so their agreement is *correlated* error, not independent confirmation. The architectural fix is differentiated agents with non-overlapping mandates plus adversarial verification; consensus alone is a triage signal, not a proof.

**Why A is Wrong:** More copies of correlated reviewers don't add independence; the marginal correlation of a 7th agent is near zero.
**Why B is Wrong:** Dissent is often the *signal*, not the noise — minority-opinion findings frequently identify shared blind spots in the majority.
**Why D is Wrong:** Removing the dissenter optimizes for echo chamber; this destroys the calibration value of disagreement.

**Pattern/Trap:** P9 Consensus Review Fallacy; P19 Self-Review Limitation

</details>

---

**Q198.** A team submits a 12,000-document batch. After it ends, `request_counts` shows 11,840 succeeded, 120 errored (`invalid_request_error`), 30 errored (server error), and 10 expired. The team's billing dashboard shows charges only for the 11,840 succeeded. What is the correct interpretation and recovery strategy?

- **A)** Errored, canceled, and expired requests are not billed. For the 120 `invalid_request_error` cases, fix the request bodies (likely prompt or schema issues specific to those inputs) and resubmit by `custom_id`; for the 30 server errors, resubmit as-is; for the 10 expired requests, re-queue.
- **B)** All 12,000 requests are billed because the batch was submitted; the dashboard is delayed.
- **C)** Cancel any related in-flight batches because the error rate exceeded a 1% threshold.
- **D)** Resubmit the entire 12,000-document batch with a new prompt to be safe.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** Anthropic's docs are explicit: only `succeeded` requests are billed within a batch; `errored`, `canceled`, and `expired` are not. The documented recovery pattern is per-state: invalid-request errors require fixing the request body before retry, server errors are retryable as-is, and expired requests need re-queueing — all driven by the `custom_id` join key.

**Why B is Wrong:** Anthropic does not bill non-succeeded requests; the dashboard reflects actual billing accurately.
**Why C is Wrong:** No 1% threshold exists in the API; 1.3% failure is well within normal operational variance.
**Why D is Wrong:** Resubmitting all 12,000 wastes 11,840 successful and already-paid extractions and doubles cost for no benefit.

**Pattern/Trap:** P7 Batch API Latency Trap; P15 Configuration Hierarchy

</details>

---

**Q199.** A team builds a code-review architecture with one Claude agent that generates findings, then in the same conversation appends "Now act as a senior reviewer and disprove any finding you cannot defend." The disprove step removes ~3% of findings. They argue this is a low-cost adversarial review. What is the most accurate evaluation?

- **A)** The 3% reduction is meaningful; this is a working adversarial pattern.
- **B)** The same conversation retains generation context, so the "senior reviewer" persona is biased toward defending its own prior findings; 3% is the rate at which the model reverses *itself*, not the rate of incorrect findings.
- **C)** Adversarial review only works with `extended thinking` enabled.
- **D)** The disprove step should be applied as a separate API call with a fresh system prompt, fresh user message containing only the findings and the source code, and ideally a different model to break correlated biases.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Independent review requires breaking context inheritance: a fresh API invocation with no prior assistant turns, ideally a different system prompt scoping it to disprove the prior findings, and where stakes warrant, a different model entirely to break correlated biases. Anthropic's Code Review architecture implements exactly this pattern.

**Why A is Wrong:** A 3% self-reversal rate measures sycophantic editing tolerance, not correctness; it does not validate the architecture.
**Why B is Wrong:** Diagnoses the problem correctly but stops short of the architectural fix; the question asks for the most accurate full evaluation including the remedy.
**Why C is Wrong:** Extended thinking improves single-pass reasoning depth but still operates within the same instance and context — it is not a substitute for independent review.

**Pattern/Trap:** P19 Self-Review Limitation; P6 Context Inheritance Misconception

</details>

---

**Q200.** A team wants to reduce API costs for automated analysis. Currently, real-time Claude calls power two workflows: (1) a blocking pre-merge check that must complete before developers can merge, and (2) a technical debt report generated overnight for review the next morning. A manager proposes switching both to the Message Batches API for its 50% cost savings. How should you evaluate this proposal?

- **A)** Switch both workflows to batch processing with status polling to check for completion.
- **B)** Switch both to batch processing with a timeout fallback to real-time if batches take too long.
- **C)** Keep real-time calls for both workflows to avoid batch result ordering issues.
- **D)** Use batch processing for the technical debt reports only; keep real-time calls for pre-merge checks.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** The Message Batches API offers 50% cost savings but has processing times up to 24 hours with no guaranteed latency SLA. This makes it unsuitable for blocking pre-merge checks where developers wait for results, but ideal for overnight batch jobs like technical debt reports.

**Why A is Wrong:** Relying on "often faster" batch completion isn't acceptable for blocking workflows; there is no guaranteed latency SLA and developers cannot wait up to 24 hours to merge.
**Why C is Wrong:** Batch results can be correlated using `custom_id` fields; result ordering is not a legitimate concern.
**Why B is Wrong:** Adds unnecessary complexity when the simpler solution is matching each API to its appropriate use case.

**Pattern/Trap:** P7 Batch API Latency Trap

</details>

---

**Q201.** A team builds an extractor that must always return a JSON object matching a fixed schema. They set `tool_choice: "auto"` and provide one tool definition. They observe ~7% of calls return plain text instead of a tool call. The team is surprised because they assumed providing tools makes the model always call them. Which explanation is correct?

- **A)** The model has a bug when only one tool is provided; use at least two tools.
- **B)** The tool schema has an error causing the model to fall back to text.
- **C)** `tool_choice: "auto"` explicitly allows the model to either call a tool OR respond in text; to guarantee a tool call use `tool_choice: "any"` or force a specific tool with `tool_choice: {"type": "tool", "name": "..."}`.
- **D)** The 7% represents rate-limited calls; add retry logic with exponential backoff.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** `tool_choice: "auto"` is Anthropic's documented default-with-tools behavior: the model may call a tool or respond in text. Guaranteeing a tool call requires `"any"` (must call one of the available tools) or a forced specific tool name. This is a configuration choice, not a bug.

**Why A is Wrong:** Single-tool configurations work normally; the behavior is about `tool_choice` mode, not the number of tools.
**Why B is Wrong:** A schema error would produce a different failure mode (validation error or malformed call), not a fallback to plain text.
**Why D is Wrong:** Rate limiting returns HTTP 429 errors, not plain-text responses in place of tool calls.

**Pattern/Trap:** P15 Configuration Hierarchy; P1 Prompt vs Programmatic Enforcement

</details>

---

**Q202.** A team is preparing a 90,000-document overnight extraction batch. A pilot of 100 representative documents on the synchronous Messages API shows ~12% of outputs have a recurring error: line items missing their currency field. They have 3 hours until the batch must submit to meet SLA. What is the right action?

- **A)** Refine the prompt and schema now (add an explicit "currency is required for every line item, infer from header if not specified per line" instruction plus 2–3 few-shot examples), re-pilot on the 100 documents, then submit the full 90,000-document batch — prompt iteration must happen *before* batch submission because there is no in-flight prompt update and validation is asynchronous.
- **B)** Submit the batch as-is and fix the 12% with a follow-up batch.
- **C)** Submit the batch and PATCH the prompt mid-flight when the issue manifests at scale.
- **D)** Skip the pilot and submit directly; 12% is acceptable.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

**Why Correct:** The Batches API has no in-flight update endpoint and validates asynchronously; a known 12% defect rate on a 90,000-document batch yields ~10,800 broken extractions before any feedback signal arrives. Anthropic's documented best practice is to dry-run on the synchronous API to debug quality, iterate the prompt to convergence, and only then submit.

**Why B is Wrong:** A follow-up batch doubles cost and adds another full processing window of latency for problems already known and fixable now.
**Why C is Wrong:** No PATCH/update endpoint exists for in-flight batches; the option fabricates a capability.
**Why D is Wrong:** A known 12% defect rate on 90,000 documents is 10,800 broken records; "acceptable" without remediation violates SLA quality requirements.

**Pattern/Trap:** P7 Batch API Latency Trap; P2 First Step Proportionality

</details>

---

**Q203.** An extraction pipeline retries failed schema validations. After analyzing 30 days of logs, the team finds that retries 1, 2, and 3 succeed at rates 73%, 41%, and 9% respectively for format errors, but 4%, 3%, and 2% for "field not found in source" errors. What is the most defensible retry policy?

- **A)** Always retry 3 times — the marginal success rate is positive on every retry.
- **B)** Retry up to 5 times because retry-with-feedback is Anthropic's recommended pattern.
- **C)** Retry 0 times — retries add cost without solving real problems.
- **D)** Cap retries at 2 for format errors (where marginal benefit is meaningful) and 0 for data-absence errors (where information is genuinely not in the source and retries produce fabrication); detect the error class via the validation message and route accordingly.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

**Why Correct:** Anthropic guidance distinguishes transient/format errors (retry with feedback works because the model has the information but produced a malformed shape) from data-absence errors (information is genuinely not in the source; additional attempts only generate more confident fabrications). A 2-3% "success rate" on data-absence retries is fabrication noise, not real recovery.

**Why A is Wrong:** A 2-3% success rate on data-absence retries is fabrication noise, not real recovery; treating it as success poisons the dataset.
**Why B is Wrong:** Anthropic's pattern recommends retries *with a maximum cap*, never unconditional retries, and explicitly distinguishes when retries are futile.
**Why C is Wrong:** Discarding retries entirely sacrifices the 73% recovery on format errors — a real and well-calibrated benefit.

**Pattern/Trap:** P13 Retry Futility; P10 Root Cause vs Symptom

</details>

---

**Q204.** A team's PR-review system uses a single Claude agent with a 12-page system prompt that lists every kind of issue to look for. Recall on critical bugs is 81%; the team wants 95%. They are debating between (a) further expanding the prompt to cover more issue types, (b) using extended thinking with `budget_tokens: 12000`, and (c) splitting the work across multiple specialized agents. Which approach is most aligned with Anthropic's documented Code Review architecture?

- **A)** Option (a) — exhaustive prompts are the simplest approach and avoid orchestration overhead.
- **B)** Option (b) — extended thinking provides the deepest single-pass analysis and is functionally equivalent to multi-agent review.
- **C)** Option (c) — multiple specialized agents each scoped to a different failure mode (data-handling, off-by-one, API misuse, security) running in parallel, combined with a cross-file integration pass and an adversarial verification step, then aggregate by deduplicating and ranking by severity.
- **D)** None of the above — recall above 81% is impossible without retraining the base model.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

**Why Correct:** Anthropic's Code Review blog documents this exact architecture: multiple specialized agents in parallel rather than one monolithic reviewer, each with a different failure-mode scope to reduce shared blind spots; a cross-file integration pass to surface issues invisible to per-file reviewers; an adversarial verification step where each agent attempts to disprove its own findings; and an aggregation step that deduplicates and ranks by severity.

**Why A is Wrong:** A 12-page prompt is already showing diminishing returns; further expansion increases contradictions and hits attention-distribution limits without adding genuinely new perspectives.
**Why B is Wrong:** Extended thinking improves single-pass reasoning depth but operates within the same instance, same prompt, and same blind spots — it is not equivalent to independent specialized review.
**Why D is Wrong:** Anthropic's reported architecture demonstrably exceeds 81% recall on substantive findings without retraining; the option fabricates a ceiling.

**Pattern/Trap:** P19 Self-Review Limitation; P9 Consensus Review Fallacy

</details>

---
