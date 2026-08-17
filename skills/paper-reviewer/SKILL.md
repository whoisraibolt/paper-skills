---
name: paper-reviewer
description: Deep pre-submission review of a scientific manuscript, modeled on Google's Paper Assistant Tool (PAT). Segments the manuscript, allocates a reasoning budget per segment, dispatches deep reviewers in parallel (each with the full text as context), and consolidates into a single report with severity, quoted evidence, and anti-hallucination checks. Use when asked to review, audit, critique, or validate a paper, thesis, dissertation, chapter, or proposal before submission. Accepts .tex, .md, .pdf, and .docx.
license: MIT
---

# paper-reviewer — revisão profunda pré-submissão

Reimplementação da arquitetura do **Paper Assistant Tool (PAT)** (Jayaram et al., Google Research, arXiv:2606.28277) usando subagentes do Claude Code no lugar do Gemini Deep Think.

A premissa do PAT, que é o que faz esta skill valer a pena em vez de "leia o artigo e critique": uma única passada de leitura gasta o orçamento de raciocínio de forma uniforme e rasa. Segmentar o manuscrito, dar a cada revisor **o texto inteiro como contexto mas só um segmento para verificar**, e depois consolidar com deduplicação e checagem de fundamentação, eleva bastante a taxa de detecção de erro real. No subconjunto Math/CS do benchmark SPOT, essa orquestração levou o mesmo modelo de 55,2% para 89,7% de detecção.

Não produz nota, ranking nem recomendação de aceite. Produz **erros objetivos e melhorias acionáveis**.

Par de escrita: `paper-writer`. Redação e revisão são passes separados por design — quem escreve não aprova o próprio texto no mesmo contexto.

---

## Estágio 0 — Resolver o alvo

1. Se o usuário nomeou um arquivo, use-o. Se não, procure o manuscrito mais provável no diretório atual (`.tex` com `\documentclass`, ou `.md` longo) e **confirme com o usuário antes de gastar os agentes** se houver mais de um candidato.
2. **Prefira sempre a fonte sobre o PDF.** O PAT lista falha de parsing de PDF entre suas três limitações mais reportadas. Se existe `.tex` ou `.md`, use-o e ignore o PDF compilado.
3. Leia o manuscrito **inteiro** antes de segmentar. Sem isso a segmentação sai errada.
4. Localize os insumos de verificação, se existirem:
   - o `.bib` / arquivo de referências;
   - dados, tabelas de resultado ou saídas de experimento no repositório (ex.: `data/outputs/`), que permitem conferir número por número;
   - revisões, auditorias ou pareceres anteriores (ex.: `auditorias/`, `resposta_*.md`, `HANDOFF.md`) — servem para **não repetir** ponto já resolvido.

---

## Estágio 1 — Segmentação

Quebre o manuscrito em **segmentos semânticos**, não em pedaços de tamanho igual. Um segmento é um conjunto de seções que compartilham um tema lógico e que se verificam em conjunto. Podem ser **não contíguos**: se o resumo antecipa um número da Seção 7, os dois pertencem ao mesmo segmento.

Segmentação típica de artigo empírico:

| Segmento | Costuma reunir |
|---|---|
| Enquadramento | Resumo, Introdução, Considerações Finais, contribuições declaradas |
| Trabalhos relacionados | Estado da arte, posicionamento da lacuna |
| Método / arquiteturas | O que foi construído ou comparado |
| Definição de métrica | Toda métrica proposta pelos autores, com sua formalização |
| Dados | Conjuntos, proveniência, construção, licenciamento |
| Protocolo experimental | O que ficou fixo, configuração, análise estatística |
| Resultados | Tabelas, figuras, números no corpo do texto |
| Discussão e limitações | Interpretação, ameaças à validade, trabalho futuro |

Ajuste ao manuscrito real. Um artigo teórico troca "Resultados" por "Provas"; um bibliométrico troca "Arquiteturas" por "Protocolo de busca".

