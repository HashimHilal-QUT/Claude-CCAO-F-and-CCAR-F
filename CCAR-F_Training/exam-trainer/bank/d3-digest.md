# Domain 3 grounding digest: Claude Code Configuration and Workflows (20%)

The core judgment: which artifact holds an instruction, at which scope, so it loads when it matters and costs nothing otherwise. CLAUDE.md and rule files are advisory; anything that must hold every time belongs in a hook or permission rule.

## 3.1 CLAUDE.md hierarchy, scoping, modular organization

- **Scopes:** managed policy (deployed by IT), user `~/.claude/CLAUDE.md`, project `./CLAUDE.md` or `./.claude/CLAUDE.md` (equivalent locations), and gitignored `./CLAUDE.local.md`. Subdirectory CLAUDE.md files load on demand, the first time Claude reads a file in that directory.
- **Additive, not overriding.** All discovered files are concatenated root-down into context. Load order decides what is read first, never what wins. A user-versus-project contradiction is a coin flip. Fix it by deleting the conflicting line, not by moving files or adding emphasis.
- **User scope is never shared.** "Teammate or CI is not getting the conventions" means check the config location first. The fix is moving content to project scope and committing it. CLAUDE.local.md is personal and never committed.
- **`@path` imports** split a file into topic files for ownership and fewer merge conflicts. They expand at launch (max four hops, relative to the importing file), so they organize but do not economize. They are never conditional loading.
- **Budget:** root file under about 200 lines, only what Claude cannot derive; bloat gets rules ignored.
- **Tempting wrong answers:** user-level file for team rules, "project overrides user", `.claude/CLAUDE.md` loading later and so winning, CAPITALS or repetition as precedence, imports to cut tokens, managed policy as a gate.
- **Flip words:** "every contributor/CI" means project scope. "Only me, all projects" means user scope. "Personal but project-specific" means CLAUDE.local.md. "Must hold every time" means a hook.

## 3.2 Custom slash commands and skills

- **Locations:** project `.claude/skills/<name>/SKILL.md` or `.claude/commands/<name>.md` (committed, shared). Personal `~/.claude/skills/` or `~/.claude/commands/` (only you). Commands and skills are one mechanism. Skills add a folder for supporting files and automatic activation. A command name comes from the file name.
- **Name collision:** enterprise beats personal beats project. A stale personal skill silently shadows the team's. This is the opposite of the CLAUDE.md intuition.
- **Frontmatter semantics:**
  - `disable-model-invocation: true` makes a skill user-only, for side effects. `user-invocable: false` is the mirror: Claude-only.
  - `argument-hint` is autocomplete text and never validates or binds. `arguments` binds named placeholders (`arguments: version` gives `$version`). `$ARGUMENTS` and `$0` work positionally.
  - `allowed-tools` pre-approves listed tools for the invoking turn only and restricts nothing. Use `disallowed-tools` or permission settings to remove tools. Use `permissions.allow` in `.claude/settings.json` for a session-wide grant.
  - `context: fork` runs the skill in an isolated subagent whose prompt is the skill body, with no conversation history. It is the answer to "exploration floods the main session". The body must be an explicit self-contained task, because guidelines-only bodies return nothing. `agent: Explore` picks the subagent type. Forks run in the background by default, and `background: false` returns the result in the same turn.
  - `` !`command` `` runs before Claude sees the body. A failure aborts the invocation.
- **Wrong answers:** `~/.claude/commands` for a team command, CLAUDE.md for a procedure, `allowed-tools` to hide output or block tools, `argument-hint` to enforce input, fork on a conventions-only skill.
- **Flip words:** "available to all contributors" means project scope. "Never fires on its own" or "side effects" means disable-model-invocation. "Keep main context clean" means context: fork.

## 3.3 Path-specific rules

- `.claude/rules/*.md` with `paths:` globs loads only when Claude reads a matching file. A rule without `paths` loads every session. This is the fix for per-area bloat and for contradictory conventions between packages.
- **Globs:** `*` matches within one directory level, `**` matches any depth. `**/*.test.tsx` matches anywhere, and `src/**/*.{ts,tsx}` uses brace expansion. `schemas/*.json` misses nested files.
- **Rule vs directory CLAUDE.md:** a directory file suits owners keeping a file beside their code. A central rule suits a file type or a convention spanning scattered paths. A directory CLAUDE.md cannot target file patterns.
- Rules are not re-injected after `/compact`. They reload on the next matching read. Debug with `/memory` (and `/context`): a file missing from the list is the problem.
- **Wrong answers:** CLAUDE.md "path prefixes" or headings (they do not exist), `@import` for conditional loading, a directory CLAUDE.md for a file-type rule, user-level rules for team conventions.

## 3.4 Plan mode vs direct execution

- **Plan mode:** Claude reads and proposes, and edits are blocked until approval. Enter it with Shift+Tab, `/plan`, or `claude --permission-mode plan`. Make it the project default with `permissions.defaultMode: "plan"`. Ctrl+G edits the plan and is the cheapest correction.
- **Choose plan mode** when the diff cannot be described in one sentence, the change spans several files, there are multiple valid approaches, the code is unfamiliar, the area is risky, or the change is hard to reverse or architectural.
- **Choose direct execution** for a clear stack trace, a single-file fix, or a mechanical change such as a rename, version bump, or typo.
- Plan mode is a workflow control, not a security boundary: its blocks are not enforced where bypass permissions are available.
- **Wrong answers:** planning a one-line hotfix, direct execution of a multi-package refactor, plan mode as a guarantee.

## 3.5 Iterative refinement

- Convergence needs a signal Claude can read. Supply concrete input and output examples (edge cases included), a failing test first, or a screenshot comparison. Otherwise the human is the verification loop.
- **Interview pattern** for ambiguous requirements: Claude interviews you, writes a spec file, then a fresh session executes it.
- **Refine sequentially, then fan out.** Converge the prompt on 2 or 3 samples before running `claude -p` across many independent files.
- After two failed corrections, clear context and write a better prompt.
- Escalate a test gate from a prompt request, to an evaluator, to a Stop hook that blocks the turn until tests pass. Evidence beats assertion.

## 3.6 CI/CD integration

- `-p`/`--print` is the only non-interactive mode. Without it the job hangs on a clarifying question. `--ci-mode`, `--batch`, `--headless`, and `CLAUDE_HEADLESS` are fabricated.
- `--output-format json` with `--json-schema` puts output in `structured_output`. Gate with `jq -e` on a field, never by grepping prose.
- `--setting-sources project` loads committed config and skips user and local config. `--bare` skips hooks, skills, plugins, MCP, memory, and CLAUDE.md, and needs `ANTHROPIC_API_KEY`.
- Pipe the diff on stdin rather than granting Bash. `Bash(git diff *)` differs from `Bash(git diff*)`, which also matches `git diff-index`.
- **Fresh session per job:** review in a new session, not the one that wrote the code. Deduplicate by passing prior PR comments as context. CLAUDE.md supplies shared standards to each session. Batches suit no blocking check.
