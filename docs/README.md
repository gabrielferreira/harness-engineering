<!--PT-->
# Harness Engineering: Handbook

> Como times de engenharia e organizações de tecnologia podem usar **AI coding assistants** (Claude Code, Cursor, GitHub Copilot, Continue, Aider, Windsurf, Cline) em projetos reais e em escala. Não como autocomplete sofisticado, mas como parte do processo de desenvolvimento.

> *Harness engineering: the discipline of configuring the context, rules, skills, and verification tooling an AI coding assistant needs to operate well in a real project.*

## Por onde começar

Dois documentos complementares, do mais curto ao mais extenso:

- **[Manifesto](./MANIFESTO.md)**: uma página com os princípios destilados (16 princípios + 6 compromissos). Comece aqui se quer entender a filosofia antes de mergulhar.
- **[Handbook](./HANDBOOK.md)**: o guia completo (22 partes + 3 apêndices) com práticas detalhadas, exemplos, templates e checklists.

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

## Versão em inglês

O [Manifesto](./MANIFESTO.md) e o [Handbook](./HANDBOOK.md) estão totalmente bilíngues (PT/EN) usando marcadores `<!--PT-->` / `<!--EN-->` no mesmo arquivo. No site, o toggle no topo alterna entre os idiomas; no GitHub, ambos aparecem em sequência.

## Licença

Este handbook é licenciado sob [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Você pode compartilhar e adaptar livremente, desde que dê crédito apropriado.

Ver [LICENSE](./LICENSE) para detalhes.

## Contribuições

Sugestões, correções e experiências do campo são bem-vindas via issue ou pull request. O handbook é um destilado de práticas, evolui com o uso real.
<!--/PT-->
<!--EN-->
# Harness Engineering: Handbook

> How engineering teams and technology organizations can use **AI coding assistants** (Claude Code, Cursor, GitHub Copilot, Continue, Aider, Windsurf, Cline) on real projects at scale. Not as fancy autocomplete, but as part of the development process.

> *Harness engineering: the discipline of configuring the context, rules, skills, and verification tooling an AI coding assistant needs to operate well in a real project.*

## Where to start

Two complementary documents, from shortest to most extensive:

- **[Manifesto](./MANIFESTO.md)**: a single page with the distilled principles (16 principles + 6 commitments). Start here if you want to grasp the philosophy before diving in.
- **[Handbook](./HANDBOOK.md)**: the full guide (22 parts + 3 appendices) with detailed practices, examples, templates, and checklists.

## What harness engineering is

**Harness engineering** is the discipline of configuring the instructions, constraints, and tools an AI coding assistant needs to operate with quality in a real project. It is what stops the AI from inventing APIs, ignoring team conventions, producing code that passes lint but breaks business rules, or causing silent debt.

A mature harness organizes the assistant's intelligence into six complementary layers:

1. **Knowledge**: specs, backlog, project context;
2. **Expertise**: domain checklists (skills);
3. **Automation**: read-only sub-agents on demand (agents);
4. **Orchestration**: phase sequencing, context budget, isolated sessions;
5. **Verification**: executable scripts, definition of done;
6. **Continuity**: persistent context files, state across sessions.

**Tool-agnostic:** the principles apply to any AI coding assistant — Claude Code, Cursor, GitHub Copilot, Continue, Aider, Windsurf, Cline, or combinations.

## Related topics the handbook connects

Content often treated separately, gathered here into a single conceptual map:

- **AI coding assistant best practices**: what, when, and how to use them;
- **Context engineering**: how to build the right context for an LLM;
- **Prompt engineering for code**: anatomy of useful prompts, by intent;
- **Spec-driven development**: the idea → backlog → spec → plan → code flow;
- **Agentic coding**: using sub-agents, orchestrating phases (Research → Plan → Implement);
- **AI governance in engineering**: ownership, security, compliance, cost, ROI;
- **Onboarding and adoption**: an incremental roadmap from zero to mature.

## What the handbook covers

- **Foundations**: the six harness layers, design principles, minimal vocabulary;
- **Context engineering**: context hierarchy, on-demand imports, portable context;
- **Orchestration**: context budget, isolated sessions (RPI: Research/Plan/Implement), cross-session continuity (the STATE.md pattern);
- **Skills and agents**: domain playbooks vs. read-only sub-agents, model choice;
- **Spec-driven development**: proportional ceremony, gates, fast-path, TDD, test strategy;
- **Backlog as single source of truth**: taxonomy, Phase vs. Wave, the no-delete rule;
- **Versioning and releases**: Conventional Commits, atomic commits, migrations;
- **Distribution and compatibility**: merge strategies (overwrite/structural/manual/skip), version tags, 3 mandatory scenarios;
- **Dual-mode**: artifacts in the repo and in an external tool (Notion, Linear, Jira) with automatic detection;
- **Quality, verification, and audits**: task checklist, executable DoD, the "second file" test, code review of AI-generated code;
- **Security in AI harnesses**: prompt injection, ambient vs. confined authority, IP and licenses, compliance (GDPR, LGPD, HIPAA, PCI);
- **Cross-cutting principles**: simplicity, human review, explicit trust boundaries;
- **Developer anti-patterns when using AI**: common errors that come from the dev, not the model;
- **When NOT to use AI**: explicit limits;
- **Governance and evolution**: ownership, pruning, migration between model versions;
- **Adoption and onboarding**: maturity tiers, when NOT to adopt a harness, how team roles change (junior, mid, senior, tech lead);
- **Health metrics**: quantitative and qualitative indicators;
- **Anatomy of a good prompt**: three intents, minimum structure, constructive mistakes;
- **Debug workflow with AI**: 5-step flow, where AI shines, where it gets in the way;
- **Cost and economics**: model tiers per task, budgeting, ROI, lock-in;
- **Technical documentation and AI**: doc-as-code, doc hierarchy, anti-patterns.

Each section stands on its own. Read it linearly once for the mental map, then consult specific sections as needed.

## Who it is for

- Senior engineers and architects;
- Tech leads standardizing AI use across squads;
- Engineering managers calibrating expectations, quality, and velocity;
- Platform engineering teams offering AI as an internal product;
- CTOs and VPs of Engineering setting org-wide direction.

## Bilingual format

Both the [Manifesto](./MANIFESTO.md) and the [Handbook](./HANDBOOK.md) are fully bilingual (PT/EN) using `<!--PT-->` / `<!--EN-->` markers in the same file. On the site, the toggle at the top switches languages; on GitHub, both appear sequentially.

## License

This handbook is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You can share and adapt freely, as long as you give appropriate credit.

See [LICENSE](./LICENSE) for details.

## Contributions

Suggestions, corrections, and field experiences are welcome via issue or pull request. The handbook is a distillation of practices and evolves with real use.
<!--/EN-->
