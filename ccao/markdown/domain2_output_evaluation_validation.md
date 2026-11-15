# Domain 2: Output Evaluation and Validation

> Claude Certified Associate – Foundations

> Exam Weight: 21% | Questions in Pool: 15

*Generated from the JSONL bank by `scripts/render_markdown.py` — do not edit by hand.*
*Adapted from two MIT-licensed sources: github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS (Copyright (c) 2026 Amey Thakur), associate-foundations; and github.com/raybeecham/claude-certified-associate-foundations (Copyright (c) 2026 Ray Beecham).*

---

**Q1.** Claude summarizes a vendor contract for you and states that the termination clause requires 60 days' notice, citing section 14.2. You are about to send the summary to your legal team. What should you do first?

- **A)** Check section 14.2 of the contract and confirm the notice period before sending
- **B)** Send it, since Claude cited a specific section
- **C)** Ask Claude how confident it is and send if the confidence is high
- **D)** Rephrase the summary in more formal language, then send

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Specific-looking citations can be fabricated, and material bound for legal review requires verification against the source document. A specific citation is not evidence of accuracy (B), self-reported confidence is not a reliability signal (C), and rewording does nothing about correctness (D).

</details>

---

**Q2.** You ask Claude to draft a competitive analysis, and the output presents market share figures for three competitors without sources. The figures look plausible. What is the appropriate handling?

- **A)** Include the figures, since plausibility is sufficient for internal documents
- **B)** Verify each figure against a market research source and keep only what checks out, with citations
- **C)** Delete the figures and note that no market data was available
- **D)** Ask Claude to regenerate until the numbers stabilize across runs

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Unsourced quantitative claims are a classic hallucination surface; the professional move is verification against an authoritative source, keeping what survives. Plausibility is not accuracy (A), deleting everything discards genuinely verifiable material (C), and consistency across regenerations does not establish truth (D).

</details>

---

**Q11.** Claude produces a competitor comparison table where one row is marked “data unavailable” and the rest are filled in. A colleague asks you to delete the empty row so the table looks complete. What is the right response?

- **A)** Delete the row, since an incomplete table undermines confidence
- **B)** Keep the row and its label, because the gap is itself a finding the reader needs
- **C)** Fill the row with a reasonable estimate and mark it as approximate
- **D)** Ask Claude to search harder until every row is populated

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

A declared gap is information: it tells the reader where the analysis is thin. Deleting it (A) hides a limitation, an unmarked estimate (C) manufactures data, and pressing the model to fill the cell (D) invites fabrication rather than retrieval.

</details>

---

**Q12.** Two runs of the same prompt give different figures for the same metric. Which conclusion is supported?

- **A)** The higher figure is more likely correct because the model found more evidence
- **B)** The figures should be averaged to reduce variance
- **C)** Neither figure is established, and the metric must be checked against the source
- **D)** The prompt is fine and the model needs a longer context window

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Disagreement between runs shows the figure is not grounded in a reliable source, so neither is established. Preferring the larger number (A) is arbitrary, averaging (B) treats two unverified numbers as measurements, and context length (D) is unrelated to whether the figure is true.

</details>

---

**Q13.** You ask Claude to extract every payment term from a 40-page contract. The output lists four terms, cleanly formatted. What is the first check?

- **A)** Confirm the formatting is consistent across the four entries
- **B)** Ask Claude whether it found all of them
- **C)** Run it again at a higher temperature to surface more terms
- **D)** Read the contract's payment sections to confirm no term was omitted

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

Extraction fails by omission more often than by error, and a tidy output gives no signal about completeness. Formatting (A) is cosmetic, self-report (B) is not evidence, and temperature (C) changes phrasing rather than recall.

</details>

---

**Q14.** A summary you commissioned states a conclusion that contradicts your own reading of the source. What should you do?

- **A)** Locate the passage the conclusion rests on and compare it against both readings
- **B)** Defer to the summary, since the model read the whole document
- **C)** Defer to your reading and treat the summary as wrong
- **D)** Ask a colleague which of the two sounds more plausible

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

The disagreement is resolvable by returning to the passage in question, which settles it on evidence. Deferring either way (B, C) decides without checking, and canvassing opinion (D) substitutes plausibility for the source.

</details>

---

**Q15.** Claude produces a well-argued recommendation with no citations, on a topic where you have no expertise. What is the appropriate use of it?

- **A)** Adopt it, since the reasoning is internally consistent
- **B)** Treat it as a hypothesis to test against sources before acting
- **C)** Discard it, because unsourced output has no value
- **D)** Ask for citations and adopt whatever comes back

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Unsourced reasoning is a starting point, useful for structuring an enquiry but not for deciding. Internal consistency is not accuracy (A), the reasoning may still be useful (C), and citations produced on demand need the same verification as the claim (D).

</details>

---

**Q52.** A team says a summarizer is “not good enough” and wants to rewrite the prompt immediately. What should happen first?

