# Band A lexicons — English

Closed word lists for the scrubbable criteria of Stage 3.5. These are the exact
lists used to produce the calibrated thresholds in `SKILL.md`.

**Why the language matters.** Running these criteria with the lexicon of another
language returns an AUC of exactly 0.500: every text scores zero and all of them
tie. The instrument does not measure a little, it measures nothing. This was
measured, not assumed.

**Inclusion criterion.** A term belongs to Band A when it can be removed by
pattern substitution without altering the propositional content of the sentence.
That is what makes it scrubbable, and it is why a low count licenses no
inference.

## A1 — Sentence-opening connectives

Matched only at the start of a sentence. A connective mid-sentence is legitimate articulation and is not what the criterion measures.
*52 terms.*
```
accordingly
additionally
as a result
besides
by contrast
consequently
conversely
crucially
finally
first
firstly
furthermore
given this
hence
however
importantly
in addition
in conclusion
in contrast
in fact
in other words
in practice
in summary
in the first place
in this context
in this sense
indeed
it is important to note
it is worth noting
lastly
moreover
nevertheless
nonetheless
notably
of note
on the other hand
overall
put differently
second
secondly
significantly
taken together
that is to say
that said
therefore
third
thirdly
this means that
thus
to conclude
with this in mind
yet
```

## A2 — Lexical absolutism

Adverbs and phrases projecting total certainty or universality without the text offering the corresponding quantifier.
*19 terms.*
```
absolutely
always
certainly
clearly
completely
entirely
evidently
fully
it is clear that
it is obvious that
never
obviously
of course
totally
undeniably
undoubtedly
unquestionably
wholly
without a doubt
```

## A4 — Unsupported intensifiers

Counted separating those with a number nearby (grounded) from those that merely emphasize. Whoever scrubs absolutism rarely scrubs these.
*16 terms.*
```
considerably
consistently
dramatically
extensively
extremely
greatly
highly
markedly
notably
profoundly
remarkably
robustly
significantly
substantially
systematically
vastly
```

## B6 — Authorial positioning markers (do not automate)

Kept for reference only. The automated proxy built on this list agreed with an independent blind reader at 49.4%, which is chance. Read the paragraphs instead.
*21 terms.*
```
in our view
it is argued
it is proposed
our approach
our proposal
the present study
the present work
this article
this paper
this research
this study
this work
we adopt
we argue
we assume
we claim
we consider
we contend
we propose
we show
we suggest
```

## A3 — Long dashes

`— –` (U+2014 em dash, U+2013 en dash). The plain hyphen (U+002D) is
excluded: it is legitimate compounding punctuation and removing it would break
words.

A3 is **language-independent** and needs no adaptation.

## Frames (B5)

Rhetorical frames are matched by regular expression rather than by word list, so
they live in the skill body rather than here.
