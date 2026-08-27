---
name: paper-writer
description: Segmented drafting of a scientific manuscript, with mandatory grounding in declared project artifacts and a project-defined authorial voice. Segments what remains to be written, allocates a reasoning budget per segment, dispatches writers in parallel (each with the full manuscript as context), and consolidates into a single draft for human review. Never publishes on its own — it produces a grounded draft, never final text. Use when asked to write, draft, or rewrite a section of a paper, thesis, dissertation, chapter, or proposal.
license: MIT
---

# paper-writer — redação segmentada com fundamentação obrigatória

Espelha a arquitetura do `paper-reviewer` (Paper Assistant Tool, Jayaram et al., Google Research, arXiv:2606.28277), mas para o lado da escrita em vez da crítica: segmentar o que falta escrever, dar a cada redator **o manuscrito inteiro como contexto de voz e consistência, mas só um segmento como alvo de redação**, e consolidar depois. A mesma lógica que eleva a taxa de detecção de erro no PAT — atenção concentrada em vez de uma passada rasa e uniforme — vale para produzir prosa consistente em vez de um rascunho genérico.

**Não produz texto pronto pra publicar.** Produz rascunho fundamentado, com toda alegação numérica rastreável a um artefato declarado, na voz definida pelo projeto — para o autor revisar e aprovar frase por frase. Diferente do `paper-reviewer` (só lê, nunca edita), esta skill escreve — por isso a disciplina de fundamentação abaixo é mais rígida, não mais frouxa: aqui uma alucinação vira afirmação falsa **dentro** do artigo, não um apontamento perdido num relatório.

---

## Configuração do projeto — obrigatória, antes de qualquer coisa

Esta skill não escreve uma frase até saber de onde os números podem vir. Procure o arquivo de configuração nesta ordem:

1. `.claude/paper-writer.md` na raiz do projeto
2. `paper-writer.config.md` na raiz do projeto
3. o caminho que o usuário indicar

**Se não existir nenhum, pare e peça.** Copie `references/project-config.template.md` (desta skill) para o projeto, peça ao usuário para preencher, e só então prossiga. Há um exemplo completo e preenchido em `references/example-config-ptbr-abnt.md`.

Escrever sem config é o modo de falha que esta skill existe para impedir: sem lista de artefatos canônicos, um redator com pressa preenche o buraco com um número plausível, e número plausível é indistinguível de número certo até o parecerista conferir.

O config declara quatro coisas:

| Bloco | O que é | Por que importa |
|---|---|---|
| **Artefatos canônicos** | os arquivos de onde os números podem vir | é a única fonte legítima |
| **Fontes supersedidas** | o que existe no repositório e está **proibido** como fonte | rascunho antigo e rodada de dados velha são o vetor de erro mais comum |
| **Narrativa de processo a excluir** | o que aconteceu mas não vai para o manuscrito | ver Regra dura 2 |
| **Guia de voz** | as convenções de escrita do projeto | é o que impede o rascunho de destoar do que já existe |

---

## Regras duras (não negociáveis, checar antes de escrever qualquer frase)

1. **Só artefato canônico é fonte.** Nenhum número, tabela, p-valor ou alegação entra vindo de um rascunho anterior, de uma rodada de dados supersedida, ou de qualquer arquivo fora da lista canônica do config. Se um valor só existe numa fonte supersedida, ele vira `[VERIFICAR]` — **nunca** é transportado "porque provavelmente não mudou".

2. **A narrativa de processo não entra no manuscrito.** O texto descreve o artefato **como ele está hoje, já corrigido** — não a jornada de descobrir e consertar um problema. Quando a metodologia de curadoria precisa aparecer, ela aparece agregada ("N itens passaram por revisão manual; M foram revisados"), nunca como log linha a linha, item por item ou versão por versão. O log é insumo interno; o manuscrito é o estado final. Confundir os dois transforma a seção de método num diário de bordo e entrega ao parecerista uma lista de problemas que já não existem.

3. **Nenhum número sem fonte rastreável.** Todo valor quantitativo cita o arquivo (e o campo, se aplicável) de onde veio. Número que devia existir mas não foi encontrado vira `[VERIFICAR: <o que falta e onde provavelmente está>]` — nunca um valor estimado, arredondado de memória ou inventado para "soar plausível".

4. **Nenhuma citação de literatura inventada.** Só cita trabalho que já está no `.bib` ou que foi localizado agora (WebSearch, com URL/DOI conferíveis). Referência sem entrada correspondente vira `[CITAÇÃO NECESSÁRIA: <o que precisa sustentar>]`.

Estas quatro regras valem para cada redator do Estágio 3, sem exceção, e são a primeira coisa a checar no Estágio 4 antes de mesclar qualquer rascunho no manuscrito real.

---

## Estágio 0 — Resolver o alvo e os insumos

1. Qual manuscrito e qual seção/segmento faltam escrever? Se não especificado, perguntar — não adivinhar o escopo antes de gastar os agentes.
2. Ler o manuscrito **inteiro** (o que já existe dele) antes de escrever qualquer palavra nova, para herdar terminologia, tom e estrutura já em uso.
3. Ler o guia de voz declarado no config.
4. Localizar os artefatos-fonte que vão alimentar **este** segmento, dentro da lista canônica. Anote o caminho exato de cada um — o Estágio 3 vai colar caminhos nos prompts, não descrições.
5. Se houver revisão anterior do `paper-reviewer` sobre este manuscrito, ler antes de escrever — não reintroduzir um defeito já apontado.

