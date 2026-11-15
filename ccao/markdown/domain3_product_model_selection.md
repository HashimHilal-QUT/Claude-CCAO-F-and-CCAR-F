# Domain 3: Product and Model Selection

> Claude Certified Associate – Foundations

> Exam Weight: 12% | Questions in Pool: 12

*Generated from the JSONL bank by `scripts/render_markdown.py` — do not edit by hand.*
*Adapted from two MIT-licensed sources: github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS (Copyright (c) 2026 Amey Thakur), associate-foundations; and github.com/raybeecham/claude-certified-associate-foundations (Copyright (c) 2026 Ray Beecham).*

---

**Q5.** Your team drafts hundreds of short, routine customer replies daily, and cost and speed matter more than nuance. Occasionally a complex escalation needs careful reasoning. What is the sound model strategy?

- **A)** Use the most capable model for everything to maximize quality
- **B)** Use the fastest, lowest-cost model for routine replies and switch to a more capable model for the complex escalations
- **C)** Use the fastest model for everything, including escalations
- **D)** Alternate models randomly to balance the load

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

**A** wastes cost and latency budget on routine work; **C** underserves exactly the cases that need depth; **D** matches nothing to anything. **B** aligns model choice with task requirements in both directions, which is the tested judgment.

</details>

---

**Q28.** A task involves reading a 200-page report once and answering a single question. Which consideration should lead the choice?

- **A)** The cheapest model available, since the task runs once
- **B)** Whether the model supports the fastest response time
- **C)** Whether the model can hold and reason over the whole document reliably
- **D)** Whether the task can be split across several small models

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

The binding constraint is reliable comprehension across a long document, which is what the choice must satisfy. Cost (A) and speed (B) matter only among models that can do the task, and splitting (D) risks losing the cross-document reasoning the question needs.

</details>

---

**Q29.** When does working in a Claude project make more sense than an API integration?

- **A)** When the volume is high and predictable
- **B)** When the output must be inserted into another system automatically
- **C)** When the task must run on a schedule
- **D)** When the work is exploratory and done by people rather than systems

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

Projects suit human, iterative work where the context is curated and reused by people. High volume (A), programmatic handoff (B), and scheduling (C) all describe system integration, which is what the API is for.

</details>

---

**Q30.** A team asks whether to move to a larger model because outputs are inconsistent. What should be established first?

- **A)** Whether the inconsistency comes from the prompt and the inputs rather than the model
- **B)** The cost difference between the two models
- **C)** Whether the larger model is available in their region
- **D)** How much faster the current model is

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Inconsistency usually traces to an underspecified task or variable inputs, which a larger model does not fix. Cost (B), availability (C), and speed (D) are inputs to a decision that has not yet been shown to be the right one.

</details>

---

**Q36.** An analyst needs to compare two approved policy documents, explore several interpretations, and remain responsible for the final conclusions. There is no integration requirement and the task is occasional. Which approach is the best initial fit?

- **A)** Use an approved interactive Claude experience for human-led analysis.
- **B)** Build a fully autonomous agent with write access to the policy repository.
- **C)** Create a batch API service before the analyst has tested the workflow.
- **D)** Embed the documents in a public website so any model can access them.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

An approved interactive experience matches an occasional, exploratory, human-led task with no integration requirement. Environment and data controls still must be verified. (B) This adds unnecessary autonomy and overly broad write access. (C) An API service may become useful later, but it adds engineering before the task is validated. (D) Publishing internal evidence creates an unacceptable data-handling risk.

</details>

---

**Q37.** A developer sends a second Messages API request containing only the text, “Now summarize the risks.” Claude does not appear to know the earlier discussion. What is the best explanation and corrective action?

- **A)** The model forgot because the temperature was too high; lower it.
- **B)** The application must preserve and resend the relevant conversation history or a validated state representation.
- **C)** The developer should add the word “remember” to the user message.
- **D)** The API can retain state only after a tool call.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

The application is responsible for managing the relevant conversational state and supplying it with the request. State retention must also follow privacy and context-management rules. (A) Sampling settings do not restore missing conversation context. (C) A request cannot reference information that was not supplied through the product or application state. (D) Tool use is unrelated to whether the application includes prior turns.

