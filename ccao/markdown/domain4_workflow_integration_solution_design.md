# Domain 4: Workflow Integration and Solution Design

> Claude Certified Associate – Foundations

> Exam Weight: 16% | Questions in Pool: 14

*Generated from the JSONL bank by `scripts/render_markdown.py` — do not edit by hand.*
*Adapted from two MIT-licensed sources: github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS (Copyright (c) 2026 Amey Thakur), associate-foundations; and github.com/raybeecham/claude-certified-associate-foundations (Copyright (c) 2026 Ray Beecham).*

---

**Q6.** Your monthly close process involves collecting figures, drafting a variance commentary, and formatting a board pack. You want Claude to help durably, not just once. What is the strongest approach?

- **A)** Create a Project with the commentary conventions and prior packs as knowledge, plus instructions for the structure, and run each close inside it
- **B)** Paste everything into a fresh chat each month and ask for the pack
- **C)** Ask Claude to do the whole close autonomously, including pulling the figures
- **D)** Use Claude only for spellchecking the final pack

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Durable, repeated workflows belong in a Project where instructions and knowledge persist and improve. Re-pasting monthly (B) rebuilds context by hand every time, full autonomy over financial figures without review (C) ignores appropriate-use judgment, and spellchecking (D) forfeits the actual value.

</details>

---

**Q7.** A department head asks you whether Claude could "handle our customer onboarding." What is the right first move?

- **A)** Say yes and start building immediately
- **B)** Map the onboarding steps, identify which involve drafting, summarizing, or lookup that Claude does well, and which need human judgment or system access it does not have
- **C)** Say no, since onboarding involves customer data
- **D)** Forward the question to Anthropic support

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

The Associate's core skill is translating a business ask into a realistic division of labor: where Claude adds value, where humans stay, and what the limits are. Unqualified yes (A) and unqualified no (C) both skip the analysis, and support (D) does not know your process.

</details>

---

**Q16.** A team wants Claude to draft weekly customer health summaries from support tickets, CRM notes, and usage data. Which design detail matters most for the output to stay useful over months?

- **A)** Choosing the largest available model
- **B)** Running the summary daily instead of weekly
- **C)** Defining what a health summary must contain and keeping that definition in one place the team maintains
- **D)** Letting each team member write their own prompt

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

A stable, maintained definition of the deliverable is what keeps output consistent as people and inputs change. Model size (A) does not fix an undefined task, higher frequency (B) multiplies an unclear output, and per-person prompts (D) guarantee drift.

</details>

---

**Q17.** Which task in a monthly reporting process is the weakest candidate for delegation to Claude?

- **A)** Drafting the narrative summary from agreed figures
- **B)** Reformatting last month's report into the new template
- **C)** Extracting the top five variances from a spreadsheet export
- **D)** Deciding which underperforming account to escalate to the executive team

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

The escalation decision carries accountability and depends on relationships and context the model does not hold. Drafting (A), reformatting (B), and extraction (C) are all bounded tasks with checkable output.

</details>

---

**Q18.** A process works well for one analyst and poorly for three others using the same prompt. What is the most likely cause?

- **A)** The prompt relies on context the first analyst supplies without noticing
- **B)** The other three need a more capable model
- **C)** The task is unsuitable for Claude
- **D)** The other three are using shorter inputs

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

One person succeeding with the same prompt usually means they are contributing unstated context, such as knowing which file to attach or what good looks like. A model change (B) does not supply missing context, the task clearly works (C), and input length (D) is a symptom rather than a cause.

</details>

---

**Q19.** When is it appropriate to keep a human approval step in an otherwise automated Claude workflow?

- **A)** Always, since automation is inherently risky
- **B)** When the action is hard to reverse or carries external consequences
- **C)** Only while the workflow is new, then remove it
- **D)** Never, because approval steps defeat the purpose of automation

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Approval earns its cost where a mistake is expensive or hard to undo. Blanket approval (A) and blanket removal (D) both ignore the specific risk, and a time-based rule (C) removes the check regardless of what the action does.

</details>

---

**Q60.** A workflow calculates exact payment totals and then drafts a plain-language explanation. Which division of responsibility is best?

- **A)** Use deterministic code for the calculations and Claude for the explanation based on validated results.
- **B)** Ask Claude to calculate and authorize the payment in one step.
- **C)** Let a human retype every number after generation.
- **D)** Use retrieval to estimate the payment.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Exact arithmetic and authorization belong in deterministic components. Claude can explain the validated results without controlling the financial action. (B) This combines probabilistic calculation with a consequential side effect. (C) Manual retyping adds error and does not improve the architecture. (D) Retrieval is unrelated to exact arithmetic.

