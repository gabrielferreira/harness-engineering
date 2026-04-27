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
