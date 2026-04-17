# Handbook de Harness Engineering

> Um guia prático para times de engenharia, tecnologia e organizações que querem usar AI coding assistants em projetos reais e em escala, não como autocomplete sofisticado, mas como parte do processo de desenvolvimento.

---

## Sumário

- [Introdução](#introdução)
- [Parte I — Fundamentos](#parte-i--fundamentos)
- [Parte II — Context Engineering](#parte-ii--context-engineering)
- [Parte III — Orquestração: Budget, Sessões e Continuidade](#parte-iii--orquestração-budget-sessões-e-continuidade)
- [Parte IV — Skills e Agents](#parte-iv--skills-e-agents)
- [Parte V — Spec-driven Development](#parte-v--spec-driven-development)
- [Parte VI — Backlog como Single Source of Truth](#parte-vi--backlog-como-single-source-of-truth)
- [Parte VII — Versionamento, Releases e Migrações](#parte-vii--versionamento-releases-e-migrações)
- [Parte VIII — Distribuição e Compatibilidade](#parte-viii--distribuição-e-compatibilidade)
- [Parte IX — Dual-mode](#parte-ix--dual-mode)
- [Parte X — Qualidade, Verificação e Auditorias](#parte-x--qualidade-verificação-e-auditorias)
- [Parte XI — Segurança em Harness de AI](#parte-xi--segurança-em-harness-de-ai)
- [Parte XII — Princípios Transversais](#parte-xii--princípios-transversais)
- [Parte XIII — Anti-padrões do Desenvolvedor Usando AI](#parte-xiii--anti-padrões-do-desenvolvedor-usando-ai)
- [Parte XIV — Quando NÃO Usar AI Assistant](#parte-xiv--quando-não-usar-ai-assistant)
- [Parte XV — Governança e Evolução do Harness](#parte-xv--governança-e-evolução-do-harness)
- [Parte XVI — Adoção: Do Zero ao Maduro](#parte-xvi--adoção-do-zero-ao-maduro)
- [Parte XVII — Métricas de Saúde do Harness](#parte-xvii--métricas-de-saúde-do-harness)
- [Parte XVIII — Onboarding Humano ao Harness](#parte-xviii--onboarding-humano-ao-harness)
- [Parte XIX — Anatomia de um Bom Prompt](#parte-xix--anatomia-de-um-bom-prompt)
- [Parte XX — Debug Workflow com AI](#parte-xx--debug-workflow-com-ai)
- [Parte XXI — Custo e Economia do AI](#parte-xxi--custo-e-economia-do-ai)
- [Parte XXII — Documentação Técnica e AI](#parte-xxii--documentação-técnica-e-ai)
- [Apêndice A — Glossário](#apêndice-a--glossário)
- [Apêndice B — Checklists compiladas](#apêndice-b--checklists-compiladas)
- [Apêndice C — Templates de Referência](#apêndice-c--templates-de-referência)

---

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

---

## Parte I — Fundamentos

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

---

## Parte II — Context Engineering

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

---

## Parte III — Orquestração: Budget, Sessões e Continuidade

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

---

## Parte IV — Skills e Agents

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

## Parte XII — Princípios Transversais

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

---

## Parte XIII — Anti-padrões do Desenvolvedor Usando AI

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

---

## Parte XIV — Quando NÃO Usar AI Assistant

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

---

## Parte XV — Governança e Evolução do Harness

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

---

## Parte XVI — Adoção: Do Zero ao Maduro

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

---

## Parte XVII — Métricas de Saúde do Harness

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

---

## Parte XVIII — Onboarding Humano ao Harness

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

---

## Parte XIX — Anatomia de um Bom Prompt

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

---

## Parte XX — Debug Workflow com AI

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

---

## Parte XXI — Custo e Economia do AI

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

---

## Parte XXII — Documentação Técnica e AI

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

---

## Apêndice A — Glossário

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

---

## Apêndice B — Checklists Compiladas

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

---

## Apêndice C — Templates de Referência

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