---

## Estágio 2 — Orçamento adaptativo

Atribua a cada segmento uma faixa de esforço conforme a densidade de afirmação verificável. Isto é o que o PAT chama de Light/Medium/High Thinking.

- **ALTO** — onde um erro invalida o artigo. Definição de métrica, provas, protocolo estatístico, tabelas de resultado, qualquer número que apareça em mais de um lugar. Estes segmentos vão para revisores com `model: opus` e instrução explícita de raciocinar linha a linha.
- **MÉDIO** — método, dados, configuração experimental, discussão. `model: opus`, verificação normal.
- **BAIXO** — enquadramento, trabalhos relacionados, seções de agradecimento e declaração. `model: sonnet` basta.

Anuncie a segmentação e o orçamento ao usuário em uma tabela curta antes de disparar. É a última chance de corrigir o recorte barato.

---

## Estágio 3 — Revisão profunda em paralelo

Dispare **um subagente por segmento**, todos na mesma mensagem para rodarem em paralelo. Use `subagent_type: general-purpose` com o `model` definido no Estágio 2.

Cada prompt de revisor deve conter, sem exceção:

1. **O manuscrito inteiro** (caminho do arquivo — o agente lê), com a instrução de que ele é contexto, não alvo.
2. **O segmento designado**, por seção e faixa de linhas, como o único alvo de verificação.
3. **SOMENTE LEITURA** — proibido usar Write, Edit ou NotebookEdit. O revisor relata, não conserta.
4. Os caminhos dos insumos de verificação do Estágio 0.
5. O contrato de achado abaixo.

### Contrato de achado

Todo achado devolvido precisa ter:

- **Severidade** — `CRÍTICO` (invalida uma conclusão), `ALTO` (exige reescrita substantiva), `MÉDIO` (enfraquece o argumento ou a clareza), `BAIXO` (correção pontual).
- **Localização** — arquivo e linha.
- **Citação literal** do trecho problemático. Sem citação, o achado não existe.
- **O defeito**, em uma frase.
- **Confiança** — `CONFIRMADO` (verificado contra a fonte, os dados ou o `.bib`) ou `PLAUSÍVEL` (suspeita fundamentada, não verificada).
- **O que teria de ser verdade para eu estar errado** — uma linha. Este campo é o que separa crítica útil de ruído.

### O que caçar

Genérico, em qualquer manuscrito:

- **Consistência numérica cruzada.** Todo número do resumo, do corpo, das tabelas e das figuras precisa bater. Onde houver dados brutos no repositório, confira contra eles. É a classe de erro mais comum e a mais barata de detectar.
- **Afirmação além da evidência.** Alegação causal sustentada por resultado correlacional; "demonstra" onde cabe "sugere"; generalização para além das condições testadas.
- **Contribuição declarada vs. entregue.** Cada item da lista de contribuições tem seção correspondente que o cumpre?
- **Perguntas de pesquisa órfãs.** Cada RQ é respondida explicitamente? Cada resposta remete a uma evidência específica?
- **Referências.** Toda `\cite` tem entrada no `.bib`; toda entrada é citada; o trabalho citado sustenta o que o texto diz que ele sustenta. Sinalize entrada com cara de inventada (DOI ausente, autoria vaga, título genérico).
- **Erros aritmeticamente pequenos e logicamente fatais** — sinal trocado, desigualdade invertida, erro de unidade, off-by-one, notação sobrecarregada. O PAT reporta que estes são o achado mais frequente e o mais subestimado.
- **Limitação ausente.** Ameaça óbvia à validade que o texto não reconhece.
- **Vazamento metodológico.** O instrumento de avaliação foi construído usando a coisa que ele avalia? Circularidade entre o que é medido e o que é usado para medir.
- **Proveniência e licenciamento** de dados e corpora, quando o texto os descreve.

### Guardas antialucinação

O PAT documenta três modos de falha próprios. Instrua cada revisor contra os três:

