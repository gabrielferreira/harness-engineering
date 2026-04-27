## Parte XX — Debug Workflow com AI

AI acelera debug quando usado corretamente. Mal usado, amplifica confusão. O fluxo abaixo é o padrão que funciona.

### 1. Antes de chamar o AI: repro mínimo

**Regra de ouro:** AI sem repro é adivinhação. Investir em reproduzir o bug de forma mínima e determinística **antes** de pedir ajuda.

Checklist de repro:
- [ ] Comando ou sequência exata que dispara o bug;
- [ ] Estado prévio necessário (dados, config, ambiente);
- [ ] Saída atual vs. saída esperada;
- [ ] Variações testadas que **não** reproduzem (ajuda a localizar).

Com repro mínimo, AI vira multiplicador. Sem ele, vira ruído.

### 2. O fluxo de 5 passos

**Passo 1. Triagem.** Descreva sintoma + repro ao AI. Peça hipóteses ordenadas por probabilidade, com justificativa.

> *"Endpoint GET /users retorna 500 intermitentemente (~10% requests) desde ontem 14h. Log mostra `connection pool timeout`. Repro: `ab -n 1000 -c 50 /users`. Liste 5 hipóteses ordenadas por probabilidade."*

**Passo 2. Priorizar por custo de verificação.** Das hipóteses do AI, qual é mais barata de confirmar/descartar? Nem sempre a mais provável, e sim a mais **barata de testar primeiro**.

**Passo 3. Instrumentação.** Pedir ao AI para gerar logs, métricas, traces que discriminem entre hipóteses. O AI é bom nisso: sugere pontos específicos do código onde instrumentar.

**Passo 4. Coletar evidência.** Rodar. Ler logs. Voltar ao AI com dados concretos, não impressões. *"Adicionei log antes e depois da query; em 47/500 requests a query demorou >5s. Hipótese 3 (query não indexada) fortalece. Verificar próximo?"*

**Passo 5. Consertar + regression test.** Quando causa-raiz identificada, AI escreve fix + teste que **falha sem o fix**. Esse é o critério: teste que não falharia sem o fix é inútil.

### 3. Onde o AI brilha no debug

- **Bisect assistido**: "entre commit A e B, qual comportamento mudou?";
- **Comparação de duas implementações**: "compare foo antigo e foo novo, aponte diferença comportamental";
- **Gerar hipóteses amplas**: rápido, sem viés de confirmação (bom contraponto ao instinto humano);
- **Instrumentação sob medida**: "adicione log estruturado nos 3 pontos críticos deste fluxo";
- **Ler stack trace longo**: resumir, mapear para arquivos, identificar frame relevante;
- **Propor regression test**: a partir de repro, escrever o teste que fixa;
- **Pesquisar padrão do erro**: "esse erro aparece quando X; veja se o código tem padrão X".

### 4. Onde o AI atrapalha

- **Racionalização a posteriori**: depois de 10 trocas, AI "confirma" hipóteses suas que são erradas. Desconfiar de concordância fácil;
- **Instinto de "consertar"**: AI sugere mudanças especulativas em 3 lugares quando bug está em 1. Pedir **apenas diagnóstico**, não fix, na fase de investigação;
- **Viés pelo último arquivo lido**: AI atribui causa ao código que está fresco no contexto;
- **Alucinação de comportamento**: "esta função deveria fazer X" sem verificar o que ela de fato faz. Exigir citação de código real;
- **Pular evidência contrária**: se dado coletado contradiz hipótese, o AI às vezes minimiza. Reler evidência sem o AI entre os passos.

### 5. Anti-padrão clássico: "shotgun debugging"

Pedir ao AI para tentar 5 mudanças ao mesmo tempo esperando que alguma conserte. Resultado típico: alguma conserta mas ninguém sabe qual nem por quê. Bug volta em forma diferente.

**Regra:** uma hipótese por vez. Uma mudança por vez. Verificação por vez.

### 6. Quando parar e chamar humano

- 3 ciclos sem progresso mensurável;
- AI está dando respostas circulares;
- Hipóteses se esgotaram (todas testadas, todas falsas);
- O bug tem correlação temporal (só em horário específico, tipicamente infraestrutura, não código);
- Envolve concorrência, rede, ou estado distribuído (ver Parte XIV).

Chamar humano = parar e mostrar o estado completo (repro, hipóteses testadas, evidência). AI é parte da ferramenta, não substituto de par humano.

---
