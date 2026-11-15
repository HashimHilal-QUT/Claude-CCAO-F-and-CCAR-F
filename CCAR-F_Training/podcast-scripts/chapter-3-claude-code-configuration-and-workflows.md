# Chapter three: Claude Code Configuration and Workflows

## Cold open

Before any theory, let's start with a story.

A contractor joins a team on a Monday. She clones the repository. She starts Claude Code. And she asks it to add a new error type to the refund tool.

Claude writes something clean. Sensible. And completely wrong for this team. It invents its own error categories. It ignores the naming pattern everyone else uses.

The lead engineer is baffled. On his laptop, Claude has followed those conventions perfectly for three weeks. So he checks her setup. Then his own. And there it is.

Every one of those conventions lives in a file in his home folder. It was never committed. It never left his machine. For three weeks, the team's standards had a membership of one.

[beat]

That story is the whole of this chapter in miniature.

Claude Code behaves the way its files tell it to behave. And one question keeps coming back. Which file holds which instruction? Who receives that file? And when does it get read?

Get the location wrong, and the instruction silently goes missing for someone. Get the loading wrong, and you pay for instructions nobody needed. Or you miss the one that mattered.

[beat]

This is Domain three of the Claude Certified Architect, Foundations exam. Claude Code configuration and workflows. It carries twenty percent of the exam. So roughly one question in five.

We'll take it in six parts, one per official task statement.

Part one is the instruction file called CLAUDE.md, and how its levels stack.

Part two is custom slash commands and skills.

Part three is path-specific rules that load only for certain files.

Part four is when to plan first, and when to just do the work.

Part five is iterative refinement. Meaning, how to make a loop of attempts actually converge.

Part six is running Claude Code inside automated pipelines.

Then a rapid trap round. And a recap of ten things to remember.

[beat]

One idea runs underneath all six parts. So let me say it now.

Everything in this domain that is written as prose is advice. Claude reads it. Weighs it. And usually follows it. But none of it can stop anything from happening.

So when a question says something must happen every time, the answer is never a better-worded sentence. It's code that runs at a fixed moment, and can say no.

Or, in four words. Prose advises. Code enforces.

Hold on to that. It decides a surprising number of questions.

## Part one: CLAUDE.md hierarchy, scoping and modular organization

Part one. The CLAUDE.md hierarchy.

By the end of this part, you'll know where the instruction file can live, how its levels combine, how to split it up, and why no amount of emphasis turns it into a lock.

[beat]

Let's start with the plain version.

Imagine a whiteboard by the door of a workshop. It's read aloud at the start of every shift.

Several parties are allowed to write on it. The organization's IT department can write on it. You can write on it. The project you're working on can write on it. And you can add a private sticky note that only you ever see.

Two things about this whiteboard matter.

First. Nobody has an eraser. Everything anyone wrote gets read out, every shift, in a fixed order.

Second. Reading it out costs attention. A crowded board buries the lines that matter.

[beat]

The technical name for that whiteboard is CLAUDE.md.

It's a plain text file of standing instructions. Claude Code loads it into context before your conversation even starts. The course video calls it persistent context. That's a good two-word summary.

And there are several places it can live. In exam terms, these are scopes.

[beat]

The study notes, checked against current documentation, name four scopes. Here they are in load order, from broadest to most specific.

One. A managed policy file that IT deploys to a protected operating-system location.

Two. Your user file, at ~/.claude/CLAUDE.md. It lives in your home folder, and it applies to every project you open.

Three. The project file. It can sit at the repository root as ./CLAUDE.md. Or inside the .claude folder at the root, as ./.claude/CLAUDE.md. Those two project locations are equivalent. Pick whichever your team prefers.

Four. A local file called CLAUDE.local.md, at the repository root. It's personal, and it's ignored by version control. So it is never committed.

[beat]

Now the first source disagreement you need to know about.

The course video describes three levels. User, project, and directory.

The notes describe four scopes. Managed policy, user, project, and local. And they treat directory files as a loading behavior of the project scope.

Are these in conflict? Not really. They slice the same system differently. The video's third level, a CLAUDE.md inside a subdirectory, is real. We'll come to it.

So. If a question lists three levels, answer in its terms. If it mentions managed policy or the local file, you now know where they sit.

[beat]

How do these files load?

Claude Code starts from the folder you launched it in. It walks up the tree. And it loads every CLAUDE.md and CLAUDE.local.md it finds, stitching them together from the top of the filesystem down toward your working folder.

In each folder, the local file is appended after the regular one.

And files in subfolders below where you started? They don't load at launch. They load on demand, the first time Claude reads a file in that subfolder.

Quick recap before the first question. Four scopes. Stitched together from the top down. Subfolder files wait until they're needed.

[beat]

Question one. Practice question D3-001. The course presenter flagged this scenario directly as an exam question.

Here's the scenario. A teammate isn't getting the conventions. Claude works perfectly for one person, and acts as if it has never heard of the project for another.

The conventions live in the lead's user file, in his home folder. A contractor cloned the repository last week, and Claude ignores them.

The stem adds a constraint. The fix must reach every contributor, and the continuous integration job, which is the automated build that runs on a server. And it must work without any per-machine setup.

What's the fix?

Take a second.

The answer. The presenter's advice was blunt: check the config location first. Then move the conventions into the project CLAUDE.md, and commit it.

[beat]

Here's the plain version. It's like pinning the house rules to your own bedroom door instead of the fridge. You see them every day, so they feel shared. But your new flatmate never walks into your room. Move the note to the fridge, where everyone looks, and the problem disappears.

In exam terms, version control is the distribution mechanism. Every clone, and every pipeline checkout, gets the file on pull.

[beat]

Now the wrong turns.

Wrong: ask the contractor to copy the file into her own home folder, and keep the copies in sync. Why? It fails the no-per-machine-setup constraint. It drifts as the conventions change. And it never reaches the build server.

Wrong: put the conventions in CLAUDE.local.md, beside the code. Why? It sounds shared, because it sits in the repository folder. But the local file is the personal, ignored scope. It's never committed. So neither the contractor nor the pipeline gets it.

Wrong: add an import line in the lead's user file, pointing at a conventions file inside the repository. This is the cleverest distractor. Why is it wrong? The import sits in a file only the lead has. Anyone without that file never follows the import.

[beat]

Listen for three constraint words. Every contributor. The pipeline. No per-machine setup. Those three together mean project scope, committed.

Hold on to this line. User scope is never shared. So when a teammate is missing the conventions, check where the file lives.

[beat]

Now the second big idea in this part. And it's the one the exam leans on hardest.

Remember the whiteboard with no eraser? The scopes are additive. They do not override each other.

All discovered content lands in context at once. And when two instructions contradict each other, Claude reconciles them by judgment, turn by turn.

[beat]

Question two. Practice question D3-002.

Here's the scenario. A developer's user file says: write commit messages as a single imperative sentence. The project file says: use Conventional Commits. That's a structured format with a type, a scope in brackets, and a summary.

Claude follows one format on some commits, and the other format on others. The developer wants the project rule to hold in this repository, without changing their other repositories.

What should they do?

Take a second.

The answer. Delete the commit-format line from the user file. And keep user scope for preferences a project will not contradict. A commit format is a project decision.

[beat]

Here's the plain version. Two notes on the same fridge. Yours says buy oat milk. The household's says buy dairy milk. Whoever shops has to guess, and they guess differently each week. Writing the household note bigger doesn't settle it. Taking your note down does.

The notes put it memorably. Hold on to this line. If your user file says always use one package manager, and the project file says another, you have not configured precedence. You have configured a coin flip.

[beat]

Now the wrong turns. They're all attempts to out-rank, rather than remove.

Wrong: move the project rule into ./.claude/CLAUDE.md, because it loads later and therefore wins. Why? It's wrong twice. The two project locations are equivalent. And load order decides what is read first, never what wins.

Wrong: restate the rule in capitals, with a note that project instructions always override user instructions. Why? Emphasis does not create precedence. Both lines stay in context.

Wrong: copy the project rule into the local file, so it appears twice and outweighs the user line. Why? Repetition is not a weighting rule. The contradiction remains. And now you pay for the text twice.

[beat]

A related question from the notes.

A senior engineer's user file says: always run the full test suite. The project file says: never run the full suite locally, because it takes forty minutes. And the engineer files a bug saying project scope should override user scope.

What's the accurate assessment? There are no override semantics to be broken. Nothing is corrupted. Remove the contradiction. And if the behavior must be guaranteed, use a hook. We'll come to that in a moment.

So remember. CLAUDE.md scopes are additive. Fix a contradiction by deleting a line. Never by moving files, or shouting.

[beat]

Next, modularity.

Plain version first. Picture a staff handbook where each department writes its own chapter, in its own document. The front page simply says: testing, see chapter three.

Everyone still gets the whole handbook on day one. The only change is that two departments no longer fight over the same page.

[beat]

The technical name is an import.

Inside a CLAUDE.md, you write an at sign followed by a path to another file. For example, @docs/testing-conventions.md. When Claude Code launches, that referenced file is expanded into context, right alongside the file that references it.

A few precise details. Four of them.

