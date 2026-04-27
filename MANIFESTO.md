**English** · [Português](MANIFESTO.pt.md)

---

# Harness Engineering Manifesto

AI coding assistants deliver what you ask for. The problem is rarely the model. It is the absence of infrastructure that tells it where it stands, what the team values, and how the work is judged.

**Harness is that infrastructure.** This document declares how we think about it.

---

## What we value

We see value on both sides, but when tension arises we prefer the first.

- **Explicit context** over implicit intuition.
- **Persisted files** over ephemeral conversations.
- **Human review between phases** over unrestricted autonomy.
- **Automated verification** over merely written convention.
- **Concrete simplicity** over premature abstraction.
- **Shared guidelines** over individual preferences.
- **Proportional ceremony** over uniform process.
- **Declared compatibility** over accidental compatibility.

---

## Principles

### 1. AI is a collaborator, not an oracle

We treat the assistant as a new colleague: fast, but in need of onboarding, conventions, review, and limits. Not as an intelligence that gets things right by magic.

### 2. Harness is infrastructure, not optimization

It is not a tweak for 10% more speed. It is the layer that determines whether AI helps or hinders. Without harness, apparent productivity becomes silent debt.

### 3. Context has cost: we reference instead of inlining

More context is not better context. Global rules go into automatic onboarding; depth is loaded on demand. Less noise, more signal.

### 4. Every important decision becomes a versioned file

Conversations vanish. Commits, specs, plans, and migrations survive session refreshes, team changes, and tool migrations.

### 5. Explicit gates guard against silent drift

Humans approve critical transitions: spec → plan, plan → code, code → merge. Automation handles the repetitive; judgement is human.

### 6. Skills inform, agents verify, humans judge

Skills are checklists before acting. Agents are read-only auditors after acting. Merge is always a human decision.

### 7. Ceremony is proportional to complexity, never uniform

A typo needs no spec. A large feature without a spec doesn't start. Heavy process on light work is as bad as no process on heavy work.

### 8. Recording what was discarded matters as much as what was done

Discarded decisions, deferred ideas, and recorded anti-patterns prevent the organization from re-running the same debate. Institutional memory is an asset.

### 9. No rule survives without automated verification

A convention that isn't a check in `verify.sh` is a convention that will be violated. If it matters, it must fail the build when broken.

### 10. Three concrete cases before abstracting

Explicit repetition beats wrong abstraction. Undoing an abstraction costs more than cleaning up copy-paste.

### 11. Compatibility is an explicit choice, not an accident

Every distributed artifact declares how it evolves: additive, migratable, or breaking. Old projects keep working until migration is offered. They are never sabotaged.

### 12. Security is part of the design, not an afterthought

Allowlists for paths and commands, external inputs as data (not instructions), pre-commit hooks, mandatory code review before merge. AI is an external collaborator: it gets only what it needs.

### 13. Simplicity is the rule; complexity must justify itself

Markdown before database. Script before framework. File before SaaS. If the repo compiles, the harness works.

### 14. Harness is living software: it rots without pruning

Unused skills, rules nobody follows, orphaned docs: we review and remove. Keeping the essential beats hoarding the complete.

### 15. Measure before opining on whether it works

Recurrence, rework, coverage, time-to-first-gate. Without metrics, *"the harness is fine"* is feeling. With metrics, it is work.

### 16. What AI cannot do well, we delegate to humans

Subtle debug, novel architectural decisions, critical incidents, regulated code without a spec. A mature harness knows AI's limits and respects them.

---

## Commitments

Whoever adopts this manifesto commits to:

- **Reading the context** before asking the AI;
- **Writing a spec** before coding anything non-trivial;
- **Recording what was discarded** alongside what was done;
- **Turning every important rule into an executable check**;
- **Reviewing, pruning, and evolving the harness continuously**;
- **Onboarding people**, not just tools.

---

*Adapt it to your context. Principles outweigh literal rules.*
