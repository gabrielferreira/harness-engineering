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
