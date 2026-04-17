# Manifesto de Harness Engineering

AI coding assistants entregam o que se pede. O problema raramente é o modelo. É a ausência de infraestrutura que diga onde ele está, o que o time valoriza, e como o trabalho é avaliado.

**Harness é essa infraestrutura.** Este documento declara como pensamos sobre ela.

---

## O que valorizamos

Reconhecemos valor em ambos os lados, mas quando há tensão, preferimos o primeiro.

- **Contexto explícito** sobre intuição implícita.
- **Arquivos persistidos** sobre conversas efêmeras.
- **Revisão humana entre fases** sobre autonomia irrestrita.
- **Verificação automatizada** sobre convenção apenas escrita.
- **Simplicidade concreta** sobre abstração prematura.
- **Diretrizes compartilhadas** sobre preferências individuais.
- **Cerimônia proporcional** sobre processo uniforme.
- **Compatibilidade declarada** sobre compatibilidade acidental.

---

## Princípios

### 1. O AI é colaborador, não oráculo

Tratamos o assistant como um colega novo: acelerado, mas que precisa de onboarding, convenções, revisão e limites. Não como uma inteligência que acerta por magia.

### 2. Harness é infraestrutura, não otimização

Não é um ajuste para ganhar 10% de velocidade. É a camada que determina se o AI ajuda ou atrapalha. Sem harness, produtividade aparente vira débito silencioso.

### 3. Contexto tem custo: referenciamos em vez de inlinar

Mais contexto não é melhor contexto. Regras globais entram no onboarding automático; profundidade é carregada sob demanda. Menos barulho, mais sinal.

### 4. Toda decisão importante vira arquivo versionado

Conversas somem. Commits, specs, planos e migrations sobrevivem ao refresh da sessão, à troca de membro, à migração de ferramenta.

### 5. Gates explícitos protegem do arrasto silencioso

Humanos aprovam transições críticas: spec → plano, plano → código, código → merge. Automação faz o repetitivo; julgamento é humano.

### 6. Skills informam, agents verificam, humanos julgam

Skills são checklists antes de agir. Agents são auditores read-only depois de agir. O merge é sempre decisão humana.

### 7. Cerimônia é proporcional à complexidade, nunca uniforme

Typo não precisa de spec. Feature grande sem spec não começa. Processo pesado em tarefa leve é tão ruim quanto ausência de processo em tarefa grande.

### 8. Registrar o descartado importa tanto quanto registrar o feito

Decisões descartadas, ideias adiadas e anti-padrões registrados impedem a organização de refazer a mesma discussão. Memória institucional é ativo.

### 9. Nenhuma regra sobrevive sem verificação automatizada

Convenção que não é check no `verify.sh` é convenção que vai ser violada. Se importa, precisa falhar o build quando quebrada.

### 10. Três casos concretos antes de abstrair

Repetição explícita é melhor que abstração errada. Abstração desfazer custa mais que copy-paste limpar.

### 11. Compatibilidade é escolha explícita, não acidente

Todo artefato distribuído declara como evolui: aditivo, migrável ou breaking. Projetos antigos continuam funcionando até que a migração seja oferecida. Nunca são sabotados.

### 12. Segurança é parte do design, não adendo

Allowlists de paths e comandos, inputs externos como dados (não instruções), pre-commit hooks, code review obrigatório antes de merge. O AI é colaborador externo: recebe só o que precisa.

### 13. Simplicidade é a regra; complexidade precisa se justificar

Markdown antes de banco de dados. Script antes de framework. Arquivo antes de SaaS. Se o repo compila, o harness funciona.

### 14. Harness é software vivo: apodrece sem poda

Skills não usadas, regras que ninguém segue, docs órfãs: revisamos e removemos. Manter o essencial vale mais do que acumular o completo.

### 15. Medir antes de opinar sobre estar funcionando

Reincidência, rework, cobertura, tempo até o primeiro gate. Sem métrica, *"o harness está bom"* é sentimento. Com métrica, é trabalho.

### 16. O que o AI não faz bem, delegamos ao humano

Debug sutil, decisão arquitetural nova, incidente crítico, código regulado sem spec. Harness maduro conhece os limites do AI e os respeita.

---

## Compromissos

Quem adota este manifesto se compromete a:

- **Ler o contexto** antes de pedir ao AI;
- **Escrever spec** antes de codar o que não é trivial;
- **Registrar o descartado** junto com o feito;
- **Transformar cada regra importante em verificação executável**;
- **Revisar, podar e evoluir o harness continuamente**;
- **Onboardar pessoas**, não só ferramentas.

---

*Adapte ao seu contexto. Princípios valem mais que regras literais.*
