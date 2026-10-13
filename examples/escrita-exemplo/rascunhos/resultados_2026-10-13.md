# Rascunho do segmento Resultados (2026-10-13)

Rascunho para revisão humana. Não é texto final. A Parte A é insumo interno e não vai para o manuscrito; só a Parte B é candidata à mesclagem em `artigo.md`.

## Parte A. Mapa de fontes

Fontes usadas, e somente elas: `dados/r2/metricas.json` e `dados/r2/testes.json`.

### A.1 Subseção 3.1 (acurácia geral)

| Valor no texto | Arquivo | Campo | Direto ou derivado |
|---|---|---|---|
| 1.200 itens | `dados/r2/metricas.json` | `n_itens`; `geral.<arq>.n` | direto |
| linha de base: 949 acertos | `dados/r2/metricas.json` | `geral.bm25.acertos` | direto |
| linha de base: 79,1% | `dados/r2/metricas.json` | `geral.bm25.acuracia_pct` | direto |
| linha de base: IC95% [76,8; 81,4] | `dados/r2/metricas.json` | `geral.bm25.ic95_pct` | direto |
| densa: 979 acertos | `dados/r2/metricas.json` | `geral.densa.acertos` | direto |
| densa: 81,6% | `dados/r2/metricas.json` | `geral.densa.acuracia_pct` | direto |
| densa: IC95% [79,4; 83,8] | `dados/r2/metricas.json` | `geral.densa.ic95_pct` | direto |
| híbrida: 1.012 acertos | `dados/r2/metricas.json` | `geral.hibrida.acertos` | direto |
| híbrida: 84,3% | `dados/r2/metricas.json` | `geral.hibrida.acuracia_pct` | direto |
| híbrida: IC95% [82,1; 86,5] | `dados/r2/metricas.json` | `geral.hibrida.ic95_pct` | direto |
| híbrida menos linha de base: 5,2 p.p. | `dados/r2/metricas.json` | `geral.hibrida.acuracia_pct`, `geral.bm25.acuracia_pct` | derivado: 84,3 - 79,1 = 5,2 |
| híbrida menos densa: 2,7 p.p. | `dados/r2/metricas.json` | `geral.hibrida.acuracia_pct`, `geral.densa.acuracia_pct` | derivado: 84,3 - 81,6 = 2,7 |
| densa menos linha de base: 2,5 p.p. | `dados/r2/metricas.json` | `geral.densa.acuracia_pct`, `geral.bm25.acuracia_pct` | derivado: 81,6 - 79,1 = 2,5 |

### A.2 Subseção 3.2 (comparações par a par)

| Valor no texto | Arquivo | Campo | Direto ou derivado |
|---|---|---|---|
| teste de McNemar | `dados/r2/testes.json` | `teste` | direto |
| correção de Bonferroni | `dados/r2/testes.json` | `correcao` | direto |
| três comparações | `dados/r2/testes.json` | `n_comparacoes` | direto |
| alfa nominal 0,05 | `dados/r2/testes.json` | `alfa_nominal` | direto |
| limiar corrigido 0,0167 | `dados/r2/testes.json` | `alfa_corrigido` | direto |
| híbrida e linha de base: p = 0,0004 | `dados/r2/testes.json` | `comparacoes[0].p_valor` (par `["hibrida","bm25"]`) | direto |
| híbrida e linha de base: abaixo do limiar corrigido | `dados/r2/testes.json` | `comparacoes[0].significativo_apos_correcao` = true | direto |
| híbrida e densa: p = 0,012 | `dados/r2/testes.json` | `comparacoes[1].p_valor` (par `["hibrida","densa"]`) | direto |
| híbrida e densa: abaixo do limiar corrigido | `dados/r2/testes.json` | `comparacoes[1].significativo_apos_correcao` = true | direto |
| densa e linha de base: p = 0,041 | `dados/r2/testes.json` | `comparacoes[2].p_valor` (par `["densa","bm25"]`) | direto |
| densa e linha de base: acima do limiar corrigido | `dados/r2/testes.json` | `comparacoes[2].significativo_apos_correcao` = false | direto |
| duas das três comparações | `dados/r2/testes.json` | `comparacoes[*].significativo_apos_correcao` | derivado: contagem de valores true (2 de 3) |
| diferenças de 5,2, 2,7 e 2,5 p.p. retomadas | `dados/r2/metricas.json` | ver A.1 | derivado, ver A.1 |

### A.3 Subseção 3.3 (acurácia por complexidade)