</details>

---

**Q61.** A system drafts a public incident statement from verified evidence. Where should the communications lead's approval occur?

- **A)** After the statement has been posted
- **B)** Only after public feedback arrives
- **C)** After evidence and policy validation but before any publishing tool can execute
- **D)** Inside a hidden model instruction with no reviewer interface

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Meaningful approval must occur before the consequential side effect and should present the evidence, uncertainty, and proposed action to an authorized reviewer. (A) Post-execution review cannot prevent harm. (B) Public feedback is not a substitute for prepublication authorization. (D) A model instruction does not create human accountability.

</details>

---

**Q62.** A payment tool times out after submission. The client does not know whether the payment completed. What is the safest next action?

- **A)** Immediately submit the same payment again with a new identifier.
- **B)** Use the original idempotency key or transaction identifier to check status before any retry.
- **C)** Ask Claude whether it thinks the payment succeeded.
- **D)** Ignore the timeout and mark the workflow complete.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

A status check tied to a stable idempotency key prevents duplicate side effects when the result of the first request is uncertain. (A) A new identifier can create a duplicate payment. (C) The model cannot determine an external transaction state without authoritative evidence. (D) Ignoring the result leaves the workflow inconsistent.

</details>

---

**Q63.** Which tool definition is most reliable for model-guided use?

- **A)** `manage_data`: Does data things.
- **B)** `run_action`: Use whenever needed; accepts any object.
- **C)** `admin`: Full system access for convenience.
- **D)** `create_draft_exception_request`: Creates a non-approved draft only, lists when it applies, requires typed fields and authorization, defines errors, and has no execution capability.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

A purpose-specific, narrow, typed, and non-ambiguous contract supports correct selection and least privilege. (A) The purpose and selection boundary are undefined. (B) An unconstrained object and broad use guidance are unsafe. (C) Full administrative access violates least privilege.

</details>

---

**Q64.** End-to-end latency increased, but the team logs only the total request duration. What is the key missing capability?

- **A)** A longer system prompt
- **B)** Stage-level timing and outcome data for retrieval, model generation, tools, validation, and human review
- **C)** A second copy of every response
- **D)** A model-generated explanation of its internal reasoning

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Stage-level telemetry is required to identify the bottleneck and choose the appropriate optimization. (A) A longer prompt may increase latency and does not identify the cause. (C) Duplicating responses does not isolate stages. (D) Internal reasoning is neither necessary nor a reliable performance trace.

</details>

---

**Q65.** A workflow pauses for two days while awaiting approval, then resumes after a service restart. Which design is required?

- **A)** Persist validated workflow state, completed steps, versions, and pending approval outside the prompt.
- **B)** Assume the model will remember the workflow after restart.
- **C)** Keep the only state in a developer's browser tab.
- **D)** Restart the entire workflow and repeat all side effects.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Long-running workflows need durable external state and validated state transitions. Model context is not a reliable workflow database. (B) The model does not independently preserve application state across service restarts. (C) A browser tab is fragile, unauditable, and not a system of record. (D) Repeating completed side effects can create duplicates.

</details>

---

**Q66.** A process always follows the same five steps with fixed validation and one approval gate. Which architecture is usually safest?

- **A)** An unconstrained autonomous agent with every enterprise tool
- **B)** An explicit workflow with bounded model calls and deterministic transitions
- **C)** A single prompt that silently performs all steps
- **D)** A public chatbot with no state store

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

A known sequence is easier to test, observe, authorize, and recover as an explicit workflow. Agentic autonomy is unnecessary. (A) Broad autonomy and tools add risk without a requirement. (C) An opaque prompt lacks stage validation and recovery. (D) The pattern does not meet integration or state requirements.

</details>

---

**Q67.** A team proposes a multi-agent system for a one-time, human-reviewed summary of two documents. What is the best design principle?

- **A)** More agents always improve factual accuracy.
- **B)** Every document task requires a workflow engine.
- **C)** Choose the simplest architecture that meets the quality, integration, control, and risk requirements.
- **D)** Use the architecture with the most components because it is easier to audit.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Complexity should be justified by requirements. A simple human-led interaction may be more appropriate and easier to govern. (A) More model calls can add new failure modes. (B) A workflow engine is not necessary for every task. (D) More components generally increase the audit surface.

</details>

---
