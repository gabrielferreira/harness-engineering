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
