# paper-writer — configuração do projeto

Config do exemplo sintético. Projeto fictício: nenhum dado aqui é real.

---

## 1. Manuscrito

- **Arquivo principal:** `artigo.md`
- **Idioma:** pt-BR
- **Bibliografia:** `referencias.bib`
- **Diretório de rascunhos:** `rascunhos/`

---

## 2. Artefatos canônicos

| Caminho | Contém | Alimenta qual segmento |
|---|---|---|
| `dados/r2/metricas.json` | acertos, acurácia no topo-5 e IC95% por arquitetura, geral e por complexidade, rodada 2 | Resultados |
| `dados/r2/testes.json` | McNemar par a par, p-valores, correção de Bonferroni, rodada 2 | Resultados, Protocolo experimental |

---

## 3. Fontes supersedidas — proibidas

| Caminho / padrão | Por que está proibido |
|---|---|
| `dados/r1/**` | rodada 1, invalidada por um erro de pré-processamento corrigido na rodada 2; os valores **mudaram** e continuam parecendo plausíveis |

---

## 4. Narrativa de processo a excluir

| Não escrever | Se precisar aparecer, aparece como |
|---|---|
| a existência da rodada 1 e o motivo de ela ter sido refeita | não aparece. O manuscrito descreve a rodada 2, no presente |

---

## 5. Guia de voz

- **Registro:** português acadêmico formal, terceira pessoa, sem coloquialismo.
- **Proibições de pontuação/estilo:** proibido travessão longo (—). Use vírgula,
  parêntese ou ponto.
- **Siglas:** definidas no formato "em inglês, English Name, ACRONYM" na primeira
  ocorrência.
- **Fluxo de figuras e tabelas, três passos, nesta ordem:**
  1. referenciar antes de inserir ("A Tabela 1 apresenta...");
  2. inserir com "Fonte: Elaborado pela autora." abaixo;
  3. descrever depois ("Como visto na Tabela 1, ...").
- **Terminologia fixa:** "arquitetura" (nunca "abordagem" ou "modelo" para o
  mesmo referente); "item" para a unidade do conjunto (nunca "exemplo");
  "linha de base" para o BM25.
- **Vetado:** linguagem promocional sem alegação verificável por trás; verbo
  causal ("causa", "leva a") para resultado comparativo; intensificador sem
  número atrás ("substancialmente melhor" sem a diferença); "significativo" sem
  o p-valor e o limiar corrigido.