One. Relative paths resolve from the importing file, not from the folder you launched in.

Two. Imports can nest, up to a maximum depth of four hops.

Three. An at sign inside a code span, meaning the text between backticks, is left alone.

Four. An import in a project file that points outside the working folder, such as into your home folder, triggers a one-time approval dialog.

[beat]

The course presenter flagged this as an exam scenario too. How do you make CLAUDE.md modular? The import is the mechanism.

His framing was ownership. The backend team edits the API patterns file. The testing team edits the testing file. And the root file stops being a merge-conflict battleground. Clean pull requests. Clean ownership.

[beat]

Question three. Practice question D3-003. This one turns on a subtle point.

Here's the scenario. A platform team's root file holds API patterns, testing conventions, and deployment rules. Claude genuinely needs all of it, in every session. Two teams keep colliding in merge conflicts. They want separate files. And they accept that total context per session stays the same.

What should they do?

Take a second.

The answer. Split the sections into topic files, and import each one from the root.

Here's the key line from the notes. Hold on to it. Imports organize. They do not economize.

An imported file still loads at launch. It still costs the same tokens as if it were pasted inline. And in this question, that's exactly what the team wants.

[beat]

Now the wrong turns. Every other option changes when the content loads.

Wrong: move the sections into rule files with path patterns. Why? That makes them conditional. So guidance needed every session goes missing whenever no matching file is read.

Wrong: move them into subfolder CLAUDE.md files. Why? That makes them load on demand. So they're absent from sessions working elsewhere.

Wrong: convert them into skills. Why? That makes them load on demand too.

The deciding phrase is: needed in every session.

[beat]

Now flip that question around, and the answer flips.

A teammate splits a six-hundred-line CLAUDE.md into eight imported files, and announces the context problem is solved. Is it? No. Startup context is unchanged.

If the goal is a smaller footprint, the tools are conditional loading, meaning path-scoped rules or skills. Plus deleting anything Claude can work out from the code itself.

And one small freebie from the notes: block-level HTML comments in a CLAUDE.md are stripped before injection. So maintainer notes cost nothing.

So remember. An import is for ownership and tidiness. Never for saving tokens. And never for conditional loading.

[beat]

Now the directory level.

Plain version. Think of an office building where each department tapes its own notice inside its own door. People read it only when they walk into that department. And each department updates its sign without asking reception.

In exam terms, you can put a CLAUDE.md inside any subfolder, such as packages/coordinator. It loads when Claude reads a file there. Or at launch, if you start Claude in that folder.

[beat]

Question four. Practice question D3-004.

Here's the scenario. A monorepo, meaning one repository holding several packages. There's a coordinator package, a web-search agent package, and a synthesis agent package. Each has its own owning team.

Each team wants its conventions in a file right next to its own code, reviewed in its own pull requests. And when an engineer works only in the coordinator, the web-search conventions should not be in context.

What's the right setup?

Take a second.

The answer. A CLAUDE.md inside each package directory, owned by that team.

[beat]

Now the wrong turns.

Wrong: put all three sections in the root file, under headings like "For packages/web-search-agent/." Why? CLAUDE.md has no path-prefix scoping. Those headings are plain text. So everything loads, every session. The course presenter named this one directly: CLAUDE.md with path prefixes does not work.

Wrong: keep a short root file, and import each package's conventions. Why? Imports expand at launch. So everything loads, including during coordinator-only work.

Wrong: central rule files at the root, with a path pattern per package, maintained by a central team. This is the subtle one. Why is it wrong? It does load conditionally. But it fails on ownership. The files sit centrally, not beside each team's code.

[beat]

We'll come back to the rule-versus-directory-file contrast in part three, because it's a favorite.

Hold on to this line. A subfolder CLAUDE.md loads on demand, and suits teams that own the code beside it.

[beat]

Last concept in this part. It ties back to the theme of the cold open.

Question five. Practice question D3-005.

Here's the scenario. The project file says: never commit directly to main. Claude complies early in sessions. But in long sessions, it has twice committed to main anyway. The release manager says the rule must hold every single time, for every contributor.

What's the fix?

Take a second.

The answer. A hook. Specifically, a PreToolUse hook.

Here's the plain version. A sign on the door saying please lock up works most nights. But not on the night someone is tired. If the door must be locked every time, you fit a lock that closes itself. A bigger sign, or one signed by the landlord, is still just a sign.

[beat]

In exam terms. Every CLAUDE.md scope, managed policy included, and every rule file, is advisory context. None of them can block an action.

A PreToolUse hook is a small script Claude Code runs before a tool call. Here, it checks whether a shell command is a git commit or git push while the current branch is main. And if so, it refuses it.

The notes call this the enforcement ladder. Three rungs.

First. Withhold the capability entirely.

Second. Deny it in code, with a hook.

Third. Validate a record afterwards.

A strongly worded sentence is none of the three.

[beat]

Now the wrong turns.

Wrong: put it on the first line, in capitals, prefixed with critical. Why? It's still advisory prose, competing with the whole context window. It can be missed, or summarized away, in a long session.

Wrong: ask IT to put it in the managed policy file. Why? That file cannot be excluded by individuals, which sounds like enforcement. But it's still CLAUDE.md content. Advice Claude weighs. Not a gate.

Wrong: put it in a rule file whose pattern matches every file, so it reloads constantly. Why? A rule is still text. And reloading text does not stop a commit.

[beat]

The constraint words are every single time, and must hold. Those words always point to a hook, or a permission rule.

We'll meet hooks again in part five. And they're covered in depth in the chapter on agentic architecture.

[beat]

A few supporting facts round out this task statement. Three of them.

One. Keep the root CLAUDE.md short. Under about two hundred lines. It should hold only what Claude cannot derive from the code, because a bloated file gets rules ignored. The notes' test: ask of each line, would removing it cause a mistake?

Two. There's a setting called claudeMdExcludes. It skips ancestor CLAUDE.md files by absolute path pattern. But it cannot exclude the managed policy file. Why? Because a policy an individual can erase is not a policy.

Three. The root project CLAUDE.md is re-read from disk and re-injected after the conversation is compacted. Subfolder files and path-scoped rules are not. We'll use that last fact in part three.

[beat]

Now a contrast segment, because the exam loves routing questions. Where does a given instruction belong?

Here's the routing, in plain terms. Six destinations.

One. A short fact every session needs, like run commands from the package folder. That goes in the project CLAUDE.md.

Two. A convention for one file type, like how React components are declared. That goes in a path-scoped rule.

Three. Reference material needed only sometimes, like a detailed API response format. That goes in a skill.

Four. A side-effecting procedure a human should time, like cutting a release. That goes in a skill or command that only a human can trigger.

Five. Something that must never happen, like committing to main. That goes in a hook.

Six. Something project-specific but personal, like your sandbox address and your seeded test account. That goes in CLAUDE.local.md.

[beat]

And the flip words.

Every contributor, or the pipeline, means project scope.

Only me, in all my projects, means user scope.

Personal, but only for this project, means the local file.

Must hold every time means a hook.

[beat]

That's part one.

If you remember one thing, make it this. CLAUDE.md is a shared briefing, not a lock. Route each instruction by who needs it, and when it should load.

Coming up in part two: custom slash commands and skills.

## Part two: Custom slash commands and skills

Part two. Custom slash commands and skills.

By the end of this part, you'll know how a skill is built, which switches decide who can start it, what its argument and tool fields really do, and how to run it in its own space.

[beat]

Plain version first.

Some instructions you want read out every shift. Others you need a few times a month. Reading those out every shift would be a waste.

For those, you want a procedure card in a labeled drawer. It's pulled out only when the job calls for it.

And because the card is pulled only when something matches, the label on the drawer does more work than anything written on the card.

[beat]

The technical name for the card is a skill.

A skill is a folder containing a file called SKILL.md. That file starts with a short header block called frontmatter, written in a simple key-and-value format. After that comes the body, which is the actual instructions.

How does a skill get triggered? Two ways. A person can type a slash and its name. That's why skills show up as slash commands. Or Claude can load it automatically, when it judges the skill relevant.

The description field in the frontmatter is what Claude reads when deciding whether to load it. So the description is the selection signal. It's not documentation.

[beat]

Where do skills live? The same logic as part one.

Project skills go in .claude/skills/, in a folder named for the skill, holding SKILL.md. They're committed and shared.

Personal skills go in ~/.claude/skills/. Only you have them.

Enterprise skills arrive through managed settings.

And plugin skills are namespaced with the plugin name and a colon, so they can't collide.

[beat]

Now the second source disagreement.

The lesson eleven slide deck treats custom slash commands and skills as two separate features.

The notes, checked against current documentation, say custom commands have merged into skills. A file at .claude/commands/deploy.md, and a skill at .claude/skills/deploy/SKILL.md, both create /deploy. And they behave the same way.

Command files still work. They take their name from the file name. And they accept the same frontmatter, except the name and paths fields, which command files ignore.

What does the skill layout add? A folder for supporting files, and automatic activation.

So if a question asks you to distinguish them, the honest answer is packaging and automatic activation. Not capability. And if a question treats them as separate features, answer in its terms.

[beat]

Here's a genuinely surprising fact. And it's a known trap.

