## Parte XIV — Quando NÃO Usar AI Assistant

Harness maduro sabe os limites. Usar AI onde ele é ruim é pior que não usar.

### 1. Debug de concorrência sutil

Race conditions, deadlocks, inconsistência de estado distribuído exigem raciocínio não-linear, hipóteses contra-intuitivas e frequentemente experimentação física (profilers, trace, logs de produção). AI **acelera** mapeamento de hipóteses, mas o salto de insight costuma ser humano.

**Uso recomendado:** AI ajuda a estruturar hipóteses e gerar logs de instrumentação. Humano interpreta.

### 2. Decisões arquiteturais novas

"Devemos adotar event sourcing?" depende de: time, skills internas, pressão de produto, infraestrutura, histórico de incidentes. AI não tem esse contexto; dá resposta estatisticamente plausível, não boa.

**Uso recomendado:** AI rascunha ADR com trade-offs conhecidos. Decisão humana.

### 3. Código regulado sem spec clara

GDPR, LGPD, PCI, HIPAA, SOX: áreas onde "parece certo" não basta. Exige rastreabilidade de requisito-regulatório → código → teste → auditoria.

**Uso recomendado:** só com spec regulatória formal e code review especializado. Sem spec, não tocar.

### 4. Incidentes críticos em produção

Pressão de tempo + escopo amplo + stakeholders + decisões reversíveis rapidamente. AI introduz variância quando você precisa de determinismo e familiaridade.

**Uso recomendado:** durante incidente, usar AI apenas para queries paralelas rápidas (ler log, extrair timeline). Commits de fix emergenciais: humano.

### 5. Refatoração gigante sem testes

Sem suíte de testes, o AI voa às cegas. Vai gerar código que parece correto, quebra feature sutil, ninguém percebe até semanas depois.

**Uso recomendado:** primeiro, escrever testes (aí sim o AI ajuda). Depois, refatorar.

### 6. Domínio muito novo ou obscuro

Em stacks/bibliotecas que saíram recentemente ou são nicho, o AI confabula mais. Inventa APIs plausíveis que não existem.

**Uso recomendado:** verificar cada função chamada contra a documentação oficial. Se o custo de verificação > custo de escrever à mão, não usar AI nessa parte.

### 7. Tarefas com requisitos contraditórios

*"Rápido, seguro, barato e simples"*: quando os requisitos se chocam, AI escolhe arbitrariamente (tipicamente seguindo o último pedido). Humano negocia trade-off consciente.

**Uso recomendado:** priorizar os requisitos (ou reformular o problema) antes de envolver o AI.

### 8. Exploração de código legado sem mapa

Sistemas sem documentação, sem testes, com convenções implícitas e desvios históricos. O AI lê cada arquivo como se fosse independente; o valor está nas conexões implícitas que não estão escritas.

**Uso recomendado:** humano explora primeiro, mapeia. Depois AI ajuda com mudanças pontuais.

### Heurística final

> *Se você não consegue descrever o resultado esperado em 3 frases verificáveis, o AI não vai entregar algo útil.*

Quando a tarefa é vaga, exploratória e precisa de julgamento, o AI tipicamente degrada performance. Quando é bem-definida e verificável, ele acelera.

---
