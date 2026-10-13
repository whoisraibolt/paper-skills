# Rascunho consolidado: seção 3 (Resultados), 2026-10-13

Rascunho para revisão humana. Não é texto final e **não foi mesclado** em `artigo.md`.

## Estado da checagem do Estágio 4

- **Regra 1 (só artefato canônico):** atendida. Fontes usadas: `dados/r2/metricas.json` e `dados/r2/testes.json`. Nada sob `dados/r1/` foi lido.
- **Regra 2 (sem narrativa de processo):** atendida. O texto da seção não menciona rodadas.
- **Regra 3 (nenhum número sem fonte):** atendida para 3.1 a 3.3; o mapa valor a valor está em `rascunhos/resultados_2026-10-13.md`, Parte A. Todos os valores das Tabelas 1 e 2, os três p-valores, o limiar corrigido e as oito diferenças derivadas foram reconferidos no contexto principal contra os dois artefatos e fecham.
- **Regra 4 (nenhuma citação inventada):** atendida. A seção não cita literatura.
- **Bloqueio de mesclagem:** quatro marcadores `[VERIFICAR]` pendentes na subseção 3.4. Enquanto existirem, a seção não entra em `artigo.md`.

## Pendências a resolver pela autora antes da mesclagem

1. **Latência (item d do roteiro da seção).** Nenhum artefato canônico do config traz latência. Faltam os três valores médios por consulta e o protocolo de medição (unidade, hardware, número de execuções, inclusão ou não do tempo de codificação da consulta). Para resolver: declarar no config o arquivo que contém esses valores, ou retirar o item (d) do roteiro. Se a latência ficar, a Seção 2.4 precisa de uma frase sobre como foi medida.
2. **Método do IC95%.** Os artefatos trazem os intervalos, mas não o método (Wald, Wilson, bootstrap), e a Seção 2.4 também não o nomeia.
3. **Estatística do McNemar.** `dados/r2/testes.json` traz apenas p-valores, sem estatística de teste nem contagens discordantes. Nada foi derivado.
4. **Sigla IC95%.** Escrita como "intervalo de confiança de 95% (IC95%)", sem o formato "em inglês, English Name, ACRONYM", por ser sigla em português. Ajustar se a regra do guia de voz valer também para ela.

## Alteração feita na consolidação

Na última frase de 3.3, o rascunho do segmento afirmava que os testes de McNemar "foram aplicados ao conjunto completo, e não a cada estrato". `dados/r2/testes.json` não declara o escopo dos testes, de modo que a afirmação era inferência sem fonte. A frase foi reduzida ao que os artefatos sustentam: não há teste por estrato reportado.

---

## 3. Resultados

### 3.1 Acurácia de recuperação no topo-5

A Tabela 1 apresenta o número de acertos, a acurácia de recuperação no topo-5 e o intervalo de confiança de 95% (IC95%) de cada arquitetura sobre os 1.200 itens do conjunto.

**Tabela 1.** Acurácia de recuperação no topo-5 por arquitetura (n = 1.200 itens).

| Arquitetura | Acertos | Acurácia no topo-5 (%) | IC95% (%) |
|---|---|---|---|
| BM25 (linha de base) | 949 | 79,1 | [76,8; 81,4] |
| Densa | 979 | 81,6 | [79,4; 83,8] |
| Híbrida | 1.012 | 84,3 | [82,1; 86,5] |

Fonte: Elaborado pela autora.

Como visto na Tabela 1, a arquitetura híbrida obteve a maior acurácia no topo-5, 84,3% (IC95%: 82,1 a 86,5), seguida pela arquitetura densa, com 81,6% (IC95%: 79,4 a 83,8), e pela linha de base, com 79,1% (IC95%: 76,8 a 81,4). A diferença entre a arquitetura híbrida e a linha de base é de 5,2 pontos percentuais; entre a híbrida e a densa, de 2,7 pontos percentuais; e entre a densa e a linha de base, de 2,5 pontos percentuais.

### 3.2 Comparações par a par

As três arquiteturas foram comparadas par a par pelo teste de McNemar, com correção de Bonferroni para três comparações. O alfa nominal de 0,05 resulta em um limiar corrigido de 0,0167.

Duas das três comparações ficam abaixo do limiar corrigido. A diferença de 5,2 pontos percentuais entre a arquitetura híbrida e a linha de base é estatisticamente significativa após a correção (p = 0,0004; limiar corrigido de 0,0167). O mesmo ocorre com a diferença de 2,7 pontos percentuais entre a arquitetura híbrida e a arquitetura densa (p = 0,012; limiar corrigido de 0,0167).

A diferença de 2,5 pontos percentuais entre a arquitetura densa e a linha de base não atinge o limiar corrigido (p = 0,041; limiar corrigido de 0,0167). O p-valor dessa comparação é inferior ao alfa nominal de 0,05, mas superior ao limiar corrigido, de modo que os dados não permitem afirmar diferença entre a arquitetura densa e a linha de base sob o critério adotado.

### 3.3 Acurácia por complexidade da consulta

Dos 1.200 itens, 780 são classificados como simples e 420 como complexos, conforme a definição da Seção 2.3. A Tabela 2 apresenta os acertos e a acurácia no topo-5 de cada arquitetura em cada um dos dois estratos.

**Tabela 2.** Acurácia de recuperação no topo-5 por arquitetura e por complexidade da consulta.

| Arquitetura | Acertos, itens simples (n = 780) | Acurácia, itens simples (%) | Acertos, itens complexos (n = 420) | Acurácia, itens complexos (%) |
|---|---|---|---|---|
| BM25 (linha de base) | 655 | 84,0 | 294 | 70,0 |
| Densa | 671 | 86,0 | 308 | 73,3 |
| Híbrida | 684 | 87,7 | 328 | 78,1 |

Fonte: Elaborado pela autora.

Como visto na Tabela 2, as três arquiteturas apresentam acurácia menor nos itens complexos do que nos itens simples. A diferença entre os dois estratos é de 14,0 pontos percentuais na linha de base (84,0% e 70,0%), de 12,7 pontos percentuais na arquitetura densa (86,0% e 73,3%) e de 9,6 pontos percentuais na arquitetura híbrida (87,7% e 78,1%).

A ordenação das arquiteturas observada no conjunto completo se repete nos dois estratos: a arquitetura híbrida apresenta a maior acurácia, seguida pela densa e pela linha de base. A distância entre a arquitetura híbrida e a linha de base é de 3,7 pontos percentuais nos itens simples e de 8,1 pontos percentuais nos itens complexos. As diferenças por estrato são reportadas de forma descritiva, sem teste de hipótese por estrato.

### 3.4 Latência por consulta

A latência média por consulta foi de [VERIFICAR: latência média por consulta da linha de base (BM25); valor ausente dos dois artefatos canônicos declarados no config; provavelmente em log de execução ou arquivo de tempos ainda não declarado como artefato canônico] para a linha de base, de [VERIFICAR: latência média por consulta da arquitetura densa; mesma fonte provável] para a arquitetura densa e de [VERIFICAR: latência média por consulta da arquitetura híbrida; mesma fonte provável] para a arquitetura híbrida. [VERIFICAR: unidade, hardware e condição de medição da latência (número de execuções, inclusão ou não do tempo de codificação da consulta); nenhum dos dois artefatos canônicos registra esse protocolo, e a Seção 2.4 não o descreve.]