When two skills share a name, one has to win. Why? Because a lookup by name has to return exactly one thing.

The order is: enterprise beats personal. And personal beats project. Your personal skill beats the team's.

That's the opposite of the intuition from CLAUDE.md. The notes explain why it isn't inconsistent. Hold on to this line. A merge never has to choose. A lookup always does.

[beat]

Here's the failure story from the notes.

An engineer wrote a personal deploy-staging skill months ago, while prototyping. It points at a cluster that no longer exists. Their invocations fail, while everyone else's succeed. Why? The stale personal skill silently shadows the committed team skill.

The remedy is to delete or rename the personal file.

Distractors will say the project skill takes precedence. Or that both skills concatenate, like CLAUDE.md files. Neither is true.

So remember. Skills resolve by name, with personal above project. That's the reverse of how CLAUDE.md behaves.

[beat]

Question one. Practice question D3-006. This one combines scope with the first frontmatter switch.

Here's the scenario. An engineer built a security audit command in their personal commands folder. It scans dependencies and opens tickets. Teammates get command not found.

The team wants three things. One, available to every contributor. Two, reviewed in pull requests like other code. Three, never triggered by Claude on its own initiative, because it creates tickets.

What should they do?

Take a second.

The answer. Commit it as a project skill. And set a frontmatter field called disable-model-invocation to true.

[beat]

Here's the plain version. It's like keeping the team's fire-drill checklist in your own desk drawer. It works perfectly for you, and nobody else can find it. Put it in the shared binder instead. And mark it: only a manager starts this drill. That way nobody sets off the alarm by accident.

In exam terms, disable-model-invocation set to true makes the skill user-only. It runs when a person types the slash command. Claude will never start it on its own. That's the right control for anything with side effects.

[beat]

Now the tempting mirror. There's another field called user-invocable. Setting it to false does the reverse. It hides the skill from people, and makes it Claude-only. That suits background knowledge that isn't a meaningful user action.

The exam places these two side by side, and hopes you grab the wrong one.

[beat]

Now the other wrong turns.

Wrong: keep it in the personal skills folder with the right switch, and share it on a wiki. Why? A wiki is not distribution. And it's never reviewed in a pull request.

Wrong: put the audit procedure into CLAUDE.md, with a line saying only run this when asked. Why? Three reasons. It pays for the procedure in every session. It can't actually stop Claude acting. And it doesn't create a slash command at all.

[beat]

A worked example from the notes pulls several fields together.

A release-candidate skill, in the project skills folder. It has disable-model-invocation set to true, so only a human fires it. It has narrow pre-approved tools, for git tag, git push, and opening a pull request. And its body says: cut release candidate for the given version and target branch.

That's the shape of a well-built side-effecting procedure.

Hold on to this line. disable-model-invocation true means only a human can start it. user-invocable false means only Claude can.

[beat]

Next, arguments.

Question two. Practice question D3-008.

Here's the scenario. A support team built a triage-ticket skill. The frontmatter says argument-hint, with ticket-id in square brackets. The body says: fetch ticket $ticket and classify it.

An engineer types /triage-ticket followed by the ticket number four eight two one three. And the literal text $ticket reaches Claude, instead of the number.

What's wrong?

Take a second.

The answer. argument-hint is autocomplete text only. Binding a named placeholder is a separate field, called arguments.

Plain version. A form field labeled ticket number tells you what to type. But if nobody wired that field to the system, whatever you type goes nowhere. The label is the hint. The wiring is what carries the value through.

[beat]

In exam terms, argument-hint shows in the menu, to remind you what to type. It never validates. And it never binds.

The arguments field is different. Its names map to argument positions, in order. So setting arguments to ticket makes $ticket resolve to the first argument.

You can also use positional placeholders. Three forms. $ARGUMENTS, for everything typed. $ARGUMENTS followed by an index, for a single position. Or the shorthand: $0, $1, and so on.

[beat]

Now the wrong turns.

Wrong: rewrite the hint to say required. Why? As if a hint could validate. It can't, whatever you write inside it.

Wrong: add a tool pre-approval for a web-fetching command, so the skill can resolve the placeholder. Why? Pre-approval is about permission, not substitution.

Wrong: move the file into the commands folder, because commands bind placeholders and skills don't. Why? They accept the same frontmatter. So moving the file changes packaging, not binding.

Hold on to this line. argument-hint hints. arguments binds.

[beat]

Now the most misread field of all. And it comes with the chapter's biggest source disagreement. The field is allowed-tools.

Question three. Practice question D3-009. This one is pick two.

Here's the scenario. An on-call team is writing a committed incident-snapshot skill. It runs kubectl get commands, which read the health of containers in a Kubernetes cluster. And it summarizes pod health for the incident channel.

Only a human may trigger it. The kubectl get commands should not stop for approval prompts during that invocation. And the stem is explicit: tool restrictions are already enforced separately, through the team's permission settings. So the skill does not need to block anything.

Which two settings?

Take a second.

[beat]

The answers. First, disable-model-invocation set to true, for human-only triggering. Second, allowed-tools set to the narrow shell rule `Bash(kubectl get *)`, with a space before the asterisk.

Here's the plain version. A note on the counter saying use the drill without asking me today lets the handyman get on with it. It doesn't lock the rest of the garage. And it expires when the visit ends. A separate house rule decides who is allowed to call the handyman in the first place.

[beat]

In exam terms. According to the notes, checked against current documentation, allowed-tools pre-approves the listed tools for the turn that invokes the skill. The grant clears when you send your next message.

And it restricts nothing. Every other tool stays callable under your normal permission settings. To remove tools, you use a field called disallowed-tools, or permission rules.

One more detail. For a project skill, the grant only takes effect after the workspace trust dialog has been accepted.

[beat]

Here's the disagreement. And you must know it.

The lesson eleven slide deck describes allowed-tools as restricting which tools the skill can use. The notes, checked against current documentation, say it only pre-approves, and restricts nothing.

For the exam, the rule is simple. If a question frames allowed-tools as a restriction, answer in the question's own terms. If it asks what the field actually does, pre-approval for one turn is the accurate answer.

This particular question was written to be safe either way, because it tells you the restrictions live elsewhere.

[beat]

Now the wrong turns in D3-009.

Wrong: user-invocable set to false. Why? It has it reversed.

Wrong: `Bash(kubectl*)`, with the asterisk straight after kubectl and no space, described as blocking unlisted tools for the session. Why? Three errors. The missing space widens the match. The field blocks nothing. And it lasts one turn, not the session.

Wrong: argument-hint, to reject invocations without a namespace. Why? You already know. Hints do not validate.

[beat]

Let's stay on that space for a moment. The space before the asterisk is load-bearing in permission rule syntax.

The rule `Bash(git diff *)`, with the space, matches git diff followed by arguments.

The rule `Bash(git diff*)`, with no space, also matches other commands that merely start with those letters. Like git diff-index.

We'll see that exact trap again in pipelines.

[beat]

A follow-on from the notes.

A team wants to run their deploy tool without prompts whenever anyone is working on a release. They propose putting it in the release skill's allowed-tools.

Does that work? For one turn. Then it quietly stops working.

For a session-wide or team-wide grant, put an allow rule in the permission settings. If the whole team should have it, that's the project's .claude/settings.json.

[beat]

Now a contrast segment across domains. Three fields share almost the same name, and the exam uses them as distractors for each other.

One. A skill's allowed-tools, here in Domain three. It pre-approves, and restricts nothing.

Two. A subagent's tools list, in Domain two. It's an availability list. A tool left out is not in that agent's session at all. So the restriction is real.

Three. The Agent SDK's allowed tools option, in Domain one. It's a permission list. That's why leaving the Agent tool out of it denies delegation.

The notes' plain version. The skill field is a note on the counter. The subagent field is what you put in the toolbox before handing it over. And the SDK field is the list of what the person is permitted to use at all.

Two of the three take capability away. The skill field is the one that doesn't.

[beat]

Hold on to this line. A skill's allowed-tools is a one-turn pre-approval that restricts nothing. And if a question calls it a restriction, answer in the question's terms.

[beat]

Last concept in this part. Running a skill in its own space.

Question four. Practice question D3-007.

Here's the scenario. A research team has an evaluate-sources skill. Its body is a list of criteria for judging source credibility. Run inline, it floods the main conversation with dozens of file reads, across sixty collected documents.

They want the main session to receive only a findings table, with file references. And they need that table back in the same turn.

What should they change?

Take a second.

[beat]

The answer has three parts. Add context: fork, with agent: Explore, and background: false. And rewrite the body as an explicit task: evaluate the documents given as arguments, and return a findings table.

Here's the plain version. Sending an assistant to the library keeps your desk clear. But only if you tell them what to find, and what to bring back. Hand them a page titled what makes a good source, and nothing else, and they come back empty-handed. They never knew the question.

[beat]

In exam terms. The frontmatter setting context: fork runs the skill in an isolated subagent. That subagent's prompt is the skill body. It has no access to your conversation history. And the main session receives only the result.

A companion field called agent picks the subagent type. Explore, Plan, general-purpose, or a custom agent you've defined. If you omit it, you get general-purpose.

