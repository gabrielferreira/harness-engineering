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
