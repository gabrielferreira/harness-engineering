**English** · [Português](HANDBOOK.pt.md)

---

# Harness Engineering Handbook

> A practical guide for engineering teams, technology orgs, and companies that want to use AI coding assistants in real projects at scale — not as fancy autocomplete, but as part of the development process.

---

## Contents

- [Introduction](#introduction)
- [Part I — Foundations](#part-i--foundations)
- [Part II — Context Engineering](#part-ii--context-engineering)
- [Part III — Orchestration: Budget, Sessions, and Continuity](#part-iii--orchestration-budget-sessions-and-continuity)
- [Part IV — Skills and Agents](#part-iv--skills-and-agents)
- [Part V — Spec-driven Development](#part-v--spec-driven-development)
- [Part VI — Backlog as Single Source of Truth](#part-vi--backlog-as-single-source-of-truth)
- [Part VII — Versioning, Releases, and Migrations](#part-vii--versioning-releases-and-migrations)
- [Part VIII — Distribution and Compatibility](#part-viii--distribution-and-compatibility)
- [Part IX — Dual-mode](#part-ix--dual-mode)
- [Part X — Quality, Verification, and Audits](#part-x--quality-verification-and-audits)
- [Part XI — Security in AI Harnesses](#part-xi--security-in-ai-harnesses)
- [Part XII — Cross-cutting Principles](#part-xii--cross-cutting-principles)
- [Part XIII — Developer Anti-patterns When Using AI](#part-xiii--developer-anti-patterns-when-using-ai)
- [Part XIV — When NOT to Use an AI Assistant](#part-xiv--when-not-to-use-an-ai-assistant)
- [Part XV — Harness Governance and Evolution](#part-xv--harness-governance-and-evolution)
- [Part XVI — Adoption: From Zero to Mature](#part-xvi--adoption-from-zero-to-mature)
- [Part XVII — Harness Health Metrics](#part-xvii--harness-health-metrics)
- [Part XVIII — Human Onboarding to the Harness](#part-xviii--human-onboarding-to-the-harness)
- [Part XIX — Anatomy of a Good Prompt](#part-xix--anatomy-of-a-good-prompt)
- [Part XX — Debug Workflow with AI](#part-xx--debug-workflow-with-ai)
- [Part XXI — Cost and Economics of AI](#part-xxi--cost-and-economics-of-ai)
- [Part XXII — Technical Documentation and AI](#part-xxii--technical-documentation-and-ai)
- [Appendix A — Glossary](#appendix-a--glossary)
- [Appendix B — Compiled Checklists](#appendix-b--compiled-checklists)
- [Appendix C — Reference Templates](#appendix-c--reference-templates)

---

## Introduction

### The problem

AI coding assistants are productive on small, surface-level tasks. In real projects, they often:

- Invent APIs that don't exist in the codebase;
- Repeat obsolete patterns the team already abandoned;
- Ignore unwritten architectural conventions;
- Produce code that passes lint but breaks business rules;
- Don't know when to stop: they solve the literal request and ignore the systemic consequence.

The model is not the culprit. The culprit is the **absence of harness** — the infrastructure of context, rules, specialization, and verification that tells the AI where it is, what the team values, and how work is judged.

### What harness engineering is

**Harness engineering is the discipline of configuring the instructions, constraints, and tools an AI coding assistant needs to operate with quality in a real project.**

It treats the AI assistant as a new collaborator who needs onboarding, standards, code review, and gates — not as an oracle that gets it right by intuition. A well-built harness:

- Says **who the project is** (stack, domain, constraints);
- Says **how the team works** (conventions, testing, security);
- Says **what to verify** before, during, and after each change;
- Says **where to stop** (scope, gates, human review);
- **Persists memory** across sessions so context isn't lost.

### Who should read this

- **Senior engineers and architects** introducing AI assistants to their teams who need to keep them within guardrails;
- **Tech leads** standardizing AI use across squads;
- **Engineering managers** calibrating expectations, quality, and velocity;
- **Platform engineering** teams offering AI as an internal product;
- **CTO/VP Engineering** making org-wide policy decisions.

### How to read this

The handbook is dense by design: each section stands on its own. Read it linearly once to get the mental map; then consult section by section when a specific problem appears.

---

## Part I — Foundations
### 1. The six layers of the harness

A mature harness organizes the assistant's intelligence into six complementary layers. Removing any one of them doesn't break everything — it degrades quality in an insidious way.

| Layer | What it is | Question it answers |
|---|---|---|
| **1. Knowledge** | Specs, backlog, project context | *What does this project do, and why?* |
| **2. Expertise** | Domain-specific checklists (skills) | *How am I supposed to do X in this project?* |
| **3. Automation** | On-demand read-only sub-agents | *Is everything OK? Is anything broken?* |
| **4. Orchestration** | Phase sequencing, context budget, isolated sessions | *In what order do I work, and where does context reset?* |
| **5. Verification** | Executable scripts, definition of done | *Is this really done?* |
| **6. Continuity** | Persistent context files, state across sessions | *Where did I leave off last time?* |

**Foundational principle:** each layer exists because the previous one isn't enough. Knowledge without expertise becomes generic code. Expertise without automation becomes an ignored checklist. Automation without orchestration becomes noise. And so on.

### 2. Harness design principles

Four principles guide everything that follows:

**Markdown-first.** The harness lives as text files in the repository, versioned alongside the code. No proprietary tool, no SaaS, no central database. If the repo compiles, the harness works.

**On demand, not always on.** Context has a cost. Global rules go into automatic onboarding; specific rules load only when the topic shows up. More context ≠ better results.

**Human review between phases.** The AI proposes; humans approve critical transitions (spec → plan, plan → code, code → merge). Explicit gates prevent silent drift.

**Persist to disk, not to chat.** Every important decision becomes a file. Conversation is ephemeral; commits, specs, and plans outlive the session.

### 3. Minimum vocabulary

Before moving on, lock in these terms (they show up throughout the handbook).

- **Harness:** the whole infrastructure (context + skills + agents + verification).
- **Context file:** file automatically loaded at the start of every session with the AI.
- **Skill / Playbook:** domain checklist ("how to do X") consulted by the AI or the human.
- **Agent / Sub-agent:** AI sub-process, typically read-only, dispatched to analyze something specific and report back.
- **Spec:** document that defines what will be built, why, and how to validate it.
- **Execution plan:** breakdown of a spec into ordered tasks.
- **Gate:** mandatory human checkpoint between phases.
- **Context budget:** available space in the AI's context window; finite, needs management.
- **Session:** a single conversation with the AI, starting from a "clean" context.

---

## Part II — Context Engineering

### 1. The main context file

Every project should have a context file the AI assistant loads automatically in every session. This file is the **project's brain** — what the assistant needs to know before touching a single line.

Typical content:

1. **Project identity:** what it is, for whom, what stage (production, beta, greenfield);
2. **Tech stack summary:** language, frameworks, database, tests, deploy;
3. **Global conventions:** how to name, how to test, how to commit, how to open a PR;
4. **Workflow:** where specs live, how the backlog works, when to ask for review;
5. **Skills and docs map:** links to on-demand content (not inline);
6. **Non-negotiable constraints:** security, compliance, sensitive data.

**Test for what gets in:** *if I remove this line, will the AI make the same mistake it already made before?* If yes, it stays. If it's something the AI can infer from the code, leave it out.

### 2. Hierarchy by depth

In small projects, a single context file is enough. In monorepos or large systems, context becomes hierarchical:

| Level | Where it lives | Typical content | Size |
|---|---|---|---|
| **L0** | Repo root | Global conventions, spec/backlog flow, security, skills map | 200–400 lines |
| **L1** | Domain (e.g. `apps/`, `services/`) | Domain-shared rules | 50–150 lines |
| **L2** | Module (e.g. `apps/api/`) | Local stack, commands, coverage, specific rules | 100–300 lines |
| **L3+** | Feature (rare) | Edge cases, third-party integrations | 30–80 lines |

**Loading rule:** concatenation, not override. Root first, subfolder after. Zero redundancy: if something applies to the whole monorepo, it lives in L0; if it only applies to the API, it lives in L2.

### 3. Import on demand

The main context references external content instead of inlining it:

- Skills by file path;
- Technical docs by path;
- Specs by ID.

This keeps the main context lean (200–400 lines) and the AI pulls depth only when the conversation calls for it. That's different from *having* the information (it exists, but doesn't take context budget by default).

### 4. Portable context

A second context file, **agnostic to which AI is running**, should exist for use with other tools (web models, other assistants, future integrations). While the main file speaks the conventions of the team's specific AI (skills, agents, slash commands), the portable one describes:

- Full tech stack;
- Repo structure;
- Architectural decisions;
- Non-obvious business rules;
- Security rules.

That way, any LLM handed this file can operate with the same base context. It's the "document" version of the harness: it reads top to bottom, no tooling required.

---

## Part III — Orchestration: Budget, Sessions, and Continuity

Context is a finite resource. The art is choosing what occupies space now, what's referenced, and what survives between sessions.

### 1. Context budget as a design constraint

Every context window (200k, 1M tokens, doesn't matter) eventually saturates. Before that, output quality already **starts dropping**: the AI ignores old instructions, contradicts recent decisions, invents when it could just look.

**Three pressures compete:**

- **Loading context** (to be right): reads code, docs, prior conversations;
- **Thinking** (to decide): chain of reasoning, hypotheses, verification;
- **Producing** (to act): edits, tests, reports.

When one dominates, the others suffer. An assistant that **only** reads code doesn't think. One that **only** thinks gets verbose. One that **only** produces makes silly mistakes.

**Rule of thumb:** *the more ambitious the work, the more important it is to keep context lean per phase*. Don't shove the whole company's documentation into context "just in case."

### 2. Budgeting practices

- **Reference, don't inline.** Skills, docs, specs go in as paths; the AI reads them when needed.
- **Summarize before extending.** In long conversations, ask for an interim summary and start a new session from it.
- **Isolate noisy phases.** Research (which explores broadly) shouldn't share context with implementation (which needs focus).
- **Trim long outputs.** A 5000-line tool call output almost always needs a filter: grep, head, tail, limit.
- **Measure.** If the platform exposes token count, glance at it periodically.

### 3. Phase-isolated sessions (RPI)

For big tasks, a single session is a terrible idea. Three separate sessions (**R**esearch, **P**lan, **I**mplement) almost always win.

| Phase | What the dedicated session does | Persisted output |
|---|---|---|
| **Research** | Explores code, reads docs, surfaces hypotheses, no production code | `research.md` with findings |
| **Plan** | Reads the research and produces an ordered plan, architectural decisions | Spec + execution plan |
| **Implement** | Reads the approved plan and executes task by task | Commits + tests |

**Why isolate:**

1. Research pollutes context with abandoned attempts; implementation doesn't need that noise.
2. The model "clings" to decisions made in earlier phases even when evidence shifts. Cognitive reset helps.
3. Cost: each phase pays its own briefing but saves on rework.

**When not to separate:** medium or trivial tasks. RPI has overhead — it only pays off at large or complex scope.

### 4. Explicit context reset

When a big phase ends (feature shipped, refactor closed), mark a **reset**: new session, just the main context file plus a reference to the freshly produced artifact. The AI doesn't need to "remember" the previous 200 exchanges; they became code, PR, changelog.

**Signs the reset is overdue:**

- The AI starts confusing current state with a previous one;
- It asks for confirmation on things already decided;
- It suggests redoing something already done.

### 5. Controlled sub-agent parallelization

Read-only sub-agents can run in parallel over the same scope (e.g. three auditors looking at security, tests, and docs in parallel). For agents that **write code**, parallelizing requires:

- **Isolated worktrees.** Each agent operates in a separate `git worktree`, with zero overwrite risk.
- **Tasks in disjoint files.** If two agents touch the same file, serialize.
- **Merge gate.** Once they all finish, a human (or a reviewer agent) consolidates.

Mark parallelizable tasks in the execution plan with `[P]`:

```markdown
## Execution plan

- [ ] T1: create User model (src/models/user.ts)
- [ ] T2 [P]: create initial migration (db/migrations/)
- [ ] T3 [P]: add test fixtures (tests/fixtures/)
- [ ] T4: implement login (depends on T1)
```

T2 and T3 are parallelizable; T4 depends on T1. Gate between waves.

### 6. Cross-session continuity: the STATE pattern

Big tasks inevitably cross a single session. To avoid losing context, keep a **STATE** file up to date.

**Minimum structure:**

```markdown
# STATE — {spec-id or task-id}

**Updated:** 2026-04-16 17:30

## Status
In progress — task T3 done, starting T4.

## Loaded context
- Spec: `.specs/FEAT-12.md`
- Plan: `.specs/FEAT-12-plan.md`
- Research: `.specs/FEAT-12-research.md`

## Done
- T1: User model ✅ (commit abc123)
- T2: migration ✅ (commit def456)
- T3: fixtures ✅ (commit ghi789)

## Pending
- T4: login endpoint (in progress)
- T5: integration tests
- T6: documentation

## Next action
Implement password validation in `login.controller.ts` — spec line 42.

## Blockers / pending decisions
- Hash with bcrypt vs argon2 (spec line 87 didn't decide) — ask in PR.

## Notes
- Use existing `user.repository.ts` (already has `findByEmail`).
- Don't touch the refresh token flow — out of scope.
```

**Discipline:**

- **Update before ending the session** (AI's last action, or manual checkpoint);
- **Read at the start of the next one** (first action, before any new thinking);
- **Persist in the repo** on a working branch (committed or not — team's call).

STATE is the project's memory between amnesias. Without it, every new session starts from zero and the AI reinvents decisions.

### 7. Self-contained briefings for sub-agents

Sub-agents start with zero context. The prompt for a sub-agent has to be **self-contained**:

- What you want;
- Why (briefly — decisions change when the reason changes);
- What's already been tried or discarded;
- Constraints (don't edit X, don't read Y);
- Expected response format.

Vague prompt to a sub-agent = generic report. Good briefing = good answer.

---

## Part IV — Skills and Agents

Skills and agents are the two main ways the AI applies specialization. Confusing them is a common mistake.

### 1. Skills: domain checklists

A **skill** is a markdown document that answers: *"when I'm about to do X in this project, what should I check?"*. It doesn't execute; it **informs**. It's read by the AI (and the human) the moment the topic appears.

**Canonical skill format:**

```markdown
# {Skill name}

## When to use
- When implementing X
- When modifying Y

## When NOT to use
- When it's just Z (use another skill)

## Checklist
- [ ] Verify A
- [ ] Validate B
- [ ] Run C

## Patterns
✅ Right: concrete example
❌ Wrong: concrete anti-example

## When to escalate
- If you hit {condition}, trigger {other skill / human}
```

**Typical skills in a mature harness:**

- Core: spec-driven, definition-of-done, testing, code-quality, security-review
- Domain: ux-review, dba-review, accessibility, observability
- Orchestration: research, execution-plan, context-reset

**Critical rule:** every skill needs **concrete examples**, not just generic placeholders. A real example is 10x more useful than three abstract bullets.

### 2. Agents: autonomous read-only auditors

An **agent** is an AI sub-process invoked on demand to analyze something specific and report. It:

- **Doesn't edit code** (by default, just reports);
- **Runs in isolated context** (doesn't pollute the main conversation);
- Returns a **structured report** with classified findings.

**Required frontmatter** for every agent:

- `description`: one sentence on what it does;
- `model`: which model tier it uses;
- `worktree`: `false` by default (read-only); `true` only if the agent is going to write;
- `model-rationale`: one sentence justifying the model choice.

### 3. Model choice by complexity

Not every agent needs the most expensive model. The choice affects cost, latency, and quality: be explicit.

| Tier | When to use | Example |
|---|---|---|
| **High** (deep reasoning) | Real consequence of being wrong, cross-finding correlation, severity judgment | Security audit, architecture review |
| **Mid** (structured checklists) | Checks with clear thresholds, analysis with documented heuristics (**recommended default**) | Code review, coverage check, spec validator |
| **Low** (formatting and reading) | Extraction, formatting, reading without complex judgment | Log summary, file listing |

**Rule of thumb:** if the agent has a checklist with numeric thresholds → mid. If it needs to correlate findings and judge severity → high. If it just reads and formats → low.

**Write the `model-rationale` in the frontmatter.** A short sentence like *"checklist with numeric thresholds, no subjective judgment"* provides traceability and eases review.

### 4. Agent output pattern

Every agent returns a report in the same format. That lets humans skim quickly and other agents consume the output.

**Required sections:**

1. Status: PASS | FAIL | PARTIAL;
2. Findings grouped by severity;
3. Next steps (linking to skills or other agents).

**Standard severities:**

- 🔴 **Critical**: blocks merge, severe security issue, incorrect data;
- 🟠 **High**: broken functionality, wrong business rule;
- 🟡 **Medium**: needed improvement, UX gap;
- ⚪ **Info**: nice-to-have, reference, context.

### 5. Skill or agent: how to decide

| Question | Skill | Agent |
|---|---|---|
| Am I going to write code? | ✅ | |
| Do I want to analyze what's already written? | | ✅ |
| Do I need local context (current file)? | ✅ | |
| Do I need to scan the whole repo? | | ✅ |
| Is it preventive (before acting)? | ✅ | |
| Is it verifying (after acting)? | | ✅ |

Skills and agents complement each other. A typical flow: *skill `security-checklist`* informs the dev before coding → *agent `security-audit`* sweeps after to confirm. One is prevention, the other detection.

---

## Part V — Spec-driven Development

### 1. The canonical flow

```
Idea → Backlog → Spec → (Research) → Plan → Implementation → Tests → Verification → Done
```

Each arrow can have a **human gate**: the moment a dev confirms the prior phase is solid before moving on. Gates keep the AI from accelerating in the wrong direction.

### 2. Ceremony proportional to complexity

Not every change deserves the same process. Over-engineering process is as bad as having none.

| Size | Criteria | Artifacts | Flow |
|---|---|---|---|
| **Trivial (fast-path)** | Typo, dependency bump, rename, 1–2 line fix | None | Code directly, commit |
| **Small** | ≤3 files, no new abstraction, no schema change | Light spec or none | Backlog → spec → code → test |
| **Medium** | <10 tasks, clear scope | Brief spec (context + requirements + criteria) | Backlog → spec → plan → code |
| **Large** | Multi-component, >10 tasks | Full spec + task breakdown | Backlog → spec → design → plan → code |
| **Complex** | Ambiguity, new domain, >20 tasks | Spec + design + parallelizable tasks + cross-session state | Research → spec → design → plan → phased execution |

**Before the first line of code is written** (medium and up), these must exist as files on disk:

1. Spec with status `approved`;
2. Execution plan with ordered tasks;
3. If large/complex: research document with findings.

### 3. Canonical spec structure

```markdown
# Spec {ID}: {Title}

**Status:** draft | approved | in progress | partial | done | discontinued

## Context
Why this spec exists, what problem it solves.

## Dependencies
Specs or components this one needs to exist.

## Functional Requirements
- FR-001: {requirement}
- FR-002: {requirement}

(Reference IDs in code comments: `// Implements FR-001`)

## Scope (verifiable checkboxes)
- [ ] Deliverable 1
- [ ] Deliverable 2

## Acceptance Criteria (testable assertions)
- Given X, when Y, then Z
- API returns 200 for case W

## Affected Files
- path/foo.ts: modify
- path/bar.ts: create

## Task Breakdown (large/complex)
| Task | Depends on | Files | Type | [P]? |
|---|---|---|---|---|
| T1 | — | foo.ts | backend | |
| T2 | T1 | bar.ts | backend | [P] |
| T3 | T1 | baz.ts | backend | [P] |

## Out of Scope
- Thing X (saved for spec Y)

## Skills to consult
- testing, security-review

## Post-implementation verification
- [ ] Tests pass
- [ ] Linter clean
- [ ] Criteria above validated
```

### 4. Task markers and parallelization

The `[P]` marker in the task table means **parallelizable**: the task doesn't depend on others in the same wave and touches files disjoint from other parallel tasks. Sub-agents in separate worktrees can execute them concurrently.

**Criteria for marking a task `[P]`:**

- Dependencies: only depends on already-completed tasks (earlier waves);
- File isolation: doesn't modify files other `[P]` tasks touch;
- No global side effect: doesn't change shared config, migrations, or schema.

**Waves:** group tasks into numbered waves. All `[P]` tasks in wave N run in parallel; wave N+1 only starts when the previous one closes. Between waves, a human (or reviewer agent) does a consolidated merge.

### 5. Delta markers for brownfield

In legacy code, the spec needs to distinguish what's new from what's modified. Use markers:

- `[ADDED]`: completely new functionality;
- `[MODIFIED]`: alter existing code (reference file and section);
- `[REMOVED]`: remove functionality (list affected callers).

In greenfield, the markers are optional (everything is implicit `[ADDED]`).

### 6. Gates and fast-path

**Gates** are points where the AI must **stop and ask for confirmation** before moving on:

- Draft spec → approved;
- Plan generated → execution;
- Code ready → verification;
- Verification ok → merge.

In trivial tasks (fast-path), gates are dispensable: the human inspects the final commit and that's it.

### 7. TDD when implementing from spec

When the project follows TDD:

1. Read the spec (acceptance criteria define scenarios);
2. Write tests **first**, based on the criteria;
3. Implement the minimum to pass (green);
4. Refactor if needed.

Exception: for small fixes, a regression test before the fix is enough. No need to write a new suite.

### 8. Test strategy with AI

The test suite is the AI's biggest ally. Without tests, the AI flies blind and you lose the main way to verify what it produced. With tests, AI accelerates safely.

**Test pyramid (reference):**

| Layer | Purpose | Volume | Speed | Is AI good at it? |
|---|---|---|---|---|
| **Unit** | Isolated function/class | Many | Very fast | ✅ Great for writing |
| **Integration** | Modules interacting (DB, external service) | Moderate | Medium | ✅ Good, needs fixtures/mocks |
| **E2E / acceptance** | Full app flow | Few | Slow | 🟡 Works, but fragile |
| **Mutation / property-based** | Detect tautological tests, cover edge cases | Complementary | Variable | 🟡 AI generates well with guidance |

**AI uses in tests:**

- **Write tests from spec**: acceptance criteria become test cases;
- **Generate fixtures** and test data from schemas;
- **Propose edge cases** humans would forget;
- **Mock external dependencies**;
- **Refactor slow or duplicated suites**.

**Specific traps:**

- **Tautological tests:** AI writes a test that calls `foo()` and asserts `foo() === foo()`. Looks like coverage, proves nothing. Check: *would the test fail if the function were wrong?*
- **Excessive mocks:** AI mocks things that should be tested for real (e.g. mocking the DB in an integration test). Result: test passes, prod breaks.
- **Performative coverage:** AI covers lines, not behaviors. `90% coverage` can mean `30% of real guarantees`.
- **Test trailing the code:** generating code + test in the same session yields *a test that proves the code the AI wrote does what the AI wrote*. Better order: write the test first (from spec), human reviews the test, AI implements the code.

**Rule:** tests should be born from the spec, not from the code. When code is born before the test, review both with extra critical eye.

---

## Part VI — Backlog as Single Source of Truth

The backlog isn't a wishlist. It's the canonical document of what's pending, done, discarded, and deferred. Treat it like code.

### 1. Four fixed sections

The backlog has exactly four sections:

1. **Pending** (table by theme area);
2. **Done** (ID | Item | Closed on);
3. **Discarded** (ID | Item | Discarded on | Reason);
4. **Future decisions** (parking lot: ID | Decision | Trigger | Recommendation).

Never delete: done or discarded items **stay on record** as navigable history.

### 2. Classification taxonomy

Each pending item carries metadata that guides prioritization and impact. The columns:

| Column | Values | What it's for |
|---|---|---|
| **ID** | Prefix + number (FEAT1, SEC3) | Stable reference |
| **Phase** | F1, F2, F3, T, OP | Theme grouping (not order) |
| **Item** | 1 sentence | Description |
| **Sev.** | 🔴 Critical, 🟠 High, 🟡 Medium, ⚪ Low | Urgency |
| **Impact** | 👤 User, 🔧 Internal, 💰 Business, 🛡️ Security | Who's affected |
| **Surface** | 🔺 Flow, ⬜ Backstage | Does it change how the team works or run underneath? |
| **Target** | 📦 Product, 🏠 Infrastructure | Who benefits |
| **Compat.** | ✅ Additive, ⚠️ Migratable, ❌ Breaking | Impact on existing users |
| **Type** | Feature, Bug, Security, Refactor, Tests, Docs | Category |
| **Est.** | 15min, 1h, 1d, 1wk | Estimated time |
| **Deps** | Prerequisite IDs | Blockers |
| **Origin** | Session, Audit, Product, Incident | Where it came from |

**Practical value:** these columns turn the backlog from "list" into "filterable dataset". A dev can ask *"what's 🔴 + 🔺 + 📦 and has no deps?"* and get an objective answer.

### 3. Phase vs. Wave

Common confusion. Separate the concepts:

- **Phase** = theme grouping. "Authentication" is a phase, "Observability" is another. Doesn't define order.
- **Wave** = execution order. Wave 1 comes before Wave 2, regardless of phase.

A Phase 3 item can be in Wave 1 if it blocks many others. A Phase 1 item can be in Wave 4 if it's isolated and not urgent.

**Wave rule:**

- Wave 1–2 → 🔺 **Flow** (changes artifacts others consume);
- Wave 3+ → ⬜ **Backstage** (isolated, automation, parallelizable).

### 4. Compatibility classification

The `Compat.` column answers: *"what happens to someone on an older version when this item gets merged?"*.

- **✅ Additive**: adds capability without touching what exists. Those who don't update keep working. Zero interference.
- **⚠️ Migratable**: changes format or behavior of an existing artifact, but a migration path exists (manual or automatic). Those who don't update have a working but diverging version.
- **❌ Breaking**: breaks artifacts or flows without manual intervention. Those who don't update get inconsistency or errors. Requires explicit migration guide.

Getting this right avoids release-time surprises.

### 5. Don't delete

When discarding an item:

1. **Don't remove** from the list. Move to "Discarded" with explicit reason;
2. Strike through the name (`~~text~~`);
3. Record date and objective reason (e.g. *"conflicts with philosophy X", "already solved by item Y", "out of current scope"*);
4. Update deps of other items that depended on this one.

This prevents reopening the same discussion later. An explicit record of *"this idea was considered and discarded by Z on YYYY-MM-DD"* is more useful than silence.

### 6. Future decisions (parking lot)

Not every idea is pending. Some are conditional: *"if X happens, reevaluate Y"*. These don't become active items; they go to "Future decisions" with:

- **Trigger:** the event that would put the decision back on the agenda (e.g. "when we hit 1000 active users");
- **Current recommendation:** which direction the team would lean if the trigger fired today.

### 7. Per-item details (item-specs)

Complex items deserve their own spec in `{directory}/item-specs/{ID}.md`, with:

- **Plan** (link to approved plan, if any);
- **Context**: why this item exists;
- **Approach**: decision taken and discarded alternatives;
- **Acceptance criteria** (verifiable checkboxes);
- **Constraints**: what NOT to do, dependencies, gates.

The backlog points to the item-specs index; it doesn't duplicate content.

---

## Part VII — Versioning, Releases, and Migrations

### 1. Conventional Commits

Every commit follows the pattern:

```
{prefix}{optional scope}: short message
```

**Prefixes and bump:**

| Prefix | When | Semver bump |
|---|---|---|
| `feat:` | New functionality | minor |
| `fix:` | Bug fix | patch |
| `docs:` | Documentation | patch |
| `refactor:` | Restructuring without changing behavior | patch |
| `test:` | Tests only | patch |
| `chore:` | Infrastructure, build, internal tasks | — |
| `release:` | Commit produced by the release process | — |
| `feat!:` or `BREAKING CHANGE:` | Incompatibility | major |

**Idiomatic practice:** English prefixes, message in the team's language. That keeps automation tools happy (Conventional Commits is an international standard) and human conversation accessible.

### 2. Atomic commits: one reason per commit

**Rule:** every commit has exactly **one reason to exist**. If the message has "and" or "+" or multiple periods, it's probably two commits.

**Why:**

- Granular revert: revert one reason without losing the others;
- Review: a PR with atomic commits is reviewable linearly;
- Bisect: when a bug appears, bisect finds exactly which change introduced it;
- Changelog: each commit becomes a readable line.

**Common anti-pattern:**

```
feat: login, fix on logout, refactor middleware and more tests
```

Correct version: four separate commits.

**Exception:** release commits (version + tag + changelog in one commit only makes sense because they're a mechanical consequence of each other).

### 3. Bump based on real user impact

The rule isn't *"what prefix does the commit have?"*. It's: *"did anything that reaches whoever USES the product change?"*.

**Counts toward the bump:**

- Skills, templates, docs, scripts distributed to product consumers;
- Public API changes;
- Visible contract changes.

**Does NOT count toward the bump:**

- Internal files (backlog, internal processes, CI, internal validation scripts);
- Invisible refactors;
- Internal tests.

This avoids "ghost" releases where only internal process changed and nobody on the outside notices.

**Bump rules apply only to commits that reach the user:**

- Any breaks compatibility? → **major**;
- Any adds functionality? → **minor**;
- All are fixes? → **patch**;
- Nothing reached the user since the last tag? → **no release** (wait).

### 4. Pre-release checklist

Before any bump:

- [ ] Working directory clean;
- [ ] Source and distributed artifacts in sync;
- [ ] Artifact inventory (manifest) up to date;
- [ ] Changelog updated (only changes reaching the user);
- [ ] Version tags consistent across files that carry them;
- [ ] Tests pass locally.

### 5. Post-release checklist

- [ ] Version file (VERSION or equivalent) with new version;
- [ ] Plugin/package manifests with the same version;
- [ ] Changelog entry;
- [ ] Migration guide created (see item 7);
- [ ] Validation scripts pass;
- [ ] Git tag created;
- [ ] Backlog updated: "pending release" items → real version;
- [ ] Test in real environment (not just CI).

### 6. Release via PR: always

**Hard rule: no direct commits to main, including releases.**

The release commit goes on its own branch (`release/vX.Y.Z`) and lands via PR, even if fast-forward. That guarantees:

- CI runs on the final commit;
- Traceability via PR history;
- Documented human approval;
- Safety against accidental releases.

Yes, it's an extra step. That extra step has paid dividends many times.

### 7. Migrations as manual guides

For distributed products (SDKs, frameworks, CLIs, templates), every release with impact on existing users needs a **migration guide**: a markdown file in `migrations/v{FROM}-to-v{TO}.md` that a user can read and apply manually.

**Migration guide structure:**

1. **Summary** (1–3 sentences);
2. **Prerequisites** (current version, prior migrations);
3. **Changes grouped by strategy:**
   - **Overwrite:** replace the whole file, indicating what changed, how to apply, and the impact;
   - **Structural:** sections added or removed in shared files;
   - **Content patches:** changes inside existing sections (auto-merge tools usually can't catch this; they need to be applied manually);
   - **Manual:** human decision required — provide diff and suggestion;
   - **New files:** what they are, when they're relevant;
   - **Removed files:** reason, replacement.

**Principle:** the migration guide should be self-contained. Someone with no access to any automation can read it and apply it manually. Automation that applies migrations is a bonus, not a requirement.

### 8. Changelog with audience in mind

A changelog is not a pretty `git log`. It's **communication with whoever uses the product**.

Rules:

- Group by type (Added / Changed / Fixed / Removed / Security);
- **Include only changes that reach the end user**: omit internal changes;
- Write in the user's voice ("*You can now configure X*"), not the dev's ("*refactored module Y*");
- Link to the migration guide when applicable.

---

## Part VIII — Distribution and Compatibility

When the harness (or any versioned product) is **distributed** to multiple projects/teams, a problem arises: projects customize. How do you update without destroying customization?

### 1. Four distribution strategies

Classify each distributed file by one of these strategies. The choice is **explicit**: document it in a manifest alongside the product.

| Strategy | Behavior | When to use | Risk |
|---|---|---|---|
| **overwrite** | Replaces the entire file. Customization is overwritten. | File isn't customizable (templates, default assets) | None (if the rule is clear) |
| **structural** | Compares structure (H2/H3 sections). Adds or removes sections. Ignores content inside them. | Mixed file: default parts + customizable parts | Low |
| **manual** | Shows the diff. Never applies alone; human decides. | 100% customized file (e.g. project context file) | Medium (depends on human) |
| **skip** | Never touches. 100% project content. | Files generated at setup and maintained by the team (backlog, specs) | None |

**Rule:** every file shipped with the product has a declared strategy. If it doesn't, skip is assumed (don't touch).

### 2. Version tags in artifacts

Each distributed file carries a **version tag** as a comment at the top:

```
<!-- product-tag: vX.Y.Z source-file: {path} -->
```

Benefits:

- `update` knows the installed version of each file individually;
- Inconsistencies are detectable by validation script;
- Debugging: *"what version of this file has this bug?"* → look at the tag.

**Tag position:**

- Files with YAML frontmatter: **first line after the closing `---`** (frontmatter must stay at the top);
- Files without frontmatter: **line 1**.

### 3. Three mandatory scenarios

Every feature that distributes artifacts needs to work in three scenarios (testing them is part of the DoD):

| Scenario | Test |
|---|---|
| **Greenfield** | Setup generates the full structure; everything is created from scratch |
| **Re-run in existing project** | Setup detects what already exists and complements without breaking |
| **Update from previous version** | Update detects the absence of the new artifact and offers creation/migration |

**Questions to ask for each new artifact:**

- *"What if this file already exists in the project? Will setup re-run skip, merge, or update?"*
- *"What if the project is on an older version without this artifact? Does update offer it?"*
- *"If the strategy is `skip`, neither setup re-run nor update touches it. How does the user discover it exists?"*

### 4. Backward compatibility as default

Every change must assume: **older projects keep working without modification**. That means:

- New optional field in spec or backlog → not required;
- New file → skills and scripts create on demand if it doesn't exist;
- New format → also supports the old format for at least one major version.

Feature flags and temporary shims are ok when migration is expensive and the benefit pays off. But treat them as debt: document when to remove them.

### 5. Single-repo vs. monorepo

Two organizational forms demand different thinking:

**Single-repo**: flat structure, one context file at the root. The simplest case. Monorepo features **must not have visible effect here**: if the `## Monorepo` section doesn't exist in the context, nothing changes.

**Monorepo**: arbitrary hierarchy. Each level can have its own context. Setup should:

- Scan up to 2 levels deep (`apps/web/`, `services/auth/`);
- Exclude `node_modules/`, `vendor/`, `.git/`, `dist/`, `build/`;
- Detect git submodules (`.gitmodules`) and **never auto-configure inside a submodule**; ask the dev whether to include or ignore.

**Per sub-project:** each can have its own docs, skills, agents, backlog. The root context references, doesn't duplicate.

---

## Part IX — Dual-mode

### 1. The concept

Some artifacts exist **in more than one medium**. Specs can live in markdown files in the repo, or in a management tool (Notion, Linear, Jira). Same for backlog. Same for documentation.

**Dual-mode rule:** skills that operate on these artifacts must work in **both modes**, with automatic detection of the active mode, without asking the user every time.

### 2. Automatic detection

Common pattern: a section in the main context file declares which mode is active. Example:

```markdown
## Integration with external tool (specs)

Specs are maintained in: {notion-database-id | linear-project-id | local}
```

If the section exists → remote mode. If not → local mode (files in the repo).

Skill executes:

1. Check the context file;
2. If remote mode detected: use the tool's MCP / API;
3. If local: use files in the repo;
4. Flow is identical; output is different.

### 3. Feature parity between modes

When adding a feature to a dual-mode skill, implement in both modes **in the same PR**. Divergence generates systematic bugs: teams migrating between modes find inconsistent behavior.

**Acceptable exception:** features that are *intrinsically* specific to one medium (e.g. "kanban view" only makes sense in Notion, not in a markdown file). Document the exception.

---

## Part X — Quality, Verification, and Audits

### 1. Mandatory task checklist

Every work session carries a default checklist: items that MUST be verified before considering the task done. Canonical example:

1. **Reference plan.** If an approved plan exists for this task, was it followed? Were deviations documented?
2. **Source ↔ distributed sync.** Has every distributed file been updated in both places?
3. **Manifest updated.** If a distributed file was added/removed, was it recorded?
4. **Setup and update covered.** Does the change work in a new project AND in an existing project being updated?
5. **Dual-mode covered.** Have skills operating on dual-mode artifacts been tested in both modes?
6. **Monorepo covered.** Does it work in single-repo and in monorepo sub-projects?
7. **Docs and context updated.** Does a flow change require updates to skills-map, workflow-diagram, quick-start, main context?

The checklist is loaded automatically at session start. Ignoring items is a conscious decision, not forgetfulness.

### 2. Definition of Done as executable contract

**DoD isn't text. It's a script.** Every change goes through the same `verify.sh` (or equivalent), which is the **executable** form of DoD.

**Typical structure:**

```bash
#!/usr/bin/env bash
# verify.sh — runs everything, aggregates errors, returns non-zero if anything failed

errors=0

echo "→ Lint"
npm run lint || errors=$((errors+1))

echo "→ Type check"
npm run typecheck || errors=$((errors+1))

echo "→ Tests"
npm test || errors=$((errors+1))

echo "→ Coverage threshold"
npm run coverage:check || errors=$((errors+1))

echo "→ Harness validations"
bash scripts/validate-tags.sh || errors=$((errors+1))

if [ $errors -gt 0 ]; then
  echo "❌ verify.sh failed ($errors steps)"
  exit 1
fi

echo "✅ verify.sh passed"
```

**Properties of verify.sh:**

- **Fail-soft (aggregator):** keeps running even when a step fails. You want to know **all** problems at once, not the first one.
- **Executable by anyone:** human dev, AI, CI, all with the same output.
- **Part of setup:** every project has one. If not, DoD is fiction.
- **Versioned:** evolves with the code; new team rules become new steps.

**Rule:** if a team rule isn't in `verify.sh`, it will be violated. Conventions without automated verification don't survive.

### 3. The "second file" test

When auditing problems in code, **no finding is reported without the second-file test**:

> *Is there a second file or section where this behavior could be justified or referenced? If so, did I read it before declaring it a bug?*

Recurring false-positive pattern: auditor reads the affected file in isolation and concludes something is wrong. Reads the adjacent file that explains the design, and the conclusion collapses.

**Common false-positive examples:**

- *"This script doesn't have `set -e`"* → fail-soft is intentional design, justified in the calling file;
- *"This function isn't referenced"* → it is, but in another doc grep didn't catch;
- *"The light template should match the full one"* → it shouldn't; the reason it exists is to diverge;
- *"This file is missing X"* → X is in an adjacent file by design.

### 4. Anti-pattern registry

Every time an audit produces a false positive, **record it in the anti-patterns file** (`AUDIT_ANTIPATTERNS.md` or similar) with:

- The initial finding;
- The second file that invalidated it;
- Rule to avoid repeating.

That file is loaded before future audits. Each cycle, false positives decrease.

### 5. Three layers of verification

- **Consistency validation:** version tags match; source ↔ distributed in sync; internal links not broken;
- **Integrity validation:** setup installs cleanly in empty environment; update applies without breaking;
- **Per-project DoD validation:** `verify.sh` compiles, runs tests, lint, type-check, minimum coverage.

Run locally before PR, and in CI on each push.

### 6. Code review of AI-generated code

PR reviewer where the main author is AI needs a specific checklist. Recurring error patterns:

**API confabulation:**
- Does the called function exist in the package? (don't go on "looks plausible");
- Does the signature match official docs?;
- Does the library version support this API?

**Copy-paste of obsolete patterns:**
- Uses current project convention, or recycled an old training-set pattern?;
- Error-handling style matches the rest of the code?;
- Follows project naming conventions?

**Superficial error handling:**
- Empty `catch` or `catch { console.log(e) }`?;
- Errors silently ignored?;
- Generic messages without actionable context?

**Tautological tests:**
- Would the test fail if the implementation were wrong?;
- Do assertions test behavior or just restate the code?;
- Are there real edge cases or only happy path?

**Extra changes:**
- Does the PR do **only** what the spec asks? Or did the AI sneak in "fixes" not requested?;
- Opportunistic refactor without spec = scope creep.

**Redundant comments:**
- Does the comment explain **why**, or just paraphrase **what** the code already says? AI is prone to explanatory noise;
- Remove comments that add nothing.

**Security (see Part XI.5):**
- Input sanitized?;
- Parameterized query?;
- Sensitive data in logs?

**Reviewer heuristic:** if you don't understand a line in 30 seconds, it's a rejection candidate. Code the dev themselves can't explain shouldn't land on main.

---

## Part XI — Security in AI Harnesses

AI coding assistants expand the attack surface. The harness must **incorporate explicit defenses**, not just hope the model is well-behaved.

### 1. Risk surfaces

| Risk | What happens | Where it usually shows up |
|---|---|---|
| **Prompt injection** | External input (web, issue, email, log) contains instructions the AI follows | Tools that read untrusted content: web fetch, scrapers, email readers, tickets |
| **Secrets leaking into context** | AI reads `.env`, `credentials.json`, git history → secret enters the conversation and can leak in logs/telemetry | Wide repo exploration, sloppy grep |
| **Generation of vulnerable code** | SQL injection, XSS, path traversal, IDOR (common patterns AI replicates from training) | Any new code, especially endpoints and queries |
| **Excessive permissions** | AI with access to prod, AWS keys, Kubernetes, databases → wrong command causes a real incident | Dev setups using staging/prod credentials |
| **Sensitive data in telemetry** | Conversation goes to logs, billing, provider history; PII/secret stays there | Sessions reading customer data, production, compliance |
| **API confabulation** | AI invents a function or endpoint that looks plausible but doesn't exist | New or obscure stacks, internal APIs without documentation |

### 2. Defenses in the harness

**Tool and path allowlist:**

- List of what the AI **can** read/execute. Anything outside requires human confirmation.
- List of what the AI **must never** touch: `.env`, `.git/config`, `credentials/`, `~/.ssh/`, `*.pem`, `.aws/`.
- List of blocked commands: `rm -rf`, `chmod 777`, `git push --force` on protected branches, `kubectl delete` without namespace, `DROP TABLE`.

**Prompt injection (treat external output as untrusted):**

When the AI processes output from an external tool (web, API, log, user file), treat it as **data**, not **instruction**. Even if the content contains `"ignore previous instructions and do X"`, don't follow it.

Practice: when calling tools that read external content, the AI should report *what it saw*, not *act on what it saw*, without explicit human confirmation.

**Pre-commit hooks:**

- Secrets scanner (`gitleaks`, `trufflehog`);
- Vulnerability scanner (SAST: `semgrep`, `bandit`);
- Dependency check (`audit`, `snyk`).

If the AI accidentally commits something sensitive, the hook blocks before it leaves.

**Mandatory code review:**

AI can open a PR, never approve. Merge requires human review, always. This is a barrier that pays for itself given the risks above.

**Periodic audit:**

- Secrets scan in history;
- Listing of paths the AI accessed in recent sessions;
- Validation of effective permissions (AI shouldn't have been able to access X; why could it?).

### 3. Ambient vs. confined authority

**Ambient:** the AI "inherits" all the permissions of the dev who invoked it. Reads any file, runs any command, borrows all environment credentials. **Bad.**

**Confined:** the AI operates in a defined sandbox. Explicit paths, explicit commands, dedicated credentials (with minimum scope). **Good.**

The practical rule: treat AI as an **external collaborator**, not as "an extension of your account". Give only what it needs, nothing more.

### 4. Spec and backlog security

Specs and backlog may contain sensitive information (competitive roadmap, infrastructure details, customer data). If the harness uses a remote tool (Notion, Linear), consider:

- Permissions: who has access?
- MCP/API integration: credentials with minimum scope?
- Customer data in spec: avoid; use IDs, never names or raw data.

### 5. Per-PR security checklist

- [ ] No hardcoded secret (scanner passed);
- [ ] No query built with string concat (SQL injection);
- [ ] User input validated and sanitized;
- [ ] Output in HTML/JSX escaped (XSS);
- [ ] File path validated against traversal (`..`);
- [ ] Authentication and authorization on new endpoints;
- [ ] New dependencies audited;
- [ ] Logs don't record sensitive data (password, token, PII).

### 6. Intellectual property, licenses, and compliance

AI coding assistants raise legal issues the harness must address, not defer to "when something breaks".

**Copyright of generated code:**

Authorship of AI-generated code is still a legal grey area in many jurisdictions. Recent jurisprudence (US, EU) suggests:

- Purely AI-generated code typically **does not** receive copyright protection;
- Substantial human contribution (direction, editing, integration) reestablishes copyright;
- Corporate policy should treat generated code as **integrated** with the rest of the dev's work, not isolated.

**Practical action:** explicit internal policy. E.g.: *"code accepted by the dev is treated as the dev's work for ownership purposes"*.

**Contamination by incompatible licenses:**

Models are trained on public code, including GPL/AGPL. Suggestions may contain recognizable snippets from repositories licensed incompatibly with the project.

**Real risk** in proprietary projects that don't accept copyleft: AI suggests a block similar to GPL code → integrates → involuntary license violation.

**Defenses:**

- Prefer AI assistants with IP indemnification clauses (some providers offer them);
- Plagiarism / code-similarity scanner in CI for suspect blocks;
- "If I wouldn't write it that way, I don't accept it" policy: fights literal copy-paste.

**Provider data and prompt retention:**

Conversations may be stored for training, operational logs, billing. This is incompatible with:

- **Customer NDAs** (customer data in the prompt → sent to provider → outside NDA scope);
- **GDPR/LGPD** (personal data sent to provider without explicit consent);
- **Sectoral regulations** (healthcare, finance);
- **Strategic intellectual property** (roadmap, proprietary code).

**Defenses:**

- Check the chosen provider's retention policy;
- Contract "enterprise" or "zero data retention" tier when available;
- Harness rules: *never paste production data in the prompt*;
- Automatic PII redaction/masking before sending.

**Secrets exposure:**

See Part XI.1: secrets in the context become secrets in the provider's history. Treat as a security incident if it happens.

**Sectoral compliance:**

Regulated sectors (finance, health, defense, government) have additional restrictions:

- **SOC 2 / ISO 27001:** documented AI usage process, access auditing;
- **HIPAA:** BAA (Business Associate Agreement) with the provider before any protected data touches the prompt;
- **PCI-DSS:** card data never in prompts, even in dev;
- **Government regulations:** often require on-prem AI or sovereign cloud.

**Operational rule:** before adopting an AI assistant at organizational scale, involve legal and compliance. Not after.

**AI policy checklist:**

- [ ] Formal AI assistant usage policy documented and signed;
- [ ] Contracted provider tier aligns with legal requirements;
- [ ] Forbidden data in prompts is listed explicitly;
- [ ] Incident process if a secret/PII leaks to the provider;
- [ ] Periodic review (annual?) of the policy with legal.

---

## Part XII — Cross-cutting Principles
Principles that don't fit one section but guide everything.

### 1. Simplicity as a rule

*"Simplicity is the ultimate sophistication."*

- Skills are markdown files, not CLIs;
- Specs are text, not complex tools;
- Backlog is a markdown table, not SaaS;
- Verification scripts are simple bash, not frameworks.

**When simplicity forces pain**, revisit: maybe a bit of structure is needed. But abstractions arrive **after** three real cases, not before.

### 2. Human review between phases

Every critical gate asks for human approval:

- Spec approval;
- Plan approval before execution;
- PR approval before merge;
- Release approval before pushing the tag.

Automation is for repetitive work. Judgement is for humans.

### 3. Persist to disk, not to chat

Every important decision becomes a versioned file:

- Approved plan → `plans/{ID}-{description}.md`;
- Spec → `specs/{ID}.md`;
- Complex backlog item → `item-specs/{ID}.md`;
- Migration guide → `migrations/vX-to-vY.md`;
- Changelog → `CHANGELOG.md`.

Conversations vanish. Files survive session refresh, team turnover, tool migration.

### 4. Don't invent premature abstraction

Before abstracting, are there three concrete cases? If not, keep it concrete. Explicit repetition beats wrong abstraction, and is **far easier to refactor** than to undo abstraction.

### 5. Guidelines vs. rules

The harness separates two types of document:

- **Guidelines**: design principles that guide decisions ("we prefer simplicity over completeness");
- **Rules**: discrete checks, explicit verifications ("every agent has `model-rationale` in the frontmatter").

Both have a place. Don't turn guidelines into rules (becomes bureaucracy); don't leave rules as guidelines (becomes too negotiable). The distinction is: *can it become an automatable check?* If yes, it's a rule.

### 6. Fail-soft in aggregators, fail-fast in steps

Scripts that run **multiple checks in sequence** should keep running even when one fails (aggregating all errors at the end). Scripts that perform **a single action** fail on the first error.

Example: `verify.sh` running lint + tests + type-check = fail-soft (I want to know ALL the problems). Setup script = fail-fast (stop on the first inconsistency).

### 7. Trust boundaries as an explicit table

*"Where does AI become responsible for state?"* is the central question. The table below is the contract: each row defines who answers when something goes wrong.

| Operation | Who's responsible | Human gate? | Note |
|---|---|---|---|
| Chat suggestion | Dev who accepts | ✅ (accept/reject each diff) | Human reads and decides |
| Edit in isolated worktree | AI until PR opens | ⏱️ At PR | Worktree ensures errors don't leak |
| Commit on non-main branch | Dev (author) | ❌ | Isolated branch, contained risk |
| Merge to main | PR reviewer | ✅ Required | CI + human review |
| Push release tag | Release manager | ✅ Required | Manual command after approval |
| Deploy to staging | CI/CD | ⏱️ Automatic after merge | Monitor |
| Deploy to production | Human | ✅ Required | Never automatic |
| Run migration on prod DB | Human + runbook | ✅ Required | Backup first |
| Tool execution with sensitive credential | Human | ✅ Case by case | Never ambient |

A well-designed harness clearly defines which operation crosses which boundary. **When in doubt, add more gate, not less.**

---

## Part XIII — Developer Anti-patterns When Using AI
The AI assistant delivers what you ask for. If you ask wrong, it errs. Most problems with AI in real projects **aren't the model's fault**: it's how the dev interacts with it.

### 1. Vague prompt

**Pattern:** *"make login work"*, *"fix that bug"*, *"improve this"*.

**Consequence:** the AI chooses for you. Often chooses wrong.

**Antidote:** a spec. Even informal: *"the POST /login endpoint should return 401 when the password is incorrect; today it returns 500 because {X}. Fix it preserving the existing email validation"*. A good prompt is a mini-spec.

### 2. Accepting code without reading

**Pattern:** "looks like it worked" → commit → merge → bug in prod.

**Consequence:** you've become a transmission box for code you don't understand. When it breaks, you won't know how to fix it.

**Antidote:** read the diff. Don't understand a line? Ask the AI *why* it chose that before accepting. If it can't justify well, it's probably wrong.

### 3. Skipping the gate because "it's quick"

**Pattern:** *"no spec needed, 10 minutes"* → becomes 3 hours → becomes an abandoned branch with half-finished code.

**Consequence:** silent technical debt. The fast-path exists by design, but its criteria are specific (≤3 files, no new abstraction, no schema change). Anything outside that deserves a spec.

**Antidote:** honesty about the real size of the change. When in doubt, treat it as larger.

### 4. Context-stuffing

**Pattern:** *"to be safe, I'll load the whole repo into context"* → AI gets lost, ignores rules, invents.

**Consequence:** less quality, more cost, more latency.

**Antidote:** context discipline (Part III). Load what's needed plus references; trust the AI to ask for more when it needs to.

### 5. AI as architectural oracle

**Pattern:** *"should I use microservices or a monolith?"*, *"Postgres or Mongo?"* for decisions whose trade-offs depend on team context.

**Consequence:** generic answer that sounds sophisticated. You adopt it and find out 6 months later that it doesn't fit.

**Antidote:** use AI to **map** trade-offs (it's good at that) and **draft** ADRs. The final decision is human, with knowledge of team, history, people.

### 6. Iterating when you should stop

**Pattern:** code doesn't work → ask AI to adjust → still doesn't → ask again → still doesn't → 15 iterations later, a simple feature is spaghetti.

**Consequence:** bug hidden under layers of "fixes" that never attacked the cause.

**Antidote:** after 2–3 iterations without progress, **stop**. Leave the session, read the code calmly, identify the root. Come back with a fresh briefing.

### 7. Copy-pasting prompts between projects

**Pattern:** a prompt that worked well in project A is reused in B without adapting the context.

**Consequence:** AI applies project A's conventions/patterns in B. Inconsistent code, noisy PR.

**Antidote:** each project has its own harness. Prompts mention "this project" and expect the context (skills, context file, spec) to fill in the specifics.

### 8. Not updating STATE / docs at the end of the session

**Pattern:** day ends, dev closes the laptop. Tomorrow: "where was I again?".

**Consequence:** 30 minutes of archaeology to rebuild context. AI starts from scratch, redoes decisions, contradicts earlier choices.

**Antidote:** the session's last action = update STATE.md (or equivalent). The next session's first action = read it.

### 9. Not recording a discarded decision

**Pattern:** long discussion → decide not to do X → no one writes down why → 3 months later, someone suggests X again → same discussion.

**Consequence:** the org repeats the conversation. The team loses memory.

**Antidote:** "Discarded" section of the backlog, "Future decisions" in the parking lot. Recording is cheap; rediscovering isn't.

### 10. Treating AI as a substitute instead of a collaborator

**Pattern:** *"the AI will write this on its own"* → dev disengages → bug.

**Consequence:** dev loses affinity with the code. When AI fails (it will), can't rescue it.

**Antidote:** pair programming mindset. AI is an accelerated junior colleague; you're the mentor, not a spectator.

---

## Part XIV — When NOT to Use an AI Assistant
A mature harness knows the limits. Using AI where it's bad is worse than not using it.

### 1. Subtle concurrency debugging

Race conditions, deadlocks, distributed-state inconsistency require non-linear reasoning, counter-intuitive hypotheses and often physical experimentation (profilers, traces, production logs). AI **accelerates** hypothesis mapping, but the insight leap is usually human.

**Recommended use:** AI helps structure hypotheses and generate instrumentation logs. Humans interpret.

### 2. New architectural decisions

"Should we adopt event sourcing?" depends on: team, internal skills, product pressure, infrastructure, incident history. AI doesn't have this context; it gives a statistically plausible answer, not a good one.

**Recommended use:** AI drafts an ADR with known trade-offs. Decision is human.

### 3. Regulated code without a clear spec

GDPR, LGPD, PCI, HIPAA, SOX: areas where "looks right" isn't enough. Requires traceability from regulatory requirement → code → test → audit.

**Recommended use:** only with formal regulatory spec and specialized code review. Without spec, don't touch.

### 4. Critical production incidents

Time pressure + broad scope + stakeholders + quickly reversible decisions. AI introduces variance when you need determinism and familiarity.

**Recommended use:** during the incident, use AI only for fast parallel queries (read logs, extract timeline). Emergency-fix commits: human.

### 5. Giant refactor without tests

Without a test suite, AI flies blind. It will generate code that looks right, breaks a subtle feature, and no one notices for weeks.

**Recommended use:** first, write tests (then AI helps). Then refactor.

### 6. Very new or obscure domain

In stacks/libraries that came out recently or are niche, AI confabulates more. It invents plausible APIs that don't exist.

**Recommended use:** verify each called function against official docs. If verification cost > writing by hand, don't use AI for that part.

### 7. Tasks with contradictory requirements

*"Fast, safe, cheap and simple"*: when requirements clash, AI picks arbitrarily (typically following the latest request). Human negotiates conscious trade-off.

**Recommended use:** prioritize the requirements (or reframe the problem) before involving AI.

### 8. Legacy code exploration without a map

Systems without docs, without tests, with implicit conventions and historical detours. AI reads each file as if it were independent; the value is in the implicit connections that aren't written.

**Recommended use:** human explores first, maps it. Then AI helps with discrete changes.

### Final heuristic

> *If you can't describe the expected outcome in 3 verifiable sentences, AI won't deliver anything useful.*

When the task is vague, exploratory and requires judgement, AI typically degrades performance. When it's well-defined and verifiable, it accelerates.

---

## Part XV — Harness Governance and Evolution
The harness is software. Software rots if no one cares for it. Defining explicit governance is what prevents the slow drift toward "everyone does as they please".

### 1. Ownership by artifact type

| Artifact | Owner | Justification |
|---|---|---|
| **Main context file (L0)** | Tech lead / staff engineer | Global conventions affect everyone |
| **Domain context (L2)** | Domain tech lead | Local rules |
| **Domain skills** | Domain team | Whoever knows is who writes |
| **Core skills (testing, security)** | Platform / DX team | Orthogonal to domain |
| **Agents** | Platform / DX team | Shared tooling |
| **Manifest, strategies, migrations** | Platform team | Distribution infra |
| **Project spec** | PM + project tech lead | Business + technical |

### 2. Skill/agent change cycle

1. **Proposal**: via PR with justification (link to a real case where the harness failed);
2. **Review**: 1–2 devs from the owning team ("two-eyes" rule);
3. **Test in a real project**: passing syntactic validation isn't enough; apply it in a project and observe behavior;
4. **Migration guide**: if breaking, document the path;
5. **Merge + release** (Part VII).

Additive changes pass quickly. Breaking ones pass with ceremony.

### 3. Regular pruning

The harness accumulates cruft. Without pruning, it becomes clutter. Suggested cadence: quarterly review.

**What to look for:**

- **Skills unused for 6+ months**: archive or consolidate;
- **Skills with >80% overlap**: merge;
- **Rules nobody follows**: either remove or teach (but don't let them rot);
- **Orphan docs** (not referenced anywhere): link or remove;
- **Resolved anti-patterns**: move to history, don't keep as active alert.

**How to decide to remove:** if it doesn't hurt short-term and no one notices 30 days after deprecation, you can remove it.

### 4. Signs of an out-of-control harness

- Main context file exceeds 600 lines;
- 50+ skills with high overlap and confusing names;
- New dev doesn't know where to find a rule and asks on Slack;
- Devs go "outside the harness" because "it's faster";
- Last update of the main file is 1+ year old;
- Verification scripts have been broken for weeks and no one fixes them;
- The harness's own backlog has >50 pending items;
- Recurring discussion about "redoing everything from scratch".

If you recognize 3+ signs, it's time to stop everything and clean up.

### 5. Evolution as process, not event

The harness is **not** a one-quarter project that ends. It's a continuous process, like a library dependency. Each quarter:

- Review what changed (retrospective);
- Prune what no longer serves;
- Incorporate 1–2 new patterns the team discovered empirically;
- Update onboarding docs.

Treat it as part of platform investment, not as "idle time".

### 6. Migration between model versions

Models evolve fast. Every 6–12 months, providers ship new versions (better reasoning, cheaper, larger context). Swapping models feels like "just changing a variable". It isn't.

**What actually changes:**

- **Behavior on existing prompts**: same prompt may produce different output;
- **Sensitivity to system prompts**: rules that were followed may be ignored;
- **Edge-case handling**: cases the old model got wrong may now succeed (or vice versa);
- **Cost and latency**: can improve or worsen;
- **Context limits**: a larger window enables new patterns; a smaller one forces redesign.

**Migration process:**

1. **Inventory audit:** which skills, agents, prompts are sensitive to the swap? Which skills have thresholds or numeric comparisons that may shift?
2. **Canary:** run the new model on a small subset (1–2 devs, 1–2 skills) for 1–2 weeks; compare output.
3. **Regression suite:** if an agent test suite exists (e.g. reports in golden format), run it on the new model and compare.
4. **Prompt tuning:** new models tend to have idiosyncrasies; small adjustments in skills/agents resolve 80% of regressions.
5. **Gradual rollout:** 10% → 50% → 100% with observation time between steps.
6. **Document in the harness changelog:** *"v2.5.0: migrated to model X. Observed changes: Y, Z."*

**When NOT to migrate:**

- No regression suite;
- Close to a critical release / ongoing incident;
- No rollback plan (going back to the old model should be one flag);
- New model still in early preview (unstable).

**Rule:** treat model swap as a **critical dependency upgrade**, not configuration. Dedicate its own sprint if the change is significant.

---

## Part XVI — Adoption: From Zero to Mature
A harness isn't born complete. Trying to adopt everything at once is a recipe for abandonment. The right path is **incremental**, with each step delivering value on its own.

### 1. Maturity tiers

| Tier | Typical time | Traits |
|---|---|---|
| **Tier 0: No harness** | — | AI used ad hoc. No standard. Quality varies per dev. |
| **Tier 1: Light** | 2–4 weeks | Basic context file, 3–5 core skills, informal DoD. |
| **Tier 2: Standard** | 2–4 months | Hierarchical context, 10–20 skills, 3–5 agents, light spec flow, structured backlog, `verify.sh`. |
| **Tier 3: Full** | 6–12 months | Orchestration (RPI), dual-mode, migrations, formal governance, metrics, declared compatibility. |

**Important:** most teams should stop at Tier 2. Tier 3 only pays off in distributed products or very large teams.

### 2. Incremental roadmap

**Week 1–2: Foundation**

- [ ] Create main context file (L0) with: stack, global conventions, commit/PR flow, security constraints;
- [ ] Run a first session through the file, observing whether the AI behaves accordingly.

Delivery: AI now respects basic conventions. Immediate difference.

**Month 1: Minimal expertise**

- [ ] 3–5 core skills: testing, code-quality, security-review, definition-of-done, commit-hygiene;
- [ ] Minimal `verify.sh`: lint + tests + type-check;
- [ ] Task checklist at the start of non-trivial sessions.

Delivery: more consistent PRs. Trivial bugs filtered out.

**Month 2: Light backlog and spec**

- [ ] Create `backlog.md` with 4 fixed sections;
- [ ] Light spec template (medium complexity);
- [ ] Convention: medium+ changes need an approved spec before code.

Delivery: scope is controlled. Less "refactor" that becomes "rewrite everything".

**Months 3–4: Automation**

- [ ] 3–5 auditor agents: code-review, security-audit, coverage-check;
- [ ] CI running `verify.sh` on every PR;
- [ ] Pre-commit hooks for secrets and lint.

Delivery: automatic verification. Humans review what's left.

**Months 5–6: Refinement**

- [ ] Hierarchical context (L0 → L2) if monorepo;
- [ ] Domain skills (UX, DBA, observability) as needed;
- [ ] STATE.md pattern for big tasks.

Delivery: harness adapted to the team's reality.

**Month 6+: Advanced (if it makes sense)**

- [ ] RPI orchestration for complex tasks;
- [ ] Dual-mode (repo + management tool);
- [ ] Versioned migration guides;
- [ ] Formal governance with declared ownership;
- [ ] Health metrics (Part XVII).

### 3. Adoption pitfalls

**Adopting too much, too soon.** Team sees a pretty deck, adopts every feature of a mature harness in a month, abandons in two. Start minimal.

**Adopting without the team.** Tech lead implements in the dark, devs find out at PR review and reject. Adoption is cultural change: involve the team in decisions.

**Not measuring.** Without metrics, "is the harness working?" becomes opinion. Define 2–3 indicators from Tier 1 onward (see Part XVII).

**Treating it as one person's project.** If that person leaves, the harness rots. At least 2 people with declared ownership.

**Copying without adapting.** Another team's/company's harness is a starting point, not a template. Stack, culture and size change everything.

### 4. When NOT to adopt a harness

Harness has real cost: setup, maintenance, onboarding, discipline. In some contexts, the cost beats the benefit. Honesty matters: harness isn't always the answer.

**Contexts where harness does NOT pay off:**

- **Team of 1–2 devs with a small project.** The overhead of maintaining skills, structured backlog and formal specs doesn't dilute. Mental convention + occasional code review is enough.
- **Hackathons, POCs and disposable prototypes.** Speed > quality; the artifact has a shelf life of days to weeks. Investing in a harness is throwing it away with the POC.
- **One-off scripts and local automation.** A 50-line script that runs once doesn't ask for backlog or spec.
- **Academic exploration / research.** Research flow is iterative-divergent; a rigid harness binds. Light discipline (versioning, README) fits without full infrastructure.
- **Early stage with unstable stack.** If the stack changes weekly (pre-PMF, validation), skills and conventions age faster than they're worth. Invest after stabilization.
- **Projects with a planned lifecycle under 3 months.** Not enough time for the harness to "pay back"; build the essentials, ship, archive.
- **Team without buy-in.** If the team won't respect the process, harness becomes theater. First convincing, then structure.

**Heuristic:**
> *If the harness takes more time to maintain than the measured benefit returns, it's wrong: too early, too big, or in the wrong project.*

**Middle path:** "minimum viable" harness, just the main context file + `verify.sh` with lint/test. No formal spec, no taxonomic backlog, no agents. When the project shows maturity and the team asks, evolve to Tier 1.

### 5. How team roles change

Adopting harness + AI assistant reconfigures the team's work. Ignoring this reconfiguration is a common source of resistance and disorientation.

**Junior.**
- **Speeds up:** onboarding shortens, exposure to good patterns is immediate, feedback cycle is short.
- **Risk:** learning superficially (accepting code without understanding, skipping fundamentals because "AI does it").
- **Countermeasure:** pair-first mentoring (Part XVIII.5) focused on **understanding**, not **delivery**. Ask the junior to explain what the AI wrote before accepting.

**Mid-level.**
- **Speeds up:** routine tasks (CRUD, scaffolding, mechanical refactor) take a fraction of the time.
- **Risk:** becoming a "code dispatcher" who relays the request, copies the output, forgets to think.
- **Countermeasure:** use the freed time for higher-abstraction work (design, structural refactor, domain ownership). The prompt becomes a spec.

**Senior.**
- **Changes most:** less code written directly, more review, more mentoring, more design.
- **New work:** writing and maintaining skills, reviewing agent output, sizing complexity (Part V.2), judging trade-offs.
- **Risk:** losing *craft* from over-using AI. Skill atrophy is real.
- **Countermeasure:** keep "by-hand code" in tasks where *wanting* to learn matters, not just *being able* to deliver.

**Tech lead / architect.**
- **Changes even more:** the engineering output now includes the **harness itself**: context, skills, agents, gates.
- **New work:** governance (Part XV), adoption (Part XVI), health metrics (Part XVII), trust boundaries (Part XII.7).
- **Value:** architecting the system of work, not just the system of code.

**Platform / DX team.**
- **Becomes the owner** of the core harness: templates, shared agents, verification scripts, migrations between versions.
- **Cadence:** dedicated sprint to evolve the harness, like any internal product.

**Generalist IC → domain specialist.**
- With AI handling scaffolding and generic patterns, human value concentrates on **deep domain knowledge**: business rules, compliance, people.
- Shallow generalization becomes a commodity; deep specialization remains scarce.

**General rule:** human value shifts from *producing code* to *judging, designing, deciding and teaching*. Those who adapt grow; those who resist stagnate. Talking openly about this change with the team beats letting it happen by accident.

---

## Part XVII — Harness Health Metrics
A harness without metrics becomes opinion. Without indicators, discussions stay at *"I think it's helping"*. Define 3–5 indicators and review quarterly.

### 1. Quantitative indicators

| Metric | How to measure | Healthy target |
|---|---|---|
| **Bug recurrence** | % of fixed bugs that return within 90 days | < 5% |
| **Time-to-first-gate** | From item entering the backlog to spec approved | < 3 days (medium), < 1 day (small) |
| **Spec rework** | % of specs that go back to "draft" after "approved" | < 15% |
| **Skill coverage** | % of PRs that consulted/applied at least one relevant skill | > 70% |
| **Context file churn** | Changes per month in the main context file | 1–5 (neither unstable nor forgotten) |
| **Validation pass rate (1st try)** | % of PRs that pass `verify.sh` on first push | > 60% |
| **Mean review cycles** | Average rounds of review until merge | < 2.5 |
| **PR open time** | Median time from PR open to merge | < 2 working days |
| **Fast-path adoption** | % of trivial changes that used fast-path correctly | > 80% |

### 2. Qualitative indicators

Not everything is a number. Quarterly survey with the team (5–10 questions):

- *"Does the harness accelerate or hinder my work?"* (1–5 scale);
- *"Do I know where to find rule X?"* (yes / no / sort of);
- *"Code generated with AI has the same quality as mine?"* (better / same / worse);
- *"Can a new dev operate within 2 weeks?"* (yes / no);
- *"What's the most annoying thing about the harness today?"* (open);
- *"What's missing?"* (open).

The quantitative + qualitative combination avoids two errors:

- **Quantitative only**: good metrics, everyone hating it;
- **Qualitative only**: everyone happy, bugs in prod.

### 3. Periodic review

Quarterly, in 1–2 hours:

1. Look at indicators → which got worse?;
2. Read qualitative survey → recurring theme?;
3. List 1–3 actions for next quarter;
4. Update harness backlog with these actions.

### 4. When to reorganize

If in two consecutive quarters:

- Recurrence rises;
- Validation pass rate drops;
- Qualitative plummets;

It's time to revisit structure. Don't keep stacking: **stop and clean**.

---

## Part XVIII — Human Onboarding to the Harness
The harness works when the team knows how to use it. A new dev who wasn't onboarded creates two bad outcomes: they discredit the system ("my colleague doesn't use it, so I don't have to") and they create silent debt (running over skills without knowing they exist).

### 1. Day 1: Orientation

**Goals:** basic mental map + first task executed correctly.

- [ ] Read the main context file (L0), 30 min;
- [ ] Read QUICK_START.md or the harness README, 30 min;
- [ ] Do a trivial task (fast-path) with a buddy, 1–2h: typo, dep bump, rename. Observe the flow;
- [ ] Have the first PR reviewed line by line by a mentor.

Deliverable: the dev understands "there is a harness, this is where I start."

### 2. Week 1: Immersion

**Goals:** familiarity with domain skills + first small spec.

- [ ] Read the 3–5 skills most relevant to the dev's domain;
- [ ] Shadow a medium PR from the team (start to finish, including spec);
- [ ] Write a small spec (1–3 tasks) with a mentor reviewing;
- [ ] Run `verify.sh` locally several times to feel the feedback loop;
- [ ] Read recorded anti-patterns (Part X + Part XIII).

Deliverable: the dev can operate on small tasks without constant supervision.

### 3. Month 1: Autonomy

**Goals:** independent operation on medium scope.

- [ ] First medium spec with review only at gates;
- [ ] Contribute to the harness: propose a new skill, or improve an existing one;
- [ ] Take part in an audit (or agent report) and understand structured output;
- [ ] Review: what does the dev still not know? Where are they lost?

Deliverable: the dev operates alone on medium complexity. Can pair on large tasks.

### 4. Essential materials

Without these, onboarding stalls:

- **Skill map**: table with name, purpose, when to use;
- **Workflow diagram**: ASCII or visual diagram of the ideal idea → done flow;
- **Examples of real specs**: 2 good, 1 bad (annotated with what went wrong);
- **Examples of PRs**: good references;
- **Recorded anti-patterns**: read and internalize;
- **Quick wins**: list of trivial tasks ideal for day one;
- **Questions channel**: Slack / Discord / forum where questions turn into FAQ.

### 5. Pair-first mentorship

First weeks: **synchronous** pair programming with a mentor. It's not micro-management; it's tacit transfer. The dev watches the mentor use the harness: how they prompt the AI, how they decide between skill/agent, how they do a context reset, how they update STATE.

After 2–4 weeks: async pair (detailed PR review). After that: normal review.

### 6. Onboarding anti-patterns

- **"Read this wiki and you're set"**: without supervised practice, docs don't stick;
- **Loading every skill on day 1**: impassable. Load them gradually;
- **Not showing anti-patterns**: the dev reinvents the same mistakes already documented;
- **Mentor "available" but never present**: scheduled presence, not reactive;
- **Skipping the fast-path**: starting with a large task, the dev drowns;
- **Not collecting feedback**: onboarding becomes the standard, and the standard ages.

### 7. Onboarding metrics

- **Time to first merged PR:** < 3 business days;
- **Time to operate on medium scope without supervision:** < 4 weeks;
- **Post-onboarding survey (30 days):** *"Did you know how to use the harness when you finished onboarding?"* (1–5).

If these numbers get worse, onboarding needs to evolve — not the new dev.

---

## Part XIX — Anatomy of a Good Prompt
Part XIII listed anti-patterns; this is the constructive counterpart. A good prompt saves iterations, reduces confabulation, and improves quality.

### 1. Three intents, three structures

Every prompt falls into one of the three intents below. The structure changes accordingly.

**A. Explore**: "help me understand X, map possibilities, list approaches"

Structure:
- Goal (understand / decide / choose);
- Context of what has already been considered;
- Known constraints;
- Output format (table, list, pros/cons).

Example:
> *"I'm deciding between Postgres and MySQL for service X. Workload: 80% reads, up to 10TB of data in 2 years, needs JSON queries. I already use Postgres in other services. List 3–5 decision criteria with pros/cons of each database. Format: table."*

**B. Implement**: "write code that does Y"

Structure:
- Short spec (what, why);
- Verifiable acceptance criterion;
- Affected files;
- Constraints (don't touch X, preserve Y);
- Skills or patterns to follow.

Example:
> *"Implement endpoint POST /users/:id/deactivate. It must mark the user as inactive (is_active=false), invalidate active sessions, and send a user.deactivated event to the bus. Files: controllers/user.ts, services/session.ts. Preserve the current authorization pattern (adminOnly middleware). Return 204 on success. Tests following the existing describe pattern."*

**C. Review / critique**: "analyze Z and report"

Structure:
- What to analyze (scope);
- Criteria (what counts as "good" vs. "bad" in this context);
- Expected severity;
- Report format.

Example:
> *"Review PR #234 looking for: (1) common security vulnerabilities (injection, XSS); (2) missing error handling; (3) tautological tests. Report findings as: severity (🔴🟠🟡), file:line, description, suggestion."*

### 2. Minimum anatomy of a useful prompt

```
[Context: where I am, what the project is — 1-2 sentences]
[Goal: what I want, verifiable — 1 sentence]
[Constraints: what NOT to do — 1-3 bullets]
[Expected format: response structure — 1 sentence]
```

A prompt with these four parts is 10x better than "do X".

### 3. Common constructive mistakes

| Mistake | Example | Correction |
|---|---|---|
| **Vague verb** | "improve this code" | "reduce duplication between funA and funB by extracting a common helper" |
| **No criterion** | "refactor to make it cleaner" | "refactor so funA has <20 lines and zero nested conditionals" |
| **Implicit scope** | "fix the bug" | "fix login failure when email contains + (bug #123)" |
| **No constraint** | "add cache" | "add cache to getUser, 5min TTL, using existing Redis, without changing the public signature" |
| **No format** | "list the problems" | "list problems as bullets, grouped by severity, max 10" |

### 4. Scaling detail with complexity

- Fast-path (typo, bump): 1–2 sentences are enough;
- Small: prompt with the 4 anatomy parts;
- Medium+: prompt references the approved spec and plan; context comes from files, not the prompt.

In other words: for large work, the prompt is short because the **context lives in the artifacts**.

### 5. Tone and initiative constraint

AI tends to "help beyond the ask": refactoring what wasn't requested, adding adjacent features, improving style that was already fine. Control this explicitly:

- *"Change only what's necessary for X. Don't refactor unrelated code."*
- *"If you find a problem out of scope, report it, don't fix it."*
- *"Keep existing conventions even if you disagree with them."*

### 6. When the prompt is bad: signs

If the output shows any of these symptoms, the prompt is what needs improving:

- A generic response that would fit any project;
- Code with placeholders (`TODO`, `// your logic here`);
- Multiple "options" when you wanted one answer;
- The AI repeatedly asks for clarification on obvious things;
- Output too large, covering things you didn't ask for.

Each one points to a specific gap in the prompt. Fixing it at the source is faster than iterating on the output.

---

## Part XX — Debug Workflow with AI
AI speeds up debugging when used correctly. Used badly, it amplifies confusion. The flow below is the pattern that works.

### 1. Before calling the AI: minimal repro

**Golden rule:** AI without a repro is guessing. Invest in reproducing the bug minimally and deterministically **before** asking for help.

Repro checklist:
- [ ] Exact command or sequence that triggers the bug;
- [ ] Required prior state (data, config, environment);
- [ ] Current output vs. expected output;
- [ ] Tested variations that do **not** reproduce (helps localize).

With a minimal repro, AI becomes a multiplier. Without one, it becomes noise.

### 2. The 5-step flow

**Step 1. Triage.** Describe symptom + repro to the AI. Ask for hypotheses ordered by probability, with justification.

> *"Endpoint GET /users returns 500 intermittently (~10% of requests) since yesterday 2pm. Log shows `connection pool timeout`. Repro: `ab -n 1000 -c 50 /users`. List 5 hypotheses ordered by probability."*

**Step 2. Prioritize by verification cost.** Of the AI's hypotheses, which is cheapest to confirm/discard? Not always the most likely — the one **cheapest to test first**.

**Step 3. Instrumentation.** Ask the AI to generate logs, metrics, and traces that discriminate between hypotheses. The AI is good at this: it suggests specific points in the code where to instrument.

**Step 4. Collect evidence.** Run it. Read logs. Go back to the AI with concrete data, not impressions. *"I added a log before and after the query; in 47/500 requests the query took >5s. Hypothesis 3 (unindexed query) strengthens. Verify next?"*

**Step 5. Fix + regression test.** Once the root cause is identified, the AI writes the fix + a test that **fails without the fix**. That's the criterion: a test that wouldn't fail without the fix is useless.

### 3. Where AI shines in debugging

- **Assisted bisect**: "between commit A and B, what behavior changed?";
- **Comparison of two implementations**: "compare old foo and new foo, point out the behavioral difference";
- **Generating broad hypotheses**: fast, without confirmation bias (good counterpoint to human instinct);
- **Tailored instrumentation**: "add structured logging at the 3 critical points of this flow";
- **Reading long stack traces**: summarize, map to files, identify the relevant frame;
- **Proposing a regression test**: from the repro, write the test that fixes it;
- **Researching the error pattern**: "this error appears when X; check whether the code has pattern X".

### 4. Where AI gets in the way

- **Post-hoc rationalization**: after 10 exchanges, the AI "confirms" your hypotheses that are wrong. Be suspicious of easy agreement;
- **"Fix it" instinct**: the AI suggests speculative changes in 3 places when the bug is in 1. Ask for **diagnosis only**, not a fix, during investigation;
- **Bias toward the last file read**: the AI attributes the cause to whatever code is fresh in context;
- **Behavior hallucination**: "this function should do X" without verifying what it actually does. Demand a citation of real code;
- **Skipping contrary evidence**: if collected data contradicts a hypothesis, the AI sometimes minimizes it. Re-read evidence without the AI between steps.

### 5. Classic anti-pattern: "shotgun debugging"

Asking the AI to try 5 changes at once hoping one fixes it. Typical result: one fixes it but nobody knows which or why. The bug comes back in a different form.

**Rule:** one hypothesis at a time. One change at a time. One verification at a time.

### 6. When to stop and call a human

- 3 cycles without measurable progress;
- AI is giving circular answers;
- Hypotheses are exhausted (all tested, all false);
- The bug has a time correlation (only at a specific hour, typically infrastructure, not code);
- It involves concurrency, the network, or distributed state (see Part XIV).

Calling a human = stop and show the full state (repro, hypotheses tested, evidence). AI is part of the tooling, not a substitute for a human pair.

---

## Part XXI — Cost and Economics of AI
AI assistants have a real cost. At organizational scale, that bill matters: for adoption decisions, budget allocation, and choice of model tier.

### 1. Where the cost shows up

| Source | What it is | How it grows |
|---|---|---|
| **Input tokens** | Everything sent to the model: context, files read, tool output, history | Grows with long conversations, broad context, noisy tool calls |
| **Output tokens** | Everything the model generates: text, code, tool calls | Grows with long answers, rewrites, multiple iterations |
| **Model tier** | Price per million tokens varies 10–20x between low and high tiers | "High" agents cost much more than "medium" |
| **Latency → productivity** | Waiting 30s for a response 10x/hour = 5min/hour idle | High latency indirectly raises human cost |
| **Retries** | Iterations to fix bad output | Multiplier on everything above |
| **Storage / retention** | Some providers charge for long retention | Low, but not zero |

### 2. Model tiers per task (cost-aware)

A return to Part IV.3, now focused on cost:

| Tier | Relative cost | Use for |
|---|---|---|
| **High** | 10–20x medium | Critical security audits, architectural decisions, complex correlation |
| **Medium** | Baseline | Default for almost everything: code, review, planning, test generation |
| **Low** | 0.1–0.3x medium | Formatting, extraction, summarization, classification |

**Rule:** downgrade the model until quality drops. Upgrade only when measured necessary. "Always use the most expensive one to be safe" is waste.

### 3. Budgeting and attribution

At organizational scale, cost has to be:

- **Observable**: dashboard with consumption per squad/project/week;
- **Attributable**: who consumed? Skills? Agents? Long sessions?;
- **Budgeted**: monthly cap per squad or product;
- **Alertable**: notification when crossing 80% of the budget.

**Organizational patterns:**

- **Budget per squad**: each squad has a monthly quota; overflow requires justification;
- **Free tier for local dev + shared budget for automation**: CI and production agents counted separately;
- **Different models per environment**: dev can use the cheaper model; PR review in CI uses the good one;
- **Soft limits + conversation**: the first month is for learning; calibrate after.

### 4. When a model upgrade pays off

Upgrading from "medium" to "high" costs ~10–20x. It pays off if:

- Bad quality is costing **human rework** (2h of dev > the token premium);
- Output decisions have **real consequences** (security, architecture, compliance);
- The task is **rare** but important (quarterly audit);
- "Medium" models consistently fail on the team's benchmark.

**It does not pay off if:**

- The task is repetitive and high-volume (formatting, extraction);
- A human reviews the output anyway (review already filters quality);
- The quality gap is marginal (<10% measured improvement).

### 5. Patterns that reduce cost without losing quality

- **Context discipline** (Part III): fewer input tokens, more focused responses;
- **RPI with mixed models**: research in medium model; plan in high model; implement in medium;
- **Context caching**: some providers offer caching for repeated prompts (skills, context files). Enable when available;
- **Efficient tool calls**: grep with a filter instead of `cat` of the entire file;
- **Short-circuit**: the agent's first step is a cheap validation; expensive analysis only runs if it passes;
- **Batch when possible**: one agent reviewing 5 files in one go is cheaper than 5 sessions.

### 6. Hidden cost: compromised optionality

Beyond direct cost, there's a strategic cost: **lock-in**. If the entire harness depends on a specific provider:

- Migration to another provider is expensive (prompts re-calibrated, agents re-tested);
- Provider price increases are inelastic;
- Provider downtime stalls the team.

**Mitigations:**

- Prompts and skills should be written in agnostic markdown (not a proprietary format);
- Avoid provider-specific features when a standard alternative exists;
- Periodically test the harness on an alternative provider (even without migrating);
- Record the provider as a concentration risk in infrastructure risk registers.

### 7. ROI: how to justify the investment

For management, cost only makes sense compared to return. Useful measures:

- **Cycle time** (idea → PR merged): compare before/after;
- **Volume per dev** (PRs, lines reviewed, specs approved);
- **Quality** (bug recurrence, hotfixes, time in incident);
- **Team satisfaction** (internal NPS).

Beware of vanity metrics: lines of code generated by AI is not a useful indicator. Volume of **useful** work delivered is.

### 8. Cost control checklist

- [ ] Monthly budget per squad defined;
- [ ] Consumption dashboard up-to-date and monitored;
- [ ] Model tiers per task type documented;
- [ ] Context caching enabled where available;
- [ ] Prompts and skills avoid dependency on proprietary features;
- [ ] Quarterly review: cost vs. ROI;
- [ ] Plan B (alternative provider) tested periodically.

---

## Part XXII — Technical Documentation and AI
Documentation is one of the most immediately useful uses of AI: it generates fast, covers volume. It's also one of the most dangerous, because it produces confident material that drifts away from the code.

### 1. Where AI helps with documentation

- **Changelogs** from commits, turning technical history into a user voice;
- **Module/package READMEs**: structure, examples, API reference from existing code;
- **Docstrings**: filling functions and classes with description + types + examples;
- **Operational runbooks**: step-by-step for incidents, deploys, rollbacks;
- **Onboarding guides**: a digestible version of technical docs for new devs;
- **ASCII diagrams**: flows, architecture, sequences (fast and editable);
- **Translations**: EN ↔ PT ↔ ES preserving technical terms.

### 2. Where AI gets in the way

- **Docs drifting from code**: the AI writes "what it seems to do" based on name and signature, not what the function *actually does*. Read the code, confirm.
- **Made-up examples**: the AI generates snippets that don't run. Every code sample in a doc should be tested.
- **Performative verbosity**: the AI loves explanatory paragraphs. Good technical doc is short. Ask to cut 40%.
- **"Docs generated by AI" disclaimer**: it shifts responsibility. If it's in the repo, it's your doc. Own it.
- **Doc instead of clean code**: "the code is confusing, I'll write a doc explaining it" is an anti-pattern. Refactoring the code is almost always better than documenting the confusion.

### 3. Doc-as-code as a principle

Docs live **in the repository**, versioned like code, with the same PR/review cycle. Consequences:

- Code change + doc change **in the same PR** (gate: reviewer blocks a PR that changes behavior without updating the doc);
- Examples in docs run in CI (doctest, extracted scripts, snippet validation);
- Doc linter (formatting, broken links, valid frontmatter);
- Releases include release docs (changelog + migration guide; see Part VII).

### 4. Doc hierarchy

| Type | Audience | Cadence | Lives in |
|---|---|---|---|
| **Inline (docstring, comment)** | Dev reading the code | Alongside the code | Source code |
| **Module README** | Dev using the module | Per release | Module folder |
| **Architecture / design doc** | Team | Per decision | `docs/adr/` or `docs/design/` |
| **Runbook / operational** | On-call, SRE | Updated after incident | `docs/ops/` |
| **Onboarding / tutorial** | New dev | Quarterly | `docs/onboarding/` |
| **Changelog** | External user | Per release | `CHANGELOG.md` |
| **Migration guide** | User doing an upgrade | Per version | `migrations/` |

Each level has different rules. AI helps in all of them, but the constraints change.

### 5. Workflow: update doc when the code changes

A pattern that works:

1. Dev makes a code change;
2. Agent detects (via pre-commit hook or CI) that files with docstrings were modified;
3. Agent generates an update proposal for the affected doc;
4. Dev reviews, adjusts, commits along with the code.

The agent shouldn't commit directly. Doc is a human decision, like any distributed artifact (see Part VIII.1).

### 6. Specific anti-patterns

- **"Complete" doc on day 1, never updated afterward.** Better a short, living doc than a long, dead one.
- **Copy-paste of comments between similar functions.** Each function deserves a precise description of what *it* does.
- **A comment that paraphrases the code.** `// increments i by 1` for `i++` is noise. A comment should say *why*, not *what*.
- **Technical doc as marketing material.** Grand voice hides the details a dev needs. Be direct.

### 7. Doc-in-PR checklist

- [ ] Docstrings of modified public functions updated?
- [ ] Module README reflects visible changes?
- [ ] Changelog has an entry if the change affects users?
- [ ] Examples run (tested)?
- [ ] Internal links not broken?
- [ ] If the change is breaking: migration guide created?

---

## Appendix A — Glossary
| Term | Definition |
|---|---|
| **Agent / Sub-agent** | A sub-process of the AI dispatched on demand to analyze something and return a report. Typically read-only. |
| **Ambient authority** | The AI operates with all the permissions of the dev who invoked it. Bad by default; prefer confined. |
| **Backlog** | The canonical document of items pending, completed, discarded, and deferred. |
| **Changelog** | A record of changes written in the voice of the end user. |
| **Confined authority** | The AI operates in a sandbox with minimal, scoped permissions. Preferable. |
| **Context budget** | The available space in the AI's context window; finite, must be managed. |
| **Context file** | A file auto-loaded in each AI session with global conventions and a map of skills/docs. |
| **Context reset** | The practice of starting a new session with a clean context after an important milestone. |
| **Delta marker** | Annotation in a brownfield spec: `[ADDED]`, `[MODIFIED]`, `[REMOVED]`. |
| **DoD (Definition of Done)** | Objective criteria defining when a task is finished. Materialized in `verify.sh`. |
| **Dual-mode** | A skill that works across more than one medium (e.g., local files or external tool), with automatic detection. |
| **Phase (backlog)** | A thematic grouping; does not define order. |
| **Fast-path** | Simplified flow for trivial tasks (no spec, no plan, no gates). |
| **Fail-soft / Fail-fast** | An aggregator script keeps going after a failure to report everything (fail-soft); a single-action script stops at the first (fail-fast). |
| **Gate** | A mandatory human verification point between phases. |
| **Harness** | Infrastructure of context, skills, agents, verification, and memory that governs how an AI assistant operates on a project. |
| **Item-spec** | Detailed spec for a complex backlog item, with plan, context, and criteria. |
| **Migration guide** | A self-contained document that lets a user manually apply the changes between two versions. |
| **`[P]` (task marker)** | Indicates a parallelizable task; can run concurrently with other `[P]` tasks in the same wave. |
| **Execution plan** | Breakdown of a spec into ordered tasks, with dependencies and parallelization points. |
| **Prompt injection** | An attack where external input contains instructions the AI could improperly follow. |
| **RPI (Research, Plan, Implement)** | A pattern of three isolated sessions for large tasks. |
| **Skill / Playbook** | A markdown document with a checklist and patterns for a specific domain ("how we do X here"). |
| **Spec** | Formal document defining what will be done, why, and acceptance criteria. |
| **STATE.md** | Continuity file across sessions: current status, next actions, blockers. |
| **Trust boundary** | The boundary where responsibility for state transitions (AI → dev, dev → reviewer, etc.). |
| **Wave (backlog)** | Execution priority order, independent of phase. |
| **Worktree isolation** | Use of `git worktree` to run sub-agents on an isolated branch, avoiding contaminating the shared working directory. |

---

## Appendix B — Compiled Checklists
### B.1. Starting a non-trivial task

- [ ] Item exists in the backlog? If not, add it before starting.
- [ ] Spec exists and was approved (for medium+)?
- [ ] Execution plan exists (for medium+)?
- [ ] Previous STATE was read (if continuation)?
- [ ] Item dependencies are completed?
- [ ] Relevant skills were consulted?

### B.2. Finishing a task

- [ ] Source and distributed in sync (if applicable);
- [ ] Manifest updated;
- [ ] Setup and update covered (if applicable);
- [ ] Dual-mode covered (if applicable);
- [ ] Docs updated (skills map, workflow, main context);
- [ ] Tests pass (`verify.sh`);
- [ ] Linter clean;
- [ ] Acceptance criteria verified;
- [ ] STATE.md updated (if continuation);
- [ ] Item moved to "Done" in the backlog.

### B.3. Creating a new agent

- [ ] Complete frontmatter (`description`, `model`, `worktree`, `model-rationale`);
- [ ] Required sections: When to use, Input, What to check, Output, Rules;
- [ ] Standard severities in the output (🔴🟠🟡⚪);
- [ ] "Next steps" section linking to related skills;
- [ ] Manifest entry;
- [ ] Reference in the main context's agents map.

### B.4. Creating a new skill

- [ ] Required sections: When to use, When NOT to use, Checklist, Patterns, When to escalate;
- [ ] At least one concrete example per section (not just placeholders);
- [ ] Dependencies declared at the top (if it depends on another skill);
- [ ] Manifest entry;
- [ ] Reference in the main context's skills map.

### B.5. Opening a PR

- [ ] Dedicated branch (never commit directly to main);
- [ ] Sub-agents that edited ran in an isolated worktree;
- [ ] Atomic commits (one reason per commit);
- [ ] Commits follow Conventional Commits;
- [ ] Local validations passed (`verify.sh`);
- [ ] PR description describes the what and why, links the spec;
- [ ] Acceptance criteria marked as validated;
- [ ] Security checklist (B.7) passed;
- [ ] CI green before merge.

### B.6. Releasing

**Pre-release:**
- [ ] Working directory clean;
- [ ] Source ↔ distributed in sync;
- [ ] Manifest updated;
- [ ] Changelog updated (only changes that reach the user);
- [ ] Version tags consistent;
- [ ] Tests and validations pass.

**Post-release:**
- [ ] Version file updated;
- [ ] Plugin/package manifests at the same version;
- [ ] Changelog has an entry;
- [ ] Migration guide created;
- [ ] Tag created in git;
- [ ] Backlog: "pending release" → real version;
- [ ] Test in a real environment post-publication.

### B.7. Per-PR security checklist

- [ ] No hardcoded secrets (scanner passed);
- [ ] No queries built with string concatenation (SQL injection);
- [ ] User input validated and sanitized;
- [ ] HTML/JSX output escaped (XSS);
- [ ] File paths validated against traversal (`..`);
- [ ] Authentication and authorization on new endpoints;
- [ ] New dependencies audited;
- [ ] Logs don't record sensitive data (password, token, PII).

### B.8. Auditing code or documentation

- [ ] Read recorded anti-patterns before starting;
- [ ] For each finding: applied the "second file" test?;
- [ ] Findings classified with standard severity;
- [ ] New false positives recorded in anti-patterns;
- [ ] Next steps indicate the skill or agent for the fix.

### B.9. Closing a long session

- [ ] STATE.md updated with: status, next action, blockers;
- [ ] Atomic commits made (don't leave orphan changes);
- [ ] Discoveries deserving their own spec were recorded in the backlog;
- [ ] Discarded decisions were recorded with reason.

### B.10. Quarterly harness review

- [ ] Review health indicators (Part XVII): any worsening?;
- [ ] Qualitative survey with the team: recurring theme?;
- [ ] Skills unused in 6+ months: archive or consolidate?;
- [ ] Skills with high overlap: merge?;
- [ ] Main context > 600 lines? Prune;
- [ ] Orphan docs: link or remove;
- [ ] Resolved anti-patterns: move to history;
- [ ] Harness backlog prioritized for the next quarter.

---

## Appendix C — Reference Templates
Boilerplate ready to copy/paste and adapt. Each template is a starting point: adapt it to context, don't copy blindly.

### C.1. Skill template

````markdown
# {Skill name}

## When to use
- {Context 1}
- {Context 2}

## When NOT to use
- {When another skill fits better}

## Checklist
- [ ] {Check 1}
- [ ] {Check 2}
- [ ] {Check 3}

## Patterns

### Concrete example
✅ **Right:**
```{language}
// code that exemplifies the good practice
```

❌ **Wrong:**
```{language}
// code that exemplifies what to avoid
```

## When to escalate
- If {critical condition} → call {skill/agent/human}
````

### C.2. Agent template

````markdown
---
description: {one sentence about what the agent does}
model: {high | medium | low}
worktree: false
model-rationale: {one sentence justifying the model choice}
---

# {Agent name}

## When to use
{Contexts in which to invoke it}

## Input
{What the agent receives: scope, parameters, format}

## What to check
1. {Check 1}
2. {Check 2}
3. {Check 3}

## Output
Report format:

### Status: PASS | FAIL | PARTIAL

### Findings

#### 🔴 Critical
- {finding}

#### 🟠 High
- {finding}

#### 🟡 Medium
- {finding}

#### ⚪ Info
- {finding}

### Next steps
- To fix: use skill `{name}` or agent `{name}`

## Rules
- {Constraint 1}
- {Constraint 2}
````

### C.3. Spec template

````markdown
# Spec {ID}: {Title}

**Status:** draft

## Context
{Why this spec exists, what problem it solves — 3-5 sentences.}

## Dependencies
- {Spec or component this depends on}

## Functional requirements
- FR-001: {verifiable requirement}
- FR-002: {verifiable requirement}

## Scope
- [ ] {Deliverable 1}
- [ ] {Deliverable 2}

## Acceptance criteria
- Given {precondition}, when {action}, then {observable result}
- {Criterion 2}

## Affected files
- `path/file1.ext`: {modify | create | remove}
- `path/file2.ext`: {modify | create | remove}

## Out of scope
- {Out of scope 1}

## Skills to consult
- {skill1}

## Post-implementation verification
- [ ] Tests pass (verify.sh)
- [ ] Acceptance criteria validated
- [ ] Docs updated if necessary
````

### C.4. Execution plan template

````markdown
# Plan: Spec {ID}

**Spec:** [{ID}](../specs/{ID}.md)
**Total estimate:** {hours/days}

## Prerequisites
- [ ] Spec approved
- [ ] Dependencies completed

## Tasks

### Wave 1
- [ ] T1: {description} — `{files}` — {estimate}
- [ ] T2 [P]: {description} — `{files}` — {estimate}

### Wave 2 (depends on Wave 1)
- [ ] T3: {description} — depends on T1
- [ ] T4 [P]: {description} — depends on T1

### Wave 3 (verification)
- [ ] T5: run verify.sh
- [ ] T6: update affected docs

## Risks and mitigations
- {Risk}: {mitigation}

## Gates
- After Wave 1: human review before continuing
- After Wave 2: code review on the PR
````

### C.5. STATE.md template

````markdown
# STATE — {spec-id or task-id}

**Updated:** {YYYY-MM-DD HH:MM}

## Status
{1-2 sentences about where I am}

## Context loaded
- Spec: `{path}`
- Plan: `{path}`
- Relevant docs: `{path}`

## What was done
- T1: {description} ✅ (commit {sha})
- T2: {description} ✅ (commit {sha})

## What's left
- T3: {description} (in progress)
- T4: {description}

## Next action
{Concrete instruction to resume, with file:line reference if applicable}

## Blockers / pending decisions
- {Open question + context + who needs to answer}

## Notes
- {Useful context discovered for resuming}
````

### C.6. Migration guide template

````markdown
# Migration: v{FROM} → v{TO}

**Summary:** {1-3 sentences about what changed and why}

**Prerequisites:**
- Be on version v{FROM}
- Have applied previous migrations

---

## Replaced files (overwrite)

### `{path}`
**What changed:** {summary}
**How to apply:** replace the file with the new one.
**Impact:** {none | behavior X differs}

---

## Structural changes (structural)

### `{path}`
**Sections added:** `## New Section A`, `## New Section B`
**Sections removed:** `## Old Section`
**Impact:** {description}

---

## Content patches (manual)

### `{path}` — section `## X`
**Reason:** {why it changed}
**Old text:**
> {snippet}

**New text:**
> {full snippet}

**Impact:** {description}

---

## Manual decisions (manual)

### `{path}`
**Diff:**
```diff
- old line
+ new line
```
**Suggestion:** {what the user should consider before applying}

---

## New files

### `{path}`
**Purpose:** {what it is}
**When relevant:** {contexts}

---

## Removed files

### `{path}`
**Reason:** {why it left}
**Replacement:** `{new path or "none"}`
````

### C.7. Changelog entry template

````markdown
## [vX.Y.Z] — YYYY-MM-DD

### Added
- {User-visible feature} (#PR)

### Changed
- {Visible behavior change} (#PR)

### Fixed
- {Bug fix that affected users} (#PR)

### Removed
- {Removed feature + replacement if any} (#PR)

### Security
- {Vulnerability fix} (#PR)

### Migration
See [migrations/v{PREVIOUS}-to-v{NEW}.md](migrations/v{PREVIOUS}-to-v{NEW}.md).
````

### C.8. Prompt template (minimum anatomy)

```
Context: {where I am, what the project is — 1-2 sentences}

Goal: {what I want, verifiable — 1 sentence}

Constraints:
- {what NOT to do}
- {other constraints}

Expected format: {response structure}
```

---

*This handbook is a distillation of practices. Adapt it to your context: principles matter more than literal rules.*
