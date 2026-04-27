[English](README.md) · **Português**

---

# Harness Engineering: Handbook

> Como times de engenharia e organizações de tecnologia podem usar **AI coding assistants** (Claude Code, Cursor, GitHub Copilot, Continue, Aider, Windsurf, Cline) em projetos reais e em escala. Não como autocomplete sofisticado, mas como parte do processo de desenvolvimento.

> *Harness engineering: the discipline of configuring the context, rules, skills, and verification tooling an AI coding assistant needs to operate well in a real project.*

## Por onde começar

Dois documentos complementares, do mais curto ao mais extenso:

- **[Manifesto](./MANIFESTO.pt.md)**: uma página com os princípios destilados (16 princípios + 6 compromissos). Comece aqui se quer entender a filosofia antes de mergulhar.
- **[Handbook](./HANDBOOK.pt.md)**: o guia completo (22 partes + 3 apêndices) com práticas detalhadas, exemplos, templates e checklists.

## O que é harness engineering

**Harness engineering** é a disciplina de configurar as instruções, restrições e ferramentas que um AI coding assistant precisa para operar com qualidade num projeto real. É o que impede que o AI invente APIs, desrespeite convenções do time, gere código que passa no lint mas quebra regra de negócio, ou cause débito silencioso.

Um harness maduro organiza a inteligência do assistant em seis camadas complementares:

1. **Conhecimento**: specs, backlog, contexto do projeto;
2. **Expertise**: checklists por domínio (skills);
3. **Automação**: sub-agentes read-only sob demanda (agents);
4. **Orquestração**: sequenciamento de fases, budget de contexto, sessões isoladas;
5. **Verificação**: scripts executáveis, definition of done;
6. **Continuidade**: arquivos de contexto persistentes, estado entre sessões.

**Agnóstico a ferramenta:** os princípios aplicam-se a qualquer AI coding assistant: Claude Code, Cursor, GitHub Copilot, Continue, Aider, Windsurf, Cline, ou combinações.

## Tópicos relacionados que o handbook conecta

Conteúdos frequentemente tratados em separado, reunidos aqui num só mapa conceitual:

- **AI coding assistant best practices**: o quê, quando, como usar;
- **Context engineering**: como construir o contexto certo para um LLM;
- **Prompt engineering para código**: anatomia de prompts úteis, por intenção;
- **Spec-driven development**: fluxo ideia → backlog → spec → plano → código;
- **Agentic coding**: uso de sub-agentes, orquestração de fases (Research → Plan → Implement);
- **AI governance em engenharia**: ownership, segurança, compliance, custo, ROI;
- **Onboarding e adoção**: roadmap incremental do zero ao maduro.

## O que o handbook cobre

- **Fundamentos**: as seis camadas do harness, princípios de design, vocabulário mínimo;
- **Context engineering**: hierarquia de contexto, import sob demanda, contexto portátil;
- **Orquestração**: context budget, sessões isoladas (RPI: Research/Plan/Implement), continuidade entre sessões (padrão STATE.md);
- **Skills e agents**: playbooks por domínio vs. sub-agentes read-only, escolha de modelo;
- **Spec-driven development**: cerimônia proporcional, gates, fast-path, TDD, estratégia de testes;
- **Backlog como single source of truth**: taxonomia, Fase vs. Wave, regra de não deletar;
- **Versionamento e releases**: Conventional Commits, commits atômicos, migrations;
- **Distribuição e compatibilidade**: estratégias de merge (overwrite/structural/manual/skip), tags de versão, 3 cenários obrigatórios;
- **Dual-mode**: artefatos em repo e ferramenta externa (Notion, Linear, Jira) com detecção automática;
- **Qualidade, verificação e auditorias**: task checklist, DoD executável, teste do "segundo arquivo", code review de código gerado por AI;
- **Segurança em harness de AI**: prompt injection, ambient vs. confined authority, IP e licenças, compliance (GDPR, LGPD, HIPAA, PCI);
- **Princípios transversais**: simplicidade, revisão humana, trust boundaries explícitos;
- **Anti-padrões do desenvolvedor usando AI**: erros comuns que são do dev, não do modelo;
- **Quando NÃO usar AI**: limites explícitos;
- **Governança e evolução**: ownership, poda, migração entre versões de modelo;
- **Adoção e onboarding**: tiers de maturidade, quando NÃO adotar harness, como os papéis no time mudam (júnior, pleno, sênior, tech lead);
- **Métricas de saúde**: indicadores quantitativos e qualitativos;
- **Anatomia de um bom prompt**: três intenções, estrutura mínima, erros construtivos;
- **Debug workflow com AI**: fluxo de 5 passos, onde o AI brilha, onde atrapalha;
- **Custo e economia**: tiers de modelo por tarefa, budget, ROI, lock-in;
- **Documentação técnica e AI**: doc-as-code, hierarquia de docs, anti-padrões.

Cada seção é independente. Leia linearmente uma vez para ter o mapa mental, depois consulte pontualmente.

## Para quem é

- Engenheiros seniores e arquitetos;
- Tech leads que padronizam uso de AI entre squads;
- Managers de engenharia calibrando expectativa, qualidade e velocidade;
- Platform engineering que oferece AI como produto interno;
- CTOs e VPs Engineering decidindo diretrizes organizacionais.

## Em outro idioma

O repo mantém arquivos por idioma na raiz para leitura limpa no GitHub:

- **Português** (este arquivo): [Manifesto](./MANIFESTO.pt.md) · [Handbook](./HANDBOOK.pt.md)
- **[English](./README.md)**: [Manifesto](./MANIFESTO.md) · [Handbook](./HANDBOOK.md)

O site em `docs/a-newsprint/` mantém um único `HANDBOOK.md` bilíngue filtrado em runtime por JS; os arquivos `HANDBOOK.md` e `HANDBOOK.pt.md` na raiz são regenerados a partir dele com `scripts/sync-handbook.sh`.

## Licença

Este handbook é licenciado sob [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Você pode compartilhar e adaptar livremente, desde que dê crédito apropriado.

Ver [LICENSE](./LICENSE) para detalhes.

## Contribuições

Sugestões, correções e experiências do campo são bem-vindas via issue ou pull request. O handbook é um destilado de práticas, evolui com o uso real.
