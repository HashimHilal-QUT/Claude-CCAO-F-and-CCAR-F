# Domain 5: Configuration and Knowledge Management

> Claude Certified Associate – Foundations

> Exam Weight: 12% | Questions in Pool: 12

*Generated from the JSONL bank by `scripts/render_markdown.py` — do not edit by hand.*
*Adapted from two MIT-licensed sources: github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS (Copyright (c) 2026 Amey Thakur), associate-foundations; and github.com/raybeecham/claude-certified-associate-foundations (Copyright (c) 2026 Ray Beecham).*

---

**Q8.** Your team's Project answers policy questions from an uploaded handbook. HR publishes a new handbook version. What must happen for the Project to stay trustworthy?

- **A)** Nothing; Claude will find the new version on its own
- **B)** Add the new handbook alongside the old one so both are available
- **C)** Replace the outdated handbook in the Project knowledge and spot-check answers against the new version
- **D)** Tell users to mention the new version in every prompt

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Project knowledge is maintained, not self-updating; stale sources are a quality defect the configurer owns. Claude does not fetch your internal documents on its own (A), keeping both versions invites contradictory answers (B), and pushing the burden onto every user (D) is not maintenance.

</details>

---

**Q31.** What belongs in a project's knowledge rather than in individual prompts?

- **A)** The specific question being asked today
- **B)** Material that every conversation in the project should be able to draw on
- **C)** The preferred output length for one report
- **D)** A one-off document being reviewed this week

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Project knowledge holds what recurs, so each conversation starts from the same base. Today's question (A), a single formatting preference (C), and a one-off document (D) all belong in the prompt that needs them.

</details>

---

**Q32.** A project's answers have grown vaguer as more documents were added. What is the likely cause?

- **A)** The model version changed
- **B)** The project has too few documents to ground answers
- **C)** The knowledge now holds overlapping or outdated material competing with the right sources
- **D)** The prompts have become too specific

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Accumulated, unmaintained knowledge dilutes retrieval, and the symptom is exactly this drift toward vagueness. A version change (A) is unrelated to what was added, and both too few documents (B) and overly specific prompts (D) contradict the described trend.

</details>

---

**Q33.** How should project knowledge be treated as the underlying material changes?

- **A)** It updates automatically from the source systems
- **B)** It only needs review when answers are visibly wrong
- **C)** It should be rebuilt from scratch each quarter
- **D)** It must be maintained deliberately, because it does not update itself

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

Project knowledge is a curated copy and stays as accurate as the person maintaining it. It does not sync (A), waiting for visible errors (B) means acting after the damage, and periodic rebuilds (C) are wasteful and still unscheduled against real change.

</details>

---

**Q68.** An internal knowledge document is used to answer policy questions, but no one knows whether it is current. What metadata is most important to establish first?

- **A)** The document's font and page color
- **B)** Its owner, authority, version or effective date, classification, scope, and review cadence
- **C)** How many users have downloaded it
- **D)** Whether it contains the word “policy”

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

A governed source needs accountability, authority, freshness, scope, and data-handling metadata before it can reliably support answers. (A) Formatting does not establish governance or freshness. (C) Popularity is not authority. (D) A keyword does not prove the document governs the use case.

</details>

---

**Q69.** Every response in a controlled application must cite approved evidence and use `insufficient_evidence` when support is absent. Where should this rule live?

- **A)** Only in each user's memory
- **B)** Only in the source documents
- **C)** In version-controlled application or system configuration, with retrieval and validation enforcing it
- **D)** In a model-generated note that is not saved

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Durable application behavior should be governed, versioned, reviewed, and tested rather than repeated informally by each user. (A) User memory is not enforceable or auditable. (B) Sources are evidence, not trusted behavioral configuration. (D) An unsaved note cannot establish repeatable system behavior.

</details>

---

