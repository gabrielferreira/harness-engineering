## Parte XVII — Métricas de Saúde do Harness

Harness sem métrica vira opinião. Sem indicadores, discussões ficam no *"acho que está ajudando"*. Defina 3-5 indicadores e revise trimestralmente.

### 1. Indicadores quantitativos

| Métrica | Como medir | Meta saudável |
|---|---|---|
| **Reincidência de bug** | % de bugs corrigidos que voltam em 90 dias | < 5% |
| **Time-to-first-gate** | Do item entrar no backlog até ter spec aprovada | < 3 dias (médio), < 1 dia (pequeno) |
| **Spec rework** | % de specs que voltam para "rascunho" depois de "aprovada" | < 15% |
| **Skill coverage** | % de PRs que consultaram/aplicaram pelo menos uma skill relevante | > 70% |
| **Context file churn** | Mudanças por mês no arquivo de contexto principal | 1-5 (nem instável, nem esquecido) |
| **Validation pass rate (1st try)** | % de PRs que passam no `verify.sh` no primeiro push | > 60% |
| **Mean review cycles** | Número médio de rodadas de revisão até merge | < 2.5 |
| **Tempo em PR aberto** | Mediana do tempo do PR aberto até merge | < 2 dias úteis |
| **Adoção do fast-path** | % de mudanças triviais que usaram fast-path corretamente | > 80% |

### 2. Indicadores qualitativos

Não tudo é número. Pesquisa trimestral com o time (5-10 questões):

- *"O harness acelera ou atrapalha meu trabalho?"* (escala 1-5);
- *"Sei onde procurar a regra X?"* (sim / não / sei mais ou menos);
- *"Código gerado com AI tem a mesma qualidade do meu?"* (melhor / igual / pior);
- *"Dev novo consegue operar em 2 semanas?"* (sim / não);
- *"Qual é a coisa mais chata do harness hoje?"* (aberta);
- *"O que falta?"* (aberta).

A combinação quantitativo + qualitativo evita dois erros:

- **Quantitativo só**: métricas boas, todo mundo odiando;
- **Qualitativo só**: todo mundo feliz, bugs em prod.

### 3. Revisão periódica

Trimestral, em 1-2h:

1. Olhar os indicadores → qual piorou?;
2. Ler pesquisa qualitativa → tema recorrente?;
3. Listar 1-3 ações para próximo trimestre;
4. Atualizar backlog do harness com essas ações.

### 4. Quando reorganizar

Se em dois trimestres consecutivos:

- Reincidência sobe;
- Validation pass rate cai;
- Qualitativo despenca;

É hora de revisitar estrutura. Não continuar empilhando: **parar e limpar**.

---