And a forked skill runs in the background by default. So to get the result back in the same turn, you set background: false. Non-interactive runs, which we meet in part six, always wait.

[beat]

Now the wrong turns.

Wrong: add fork and Explore, but leave the body as a list of criteria. This is the trap that catches people. Why? A forked subagent gets the body and nothing else. A body of pure guidelines gives it criteria, but no task. And it returns nothing useful. The notes call this fork-forgetting.

Wrong: keep it inline, and pre-approve read-only tools. Why? That moves no work out of the main context. The reads still land there.

Wrong: keep it inline, with an argument hint for a folder. Why? That neither validates nor isolates anything.

[beat]

Two more facts about forks from the notes.

First. A background fork's edits fall outside session checkpoints. So /rewind will not undo them.

Second. If your content is reference material or conventions, rather than a task, keep it as a normal inline skill. That already loads only when invoked, or judged relevant.

[beat]

And two final frontmatter details worth recognizing.

First. An exclamation mark followed by a command in backticks, inside the body, runs that shell command before Claude sees the skill. And it pastes the output in. If that command fails, the whole invocation aborts.

Second, portability. The Agent Skills open standard defines six fields. They are name, description, license, compatibility, metadata, and allowed-tools. Everything else we discussed is a Claude Code extension. And a skill uploaded to claude.ai, or through the Skills API, is rejected if it carries an extension field.

[beat]

That's part two.

If you remember one thing, make it this. context: fork isolates the work. But only a body written as a task gives the subagent something to do.

Coming up in part three: path-specific rules for conditional convention loading.

## Part three: Path-specific rules for conditional convention loading

Part three. Path-specific rules.

By the end of this part, you'll know how to make a convention load only for certain files, how the patterns work, how to debug a rule that isn't loading, and when to pick a rule over a subfolder CLAUDE.md.

[beat]

Plain version.

The whiteboard by the door is read to everybody who walks in. A sign taped to the door of one room is read only by the people who go into that room.

A convention that governs the payments code should cost nothing on a day when nobody opens the payments code.

And there's a catch worth saying up front. A sign works only when someone opens that particular door. And it cannot stop anyone doing anything.

[beat]

The technical name is a path-scoped rule.

You put a markdown file in the .claude/rules/ folder. At the top, you give it frontmatter with a field called paths. That field holds a list of file patterns, called globs. The rule loads only when Claude works with a file matching one of those patterns.

What about a rule in that folder with no paths field? It loads unconditionally at launch. Every session.

And rules in that folder are found by their own mechanism. You don't import them.

[beat]

The course presenter flagged this as the exam answer for conditional file-type rules. And he repeated it on purpose, so it would stick.

Hold on to this line. The rules folder plus paths frontmatter is the answer for conditional, file-type conventions.

His sample question was different rules for TypeScript files and Terraform files. The answer: rule files with path patterns. One for the TypeScript source. One for the Terraform folder.

[beat]

Question one. Practice question D3-010.

Here's the scenario. A monorepo with fourteen packages. Test files ending in .test.ts and .spec.ts are scattered through all of them, often beside the source files.

The team wants strict test conventions, like never use the any type, and always declare return types in test helpers. Those conventions should load only when Claude works on a test file. Never during ordinary source edits. And no team owns test conventions per package.

What's the setup?

Take a second.

The answer. A single rule file, .claude/rules/testing.md, with paths set to `**/*.test.ts` and `**/*.spec.ts`. Those patterns match test files at any depth.

Plain version. It's like a recipe card marked desserts only, that comes out whenever someone bakes, whichever kitchen they're in. Taping a copy inside every kitchen door means people read it while making soup too.

[beat]

Now the wrong turns.

Wrong: a CLAUDE.md in each of the fourteen packages. Why? Directory files scope by location, not by file type. So they also load during source edits in those packages. And the text is duplicated fourteen times.

Wrong: a section in the root CLAUDE.md, headed for files matching test patterns. Why? CLAUDE.md has no conditional scoping. That heading is just text.

Wrong: an import of a testing document from the root. Why? Imports expand at launch. So the conventions load in every session.

The deciding words are file type, scattered, and only when.

So remember. When the condition is a file type rather than a folder, reach for a rule with paths.

[beat]

Now glob syntax. The exam builds troubleshooting questions on it.

Plain version. A sign reading rules for the ground floor is not read by anyone working upstairs, even though it's the same building. If you meant every floor, the sign has to say all floors.

In exam terms. A single asterisk matches anything within one directory level. A double asterisk matches any number of directories.

So. `**/*.ts` matches TypeScript anywhere. `src/**/*` matches everything under the source folder. `*.md` on its own matches only markdown files at the project root. And braces let you list several extensions at once, as in `src/**/*.{ts,tsx}`.

[beat]

Question two. Practice question D3-011.

Here's the scenario. A repository keeps invoice schemas under a schemas folder, organized into subfolders like schemas/invoices/v2. A rule has paths set to `schemas/*.json`. While Claude edits a file three levels down, /memory doesn't list the rule, and Claude ignores its conventions.

What's the root cause?

Take a second.

The answer. The single asterisk stops at the first level. So the pattern covers only files sitting directly in schemas. The fix is `schemas/**/*.json`.

[beat]

Now the wrong turns.

Wrong: path rules load only in sessions started from the folder containing the matched files. Why? They don't. Rules live centrally, and fire on matching reads wherever you started.

Wrong: rules are discovered only when the root CLAUDE.md imports them. Why? They aren't. And an import would load the content unconditionally anyway.

Wrong: the pattern's brace expansions exceed the budget. Why? There are no braces in this pattern.

[beat]

That last distractor is built on a real edge case. So know it.

Brace groups multiply. And a rule's whole paths list shares a budget of one thousand expanded patterns. A pattern that would exceed the budget is used unexpanded. So its literal braces match nothing.

Similarly, a square bracket that cannot be read as a valid bracket expression makes that one pattern match nothing. The rule's other patterns keep working.

Both fail quietly. That's why they make good troubleshooting distractors. But you only reach for them when the pattern actually contains braces or brackets.

Hold on to this line. One star is one folder level. Two stars is any depth.

[beat]

Question three. Practice question D3-012. This is the mirror problem.

Here's the scenario. A developer added a Terraform rule, Terraform being a tool for describing cloud infrastructure as code. The rule has naming and module conventions, and no frontmatter.

Now frontend engineers see Claude suggesting Terraform-style snake case names in React components. And every session carries the Terraform text, even when no infrastructure file is touched. All Terraform files live under an infra folder.

What's going on, and what's the fix?

Take a second.

The answer. A rule with no paths loads every session. That single fact explains both symptoms. The context cost, and the cross-contamination. The fix is to add frontmatter with paths set to `infra/**/*.tf`.

Plain version. A notice meant for the garage mechanics is pinned in the main entrance. So the receptionist starts using mechanic jargon on the phone. Moving the notice to the garage door fixes it. Writing mechanics only on it, while leaving it in the entrance, doesn't.

[beat]

Now the wrong turns.

Wrong: move it to the personal rules folder, so the frontend team stops getting it. Why? That removes it from the infrastructure team, and from the pipeline too.

Wrong: add a first line saying apply these only to Terraform files. Why? A prose scope statement still loads every session, and relies on judgment.

Wrong: move it into the root CLAUDE.md, under a Terraform-only heading. Why? Headings don't scope anything.

So remember. A rule without paths is always on. Add paths to make it conditional.

[beat]

Now debugging.

The course presenter flagged this as an exam scenario as well. How do you check whether Claude is loading your files?

The answer he gave is the /memory command. If a file you expected isn't in its list, that's your problem to fix. Perhaps a naming or configuration mistake.

[beat]

A small source disagreement here. It's worth a moment.

The transcript says /memory lists what loaded. The command reference says it opens memory files so you can edit them.

It does both. In the video's demonstration, it shows project and user memory, and which files are in play. And you can open them from there.

For the exam, the scenario is using /memory to see what loaded.

[beat]

Question four. Practice question D3-013.

Here's the scenario. A developer added a refund-tool rule, with paths set to `tools/refund/**/*.py`. They report Claude still ignores the refund conventions while editing tools/refund/policy.py. They want to fix it.

What should they do first?

Take a second.

The answer. Run /memory after Claude has read that file, and check whether the rule is listed.

Plain version. When a guest says they never got your note, first check whether it's actually on the noticeboard. Don't repaint it in red, or glue copies to every wall, until you know which problem you're fixing.

[beat]

In exam terms, the timing matters. Path-scoped rules load when Claude reads a matching file. So check after the read.

If the rule is absent, the problem is configuration. Like the glob, or the location. If it's present, the problem lies elsewhere.

[beat]

Now the wrong turns. They're all remedies before diagnosis.

Wrong: copy the conventions into the root CLAUDE.md. Why? It's a global fix that adds permanent cost to every session. And it may not address the cause.

Wrong: rewrite with mandatory headings. Why? Emphasis cannot help a rule that never loaded.

Wrong: convert it into a user-only skill. Why? It changes the mechanism before knowing what failed. And it makes correct behavior depend on someone remembering to invoke it.

