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

