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
