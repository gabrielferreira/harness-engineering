<!--PT-->
# Manifesto de Harness Engineering

AI coding assistants entregam o que se pede. O problema raramente é o modelo. É a ausência de infraestrutura que diga onde ele está, o que o time valoriza, e como o trabalho é avaliado.

**Harness é essa infraestrutura.** Este documento declara como pensamos sobre ela.
<!--/PT-->
<!--EN-->
# Harness Engineering Manifesto

AI coding assistants deliver what you ask for. The problem is rarely the model. It is the absence of infrastructure that tells it where it stands, what the team values, and how the work is judged.

**Harness is that infrastructure.** This document declares how we think about it.
<!--/EN-->

---

<!--PT-->
## O que valorizamos

Reconhecemos valor em ambos os lados, mas quando há tensão, preferimos o primeiro.

- **Contexto explícito** sobre intuição implícita.
- **Arquivos persistidos** sobre conversas efêmeras.
- **Revisão humana entre fases** sobre autonomia irrestrita.
- **Verificação automatizada** sobre convenção apenas escrita.
- **Simplicidade concreta** sobre abstração prematura.
- **Diretrizes compartilhadas** sobre preferências individuais.
- **Cerimônia proporcional** sobre processo uniforme.
- **Compatibilidade declarada** sobre compatibilidade acidental.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Princípios

### 1. O AI é colaborador, não oráculo

Tratamos o assistant como um colega novo: acelerado, mas que precisa de onboarding, convenções, revisão e limites. Não como uma inteligência que acerta por magia.

### 2. Harness é infraestrutura, não otimização

Não é um ajuste para ganhar 10% de velocidade. É a camada que determina se o AI ajuda ou atrapalha. Sem harness, produtividade aparente vira débito silencioso.

### 3. Contexto tem custo: referenciamos em vez de inlinar

Mais contexto não é melhor contexto. Regras globais entram no onboarding automático; profundidade é carregada sob demanda. Menos barulho, mais sinal.

### 4. Toda decisão importante vira arquivo versionado

Conversas somem. Commits, specs, planos e migrations sobrevivem ao refresh da sessão, à troca de membro, à migração de ferramenta.

### 5. Gates explícitos protegem do arrasto silencioso

Humanos aprovam transições críticas: spec → plano, plano → código, código → merge. Automação faz o repetitivo; julgamento é humano.

### 6. Skills informam, agents verificam, humanos julgam

Skills são checklists antes de agir. Agents são auditores read-only depois de agir. O merge é sempre decisão humana.

### 7. Cerimônia é proporcional à complexidade, nunca uniforme

Typo não precisa de spec. Feature grande sem spec não começa. Processo pesado em tarefa leve é tão ruim quanto ausência de processo em tarefa grande.

### 8. Registrar o descartado importa tanto quanto registrar o feito

Decisões descartadas, ideias adiadas e anti-padrões registrados impedem a organização de refazer a mesma discussão. Memória institucional é ativo.

### 9. Nenhuma regra sobrevive sem verificação automatizada

Convenção que não é check no `verify.sh` é convenção que vai ser violada. Se importa, precisa falhar o build quando quebrada.

### 10. Três casos concretos antes de abstrair

Repetição explícita é melhor que abstração errada. Abstração desfazer custa mais que copy-paste limpar.

### 11. Compatibilidade é escolha explícita, não acidente

Todo artefato distribuído declara como evolui: aditivo, migrável ou breaking. Projetos antigos continuam funcionando até que a migração seja oferecida. Nunca são sabotados.

### 12. Segurança é parte do design, não adendo

Allowlists de paths e comandos, inputs externos como dados (não instruções), pre-commit hooks, code review obrigatório antes de merge. O AI é colaborador externo: recebe só o que precisa.

### 13. Simplicidade é a regra; complexidade precisa se justificar

Markdown antes de banco de dados. Script antes de framework. Arquivo antes de SaaS. Se o repo compila, o harness funciona.

### 14. Harness é software vivo: apodrece sem poda

Skills não usadas, regras que ninguém segue, docs órfãs: revisamos e removemos. Manter o essencial vale mais do que acumular o completo.

### 15. Medir antes de opinar sobre estar funcionando

Reincidência, rework, cobertura, tempo até o primeiro gate. Sem métrica, *"o harness está bom"* é sentimento. Com métrica, é trabalho.

### 16. O que o AI não faz bem, delegamos ao humano

Debug sutil, decisão arquitetural nova, incidente crítico, código regulado sem spec. Harness maduro conhece os limites do AI e os respeita.
<!--/PT-->
<!--EN-->
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
<!--/EN-->

---

<!--PT-->
## Compromissos

Quem adota este manifesto se compromete a:

- **Ler o contexto** antes de pedir ao AI;
- **Escrever spec** antes de codar o que não é trivial;
- **Registrar o descartado** junto com o feito;
- **Transformar cada regra importante em verificação executável**;
- **Revisar, podar e evoluir o harness continuamente**;
- **Onboardar pessoas**, não só ferramentas.
<!--/PT-->
<!--EN-->
## Commitments

Whoever adopts this manifesto commits to:

- **Reading the context** before asking the AI;
- **Writing a spec** before coding anything non-trivial;
- **Recording what was discarded** alongside what was done;
- **Turning every important rule into an executable check**;
- **Reviewing, pruning, and evolving the harness continuously**;
- **Onboarding people**, not just tools.
<!--/EN-->

---

<!--PT-->
*Adapte ao seu contexto. Princípios valem mais que regras literais.*
<!--/PT-->
<!--EN-->
*Adapt it to your context. Principles outweigh literal rules.*
<!--/EN-->
