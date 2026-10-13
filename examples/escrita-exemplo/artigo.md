# Avaliação de Arquiteturas de Recuperação em Domínio Técnico Especializado

> **MANUSCRITO SINTÉTICO.** Este texto não é um artigo real e não descreve
> pesquisa real. Foi escrito para demonstrar o `paper-writer`. Nenhum dado,
> número ou referência aqui é verdadeiro. Ver `README.md` nesta pasta.

## 1. Introdução

Sistemas de geração aumentada por recuperação (em inglês, *Retrieval-Augmented
Generation*, RAG) combinam um componente de busca com um modelo de linguagem, o
que permite respostas fundamentadas em documentos externos. Em domínios técnicos
especializados, a terminologia é densa, os documentos são longos e a
sobreposição léxica entre consulta e documento relevante é baixa.

Este trabalho investiga duas perguntas de pesquisa:

- **PP1.** Qual arquitetura de recuperação apresenta melhor desempenho em domínio
  técnico especializado?
- **PP2.** Como a complexidade da consulta afeta o desempenho de recuperação?

## 2. Método

### 2.1 Arquiteturas avaliadas

Foram avaliadas três arquiteturas: recuperação léxica baseada em BM25, adotada
como linha de base; recuperação densa com codificador bi-encoder; e recuperação
híbrida, que combina as duas por soma ponderada dos escores normalizados.

### 2.2 Conjunto de consultas

O conjunto é composto por 1.200 consultas em domínio técnico, anotadas por dois
especialistas, com resolução de discordância por um terceiro. Cada item possui
ao menos um documento relevante identificado.

### 2.3 Definição de complexidade

Um item é classificado como **complexo** quando menciona mais de duas entidades
técnicas distintas, e como **simples** caso contrário.

### 2.4 Protocolo

Todas as arquiteturas foram avaliadas sobre o mesmo conjunto, com os mesmos
documentos indexados e hiperparâmetros fixados previamente. A métrica principal
é a acurácia de recuperação no topo-5. As arquiteturas foram comparadas par a
par pelo teste de McNemar, com correção de Bonferroni para três comparações.

## 3. Resultados

<!-- A ESCREVER. A seção deve cobrir, nesta ordem:
     (a) acurácia no topo-5 e IC95% das três arquiteturas, em tabela;
     (b) comparações par a par e o que sobrevive à correção de Bonferroni;
     (c) acurácia por complexidade da consulta, em tabela;
     (d) latência média por consulta de cada arquitetura. -->

## 4. Discussão

<!-- A ESCREVER, depois dos Resultados. -->