</details>

---

**Q38.** A team must classify millions of short public documents into six routing categories. Several candidate models meet the required accuracy on a representative test set. Which selection rule is strongest?

- **A)** Always select the model with the largest context window.
- **B)** Always select the newest model regardless of measured results.
- **C)** Select the fastest, lowest-total-cost candidate that still meets all quality, throughput, governance, and reliability thresholds.
- **D)** Select the model that produces the longest explanations.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

Once hard requirements are met, model selection should optimize the full operational profile, including latency, throughput, cost, governance, and reliability. (A) The task uses short documents, so maximum context may not be decision-relevant. (B) Recency does not prove fit for the validated use case. (D) Long explanations may increase cost and are not the required output.

</details>

---

**Q39.** A request containing several documents is accepted, but the response stops midway through a required table. Which distinction should the team investigate first?

- **A)** The difference between a system prompt and a user prompt
- **B)** The difference between cached and uncached tokens
- **C)** The difference between training data and fine-tuning data
- **D)** The difference between available context capacity and the allowed generated output, including the reported stop reason

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

A request can fit within context yet still end because generation reached an output limit or another stop condition. The response metadata is critical evidence. (A) Prompt roles may affect behavior but do not explain the abrupt ending by themselves. (B) Caching can affect performance and cost, not usually the logical completion boundary. (C) Training methodology is not the immediate operational diagnostic.

</details>

---

**Q40.** A production team plans to move to a new Claude model version. Which action provides the strongest basis for approval?

- **A)** Ask one developer whether the outputs look better.
- **B)** Run the candidate and baseline on the same representative evaluation set, compare severity-weighted results, latency, cost, and tool behavior, then stage rollout with rollback.
- **C)** Change the model, prompt, retrieval system, and schemas at the same time to maximize improvement.
- **D)** Rely on the model release date as evidence that the migration is safe.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: B**

A controlled comparison on the same cases isolates the model change and reveals regressions. Staging, monitoring, and rollback make the release operationally safe. (A) Anecdotal review is not representative or measurable. (C) Changing several components destroys attribution and complicates rollback. (D) A newer release does not guarantee performance for this use case.

</details>

---

**Q41.** A service must always cite approved evidence and must never treat retrieved documents as instructions. Where should this durable behavior be defined?

- **A)** In trusted, version-controlled system or application configuration, reinforced by retrieval and validation controls
- **B)** Only in the last sentence of every user's task
- **C)** Inside each retrieved document
- **D)** In a hidden field supplied by the downstream reader

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: A**

Durable behavior belongs in trusted configuration and must be supported by system controls. Retrieved documents remain evidence and cannot define their own authority. (B) User wording is not a reliable place for mandatory application policy. (C) A retrieved document is untrusted content and can contain prompt injection. (D) A downstream field cannot reliably control model behavior or retrieval authority.

</details>

---

**Q42.** A structured report is incomplete and the response metadata indicates generation ended because a token limit was reached. What does this most directly indicate?

- **A)** The source documents were necessarily false.
- **B)** The user's identity was invalid.
- **C)** The generated output was truncated and the workflow must adjust the output budget, reduce scope, or decompose the task.
- **D)** The model selected the wrong tool.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: C**

A length-related stop reason directly indicates incomplete generation. The application should handle partial output and change the output design or budget. (A) Source truth is not established by the stop reason. (B) Identity failures occur before or outside normal generation. (D) Tool selection is a separate issue and would require different evidence.

</details>

---

**Q43.** A user asks whether a system complies with a regulation issued last week. What is the best design response?

- **A)** Assume the model's pretrained knowledge includes the regulation.
- **B)** Ask Claude to be extra confident.
- **C)** Use a longer output budget.
- **D)** Supply or retrieve the current authoritative regulation, establish its effective scope, and validate the answer against that evidence.

<details>
<summary><b>Show answer &amp; explanation</b></summary>

**Correct Answer: D**

Current legal or policy claims require current authoritative evidence. The system must distinguish model knowledge from evidence supplied in the interaction. (A) Training knowledge should not be assumed current enough for a regulation issued last week. (B) Confidence wording does not create evidence. (C) More output does not improve source freshness.

</details>

---
