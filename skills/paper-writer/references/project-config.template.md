# paper-writer — configuração do projeto

Copie este arquivo para `.claude/paper-writer.md` na raiz do repositório do seu
manuscrito e preencha. A skill não escreve nada até encontrá-lo.

Ele é versionado junto com o manuscrito e evolui com ele. A skill permanece
genérica; tudo que é específico do seu trabalho mora aqui.

Há um exemplo completo e preenchido em `example-config-ptbr-abnt.md`.

---

## 1. Manuscrito

- **Arquivo principal:** `<caminho/para/artigo.tex ou .md>`
- **Idioma:** `<pt-BR | en | ...>`
- **Bibliografia:** `<caminho/para/referencias.bib>`
- **Diretório de rascunhos:** `<caminho/para/rascunhos/>`

---

## 2. Artefatos canônicos

> A **única** origem legítima de número, tabela ou p-valor. Um redator que não
> encontra o valor aqui escreve `[VERIFICAR: ...]` — nunca estima.

Liste caminho e conteúdo. Seja específico: `data/outputs/` não é um artefato, é
uma pasta.

| Caminho | Contém | Alimenta qual segmento |
|---|---|---|
| `<caminho>` | `<que números/tabelas moram aqui>` | `<Resultados, Dados, ...>` |
| | | |

---

## 3. Fontes supersedidas — proibidas

> O vetor de erro mais comum. Rascunho antigo e rodada de dados velha continuam
> existindo no repositório, continuam parecendo corretos, e um número deles passa
> despercebido porque "é quase igual".

Liste tudo que existe no repositório e **não** pode ser fonte, com o motivo.

| Caminho / padrão | Por que está proibido |
|---|---|
| `<ex.: data/outputs/**/*_v1/**>` | `<superseded pela rodada v2; valores diferentes>` |
| `<ex.: artigo_antigo.tex>` | `<versão anterior; números não reverificados>` |
| | |

---

## 4. Narrativa de processo a excluir

> Regra dura 2: o manuscrito descreve o artefato **como ele está hoje**, não a
> jornada de descobrir e consertar um problema.

O que aconteceu no projeto mas **não** entra no texto, e como aparece se
precisar aparecer:

| Não escrever | Se precisar aparecer, aparece como |
|---|---|
| `<ex.: log item-a-item da revisão manual>` | `<parágrafo agregado: "N itens revisados, M corrigidos">` |
| | |

---

## 5. Guia de voz

> Colado literalmente no prompt de cada redator. Quanto mais concreto, menos o
> rascunho destoa do que você já escreveu.

Preencha o que se aplica ao seu projeto; apague o resto.

- **Registro:** `<ex.: português acadêmico formal, terceira pessoa>`
- **Proibições de pontuação/estilo:** `<ex.: proibido travessão longo (—)>`
- **Siglas:** `<ex.: "em inglês, English Name, ACRONYM" na primeira ocorrência>`
- **Seções obrigatórias:** `<ex.: "Considerações Finais" ao fechar o manuscrito>`
- **Fluxo de figuras e tabelas:** `<ex.: referenciar antes → inserir com fonte →
  descrever depois>`
- **Legenda/fonte de figura:** `<ex.: "Fonte: Elaborado pela autora.">`
- **Figuras com texto embutido:** `<ex.: gerar sempre PT-BR e EN>`
- **Formato-fonte de figura:** `<ex.: script Python/matplotlib editável, não .drawio>`
- **Terminologia fixa:** `<termos que têm um nome só e não podem variar>`
- **Vetado:** `<ex.: linguagem promocional ("resultados notáveis", "abordagem
  inovadora") sem alegação verificável por trás; elogio ao próprio texto>`

---

## 6. Opcional — seções que ainda serão reescritas

Se você já sabe que certas seções vão ser refeitas, liste aqui. O
`paper-reviewer` usa essa lista para separar "corrigir agora" de "só não repetir
no texto novo", e o `paper-writer` evita gastar redator em texto condenado.

- `<seção>`
