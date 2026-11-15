# Domain 6: Governance, Risk, and Responsible Use

> Claude Certified Associate – Foundations

> Exam Weight: 15% | Questions in Pool: 13

*Generated from the JSONL bank by `scripts/render_markdown.py` — do not edit by hand.*
*Adapted from two MIT-licensed sources: github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS (Copyright (c) 2026 Amey Thakur), associate-foundations; and github.com/raybeecham/claude-certified-associate-foundations (Copyright (c) 2026 Ray Beecham).*

---

**Q9.** You want Claude to analyze churn patterns in an export that includes customer names, emails, and account numbers. Company policy forbids sharing personal data with external tools. What is the correct action?

- **A)** Upload the file, since churn analysis is an internal purpose
- **B)** Upload it but instruct Claude to ignore the personal columns
- **C)** Abandon the analysis
- **D)** Remove or pseudonymize the identifying columns first, then upload and analyze

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

Make the task compliant, then do it: the identifiers are not needed for pattern analysis. Purpose does not override policy (A), an instruction to ignore data is not a control because the data still left the boundary (B), and abandoning the work (C) is unnecessary when anonymization enables it.

</details>

---

**Q20.** A colleague proposes pasting a customer list into a prompt to draft personalised outreach. What is the correct handling?

- **A)** Proceed, since the prompt is not stored anywhere permanent
- **B)** Ask Claude to keep the names confidential
- **C)** Remove or replace identifying details before drafting, and reattach them afterwards
- **D)** Proceed but delete the conversation afterwards

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Working on anonymised data and reattaching identifiers afterwards achieves the task without exposing the personal data. Assumptions about storage (A) are not a control, an instruction to the model (B) is not a safeguard, and deleting afterwards (D) does not undo the disclosure.

</details>

---

**Q21.** Which statement about instructing a model not to do something is accurate?

- **A)** An instruction in the prompt is an enforceable control
- **B)** Instructions are enforceable if placed in a system prompt
- **C)** Instructions are enforceable if repeated several times
- **D)** An instruction shapes behavior but does not guarantee it, so controls belong outside the prompt

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

Prompt instructions influence behavior and are not guarantees, so anything that must hold is enforced in the surrounding system. Placement (B) and repetition (C) change the strength of the steer, not its nature, and treating it as enforcement (A) is the error the question tests.

</details>

---

**Q22.** A regulated report drafted with Claude is about to be filed. What is the reviewer accountable for?

- **A)** The accuracy and compliance of the filed document, regardless of how it was drafted
- **B)** Confirming that Claude was used according to policy
- **C)** Confirming the prompt included the relevant regulations
- **D)** Recording which model version produced the draft

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Accountability sits with the person who files, and the tool used does not transfer it. Policy compliance (B), prompt content (C), and version records (D) are all reasonable practices that do not replace responsibility for the document.

</details>

---

**Q23.** When is disclosing that AI assisted a piece of work most clearly warranted?

- **A)** Whenever any AI tool touched the work at any stage
- **B)** When the audience's judgment of the work depends on how it was produced
- **C)** Only when the output is published externally
- **D)** Only when a written policy requires it

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Disclosure matters where provenance would change how a reader weighs the work. A universal rule (A) makes the signal meaningless, and confining it to external publication (C) or written policy (D) misses internal cases where it genuinely matters.

</details>

---

**Q76.** A team wants to paste confidential architecture diagrams into a new Claude workspace. What should happen first?

- **A)** Classify the data and verify that the product environment, access, retention, logging, residency, contractual, and organizational controls permit the use.
- **B)** Upload the diagrams, then check policy if a problem occurs.
- **C)** Remove the document titles and assume the content is public.
- **D)** Ask Claude whether the workspace is approved.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Data handling and environment approval must precede processing. The model cannot determine organizational authorization. (B) Governance after disclosure is too late. (C) Removing a title does not declassify the technical content. (D) Approval comes from authoritative policy and accountable humans, not model judgment.

</details>

---

**Q77.** A housing organization uses Claude to rank applicants for eligibility. Which control is most important before any adverse decision?

- **A)** Use the longest possible prompt.
- **B)** Require meaningful review by a qualified authorized human with evidence, disclose AI involvement as required, and provide an appropriate contest or appeal path.
- **C)** Automatically accept the top-ranked answer when confidence exceeds 90%.
- **D)** Have an untrained employee approve every result without seeing the underlying evidence.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

