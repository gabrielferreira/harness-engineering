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