| Valor no texto | Arquivo | Campo | Direto ou derivado |
|---|---|---|---|
| 780 itens simples | `dados/r2/metricas.json` | `por_complexidade.simples.n` | direto |
| 420 itens complexos | `dados/r2/metricas.json` | `por_complexidade.complexa.n` | direto |
| simples, linha de base: 655 acertos; 84,0% | `dados/r2/metricas.json` | `por_complexidade.simples.bm25.acertos`; `.acuracia_pct` | direto |
| simples, densa: 671 acertos; 86,0% | `dados/r2/metricas.json` | `por_complexidade.simples.densa.acertos`; `.acuracia_pct` | direto |
| simples, híbrida: 684 acertos; 87,7% | `dados/r2/metricas.json` | `por_complexidade.simples.hibrida.acertos`; `.acuracia_pct` | direto |
| complexos, linha de base: 294 acertos; 70,0% | `dados/r2/metricas.json` | `por_complexidade.complexa.bm25.acertos`; `.acuracia_pct` | direto |
| complexos, densa: 308 acertos; 73,3% | `dados/r2/metricas.json` | `por_complexidade.complexa.densa.acertos`; `.acuracia_pct` | direto |
| complexos, híbrida: 328 acertos; 78,1% | `dados/r2/metricas.json` | `por_complexidade.complexa.hibrida.acertos`; `.acuracia_pct` | direto |
| linha de base, simples menos complexos: 14,0 p.p. | `dados/r2/metricas.json` | `por_complexidade.simples.bm25.acuracia_pct`, `por_complexidade.complexa.bm25.acuracia_pct` | derivado: 84,0 - 70,0 = 14,0 |
| densa, simples menos complexos: 12,7 p.p. | `dados/r2/metricas.json` | `por_complexidade.simples.densa.acuracia_pct`, `por_complexidade.complexa.densa.acuracia_pct` | derivado: 86,0 - 73,3 = 12,7 |
| híbrida, simples menos complexos: 9,6 p.p. | `dados/r2/metricas.json` | `por_complexidade.simples.hibrida.acuracia_pct`, `por_complexidade.complexa.hibrida.acuracia_pct` | derivado: 87,7 - 78,1 = 9,6 |
| simples, híbrida menos linha de base: 3,7 p.p. | `dados/r2/metricas.json` | `por_complexidade.simples.hibrida.acuracia_pct`, `por_complexidade.simples.bm25.acuracia_pct` | derivado: 87,7 - 84,0 = 3,7 |
| complexos, híbrida menos linha de base: 8,1 p.p. | `dados/r2/metricas.json` | `por_complexidade.complexa.hibrida.acuracia_pct`, `por_complexidade.complexa.bm25.acuracia_pct` | derivado: 78,1 - 70,0 = 8,1 |

### A.4 Subseção 3.4 (latência)

Nenhum valor de latência consta em `dados/r2/metricas.json` nem em `dados/r2/testes.json`. Nenhum número foi escrito.

### A.5 Conferências de consistência interna feitas sobre os artefatos

Todas fecham; nenhuma dessas contas aparece no texto além do que está listado acima.

- Acertos por estrato somam o total geral: 655 + 294 = 949; 671 + 308 = 979; 684 + 328 = 1.012.
- Tamanhos dos estratos somam o total: 780 + 420 = 1.200.
- Cada `acuracia_pct` coincide com acertos/n arredondado a uma casa decimal (geral e por complexidade).
- `alfa_corrigido` coincide com 0,05 / 3 arredondado a quatro casas (0,0167).
- Cada `significativo_apos_correcao` é coerente com a comparação entre `p_valor` e `alfa_corrigido`.

### A.6 Marcadores deixados em aberto

| Marcador | Onde | Motivo |
|---|---|---|
| `[VERIFICAR: latência média por consulta da linha de base ...]` | 3.4 | valor ausente dos dois artefatos canônicos |
| `[VERIFICAR: latência média por consulta da arquitetura densa ...]` | 3.4 | idem |
| `[VERIFICAR: latência média por consulta da arquitetura híbrida ...]` | 3.4 | idem |
| `[VERIFICAR: unidade, hardware e condição de medição ...]` | 3.4 | os artefatos não trazem protocolo de medição de latência; a seção 2.4 do manuscrito também não descreve um |

Nenhum `[CITAÇÃO NECESSÁRIA]` foi deixado: a seção não cita literatura.

## Parte B. Texto da seção

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

A ordenação das arquiteturas observada no conjunto completo se repete nos dois estratos: a arquitetura híbrida apresenta a maior acurácia, seguida pela densa e pela linha de base. A distância entre a arquitetura híbrida e a linha de base é de 3,7 pontos percentuais nos itens simples e de 8,1 pontos percentuais nos itens complexos. As diferenças por estrato são reportadas de forma descritiva: os testes da Seção 3.2 foram aplicados ao conjunto completo, e não a cada estrato.

### 3.4 Latência por consulta

A latência média por consulta foi de [VERIFICAR: latência média por consulta da linha de base (BM25); valor ausente de `dados/r2/metricas.json` e de `dados/r2/testes.json`; provavelmente em log de execução ou arquivo de tempos da mesma execução que gerou as métricas] para a linha de base, de [VERIFICAR: latência média por consulta da arquitetura densa; mesma fonte provável] para a arquitetura densa e de [VERIFICAR: latência média por consulta da arquitetura híbrida; mesma fonte provável] para a arquitetura híbrida. [VERIFICAR: unidade, hardware e condição de medição da latência (número de execuções, inclusão ou não do tempo de codificação da consulta); nenhum dos dois artefatos canônicos registra esse protocolo, e a Seção 2.4 não o descreve.]
