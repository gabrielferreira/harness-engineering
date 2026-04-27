## Parte XIX — Anatomia de um Bom Prompt

A Parte XIII listou anti-padrões; esta é a contrapartida construtiva. Um bom prompt economiza iterações, reduz confabulação e melhora qualidade.

### 1. Três intenções, três estruturas

Todo prompt cai numa das três intenções abaixo. A estrutura muda.

**A. Explorar**: "me ajude a entender X, mapear possibilidades, listar abordagens"

Estrutura:
- Objetivo (entender / decidir / escolher);
- Contexto do que já foi considerado;
- Restrições conhecidas;
- Formato de saída (tabela, lista, prós/contras).

Exemplo:
> *"Estou decidindo entre Postgres e MySQL para o serviço X. Workload: 80% leitura, dados de até 10TB em 2 anos, precisa de JSON queries. Já uso Postgres em outros serviços. Liste 3-5 critérios de decisão com prós/contras de cada banco. Formato: tabela."*

**B. Implementar**: "escreva código que faz Y"

Estrutura:
- Spec curta (o que, por quê);
- Critério de aceitação verificável;
- Arquivos afetados;
- Restrições (não tocar em X, preservar Y);
- Skills ou padrões a seguir.

Exemplo:
> *"Implementar endpoint POST /users/:id/deactivate. Deve marcar o usuário como inativo (is_active=false), invalidar sessões ativas, e enviar evento user.deactivated para o bus. Arquivos: controllers/user.ts, services/session.ts. Preservar o padrão de autorização atual (middleware adminOnly). Retornar 204 em sucesso. Testes seguindo o padrão do describe existente."*

**C. Revisar / criticar**: "analise Z e reporte"

Estrutura:
- O que analisar (escopo);
- Critérios (o que é "bom" vs. "ruim" neste contexto);
- Severidade esperada;
- Formato do relatório.

Exemplo:
> *"Revisar o PR #234 procurando: (1) vulnerabilidades de segurança comuns (injection, XSS); (2) tratamento de erro ausente; (3) testes tautológicos. Reportar achados em formato: severidade (🔴🟠🟡), arquivo:linha, descrição, sugestão."*

### 2. Anatomia mínima de um prompt útil

```
[Contexto: onde estou, o que é o projeto — 1-2 frases]
[Objetivo: o que quero, verificável — 1 frase]
[Restrições: o que NÃO fazer — 1-3 bullets]
[Formato esperado: estrutura da resposta — 1 frase]
```

Prompt com essas quatro partes é 10x melhor que "faça X".

### 3. Erros construtivos comuns

| Erro | Exemplo | Correção |
|---|---|---|
| **Verbo vago** | "melhore esse código" | "reduza duplicação entre funA e funB extraindo helper comum" |
| **Sem critério** | "refatore para ficar mais limpo" | "refatore para que funA tenha <20 linhas e zero condicionais aninhadas" |
| **Escopo implícito** | "consertar o bug" | "consertar falha em login quando email contém + (bug #123)" |
| **Sem restrição** | "adicionar cache" | "adicionar cache em getUser, TTL 5min, usando Redis existente, sem mudar assinatura pública" |
| **Sem formato** | "liste os problemas" | "liste problemas em bullets, agrupados por severidade, máximo 10" |

### 4. Escalar o detalhamento com a complexidade

- Fast-path (typo, bump): 1-2 frases bastam;
- Pequeno: prompt com 4 partes da anatomia;
- Médio+: prompt referencia spec aprovada e plano; contexto vem dos arquivos, não do prompt.

Ou seja: para trabalho grande, o prompt é curto porque o **contexto está nos artefatos**.

### 5. Tom e restrição de iniciativa

AI tende a "ajudar além do pedido": refatora o que não foi pedido, adiciona features vizinhas, melhora estilo que estava bom. Controlar explicitamente:

- *"Só mude o necessário para X. Não refatore código não relacionado."*
- *"Se encontrar problema fora do escopo, reporte, não corrija."*
- *"Mantenha convenções existentes mesmo se você discordar delas."*

### 6. Quando o prompt está ruim: sinais

Se o output tem um destes sintomas, o prompt é que precisa melhorar:

- Resposta genérica que caberia em qualquer projeto;
- Código com placeholders (`TODO`, `// your logic here`);
- Múltiplas "opções" quando você queria uma resposta;
- AI pede esclarecimento repetidas vezes sobre coisa óbvia;
- Output grande demais, cobrindo coisas que você não pediu.

Cada um indica lacuna específica no prompt. Corrigir na origem é mais rápido que iterar no output.

---
