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
