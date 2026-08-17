# Revisão pré-submissão — manuscrito-exemplo.md

2026-08-17 · 5 segmentos · 5 revisores + 1 de assinatura de linguagem · 9 achados após deduplicação

> Relatório produzido pelo `paper-reviewer` sobre [`manuscrito-exemplo.md`](manuscrito-exemplo.md),
> um manuscrito **sintético** com defeitos plantados. Os números do Estágio 3.5
> são medidos, não ilustrativos.

## Veredito

Dois problemas impedem a submissão hoje. O primeiro é uma inconsistência
numérica entre o resumo e a Tabela 1 no resultado principal do artigo. O segundo
é de validade: a Seção 4 apresenta como achado empírico um padrão que a
definição da Seção 3.3 garante por construção. Há ainda uma pergunta de pesquisa
declarada e nunca respondida, e uma contribuição declarada e nunca entregue.

---

## Erros

### [CRÍTICO] O número principal do artigo diverge entre resumo e tabela

**Onde:** `manuscrito-exemplo.md:16` e `manuscrito-exemplo.md:90`
**Texto:** "atingindo acurácia de 87,3% contra 79,1% da linha de base" (resumo)
versus "| Híbrida | 84,3% | [82,1, 86,5] |" (Tabela 1)
**Defeito:** O resumo reporta 87,3% e a tabela reporta 84,3% para a mesma
condição. A diferença declarada em relação à linha de base (5,2 pontos, linha 93)
confere com a tabela, não com o resumo.
**Confiança:** CONFIRMADO — 84,3 − 79,1 = 5,2, que é o valor no corpo do texto.
O resumo é o valor divergente.
**Eu estaria errado se:** o resumo se referisse a outra métrica ou a outro
recorte do conjunto, o que o texto não indica em nenhum momento.
**Correção sugerida:** corrigir o resumo para 84,3% e conferir todas as demais
ocorrências do número no manuscrito.

### [CRÍTICO] Achado garantido por construção apresentado como descoberta empírica

**Onde:** `manuscrito-exemplo.md:96`, definição em `:76`
**Texto:** "consultas classificadas como complexas mencionam, em média, 3,4
entidades técnicas, enquanto consultas simples mencionam 1,6. Esse achado
evidencia que a complexidade de consulta está de fato associada à densidade de
entidades."
**Defeito:** A Seção 3.3 define complexa como "mais de duas entidades técnicas
distintas". A regra de classificação **é** a densidade de entidades. Que o grupo
"mais de duas" tenha média superior ao grupo "até duas" é consequência
aritmética da definição, não resultado. Isto é problema de validade, não de
redação: um parecerista atento aponta.
**Confiança:** CONFIRMADO — verificado contra a definição no próprio manuscrito.
**Eu estaria errado se:** a densidade de entidades tivesse sido medida por um
instrumento independente da regra de partição, o que o texto não descreve.
**Correção sugerida:** remover a frase, ou substituí-la por uma validação da
definição contra um critério externo (julgamento de especialista, tempo de
resposta, taxa de acerto humano).

### [ALTO] Alegação causal sustentada por evidência comparativa

**Onde:** `manuscrito-exemplo.md:15`, `:117`
**Texto:** "a arquitetura híbrida causa melhora significativa no desempenho"
**Defeito:** O desenho é uma comparação de desempenho entre três arquiteturas
sobre o mesmo conjunto. Isso sustenta "obteve desempenho superior", não "causa
melhora". Nenhuma intervenção foi manipulada e nenhum mecanismo foi isolado.
**Confiança:** CONFIRMADO — o protocolo da Seção 3.4 descreve avaliação
comparativa, sem desenho causal.
**Eu estaria errado se:** houvesse um experimento de ablação isolando o
componente responsável, o que não consta.
**Correção sugerida:** trocar "causa melhora significativa" por "apresentou
desempenho superior" nas duas ocorrências.

### [ALTO] Pergunta de pesquisa declarada e nunca respondida

