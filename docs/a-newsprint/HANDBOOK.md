<!--PT-->
# Handbook de Harness Engineering

> Um guia prático para times de engenharia, tecnologia e organizações que querem usar AI coding assistants em projetos reais e em escala, não como autocomplete sofisticado, mas como parte do processo de desenvolvimento.
<!--/PT-->
<!--EN-->
# Harness Engineering Handbook

> A practical guide for engineering teams, technology orgs, and companies that want to use AI coding assistants in real projects at scale — not as fancy autocomplete, but as part of the development process.
<!--/EN-->

---

<!--PT-->
## Sumário
<!--/PT-->
<!--EN-->
## Contents
<!--/EN-->

- [Introdução](#introdução)
- [Parte I — Fundamentos](#parte-i--fundamentos)
- [Parte II — Context Engineering](#parte-ii--context-engineering)
- [Parte III — Orquestração: Budget, Sessões e Continuidade](#parte-iii--orquestração-budget-sessões-e-continuidade)
- [Parte IV — Skills e Agents](#parte-iv--skills-e-agents)
- [Parte V — Spec-driven Development](#parte-v--spec-driven-development)

---

<!--PT-->
## Introdução

### O problema

AI coding assistants são produtivos em tarefas pequenas e superficiais. Em projetos reais, eles frequentemente:

- Inventam APIs que não existem no código;
- Repetem padrões obsoletos que o time já abandonou;
- Desrespeitam convenções arquiteturais não escritas;
- Geram código que passa no lint mas quebra regra de negócio;
- Não sabem onde parar: resolvem o pedido literal e ignoram a consequência sistêmica.

O culpado não é o modelo. É a **ausência de harness**: a infraestrutura de contexto, regras, especialização e verificação que informa o AI sobre onde ele está, o que o time valoriza e como o trabalho é avaliado.

### O que é harness engineering

**Harness engineering é a disciplina de configurar as instruções, restrições e ferramentas que um AI coding assistant precisa para operar com qualidade num projeto real.**

É tratar o AI assistant como um colaborador novo que precisa de onboarding, padrões, code review e gates, não como um oráculo que acerta por intuição. Um harness bem construído:

- Diz **quem é o projeto** (stack, domínio, restrições);
- Diz **como o time trabalha** (convenções, testes, segurança);
- Diz **o que verificar** antes, durante e depois de cada mudança;
- Diz **onde parar** (escopo, gates, revisão humana);
- **Persiste memória** entre sessões para que contexto não se perca.

### Quem deve ler

- **Engenheiros seniores e arquitetos** que introduzem AI assistants nos seus times e precisam mantê-los dentro dos guardrails;
- **Tech leads** que querem padronizar o uso de AI entre squads;
- **Managers de engenharia** que precisam calibrar expectativa, qualidade e velocidade;
- **Platform engineering** que oferece AI como produto interno para outras áreas;
- **Pessoas de CTO/VP Engineering** decidindo diretrizes organizacionais.

### Como ler

O handbook é denso por design: cada seção é independente. Leia linearmente uma vez para ter o mapa mental; depois consulte por seção quando aparecer o problema específico.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte I — Fundamentos
<!--/PT-->
<!--EN-->
## Part I — Foundations
<!--/EN-->
<!--PT-->
### 1. As seis camadas do harness

Um harness maduro organiza a inteligência do assistant em seis camadas complementares. Remover uma delas não quebra tudo, mas degrada a qualidade de forma insidiosa.

| Camada | O que é | Pergunta que responde |
|---|---|---|
| **1. Conhecimento** | Specs, backlog, contexto do projeto | *O que este projeto faz e por quê?* |
| **2. Expertise** | Checklists por domínio (skills) | *Como eu devo fazer X neste projeto?* |
| **3. Automação** | Sub-agentes read-only sob demanda | *Está tudo certo? Tem algo quebrado?* |
| **4. Orquestração** | Sequenciamento de fases, budget de contexto, sessões isoladas | *Em que ordem faço, e onde o contexto reseta?* |
| **5. Verificação** | Scripts executáveis, definition of done | *Isso está realmente pronto?* |
| **6. Continuidade** | Arquivos de contexto persistentes, estado entre sessões | *Onde eu parei da última vez?* |

**Princípio fundamental:** cada camada existe porque a anterior não é suficiente. Conhecimento sem expertise vira código genérico. Expertise sem automação vira checklist ignorada. Automação sem orquestração vira ruído. E assim por diante.

### 2. Princípios de design do harness

Quatro princípios orientam tudo que vem a seguir:

**Markdown-first.** O harness vive como arquivos de texto no repositório, versionados junto com o código. Nenhuma ferramenta proprietária, nenhum SaaS, nenhum banco de dados central. Se o repo compila, o harness funciona.

**Sob demanda, não sempre.** Contexto tem custo. Regras globais entram no onboarding automático; regras específicas são carregadas só quando o tópico aparece. Mais contexto ≠ melhor resultado.

**Revisão humana entre fases.** O AI propõe; humanos aprovam transições críticas (spec → plano, plano → código, código → merge). Gates explícitos impedem deriva silenciosa.

**Persistir no disco, não na conversa.** Toda decisão importante vira arquivo. Conversa é efêmera; commits, specs e planos sobrevivem à sessão.

### 3. Vocabulário mínimo

Antes de seguir, fixe estes termos (eles aparecem ao longo do handbook).

- **Harness:** a infraestrutura inteira (contexto + skills + agents + verificação).
- **Context file:** arquivo carregado automaticamente no início de cada sessão com o AI.
- **Skill / Playbook:** checklist de domínio ("como fazer X") consultado pelo AI ou pelo humano.
- **Agent / Sub-agent:** sub-processo do AI, tipicamente read-only, despachado para analisar algo específico e reportar.
- **Spec:** documento que define o que vai ser feito, por quê e como validar.
- **Plano de execução:** quebra de uma spec em tasks ordenadas.
- **Gate:** ponto de verificação humana obrigatório entre fases.
- **Context budget:** espaço disponível na janela de contexto do AI; finito, precisa ser gerenciado.
- **Sessão:** uma conversa única com o AI, com contexto começando "limpo".
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte II — Context Engineering
<!--/PT-->
<!--EN-->
## Part II — Context Engineering
<!--/EN-->

<!--PT-->
### 1. O arquivo de contexto principal

Todo projeto deve ter um arquivo de contexto carregado automaticamente pelo AI assistant em toda sessão. Esse arquivo é o **cérebro do projeto**: o que o assistant precisa saber antes de tocar qualquer linha.

Conteúdo típico:

1. **Identidade do projeto:** o que é, para quem, qual o estado (produção, beta, greenfield);
2. **Stack técnica resumida:** linguagem, frameworks, banco, testes, deploy;
3. **Convenções globais:** como nomear, como testar, como commitar, como fazer PR;
4. **Fluxo de trabalho:** onde ficam specs, como o backlog funciona, quando pedir revisão;
5. **Mapa de skills e docs:** links para conteúdo sob demanda (não inline);
6. **Restrições não-negociáveis:** segurança, compliance, dados sensíveis.

**Métrica para decidir o que entra:** *se eu remover esta linha, o AI vai cometer o mesmo erro que já cometeu antes?* Se sim, entra. Se é informação que ele pode inferir do código, fica de fora.

### 2. Hierarquia por profundidade

Em projetos pequenos, um único arquivo de contexto basta. Em monorepos ou sistemas grandes, o contexto vira hierárquico:

| Nível | Onde vive | Conteúdo típico | Tamanho |
|---|---|---|---|
| **L0** | Raiz do repo | Convenções globais, fluxo de specs/backlog, segurança, mapa de skills | 200-400 linhas |
| **L1** | Domínio (ex: `apps/`, `services/`) | Regras compartilhadas do domínio | 50-150 linhas |
| **L2** | Módulo (ex: `apps/api/`) | Stack local, comandos, coverage, regras específicas | 100-300 linhas |
| **L3+** | Feature (raro) | Edge cases, integrações de terceiros | 30-80 linhas |

**Regra de carregamento:** concatenação, não override. Raiz primeiro, subpasta depois. Zero redundância: se algo vale para todo o monorepo, fica em L0; se só vale para a API, fica em L2.

### 3. Import sob demanda

O contexto principal referencia conteúdo externo em vez de inliná-lo:

- Skills pelo caminho do arquivo;
- Docs técnicas por caminho;
- Specs por ID.

Assim o contexto principal fica enxuto (200-400 linhas) e o AI puxa profundidade só quando a conversa exigir. Isso é diferente de *ter* a informação (ela existe, mas não ocupa context budget por padrão).

### 4. Contexto portátil

Um segundo arquivo de contexto, **agnóstico a qual AI está rodando**, deve existir para uso com outras ferramentas (modelos web, outros assistants, futuras integrações). Enquanto o arquivo principal fala com as convenções do AI específico do time (skills, agents, slash commands), o portátil descreve:

- Stack técnica completa;
- Estrutura do repositório;
- Decisões arquiteturais;
- Regras de negócio não óbvias;
- Regras de segurança.

Assim, qualquer LLM que receber esse arquivo consegue operar com o mesmo contexto base. É a versão "documento" do harness: lê-se de cima a baixo, sem ferramental.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte III — Orquestração: Budget, Sessões e Continuidade
<!--/PT-->
<!--EN-->
## Part III — Orchestration: Budget, Sessions, and Continuity
<!--/EN-->

<!--PT-->
Context é recurso finito. A arte é escolher o que ocupa espaço agora, o que é referenciado, e o que sobrevive entre sessões.

### 1. Context budget como restrição de design

Toda janela de contexto (200k, 1M tokens, não importa) eventualmente satura. Antes disso, a qualidade do output já **começa a cair**: o AI ignora instruções antigas, contradiz decisões recentes, inventa quando poderia olhar.

**Três pressões competem:**

- **Carregar contexto** (para acertar): lê código, docs, conversas anteriores;
- **Pensar** (para decidir): cadeia de raciocínio, hipóteses, verificação;
- **Produzir** (para agir): edições, testes, relatórios.

Quando uma domina, as outras sofrem. Um assistant que **só** lê código não pensa. Um que **só** pensa vira verborrágico. Um que **só** produz comete erros bobos.

**Regra de ouro:** *quanto mais ambicioso o trabalho, mais importante é manter o contexto enxuto por fase*. Não enfiar toda a documentação da empresa no contexto "pra garantir".

### 2. Práticas de orçamento

- **Referenciar, não inlinar.** Skills, docs, specs entram como caminho; o AI lê quando precisar.
- **Resumir antes de prolongar.** Em conversas longas, pedir um sumário intermediário e começar nova sessão a partir dele.
- **Isolar fases ruidosas.** Research (que explora amplamente) não deve dividir contexto com implementação (que precisa foco).
- **Podar outputs longos.** Saída de tool call de 5000 linhas quase sempre precisa de filtro: grep, head, tail, limit.
- **Medir.** Se a plataforma expõe token count, olhar periodicamente.

### 3. Sessões isoladas por fase (RPI)

Para tarefas grandes, uma única sessão é péssima ideia. Três sessões separadas (**R**esearch, **P**lan, **I**mplement) quase sempre ganham.

| Fase | Sessão dedicada faz | Entrega persistida |
|---|---|---|
| **Research** | Explora código, lê docs, levanta hipóteses, sem escrever produção | `research.md` com achados |
| **Plan** | Lê a research e produz plano ordenado, decisões arquiteturais | Spec + plano de execução |
| **Implement** | Lê o plano aprovado e executa task a task | Commits + testes |

**Por que isolar:**

1. Research polui o contexto com tentativas abandonadas; implementação não precisa desse ruído.
2. O modelo "se agarra" a decisões tomadas em fases anteriores mesmo quando a evidência muda. Reset cognitivo ajuda.
3. Custo: cada fase paga seu próprio briefing, mas economiza em retrabalho.

**Quando não separar:** tarefas médias ou triviais. RPI tem overhead, só compensa em escopo grande/complexo.

### 4. Context reset explícito

Quando uma fase grande termina (feature entregue, refactor fechado), marcar **reset**: nova sessão, apenas com o context file principal + referência ao artefato recém-produzido. O AI não precisa "lembrar" das 200 trocas anteriores; elas viraram código, PR, changelog.

**Sinal de que o reset está atrasado:**

- O AI começa a confundir o estado atual com um estado anterior;
- Pede confirmação de coisas já decididas;
- Sugere refazer algo já feito.

### 5. Paralelização controlada de sub-agentes

Sub-agentes read-only podem rodar em paralelo no mesmo escopo (ex: três auditores olhando segurança, testes e documentação em paralelo). Para agentes que **escrevem código**, paralelizar exige:

- **Worktrees isoladas.** Cada agent opera em `git worktree` separado, com zero risco de sobrescrita.
- **Tasks em arquivos disjuntos.** Se dois agents tocam o mesmo arquivo, serialize.
- **Gate de merge.** Depois que todos terminam, um humano (ou um agente revisor) consolida.

Marcar no plano de execução com `[P]` as tasks que podem rodar em paralelo:

```markdown
## Plano de execução

- [ ] T1: criar modelo User (src/models/user.ts)
- [ ] T2 [P]: criar migration inicial (db/migrations/)
- [ ] T3 [P]: adicionar fixtures de teste (tests/fixtures/)
- [ ] T4: implementar login (depende de T1)
```

T2 e T3 são paralelizáveis; T4 depende de T1. Gate entre waves.

### 6. Continuidade entre sessões: o padrão STATE

Tarefas grandes inevitavelmente ultrapassam uma única sessão. Para não perder contexto, mantenha um arquivo **STATE** atualizado.

**Estrutura mínima:**

```markdown
# STATE — {spec-id ou task-id}

**Atualizado:** 2026-04-16 17:30

## Status
Em andamento — task T3 concluída, iniciando T4.

## Contexto carregado
- Spec: `.specs/FEAT-12.md`
- Plano: `.specs/FEAT-12-plan.md`
- Research: `.specs/FEAT-12-research.md`

## O que foi feito
- T1: modelo User ✅ (commit abc123)
- T2: migration ✅ (commit def456)
- T3: fixtures ✅ (commit ghi789)

## O que falta
- T4: endpoint de login (em andamento)
- T5: testes de integração
- T6: documentação

## Próxima ação
Implementar validação de senha no `login.controller.ts` — spec linha 42.

## Blockers / decisões pendentes
- Hash com bcrypt vs argon2 (linha 87 da spec não decidiu) — perguntar no PR.

## Notas
- Usar `user.repository.ts` existente (já tem `findByEmail`).
- Não tocar no fluxo de refresh token — fora do escopo.
```

**Disciplina de uso:**

- **Atualizar antes de encerrar sessão** (última ação do AI, ou checkpoint manual);
- **Ler no início da próxima** (primeira ação, antes de qualquer pensamento novo);
- **Persistir no repo** em branch de trabalho (commitado ou não, decisão do time).

O STATE é a memória do projeto entre amnésias. Sem ele, cada nova sessão começa do zero e o AI reinventa decisões.

### 7. Briefing auto-contido para sub-agentes

Sub-agentes começam com contexto zero. O prompt para um sub-agente precisa ser **auto-contido**:

- O que você quer;
- Por quê (brevemente, porque decisões mudam quando a razão muda);
- O que já foi tentado ou descartado;
- Restrições (não editar X, não ler Y);
- Formato da resposta esperada.

Prompt vago para sub-agente = relatório genérico. Bom briefing = boa resposta.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte IV — Skills e Agents
<!--/PT-->
<!--EN-->
## Part IV — Skills and Agents
<!--/EN-->

<!--PT-->
Skills e agents são as duas formas principais do AI aplicar especialização. Confundi-los é um erro comum.

### 1. Skills: checklists por domínio

Uma **skill** é um documento markdown que responde: *"quando vou fazer X neste projeto, o que devo verificar?"*. Ela não executa; ela **informa**. É lida pelo AI (e pelo humano) no momento em que o tópico aparece.

**Formato canônico de skill:**

```markdown
# {Nome da skill}

## Quando usar
- Ao implementar X
- Ao modificar Y

## Quando NÃO usar
- Quando for apenas Z (use outra skill)

## Checklist
- [ ] Verificar A
- [ ] Validar B
- [ ] Rodar C

## Padrões
✅ Correto: exemplo concreto
❌ Errado: anti-exemplo concreto

## Quando escalar
- Se encontrar {condição}, acionar {outra skill / humano}
```

**Skills típicas de um harness maduro:**

- Core: spec-driven, definition-of-done, testing, code-quality, security-review
- Domínio: ux-review, dba-review, accessibility, observability
- Orquestração: research, execution-plan, context-reset

**Regra crítica:** toda skill precisa ter **exemplos concretos**, não apenas placeholders genéricos. Um exemplo real é 10x mais útil que três bullets abstratos.

### 2. Agents: auditores read-only autônomos

Um **agent** é um sub-processo do AI invocado sob demanda para analisar algo específico e reportar. Ele:

- **Não edita código** (por padrão, só relata);
- **Roda em contexto isolado** (não polui a conversa principal);
- Retorna um **relatório estruturado** com achados classificados.

**Frontmatter obrigatório** em cada agent:

- `description`: uma frase do que ele faz;
- `model`: qual tier de modelo usa;
- `worktree`: `false` por padrão (read-only); `true` só se o agent for escrever;
- `model-rationale`: uma frase justificando a escolha do modelo.

### 3. Escolha de modelo por complexidade

Nem todo agent precisa do modelo mais caro. A escolha afeta custo, latência e qualidade: seja explícito.

| Tier | Quando usar | Exemplo |
|---|---|---|
| **Alto** (raciocínio profundo) | Consequência real de erro, correlação entre achados, julgamento de severidade | Auditoria de segurança, review arquitetural |
| **Médio** (checklists estruturados) | Verificações com thresholds claros, análise com heurísticas documentadas (**default recomendado**) | Code review, coverage check, spec validator |
| **Baixo** (formatação e leitura) | Extração, formatação, leitura sem julgamento complexo | Resumo de logs, listagem de arquivos |

**Regra prática:** se o agent tem checklist com thresholds numéricos → médio. Se precisa correlacionar findings e julgar severidade → alto. Se só lê e formata → baixo.

**Escreva o `model-rationale` no frontmatter.** Uma frase curta como *"checklist com thresholds numéricos, sem julgamento subjetivo"* garante rastreabilidade e facilita revisão.

### 4. Padrão de output de agent

Todo agent retorna relatório no mesmo formato. Isso viabiliza que humanos leiam rápido e outros agents consumam o output.

**Seções obrigatórias:**

1. Status: PASS | FAIL | PARTIAL;
2. Findings agrupados por severidade;
3. Próximos passos (linkando para skills ou outros agents).

**Severidades padrão:**

- 🔴 **Crítico**: bloqueia merge, segurança grave, dado incorreto;
- 🟠 **Alto**: funcionalidade quebrada, regra de negócio errada;
- 🟡 **Médio**: melhoria necessária, gap de UX;
- ⚪ **Info**: nice-to-have, referência, contexto.

### 5. Skill ou agent: como decidir

| Pergunta | Skill | Agent |
|---|---|---|
| Vou escrever código? | ✅ | |
| Quero analisar o que já está escrito? | | ✅ |
| Preciso de contexto local (arquivo atual)? | ✅ | |
| Preciso varrer o repo todo? | | ✅ |
| É preventivo (antes de agir)? | ✅ | |
| É verificativo (depois de agir)? | | ✅ |

Skills e agents se complementam. Um fluxo típico: *skill `security-checklist`* informa o dev antes de codar → *agent `security-audit`* varre depois para confirmar. Um é prevenção, o outro é detecção.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte V — Spec-driven Development

### 1. O fluxo canônico

```
Ideia → Backlog → Spec → (Research) → Plano → Implementação → Testes → Verificação → Done
```

Cada seta pode ter um **gate humano**: o momento em que um dev confirma que a fase anterior está sólida antes de avançar. Gates impedem o AI de acelerar na direção errada.

### 2. Cerimônia proporcional à complexidade

Nem toda mudança merece o mesmo processo. Over-engineering de processo é tão ruim quanto ausência dele.

| Tamanho | Critério | Artefatos | Fluxo |
|---|---|---|---|
| **Trivial (fast-path)** | Typo, bump de dependência, rename, fix 1-2 linhas | Nenhum | Codar direto, commit |
| **Pequeno** | ≤3 arquivos, sem nova abstração, sem mudança de schema | Spec leve ou nenhuma | Backlog → spec → código → teste |
| **Médio** | <10 tasks, escopo claro | Spec breve (contexto + requisitos + critérios) | Backlog → spec → plano → código |
| **Grande** | Multi-componente, >10 tasks | Spec completa + breakdown de tasks | Backlog → spec → design → plano → código |
| **Complexo** | Ambiguidade, domínio novo, >20 tasks | Spec + design + tasks paralelizáveis + estado entre sessões | Research → spec → design → plano → execução por fases |

**Antes de escrever a primeira linha de código** (médio para cima), devem existir como arquivos no disco:

1. Spec com status `aprovada`;
2. Plano de execução com ordem de tasks;
3. Se grande/complexo: documento de research com achados.

### 3. Estrutura canônica de uma spec

```markdown
# Spec {ID}: {Título}

**Status:** rascunho | aprovada | em andamento | parcial | concluída | descontinuada

## Contexto
Por que esta spec existe, qual problema resolve.

## Dependências
Specs ou componentes que esta precisa para existir.

## Requisitos Funcionais
- RF-001: {requisito}
- RF-002: {requisito}

(Referenciar IDs em comentários no código: `// Implements RF-001`)

## Escopo (checkboxes verificáveis)
- [ ] Item entregável 1
- [ ] Item entregável 2

## Critérios de Aceitação (afirmações testáveis)
- Dado X, quando Y, então Z
- A API retorna 200 para caso W

## Arquivos Afetados
- path/foo.ts: modificar
- path/bar.ts: criar

## Breakdown de Tasks (grande/complexo)
| Task | Depende de | Arquivos | Tipo | [P]? |
|---|---|---|---|---|
| T1 | — | foo.ts | backend | |
| T2 | T1 | bar.ts | backend | [P] |
| T3 | T1 | baz.ts | backend | [P] |

## Não Fazer (fora do escopo)
- Coisa X (fica para spec Y)

## Skills a consultar
- testing, security-review

## Verificação pós-implementação
- [ ] Testes passam
- [ ] Linter limpo
- [ ] Critérios acima validados
```

### 4. Task markers e paralelização

O marcador `[P]` na tabela de tasks indica **paralelizável**: a task não depende de outras na mesma wave e toca arquivos disjuntos de tasks paralelas. Sub-agentes em worktrees separados podem executá-las concorrentemente.

**Critérios para marcar uma task como `[P]`:**

- Dependências: só depende de tasks já concluídas (waves anteriores);
- Isolamento de arquivos: não modifica arquivos que outras `[P]` tocam;
- Sem efeito colateral global: não altera config, migrations ou schema compartilhado.

**Waves:** agrupar tasks em ondas numeradas. Todas as `[P]` da wave N rodam em paralelo; a wave N+1 só começa quando a anterior fecha. Entre waves, humano (ou agent revisor) faz merge consolidado.

### 5. Delta markers para brownfield

Em código legado, a spec precisa distinguir o que é novo vs. o que é modificado. Use marcadores:

- `[ADDED]`: funcionalidade completamente nova;
- `[MODIFIED]`: alterar código existente (referenciar arquivo e seção);
- `[REMOVED]`: remover funcionalidade (listar callers afetados).

Em greenfield, os marcadores são opcionais (tudo é `[ADDED]` implícito).

### 6. Gates e fast-path

**Gates** são pontos onde o AI deve **parar e pedir confirmação** antes de avançar:

- Spec rascunho → aprovada;
- Plano gerado → execução;
- Código pronto → verificação;
- Verificação ok → merge.

Em tarefas triviais (fast-path), os gates são dispensáveis: o humano inspeciona o commit final e pronto.

### 7. TDD ao implementar a partir de spec

Quando o projeto segue TDD:

1. Ler a spec (critérios de aceitação definem cenários);
2. Escrever testes **primeiro**, baseados nos critérios;
3. Implementar o mínimo para passar (green);
4. Refatorar se necessário.

Exceção: para fixes pequenos, teste de regressão antes do fix é suficiente. Não precisa escrever suíte nova.

### 8. Estratégia de testes com AI

A suíte de testes é o maior aliado do AI. Sem testes, o AI voa às cegas e você perde a principal forma de verificar o que ele produziu. Com testes, AI acelera com segurança.

**Pirâmide de testes (referência):**

| Camada | Propósito | Volume | Velocidade | AI é bom? |
|---|---|---|---|---|
| **Unit** | Função/classe isolada | Muitos | Muito rápido | ✅ Ótimo para escrever |
| **Integration** | Módulos interagindo (DB, serviço externo) | Moderado | Médio | ✅ Bom, mas precisa de fixtures/mocks |
| **E2E / acceptance** | Fluxo completo da aplicação | Poucos | Lento | 🟡 Funciona, mas frágil |
| **Mutation / property-based** | Detectar testes tautológicos, cobrir edge cases | Complementar | Variável | 🟡 AI gera bem com guidance |

**Usos do AI em testes:**

- **Escrever testes a partir de spec**: critérios de aceitação viram casos de teste;
- **Gerar fixtures** e dados de teste a partir de schemas;
- **Propor casos de borda** que o humano esqueceria;
- **Mock de dependências** externas;
- **Refatorar suítes** lentas ou duplicadas.

**Armadilhas específicas:**

- **Testes tautológicos:** AI escreve teste que chama `foo()` e asserta `foo() === foo()`. Parece cobertura, mas não prova nada. Verificação: *o teste falharia se a função estivesse errada?*
- **Mocks excessivos:** AI mocka coisas que deveriam ser testadas de verdade (ex: mock do DB em teste de integração). Resultado: teste passa, prod quebra.
- **Cobertura performativa:** AI cobre linhas, não comportamentos. `90% coverage` pode significar `30% das garantias reais`.
- **Teste a reboque do código:** gerar código + teste na mesma sessão vira *teste que prova que o código que o AI escreveu faz o que o AI escreveu*. Ordem melhor: escrever teste primeiro (com base na spec), humano revisa o teste, AI implementa o código.

**Regra:** testes devem nascer da spec, não do código. Quando o código nasce antes do teste, revisar ambos com olhar crítico redobrado.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte VI — Backlog como Single Source of Truth

O backlog não é uma lista de desejos. É o documento canônico do que está pendente, concluído, descartado e adiado. Trate-o como código.

### 1. Quatro seções fixas

O backlog tem exatamente quatro seções:

1. **Pendentes** (tabela por área temática);
2. **Concluídos** (ID | Item | Concluído em);
3. **Descartados** (ID | Item | Descartado em | Motivo);
4. **Decisões futuras** (parking lot: ID | Decisão | Gatilho | Recomendação).

Nunca deletar: itens concluídos ou descartados **permanecem registrados** como histórico navegável.

### 2. Taxonomia de classificação

Cada item pendente carrega metadados que orientam priorização e impacto. As colunas são:

| Coluna | Valores | Para que serve |
|---|---|---|
| **ID** | Prefixo + número (FEAT1, SEC3) | Referência estável |
| **Fase** | F1, F2, F3, T, OP | Agrupamento temático (não ordem) |
| **Item** | 1 frase | Descrição |
| **Sev.** | 🔴 Crítico, 🟠 Alto, 🟡 Médio, ⚪ Baixo | Urgência |
| **Impacto** | 👤 Usuário, 🔧 Interno, 💰 Negócio, 🛡️ Segurança | Quem é afetado |
| **Superfície** | 🔺 Fluxo, ⬜ Bastidor | Muda como o time trabalha ou roda por baixo? |
| **Destino** | 📦 Produto, 🏠 Infraestrutura | Quem se beneficia |
| **Compat.** | ✅ Aditivo, ⚠️ Migrável, ❌ Breaking | Impacto em quem já usa |
| **Tipo** | Feature, Bug, Segurança, Refactor, Testes, Docs | Categoria |
| **Est.** | 15min, 1h, 1d, 1sem | Tempo estimado |
| **Deps** | IDs de pré-requisitos | Bloqueios |
| **Origem** | Sessão, Auditoria, Produto, Incidente | De onde veio |

**Valor prático:** essas colunas convertem o backlog de "lista" em "dataset filtrável". Um dev consegue perguntar *"o que é 🔴 + 🔺 + 📦 e não tem deps?"* e ter uma resposta objetiva.

### 3. Fase vs. Wave

Confusão comum. Separe os conceitos:

- **Fase** = agrupamento temático. "Autenticação" é uma fase, "Observabilidade" é outra. Não define ordem.
- **Wave** = ordem de execução. Wave 1 vem antes de Wave 2, independente da fase.

Um item da Fase 3 pode estar na Wave 1 se é bloqueador de muitos outros. Um item da Fase 1 pode estar na Wave 4 se é isolado e não tem pressa.

**Regra para Waves:**

- Wave 1-2 → 🔺 **Fluxo** (muda artefatos que outros consomem);
- Wave 3+ → ⬜ **Bastidor** (isolados, automação, paralelizáveis).

### 4. Classificação de compatibilidade

A coluna `Compat.` responde: *"o que acontece com quem está numa versão antiga quando este item é mergeado?"*.

- **✅ Aditivo**: adiciona capacidade sem tocar o existente. Quem não atualizar continua funcionando. Zero interferência.
- **⚠️ Migrável**: muda formato ou comportamento de artefato existente, mas existe caminho de migração (manual ou automático). Quem não atualizar fica com versão antiga funcional, porém divergente.
- **❌ Breaking**: quebra artefatos ou fluxos sem intervenção manual. Quem não atualizar terá inconsistência ou erros. Exige guia de migração explícito.

Classificar certo aqui evita surpresas no release.

### 5. Regra de não deletar

Ao descartar um item:

1. **Não remover** da lista. Mover para "Descartados" com motivo explícito;
2. Riscar o nome (`~~texto~~`);
3. Registrar data e motivo objetivo (ex: *"conflita com filosofia X", "já resolvido pelo item Y", "fora do escopo atual"*);
4. Atualizar deps de outros itens que dependiam deste.

Isso evita reabrir a mesma discussão no futuro. Um registro explícito de *"essa ideia foi considerada e descartada por Z em AAAA-MM-DD"* é mais útil que o silêncio.

### 6. Decisões futuras (parking lot)

Nem toda ideia é pendente. Algumas são condicionais: *"se X acontecer, reavaliar Y"*. Essas não viram itens ativos; vão para "Decisões futuras" com:

- **Gatilho:** o evento que faria a decisão voltar à pauta (ex: "quando atingirmos 1000 usuários ativos");
- **Recomendação atual:** qual direção o time tenderia se o gatilho ocorresse hoje.

### 7. Detalhes por item (item-specs)

Itens complexos merecem uma spec própria em `{diretório}/item-specs/{ID}.md`, com:

- **Plano** (link para plano aprovado, se houver);
- **Contexto**: por que este item existe;
- **Abordagem**: decisão tomada e alternativas descartadas;
- **Critérios de aceitação** (checkboxes verificáveis);
- **Restrições**: o que NÃO fazer, dependências, gates.

O backlog aponta para o índice de item-specs; não duplica conteúdo.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte VII — Versionamento, Releases e Migrações

### 1. Conventional Commits

Todo commit segue o padrão:

```
{prefixo}{escopo opcional}: mensagem curta
```

**Prefixos e bump:**

| Prefixo | Quando | Bump semver |
|---|---|---|
| `feat:` | Funcionalidade nova | minor |
| `fix:` | Correção de bug | patch |
| `docs:` | Documentação | patch |
| `refactor:` | Reestruturação sem mudar comportamento | patch |
| `test:` | Só testes | patch |
| `chore:` | Infraestrutura, build, tarefas internas | — |
| `release:` | Commit gerado pelo processo de release | — |
| `feat!:` ou `BREAKING CHANGE:` | Incompatibilidade | major |

**Prática idiomática:** prefixos em inglês, mensagem no idioma do time. Isso mantém ferramentas de automação felizes (Conventional Commits é padrão internacional) e conversa humana acessível.

### 2. Commits atômicos: um motivo por commit

**Regra:** cada commit tem exatamente **um motivo de existir**. Se a mensagem tem "e" ou "+" ou múltiplos pontos, provavelmente são dois commits.

**Por que:**

- Revert granular: reverter um motivo sem perder os outros;
- Revisão: PR com commits atômicos é revisável linearmente;
- Bisect: quando bug aparece, bisect encontra exatamente qual mudança introduziu;
- Changelog: cada commit vira uma linha legível.

**Anti-padrão comum:**

```
feat: login, fix no logout, refactor do middleware e mais testes
```

Versão correta: quatro commits separados.

**Exceção:** commits de release (versão + tag + changelog em um commit só faz sentido porque são consequência mecânica uns dos outros).

### 3. Bump baseado no impacto real no usuário

A regra não é *"que prefixo o commit tem?"*. É: *"algo que chega a quem USA o produto mudou?"*.

**Conta para o bump:**

- Skills, templates, docs, scripts distribuídos para quem consome o produto;
- Mudanças em APIs públicas;
- Mudanças em contratos visíveis.

**NÃO conta para o bump:**

- Arquivos internos (backlog, processos internos, CI, scripts de validação interna);
- Refatorações invisíveis;
- Testes internos.

Isso evita releases "fantasma" onde só mudou processo interno e ninguém lá fora percebe.

**Regras de bump aplicadas apenas aos commits que chegam ao usuário:**

- Algum quebra compatibilidade? → **major**;
- Algum adiciona funcionalidade? → **minor**;
- Todos são correções? → **patch**;
- Nada chega ao usuário desde a última tag? → **sem release** (aguarda).

### 4. Checklist pré-release

Antes de qualquer bump:

- [ ] Working directory limpo;
- [ ] Artefatos source e distribuídos em sincronia;
- [ ] Inventário de artefatos (manifest) atualizado;
- [ ] Changelog atualizado (só mudanças que chegam ao usuário);
- [ ] Tags de versão consistentes nos arquivos que as carregam;
- [ ] Testes passam localmente.

### 5. Checklist pós-release

- [ ] Arquivo de versão (VERSION ou equivalente) com nova versão;
- [ ] Manifests de plugin/pacote com mesma versão;
- [ ] Changelog com entrada;
- [ ] Migration guide criado (ver item 7);
- [ ] Scripts de validação passam;
- [ ] Tag criada no git;
- [ ] Backlog atualizado: itens "pendente release" → versão real;
- [ ] Teste em ambiente real (não só CI).

### 6. Release via PR: sempre

**Regra absoluta: nenhum commit direto em main, incluindo releases.**

O commit de release vai em branch própria (`release/vX.Y.Z`) e entra via PR, mesmo sendo fast-forward. Isso garante:

- CI roda no commit final;
- Rastreabilidade via PR history;
- Aprovação humana documentada;
- Segurança contra releases acidentais.

Sim, dá um passo extra. Esse passo extra pagou dividendos muitas vezes.

### 7. Migrations como guias manuais

Para produtos distribuídos (SDKs, frameworks, CLIs, templates), toda release que tem impacto em quem já usa o produto precisa de um **guia de migração**: um arquivo markdown em `migrations/v{FROM}-to-v{TO}.md` que um usuário consegue ler e aplicar manualmente.

**Estrutura do migration guide:**

1. **Resumo** (1-3 frases);
2. **Pré-requisitos** (versão atual, migrations anteriores);
3. **Mudanças agrupadas por estratégia:**
   - **Overwrite:** substituir arquivo inteiro, indicando o que mudou, como aplicar e o impacto;
   - **Structural:** seções adicionadas ou removidas em arquivos compartilhados;
   - **Content patches:** mudanças dentro de seções existentes (ferramentas de merge automático normalmente não pegam isso; precisam ser aplicadas manualmente);
   - **Manual:** decisão humana requerida, fornecer diff e sugestão;
   - **Arquivos novos:** o que são, quando são relevantes;
   - **Arquivos removidos:** motivo, substituto.

**Princípio:** o migration guide deve ser auto-contido. Alguém sem acesso a qualquer ferramental automatizado consegue ler e aplicar manualmente. Automação que aplica migrations é bônus, não requisito.

### 8. Changelog com audiência em mente

Changelog não é `git log` bonito. É **comunicação com quem usa o produto**.

Regras:

- Agrupar por tipo (Added / Changed / Fixed / Removed / Security);
- **Incluir apenas mudanças que chegam ao usuário final**: omitir mudanças internas;
- Escrever na voz do usuário ("*Agora você pode configurar X*"), não na voz do dev ("*refatorei o módulo Y*");
- Linkar para migration guide quando aplicável.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->

## Parte VIII — Distribuição e Compatibilidade

Quando o harness (ou qualquer produto versionado) é **distribuído** para múltiplos projetos/times, surge um problema: projetos customizam. Como atualizar sem destruir customização?

### 1. Quatro estratégias de distribuição

Classifique cada arquivo distribuído por uma destas estratégias. A escolha é **explícita**: documente num manifest ao lado do produto.

| Estratégia | Comportamento | Quando usar | Risco |
|---|---|---|---|
| **overwrite** | Substitui o arquivo inteiro. Customização é sobrescrita. | Arquivo não é customizável (templates, assets padrão) | Nenhum (se a regra for clara) |
| **structural** | Compara estrutura (seções H2/H3). Adiciona ou remove seções. Ignora conteúdo dentro delas. | Arquivo misto: partes padrão + partes customizáveis | Baixo |
| **manual** | Mostra o diff. Nunca aplica sozinho; humano decide. | Arquivo 100% customizado (ex: arquivo de contexto do projeto) | Médio (depende do humano) |
| **skip** | Nunca toca. 100% conteúdo do projeto. | Arquivos gerados no setup e mantidos pelo time (backlog, specs) | Nenhum |

**Regra:** todo arquivo que sai junto com o produto tem uma estratégia declarada. Se não tem, assume-se skip (não mexe).

### 2. Tags de versão em artefatos

Cada arquivo distribuído carrega uma **tag de versão** como comentário no topo:

```
<!-- produto-tag: vX.Y.Z arquivo-source: {path} -->
```

Benefícios:

- `update` sabe a versão instalada de cada arquivo individualmente;
- Inconsistências são detectáveis por script de validação;
- Debugging: *"que versão deste arquivo tem esse bug?"* → olha a tag.

**Posição da tag:**

- Arquivos com frontmatter YAML: **primeira linha após o fechamento `---`** (frontmatter precisa ficar no topo);
- Arquivos sem frontmatter: **linha 1**.

### 3. Três cenários obrigatórios

Toda feature que distribui artefatos precisa funcionar em três cenários (testá-los é parte do DoD):

| Cenário | Teste |
|---|---|
| **Greenfield** | Setup gera estrutura completa; tudo é criado do zero |
| **Re-run em projeto existente** | Setup detecta o que já existe e complementa sem quebrar |
| **Update de versão anterior** | Update detecta ausência do novo artefato e oferece criação/migração |

**Perguntas a fazer para cada artefato novo:**

- *"E se este arquivo já existe no projeto? Setup re-run vai pular, mesclar ou atualizar?"*
- *"E se o projeto está em versão antiga sem este artefato? Update oferece?"*
- *"Se a estratégia é `skip`, nem setup re-run nem update tocam. Como o usuário descobre que existe?"*

### 4. Backward compatibility como default

Toda mudança deve assumir: **projetos mais antigos continuam funcionando sem modificação**. Isso significa:

- Novo campo opcional em spec ou backlog → não obrigatório;
- Novo arquivo → skills e scripts criam sob demanda se não existe;
- Novo formato → suporta também o formato antigo por pelo menos uma versão major.

Feature flags e shims temporários são ok quando a migração custa caro e o benefício compensa. Mas trate-os como dívida: documente quando removê-los.

### 5. Single-repo vs. monorepo

Duas formas de organização exigem pensamento diferente:

**Single-repo**: estrutura plana, um arquivo de contexto na raiz. Caso mais simples. Features de monorepo **não devem ter efeito visível aqui**: se a seção `## Monorepo` não existe no contexto, nada muda.

**Monorepo**: hierarquia arbitrária. Cada nível pode ter seu próprio contexto. O setup deve:

- Escanear até 2 níveis de profundidade (`apps/web/`, `services/auth/`);
- Excluir `node_modules/`, `vendor/`, `.git/`, `dist/`, `build/`;
- Detectar git submodules (`.gitmodules`) e **nunca configurar automaticamente dentro de submodule**; perguntar ao dev se inclui ou ignora.

**Por sub-projeto:** cada um pode ter seus próprios docs, skills, agents, backlog. O contexto raiz referencia, não duplica.
<!--/PT-->
<!--EN-->

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
<!--/EN-->

---

<!--PT-->

## Parte IX — Dual-mode

### 1. O conceito

Alguns artefatos existem **em mais de um meio**. Specs podem viver em arquivos markdown no repo, ou em tool de gestão (Notion, Linear, Jira). Backlog idem. Documentação idem.

**Regra dual-mode:** skills que operam nesses artefatos devem funcionar em **ambos os modos**, com detecção automática do modo vigente, sem perguntar ao usuário toda vez.

### 2. Detecção automática

Padrão comum: uma seção no arquivo de contexto principal declara qual modo está ativo. Exemplo:

```markdown
## Integração com ferramenta externa (specs)

Specs são mantidas em: {notion-database-id | linear-project-id | local}
```

Se a seção existe → modo remoto. Se não existe → modo local (arquivos no repo).

Skill executa:

1. Verificar arquivo de contexto;
2. Se modo remoto detectado: usar MCP / API da ferramenta;
3. Se modo local: usar arquivos no repo;
4. Fluxo é idêntico; saída é diferente.

### 3. Paridade de features entre modos

Ao adicionar uma feature numa skill dual-mode, implementar nos dois modos **no mesmo PR**. Divergência gera bug sistemático: times que migram entre modos encontram comportamento inconsistente.

**Exceção aceitável:** features que são *intrinsecamente* específicas a um meio (ex: "view kanban" só faz sentido em Notion, não em arquivo markdown). Documente a exceção.
<!--/PT-->
<!--EN-->

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
<!--/EN-->

---

<!--PT-->

## Parte X — Qualidade, Verificação e Auditorias

### 1. Task checklist obrigatório

Toda sessão que executa trabalho carrega um checklist padrão: itens que DEVEM ser verificados antes de considerar a tarefa pronta. Exemplo canônico:

1. **Plano de referência.** Se existe plano aprovado para esta tarefa, foi respeitado? Desvios foram documentados?
2. **Sincronia source ↔ distribuído.** Todo arquivo distribuído foi atualizado nos dois lugares?
3. **Manifest atualizado.** Se adicionou/removeu arquivo distribuído, foi registrado?
4. **Setup e update cobertos.** A mudança funciona em projeto novo E em projeto existente sendo atualizado?
5. **Dual-mode coberto.** Skills que operam em artefatos dual-mode foram testadas nos dois modos?
6. **Monorepo coberto.** Funciona em single-repo e em sub-projetos de monorepo?
7. **Docs e contexto atualizados.** Mudança de fluxo exige update em skills-map, workflow-diagram, quick-start, contexto principal?

O checklist é carregado automaticamente no início da sessão. Ignorar itens é decisão consciente, não esquecimento.

### 2. Definition of Done como contrato executável

**DoD não é um texto. É um script.** Toda mudança passa pelo mesmo `verify.sh` (ou equivalente), que é a forma **executável** do DoD.

**Estrutura típica:**

```bash
#!/usr/bin/env bash
# verify.sh — roda tudo, agrega erros, retorna non-zero se algo falhou

errors=0

echo "→ Lint"
npm run lint || errors=$((errors+1))

echo "→ Type check"
npm run typecheck || errors=$((errors+1))

echo "→ Testes"
npm test || errors=$((errors+1))

echo "→ Coverage threshold"
npm run coverage:check || errors=$((errors+1))

echo "→ Validações do harness"
bash scripts/validate-tags.sh || errors=$((errors+1))

if [ $errors -gt 0 ]; then
  echo "❌ verify.sh falhou ($errors etapas)"
  exit 1
fi

echo "✅ verify.sh passou"
```

**Propriedades do verify.sh:**

- **Fail-soft (agregador):** continua rodando mesmo se um passo falha. Quer saber **todos** os problemas de uma vez, não o primeiro.
- **Executável por qualquer um:** dev humano, AI, CI, todos com a mesma saída.
- **Parte do setup:** todo projeto tem um. Se não tem, DoD é ficção.
- **Versionado:** evolui junto com o código; novas regras do time viram novos passos.

**Regra:** se uma regra do time não está no `verify.sh`, ela vai ser violada. Convenção sem verificação automatizada não sobrevive.

### 3. Teste do "segundo arquivo"

Ao rodar auditoria de problemas no código, **nenhum achado é reportado sem o teste do segundo arquivo**:

> *Existe um segundo arquivo ou seção onde esse comportamento poderia estar justificado ou referenciado? Se sim, li antes de afirmar que é bug?*

Padrão de falso positivo recorrente: auditor lê o arquivo afetado isoladamente e conclui que algo está errado. Lê o arquivo adjacente que explica o design, e a conclusão desmorona.

**Exemplos comuns de falso positivo:**

- *"Este script não tem `set -e`"* → o design é fail-soft intencional, justificado no arquivo que o chama;
- *"Esta função não está referenciada"* → está, mas em outro doc que o grep não pegou;
- *"O template light deveria ser igual ao full"* → não deveria; razão de existir é divergir;
- *"Este arquivo falta X"* → X está em arquivo adjacente por design.

### 4. Registro de anti-padrões

Toda vez que uma auditoria produz falso positivo, **registre no arquivo de anti-padrões** (`AUDIT_ANTIPATTERNS.md` ou similar) com:

- O achado inicial;
- O segundo arquivo que invalidou;
- Regra para evitar repetir.

Esse arquivo é carregado antes de auditorias futuras. A cada ciclo, falsos positivos diminuem.

### 5. Três camadas de verificação

- **Validação de consistência:** tags de versão batem; source ↔ distribuído em sincronia; links internos não quebrados;
- **Validação de integridade:** setup instala limpo em ambiente vazio; update aplica sem quebrar;
- **Validação de DoD por projeto:** `verify.sh` compila, roda testes, lint, type-check, coverage mínimo.

Rodar localmente antes de PR, e no CI em cada push.

### 6. Code review de código gerado por AI

Reviewer de PR onde o autor principal é o AI precisa de checklist específico. Padrões recorrentes de erro:

**Confabulação de API:**
- Função chamada existe no pacote? (não se baseie no "parece plausível");
- Assinatura confere com a documentação oficial?;
- Versão da biblioteca suporta esta API?

**Copy-paste de padrões obsoletos:**
- Usa convenção atual do projeto, ou reciclou padrão antigo do treino?;
- Estilo de tratamento de erro bate com o resto do código?;
- Segue as convenções de nomenclatura do projeto?

**Tratamento de erro superficial:**
- `catch` vazio ou `catch { console.log(e) }`?;
- Erros ignorados silenciosamente?;
- Mensagens genéricas sem contexto acionável?

**Testes tautológicos:**
- O teste falharia se a implementação estivesse errada?;
- Assertivas testam comportamento ou só re-afirmam o código?;
- Há casos de borda reais ou só happy path?

**Mudanças "a mais":**
- O PR faz **só** o que a spec pede? Ou o AI aproveitou para "arrumar" coisas não solicitadas?;
- Refatoração oportunista sem spec = scope creep.

**Comentários redundantes:**
- Comentário explica **por que**, ou só parafraseia o **que** o código já diz? AI é propenso a gerar ruído explicativo;
- Remover comentários que não agregam.

**Segurança (ver Parte XI.5):**
- Input sanitizado?;
- Query parametrizada?;
- Dados sensíveis em log?

**Heurística do reviewer:** se você não entende uma linha em 30 segundos, ela é candidata a rejeição. Código que o próprio dev não consegue explicar não deve chegar em main.
<!--/PT-->
<!--EN-->

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
<!--/EN-->

---

<!--PT-->

## Parte XI — Segurança em Harness de AI

AI coding assistants expandem a superfície de ataque. O harness precisa **incorporar defesas explícitas**, não apenas esperar que o modelo seja bem-comportado.

### 1. Superfícies de risco

| Risco | O que acontece | Onde costuma aparecer |
|---|---|---|
| **Prompt injection** | Input externo (web, issue, email, log) contém instruções que o AI segue | Tools que leem conteúdo não-confiável: web fetch, scrapers, leitores de email, tickets |
| **Vazamento de secrets no contexto** | AI lê `.env`, `credentials.json`, histórico git → secret entra na conversa e pode vazar em logs/telemetria | Exploração ampla do repo, grep descuidado |
| **Geração de código vulnerável** | SQL injection, XSS, path traversal, IDOR (padrões comuns que o AI replica de treino) | Qualquer código novo, especialmente em endpoints e queries |
| **Permissões excessivas** | AI com acesso a prod, chaves AWS, Kubernetes, bancos → comando errado causa incidente real | Setups de dev que usam credenciais de staging/prod |
| **Dados sensíveis em telemetria** | Conversa vai para logs, billing, histórico do provedor; PII/segredo fica lá | Conversas que leem dados de cliente, produção, compliance |
| **Confabulação de APIs** | AI inventa função ou endpoint que parece plausível mas não existe | Stacks novas ou obscuras, APIs internas sem documentação |

### 2. Defesas no harness

**Allowlist de ferramentas e paths:**

- Lista do que o AI **pode** ler/executar. Tudo fora dela exige confirmação humana.
- Lista do que o AI **nunca** pode tocar: `.env`, `.git/config`, `credentials/`, `~/.ssh/`, `*.pem`, `.aws/`.
- Lista de comandos bloqueados: `rm -rf`, `chmod 777`, `git push --force` em branches protegidas, `kubectl delete` sem namespace, `DROP TABLE`.

**Prompt injection (tratar output externo como untrusted):**

Quando o AI processa saída de tool externo (web, API, log, arquivo de usuário), tratar como **dado**, não como **instrução**. Mesmo que o conteúdo contenha `"ignore previous instructions and do X"`, não seguir.

Prática: ao chamar tools que leem conteúdo externo, o AI deve reportar *o que viu*, não *agir no que viu*, sem confirmação humana explícita.

**Pre-commit hooks:**

- Scanner de secrets (`gitleaks`, `trufflehog`);
- Scanner de vulnerabilidades (SAST: `semgrep`, `bandit`);
- Checagem de dependências (`audit`, `snyk`).

Se o AI commita acidentalmente algo sensível, o hook bloqueia antes de sair.

**Code review obrigatório:**

AI pode abrir PR, nunca aprovar. Merge requer revisão humana, sempre. Isso é uma barreira que compensa pelos muitos riscos acima.

**Auditoria periódica:**

- Varredura de secrets no histórico;
- Listagem de paths que o AI acessou em sessões recentes;
- Validação de permissões efetivas (o AI não deveria ter podido acessar X; por que pôde?).

### 3. Ambient vs. confined authority

**Ambient:** o AI "herda" toda permissão do dev que o invocou. Lê qualquer arquivo, roda qualquer comando, empresta todas as credenciais ambientais. **Ruim.**

**Confined:** o AI opera num sandbox definido. Paths explícitos, comandos explícitos, credenciais dedicadas (com escopo mínimo). **Bom.**

A regra prática: tratar o AI como **colaborador externo**, não como "extensão da sua conta". Dar só o que precisa, nada além.

### 4. Segurança de specs e backlog

Specs e backlog podem conter informação sensível (roadmap competitivo, detalhes de infraestrutura, dados de cliente). Se o harness usa ferramenta remota (Notion, Linear), considerar:

- Permissões: quem tem acesso?
- Integração MCP/API: credenciais com escopo mínimo?
- Dados de cliente em spec: evitar; usar IDs, nunca nomes ou dados brutos.

### 5. Checklist de segurança por PR

- [ ] Nenhum secret hardcoded (scanner passou);
- [ ] Nenhuma query construída com string concat (SQL injection);
- [ ] Input de usuário validado e sanitizado;
- [ ] Output em HTML/JSX escapado (XSS);
- [ ] Path de arquivo validado contra traversal (`..`);
- [ ] Autenticação e autorização nos endpoints novos;
- [ ] Dependências novas auditadas;
- [ ] Logs não registram dados sensíveis (senha, token, PII).

### 6. Propriedade intelectual, licenças e compliance

AI coding assistants levantam questões legais que o harness precisa endereçar, não delegar para "quando der problema".

**Copyright de código gerado:**

A autoria de código gerado por AI ainda é área cinza legal em muitas jurisdições. Jurisprudência recente (EUA, UE) sugere que:

- Código puramente gerado por AI tipicamente **não** recebe proteção de copyright;
- Contribuição humana substancial (direção, edição, integração) restabelece copyright;
- Política corporativa deve tratar código gerado como **integrado** ao resto do trabalho do dev, não isolado.

**Ação prática:** política interna explícita. Ex: *"código aceito pelo dev é tratado como trabalho do dev para fins de propriedade"*.

**Contaminação por licenças incompatíveis:**

Modelos são treinados em código público, inclusive GPL/AGPL. Sugestões podem conter trechos reconhecíveis de repositórios licenciados de forma incompatível com o projeto.

**Risco real** em projetos proprietários que não aceitam copyleft: AI sugere bloco similar a código GPL → integra → violação de licença involuntária.

**Defesas:**

- Preferir AI assistants com cláusula de indenização por IP (alguns provedores oferecem);
- Scanner de plágio / similaridade de código em CI para blocos suspeitos;
- Política de "se eu não escreveria daquele jeito, não aceito": combate copy-paste literal.

**Retenção de prompts e dados pelo provedor:**

Conversas podem ser armazenadas para treinamento, logs operacionais, billing. Isso é incompatível com:

- **NDA com clientes** (dados do cliente no prompt → enviados ao provedor → fora do escopo do NDA);
- **GDPR/LGPD** (dados pessoais enviados ao provedor sem consentimento explícito);
- **Regulamentações setoriais** (saúde, financeiro);
- **Propriedade intelectual estratégica** (roadmap, código proprietário).

**Defesas:**

- Verificar política de retenção do provedor escolhido;
- Contratar tier "enterprise" ou "zero data retention" quando disponível;
- Regras no harness: *nunca colar dados de produção no prompt*;
- Redação/masking automático de PII antes de enviar.

**Exposição de secrets:**

Ver Parte XI.1: secrets no contexto viram secrets no histórico do provedor. Tratar como incidente de segurança se ocorrer.

**Compliance setorial:**

Setores regulados (financeiro, saúde, defesa, governo) têm restrições adicionais:

- **SOC 2 / ISO 27001:** processo documentado de uso de AI, auditoria de acessos;
- **HIPAA:** BAA (Business Associate Agreement) com o provedor antes de qualquer dado protegido tocar o prompt;
- **PCI-DSS:** dados de cartão nunca em prompts, mesmo em ambiente de dev;
- **Regulamentações de governo:** muitas vezes exigem AI on-premise ou em cloud soberana.

**Regra operacional:** antes de adotar AI assistant em escala organizacional, envolver jurídico e compliance. Não depois.

**Checklist de política de AI:**

- [ ] Política formal sobre uso de AI assistant documentada e assinada;
- [ ] Tier do provedor contratado está alinhado aos requisitos legais;
- [ ] Dados proibidos em prompts estão listados explicitamente;
- [ ] Processo de incidente caso secret/PII vaze para o provedor;
- [ ] Revisão periódica (anual?) da política com jurídico.
<!--/PT-->
<!--EN-->

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
<!--/EN-->

---

<!--PT-->
## Parte XII — Princípios Transversais
<!--/PT-->
<!--EN-->
## Part XII — Cross-cutting Principles
<!--/EN-->
<!--PT-->
Princípios que não cabem numa seção mas guiam tudo.

### 1. Simplicidade como regra

*"Simplicidade é a máxima sofisticação."*

- Skills são arquivos markdown, não CLIs;
- Specs são texto, não ferramentas complexas;
- Backlog é tabela markdown, não SaaS;
- Scripts de verificação são bash simples, não frameworks.

**Quando a simplicidade força dor**, revise: talvez precise um pouco de estrutura. Mas abstrações chegam **depois** de três casos reais, não antes.

### 2. Revisão humana entre fases

Todo gate crítico pede aprovação humana:

- Aprovação de spec;
- Aprovação de plano antes de execução;
- Aprovação de PR antes de merge;
- Aprovação de release antes de push da tag.

Automação é para o trabalho repetitivo. Julgamento é para humanos.

### 3. Persistir no disco, não na conversa

Toda decisão importante vira arquivo versionado:

- Plano aprovado → `plans/{ID}-{descricao}.md`;
- Spec → `specs/{ID}.md`;
- Item de backlog com complexidade → `item-specs/{ID}.md`;
- Migration guide → `migrations/vX-to-vY.md`;
- Changelog → `CHANGELOG.md`.

Conversas somem. Arquivos sobrevivem ao refresh da sessão, à troca de membro do time, à migração de ferramenta.

### 4. Não inventar abstração prematura

Antes de abstrair, existem três casos concretos? Se não, mantenha concreto. Repetição explícita é melhor que abstração errada, e **bem mais fácil de refatorar** do que abstração desfazer.

### 5. Diretrizes vs. regras

Harness separa dois tipos de documento:

- **Diretrizes**: princípios de design que guiam decisões ("preferimos simplicidade sobre completude");
- **Regras**: checks pontuais, verificações explícitas ("todo agent tem `model-rationale` no frontmatter").

Ambos têm lugar. Não transforme diretrizes em regras (vira burocracia); não deixe regras como diretrizes (vira negociável demais). A distinção está em: *vira check automatizável?* Se sim, é regra.

### 6. Fail-soft em agregadores, fail-fast em steps

Scripts que rodam **múltiplas verificações em sequência** devem continuar rodando mesmo quando uma falha (agregam todos os erros no final). Scripts que fazem **uma ação única** falham no primeiro erro.

Exemplo: `verify.sh` que roda lint + testes + type-check = fail-soft (quero saber TODOS os problemas). Script de setup = fail-fast (parar na primeira inconsistência).

### 7. Trust boundaries como tabela explícita

*"Onde o AI vira responsável pelo estado?"* é a pergunta central. A tabela abaixo é o contrato: cada linha define quem responde quando dá errado.

| Operação | Quem é responsável | Gate humano? | Observação |
|---|---|---|---|
| Sugestão em chat | Dev que aceita | ✅ (aceitar/rejeitar cada diff) | Humano lê e decide |
| Edit em worktree isolada | AI até abrir PR | ⏱️ No PR | Worktree garante que erro não vaza |
| Commit em branch não-main | Dev (autor) | ❌ | Branch isolada, risco contido |
| Merge em main | Reviewer do PR | ✅ Obrigatório | CI + revisão humana |
| Push de tag de release | Release manager | ✅ Obrigatório | Comando manual após aprovação |
| Deploy em staging | CI/CD | ⏱️ Automático após merge | Monitorar |
| Deploy em produção | Humano | ✅ Obrigatório | Nunca automático |
| Rodar migration em banco prod | Humano + runbook | ✅ Obrigatório | Backup antes |
| Execução de tool com credencial sensível | Humano | ✅ Caso a caso | Nunca ambient |

Um harness bem desenhado define claramente qual operação cruza qual fronteira. **Quando em dúvida, adicionar mais gate, não menos.**
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte XIII — Anti-padrões do Desenvolvedor Usando AI
<!--/PT-->
<!--EN-->
## Part XIII — Developer Anti-patterns When Using AI
<!--/EN-->
<!--PT-->
O AI assistant entrega o que você pede. Se você pede errado, ele erra. A maior parte dos problemas com AI em projetos reais **não é do modelo**: é da forma como o dev interage com ele.

### 1. Prompt vago

**Padrão:** *"faça o login funcionar"*, *"ajusta esse bug"*, *"melhora isso aí"*.

**Consequência:** o AI escolhe por você. Escolhe errado com frequência.

**Antídoto:** especificação. Mesmo informal: *"o endpoint POST /login deve retornar 401 quando a senha está incorreta, hoje retorna 500 porque {X}. Corrigir preservando a validação de email existente"*. Bom prompt é mini-spec.

### 2. Aceitar código sem ler

**Padrão:** "parece que funcionou" → commit → merge → bug em prod.

**Consequência:** você virou caixa de transmissão de código que não entende. Quando quebrar, não saberá consertar.

**Antídoto:** ler o diff. Não entendeu uma linha? Perguntar ao AI *por quê* aquela escolha antes de aceitar. Se ele não justificar bem, provavelmente está errado.

### 3. Pular o gate porque "é rápido"

**Padrão:** *"não precisa de spec, é 10 minutos"* → vira 3h → vira ramo abandonado com código pela metade.

**Consequência:** débito técnico silencioso. O fast-path existe por design, mas seu critério é específico (≤3 arquivos, sem nova abstração, sem mudança de schema). Tudo fora disso merece spec.

**Antídoto:** honestidade com o tamanho real da mudança. Quando em dúvida, trate como maior.

### 4. Contexto-stuffing

**Padrão:** *"pra garantir, vou carregar o repo inteiro no contexto"* → AI se perde, ignora regras, inventa.

**Consequência:** menos qualidade, mais custo, mais latência.

**Antídoto:** disciplina de contexto (Parte III). Carregar o necessário + referências; confiar no AI para pedir mais quando precisar.

### 5. AI como oráculo arquitetural

**Padrão:** *"devo usar microserviço ou monolito?"*, *"Postgres ou Mongo?"* para decisões com trade-offs dependentes do contexto do time.

**Consequência:** resposta genérica que parece sofisticada. Você adota e descobre 6 meses depois que não cabe.

**Antídoto:** usar AI para **mapear** trade-offs (ele é bom nisso) e **rascunhar** ADRs. Decisão final é humana, com conhecimento de time, história, pessoas.

### 6. Iterar quando deveria parar

**Padrão:** código não funciona → pede pro AI ajustar → ainda não → pede de novo → ainda não → 15 iterações depois, uma feature simples virou spaghetti.

**Consequência:** bug escondido debaixo de camadas de "correções" que nunca atacaram a causa.

**Antídoto:** após 2-3 iterações sem progresso, **parar**. Sair da sessão, ler o código com calma, identificar a raiz. Voltar com briefing novo.

### 7. Copy-paste de prompt entre projetos

**Padrão:** prompt que funcionou bem em projeto A é reutilizado em B sem adaptação de contexto.

**Consequência:** AI aplica convenções/padrões do projeto A em B. Código inconsistente, PR barulhento.

**Antídoto:** cada projeto tem seu harness. Prompts mencionam "este projeto" e esperam que o contexto (skills, arquivo de contexto, spec) preencha o específico.

### 8. Não atualizar STATE / docs no fim da sessão

**Padrão:** dia acaba, dev fecha laptop. Amanhã: "onde eu estava mesmo?".

**Consequência:** 30 minutos de arqueologia para reconstruir contexto. AI recomeça do zero, refaz decisões, contradiz escolhas anteriores.

**Antídoto:** última ação da sessão = atualizar STATE.md (ou equivalente). Primeira ação da próxima = ler.

### 9. Não registrar decisão descartada

**Padrão:** discussão longa → decide não fazer X → ninguém anota por quê → 3 meses depois, alguém sugere X de novo → mesma discussão.

**Consequência:** organização repete conversa. Time perde memória.

**Antídoto:** seção "Descartados" do backlog, "Decisões futuras" no parking lot. Registrar é cheap; redescobrir não.

### 10. Tratar AI como substituto em vez de colaborador

**Padrão:** *"o AI vai escrever isso sozinho"* → dev desliga o cérebro → bug.

**Consequência:** dev perde afinidade com o código. Quando AI falha (vai falhar), não sabe socorrer.

**Antídoto:** pair programming mindset. AI é colega júnior acelerado; você é mentor, não espectador.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte XIV — Quando NÃO Usar AI Assistant
<!--/PT-->
<!--EN-->
## Part XIV — When NOT to Use an AI Assistant
<!--/EN-->
<!--PT-->
Harness maduro sabe os limites. Usar AI onde ele é ruim é pior que não usar.

### 1. Debug de concorrência sutil

Race conditions, deadlocks, inconsistência de estado distribuído exigem raciocínio não-linear, hipóteses contra-intuitivas e frequentemente experimentação física (profilers, trace, logs de produção). AI **acelera** mapeamento de hipóteses, mas o salto de insight costuma ser humano.

**Uso recomendado:** AI ajuda a estruturar hipóteses e gerar logs de instrumentação. Humano interpreta.

### 2. Decisões arquiteturais novas

"Devemos adotar event sourcing?" depende de: time, skills internas, pressão de produto, infraestrutura, histórico de incidentes. AI não tem esse contexto; dá resposta estatisticamente plausível, não boa.

**Uso recomendado:** AI rascunha ADR com trade-offs conhecidos. Decisão humana.

### 3. Código regulado sem spec clara

GDPR, LGPD, PCI, HIPAA, SOX: áreas onde "parece certo" não basta. Exige rastreabilidade de requisito-regulatório → código → teste → auditoria.

**Uso recomendado:** só com spec regulatória formal e code review especializado. Sem spec, não tocar.

### 4. Incidentes críticos em produção

Pressão de tempo + escopo amplo + stakeholders + decisões reversíveis rapidamente. AI introduz variância quando você precisa de determinismo e familiaridade.

**Uso recomendado:** durante incidente, usar AI apenas para queries paralelas rápidas (ler log, extrair timeline). Commits de fix emergenciais: humano.

### 5. Refatoração gigante sem testes

Sem suíte de testes, o AI voa às cegas. Vai gerar código que parece correto, quebra feature sutil, ninguém percebe até semanas depois.

**Uso recomendado:** primeiro, escrever testes (aí sim o AI ajuda). Depois, refatorar.

### 6. Domínio muito novo ou obscuro

Em stacks/bibliotecas que saíram recentemente ou são nicho, o AI confabula mais. Inventa APIs plausíveis que não existem.

**Uso recomendado:** verificar cada função chamada contra a documentação oficial. Se o custo de verificação > custo de escrever à mão, não usar AI nessa parte.

### 7. Tarefas com requisitos contraditórios

*"Rápido, seguro, barato e simples"*: quando os requisitos se chocam, AI escolhe arbitrariamente (tipicamente seguindo o último pedido). Humano negocia trade-off consciente.

**Uso recomendado:** priorizar os requisitos (ou reformular o problema) antes de envolver o AI.

### 8. Exploração de código legado sem mapa

Sistemas sem documentação, sem testes, com convenções implícitas e desvios históricos. O AI lê cada arquivo como se fosse independente; o valor está nas conexões implícitas que não estão escritas.

**Uso recomendado:** humano explora primeiro, mapeia. Depois AI ajuda com mudanças pontuais.

### Heurística final

> *Se você não consegue descrever o resultado esperado em 3 frases verificáveis, o AI não vai entregar algo útil.*

Quando a tarefa é vaga, exploratória e precisa de julgamento, o AI tipicamente degrada performance. Quando é bem-definida e verificável, ele acelera.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte XV — Governança e Evolução do Harness
<!--/PT-->
<!--EN-->
## Part XV — Harness Governance and Evolution
<!--/EN-->
<!--PT-->
O harness é software. Software apodrece se ninguém cuida. Definir governança explícita é o que impede virada lenta para "cada um faz como quer".

### 1. Ownership por tipo de artefato

| Artefato | Dono | Justificativa |
|---|---|---|
| **Arquivo de contexto principal (L0)** | Tech lead / staff engineer | Convenções globais afetam todo mundo |
| **Contexto de domínio (L2)** | Tech lead do domínio | Regras locais |
| **Skills de domínio** | Time do domínio | Quem sabe é quem escreve |
| **Skills core (testing, security)** | Platform / DX team | Ortogonais ao domínio |
| **Agents** | Platform / DX team | Tooling compartilhado |
| **Manifest, estratégias, migrations** | Platform team | Infra de distribuição |
| **Spec de um projeto** | PM + tech lead do projeto | Negócio + técnica |

### 2. Ciclo de mudança de skill/agent

1. **Proposta**: via PR com justificativa (link para caso real onde o harness falhou);
2. **Revisão**: 1-2 devs do time dono (regra do "dois olhos");
3. **Teste em projeto real**: não basta passar validação sintática; aplicar num projeto e observar comportamento;
4. **Migration guide**: se for breaking, documentar o caminho;
5. **Merge + release** (Parte VII).

Mudanças aditivas passam rápido. Breaking passa com cerimônia.

### 3. Poda regular

Harness acumula cruft. Sem poda, vira entulho. Cadência sugerida: revisão trimestral.

**O que procurar:**

- **Skills não usadas em 6+ meses**: arquivar ou consolidar;
- **Skills com >80% de sobreposição**: mesclar;
- **Regras que ninguém segue**: ou remover, ou ensinar (mas não deixar apodrecendo);
- **Docs órfãs** (não referenciadas em lugar nenhum): linkar ou remover;
- **Anti-padrões resolvidos**: mover para histórico, não manter como alerta ativo.

**Como decidir remover:** se não dói no curto prazo e ninguém nota em 30 dias após deprecation, pode remover.

### 4. Sinais de harness fora de controle

- Contexto principal passa de 600 linhas;
- 50+ skills com alta sobreposição e nomes confusos;
- Dev novo não sabe onde procurar a regra e pergunta no Slack;
- Devs fazem "fora do harness" porque "é mais rápido";
- Última atualização do arquivo principal tem 1+ ano;
- Scripts de verificação estão quebrados há semanas e ninguém conserta;
- Backlog do harness próprio tem >50 itens pendentes;
- Discussão recorrente sobre "refazer tudo do zero".

Se você reconhece 3+ sinais, é hora de parar tudo e fazer faxina.

### 5. Evolução como processo, não evento

Harness **não** é projeto de trimestre que termina. É processo contínuo, como dependência de biblioteca. Cada trimestre:

- Revisa o que mudou (retrospectiva);
- Poda o que não serve mais;
- Incorpora 1-2 padrões novos que o time descobriu empiricamente;
- Atualiza docs de onboarding.

Trate como parte do investimento de plataforma, não como "tempo ocioso".

### 6. Migração entre versões de modelo

Modelos evoluem rápido. A cada 6-12 meses, provedores lançam versões novas (melhor raciocínio, mais barato, context maior). Trocar de modelo parece "só trocar uma variável". Não é.

**O que muda de fato:**

- **Comportamento em prompts existentes**: mesmo prompt pode gerar output diferente;
- **Sensibilidade a system prompts**: regras que eram seguidas podem ser ignoradas;
- **Tratamento de edge cases**: casos que o modelo antigo errava podem acertar (ou vice-versa);
- **Custo e latência**: pode melhorar ou piorar;
- **Limites de contexto**: janela maior permite novos padrões; janela menor força re-desenho.

**Processo de migração:**

1. **Audit inventário:** quais skills, agents, prompts são sensíveis à troca? Quais skills têm thresholds ou comparações numéricas que podem mudar?
2. **Canary:** rodar modelo novo em subconjunto pequeno (1-2 devs, 1-2 skills) por 1-2 semanas; comparar output.
3. **Regression suite:** se existe suíte de testes de agents (ex: relatórios em golden format), rodar no modelo novo e comparar.
4. **Ajuste de prompts:** modelos novos costumam ter idiossincrasias; pequenos ajustes em skills/agents resolvem 80% das regressões.
5. **Rollout gradual:** 10% → 50% → 100% com tempo de observação entre etapas.
6. **Documentar no changelog do harness:** *"v2.5.0: migrado para modelo X. Mudanças observadas: Y, Z."*

**Quando NÃO migrar:**

- Sem suíte de regressão;
- Próximo a release crítico / incidente em andamento;
- Sem plano de rollback (voltar ao modelo antigo deve ser 1 flag);
- Modelo novo ainda em early preview (instável).

**Regra:** tratar troca de modelo como **upgrade de dependência crítica**, não como configuração. Dedicar sprint próprio se a mudança for significativa.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte XVI — Adoção: Do Zero ao Maduro
<!--/PT-->
<!--EN-->
## Part XVI — Adoption: From Zero to Mature
<!--/EN-->
<!--PT-->
Harness não nasce completo. Tentar adotar tudo de uma vez é a receita para abandono. O caminho certo é **incremental**, com cada passo entregando valor sozinho.

### 1. Tiers de maturidade

| Tier | Tempo típico | Características |
|---|---|---|
| **Tier 0: Sem harness** | — | AI usado ad hoc. Sem padrão. Qualidade varia por dev. |
| **Tier 1: Light** | 2-4 semanas | Arquivo de contexto básico, 3-5 skills core, DoD informal. |
| **Tier 2: Standard** | 2-4 meses | Contexto hierárquico, 10-20 skills, 3-5 agents, spec fluxo leve, backlog estruturado, `verify.sh`. |
| **Tier 3: Full** | 6-12 meses | Orquestração (RPI), dual-mode, migrations, governance formal, métricas, compatibilidade declarada. |

**Importante:** a maioria dos times deve parar no Tier 2. Tier 3 só compensa em produtos distribuídos ou times muito grandes.

### 2. Roadmap incremental

**Semana 1-2: Fundação**

- [ ] Criar arquivo de contexto principal (L0) com: stack, convenções globais, fluxo de commit/PR, restrições de segurança;
- [ ] Rodar primeira sessão pelo arquivo, observando se o AI comporta-se de acordo.

Entrega: AI já respeita convenções básicas. Diferença imediata.

**Mês 1: Expertise mínima**

- [ ] 3-5 skills core: testing, code-quality, security-review, definition-of-done, commit-hygiene;
- [ ] `verify.sh` mínimo: lint + testes + type-check;
- [ ] Task checklist no início de sessões não-triviais.

Entrega: PRs mais consistentes. Bugs triviais filtrados.

**Mês 2: Backlog e spec leves**

- [ ] Criar `backlog.md` com 4 seções fixas;
- [ ] Template de spec leve (médio complexidade);
- [ ] Convenção: mudanças médias+ precisam de spec aprovada antes do código.

Entrega: escopo controlado. Menos "refactor" que vira "reescrever tudo".

**Mês 3-4: Automação**

- [ ] 3-5 agents auditores: code-review, security-audit, coverage-check;
- [ ] CI rodando `verify.sh` em cada PR;
- [ ] Pre-commit hooks para secrets e lint.

Entrega: verificação automática. Humano revisa o que sobra.

**Mês 5-6: Refinamento**

- [ ] Contexto hierárquico (L0 → L2) se monorepo;
- [ ] Skills de domínio (UX, DBA, observabilidade) conforme necessidade;
- [ ] Padrão STATE.md para tasks grandes.

Entrega: harness adaptado à realidade do time.

**Mês 6+: Avançado (se fizer sentido)**

- [ ] Orquestração RPI para tarefas complexas;
- [ ] Dual-mode (repo + ferramenta de gestão);
- [ ] Migration guides versionados;
- [ ] Governance formal com ownership declarado;
- [ ] Métricas de saúde (Parte XVII).

### 3. Armadilhas de adoção

**Adotar demais, cedo demais.** Time vê apresentação bonita, adota todas as features do harness maduro num mês, abandona em dois. Comece mínimo.

**Adotar sem o time.** Tech lead implementa no escuro, devs descobrem no PR e rejeitam. Adoção é mudança cultural: envolver o time nas decisões.

**Não medir.** Sem métrica, "harness está funcionando?" vira opinião. Definir 2-3 indicadores desde o Tier 1 (ver Parte XVII).

**Tratar como projeto de uma pessoa.** Se a pessoa sai, o harness apodrece. Pelo menos 2 pessoas com ownership declarado.

**Copiar sem adaptar.** Harness de outro time/empresa é ponto de partida, não template. Stack, cultura e tamanho mudam tudo.

### 4. Quando NÃO adotar harness

Harness tem custo real: setup, manutenção, onboarding, disciplina. Em alguns contextos, o custo supera o benefício. Honestidade importa: harness não é sempre a resposta.

**Contextos onde harness NÃO paga:**

- **Time de 1-2 devs com projeto pequeno.** A overhead de manter skills, backlog estruturado e specs formais não se dilui. Convenção mental + code review pontual bastam.
- **Hackathons, POCs e protótipos descartáveis.** Velocidade > qualidade; o artefato tem shelf life de dias a semanas. Investir em harness é jogar fora com o POC.
- **Scripts one-off e automações locais.** Um script de 50 linhas que roda uma vez não pede backlog nem spec.
- **Exploração acadêmica / pesquisa.** Fluxo de pesquisa é iterativo-divergente; harness rígido engessa. Cabe disciplina leve (versionamento, README) sem a infraestrutura completa.
- **Early-stage com stack instável.** Se a stack muda toda semana (pré-PMF, validação), skills e convenções envelhecem mais rápido do que valem. Investir pós-estabilização.
- **Projetos cujo ciclo de vida planejado é inferior a 3 meses.** Sem tempo para o harness "pagar"; crie o essencial, entregue, arquive.
- **Equipe sem buy-in.** Se o time não vai respeitar o processo, harness vira teatro. Primeiro o convencimento, depois a estrutura.

**Heurística:**
> *Se o harness toma mais tempo para manter do que o benefício mensurado devolve, está errado: ou cedo demais, ou grande demais, ou no projeto errado.*

**Caminho do meio:** harness "mínimo viável", só o arquivo de contexto principal + `verify.sh` com lint/test. Sem spec formal, sem backlog taxonômico, sem agents. Quando o projeto mostrar maturidade e o time pedir, evoluir para Tier 1.

### 5. Como os papéis no time mudam

Adotar harness + AI assistant reconfigura o trabalho do time. Ignorar essa reconfiguração é fonte comum de resistência e desorientação.

**Júnior.**
- **Acelera:** onboarding encurta, exposição a padrões bons é imediata, ciclo de feedback é curto.
- **Risco:** aprender superficialmente (aceitar código sem entender, pular fundamentos porque "o AI faz").
- **Contramedida:** mentoria pair-first (Parte XVIII.5) com foco em **entender**, não em **entregar**. Pedir ao júnior para explicar o que o AI escreveu antes de aceitar.

**Pleno.**
- **Acelera:** tarefas rotineiras (CRUD, scaffolding, refactor mecânico) saem em fração do tempo.
- **Risco:** virar "despachante de código" que transmite pedido, copia output, esquece de pensar.
- **Contramedida:** usar o tempo liberado para trabalho de maior abstração (design, refactor estrutural, ownership de domínios). Prompt vira especificação.

**Sênior.**
- **Muda mais:** menos código escrito direto, mais revisão, mais mentoria, mais desenho.
- **Novo trabalho:** escrever e manter skills, revisar output de agents, dimensionar complexidade (Parte V.2), julgar trade-offs.
- **Risco:** perder *craft* por usar AI demais. Atrofia de habilidades existe.
- **Contramedida:** manter "código do próprio punho" em tarefas onde *querer* aprender importa, não só *conseguir* entregar.

**Tech lead / arquiteto.**
- **Muda mais ainda:** o produto de engenharia passa a incluir o **próprio harness**: contexto, skills, agents, gates.
- **Novo trabalho:** governança (Parte XV), adoção (Parte XVI), métricas de saúde (Parte XVII), trust boundaries (Parte XII.7).
- **Valor:** arquitetar o sistema de trabalho, não só o sistema de código.

**Platform / DX team.**
- **Passa a ser dona** do harness core: templates, agents compartilhados, scripts de verificação, migrations entre versões.
- **Cadência:** sprint próprio para evoluir harness, como qualquer produto interno.

**IC generalista → especialista em domínio.**
- Com AI pegando scaffold e padrões genéricos, o valor humano se concentra em **conhecimento profundo de domínio**: regras de negócio, compliance, pessoas.
- Generalização rasa torna-se commodity; especialização profunda continua escassa.

**Regra geral:** o valor humano desloca de *produzir código* para *julgar, desenhar, decidir e ensinar*. Quem adapta, cresce; quem resiste, estagna. Conversar abertamente sobre essa mudança com o time é melhor que deixar acontecer por acidente.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte XVII — Métricas de Saúde do Harness
<!--/PT-->
<!--EN-->
## Part XVII — Harness Health Metrics
<!--/EN-->
<!--PT-->
Harness sem métrica vira opinião. Sem indicadores, discussões ficam no *"acho que está ajudando"*. Defina 3-5 indicadores e revise trimestralmente.

### 1. Indicadores quantitativos

| Métrica | Como medir | Meta saudável |
|---|---|---|
| **Reincidência de bug** | % de bugs corrigidos que voltam em 90 dias | < 5% |
| **Time-to-first-gate** | Do item entrar no backlog até ter spec aprovada | < 3 dias (médio), < 1 dia (pequeno) |
| **Spec rework** | % de specs que voltam para "rascunho" depois de "aprovada" | < 15% |
| **Skill coverage** | % de PRs que consultaram/aplicaram pelo menos uma skill relevante | > 70% |
| **Context file churn** | Mudanças por mês no arquivo de contexto principal | 1-5 (nem instável, nem esquecido) |
| **Validation pass rate (1st try)** | % de PRs que passam no `verify.sh` no primeiro push | > 60% |
| **Mean review cycles** | Número médio de rodadas de revisão até merge | < 2.5 |
| **Tempo em PR aberto** | Mediana do tempo do PR aberto até merge | < 2 dias úteis |
| **Adoção do fast-path** | % de mudanças triviais que usaram fast-path corretamente | > 80% |

### 2. Indicadores qualitativos

Não tudo é número. Pesquisa trimestral com o time (5-10 questões):

- *"O harness acelera ou atrapalha meu trabalho?"* (escala 1-5);
- *"Sei onde procurar a regra X?"* (sim / não / sei mais ou menos);
- *"Código gerado com AI tem a mesma qualidade do meu?"* (melhor / igual / pior);
- *"Dev novo consegue operar em 2 semanas?"* (sim / não);
- *"Qual é a coisa mais chata do harness hoje?"* (aberta);
- *"O que falta?"* (aberta).

A combinação quantitativo + qualitativo evita dois erros:

- **Quantitativo só**: métricas boas, todo mundo odiando;
- **Qualitativo só**: todo mundo feliz, bugs em prod.

### 3. Revisão periódica

Trimestral, em 1-2h:

1. Olhar os indicadores → qual piorou?;
2. Ler pesquisa qualitativa → tema recorrente?;
3. Listar 1-3 ações para próximo trimestre;
4. Atualizar backlog do harness com essas ações.

### 4. Quando reorganizar

Se em dois trimestres consecutivos:

- Reincidência sobe;
- Validation pass rate cai;
- Qualitativo despenca;

É hora de revisitar estrutura. Não continuar empilhando: **parar e limpar**.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte XVIII — Onboarding Humano ao Harness
<!--/PT-->
<!--EN-->
## Part XVIII — Human Onboarding to the Harness
<!--/EN-->
<!--PT-->
Harness funciona quando o time sabe usar. Dev novo que não foi onboardado gera duas consequências ruins: descredibiliza o sistema ("meu colega não usa, então não preciso") e cria débito silencioso (atropela skills sem saber que existiam).

### 1. Dia 1: Orientação

**Objetivos:** mapa mental básico + primeira tarefa executada corretamente.

- [ ] Ler o arquivo de contexto principal (L0), 30 min;
- [ ] Ler QUICK_START.md ou README do harness, 30 min;
- [ ] Fazer uma tarefa trivial (fast-path) acompanhado, 1-2h: typo, bump de dep, rename. Observar o fluxo;
- [ ] Ter o primeiro PR revisado linha por linha por mentor.

Entrega: dev entende "existe um harness, aqui é onde começo".

### 2. Semana 1: Imersão

**Objetivos:** familiaridade com skills do domínio + primeira spec pequena.

- [ ] Ler as 3-5 skills mais relevantes ao domínio do dev;
- [ ] Acompanhar um PR médio do time (do início ao fim, incluindo spec);
- [ ] Fazer uma spec pequena (1-3 tasks) com mentor revisando;
- [ ] Rodar `verify.sh` local várias vezes para sentir o feedback;
- [ ] Ler anti-padrões registrados (Parte X + Parte XIII).

Entrega: dev consegue operar em tarefas pequenas sem supervisão constante.

### 3. Mês 1: Autonomia

**Objetivos:** operação independente em escopo médio.

- [ ] Primeira spec média com revisão apenas em gates;
- [ ] Contribuir para o harness: propor uma skill nova, ou melhorar uma existente;
- [ ] Participar de uma auditoria (ou reporte de agent) e entender output estruturado;
- [ ] Review: o que o dev ainda não sabe? Onde está perdido?.

Entrega: dev opera sozinho em complexidade média. Pode ser par em tarefas grandes.

### 4. Materiais essenciais

Sem estes, onboarding trava:

- **Mapa de skills**: tabela com nome, propósito, quando usar;
- **Workflow diagram**: diagrama ASCII ou visual do fluxo ideia → done;
- **Exemplos de specs reais**: 2 boas, 1 ruim (anotada com o que deu errado);
- **Exemplos de PRs**: boas referências;
- **Anti-padrões registrados**: ler e internalizar;
- **Quick wins**: lista de tarefas triviais ideais para primeiro dia;
- **Canal de perguntas**: Slack / Discord / fórum onde dúvidas viram FAQ.

### 5. Mentoria pair-first

Primeiras semanas: pair programming **síncrono** com mentor. Não é micro-management; é transferência de tácito. Dev observa mentor usar o harness: como ele pede ao AI, como decide entre skill/agent, como faz context reset, como atualiza STATE.

Depois de 2-4 semanas: pair assíncrono (review de PR detalhado). Depois: review normal.

### 6. Anti-padrões de onboarding

- **"Lê essa wiki e vira"**: sem prática acompanhada, doc não gruda;
- **Carregar com todas as skills no dia 1**: intransitável. Carregar aos poucos;
- **Não mostrar anti-padrões**: dev reinventa os mesmos erros que já foram documentados;
- **Mentor "disponível", mas nunca presente**: presença agendada, não reativa;
- **Skip do fast-path**: começa com tarefa grande, dev se afoga;
- **Não coletar feedback**: onboarding vira padrão e o padrão envelhece.

### 7. Métrica de onboarding

- **Tempo até primeiro PR mergeado:** < 3 dias úteis;
- **Tempo até operar em escopo médio sem supervisão:** < 4 semanas;
- **Pesquisa pós-onboarding (30 dias):** *"Sabia usar o harness ao sair do onboarding?"* (1-5).

Se estes números pioram, onboarding precisa evoluir, não o novo dev.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte XIX — Anatomia de um Bom Prompt
<!--/PT-->
<!--EN-->
## Part XIX — Anatomy of a Good Prompt
<!--/EN-->
<!--PT-->
A Parte XIII listou anti-padrões; esta é a contrapartida construtiva. Um bom prompt economiza iterações, reduz confabulação e melhora qualidade.

### 1. Três intenções, três estruturas

Todo prompt cai numa das três intenções abaixo. A estrutura muda.

**A. Explorar**: "me ajude a entender X, mapear possibilidades, listar abordagens"

Estrutura:
- Objetivo (entender / decidir / escolher);
- Contexto do que já foi considerado;
- Restrições conhecidas;
- Formato de saída (tabela, lista, prós/contras).

Exemplo:
> *"Estou decidindo entre Postgres e MySQL para o serviço X. Workload: 80% leitura, dados de até 10TB em 2 anos, precisa de JSON queries. Já uso Postgres em outros serviços. Liste 3-5 critérios de decisão com prós/contras de cada banco. Formato: tabela."*

**B. Implementar**: "escreva código que faz Y"

Estrutura:
- Spec curta (o que, por quê);
- Critério de aceitação verificável;
- Arquivos afetados;
- Restrições (não tocar em X, preservar Y);
- Skills ou padrões a seguir.

Exemplo:
> *"Implementar endpoint POST /users/:id/deactivate. Deve marcar o usuário como inativo (is_active=false), invalidar sessões ativas, e enviar evento user.deactivated para o bus. Arquivos: controllers/user.ts, services/session.ts. Preservar o padrão de autorização atual (middleware adminOnly). Retornar 204 em sucesso. Testes seguindo o padrão do describe existente."*

**C. Revisar / criticar**: "analise Z e reporte"

Estrutura:
- O que analisar (escopo);
- Critérios (o que é "bom" vs. "ruim" neste contexto);
- Severidade esperada;
- Formato do relatório.

Exemplo:
> *"Revisar o PR #234 procurando: (1) vulnerabilidades de segurança comuns (injection, XSS); (2) tratamento de erro ausente; (3) testes tautológicos. Reportar achados em formato: severidade (🔴🟠🟡), arquivo:linha, descrição, sugestão."*

### 2. Anatomia mínima de um prompt útil

```
[Contexto: onde estou, o que é o projeto — 1-2 frases]
[Objetivo: o que quero, verificável — 1 frase]
[Restrições: o que NÃO fazer — 1-3 bullets]
[Formato esperado: estrutura da resposta — 1 frase]
```

Prompt com essas quatro partes é 10x melhor que "faça X".

### 3. Erros construtivos comuns

| Erro | Exemplo | Correção |
|---|---|---|
| **Verbo vago** | "melhore esse código" | "reduza duplicação entre funA e funB extraindo helper comum" |
| **Sem critério** | "refatore para ficar mais limpo" | "refatore para que funA tenha <20 linhas e zero condicionais aninhadas" |
| **Escopo implícito** | "consertar o bug" | "consertar falha em login quando email contém + (bug #123)" |
| **Sem restrição** | "adicionar cache" | "adicionar cache em getUser, TTL 5min, usando Redis existente, sem mudar assinatura pública" |
| **Sem formato** | "liste os problemas" | "liste problemas em bullets, agrupados por severidade, máximo 10" |

### 4. Escalar o detalhamento com a complexidade

- Fast-path (typo, bump): 1-2 frases bastam;
- Pequeno: prompt com 4 partes da anatomia;
- Médio+: prompt referencia spec aprovada e plano; contexto vem dos arquivos, não do prompt.

Ou seja: para trabalho grande, o prompt é curto porque o **contexto está nos artefatos**.

### 5. Tom e restrição de iniciativa

AI tende a "ajudar além do pedido": refatora o que não foi pedido, adiciona features vizinhas, melhora estilo que estava bom. Controlar explicitamente:

- *"Só mude o necessário para X. Não refatore código não relacionado."*
- *"Se encontrar problema fora do escopo, reporte, não corrija."*
- *"Mantenha convenções existentes mesmo se você discordar delas."*

### 6. Quando o prompt está ruim: sinais

Se o output tem um destes sintomas, o prompt é que precisa melhorar:

- Resposta genérica que caberia em qualquer projeto;
- Código com placeholders (`TODO`, `// your logic here`);
- Múltiplas "opções" quando você queria uma resposta;
- AI pede esclarecimento repetidas vezes sobre coisa óbvia;
- Output grande demais, cobrindo coisas que você não pediu.

Cada um indica lacuna específica no prompt. Corrigir na origem é mais rápido que iterar no output.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte XX — Debug Workflow com AI
<!--/PT-->
<!--EN-->
## Part XX — Debug Workflow with AI
<!--/EN-->
<!--PT-->
AI acelera debug quando usado corretamente. Mal usado, amplifica confusão. O fluxo abaixo é o padrão que funciona.

### 1. Antes de chamar o AI: repro mínimo

**Regra de ouro:** AI sem repro é adivinhação. Investir em reproduzir o bug de forma mínima e determinística **antes** de pedir ajuda.

Checklist de repro:
- [ ] Comando ou sequência exata que dispara o bug;
- [ ] Estado prévio necessário (dados, config, ambiente);
- [ ] Saída atual vs. saída esperada;
- [ ] Variações testadas que **não** reproduzem (ajuda a localizar).

Com repro mínimo, AI vira multiplicador. Sem ele, vira ruído.

### 2. O fluxo de 5 passos

**Passo 1. Triagem.** Descreva sintoma + repro ao AI. Peça hipóteses ordenadas por probabilidade, com justificativa.

> *"Endpoint GET /users retorna 500 intermitentemente (~10% requests) desde ontem 14h. Log mostra `connection pool timeout`. Repro: `ab -n 1000 -c 50 /users`. Liste 5 hipóteses ordenadas por probabilidade."*

**Passo 2. Priorizar por custo de verificação.** Das hipóteses do AI, qual é mais barata de confirmar/descartar? Nem sempre a mais provável, e sim a mais **barata de testar primeiro**.

**Passo 3. Instrumentação.** Pedir ao AI para gerar logs, métricas, traces que discriminem entre hipóteses. O AI é bom nisso: sugere pontos específicos do código onde instrumentar.

**Passo 4. Coletar evidência.** Rodar. Ler logs. Voltar ao AI com dados concretos, não impressões. *"Adicionei log antes e depois da query; em 47/500 requests a query demorou >5s. Hipótese 3 (query não indexada) fortalece. Verificar próximo?"*

**Passo 5. Consertar + regression test.** Quando causa-raiz identificada, AI escreve fix + teste que **falha sem o fix**. Esse é o critério: teste que não falharia sem o fix é inútil.

### 3. Onde o AI brilha no debug

- **Bisect assistido**: "entre commit A e B, qual comportamento mudou?";
- **Comparação de duas implementações**: "compare foo antigo e foo novo, aponte diferença comportamental";
- **Gerar hipóteses amplas**: rápido, sem viés de confirmação (bom contraponto ao instinto humano);
- **Instrumentação sob medida**: "adicione log estruturado nos 3 pontos críticos deste fluxo";
- **Ler stack trace longo**: resumir, mapear para arquivos, identificar frame relevante;
- **Propor regression test**: a partir de repro, escrever o teste que fixa;
- **Pesquisar padrão do erro**: "esse erro aparece quando X; veja se o código tem padrão X".

### 4. Onde o AI atrapalha

- **Racionalização a posteriori**: depois de 10 trocas, AI "confirma" hipóteses suas que são erradas. Desconfiar de concordância fácil;
- **Instinto de "consertar"**: AI sugere mudanças especulativas em 3 lugares quando bug está em 1. Pedir **apenas diagnóstico**, não fix, na fase de investigação;
- **Viés pelo último arquivo lido**: AI atribui causa ao código que está fresco no contexto;
- **Alucinação de comportamento**: "esta função deveria fazer X" sem verificar o que ela de fato faz. Exigir citação de código real;
- **Pular evidência contrária**: se dado coletado contradiz hipótese, o AI às vezes minimiza. Reler evidência sem o AI entre os passos.

### 5. Anti-padrão clássico: "shotgun debugging"

Pedir ao AI para tentar 5 mudanças ao mesmo tempo esperando que alguma conserte. Resultado típico: alguma conserta mas ninguém sabe qual nem por quê. Bug volta em forma diferente.

**Regra:** uma hipótese por vez. Uma mudança por vez. Verificação por vez.

### 6. Quando parar e chamar humano

- 3 ciclos sem progresso mensurável;
- AI está dando respostas circulares;
- Hipóteses se esgotaram (todas testadas, todas falsas);
- O bug tem correlação temporal (só em horário específico, tipicamente infraestrutura, não código);
- Envolve concorrência, rede, ou estado distribuído (ver Parte XIV).

Chamar humano = parar e mostrar o estado completo (repro, hipóteses testadas, evidência). AI é parte da ferramenta, não substituto de par humano.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte XXI — Custo e Economia do AI
<!--/PT-->
<!--EN-->
## Part XXI — Cost and Economics of AI
<!--/EN-->
<!--PT-->
AI assistants têm custo real. Em escala organizacional, essa conta importa: para decisão de adoção, alocação de budget e escolha de tier de modelo.

### 1. Onde o custo aparece

| Fonte | O que é | Como cresce |
|---|---|---|
| **Tokens de input** | Tudo que vai para o modelo: contexto, arquivos lidos, output de tools, histórico | Cresce com conversa longa, contexto amplo, tool calls ruidosas |
| **Tokens de output** | Tudo que o modelo gera: texto, código, chamadas de tool | Cresce com resposta longa, re-escrita, múltiplas iterações |
| **Tier de modelo** | Preço por milhão de tokens varia 10-20x entre tiers baixo e alto | Agents "alto" custam muito mais que "médio" |
| **Latência → produtividade** | Esperar 30s por resposta 10x/hora = 5min/hora parados | Latência alta indiretamente aumenta custo humano |
| **Retentativas** | Iterações para corrigir output ruim | Multiplicador de tudo acima |
| **Storage / retention** | Alguns provedores cobram por retenção longa | Baixo, mas não zero |

### 2. Tiers de modelo por tarefa (custo consciente)

Retomada da Parte IV.3, agora com foco em custo:

| Tier | Custo relativo | Use para |
|---|---|---|
| **Alto** | 10-20x o médio | Auditoria de segurança crítica, decisões arquiteturais, correlação complexa |
| **Médio** | Baseline | Default para quase tudo: código, review, planejamento, geração de testes |
| **Baixo** | 0.1-0.3x o médio | Formatação, extração, resumo, classificação |

**Regra:** rebaixar modelo até a qualidade cair. Aumentar só quando medido necessário. "Usar sempre o mais caro pra garantir" é desperdício.

### 3. Orçamento e atribuição

Em escala organizacional, custo precisa ser:

- **Observável**: dashboard com consumo por squad/projeto/semana;
- **Atribuível**: quem consumiu? Skills? Agents? Sessões longas?;
- **Orçado**: teto mensal por squad ou produto;
- **Alertável**: notificação ao ultrapassar 80% do budget.

**Padrões organizacionais:**

- **Budget por squad**: cada squad tem cota mensal; overflow requer justificativa;
- **Free tier para dev local + budget compartilhado para automação**: CI e agents em produção contam separado;
- **Modelos diferentes por ambiente**: dev pode usar modelo mais barato; PR review em CI usa o bom;
- **Soft limits + conversa**: primeiro mês é aprender; depois calibrar.

### 4. Quando upgrade de modelo paga

Upgrade de "médio" para "alto" custa ~10-20x. Paga se:

- Qualidade ruim está custando **retrabalho humano** (2h de dev > custo de token diferenciado);
- Decisões do output têm **consequência real** (security, arquitetura, compliance);
- A tarefa é **rara** mas importante (auditoria trimestral);
- Modelos "médios" falham consistentemente em benchmark do time.

**Não paga se:**

- Tarefa é repetitiva e alto volume (formatação, extração);
- Humano revisa o output mesmo assim (revisão já filtra qualidade);
- Gap de qualidade é marginal (<10% melhoria mensurada).

### 5. Padrões que reduzem custo sem perder qualidade

- **Context discipline** (Parte III): menos token de input, respostas mais focadas;
- **RPI com modelo misto**: research em modelo médio; plan em modelo alto; implement em médio;
- **Cache de contexto**: alguns provedores oferecem cache para prompts repetidos (skills, contexto file). Ativar quando disponível;
- **Tool call eficiente**: grep com filtro em vez de `cat` do arquivo inteiro;
- **Short-circuit**: primeiro passo do agent é validação barata; só roda análise cara se passar;
- **Batch quando possível**: um agent que revisa 5 arquivos uma vez é mais barato que 5 sessões.

### 6. Custo escondido: opcionalidade comprometida

Além do custo direto, há um custo estratégico: **lock-in**. Se todo o harness depende de um provedor específico:

- Migração para outro provedor é cara (prompts re-calibrados, agents re-testados);
- Aumento de preço do provedor é inelástico;
- Indisponibilidade do provedor paralisa o time.

**Mitigações:**

- Prompts e skills devem ser escritos em markdown agnóstico (não em formato proprietário);
- Evitar features específicas de um provedor quando alternativa padrão existe;
- Testar periodicamente o harness em provedor alternativo (mesmo que não migre);
- Registrar provedor como risco de concentração nos registros de risco de infraestrutura.

### 7. ROI: como justificar o investimento

Para gestão, o custo só faz sentido comparado ao retorno. Medidas úteis:

- **Tempo de ciclo** (idea → PR merged): comparar antes/depois;
- **Volume por dev** (PRs, linhas revisadas, specs aprovadas);
- **Qualidade** (reincidência de bug, hotfixes, tempo em incident);
- **Satisfação do time** (NPS interno).

Cuidado com métricas vanity: linhas de código geradas por AI não é indicador útil. Volume de trabalho **útil** entregue é.

### 8. Checklist de controle de custo

- [ ] Budget mensal por squad definido;
- [ ] Dashboard de consumo atualizado e monitorado;
- [ ] Tiers de modelo por tipo de tarefa documentados;
- [ ] Cache de contexto ativado onde disponível;
- [ ] Prompts e skills evitam dependência de features proprietárias;
- [ ] Revisão trimestral: custo vs. ROI;
- [ ] Plano B (provedor alternativo) testado periodicamente.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Parte XXII — Documentação Técnica e AI
<!--/PT-->
<!--EN-->
## Part XXII — Technical Documentation and AI
<!--/EN-->
<!--PT-->
Documentação é dos usos mais imediatamente úteis do AI: gera rápido, cobre volume. Também dos mais perigosos, porque produz material confiante que descola do código.

### 1. Onde AI ajuda em documentação

- **Changelogs** a partir de commits, transformando histórico técnico em voz do usuário;
- **README de módulo/pacote**: estrutura, exemplos, API reference a partir de código existente;
- **Docstrings**: preencher funções e classes com descrição + tipos + exemplos;
- **Runbooks operacionais**: passo a passo para incidentes, deploys, rollbacks;
- **Guias de onboarding**: versão compreensível de docs técnicas para dev novo;
- **Diagramas ASCII**: fluxos, arquitetura, sequência (rápido e editável);
- **Traduções**: EN ↔ PT ↔ ES preservando termos técnicos.

### 2. Onde AI atrapalha

- **Docs descoladas do código**: AI escreve "o que parece fazer" com base em nome e assinatura, não no que a função *faz*. Leia o código, confirme.
- **Exemplos inventados**: AI gera snippets que não rodam. Toda amostra de código em doc deve ser testada.
- **Verbosidade performática**: AI ama parágrafos explicativos. Doc técnica boa é curta. Peça para cortar 40%.
- **"Docs generated by AI" disclaimer**: desloca responsabilidade. Se está no repo, é sua doc. Assuma.
- **Doc em vez de código limpo**: "o código é confuso, vou escrever um doc explicando" é anti-padrão. Refatorar o código é quase sempre melhor que documentar a confusão.

### 3. Doc-as-code como princípio

Docs vivem **no repositório**, versionadas como o código, com o mesmo ciclo de PR/review. Consequências:

- Mudança de código + mudança de doc **no mesmo PR** (gate: reviewer bloqueia PR que muda comportamento sem atualizar doc);
- Exemplos em doc rodam em CI (doctest, scripts extraídos, validação de snippet);
- Linter de doc (formatação, links quebrados, frontmatter válido);
- Releases incluem doc do release (changelog + migration guide; ver Parte VII).

### 4. Hierarquia de docs

| Tipo | Audiência | Cadência | Vive em |
|---|---|---|---|
| **Inline (docstring, comentário)** | Dev lendo o código | Junto com código | Código fonte |
| **Module README** | Dev usando o módulo | Por release | Pasta do módulo |
| **Architecture / design doc** | Time | Decisão | `docs/adr/` ou `docs/design/` |
| **Runbook / operacional** | On-call, SRE | Atualizado após incidente | `docs/ops/` |
| **Onboarding / tutorial** | Dev novo | Trimestral | `docs/onboarding/` |
| **Changelog** | Usuário externo | Por release | `CHANGELOG.md` |
| **Migration guide** | Usuário fazendo upgrade | Por versão | `migrations/` |

Cada nível tem regras diferentes. AI ajuda em todos, mas as restrições mudam.

### 5. Workflow: atualizar doc quando o código muda

Padrão que funciona:

1. Dev faz mudança no código;
2. Agent detecta (via hook de pre-commit ou CI) que arquivos com docstring foram modificados;
3. Agent gera proposta de update para a doc afetada;
4. Dev revisa, ajusta, commita junto com o código.

Agent não deve commitar direto. Doc é decisão humana, como qualquer artefato distribuído (ver Parte VIII.1).

### 6. Anti-padrões específicos

- **Doc "completa" no dia 1, nunca atualizada depois.** Melhor doc curta e viva que doc longa e morta.
- **Copy-paste de comentário entre funções parecidas.** Cada função merece descrição precisa do que *ela* faz.
- **Comentário que parafraseia o código.** `// incrementa i em 1` para `i++` é ruído. Comentário deve dizer *por quê*, não *o quê*.
- **Doc técnica como produto de marketing.** Voz grandiloquente esconde detalhes que o dev precisa. Seja direto.

### 7. Checklist de doc no PR

- [ ] Docstrings das funções públicas modificadas atualizadas?
- [ ] README de módulo reflete mudanças visíveis?
- [ ] Changelog tem entrada se a mudança afeta usuário?
- [ ] Exemplos rodam (testados)?
- [ ] Links internos não quebraram?
- [ ] Se a mudança for breaking: migration guide criado?
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Apêndice A — Glossário
<!--/PT-->
<!--EN-->
## Appendix A — Glossary
<!--/EN-->
<!--PT-->
| Termo | Definição |
|---|---|
| **Agent / Sub-agent** | Sub-processo do AI despachado sob demanda para analisar algo e retornar relatório. Tipicamente read-only. |
| **Ambient authority** | AI opera com todas as permissões do dev que o invocou. Ruim por padrão; preferir confined. |
| **Backlog** | Documento canônico de itens pendentes, concluídos, descartados e adiados. |
| **Changelog** | Registro de mudanças escrito na voz do usuário final. |
| **Confined authority** | AI opera em sandbox com permissões mínimas e escopadas. Preferível. |
| **Context budget** | Espaço disponível na janela de contexto do AI; finito, precisa ser gerenciado. |
| **Context file** | Arquivo carregado automaticamente em cada sessão do AI, com convenções globais e mapa de skills/docs. |
| **Context reset** | Prática de começar nova sessão com contexto limpo após marco importante. |
| **Delta marker** | Anotação em spec brownfield: `[ADDED]`, `[MODIFIED]`, `[REMOVED]`. |
| **DoD (Definition of Done)** | Critérios objetivos que definem quando uma tarefa está pronta. Concretizado em `verify.sh`. |
| **Dual-mode** | Skill que funciona em mais de um meio (ex: arquivos locais ou ferramenta externa), com detecção automática. |
| **Fase (backlog)** | Agrupamento temático, não define ordem. |
| **Fast-path** | Fluxo simplificado para tarefas triviais (sem spec, sem plano, sem gates). |
| **Fail-soft / Fail-fast** | Script agregador continua após falha para reportar tudo (fail-soft); script de ação única para na primeira (fail-fast). |
| **Gate** | Ponto de verificação humana obrigatória entre fases. |
| **Harness** | Infraestrutura de contexto, skills, agents, verificação e memória que governa como um AI assistant opera num projeto. |
| **Item-spec** | Spec detalhada de um item de backlog complexo, com plano, contexto, critérios. |
| **Migration guide** | Documento auto-contido que permite a um usuário aplicar manualmente as mudanças entre duas versões. |
| **`[P]` (task marker)** | Indica task paralelizável; pode rodar concorrente com outras `[P]` da mesma wave. |
| **Plano de execução** | Quebra de uma spec em tasks ordenadas, com dependências e pontos de paralelização. |
| **Prompt injection** | Ataque onde input externo contém instruções que o AI poderia seguir indevidamente. |
| **RPI (Research, Plan, Implement)** | Padrão de três sessões isoladas para tarefas grandes. |
| **Skill / Playbook** | Documento markdown com checklist e padrões para um domínio específico ("como fazer X aqui"). |
| **Spec** | Documento formal definindo o que vai ser feito, por quê, critérios de aceitação. |
| **STATE.md** | Arquivo de continuidade entre sessões: status atual, próximas ações, blockers. |
| **Trust boundary** | Fronteira onde a responsabilidade por estado transita (AI → dev, dev → reviewer, etc.). |
| **Wave (backlog)** | Ordem de prioridade de execução, independente da fase. |
| **Worktree isolation** | Uso de `git worktree` para rodar sub-agentes em branch isolada, evitando contaminar working directory compartilhado. |
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Apêndice B — Checklists Compiladas
<!--/PT-->
<!--EN-->
## Appendix B — Compiled Checklists
<!--/EN-->
<!--PT-->
### B.1. Ao iniciar uma tarefa não-trivial

- [ ] Item existe no backlog? Se não, adicionar antes de começar.
- [ ] Spec existe e foi aprovada (para médio+)?
- [ ] Plano de execução existe (para médio+)?
- [ ] STATE anterior foi lido (se continuação)?
- [ ] Dependências do item estão concluídas?
- [ ] Skills relevantes foram consultadas?

### B.2. Ao finalizar uma tarefa

- [ ] Source e distribuído em sincronia (se aplicável);
- [ ] Manifest atualizado;
- [ ] Setup e update cobertos (se aplicável);
- [ ] Dual-mode coberto (se aplicável);
- [ ] Docs atualizadas (skills-map, workflow, contexto principal);
- [ ] Testes passam (`verify.sh`);
- [ ] Linter limpo;
- [ ] Critérios de aceitação verificados;
- [ ] STATE.md atualizado (se continuação);
- [ ] Item movido para "Concluídos" no backlog.

### B.3. Ao criar um agent novo

- [ ] Frontmatter completo (`description`, `model`, `worktree`, `model-rationale`);
- [ ] Seções obrigatórias: Quando usar, Input, O que verificar, Output, Regras;
- [ ] Severidades padrão no output (🔴🟠🟡⚪);
- [ ] Seção "Próximos passos" linkando para skills relacionadas;
- [ ] Entrada no manifest;
- [ ] Referência no mapa de agents do contexto principal.

### B.4. Ao criar uma skill nova

- [ ] Seções obrigatórias: Quando usar, Quando NÃO usar, Checklist, Padrões, Quando escalar;
- [ ] Pelo menos um exemplo concreto por seção (não só placeholders);
- [ ] Dependências declaradas no topo (se depende de outra skill);
- [ ] Entrada no manifest;
- [ ] Referência no mapa de skills do contexto principal.

### B.5. Ao abrir um PR

- [ ] Branch dedicada (nunca commit direto em main);
- [ ] Sub-agentes que editaram rodaram em worktree isolada;
- [ ] Commits atômicos (um motivo por commit);
- [ ] Commits seguem Conventional Commits;
- [ ] Validações locais passaram (`verify.sh`);
- [ ] PR description descreve o quê e por quê, linka spec;
- [ ] Critérios de aceitação marcados como validados;
- [ ] Checklist de segurança (B.7) passou;
- [ ] CI verde antes do merge.

### B.6. Ao fazer release

**Pré-release:**
- [ ] Working directory limpo;
- [ ] Source ↔ distribuído sincronizado;
- [ ] Manifest atualizado;
- [ ] Changelog atualizado (só mudanças que chegam ao usuário);
- [ ] Tags de versão consistentes;
- [ ] Testes e validações passam.

**Pós-release:**
- [ ] Arquivo de versão atualizado;
- [ ] Manifests de plugin/pacote com mesma versão;
- [ ] Changelog com entrada;
- [ ] Migration guide criado;
- [ ] Tag criada no git;
- [ ] Backlog: "pendente release" → versão real;
- [ ] Teste em ambiente real pós-publicação.

### B.7. Checklist de segurança por PR

- [ ] Nenhum secret hardcoded (scanner passou);
- [ ] Nenhuma query construída com string concat (SQL injection);
- [ ] Input de usuário validado e sanitizado;
- [ ] Output em HTML/JSX escapado (XSS);
- [ ] Path de arquivo validado contra traversal (`..`);
- [ ] Autenticação e autorização nos endpoints novos;
- [ ] Dependências novas auditadas;
- [ ] Logs não registram dados sensíveis (senha, token, PII).

### B.8. Ao auditar código ou documentação

- [ ] Leu anti-padrões registrados antes de começar;
- [ ] Para cada achado: aplicou teste do "segundo arquivo"?;
- [ ] Achados classificados por severidade padrão;
- [ ] Falsos positivos novos registrados em anti-padrões;
- [ ] Próximos passos indicam skill ou agent para correção.

### B.9. Ao encerrar uma sessão grande

- [ ] STATE.md atualizado com: status, próxima ação, blockers;
- [ ] Commits atômicos feitos (não deixar mudanças órfãs);
- [ ] Descobertas que merecem spec própria foram registradas no backlog;
- [ ] Decisões descartadas foram registradas com motivo.

### B.10. Revisão trimestral do harness

- [ ] Revisar indicadores de saúde (Parte XVII): algum piorou?;
- [ ] Pesquisa qualitativa com o time: tema recorrente?;
- [ ] Skills não usadas em 6+ meses: arquivar ou consolidar?;
- [ ] Skills com alta sobreposição: mesclar?;
- [ ] Contexto principal > 600 linhas? Podar;
- [ ] Docs órfãs: linkar ou remover;
- [ ] Anti-padrões resolvidos: mover para histórico;
- [ ] Backlog do harness priorizado para o próximo trimestre.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Apêndice C — Templates de Referência
<!--/PT-->
<!--EN-->
## Appendix C — Reference Templates
<!--/EN-->
<!--PT-->
Boilerplate pronto para copiar/colar e adaptar. Cada template é ponto de partida: adapte ao contexto, não copie cego.

### C.1. Template de skill

````markdown
# {Nome da skill}

## Quando usar
- {Contexto 1}
- {Contexto 2}

## Quando NÃO usar
- {Quando outra skill serve melhor}

## Checklist
- [ ] {Verificação 1}
- [ ] {Verificação 2}
- [ ] {Verificação 3}

## Padrões

### Exemplo concreto
✅ **Correto:**
```{linguagem}
// código que exemplifica a boa prática
```

❌ **Errado:**
```{linguagem}
// código que exemplifica o que evitar
```

## Quando escalar
- Se {condição crítica} → acionar {skill/agent/humano}
````

### C.2. Template de agent

````markdown
---
description: {uma frase do que o agent faz}
model: {alto | médio | baixo}
worktree: false
model-rationale: {uma frase justificando a escolha do modelo}
---

# {Nome do agent}

## Quando usar
{Contextos em que invocar}

## Input
{O que o agent recebe: escopo, parâmetros, formato}

## O que verificar
1. {Check 1}
2. {Check 2}
3. {Check 3}

## Output
Formato do relatório:

### Status: PASS | FAIL | PARTIAL

### Findings

#### 🔴 Crítico
- {finding}

#### 🟠 Alto
- {finding}

#### 🟡 Médio
- {finding}

#### ⚪ Info
- {finding}

### Próximos passos
- Para corrigir: use skill `{nome}` ou agent `{nome}`

## Regras
- {Restrição 1}
- {Restrição 2}
````

### C.3. Template de spec

````markdown
# Spec {ID}: {Título}

**Status:** rascunho

## Contexto
{Por que esta spec existe, qual problema resolve — 3-5 frases.}

## Dependências
- {Spec ou componente de que depende}

## Requisitos Funcionais
- RF-001: {requisito verificável}
- RF-002: {requisito verificável}

## Escopo
- [ ] {Entregável 1}
- [ ] {Entregável 2}

## Critérios de Aceitação
- Dado {pré-condição}, quando {ação}, então {resultado observável}
- {Critério 2}

## Arquivos Afetados
- `path/file1.ext`: {modificar | criar | remover}
- `path/file2.ext`: {modificar | criar | remover}

## Não Fazer
- {Fora do escopo 1}

## Skills a consultar
- {skill1}

## Verificação pós-implementação
- [ ] Testes passam (verify.sh)
- [ ] Critérios de aceitação validados
- [ ] Docs atualizadas se necessário
````

### C.4. Template de plano de execução

````markdown
# Plano: Spec {ID}

**Spec:** [{ID}](../specs/{ID}.md)
**Estimativa total:** {horas/dias}

## Pré-requisitos
- [ ] Spec aprovada
- [ ] Dependências concluídas

## Tasks

### Wave 1
- [ ] T1: {descrição} — `{arquivos}` — {estimativa}
- [ ] T2 [P]: {descrição} — `{arquivos}` — {estimativa}

### Wave 2 (depende de Wave 1)
- [ ] T3: {descrição} — depende de T1
- [ ] T4 [P]: {descrição} — depende de T1

### Wave 3 (verificação)
- [ ] T5: rodar verify.sh
- [ ] T6: atualizar docs afetadas

## Riscos e mitigações
- {Risco}: {mitigação}

## Gates
- Após Wave 1: revisão humana antes de seguir
- Após Wave 2: code review no PR
````

### C.5. Template de STATE.md

````markdown
# STATE — {spec-id ou task-id}

**Atualizado:** {AAAA-MM-DD HH:MM}

## Status
{1-2 frases sobre onde estou}

## Contexto carregado
- Spec: `{path}`
- Plano: `{path}`
- Docs relevantes: `{path}`

## O que foi feito
- T1: {descrição} ✅ (commit {sha})
- T2: {descrição} ✅ (commit {sha})

## O que falta
- T3: {descrição} (em andamento)
- T4: {descrição}

## Próxima ação
{Instrução concreta para retomar, com referência a arquivo:linha se aplicável}

## Blockers / decisões pendentes
- {Questão aberta + contexto + quem precisa responder}

## Notas
- {Contexto descoberto útil para retomar}
````

### C.6. Template de migration guide

````markdown
# Migration: v{FROM} → v{TO}

**Resumo:** {1-3 frases sobre o que mudou e por quê}

**Pré-requisitos:**
- Estar na versão v{FROM}
- Ter aplicado migrations anteriores

---

## Arquivos substituídos (overwrite)

### `{path}`
**O que mudou:** {resumo}
**Como aplicar:** substituir o arquivo pelo novo.
**Impacto:** {nenhum | comportamento X difere}

---

## Mudanças estruturais (structural)

### `{path}`
**Seções adicionadas:** `## Nova Seção A`, `## Nova Seção B`
**Seções removidas:** `## Antiga Seção`
**Impacto:** {descrição}

---

## Patches de conteúdo (manual)

### `{path}` — seção `## X`
**Motivo:** {por que mudou}
**Texto antigo:**
> {trecho}

**Texto novo:**
> {trecho completo}

**Impacto:** {descrição}

---

## Decisões manuais (manual)

### `{path}`
**Diff:**
```diff
- linha antiga
+ linha nova
```
**Sugestão:** {o que o usuário deve considerar antes de aplicar}

---

## Arquivos novos

### `{path}`
**Propósito:** {o que é}
**Quando é relevante:** {contextos}

---

## Arquivos removidos

### `{path}`
**Motivo:** {por que saiu}
**Substituto:** `{novo path ou "nenhum"}`
````

### C.7. Template de entrada de changelog

````markdown
## [vX.Y.Z] — AAAA-MM-DD

### Added
- {Feature visível ao usuário} (#PR)

### Changed
- {Mudança de comportamento visível} (#PR)

### Fixed
- {Bug corrigido que afetava usuário} (#PR)

### Removed
- {Feature removida + substituto se houver} (#PR)

### Security
- {Correção de vulnerabilidade} (#PR)

### Migration
Ver [migrations/v{ANTERIOR}-to-v{NOVA}.md](migrations/v{ANTERIOR}-to-v{NOVA}.md).
````

### C.8. Template de prompt (anatomia mínima)

```
Contexto: {onde estou, o que é o projeto — 1-2 frases}

Objetivo: {o que quero, verificável — 1 frase}

Restrições:
- {o que NÃO fazer}
- {outras restrições}

Formato esperado: {estrutura da resposta}
```

---

*Este handbook é um destilado de práticas. Adapte ao seu contexto: princípios valem mais que regras literais.*
<!--/PT-->
<!--EN-->
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
<!--/EN-->