1. **Não alegue que algo está desatualizado** — data, versão, "estado da arte" — sem verificar. Se não deu para verificar, o achado é `PLAUSÍVEL` e vem redigido como pergunta.
2. **Não invente referência, teorema ou trabalho relacionado.** Se citar literatura externa, tem de ser algo que o revisor consiga localizar.
3. **Não declare um argumento incorreto por não tê-lo entendido.** Antes de marcar `CRÍTICO` em um raciocínio, o revisor deve reconstruir o argumento do autor com as próprias palavras e só então apontar onde ele quebra. Se a reconstrução não fecha, o achado vira `PLAUSÍVEL` com a dúvida explicitada.

Nada de elogio. O relatório não tem seção de pontos fortes.

---

## Estágio 3.5 — Assinatura de linguagem automatizada

Um revisor dedicado, sobre o **manuscrito inteiro**. Não é um segmento: os sinais
abaixo são de **frequência**, e frequência só se mede no texto todo.

### Escopo: só o manuscrito

Este estágio lê **o arquivo do manuscrito e nada mais**. Não abre o histórico do
versionamento, não abre briefings, roteiros de redação ou notas internas do
projeto, e não envia o texto para serviço externo.

Três razões, e as três são de projeto, não de conveniência:

1. **O parecerista só vê o manuscrito.** Se esta skill existe para antecipar o
   parecer, ela tem de trabalhar com o que o parecerista enxerga. Achado que
   depende de artefato interno não sobrevive à submissão.
2. **A evidência interna é ambígua na origem.** Um briefing que catalogou os
   vícios do próprio autor faz "o texto bate com o briefing" deixar de
   distinguir hábito próprio de padrão importado. A evidência parece forte e não
   é.
3. **Não generaliza.** Um estágio que só funciona onde existe repositório e
   briefing não é um estágio; é um acidente daquele projeto.

Há uma consequência disso, e ela é o ponto seguinte.

### A assimetria diagnóstica — a regra que rege este estágio

Os critérios desta seção **não valem todos a mesma coisa**, e a diferença não é
de importância: é de **custo de burlar**.

Contar conector e advérbio absolutista é barato de zerar. Uma busca-e-substitui
de dez minutos limpa os dois sem tocar em uma linha de raciocínio. Logo:

> **Critério raspável só informa quando dispara. Quando passa, não informa nada.**

Isso é obrigatório no relatório. Um manuscrito com 0,3 conector por parágrafo
pode ser um texto bem escrito ou um texto raspado na véspera, e a contagem não
separa os dois. Reportar "quatro dos seis critérios não disparam" como se fosse
boa notícia emite um **atestado de limpeza que o instrumento não pode dar** — e é
pior do que não medir, porque tranquiliza.

Redija sempre assim: *"Critérios 1 e 3 não disparam. São raspáveis por
busca-e-substitui e, portanto, **não-diagnósticos quando passam**: a contagem
baixa não licencia nenhuma inferência."*

### Faixa A — raspáveis (contam só se dispararem)

| # | Critério | Alerta |
|---|---|---|
| A1 | Conectores encabeçando frase (*além disso, contudo, entretanto, portanto, vale destacar, em outras palavras, isso significa que, em conclusão*) | acima de 4 por parágrafo |
| A2 | Absolutismo lexical (*sempre, nunca, claramente, obviamente, sem dúvida, evidentemente*) | acima de 3 por página |
| A3 | Travessão longo (—) em excesso | — |

Se dispararem, são achados normais, com contagem e trecho. Se não dispararem,
**uma linha dizendo que são não-diagnósticos, e nada mais**. Não os liste como
"verificado e limpo".

Sub-achado que a Faixa A não pega e que costuma sobreviver à raspagem:
**intensificador sem lastro** (*expressivo, substancialmente, consistentemente,
sistematicamente, altamente*). Quem raspa absolutismo raramente raspa isto. Conte
e separe os que têm um número por trás dos que só enfatizam.

