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
