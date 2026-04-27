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