The constraint word is first. When a stem asks what to do first, the answer is almost always to diagnose.

[beat]

Two related tools from the notes.

First. The /context command lists which memory files actually loaded.

Second. A hook event called InstructionsLoaded can log which instruction files loaded, and when. That's the right tool for debugging rules that load lazily.

[beat]

Now the compaction trap. It connects to the chapter on context management.

Here's the scenario. A path-scoped rule for database migrations works reliably early in a long session. Then the session compacts, meaning the conversation is summarized to free space. After that, Claude proposes a destructive column drop, while still working in the migrations folder.

Why?

The root project CLAUDE.md is re-read and re-injected after compaction. But subfolder CLAUDE.md files and path-scoped rules are not.

A path rule reloads only the next time Claude reads a matching file. If Claude keeps editing without a fresh read, the rule is simply no longer in the window.

[beat]

Distractors will offer three wrong causes. That rules become inert by design after compaction. That compaction rewrote the file on disk. Or that double asterisk became invalid. None of those is true.

And if the convention must survive regardless of context state? Two options. Promote it to a PreToolUse hook that inspects the edit. Or move it into the root file, and accept the always-on cost.

Also note. Path rules trigger on reading a matching file. Not on every tool call.

[beat]

Now the contrast segment the exam loves. Path-scoped rule versus subfolder CLAUDE.md.

Both load conditionally. The deciding question is usually ownership, and shape.

A subfolder CLAUDE.md sits with its code. It loads when Claude works in that folder. That suits a monorepo where each package owner maintains a file beside the code they own. That was D3-004.

A central rule in the rules folder fires on a glob. That suits a file type, or a convention spanning scattered paths. And it keeps all conventions reviewable in one directory. That was D3-010.

A subfolder CLAUDE.md cannot target file patterns at all.

[beat]

A self-check from the notes puts it well.

Say you have three services with incompatible testing conventions. Both answers are defensible. Choose per-directory files when each service team should own its file. Choose central rules when you want everything reviewable in one place.

What you must never do is leave all three in the root file. Every session pays for two irrelevant sets. And their contradictions degrade adherence to all three.

And neither mechanism is a gate. A rule that must hold every time belongs in a hook.

[beat]

One last detail, about priority.

Personal rules in ~/.claude/rules/ load before project rules. The documentation describes this as giving project rules higher priority.

It's a load-order fact. So don't confuse it with the skill collision order from part two.

[beat]

That's part three.

If you remember one thing, make it this. Rules with paths load only on matching reads. They're not re-injected after compaction. And you debug them with /memory.

Coming up in part four: plan mode versus direct execution.

## Part four: Plan mode versus direct execution

Part four. Plan mode versus direct execution.

By the end of this part, you'll know when to plan first, when to just do the work, and why plan mode is a habit and not a lock.

[beat]

Plain version.

If you ask a builder to knock through a wall, you'd like to see the drawing before the sledgehammer comes out. Not because the builder is careless. Because the drawing is the cheapest place to find out you meant the other wall.

Now ask the same builder to change a lightbulb, and get a drawing back. Something has gone wrong with the process.

So the question is never whether planning is good in general. It's whether a wrong first attempt would cost more than the drawing.

[beat]

The technical name is plan mode.

In plan mode, Claude researches and proposes, without editing. It reads files and runs exploratory commands. Then it writes a plan. And edits stay blocked until you approve.

How do you enter it? Three ways. Press Shift+Tab. Prefix a single prompt with /plan. Or start Claude with claude --permission-mode plan.

To make it the default for a project, set permissions.defaultMode to plan in the committed .claude/settings.json.

[beat]

When the plan arrives, you have three choices. Approve it into automatic editing. Approve it into manual approval of each edit. Or keep planning.

And pressing Ctrl+G opens the plan in your own editor, so you can correct it before Claude acts. The notes call that the cheapest intervention in the whole workflow.

[beat]

The deciding test is the one-sentence test.

If you can describe the change in one sentence, and it sits in one file, and the path is obvious, execute directly.

Plan when any of these is true. The change spans several files. There are several valid approaches. You don't know the code. The area is risky, like authentication or billing. Or the change is hard to reverse, or architectural.

[beat]

The supporting pattern is explore, plan, implement, commit. Four steps.

One. Explore, with reading prompts only.

Two. Plan, and edit the plan.

Three. Approve and implement, while checking against the plan.

Four. Commit.

Quick recap before the questions. Plan mode reads, proposes, and waits for you. The one-sentence test decides whether you need it.

[beat]

Question one. Practice question D3-014.

Here's the scenario. A production error log shows a stack trace. It points to an off-by-one error in a paginate function, in a single file. The fix is obvious. A regression test already reproduces the bug. And the hotfix must ship within the hour.

Plan, or execute?

Take a second.

The answer. Execute directly. Fix the function, run the regression test, and show the passing output.

Plain version. If a lightbulb has blown, you replace it. You don't ask an architect for drawings. Drawings are for knocking through walls, where a mistake is expensive to undo.

[beat]

Now the wrong turns.

Wrong: enter plan mode first, because anything going to production deserves a plan. Why? The notes call this planning theater. The round trip costs more than the change, and it delays the hotfix.

Wrong: launch an Explore subagent to map every caller first. Why? That's discovery for unclear scope. And the stack trace has already localized the defect.

Wrong: start with the interview pattern. Why? That's for ambiguous requirements. And the expected behavior is already encoded in the failing test.

[beat]

The constraint words are clear stack trace, single file, obvious fix, and within the hour.

And notice that the correct answer includes showing the passing test output. That's evidence rather than assertion. It's the theme of part five.

Hold on to this line. If you can say the diff in one sentence, just do it, and show the test passing.

[beat]

Question two. Practice question D3-015. The opposite case.

Here's the scenario. An engineer who joined last week must move a data extraction pipeline from thirty regex-based parser files to a schema-driven approach. Regex means pattern-matching code. There are at least two credible designs. And a wrong first attempt would touch every parser, and be painful to unwind.

Plan, or execute?

Take a second.

The answer. Start in plan mode. Let Claude read the parsers and propose a phased plan. Edit it with Ctrl+G. Then approve and implement.

Every trigger is present. Unfamiliar code. Competing designs. Thirty files. And an expensive failure.

Plain version. Before rewiring a whole house, you ask the electrician for a drawing. You mark up the parts you disagree with. And only then do you let them start. Going room by room with no plan, and saying we can always rip it out, is how you pay twice.

[beat]

Now the wrong turns.

Wrong: execute directly across all thirty files with acceptEdits, the mode that accepts edits automatically, relying on git to revert. Why? Unwinding thirty files of rework is exactly the cost planning avoids. And you get an unreviewable diff.

Wrong: start in plan mode, but keep bypass permissions on to avoid prompts. Why? This misunderstands what plan mode is. We'll see why in a moment.

Wrong: fan out one non-interactive run per parser immediately, because each file is independent. Why? Fanning out before the design is chosen, and proven on a sample, reproduces an unvetted approach across every file. We'll meet that sequencing rule again in part five.

Hold on to this line. Uncertain approach, many files, unfamiliar code, costly failure. Plan first, and edit the plan.

[beat]

Now the concept the exam uses to separate practitioners from people who read the brochure.

Question three. Practice question D3-016. This one is pick two.

Here's the scenario. A team lead wants every contributor's sessions to start in plan mode by default. The lead is also counting on plan mode to guarantee that nothing under a migrations folder is ever edited without approval. Including in sessions where some engineers enable bypass permissions.

Which two actions?

Take a second.

The answers. First. Set permissions.defaultMode to plan in the committed project settings file. That makes it the team default, and shares it through version control.

Second. Protect the migrations folder with a permission deny rule, or a PreToolUse hook, instead of relying on plan mode.

[beat]

Here's why.

Plain version. Asking every builder to show you a drawing before starting is a good habit. But it doesn't lock the cupboard with the fuse box. If nobody may ever touch the fuse box, you put a lock on it. The drawing habit covers everything else.

In exam terms. In sessions where bypass permissions are available, plan mode's blocks are not enforced. So an edit Claude attempts while planning will run.

Hold on to this line. Plan mode is a workflow control, not a security boundary.

[beat]

Now the wrong turns.

Wrong: rely on plan mode for the guarantee, because it blocks edits in every mode. Why? False, for the reason you just heard.

Wrong: add always start in plan mode to the lead's personal CLAUDE.md. Why? User scope is never shared. And prose cannot set anyone's permission mode.

Wrong: plan mode stops Claude reading files, so write the plan from a description. Why? False. Plan mode lets Claude read and explore. What it blocks is edits, until approval.

[beat]

A related trap from the notes' exam items.

An option says: execute a large refactor directly with acceptEdits, the mode that accepts edits automatically, because plan mode blocks the edits the task requires.

Why is that wrong? It misdescribes the mechanism. Approving a plan exits plan mode into an editing mode. Plan mode does not prevent the eventual edits.

[beat]

Now a contrast. This is where two ideas are most often confused. Plan mode, versus a permission rule or hook.

Plan mode changes what you approve, and when. A permission rule or hook changes what the tools are physically able to do.

When a stem says default, habit, or workflow, think plan mode. When it says guarantee, never, or must not, think deny rule or hook.

