# Exemplo preenchido — tese em PT-BR, convenções ABNT

Este é um exemplo **fictício mas realista**, para mostrar o nível de
especificidade que a skill espera. Não copie os caminhos; copie o grau de
detalhe.

Cenário: tese de doutorado em Ciência da Computação, avaliação empírica
comparando arquiteturas de recuperação, com uma segunda rodada de experimentos
que substituiu a primeira.

---

## 1. Manuscrito

- **Arquivo principal:** `tese/tese.tex`
- **Idioma:** pt-BR
- **Bibliografia:** `tese/referencias.bib`
- **Diretório de rascunhos:** `tese/rascunhos/`

---

## 2. Artefatos canônicos

| Caminho | Contém | Alimenta qual segmento |
|---|---|---|
| `data/outputs/analysis/metricas_r2.json` | acurácia, F1 e IC95% por arquitetura, rodada 2 | Resultados |
| `data/outputs/analysis/testes_r2.json` | McNemar, p-valores, correção de Bonferroni | Resultados, Protocolo experimental |
| `data/outputs/corpus/manifesto_r2.json` | nº de itens, distribuição por categoria, licença de cada fonte | Dados |
| `configs/experimento_r2.yaml` | hiperparâmetros, seeds, versões de modelo fixadas | Protocolo experimental |
| `figuras/gerar_*.py` | scripts que produzem cada figura (a figura é derivada, o script é a fonte) | Resultados |

---

## 3. Fontes supersedidas — proibidas

| Caminho / padrão | Por que está proibido |
|---|---|
| `data/outputs/**/*_r1/**` | rodada 1, invalidada por um erro de pré-processamento corrigido na rodada 2; os números **mudaram** e continuam parecendo plausíveis |
| `data/outputs/analysis/metricas.json` | sem sufixo de rodada — ambíguo, provavelmente r1. Se um valor só existe aqui, é `[VERIFICAR]` |
| `tese/tese_2025.tex` | versão anterior da tese; nenhum número dela foi reverificado contra a r2 |
| `notas/resultados_preliminares.md` | anotações de bancada, nunca conferidas |

> Nota de método: o critério aqui não é "está velho", é **"os valores mudaram e
> a diferença não é visível a olho"**. É exatamente isso que faz um número
> supersedido atravessar a revisão.

---

## 4. Narrativa de processo a excluir

| Não escrever | Se precisar aparecer, aparece como |
|---|---|
| a descoberta do bug de pré-processamento e o rerun da rodada 1 para a 2 | não aparece. O manuscrito descreve o pipeline corrigido, no presente |
| tabela item-a-item de quais questões foram revisadas manualmente | parágrafo agregado: "1.240 itens passaram por revisão manual; 87 foram corrigidos e 12 descartados" |
| histórico de quais arquiteturas entraram e saíram da comparação | a seção de método descreve as arquiteturas que **estão** na comparação final |

---

## 5. Guia de voz

- **Registro:** português acadêmico formal, terceira pessoa, sem coloquialismo.
- **Proibições de pontuação/estilo:** proibido travessão longo (—). Use vírgula,
  parêntese ou ponto.
- **Siglas:** definidas no formato "em inglês, English Name, ACRONYM" na primeira
  ocorrência. Ex.: "geração aumentada por recuperação (em inglês,
  *Retrieval-Augmented Generation*, RAG)".
- **Seções obrigatórias:** "Considerações Finais" ao fechar o manuscrito.
- **Fluxo de figuras e tabelas, três passos, nesta ordem:**
  1. referenciar antes de inserir ("A Figura 3 apresenta...");
  2. inserir com "Fonte: Elaborado pela autora." na legenda;
  3. descrever depois ("Como visto na Figura 3, ...").
- **Figuras com texto embutido:** gerar sempre as duas versões, PT-BR e EN, mesmo
  que a tradução do artigo ainda não tenha começado.
- **Formato-fonte de figura:** o script Python/matplotlib que gera a figura é a
  fonte editável. Não manter `.drawio` em paralelo.
- **Terminologia fixa:** "arquitetura" (nunca "abordagem" ou "modelo" para o
  mesmo referente); "item" para a unidade do corpus (nunca "questão" ou
  "exemplo").
- **Vetado:** linguagem promocional sem alegação verificável por trás
  ("resultados notáveis", "abordagem inovadora", "avanço significativo" sem
  p-valor); elogio ao próprio texto; intensificador sem número atrás
  ("substancialmente melhor" sem a diferença).

---

## 6. Seções que ainda serão reescritas

- Trabalhos relacionados (aguardando decisão de escopo)
