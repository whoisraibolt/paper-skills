# Léxicos da Faixa A — português

Listas fechadas dos critérios raspáveis do Estágio 3.5. São exatamente as listas
usadas para produzir os limiares calibrados do `SKILL.md`.

**Por que o idioma importa.** Rodar estes critérios com o léxico de outra língua
devolve AUC exatamente 0,500: todo texto pontua zero e todos empatam. O
instrumento não mede pouco, mede nada. Isso foi medido, não suposto.

**Critério de inclusão.** Um termo pertence à Faixa A quando pode ser removido
por substituição de padrão sem alterar o conteúdo proposicional da sentença. É
isso que o torna raspável, e é por isso que contagem baixa não licencia
inferência.

## A1 — Conectores encabeçando frase

Casados apenas na abertura da sentença. Conector no meio da frase é articulação legítima e não é o que o critério mede.
*63 termos.*
```
ademais
adicionalmente
além disso
além do mais
assim sendo
cabe destacar
cabe mencionar
cabe ressaltar
com efeito
complementarmente
consequentemente
contudo
de fato
dessa forma
desse modo
desta forma
deste modo
diante disso
diante do exposto
dito de outro modo
dito isso
em conclusão
em outras palavras
em primeiro lugar
em resumo
em segundo lugar
em suma
em síntese
entretanto
finalmente
importa destacar
isso implica que
isso significa que
isto é
logo
na prática
nesse cenário
nesse contexto
nesse sentido
nesse ínterim
neste contexto
neste sentido
no entanto
não obstante
ou seja
outrossim
paralelamente
por conseguinte
por fim
por outro lado
por um lado
portanto
posto isso
primeiramente
sendo assim
todavia
vale destacar
vale mencionar
vale notar
vale ressaltar
é fundamental destacar
é importante destacar
é importante ressaltar
```

## A2 — Absolutismo lexical

Advérbios e locuções que projetam certeza total ou universalidade sem que o texto ofereça o quantificador correspondente.
*21 termos.*
```
absolutamente
certamente
claramente
completamente
evidentemente
indubitavelmente
inegavelmente
inquestionavelmente
inteiramente
jamais
nunca
obviamente
plenamente
seguramente
sem dúvida
sem sombra de dúvida
sempre
totalmente
é claro que
é evidente que
é óbvio que
```

## A4 — Intensificadores sem lastro

Contados separando os que têm um número por perto (com lastro) dos que só enfatizam. Quem raspa absolutismo raramente raspa estes.
*16 termos.*
```
altamente
amplamente
consideravelmente
consistentemente
drasticamente
expressiva
expressivamente
expressivo
extremamente
notavelmente
profundamente
robustamente
significativamente
sistematicamente
substancial
substancialmente
```

## B6 — Marcadores de posicionamento autoral (não automatizar)

Mantido apenas como referência. O proxy automático construído sobre esta lista concordou com um leitor independente e cego em 49,4%, que é o acaso. Leia os parágrafos.
*25 termos.*
```
a presente pesquisa
adota-se
adotou-se
argumenta-se
argumentamos
assume-se
considera-se
defende-se
defendemos
entende-se
esta dissertação
esta pesquisa
esta tese
este artigo
este estudo
este trabalho
nossa abordagem
nossa proposta
nosso trabalho
o presente trabalho
opta-se
optou-se
propomos
propõe-se
sustenta-se
```

## A3 — Travessão longo

`— –` (U+2014 travessão, U+2013 meio-travessão). O hífen comum (U+002D)
fica de fora: é pontuação legítima de composição e removê-lo quebraria palavra.

A3 é **independente de língua** e não precisa de adaptação.

## Frames (B5)

Frames retóricos são casados por expressão regular, não por lista de palavras,
então ficam no corpo da skill e não aqui.
