# Exemplo do `paper-writer` — projeto sintético

> **TUDO AQUI É SINTÉTICO.** O projeto, o manuscrito e os dados foram criados
> para demonstrar o `paper-writer`. Nenhum número descreve um experimento real.

Esta pasta é um projeto de manuscrito fictício, do jeito que a skill o
encontraria, mais o que ela produziu ao receber o pedido:

> Escreva só a seção 3 (Resultados) de artigo.md.

## O que há na pasta

| Arquivo | Papel |
|---|---|
| [`paper-writer.config.md`](paper-writer.config.md) | o config do projeto: artefatos canônicos, fontes proibidas, guia de voz |
| [`artigo.md`](artigo.md) | o manuscrito, com a seção 3 ainda por escrever |
| [`dados/r2/`](dados/r2/) | os dois artefatos canônicos, únicas fontes permitidas de número |
| [`dados/r1/metricas.json`](dados/r1/metricas.json) | uma rodada supersedida, declarada como **proibida** no config |
| [`rascunhos/rascunho_resultados_2026-10-13.md`](rascunhos/rascunho_resultados_2026-10-13.md) | **a saída**: o rascunho consolidado, com a checagem do Estágio 4 |
| [`rascunhos/resultados_2026-10-13.md`](rascunhos/resultados_2026-10-13.md) | o rascunho do redator do segmento, com o mapa de fonte valor a valor |

Os dois arquivos de `rascunhos/` estão como a skill os gravou, sem edição
posterior.

## O que observar

**A rodada proibida não entrou.** `dados/r1/metricas.json` diz que a arquitetura
híbrida atinge 87,3%. A rodada 2 diz 84,3%. O rascunho usa 84,3% e a rodada 1
não foi aberta. É o mesmo par de números que o
[exemplo do `paper-reviewer`](../revisao-exemplo.md) flagra divergindo entre
resumo e tabela: lá o erro é encontrado depois de escrito, aqui ele não chega a
ser escrito.

**O número que falta virou marcador, não estimativa.** O roteiro da seção pede a
latência por consulta. Esse valor só existe na rodada proibida, então a
subseção 3.4 sai com quatro `[VERIFICAR: ...]`, cada um dizendo o que falta e
onde provavelmente está.

**Marcador pendente bloqueia a mesclagem.** Por causa deles, `artigo.md` não foi
alterado. O rascunho lista o que a autora precisa resolver antes.

**"Significativo" vem com p-valor e limiar.** A comparação entre a arquitetura
densa e a linha de base tem p = 0,041, abaixo de 0,05 e acima do limiar
corrigido de 0,0167. O rascunho diz que ela não atinge o limiar, em vez de
chamá-la de significativa.

**A consolidação cortou uma frase sem fonte.** O redator afirmou algo sobre o
escopo dos testes que nenhum artefato declara. O rascunho consolidado registra o
corte e o motivo.

## Limites deste exemplo

É um pedido de uma seção só, então houve um único segmento e um único redator; o
paralelismo entre segmentos não aparece aqui. O projeto foi montado para que a
latência faltasse de propósito.