**Onde:** `manuscrito-exemplo.md:38`
**Texto:** "**PP3.** Qual o custo computacional relativo de cada arquitetura em
produção?"
**Defeito:** Nenhuma seção do manuscrito reporta custo computacional, latência,
memória ou throughput. PP1 e PP2 são respondidas; PP3 é abandonada.
**Confiança:** CONFIRMADO — varredura completa do manuscrito por termos de custo.
**Eu estaria errado se:** os dados de custo estivessem em material suplementar
referenciado, o que o texto não faz.
**Correção sugerida:** reportar os dados de custo, ou remover PP3 do escopo
declarado.

### [ALTO] Contribuição declarada e não entregue

**Onde:** `manuscrito-exemplo.md:42`
**Texto:** "(iii) um conjunto de consultas anotadas disponibilizado publicamente"
**Defeito:** Não há link, DOI, repositório, licença nem declaração de
disponibilidade em nenhum ponto do manuscrito.
**Confiança:** CONFIRMADO.
**Eu estaria errado se:** a disponibilização estivesse condicionada à aceitação
do artigo, caso em que isso precisa estar escrito.
**Correção sugerida:** incluir o endereço e a licença do conjunto, ou retirar a
contribuição da lista.

### [MÉDIO] Generalização além das condições testadas

**Onde:** `manuscrito-exemplo.md:19`, `:119`
**Texto:** "a adoção de recuperação híbrida é sempre recomendável em domínios
especializados"
**Defeito:** Foi avaliado um domínio, um conjunto de consultas e uma métrica. O
advérbio "sempre" e o plural "domínios" projetam uma generalidade que o desenho
não sustenta.
**Confiança:** CONFIRMADO.
**Eu estaria errado se:** houvesse avaliação em mais de um domínio.
**Correção sugerida:** "foi a alternativa mais eficaz no domínio avaliado".

### [MÉDIO] Seção de trabalhos relacionados sem uma única citação

**Onde:** `manuscrito-exemplo.md:46-56`
**Texto:** "Trabalhos seminais estabeleceram que representações aprendidas
superam métodos léxicos em domínio aberto."
**Defeito:** A seção inteira atribui afirmações a "trabalhos seminais",
"estudos posteriores" e "trabalhos recentes" sem nenhuma referência. Cada uma
dessas afirmações é verificável e precisa de fonte.
**Confiança:** CONFIRMADO.
**Eu estaria errado se:** o sistema de citação estivesse sendo aplicado em etapa
posterior de formatação, o que ainda assim precisaria de marcadores.
**Correção sugerida:** citar as fontes de cada afirmação atribuída.

### [MÉDIO] Interpretação declarada como sustentada sem teste correspondente

**Onde:** `manuscrito-exemplo.md:112`
**Texto:** "Essa interpretação é claramente sustentada pelos dados."
**Defeito:** A interpretação oferecida (dispersão de entidades dificulta a
formação de representação única) é uma hipótese de mecanismo. Os dados mostram
queda de desempenho em consultas complexas, o que é compatível com essa
hipótese e com várias outras.
**Confiança:** CONFIRMADO.
**Eu estaria errado se:** houvesse análise de representações que discriminasse
essa hipótese das concorrentes.
**Correção sugerida:** "é compatível com os dados", e enunciar ao menos uma
explicação alternativa.

### [MÉDIO] Limitação ausente

**Onde:** seção 5 e 6
**Defeito:** O manuscrito não reconhece nenhuma ameaça à validade. As mais
evidentes: domínio único, conjunto de consultas único, ausência de teste de
significância entre arquiteturas (os intervalos de confiança de Densa e Híbrida
se sobrepõem: [79,4, 83,8] e [82,1, 86,5]).
**Confiança:** CONFIRMADO — sobreposição verificada na Tabela 1.
**Eu estaria errado se:** houvesse seção de limitações que eu não localizei.
**Correção sugerida:** incluir seção de limitações e reportar teste pareado
entre as arquiteturas.

---

## Estágio 3.5 — Assinatura de linguagem automatizada

