# Domain 4 grounding digest: Prompt Engineering and Structured Output (20%)

Core idea: a schema guarantees shape, never truth. Stems pair a named symptom with a plausible wrong remedy; the best answer fixes the cause at the lowest cost.

## 4.1 Explicit criteria to cut false positives

- **Diagnosis:** low precision with high recall means the criterion has no stated boundary, so the model picks a permissive one. Ignored flags are the "car alarm effect": people stop looking and a real issue ships.
- **Correct pattern:** categorical REPORT/SKIP rules or a conjunctive test (all conditions must hold). Add an exclusion list naming common near misses, a quoted excerpt per positive finding, and a required `needs_human_review` outcome naming the unverifiable test. State that an empty result is valid. Define severity levels with concrete code examples.
- **Noisy category:** if one category runs a false positive rate of about 60 percent or more, disable that category alone. Write its re-enable date into the prompt, and leave the precise categories untouched.
- **For extraction:** ALWAYS extract / NEVER fabricate / SKIP if absent. Absent means null, not inferred.
- **Tempting wrong answers:** "be conservative", "be thorough" (vague and contradictory). Emphasis, capitals, audit threats. Filtering on self-reported confidence: calibrated to training data, not your standards, and not business importance. Lower temperature: determinism is not precision. A global threshold that also mutes the good categories. Voting over the same vague criterion.
- **Answer-flipping words:** "what is the first/most effective step" means categorical criteria. "Uncertain cases must stay visible" means an abstention channel. "One category is noisy" means disable that category.

## 4.2 Few-shot for consistency

- **Diagnosis:** inconsistency is not hallucination. The model understands the task but resolves an ambiguous boundary differently across runs. More prose hits an instruction ceiling: words like "severe" calibrate against general data. Examples show; instructions only describe.
- **Correct pattern:** a small targeted set (sources say two to four or three to five; don't hinge on the count). Run inputs several times to find where output flips, and spend examples only on those fault lines. Show input, reasoning, output: the derivation generalises, output-only invites pattern matching. Put near misses on both sides of each boundary, balance outcomes, and match incidental features such as length. State the house rule in the reasoning when two labels are defensible. Exercise the abstention path once. Wrap examples in `<example>` tags inside `<examples>`.
- **Tempting wrong answers:** obvious or highest-volume cases (no boundary information). One-sided outcomes (teaches a frequency prior). Many examples (bloat, pattern matching). More prose. Temperature 0. Treating examples as a format guarantee: they make the right format likely, never certain.

## 4.3 Enforcing structure with tool use and schemas

- **Correct pattern:** define an extraction tool whose `input_schema` is the contract and force the call with `tool_choice`, or use Structured Outputs (`output_config.format` with a JSON schema). `auto` lets the model answer in prose, which is the cause of intermittent parser crashes. Sources disagree on `any` versus naming the tool, so prefer answers that don't hinge on it.
- **Schema design:** type optional fields as string-or-null and keep them in `required`. Required non-nullable forces fabrication; dropping the field from `required` loses the presence guarantee. Add `fields_not_found` and `additionalProperties: false`, and forbid inferring or computing values in descriptions. `enum`, `const`, `pattern`, `anyOf`, `required` are enforced; `minimum`, `maximum`, `minLength`, `maxLength` are not (SDKs strip them and validate client-side). Prefer `enum` when values are enumerable.
- **Response handling:** check `stop_reason` before parsing. `max_tokens` means truncated; `refusal` goes to an exception queue, not the retry loop.
- **CLI trap:** `--output-format json` shapes the CLI wrapper. `--json-schema` constrains the answer, which lands in `structured_output`.
- **Tempting wrong answers:** "JSON only" in capitals. Prefill an opening brace (retired on Claude 4.6 and later, and incompatible with enforcement). Tolerant regex repair. A stricter pattern to stop fabricated values: a fabricated value is well formed.

## 4.4 Validation, retry, and feedback loops

- **Three tiers:** (1) structural, handled by enforcement. (2) Internal semantic: totals reconcile, nulls match `fields_not_found`, dates are plausible. (3) External semantic: vendor master, purchase-order lookup. Only tier three catches a coherent extraction of the wrong document.
- **Correct retry:** append the prior attempt as an assistant turn and return the error as a `tool_result` with `is_error: true`, naming the field, observed value, rule, and next action. State which side of a discrepancy is authoritative, or the model overwrites the printed total with its sum and destroys the evidence. Cap attempts (house guidance, two or three), then route to a human. Log the failure taxonomy.
- **Absent data:** retries fix format, not missing information. If the document never states it, stop retrying, return null, and route to a person.
- **Tempting wrong answers:** resending the identical prompt (pure resampling). A generic "validation failed, try again". Raising the retry cap. Backoff, which is for rate limits. A bigger model. Telling the model to "look harder" or estimate. A stricter schema for a semantic error.

## 4.5 Batch processing

- **Deciding axis:** is a user or pipeline blocked waiting on this result? If yes, use the standard API: pre-merge checks, live chat, tight service targets. The second test: does the task need multi-turn tool calling? A batch request is single-turn, so agentic loops cannot run in it.
- **Facts:** 50 percent cost, same model and quality. Up to 24 hours with no guaranteed delivery; most finish within an hour, but design to the worst case. Results are unordered, so join on a meaningful `custom_id`, never on position. `ended` means every request is terminal, not successful: switch over `succeeded`, `errored`, `canceled`, and `expired`, and re-queue the recoverable ones. No streaming inside batches.
- **Tempting wrong answers:** "most finish in an hour, so it fits a four-hour SLA". Faster polling. Many small batches (failure is already per request). "Batch lowers quality".

## 4.6 Multi-instance and multi-pass review

- **Self-review:** an instance reviewing its own output keeps its reasoning and is biased. Use an independent instance with fresh context, not "review more carefully".
- **Multi-pass (sequential):** verify each field against the source with quotes and null what is unsupported. It catches fabrication at 2x to 3x cost. For code: parallel per-file passes for depth, then an integration pass for cross-file breadth.
- **Multi-instance (parallel):** use disagreement to localise ambiguity, not to vote. Unanimity is not correctness: a shared flawed criterion gives confident, agreeing wrong answers, and the fix is the criterion.
- **Tiered escalation (about 1.2x to 1.5x):** the default when volume and budget appear together. Build triggers from validation failures, a confidence enum tied to observable properties (handwritten, rotated, illegible), and pre-call signals. Audit the unescalated population.
- **Tempting wrong answers:** uniform 3x review. Random sampling as a trigger. A free-floating confidence score. Majority voting. More instances on a bad criterion.
