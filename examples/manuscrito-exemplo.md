# Avaliação de Arquiteturas de Recuperação em Domínio Técnico Especializado

> **MANUSCRITO SINTÉTICO.** Este texto não é um artigo real e não descreve
> pesquisa real. Foi escrito para demonstrar o `paper-reviewer`, com defeitos
> plantados deliberadamente. Nenhum dado, número ou referência aqui é verdadeiro.
> Ver `revisao-exemplo.md` para o relatório que a skill produz sobre ele.

## Resumo

A geração aumentada por recuperação tem sido amplamente adotada em sistemas de
pergunta e resposta. Contudo, seu comportamento em domínios técnicos
especializados permanece pouco compreendido. Além disso, a literatura raramente
examina o efeito da complexidade da consulta sobre o desempenho de recuperação.
Este trabalho avalia três arquiteturas de recuperação sobre um conjunto de 1.200
consultas em domínio técnico. Os resultados demonstram que a arquitetura híbrida
causa melhora significativa no desempenho, atingindo acurácia de 87,3% contra
79,1% da linha de base. Vale destacar que consultas complexas apresentaram
desempenho claramente inferior. Portanto, conclui-se que a adoção de recuperação
híbrida é sempre recomendável em domínios especializados.

## 1. Introdução

Sistemas de geração aumentada por recuperação combinam um componente de busca
com um modelo de linguagem, permitindo respostas fundamentadas em documentos
externos. Essa abordagem tem sido amplamente adotada, e sua eficácia em domínios
gerais está bem documentada.

Entretanto, domínios técnicos especializados impõem desafios adicionais. A
terminologia é densa, os documentos são longos e a sobreposição léxica entre
consulta e documento relevante é frequentemente baixa. Em outras palavras, o
cenário é sistematicamente mais difícil que o de domínio aberto.

Este trabalho investiga três perguntas de pesquisa:

- **PP1.** Qual arquitetura de recuperação apresenta melhor desempenho em domínio
  técnico especializado?
- **PP2.** Como a complexidade da consulta afeta o desempenho de recuperação?
- **PP3.** Qual o custo computacional relativo de cada arquitetura em produção?

As contribuições são: (i) uma comparação controlada de três arquiteturas; (ii)
uma caracterização do efeito da complexidade de consulta; e (iii) um conjunto de
consultas anotadas disponibilizado publicamente.

## 2. Trabalhos Relacionados

A literatura sobre recuperação densa consolidou-se na última década. Trabalhos
seminais estabeleceram que representações aprendidas superam métodos léxicos em
domínio aberto. Por outro lado, estudos posteriores demonstraram que métodos
léxicos permanecem competitivos quando há vocabulário técnico especializado.

Trabalhos recentes propuseram arquiteturas híbridas, que combinam pontuação
léxica e densa. Contudo, a avaliação dessas propostas concentra-se em conjuntos
de dados de domínio aberto, e a transferência para domínios especializados
permanece pouco investigada. Esta lacuna motiva o presente trabalho.

## 3. Método

### 3.1 Arquiteturas avaliadas

Foram avaliadas três arquiteturas: recuperação léxica baseada em BM25;
recuperação densa com codificador bi-encoder; e recuperação híbrida, que combina
as duas por soma ponderada dos escores normalizados.

### 3.2 Conjunto de consultas

O conjunto é composto por 1.200 consultas em domínio técnico, anotadas por dois
especialistas com resolução de discordância por um terceiro. Cada consulta possui
ao menos um documento relevante identificado.

### 3.3 Definição de complexidade

Uma consulta é classificada como **complexa** quando menciona mais de duas
entidades técnicas distintas, e como **simples** caso contrário. Essa definição
permite particionar o conjunto de forma objetiva e reprodutível.

### 3.4 Protocolo

Todas as arquiteturas foram avaliadas sobre o mesmo conjunto, com os mesmos
documentos indexados. Os hiperparâmetros foram fixados previamente. A métrica
principal é a acurácia de recuperação no topo-5.

## 4. Resultados

A Tabela 1 apresenta o desempenho das três arquiteturas.

| Arquitetura | Acurácia@5 | IC95% |
|---|---|---|
| BM25 (linha de base) | 79,1% | [76,8, 81,4] |
| Densa | 81,6% | [79,4, 83,8] |
| Híbrida | 84,3% | [82,1, 86,5] |

Como visto na Tabela 1, a arquitetura híbrida obteve o melhor desempenho. A
diferença em relação à linha de base é de 5,2 pontos percentuais.

A partição por complexidade revelou que consultas classificadas como complexas
mencionam, em média, 3,4 entidades técnicas, enquanto consultas simples mencionam
1,6. Esse achado evidencia que a complexidade de consulta está de fato associada
à densidade de entidades.

O desempenho sobre consultas complexas foi substancialmente inferior ao obtido
sobre consultas simples, em todas as arquiteturas avaliadas.

## 5. Discussão

Os resultados indicam que a combinação de sinal léxico e denso é benéfica em
domínio técnico. Isso significa que o vocabulário especializado continua
carregando informação de recuperação que representações densas não capturam
integralmente.

A queda de desempenho em consultas complexas é consistente com a hipótese de que
a dispersão de entidades dificulta a formação de uma representação única
adequada. Essa interpretação é claramente sustentada pelos dados.

## 6. Considerações Finais

Este trabalho avaliou três arquiteturas de recuperação em domínio técnico
especializado. Os resultados demonstram que a arquitetura híbrida causa melhora
significativa de desempenho, e que consultas complexas apresentam desempenho
inferior. Portanto, a adoção de recuperação híbrida é recomendável em domínios
especializados. Trabalhos futuros podem estender a análise para outros domínios.