Medido sobre o manuscrito inteiro: 767 palavras, 40 sentenças, 21 parágrafos.

### Faixa A — raspáveis

| Critério | Medido | Limiar | Dispara |
|---|---|---|---|
| A1 conectores encabeçando frase | 10 no total, máx. 4 por parágrafo | > 4 por parágrafo | não |
| A2 absolutismo lexical | 3,91 por 1.000 palavras | 8,57 | não |
| A3 travessão longo | 0 | > 0 | não |

**A1, A2 e A3 não disparam. São raspáveis por busca-e-substitui e, portanto,
não-diagnósticos quando passam: a contagem baixa não licencia nenhuma
inferência.** Um texto com estes três limpos pode ser bem escrito ou ter sido
raspado na véspera, e a medição não separa os dois casos.

Sub-achado que a Faixa A não pega: **4 intensificadores, 3 deles sem lastro
numérico** (*amplamente* ×2, *sistematicamente*, *substancialmente*). Quem raspa
absolutismo raramente raspa isto.

### Faixa B — resistentes

| Critério | Medido | Limiar | Dispara |
|---|---|---|---|
| B1 simetria de template | CV 0,560 global; 0,455 no pior bloco (Introdução) | < 0,30 | não |
| B2 redundância semântica | 3 cadeias de 8+ palavras repetidas | qualquer | **sim** |
| B4 hipotaxe inflacionada | 0 sentenças acima de 60 palavras (máx. 59) | > 0 | não |
| B5 frame retórico único | nenhum frame dominante | > 20% | não |
| B6 voz autoral ausente | 81,0% dos parágrafos (17 de 21) | > 70% | **sim** |
| B7 conclusão tautológica | 17,4% de sobreposição com o corpo | qualquer | **sim** |
| B8 ritmo robótico | CV do comprimento de sentença 0,606 | < 0,30 | não |

**B2.** A cadeia mais longa repetida é *"os resultados demonstram que a
arquitetura híbrida causa melhora significativa"*, presente no resumo (linha 15)
e nas Considerações Finais (linha 117), praticamente idêntica. Note que esta
cadeia contém o achado [ALTO] da alegação causal: o mesmo erro aparece duas
vezes porque a conclusão foi copiada do resumo.

**B6.** 17 de 21 parágrafos relatam sem posicionar. **Este número é de proxy
automático e super-marca**: a medição não reconhece posicionamento indireto. A
diferença observada entre proxy e leitura humana é de 15 a 25 pontos
percentuais. Use para localizar parágrafos, não para dar veredito.

**B7.** A conclusão reformula o resumo sem acrescentar leitura. Combinado com
B2, indica que a Seção 6 foi construída por reciclagem em vez de síntese.

### Enquadramento

Estes marcadores **não provam autoria por IA**. Um humano apressado produz todos
eles; um texto assistido e bem revisado não produz nenhum. O que eles medem é
escrita fraca: previsibilidade estrutural, ênfase artificial e afirmação sem
lastro. É assim que devem ser reportados, porque é o que se sustenta e é o que é
acionável.

---

## Melhorias

- **Tabela 1 sem teste de significância.** Os intervalos de Densa e Híbrida se
  sobrepõem. Um teste pareado entre arquiteturas tornaria a comparação
  defensável.
- **A definição de complexidade merece validação externa**, independentemente da
  correção do achado tautológico. Uma definição operacional só é útil se
  corresponder a alguma dificuldade real.
- **A Seção 5 tem dois parágrafos para três resultados.** O efeito da
  arquitetura densa isolada não é discutido em nenhum momento.

---

## Verificado e limpo

- Aritmética da diferença entre linha de base e híbrida (5,2 pp) confere com a
  Tabela 1.
- Todos os intervalos de confiança da Tabela 1 são simétricos em torno do ponto
  estimado e internamente consistentes.
- A contagem de consultas (1.200) é consistente entre o resumo e a Seção 3.2.
- Nenhuma referência inventada foi detectada, porque não há nenhuma referência.