- **A)** Increase the number of adjectives in the prompt.
- **B)** Define measurable success criteria and construct representative tests that expose the reported failure.
- **C)** Select the longest available output setting.
- **D)** Ask users to accept more variation.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

The team must define what acceptable performance means and how it will be measured before prompt changes can be evaluated. (A) Wording changes without criteria cannot be assessed objectively. (C) Output length may be unrelated to the actual failure. (D) Changing expectations without understanding the use case is not evaluation.

</details>

---

**Q53.** A workflow must return exactly one of four allowed status labels and a valid control identifier. Which grader is best for these properties?

- **A)** Deterministic code that validates the enumeration and identifier
- **B)** An unstructured human opinion
- **C)** A second model asked whether the output feels correct
- **D)** The original model's self-reported confidence

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Allowed values and identifier validity are exact, machine-checkable properties. Deterministic validation is consistent and auditable. (B) Human review is unnecessarily expensive and less consistent for exact checks. (C) A model grader adds variability to a deterministic property. (D) Self-reported confidence does not validate the actual fields.

</details>

---

**Q54.** A customer-support answer must follow policy, contain required disclosures, and communicate with appropriate empathy. Which evaluation design is strongest?

- **A)** Use only exact string matching for the whole answer.
- **B)** Use only a single reviewer's overall impression.
- **C)** Use deterministic checks for required policy elements plus a calibrated human or model-assisted rubric for nuanced communication, with periodic human review.
- **D)** Use response length as the sole metric.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Different properties require different graders. Exact requirements can be automated, while nuanced tone needs a calibrated semantic judgment process. (A) Exact matching cannot reliably score nuanced communication. (B) One uncalibrated impression is subjective and difficult to reproduce. (D) Length does not measure policy fidelity or empathy.

</details>

---

**Q55.** An assistant invents implementation dates that are absent from the approved documents. Which combined control is strongest?

- **A)** Ask for more detailed dates.
- **B)** Increase creativity so the dates appear natural.
- **C)** Remove citations to make the answer easier to read.
- **D)** Restrict claims to approved sources, permit `unknown`, require claim-level citations or quotations, and validate support before release.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

The system should make unsupported specificity unnecessary and detectable by grounding every claim and permitting abstention. (A) Requesting more detail can increase fabrication when evidence is absent. (B) Creativity is contrary to evidence-bound reporting. (C) Removing citations reduces traceability.

</details>

---

**Q56.** A policy assistant performs well on ten clean examples written by its developers. Which addition most improves confidence in production readiness?

- **A)** Ten paraphrases of the same clean examples
- **B)** Realistic cases covering normal inputs, missing and conflicting evidence, stale sources, long inputs, unauthorized requests, and prompt injection attempts
- **C)** One very long prompt that includes every possible instruction
- **D)** A reviewer who reads only the best outputs

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

A representative evaluation set must reflect the real distribution and intentionally test edge and adversarial conditions. (A) Paraphrases improve volume but not risk coverage. (C) Prompt length is not a substitute for test diversity. (D) Selecting only successful outputs creates severe bias.

</details>

---

**Q57.** A candidate version scores 96% overall, up from 93%. However, one test exposes another business unit's confidential document. What is the correct release decision?

- **A)** Release because the aggregate score improved.
- **B)** Average the privacy failure with the style scores.
- **C)** Block release, investigate the access-control failure, and require a validated fix before reconsideration.
- **D)** Release to all users but add a warning.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Unauthorized disclosure is a critical failure and must be a hard release gate. Aggregate quality cannot offset it. (A) An average hides severity and does not make the disclosure acceptable. (B) Privacy should not be diluted by unrelated low-severity metrics. (D) A warning does not prevent unauthorized access.

</details>

---

**Q58.** Claude drafts individualized legal guidance from uploaded records. What validation approach is most appropriate before the guidance affects a person's decision?

- **A)** Require review by a qualified legal professional with access to the evidence, disclose AI involvement as required, and preserve the person's ability to question or contest the guidance.
- **B)** Use the model's confidence score as final approval.
- **C)** Publish automatically when the prose is fluent.
- **D)** Ask an untrained reviewer to click approve within ten seconds.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

High-impact legal guidance requires meaningful qualified human oversight, evidence access, and appropriate disclosure. Accountability cannot be delegated to model confidence. (B) Self-reported confidence is not a legal or factual validation. (C) Fluency does not establish correctness or suitability. (D) An unqualified, rushed reviewer is not meaningful oversight.

</details>

---

**Q59.** A classification result changes across repeated runs on the same input. The business requires stable routing. What is the strongest evaluation response?

- **A)** Review only the first run.
- **B)** Accept variation because language models are probabilistic.
- **C)** Measure the length of each explanation.
- **D)** Run repeated trials, measure label agreement and worst-case behavior, set a consistency threshold, and test prompt, schema, and model changes against it.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

When stability is a requirement, the evaluation must measure output variance at the level that matters and enforce a threshold. (A) A single run cannot reveal instability. (B) Probabilistic behavior does not remove the business requirement. (C) Explanation length is not label consistency.

</details>

---