**Q70.** A service repeatedly sends the same long system instructions, tool definitions, and approved reference text, followed by a different short user task. Data policy permits caching. What optimization is most relevant?

- **A)** Place the stable reusable content in a consistent prompt prefix and use the platform's prompt-caching behavior, then measure actual hits.
- **B)** Move a changing timestamp to the beginning of the prompt.
- **C)** Store the API credential in the cached text.
- **D)** Randomize the order of tool definitions on each request.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Prompt caching is designed for stable, repeatedly reused prefixes. The design must follow current platform semantics and data policy and should be verified with usage diagnostics. (B) A changing early field can invalidate the reusable prefix. (C) Credentials must never be stored in prompt text or cache. (D) Changing order prevents prefix reuse.

</details>

---

**Q71.** A policy assistant retrieves fifty documents for every question. Answers are slow and sometimes combine conflicting versions. What is the best redesign?

- **A)** Increase the response length so all documents are discussed.
- **B)** Tell Claude to ignore conflict without identifying it.
- **C)** Remove authorization filters so retrieval is faster.
- **D)** Retrieve the smallest relevant, permitted, authoritative, current set and attach provenance and conflict metadata.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

Retrieval should select high-quality evidence, not maximize volume. Authority, freshness, relevance, and access belong in the retrieval pipeline. (A) More generated text does not resolve noisy or conflicting evidence. (B) Conflict must be resolved by documented authority or surfaced. (C) Removing authorization creates a data exposure risk.

</details>

---

**Q72.** A prompt needs to call an internal search service that requires a credential. Where should the credential be stored?

- **A)** In the system prompt so Claude can copy it into the tool call
- **B)** In an example inside the repository
- **C)** In an approved secret manager, used by the application or connector without exposing the value to the model
- **D)** In the generated output with a warning

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Credentials belong in a secret-management boundary and should be supplied only to the authorized service call. (A) Prompt text may be logged or exposed and is not a secret store. (B) Repository examples are public or broadly accessible. (D) Outputting a credential is disclosure, regardless of warning.

</details>

---

**Q73.** Users in Business Unit A can retrieve confidential documents from Business Unit B because the model is instructed not to reveal them. What is the correct control?

- **A)** Make the non-disclosure instruction more forceful.
- **B)** Enforce identity-aware authorization before retrieval so unauthorized documents never enter the model context.
- **C)** Ask users to promise not to request other units' data.
- **D)** Filter the final answer after the model has processed all documents.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

Access control must prevent unauthorized data from reaching the model. Prompt instructions and output filtering are not substitutes for retrieval authorization. (A) Instructions do not enforce access control. (C) User promises are not a technical authorization mechanism. (D) Post-generation filtering is too late because the model already received the data.

</details>

---

**Q74.** A knowledge file has a recent upload timestamp but contains an older policy with no owner or review date. What is the primary risk?

- **A)** The system may treat stale or superseded content as authoritative because file metadata does not establish content freshness.
- **B)** The file will necessarily exceed the context window.
- **C)** The model will always refuse to read it.
- **D)** The document cannot contain any useful information.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Upload or modification time is not sufficient evidence of policy currency. Content version, effective date, authority, and ownership are needed. (B) File age does not determine context size. (C) A stale document is not inherently unreadable. (D) It may still be useful as historical or advisory evidence if labeled correctly.

</details>

---

**Q75.** A current public standard and a current approved internal standard give different minimum requirements. The internal standard applies to the organization and is stricter. What should the assistant do?

- **A)** Choose the shorter document.
- **B)** Blend the requirements and omit the difference.
- **C)** Select the public standard because it is public.
- **D)** Apply the documented authority and scope rules, cite both where useful, and state that the stricter internal standard governs the organization.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

Source resolution depends on authority and scope, not convenience. The conflict and governing rule should remain traceable. (A) Length has no relationship to authority. (B) Blending hides a material difference. (C) Public availability does not override an approved internal requirement within scope.

</details>

---
