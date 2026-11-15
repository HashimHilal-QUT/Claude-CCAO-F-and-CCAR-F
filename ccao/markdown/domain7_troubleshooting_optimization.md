# Domain 7: Troubleshooting and Optimization

> Claude Certified Associate – Foundations

> Exam Weight: 10% | Questions in Pool: 11

*Generated from the JSONL bank by `scripts/render_markdown.py` — do not edit by hand.*
*Adapted from two MIT-licensed sources: github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS (Copyright (c) 2026 Amey Thakur), associate-foundations; and github.com/raybeecham/claude-certified-associate-foundations (Copyright (c) 2026 Ray Beecham).*

---

**Q10.** A prompt that worked well for weeks now produces off-target answers after your team added many new documents to the Project. What is the best first diagnostic?

- **A)** Check whether the newly added knowledge is diluting or contradicting the sources the answers should draw from
- **B)** Rewrite the prompt from scratch
- **C)** Switch to a larger model
- **D)** Delete the Project and start over

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

The change that coincided with the regression is the first suspect: new knowledge can crowd out or conflict with the relevant sources. Rewriting the prompt (B), upgrading the model (C), or rebuilding everything (D) all treat symptoms before diagnosing the actual change.

</details>

---

**Q34.** A workflow that has run reliably for months begins returning off-target output. What is the first diagnostic step?

- **A)** Establish what changed: the inputs, the configuration, or the knowledge
- **B)** Rewrite the prompt from scratch
- **C)** Switch to a different model
- **D)** Increase the amount of context supplied

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

A working system that degrades points to a change, and identifying it is faster and safer than rebuilding. Rewriting (B), switching models (C), and adding context (D) all alter the system before the cause is known.

</details>

---

**Q35.** Output quality is acceptable but the process takes too long to be worth using. What should be examined first?

- **A)** Whether a faster model would meet the quality bar
- **B)** Whether the slow part is the model or the human steps around it
- **C)** Whether the prompt can be shortened
- **D)** Whether the task should be abandoned

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Locating the actual delay comes before optimising anything, and in practice the surrounding steps often dominate. Changing the model (A) or the prompt (C) assumes the model is the bottleneck, and abandoning (D) discards a process that already produces acceptable output.

</details>

---

**Q84.** A report generator became less accurate after a release that changed the model, prompt, tools, retrieval query, and schema. What is the best first technical step?

- **A)** Reconstruct the known-good baseline and compare one changed component at a time on the same evaluation set.
- **B)** Keep all changes and add more instructions.
- **C)** Retry each failed case until it passes once.
- **D)** Assume the model is the only possible cause.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

A known-good baseline and controlled variable isolation are required to attribute the regression. (B) Additional uncontrolled change makes attribution harder. (C) A single pass can hide intermittent or systematic failure. (D) Any of the changed components could be responsible.

</details>

---

**Q85.** Claude chooses the public search tool instead of the internal standards tool. Both tools have similar names and descriptions. Which fix is most directly supported by the symptom?

- **A)** Increase the maximum output length.
- **B)** Differentiate the tool purposes and when-to-use rules, strengthen schemas and examples, and expose only eligible tools.
- **C)** Allow the public tool to access internal data.
- **D)** Remove all tool descriptions.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Ambiguous tool descriptions and selection boundaries are a common cause of wrong-tool behavior. Narrow exposure also reduces confusion and privilege. (A) Output length does not control tool selection. (C) Broadening access creates security risk. (D) Descriptions are necessary for informed selection.

</details>

---

**Q86.** A tool call contains an invented field named `system_owner_email`, which is neither required nor authorized. What is the strongest fix?

- **A)** Silently accept the field when it looks plausible.
- **B)** Ask Claude to spell the email more carefully.
- **C)** Use a strict schema that forbids extra fields, validate all parameters in the application, and require authoritative lookup for any identifier.
- **D)** Send the email to test whether it exists.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

The tool boundary must reject fields outside the contract and prevent model-invented identifiers from causing action. (A) Silent coercion hides errors and can create unauthorized behavior. (B) Spelling does not establish authority or provenance. (D) Testing an invented address can itself create an unauthorized side effect.

</details>

---

**Q87.** Prompt-cache hit rates collapse after a release even though the long reference text did not change. Which item should the team inspect first?

- **A)** Whether any content, ordering, tool definitions, or cache breakpoint in the reusable prefix changed
- **B)** Whether the final user answer used more adjectives
- **C)** Whether reviewers liked the output tone
- **D)** Whether the model's pretrained knowledge changed

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Cache reuse depends on the applicable stable prefix and platform semantics. Seemingly small early changes or reordered tools can invalidate reuse. (B) Generated answer wording does not determine the input prefix match. (C) Tone review is unrelated to cache identity. (D) Pretrained knowledge is not the direct cache key.

</details>

---

**Q88.** P95 end-to-end latency rose by 50%. The workflow includes retrieval, two model calls, a database tool, validation, and human approval. What should the team do first?

- **A)** Remove validation immediately.
- **B)** Switch to the smallest model without testing quality.
- **C)** Measure latency and queueing for every stage, then optimize the actual bottleneck against quality and risk thresholds.
- **D)** Increase the retry count.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Stage-level measurement identifies whether the bottleneck is retrieval, model generation, tools, validation, or approval. Optimization should preserve required quality and controls. (A) Removing validation can create unacceptable risk and may not fix latency. (B) A model change requires evaluation and may not address the bottleneck. (D) More retries can increase latency and cost.

</details>

---

**Q89.** A previously allowed analytical task now receives a refusal. What is the strongest troubleshooting approach?

- **A)** Keep rephrasing until a guardrail is bypassed.
- **B)** Inspect the exact task, current policy and permissions, refusal or stop metadata, and recent changes, then redesign only the permitted portion or escalate.
- **C)** Disable all safety controls.
- **D)** Assume every refusal is a service outage.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

A refusal can reflect policy, authorization, task framing, or system change. Troubleshooting must respect the boundary rather than evade it. (A) Repeated evasion attempts are unsafe and do not diagnose the cause. (C) Safety controls must not be removed to force completion. (D) A refusal is distinct from a generic service outage.

</details>

---

**Q90.** A report repeatedly ends at the same point, and the stop reason indicates the maximum generation length. What is the best remediation?

- **A)** Assume the missing content was not important.
- **B)** Retry indefinitely with the same budget.
- **C)** Remove the output schema.
- **D)** Increase the output budget when appropriate, reduce irrelevant context or requested verbosity, decompose or paginate the task, and validate partial output.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

The evidence identifies a generation-length problem. The design should allocate budget or split the work and explicitly handle incomplete output. (A) The required report is incomplete. (B) Identical retries preserve the same limit and add cost. (C) Removing structure can make partial output harder to detect and integrate.

</details>

---

**Q91.** Which change process produces the most trustworthy optimization result?

- **A)** Record a baseline, change one material variable, rerun representative tests and operational metrics, document the result, and preserve rollback.
- **B)** Change every component and judge one attractive output.
- **C)** Optimize only for cost and ignore quality.
- **D)** Deploy directly to all users without monitoring.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Controlled experimentation enables attribution, regression detection, and safe reversal. (B) One attractive output is not representative, and multiple changes obscure causality. (C) Optimization must respect quality, safety, and mission requirements. (D) Unmonitored full deployment creates avoidable risk.

</details>

---
