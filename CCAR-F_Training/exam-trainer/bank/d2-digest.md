# Domain 2 digest: Tool Design and MCP Integration (18%)

Items give a working-but-degrading system and ask which structural change fixes the root cause. The best answer changes the contract: the description, schema, error payload, tool set, scope, or primitive. It does not reword a prompt. Distractors fix symptoms: a prompt rule for a bad description, a retry for a denial, `tool_choice` for too many tools, a subagent for a language problem.

## 2.1 Tool interfaces and descriptions

- The model sees only the name, the description, and the parameter descriptions, and the description is the top factor in tool performance. Write at least 3-4 sentences: the outcome, when to call it, when not to, input format, return shape, and edge-case behaviour.
- Negative boundaries matter most. Say what the tool does not return and name the alternative tool. Without that, the agent repeats calls hoping missing data appears.
- Near-synonym descriptions make selection close to random. Fix them with mutually exclusive boundaries and namespaced, meaningful names (`search_public_web`, `jira_issues_search`).
- Misrouting fix order: rename and split, then expand descriptions, then few-shot examples, and classifiers or architecture last. A custom tool losing to built-in Grep also gets the description fix first.
- Consolidate tools always called in sequence, endpoint-mirror tools, and same-resource verbs (behind an `action` parameter). Split when risk differs (plan vs apply), when return shapes differ, or when a parameter is required only if another has a certain value.
- Constraint words: "always called together" means consolidate. "Rarely needed" or "slow or billed upstream" means do not merge. "Cannot rely on instructions" means split on risk and withhold the risky tool. "First step" or "lowest complexity" means fix names and descriptions.

## 2.2 Structured errors

- **Two channels.** JSON-RPC protocol errors cover an unknown tool, a malformed request, or a server fault. Anything a well-formed call reached, where your logic decided the outcome, is a result with `isError: true` plus actionable prose. That includes upstream failures, validation, business rules, and permissions. Models recover from results, not from protocol errors.
- **Silent failures.** Returning `[]` on a timeout makes an outage look like zero records. An uncaught exception leaves the model with no context. Both are anti-patterns.
- **Classes:**
  - Transient: retry, bounded, with a hint.
  - Validation: fix the input or escalate.
  - Business: not retryable; change the plan, and the error names the rule and a `next_action`.
  - Permission: not retryable; stop and escalate, name the scope, never widen it automatically.
- Classification overrides the retry counter. Lowering the retry cap on a denial treats a symptom.
- Put prose in `content` for the model. Put `error_class`, `retryable`, `retry_after_seconds`, and `correlation_id` in `structuredContent` for orchestration code. Never regex the prose, and never strip it.
- A subagent retries its own transient failures and escalates a structured error only when retries run out. The coordinator keeps partial results and reports the gap; aborting the whole run is wrong.
- Wrong patterns: generic "try again" messages; business or permission errors sent as JSON-RPC errors; `isError: false` on a failure.

## 2.3 Distribution and tool_choice

- Every tool costs context and adds a candidate to every selection. For a crowded catalog, consolidate first, then distribute across role-based agents, then fix descriptions. Deferral or tool search comes last, because it cuts cost without fixing overlap.
- Subagent `tools` is an allowlist; omitting it inherits everything. `disallowedTools` is a denylist that fails by omission: denying `Write` leaves `Edit` and `Bash`. Prefer allowlists. Declare `mcpServers` inline in the one subagent that needs them.
- **Three separate levers:** distribution (which tools an agent has), permission (which calls run without a prompt), and `tool_choice` (whether a request may end without a tool call).
- **`tool_choice` values:**
  - `auto`: default, for exploratory loops.
  - `any`: some call is required and the model picks; use when several schemas are acceptable.
  - `tool` plus `name`: one schema is the deliverable.
  - `none`: final summary turn.
- Wrong patterns: `any` on every loop turn; `none` to suppress one tool; forcing a call to hide a bad description.

## 2.4 MCP integration

- **Scopes.** Local is the default for `claude mcp add` and private. Project scope is `.mcp.json` at the repo root, committed and shared. User scope is private and applies across all your projects. For duplicate names, precedence is local > project > user, and the winning entry is used whole, never merged. "Teammates lack the tools" means move the server to `.mcp.json`.
- **Secrets.** Use `${VAR}` with no default for secrets and `${VAR:-default}` for endpoints and paths. An unset variable still loads: `claude mcp list` warns and the literal text is sent, so it shows up later as an auth failure. The fix is to inject the variable, never to add a default token. HTTP entries need `type`.
- **Primitives by control.** Tools are model-controlled. Resources are application-driven: catalogs with stable URIs, where the model does not guess names. Prompts are user-controlled, invoked deliberately as slash commands. Large document sets become resources; human-started workflows become prompts.
- Tools are addressed as `mcp__server__tool` in permissions and `tools` lists.
- Annotations such as `readOnlyHint` are untrusted hints, never authorization. Enforce with permission rules on the exact tool name, scoped credentials, and the tool set you grant.

## 2.5 Built-in tools

- **Grep** searches contents and respects `.gitignore`. Its modes are `files_with_matches`, `content`, and `count`.
- **Glob** matches names and paths, never contents, and ignores `.gitignore`.
- **Read** comes after Grep or Glob. "Read all files first" is the classic distractor.
- **Write** fully overwrites. **Edit** needs a unique `old_string`, so widen a non-unique anchor with surrounding lines. `replace_all` changes every match. Read plus Write is the fallback only when no unique anchor exists, and full rewrites of large files risk dropping code.
- **Bash** runs each call as a separate process. The working directory persists; environment variables do not. Using Bash for search loses structured output, truncation flags, and precise permission rules, because rules against Bash must match command strings.