### Faixa B — resistentes (o peso do estágio)

Nenhum destes se remove com busca-e-substitui. Todos exigem reescrever. São, por
isso, os únicos que carregam informação de verdade.

| # | Critério | Como medir | Alerta |
|---|---|---|---|
| B1 | **Simetria de template** | coeficiente de variação do tamanho dos parágrafos, global **e por bloco de seção** | CV abaixo de 30% |
| B2 | **Redundância semântica** | n-gramas de 8+ palavras repetidos; mesma proposição em pontos distantes | qualquer cadeia |
| B3 | **Tautologia definicional** | achado que a regra de classificação **garante por construção** | qualquer ocorrência |
| B4 | **Hipotaxe inflacionada** | distribuição do comprimento de sentença, com atenção à cauda | sentenças acima de ~60 palavras |
| B5 | **Frame retórico único** | contagem do modo *default* de afirmar (*X, e não Y*; *não apenas… mas também*; *ao passo que*) | frame dominante em >20% dos parágrafos |
| B6 | **Voz autoral ausente** | proporção de parágrafos que relatam sem posicionar | acima de 70% |
| B7 | **Conclusão tautológica** | sobreposição da conclusão com o corpo, mais leitura direta | qualquer ocorrência |
| B8 | **Ritmo robótico** | mesma medida de B4, outra cauda: sujeito + verbo + complemento em cadeia | CV do comprimento de sentença abaixo de 30% |
| B9 | **Ilusão de profundidade** | reformulação para ganhar volume; metáfora genérica no lugar de análise; afirmação autoevidente vendida como implicação | qualquer ocorrência |

**B4 e B8 são a mesma medição, lida nas duas pontas.** Calcule uma vez a
distribuição do comprimento de sentença: CV baixo acusa B8, cauda longa acusa
B4. Um manuscrito raramente tem os dois.

Quatro notas de medição, aprendidas em uso:

- **B1 mede por bloco, não só global.** Um CV global saudável esconde uma seção
  de quatro parágrafos com CV de 4% — que é exatamente onde o leitor aprende o
  formulário e para de ler. Reporte o pior bloco, não a média.
- **B3 é o achado mais grave que este estágio produz, e não é defeito de estilo.**
  Quando o texto define uma categoria e depois apresenta como descoberta um
  padrão que a definição garante, isso é **problema de validade**. Um parecerista
  atento aponta. Marque como `CRÍTICO` e mande para o Estágio 4 verificar.