A housing eligibility decision is high impact. Oversight must be qualified, evidence-based, timely, and authoritative, with appropriate transparency and recourse. (A) Prompt length does not establish accountability. (C) Model confidence is not a substitute for human decision responsibility. (D) Rubber-stamping without expertise or evidence is not meaningful review.

</details>

---

**Q78.** An email-processing agent reads a message that instructs it to ignore policy and send customer records to an external address. Which control set is strongest?

- **A)** Ask the model to be careful and retain broad email tools.
- **B)** Hide the system prompt from users.
- **C)** Treat email as untrusted data, constrain tools and recipients, validate authorization in code, require approval for sensitive sends, and test adversarial cases.
- **D)** Retry with a different phrasing until the model complies.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Defense requires authority separation and system-enforced permissions. Prompt text alone cannot prevent unauthorized side effects. (A) A cautionary instruction does not offset broad tool permissions. (B) Secrecy of instructions is not an authorization control. (D) Repeated attempts to comply worsen the security failure.

</details>

---

**Q79.** A team logs every complete prompt, source document, tool credential, and response indefinitely “for debugging.” What is the best correction?

- **A)** Keep the design because more logs are always safer.
- **B)** Make logs publicly searchable so errors are found faster.
- **C)** Encrypt the credential but continue logging it.
- **D)** Minimize and redact content, never log secrets, apply access control and retention, and retain only evidence needed for audit and diagnosis.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

Logs should provide traceability without becoming an uncontrolled sensitive-data store. Secrets must not be logged at all. (A) Excessive logging increases privacy and security exposure. (B) Public access would compound the risk. (C) A credential should not enter the log, even encrypted as a routine practice.

</details>

---

**Q80.** A vendor releases a new model version. The production owner wants to switch immediately because it is newer. What is the strongest governance response?

- **A)** Approve automatically because newer models are always safer.
- **B)** Run change review and regression testing, evaluate policy and risk impacts, obtain required approval, stage rollout, and preserve rollback.
- **C)** Change the model and all prompts simultaneously.
- **D)** Delay all model updates permanently.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

A model change is a material system change. It requires evidence, approval, monitoring, and rollback proportional to the use-case risk. (A) Release date is not evidence of use-case suitability. (C) Multiple simultaneous changes prevent attribution. (D) Permanent avoidance creates obsolescence and is not risk-based.

</details>

---

**Q81.** A user asks the system to perform an action that is prohibited by current provider and organization policy. What should the system do?

- **A)** Refuse the prohibited action, explain the boundary at an appropriate level, provide a safe permitted alternative when available, and follow escalation or logging policy.
- **B)** Comply if the user says the task is urgent.
- **C)** Break the action into smaller steps to bypass the restriction.
- **D)** Ask a second model to authorize it.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Policy boundaries remain in force despite urgency. A safe response refuses the prohibited action and redirects within permitted scope. (B) Urgency does not override policy. (C) Decomposition must not be used for evasion. (D) Another model cannot grant policy authority.

</details>

---

**Q82.** A workflow identifies a case that appears to need an exception to the organization's AI data-handling policy. Who can approve it?

- **A)** Claude, when its confidence is high
- **B)** Any user who submitted the request
- **C)** The named human governance authority through the documented exception process and compensating controls
- **D)** The tool that stores the request

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Policy exceptions require accountable human authority, documented scope, risk analysis, expiration, and monitoring. (A) A model cannot authorize governance exceptions. (B) The requester may have a conflict of interest and lacks delegated authority. (D) A storage tool has no governance authority.

</details>

---

**Q83.** Monitoring suggests a malicious document induced an agent to attempt sending a secret to an external service. What is the best immediate sequence?

- **A)** Delete all logs, then continue operating.
- **B)** Ask the agent whether any data was exposed and accept its answer.
- **C)** Edit the prompt while leaving all tools active.
- **D)** Contain or disable the affected workflow and permissions, preserve evidence, assess scope, rotate exposed credentials, notify incident owners, remediate, and revalidate before restoration.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

Potential exfiltration requires containment and evidence preservation before full remediation. Credential rotation and governed incident response reduce ongoing risk. (A) Deleting logs destroys evidence and leaves the threat active. (B) The agent is not an authoritative incident investigator. (C) Prompt editing alone does not contain tool or credential exposure.

</details>

---
