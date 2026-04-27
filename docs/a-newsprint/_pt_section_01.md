## Parte XIII — Anti-padrões do Desenvolvedor Usando AI

O AI assistant entrega o que você pede. Se você pede errado, ele erra. A maior parte dos problemas com AI em projetos reais **não é do modelo**: é da forma como o dev interage com ele.

### 1. Prompt vago

**Padrão:** *"faça o login funcionar"*, *"ajusta esse bug"*, *"melhora isso aí"*.

**Consequência:** o AI escolhe por você. Escolhe errado com frequência.

**Antídoto:** especificação. Mesmo informal: *"o endpoint POST /login deve retornar 401 quando a senha está incorreta, hoje retorna 500 porque {X}. Corrigir preservando a validação de email existente"*. Bom prompt é mini-spec.

### 2. Aceitar código sem ler

**Padrão:** "parece que funcionou" → commit → merge → bug em prod.

**Consequência:** você virou caixa de transmissão de código que não entende. Quando quebrar, não saberá consertar.

**Antídoto:** ler o diff. Não entendeu uma linha? Perguntar ao AI *por quê* aquela escolha antes de aceitar. Se ele não justificar bem, provavelmente está errado.

### 3. Pular o gate porque "é rápido"

**Padrão:** *"não precisa de spec, é 10 minutos"* → vira 3h → vira ramo abandonado com código pela metade.

**Consequência:** débito técnico silencioso. O fast-path existe por design, mas seu critério é específico (≤3 arquivos, sem nova abstração, sem mudança de schema). Tudo fora disso merece spec.

**Antídoto:** honestidade com o tamanho real da mudança. Quando em dúvida, trate como maior.

### 4. Contexto-stuffing

**Padrão:** *"pra garantir, vou carregar o repo inteiro no contexto"* → AI se perde, ignora regras, inventa.

**Consequência:** menos qualidade, mais custo, mais latência.

**Antídoto:** disciplina de contexto (Parte III). Carregar o necessário + referências; confiar no AI para pedir mais quando precisar.

### 5. AI como oráculo arquitetural

**Padrão:** *"devo usar microserviço ou monolito?"*, *"Postgres ou Mongo?"* para decisões com trade-offs dependentes do contexto do time.

**Consequência:** resposta genérica que parece sofisticada. Você adota e descobre 6 meses depois que não cabe.

**Antídoto:** usar AI para **mapear** trade-offs (ele é bom nisso) e **rascunhar** ADRs. Decisão final é humana, com conhecimento de time, história, pessoas.

### 6. Iterar quando deveria parar

**Padrão:** código não funciona → pede pro AI ajustar → ainda não → pede de novo → ainda não → 15 iterações depois, uma feature simples virou spaghetti.

**Consequência:** bug escondido debaixo de camadas de "correções" que nunca atacaram a causa.

**Antídoto:** após 2-3 iterações sem progresso, **parar**. Sair da sessão, ler o código com calma, identificar a raiz. Voltar com briefing novo.

### 7. Copy-paste de prompt entre projetos

**Padrão:** prompt que funcionou bem em projeto A é reutilizado em B sem adaptação de contexto.

**Consequência:** AI aplica convenções/padrões do projeto A em B. Código inconsistente, PR barulhento.

**Antídoto:** cada projeto tem seu harness. Prompts mencionam "este projeto" e esperam que o contexto (skills, arquivo de contexto, spec) preencha o específico.

### 8. Não atualizar STATE / docs no fim da sessão

**Padrão:** dia acaba, dev fecha laptop. Amanhã: "onde eu estava mesmo?".

**Consequência:** 30 minutos de arqueologia para reconstruir contexto. AI recomeça do zero, refaz decisões, contradiz escolhas anteriores.

**Antídoto:** última ação da sessão = atualizar STATE.md (ou equivalente). Primeira ação da próxima = ler.

### 9. Não registrar decisão descartada

**Padrão:** discussão longa → decide não fazer X → ninguém anota por quê → 3 meses depois, alguém sugere X de novo → mesma discussão.

**Consequência:** organização repete conversa. Time perde memória.

**Antídoto:** seção "Descartados" do backlog, "Decisões futuras" no parking lot. Registrar é cheap; redescobrir não.

### 10. Tratar AI como substituto em vez de colaborador

**Padrão:** *"o AI vai escrever isso sozinho"* → dev desliga o cérebro → bug.

**Consequência:** dev perde afinidade com o código. Quando AI falha (vai falhar), não sabe socorrer.

**Antídoto:** pair programming mindset. AI é colega júnior acelerado; você é mentor, não espectador.

---