- **B6 super-marca quando automatizado.** Regex não reconhece posicionamento
  indireto (*"converge com a avaliação conduzida neste trabalho"*, *"esta lacuna
  constitui a motivação central"*). Use o automático para **localizar**, depois
  reconfira à mão antes de dar veredito. A diferença observada entre proxy e
  leitura foi de 15 a 25 pontos percentuais.

### O enquadramento honesto, que vai no relatório

Estes marcadores **não provam autoria por IA**. Um humano apressado produz todos
eles; um texto assistido e bem revisado não produz nenhum. O que eles medem de
fato é **escrita fraca**: previsibilidade estrutural, ênfase artificial e
afirmação sem lastro. Reporte-os como defeito de redação, que é o que se
sustenta, e não como acusação de autoria, que não se sustenta.

Isso é o que torna o achado acionável: "cinco conectores neste parágrafo" é
corrigível e indiscutível; "provavelmente escrito por IA" é indefensável e
ofensivo se errado.

### Prioridade: o que vai ser reescrito de qualquer jeito

Se o usuário já sabe que certas seções serão reescritas, peça a lista antes de
disparar e **separe os achados em dois grupos**:

- **Corrigir** — o que está em seção que sobrevive. Exige ação.
- **Evitar na escrita nova** — o que está em seção condenada. Não vale corrigir;
  vale como padrão a não repetir no texto que vem.

Sem essa separação o relatório manda reescrever o que já ia ser reescrito, e o
usuário gasta atenção à toa.

### Três coisas que esta skill deliberadamente não faz

**Não emite uma porcentagem única de probabilidade.** Somar notas de critérios e
multiplicar por uma constante produz um número de aparência científica sem
validação por trás: não há calibração contra corpus rotulado, os critérios não
são independentes, e o resultado varia com o revisor. Reporte as contagens
contra os limiares e deixe o leitor concluir. Se o usuário pedir explicitamente
o número composto, entregue — e registre no relatório que ele não é uma
probabilidade calibrada.

**Não cola o manuscrito em serviço de terceiros.** Enviar trabalho não publicado
para uma API externa o expõe: pode ser retido, cacheado ou indexado, e em
submissão sob revisão cega isso é um problema real. A varredura roda localmente,
sobre o arquivo. Se o usuário quiser usar um detector externo, é decisão dele — e
vale avisar antes que a decisão está sendo tomada.

**Não audita conduta.** Este estágio diagnostica **o texto**. Não infere quem
escreveu, não avalia se a declaração de uso de IA do manuscrito é suficiente, e
não cruza o texto com o histórico do projeto para levantar essa pergunta. É uma
questão real e é do autor, mas é de outra natureza — sai de "a redação tem estes
defeitos" e entra em "a conduta declarada tem esta lacuna", sem que o usuário
tenha pedido a segunda. Se o usuário quiser essa análise, ela se pede
explicitamente e roda separada.

---

## Estágio 4 — Síntese global

Feito por você, no contexto principal, depois que todos os revisores voltarem.

1. **Deduplique.** O mesmo defeito visto de dois segmentos vira um achado, com as duas localizações.
2. **Derrube o infundado.** Achado sem citação literal, ou cuja citação não confere com o texto real, é descartado — não rebaixado, descartado. Abra o arquivo e confirme por amostragem os achados `CRÍTICO` e `ALTO`.
3. **Verifique a fundamentação.** Para achados que dependem de fato externo (uma referência existe? um número bate com os dados?), confirme você mesmo antes de reportar. Use WebSearch para literatura, leitura de arquivo para dados. Isto é o `search grounding` do PAT.
4. **Reordene por severidade real**, não pela ordem dos segmentos.
5. **Separe erro de melhoria.** Duas listas distintas: o que está errado e o que ficaria melhor.

### Saída

Grave em `revisoes/revisao_<nome-do-manuscrito>_<AAAA-MM-DD>.md`, ao lado do manuscrito, e resuma no chat apenas os `CRÍTICO` e `ALTO`.

```markdown
# Revisão pré-submissão — <manuscrito>
<data> · <N> segmentos · <N> revisores · <N> achados após deduplicação

## Veredito
<2-4 frases: o que impede a submissão hoje, se algo impede.>

## Erros
### [CRÍTICO] <título curto>
**Onde:** arquivo:linha
**Texto:** "<citação literal>"
**Defeito:** <uma frase>
**Confiança:** CONFIRMADO — <como foi verificado>
**Eu estaria errado se:** <uma linha>
**Correção sugerida:** <acionável>

## Melhorias
<mesma estrutura, sem severidade>

## Verificado e limpo
<lista curta do que foi checado e não apresentou problema — números conferidos contra dados, citações batidas contra o .bib. Serve para o usuário saber o que NÃO precisa reconferir à mão.>
```

---

## Notas de operação

- Manuscrito curto (< ~15 páginas) pode ir com 4-5 segmentos. Tese ou artigo longo pede 8-10.
- Se o usuário pedir foco (`só a estatística`), reduza os segmentos ao escopo pedido e diga explicitamente no relatório o que ficou de fora.
- Se houver auditoria anterior, o relatório precisa dizer quais achados são **novos** e quais **reincidem**.
- Rodar de novo depois das correções é barato e é o uso pretendido. O PAT deu uma rodada por manuscrito; esta skill não tem esse limite.
