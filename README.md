**English** · [Português](README.pt.md)

---

# Harness Engineering: Handbook

> How engineering teams and technology organizations can use **AI coding assistants** (Claude Code, Cursor, GitHub Copilot, Continue, Aider, Windsurf, Cline) on real projects at scale. Not as fancy autocomplete, but as part of the development process.

> *Harness engineering: the discipline of configuring the context, rules, skills, and verification tooling an AI coding assistant needs to operate well in a real project.*

## Where to start

Two complementary documents, from shortest to most extensive:

- **[Manifesto](./MANIFESTO.md)**: a single page with the distilled principles (16 principles + 6 commitments). Start here if you want to grasp the philosophy before diving in.
- **[Handbook](./HANDBOOK.md)**: the full guide (22 parts + 3 appendices) with detailed practices, examples, templates, and checklists.

## What harness engineering is

**Harness engineering** is the discipline of configuring the instructions, constraints, and tools an AI coding assistant needs to operate with quality in a real project. It is what stops the AI from inventing APIs, ignoring team conventions, producing code that passes lint but breaks business rules, or causing silent debt.

A mature harness organizes the assistant's intelligence into six complementary layers:

1. **Knowledge**: specs, backlog, project context;
2. **Expertise**: domain checklists (skills);
3. **Automation**: read-only sub-agents on demand (agents);
4. **Orchestration**: phase sequencing, context budget, isolated sessions;
5. **Verification**: executable scripts, definition of done;
6. **Continuity**: persistent context files, state across sessions.

**Tool-agnostic:** the principles apply to any AI coding assistant — Claude Code, Cursor, GitHub Copilot, Continue, Aider, Windsurf, Cline, or combinations.

## Related topics the handbook connects

Content often treated separately, gathered here into a single conceptual map:

- **AI coding assistant best practices**: what, when, and how to use them;
- **Context engineering**: how to build the right context for an LLM;
- **Prompt engineering for code**: anatomy of useful prompts, by intent;
- **Spec-driven development**: the idea → backlog → spec → plan → code flow;
- **Agentic coding**: using sub-agents, orchestrating phases (Research → Plan → Implement);
- **AI governance in engineering**: ownership, security, compliance, cost, ROI;
- **Onboarding and adoption**: an incremental roadmap from zero to mature.

## What the handbook covers

- **Foundations**: the six harness layers, design principles, minimal vocabulary;
- **Context engineering**: context hierarchy, on-demand imports, portable context;
- **Orchestration**: context budget, isolated sessions (RPI: Research/Plan/Implement), cross-session continuity (the STATE.md pattern);
- **Skills and agents**: domain playbooks vs. read-only sub-agents, model choice;
- **Spec-driven development**: proportional ceremony, gates, fast-path, TDD, test strategy;
- **Backlog as single source of truth**: taxonomy, Phase vs. Wave, the no-delete rule;
- **Versioning and releases**: Conventional Commits, atomic commits, migrations;
- **Distribution and compatibility**: merge strategies (overwrite/structural/manual/skip), version tags, 3 mandatory scenarios;
- **Dual-mode**: artifacts in the repo and in an external tool (Notion, Linear, Jira) with automatic detection;
- **Quality, verification, and audits**: task checklist, executable DoD, the "second file" test, code review of AI-generated code;
- **Security in AI harnesses**: prompt injection, ambient vs. confined authority, IP and licenses, compliance (GDPR, LGPD, HIPAA, PCI);
- **Cross-cutting principles**: simplicity, human review, explicit trust boundaries;
- **Developer anti-patterns when using AI**: common errors that come from the dev, not the model;
- **When NOT to use AI**: explicit limits;
- **Governance and evolution**: ownership, pruning, migration between model versions;
- **Adoption and onboarding**: maturity tiers, when NOT to adopt a harness, how team roles change (junior, mid, senior, tech lead);
- **Health metrics**: quantitative and qualitative indicators;
- **Anatomy of a good prompt**: three intents, minimum structure, constructive mistakes;
- **Debug workflow with AI**: 5-step flow, where AI shines, where it gets in the way;
- **Cost and economics**: model tiers per task, budgeting, ROI, lock-in;
- **Technical documentation and AI**: doc-as-code, doc hierarchy, anti-patterns.

Each section stands on its own. Read it linearly once for the mental map, then consult specific sections as needed.

## Who it is for

- Senior engineers and architects;
- Tech leads standardizing AI use across squads;
- Engineering managers calibrating expectations, quality, and velocity;
- Platform engineering teams offering AI as an internal product;
- CTOs and VPs of Engineering setting org-wide direction.

## Read in another language

The repo keeps per-language files at the root for clean GitHub reading:

- **English** (this file): [Manifesto](./MANIFESTO.md) · [Handbook](./HANDBOOK.md)
- **[Português](./README.pt.md)**: [Manifesto](./MANIFESTO.pt.md) · [Handbook](./HANDBOOK.pt.md)

The site under `docs/a-newsprint/` keeps a single bilingual `HANDBOOK.md` filtered at runtime by JS; the root `HANDBOOK.md` and `HANDBOOK.pt.md` are regenerated from it with `scripts/sync-handbook.sh`.

## License

This handbook is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You can share and adapt freely, as long as you give appropriate credit.

See [LICENSE](./LICENSE) for details.

## Contributions

Suggestions, corrections, and field experiences are welcome via issue or pull request. The handbook is a distillation of practices and evolves with real use.