---

## Estágio 1 — Segmentação

Quebre o que falta escrever em **segmentos semânticos**, mesma lógica do `paper-reviewer`: um segmento reúne o que compartilha tema lógico e se escreve em conjunto, mesmo que não contíguo no documento final.

| Segmento | Costuma reunir |
|---|---|
| Enquadramento | Resumo, Introdução, contribuições declaradas |
| Trabalhos relacionados | Estado da arte, posicionamento da lacuna |
| Método / arquiteturas | O que foi construído ou comparado |
| Definição de métrica | Formalização de toda métrica proposta |
| Dados | Conjuntos, proveniência, construção, licenciamento |
| Protocolo experimental | O que ficou fixo, configuração, análise estatística |
| Resultados | Tabelas, figuras, números no corpo |
| Discussão e limitações | Interpretação, ameaças à validade, trabalho futuro |
| Conclusão | Fechamento, conforme exigido pelo guia de voz do projeto |

Ajuste ao manuscrito real, igual ao `paper-reviewer`.

---

## Estágio 2 — Orçamento adaptativo

Mesma lógica do `paper-reviewer`, adaptada para densidade de decisão de conteúdo em vez de densidade de afirmação verificável:

- **ALTO** — Resultados, Definição de métrica, Protocolo experimental: qualquer segmento onde um número errado ou uma alegação estatística mal calibrada compromete o artigo. `model: opus`, redator instruído a **citar a fonte de cada número antes de escrever a frase que o usa**.
- **MÉDIO** — Método, Dados, Discussão. `model: opus`, verificação normal de fundamentação.
- **BAIXO** — Enquadramento, Trabalhos relacionados. `model: sonnet` basta.

Anuncie a segmentação e o orçamento antes de disparar — última chance de corrigir o recorte.

---

## Estágio 3 — Redação em paralelo

Dispare **um subagente por segmento**, todos na mesma mensagem. `subagent_type: general-purpose`, `model` do Estágio 2.

A lista abaixo vai **inteira** em cada prompt — não resumida, e nunca supondo que o subagente herda o seu contexto. Isso é deliberado: instrução colada na tarefa é seguida, enquanto a mesma instrução lá atrás, numa sessão longa, decai.

Cada prompt de redator deve conter, sem exceção:

1. **O manuscrito inteiro** (caminho do arquivo, se existir), como contexto de voz e terminologia — não para copiar, para não destoar.
2. **O segmento designado**, como único alvo de redação.
3. **As quatro regras duras** do topo deste documento, coladas literalmente no prompt.
4. **Os caminhos exatos dos artefatos-fonte** daquele segmento — o caminho do arquivo, não "veja os dados".
5. **A lista de fontes supersedidas**, com a instrução explícita de que são proibidas.
6. **O guia de voz do projeto**, colado literalmente.
7. Instrução de **escrever num arquivo de rascunho separado** (`rascunhos/<segmento>_<AAAA-MM-DD>.md` ou o caminho definido no config), nunca direto no manuscrito final — a mesclagem é do Estágio 4, depois de checar fundamentação.

---

## Estágio 4 — Síntese e handoff

Feito por você, no contexto principal, depois que todos os redatores voltarem.

1. **Cheque as quatro regras duras primeiro**, em cada rascunho de segmento — antes de qualquer outra coisa. Rascunho com `[VERIFICAR]`/`[CITAÇÃO NECESSÁRIA]` pendente, ou com número sem fonte citada, **não mescla** até resolver.
2. **Harmonize voz e terminologia entre segmentos.** O mesmo conceito não pode ganhar dois nomes diferentes em segmentos vizinhos.
3. **Elimine redundância entre segmentos** — a mesma alegação/número não deve aparecer justificado do zero duas vezes.
4. **Verifique você mesmo os números de maior risco** (os que apareceriam em mais de um lugar do artigo) contra o artefato-fonte, antes de mesclar.
5. Só então mescle os rascunhos no manuscrito real.

### Depois de mesclar

Redação e revisão são passes separados por design — quem escreve não aprova o próprio texto no mesmo contexto. Depois de mesclar, recomende (ou já dispare, se o usuário topar) uma passada do `paper-reviewer` sobre as seções novas/alteradas antes de considerar o trecho pronto. Se houver uma lista de seções que ainda serão reescritas depois, informe o `paper-reviewer` disso — ele já sabe separar "corrigir" de "evitar na escrita nova".

### Saída

Grave o rascunho consolidado ao lado do manuscrito (ex.: `rascunhos/rascunho_<segmento-ou-secao>_<AAAA-MM-DD>.md`) antes de mesclar, para o autor conseguir comparar lado a lado se quiser. Resuma no chat: o que foi escrito, quais `[VERIFICAR]`/`[CITAÇÃO NECESSÁRIA]` ficaram em aberto (se algum sobreviveu à checagem do Estágio 4, isso é uma falha do processo — não deveria sobreviver), e se recomenda rodar o `paper-reviewer` em seguida.

---

## Notas de operação

- Se o usuário pedir foco (`só a seção de resultados`), reduza os segmentos ao escopo pedido.
- Se o manuscrito ainda não existe, o Estágio 0 vira "definir estrutura" antes de segmentar — pergunte o esqueleto de seções esperado em vez de inventar um.
- Rodar de novo depois de o `paper-reviewer` apontar problema é o uso pretendido — não há limite de rodadas por seção.
- O config é do projeto, não da skill. Ele fica versionado no repositório do manuscrito e evolui com ele; a skill permanece genérica.