The same split appears in part one: advice versus enforcement. And it will appear again in part five.

[beat]

That's part four.

If you remember one thing, make it this. Plan mode is a habit, not a lock. Anything that must not happen needs a permission rule or a hook.

Coming up in part five: iterative refinement for progressive improvement.

## Part five: Iterative refinement for progressive improvement

Part five. Iterative refinement.

By the end of this part, you'll know how to give Claude a check it can run for itself, when to stop correcting and start fresh, how to guarantee a green test suite, and when to work one at a time versus in parallel.

[beat]

Plain version.

Picture someone hanging a shelf. If they have a spirit level, they can tell whether the shelf is straight without leaving the room.

If they don't, every adjustment ends with them calling downstairs, and waiting for you to come and look. The shelf still goes up. But you're now inside the loop. And the work moves at the speed of your attention.

Most of iterative refinement is the business of handing over a spirit level.

[beat]

The technical framing is this.

Claude stops when the work looks done. Without a check it can run for itself, looks done is the only signal available. And you become the verification loop.

Refinement converges when each iteration produces a signal Claude can read.

What manufactures that signal? Four techniques.

One. Concrete input and output examples.

Two. A failing test, written first.

Three. A screenshot to compare against.

Four. A script that exits with a failure code.

[beat]

Question one. Practice question D3-017.

Here's the scenario. An engineer asks Claude to write a function that normalizes invoice dates to the international standard date format, ISO 8601.

Each attempt looks finished. But review keeps finding failures on certain inputs. Zero three, zero four, twenty-five, written with slashes between the parts. Four March twenty twenty-five. And blank strings. The engineer has become the only source of feedback.

What's the fix?

Take a second.

The answer. Give input and expected-output pairs, including the ambiguous and blank cases. And have Claude run them as tests.

Plain version: hand the person a spirit level. Example cases with expected answers are the spirit level.

[beat]

In exam terms, that does three things. It defines done in a testable form. It encodes the edge cases you would otherwise catch in review. And it closes the loop.

The same move works visually. Paste a screenshot. Have Claude build it. Screenshot the result. List the differences. Fix them.

[beat]

Now the wrong turns.

Wrong: a longer, more detailed prose description of every accepted format. Why? It's still nothing Claude can check for itself.

Wrong: ask Claude to review its own output carefully, and confirm it handles every case. Why? That's verification by assertion. It produces a claim, not evidence.

Wrong: split the work across three parallel sessions, and keep the one that looks most robust. Why? It multiplies cost without adding a check. And looks most robust is still a human judgment.

Hold on to this line. Give Claude examples it can run as tests, or you stay stuck as the only checker.

[beat]

Question two. Practice question D3-018.

Here's the scenario. Deep in a long session, an engineer has twice corrected Claude on the same issue. An internal command-line tool keeps swallowing a non-zero exit code. Both corrections produced plausible changes that didn't fix it. And the context now holds three failed approaches.

What now?

Take a second.

The answer. The sources give an explicit stopping rule. After two failed corrections on the same issue, clear the context. Start again with a better prompt. One that states what was learned, and names a failing test.

Plain version. If you've given someone directions twice and they're still lost, repeating them louder doesn't help. Especially while they're still holding the two wrong maps. Take the old maps away, and hand over one clear new one.

In exam terms, the accumulated failed approaches are part of the problem. So anything that keeps them in the window keeps the problem.

[beat]

Now the wrong turns.

Wrong: a third, more forceful correction, listing everything that went wrong. Why? That's the documented anti-pattern.

Wrong: switch the same session into plan mode, to reconsider with all three attempts visible. Why? Plan mode doesn't remove the failed approaches from context. They keep competing.

Wrong: raise the session's turn limit. Why? More turns make a non-converging loop longer, not convergent.

That last one is a cross-domain pattern, and you'll meet it in the agentic architecture chapter. Raising a cap is not a fix for a loop that lacks a signal.

Hold on to this line. Two failed corrections, then clear and rewrite, with a failing test in the new prompt.

[beat]

Question three. Practice question D3-019.

Here's the scenario. A team runs Claude Code overnight, on unattended refactoring. Several mornings in a row, the transcript ends with all tests pass. Yet running the suite shows failures. CLAUDE.md already says run the full test suite before finishing. They need a guarantee that no unattended run ends while the suite is failing.

What gives them that guarantee?

Take a second.

The answer. A Stop hook.

Plain version. Asking the last person out to check every window is shut works most nights. If the building must never be left with a window open, you fit an alarm that will not arm while any window is still open.

[beat]

In exam terms, the notes describe a ladder for how hard a test gate holds. Three rungs.

Lowest rung. Ask Claude to run the check, inside one prompt.

Middle rung. Set it as a session-long condition that an evaluator re-checks after every turn.

Top rung. A Stop hook. It runs when Claude tries to end its turn. It runs your test script. And it blocks the turn from ending while any test fails, handing Claude the failure output to act on.

Guarantee, and unattended, push you to the top rung.

[beat]

Now the wrong turns.

Wrong: strengthen the CLAUDE.md wording with capital-letter musts. Why? It's still advisory. And that's exactly the observed failure.

Wrong: require Claude to paste the final test output into its summary. Why? It's good practice for reviewability. But it's still a request an unattended run can skip.

Wrong: add a PostToolUse hook that logs every test command for morning review. Why? Logging records what happened. It doesn't prevent anything.

One cross-reference. The same Stop event is used in Domain one to persist state at the end of a run. And a single hook can do both.

Hold on to this line. When a green test suite must be guaranteed, a Stop hook enforces it. A sentence only requests it.

[beat]

Now the rest of this task statement. The practice questions touch it less, but the notes and exam-style items cover it. Two topics.

First, the interview pattern.

Plain version. Take a feature you haven't fully thought through, before any code exists. You let the builder interview you until the hard questions are answered. Everything gets written down. Then you hand that write-up to a fresh builder, who never heard the debate.

[beat]

In exam terms. You start with a minimal prompt, and ask Claude to interview you in detail. On implementation, interfaces, edge cases, and tradeoffs. Skipping obvious questions.

When the space is covered, Claude writes a complete specification to a file. And you start a fresh session to execute it.

The fresh session is the point. Its context holds the spec and nothing else. No rejected options.

[beat]

A self-check in the notes describes the failure. A colleague implements in the same session as the interview. And the implementation drifts toward an approach that was explicitly rejected. Why? Because the rejected options are still sitting in the window.

Good specs do three things. They name the files and interfaces involved. They state what is out of scope. And they end with a verification step.

[beat]

Now the wrong turns for the interview pattern.

Wrong: write the most detailed single prompt possible. Why? It cannot surface decisions nobody has made yet.

Wrong: run four parallel sessions, and pick the best-looking result.

Wrong: park the feature's requirements in CLAUDE.md. Why? It costs context indefinitely. And it still leaves the design undecided.

[beat]

Second topic. Sequential versus parallel.

Plain version. When each attempt teaches you something about the next one, work one at a time. When the pieces genuinely don't affect each other, split them up. But only after you've proven your recipe on a couple of samples.

In exam terms. Debugging and architecture are sequential. Why? Because attempt two depends on what attempt one revealed. And an interface decision constrains the implementation.

Mechanical migrations across many independent files can be parallelized. Two ways. As sessions in separate worktrees, which also support a writer-and-reviewer split. Or as a fan-out loop, calling Claude non-interactively once per file, with each run returning a short verdict, like OK or FAIL.

[beat]

The rule is this. Refine sequentially on two or three representative files first. Then fan out. And verify the batch with the test suite, rather than trusting the verdicts.

Reverse the order, and you get hundreds of copies of the same mistake.

[beat]

An exam-style item in the notes sets nine hundred files, and a sample that dropped structured fields.

The options include three wrong turns. Launching the full run immediately, and fixing afterwards. Writing a path rule, so conversion happens automatically. And running all nine hundred in one interactive session, so Claude accumulates context.

The right answer refines on the sample. Then it fans out, with narrow tool pre-approvals. And it verifies with tests.

This connects back to D3-015's distractor, about fanning out before the design is proven.

[beat]

That's part five.

If you remember one thing, make it this. Refinement converges on a signal Claude can read. Converge on a sample, then fan out.

Coming up in part six: integrating Claude Code into CI/CD pipelines.

## Part six: Integrating Claude Code into CI/CD pipelines

Part six. Claude Code in pipelines.

By the end of this part, you'll know how to run Claude Code with nobody watching, how to gate a merge on something a machine can read, how to stop duplicate and biased reviews, and how to control what a pipeline run inherits.

[beat]

Plain version.

Leaving a voicemail that ends with a question is pointless if nobody will ever listen and call back. The conversation just stalls.

A pipeline is a room with nobody in it. Whatever runs there must say everything up front. It must expect no reply. And it must bring its own configuration, rather than trusting whatever happens to be lying around on the machine.

[beat]

The technical name for that room is continuous integration and continuous delivery, usually said as C-I-C-D.

It's the automated system, such as GitHub Actions or GitLab, that builds, tests and checks code on a server every time someone pushes.

The episode on this topic opens with exactly our first question.

