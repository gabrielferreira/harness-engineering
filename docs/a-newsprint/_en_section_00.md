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
