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