[beat]

Question one. Practice question D3-020.

Here's the scenario. A GitHub Actions step runs claude, followed by a prompt asking it to review the failing tests and suggest fixes. On a developer's laptop, it works, because the developer answers Claude's follow-up questions. In the pipeline, the job sits idle until the workflow timeout kills it.

What's missing?

Take a second.

The answer. Invoke it as claude -p, followed by the prompt.

The episode's presenter explains it well. Locally, there's a human in the loop. In the pipeline, Claude asks a clarifying question. Nobody responds. The job hangs. And engineers blame the integration, when nothing is wrong with it except a missing flag.

[beat]

In exam terms. The -p flag, whose long form is --print, is the non-interactive mode. One prompt in. One response out. A clean exit.

It reads standard input, so you can pipe a diff or a build log into it. And it exits with zero on success, and non-zero on failure. So later pipeline steps can branch on the result.

[beat]

Now the wrong turns. They're fabricated flags, and the presenter called them out as exam tricks.

Wrong: a --ci-mode flag.

Wrong: a --batch flag.

Wrong: a --headless flag.

Wrong: an environment variable called CLAUDE_HEADLESS.

Why? None of them exist. The -p flag is the single valid way to run Claude Code headless.

Hold on to this line. In a pipeline, always -p. Anything that sounds like headless mode or CI mode is invented.

[beat]

Question two. Practice question D3-021.

Here's the scenario. A pipeline runs a Claude review with -p. A later step blocks the merge if any finding is critical. That step searches the prose output for the word critical.

It has blocked clean pull requests. And it has passed a real critical bug that Claude described as severe. The merge check must decide on a field the pipeline controls, not on phrasing.

What's the fix?

Take a second.

The answer. Add --output-format json. Add --json-schema, with a schema whose severity field only allows a fixed list of values, such as critical, major and minor. Then gate the step with jq -e.

Plain version. A form with a tick box marked critical, yes or no, can be sorted by a machine. A free-text note saying this looks pretty bad cannot. The pipeline needs the tick box, not the note.

[beat]

In exam terms. JSON, short for JavaScript Object Notation, is a structured data format machines can parse. With a schema supplied, the conforming output lands in a field called structured_output, in the result.

Then you gate the step with a command-line JSON tool called jq, run as jq -e. That makes the step fail based on a parsed value. The model's wording is never consulted.

As the presenter put it, default prose is great for humans, and useless for pipelines.

And the --output-format flag takes three values: text, json, or stream-json.

[beat]

Now the wrong turns.

Wrong: tell Claude to end every response with a verdict line, and search for that line. Why? It's better than free prose. But the gate still depends on the model's phrasing, rather than a field the pipeline owns.

Wrong: search for a maintained list of synonyms. Why? It's still pattern-matching on prose. Still false blocks, and false passes.

Wrong: submit the review through the Message Batches API, because it returns structured results. Why? Batches have a twenty-four-hour processing window, and no latency guarantee. So they're wrong for any blocking check. The episode names that one directly: never use batches for a blocking pre-merge check.

[beat]

One cross-reference for Domain four. The --output-format flag shapes the command-line tool's wrapper document. That's different from the API's structured output parameter. That chapter disambiguates all the similar names.

Hold on to this line. Gate a pipeline on a schema field checked by code. Never on words in prose.

[beat]

Question three. Practice question D3-022. The presenter flagged this one as a certain exam scenario. How do you stop Claude doing double work?

Here's the scenario. A pull request review job runs -p on every push. Each small follow-up commit triggers a full re-review. And Claude reposts the same comments it made on earlier pushes. Developers have started muting the bot. The runners are ephemeral containers, meaning each job gets a fresh machine that is thrown away afterwards.

What's the fix?

Take a second.

The answer. In a prior step, fetch Claude's earlier comments on the pull request, using gh, the GitHub command-line tool. Save them to a file. Pass them into the fresh -p session. And ask only for net-new issues.

Plain version. A new proofreader who hasn't seen your earlier notes will circle the same typos again. Hand them the list of what's already been flagged, and ask them to mark only what's new.

[beat]

In exam terms, the episode calls this the deduplication loop. Fetch the previous comments. Pass them into fresh session context. Generate new comments only. Repeat.

It keeps the fresh session's objectivity, while ending notification fatigue.

[beat]

Now the wrong turns.

Wrong: use claude -c -p to continue the previous session, so Claude remembers. Why? Continuing depends on conversation state that an ephemeral runner does not keep. And a same-session reviewer tends to rationalize its earlier reasoning.

Wrong: review only the first push to each pull request. Why? It removes duplicates by never reviewing the new code.

Wrong: report only critical findings. Why? It hides legitimate issues. And it still re-reports the same critical ones every push.

Hold on to this line. Deduplicate by handing prior findings to a fresh session. Not by continuing an old one.

[beat]

That leads straight to the next one, and the idea the presenter called the psychology of review.

Question four. Practice question D3-024.

Here's the scenario. A pipeline job uses -p to generate unit tests for changed code. Then it continues the same session with claude -c -p, to review those tests. The review almost never flags anything. Yet the tests routinely miss negative paths. Those are the cases where input is bad, or something fails.

What's the fix?

Take a second.

The answer. Run the review as a separate job, in a fresh -p session, with test standards supplied by the project CLAUDE.md.

Plain version. Asking the author of an essay to proofread it straight away rarely finds much, because they read what they meant to write. A colleague who didn't write it sees what's actually on the page.

The presenter's version was developers and testers. The developer tests along the path they built. The tester, with fresh eyes, thinks of new scenarios.

[beat]

In exam terms. A session that wrote the code retains the reasoning behind it, and tends to review by rationalizing. A fresh session has nothing to defend.

And because a fresh session remembers nothing, CLAUDE.md is how shared standards reach every job. Coding standards. Review criteria. Security policies. Testing requirements, like naming patterns, mocking rules, and coverage targets. Every new session loads it automatically.

[beat]

Now the wrong turns.

Wrong: keep the continued session, but instruct Claude to be highly critical and list at least three weaknesses. Why? The bias remains. And a quota invites invented findings.

Wrong: increase --max-turns. Why? That's just more time for a biased reviewer.

Wrong: add JSON output. Why? It helps gating, but it doesn't change the review's quality.

[beat]

Now a contrast segment on sessions, since this spans chapters.

Continuing a session keeps the reasoning. That's useful for picking up your own work, and harmful for reviewing it.

A fresh session gives objectivity. The price is that it knows nothing. So you pay that price back with CLAUDE.md for standing rules, and with explicit context, like prior findings, for anything situational.

You'll meet the same resume, fork, or fresh-start decision in the chapter on context management.

Hold on to this line. Separate jobs, separate sessions, with CLAUDE.md carrying the standards into each one.

[beat]

Question five. Practice question D3-023. This one is about controlling what the pipeline inherits. And it's pick two.

Here's the scenario. A conventions gate runs -p on a shared self-hosted runner. Three requirements. It must apply the repository's committed CLAUDE.md and rules. It must not execute any hooks from engineers' personal settings on that machine. And it should see the pull request diff, without being granted shell access.

Which two?

Take a second.

The answers. First, --setting-sources project. Second, compute the diff in an earlier step, pipe it into -p on standard input, and pre-approve only the read-only tools Read, Grep and Glob.

Plain version. When you borrow a colleague's desk for the day, you want the company handbook on it. But not their personal sticky notes telling you to do things their way. And if all you need is one document, someone hands it to you. You don't get the keys to the filing room.

[beat]

In exam terms. The --setting-sources flag takes a list drawn from user, project and local. With just project, it loads the repository's configuration, while skipping user and local configuration. So personal hooks stay out.

And piping the data removes any need for a shell permission. That's least privilege.

[beat]

Now the wrong turns. The big one is --bare.

Wrong: --bare. Why? Bare mode skips automatic discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md itself. MCP, the Model Context Protocol, is how external tools plug in. Bare sounds perfect for keeping personal hooks out. But it would also skip the committed CLAUDE.md that this gate exists to apply.

Bare suits jobs that must ignore everything the repository and the machine ship. It also never reads stored login credentials. So you must set the ANTHROPIC_API_KEY variable explicitly.

[beat]

Two more wrong turns.

Wrong: --permission-mode plan, to stop user hooks. Why? Plan mode governs edits, not configuration discovery.

Wrong: pre-approving `Bash(git diff*)` through --allowedTools, with no space before the asterisk. Why? It grants shell access the job doesn't need. And, as you heard in part two, it also matches commands like git diff-index.

[beat]

So the contrast. Bare, versus setting-sources project.

Bare drops everything auto-discovered, CLAUDE.md included. You pass back only what you need, with explicit flags for settings, MCP configuration, or an appended system prompt. So every input is visible in the workflow file.

Setting-sources project keeps the team's committed configuration, and drops the personal.

[beat]

When does bare win? An exam-style item in the notes shows it.

A nightly summary job on a shared runner starts reformatting files and opening commits. That's after another team rebuilt the base image, with no change to the workflow. Discovered hooks or skills on the new image explain it. And bare restores predictable behavior.

