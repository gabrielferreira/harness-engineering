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