The distractors there all treat symptoms. Plan mode. JSON output to detect edits afterwards. Version pinning with verbose logging.

Hold on to this line. Setting-sources project keeps the team's config and drops personal config. Bare drops everything, CLAUDE.md included.

[beat]

A few remaining pieces of this task statement. First, the GitHub Action.

The higher-level GitHub option is the Claude Code GitHub Action. To set it up, you run /install-github-app, or install the Claude GitHub App. You add an API key or OAuth token secret. And you copy a workflow file.

Its mode depends on one input: the prompt input.

With no prompt input, it runs in interactive mode. It waits for someone to write @claude in an issue or pull request comment. And it replies in a comment.

With a prompt input, it runs in automation mode, on any event, including a scheduled cron job. And it writes results to the workflow run log.

So a mention-driven reviewer omits the prompt. And a Monday dependency report supplies one.

[beat]

It also checks the triggering actor. Users need write access. And bot accounts are rejected unless listed in the allowed_bots setting. That stops two bots triggering each other in a loop.

For GitLab, the shape is the same. One job in the pipeline file. The API key as a masked variable. The command-line tool installed in the setup script. And claude -p with --permission-mode acceptEdits, when the job should open a merge request.

[beat]

And the governing principle for all of it. Pipelines are where permission design becomes the control.

Five habits.

One. Grant least privilege, with precise tool rules.

Two. Keep credentials in secrets.

Three. Pipe data in, rather than granting tools to fetch it.

Four. Fail steps on parsed signals.

Five. Route every change through a pull or merge request.

The notes call the alternative the overprivileged pipeline. A broad permission mode, because writing an allowlist felt tedious. Plus whatever the runner image carries.

[beat]

That's part six.

If you remember one thing, make it this. A pipeline run must name everything it needs on the command line, and inherit nothing by accident.

Coming up next: the trap round.

## Trap round

The trap round.

Rapid fire. For each one, the pattern is: if you see this, think that. I'll take them in small groups, so you always know where you are.

[beat]

First group. Instruction files and scopes.

If you see a teammate or the pipeline not getting conventions that work for one person, think: check the config location. Move it from the user file to the committed project file.

If you see CLAUDE.local.md offered as a way to share with the team, think: personal, and ignored by version control. Never shared.

If you see project scope overrides user scope, or ./.claude/CLAUDE.md loads later and wins, think: scopes are additive. Delete the contradiction.

If you see capitals, CRITICAL, MUST, or repeating a line to give it weight, think: emphasis is not precedence, and not enforcement.

If you see imports offered to cut startup tokens, think: imports organize, they do not economize.

If you see imports offered for conditional loading, think: no. Imports expand at launch.

If you see a CLAUDE.md heading that says for files matching some path, think: CLAUDE.md has no path prefixes. That heading is just text.

[beat]

Next group. What loads, and when.

If you see a file-type convention scattered across the tree, think: a rule in the rules folder, with paths.

If you see each package team wanting its own file beside its own code, think: a subfolder CLAUDE.md.

If you see a rule with no frontmatter causing cross-contamination and constant cost, think: add paths. Without paths, it loads every session.

If you see a single-star glob missing nested files, think: double star, for any depth.

If you see brace-expansion budget offered as the cause for a pattern with no braces, think: it cannot apply.

If you see the question, what should they do first about a missing rule, think: run /memory after Claude reads the matching file.

If you see a path rule forgotten after a long session compacted, think: path rules are not re-injected. They reload on the next matching read.

[beat]

Now the one that cuts across everything.

If you see never, must hold every time, or guarantee, think: hook or permission rule. Not prose. Not managed policy. Not plan mode.

[beat]

Next group. Skills.

If you see a side-effecting command that must never fire on its own, think: disable-model-invocation true.

If you see user-invocable false offered for that job, think: reversed. That makes it Claude-only.

If you see argument-hint offered to validate or bind input, think: hints only. arguments binds named placeholders.

If you see allowed-tools described as blocking tools for the session, think: the notes say it pre-approves for one turn, and restricts nothing. But if the question itself frames it as a restriction, answer in the question's terms.

If you see a team-wide or session-wide pre-approval, think: an allow rule in project permission settings. Not skill frontmatter.

If you see a stale personal skill breaking one engineer's command, think: personal beats project on a name clash. Delete or rename the personal skill.

If you see exploration flooding the main conversation, think: context: fork, with a body written as a task. And background: false, if you need the answer this turn.

If you see context: fork on a skill that is only guidelines, think: fork-forgetting. It returns nothing useful.

[beat]

Next group. Planning and refinement.

If you see a one-sentence, single-file fix under time pressure, think: direct execution, and show the test passing.

If you see unfamiliar code, several valid designs, many files, and a costly failure, think: plan mode, and edit the plan with Control G.

If you see plan mode offered as a safety guarantee, think: workflow control, not a security boundary. Its blocks are not enforced where bypass permissions are available.

If you see Claude saying all tests pass with no output, think: verification by assertion. Require evidence. And for a guarantee, a Stop hook.

If you see two failed corrections on the same issue, think: clear the context, and write a better prompt with a failing test.

If you see raising the turn limit to fix a loop that is not converging, think: the loop lacks a signal, not a budget.

If you see fanning out across many files before the prompt works on a sample, think: refine sequentially first, then fan out.

If you see implementing in the same session as the interview, think: write the spec to a file, and start fresh.

[beat]

Last group. Pipelines.

If you see a pipeline job hanging until timeout, think: -p.

If you see --ci-mode, --batch, --headless, or CLAUDE_HEADLESS, think: fabricated.

If you see a merge gate searching prose for a word, think: --output-format json, --json-schema with an enum, and jq -e on structured_output.

If you see the Batches API for a blocking check, think: twenty-four-hour window, no latency guarantee. Wrong tool.

If you see the same review comments reposted on every push, think: fetch prior comments, and pass them into a fresh session.

If you see claude -c -p to continue a session for review, think: rationalization. And state an ephemeral runner does not keep.

[beat]

And the last three, about what a runner inherits.

If you see personal hooks leaking into a job that must still apply CLAUDE.md, think: --setting-sources project. Not --bare.

If you see a rebuilt runner image suddenly changing a job's behavior, think: --bare. Plus an explicit ANTHROPIC_API_KEY.

If you see a shell rule with no space before the asterisk, think: the grant is wider than intended. And better still, pipe the data in.

[beat]

That's the trap round.

Coming up: the closing recap, ten things to remember.

## Closing recap: ten things to remember

Closing recap. Ten things to remember.

For each one, you'll get the plain version first. Then the technical name.

[beat]

One. Instruction files stack up. They do not overrule each other. When two contradict, delete one.

The technical name: CLAUDE.md scopes are additive. Managed policy, user, project and local, concatenated from the root down.

[beat]

Two. Your personal file never leaves your machine. So team rules go in the file the repository carries.

The technical name: user scope at ~/.claude/CLAUDE.md, versus a committed project CLAUDE.md. And the gitignored CLAUDE.local.md, for personal project notes.

[beat]

Three. Splitting a big instruction file into pieces helps people own their parts. But it saves nothing.

The technical name: at-path imports expand at launch, up to four hops. They organize without economizing.

[beat]

Four. Conventions for one kind of file should appear only when that kind of file is touched.

The technical name: a rule in .claude/rules/ with paths frontmatter globs. One star is one level. Two stars is any depth. And a rule with no paths loads every session.

[beat]

Five. When something doesn't seem to be loading, check what actually loaded before changing anything.

The technical name: the /memory command, backed by /context, checked after Claude reads a matching file.

[beat]

Six. A reusable procedure belongs in a card pulled on demand, shared through the repository. And anything with side effects should be startable only by a person.

The technical name: a project skill in .claude/skills/, with disable-model-invocation set to true. user-invocable false is the mirror. And personal skills beat project skills on a name clash.

[beat]

Seven. A hint is not wiring. And a one-time permission slip is not a lock.

The technical name: argument-hint is autocomplete, and arguments binds placeholders. allowed-tools pre-approves for the invoking turn, and restricts nothing. Though the lesson deck calls it a restriction, so answer in a question's own terms.

[beat]

Eight. Send big investigations off to a helper with a clear task, so your main conversation stays clean.

The technical name: context: fork with an agent type, a body written as a self-contained task, and background: false to get the result in the same turn.

[beat]

Nine. Plan when being wrong is expensive. Just do it when the change fits in one sentence. And never mistake the planning habit for a lock.

The technical name: plan mode via Shift+Tab, /plan, or permissions.defaultMode set to plan. Edited with Ctrl+G. And not a security boundary where bypass permissions are available.

And refinement converges only on a signal Claude can read. Examples. Failing tests. A Stop hook. And a fresh start after two failed corrections.

[beat]

Ten. In a pipeline, nobody is there to answer. So the run must be one-shot, machine-readable, reviewed with fresh eyes, and carry its own settings.

The technical name: claude -p. --output-format json with --json-schema, gated by jq -e. A fresh session per job, with prior findings passed in. And --setting-sources project, or --bare, to control what the runner contributes.

[beat]

And the one idea underneath all ten.

Hold on to this line. Prose advises. Code enforces.

When the stem says every time, reach for the hook.
