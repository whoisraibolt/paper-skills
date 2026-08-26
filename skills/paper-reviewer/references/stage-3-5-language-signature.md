# Stage 3.5 — automated language signature (the full instrument)

Loaded on demand by the Stage 3.5 reviewer. `SKILL.md` carries the dispatch rule
and the two sentences that have to survive into the report even if this file is
never opened; everything needed in order to actually **measure** is here.

Read this file in full before measuring anything, and pair it with the lexicon
that matches the manuscript's language: [`lexicons-en.md`](lexicons-en.md) or
[`lexicons-pt.md`](lexicons-pt.md).

This stage is not from the PAT paper. It is original to this repository.

---

### Scope: the manuscript and nothing else

This stage reads **the manuscript file and nothing else**. It does not open
version history, briefings, writing plans or internal project notes, and it does
not send the text to an external service.

Three reasons, all of them design rather than convenience:

1. **The referee sees only the manuscript.** If this skill exists to anticipate
   the referee, it has to work with what the referee sees. A finding that depends
   on an internal artifact does not survive submission.
2. **Internal evidence is ambiguous in origin.** A briefing that catalogued the
   author's own tics makes "the text matches the briefing" stop distinguishing a
   personal habit from an imported pattern. The evidence looks strong and is not.
3. **It does not generalize.** A stage that only works where a repository and a
   briefing exist is not a stage; it is an accident of that project.

There is a consequence, and it is the next point.

### The diagnostic asymmetry — the rule that governs this stage

The criteria in this section **are not worth the same**, and the difference is
not one of importance: it is one of **cost of evasion**.

Counting connectives and absolutist adverbs is cheap to zero out. A ten-minute
find-and-replace clears both without touching a line of reasoning. Therefore:

> **A scrubbable criterion informs only when it fires. When it passes, it informs
> nothing.**

This is mandatory in the report. A manuscript with 0.3 connectives per paragraph
may be a well-written text or a text scrubbed the night before, and the count
does not separate the two. Reporting "four of six criteria did not fire" as good
news issues a **certificate of cleanliness the instrument cannot give**, and that
is worse than not measuring, because it reassures.

Always phrase it like this: *"Criteria 1 and 3 do not fire. They are removable by
find-and-replace and are therefore **non-diagnostic when they pass**: the low
count licenses no inference."*

### Band A — scrubbable (count only when they fire)

| # | Criterion | Alert |
|---|---|---|
| A1 | Sentence-opening connectives (*moreover, however, therefore, furthermore, it is worth noting, in other words, this means that, in conclusion*) | above **0.48 per paragraph** |
| A2 | Lexical absolutism (*always, never, clearly, obviously, undoubtedly, evidently*) | above **2.3 per 1,000 words** |
| A3 | Long dashes in excess | any density above the human baseline |

> **Where these thresholds come from.** They were calibrated against 76 full-text
> Brazilian Portuguese articles from SciELO published up to 2019, at the 95th
> percentile of human writing. Earlier versions were asserted from practice and
> were wrong by up to a factor of eight: A1 alerted above 4 per paragraph when
> real academic text, human and machine alike, runs at 0.2 to 0.4. That threshold
> never fired.
>
> The calibration is specific to that corpus. Applying it to another language,
> genre or field is unmeasured extrapolation, and recalibrating first is worth
> the effort.

If they fire, they are ordinary findings, with a count and a quoted passage. If
they do not fire, **one line saying they are non-diagnostic, and nothing else**.
Do not list them as "checked and clean".

A sub-finding Band A misses, and which usually survives scrubbing: **unsupported
intensifiers** (*significantly, substantially, consistently, systematically,
highly*). Whoever scrubs absolutism rarely scrubs these. Count them and separate
the ones with a number behind them from the ones that merely emphasize.

### Language dependence, measured

**Band A criteria are language-specific, and running them on the wrong language
measures nothing at all.** Running Portuguese lexicons over an English corpus
returned an AUC of exactly 0.500 on five criteria: every text scored zero and all
of them tied.

This holds for any detector resting on a word list, and it is rarely declared.
Lexicons for both languages ship with this skill; see
[`lexicons-en.md`](lexicons-en.md) and
[`lexicons-pt.md`](lexicons-pt.md). Use the one that matches
the manuscript.

A3 (long dashes) and the length-derived and n-gram criteria are
language-independent and transfer without adaptation.

### Band B — resistant (the weight of this stage)

None of these can be removed by find-and-replace. All require rewriting. They
are, for that reason, the only ones carrying real information.

| # | Criterion | How to measure | Alert |
|---|---|---|---|
| B1 | **Template symmetry** | coefficient of variation of paragraph length, global **and per section block** | CV below 34% |
| B2 | **Semantic redundancy** | repeated n-grams of 8+ words; the same proposition at distant points | any chain |
| B3 | **Definitional tautology** | a finding the classification rule **guarantees by construction** | any occurrence |
| B4 | **Inflated hypotaxis** | distribution of sentence length, watching the tail | sentences above ~60 words |
| B5 | **Single rhetorical frame** | count of the *default* mode of asserting (*X, and not Y*; *not only… but also*; *whereas*) | dominant frame in **>7.0%** of paragraphs |
| B6 | **Absent authorial voice** | **human reading; do not automate** | no threshold — see below |
| B7 | **Tautological conclusion** | overlap of the conclusion with the body, plus direct reading | any occurrence |
| B8 | **Robotic rhythm** | same measurement as B4, other tail: subject + verb + complement in a chain | CV of sentence length below 43% |
| B9 | **Illusion of depth** | restatement to gain volume; a generic metaphor in place of analysis; a self-evident claim sold as an implication | any occurrence |

**B4 and B8 are the same measurement read from both ends.** Compute the
distribution of sentence length once: a low CV accuses B8, a long tail accuses
B4. A manuscript rarely has both.

Four measurement notes, learned in use:

- **B1 measures per block, not only globally.** A healthy global CV hides a
  four-paragraph section with a CV of 4%, which is exactly where the reader
  learns the formula and stops reading. Report the worst block, not the average.
- **B3 is the most serious finding this stage produces, and it is not a style
  defect.** When a text defines a category and then presents as a discovery a
  pattern the definition guarantees, that is a **validity problem**. An attentive
  referee will catch it. Mark it `CRITICAL` and send it to Stage 4 for
  verification.
- **B6 must not be automated. This was measured, not estimated.** An earlier
  version of this skill said the regular-expression proxy over-marked by 15 to 25
  percentage points and recommended using it to *locate* paragraphs. We measured
  it: against an independent blind reader, on a stratified sample of 154
  paragraphs from human articles, agreement was **49.4%**. For a binary judgement
  that is chance, and the disagreement is bidirectional (60.0% in one direction,
  40.5% in the other), which is the signature of two unrelated measures.

  Locating at chance is drawing lots, so not even the weakened recommendation
  holds. **B6 remains a criterion; what is withdrawn is its automation.** Read the
  paragraphs and judge whether the author takes a position or merely reports.

  A caveat on the validation itself: the independent reader is a model, not a
  person. That supports the claim that the two measures disagree, not which of
  them is right.

### The honest framing, which goes in the report

These markers **do not prove AI authorship**. A rushed human produces all of
them; a well-revised assisted text produces none. What they actually measure is
**weak writing**: structural predictability, artificial emphasis and claims
without backing. Report them as writing defects, which is what holds up, and not
as an accusation of authorship, which does not.

That is what makes the finding actionable: "five connectives in this paragraph"
is fixable and indisputable; "probably written by AI" is indefensible and
offensive if wrong.

### Priority: what will be rewritten anyway

If the user already knows certain sections will be rewritten, ask for the list
before dispatching and **split the findings into two groups**:

- **Fix** — what sits in a section that survives. Requires action.
- **Avoid in the new writing** — what sits in a section already condemned. Not
  worth fixing; worth keeping as a pattern not to repeat in the text to come.

Without that split, the report tells the user to rewrite what was going to be
rewritten anyway, and they spend attention for nothing.

### Three things this skill deliberately does not do

**It does not emit a single probability percentage.** Summing criterion scores
and multiplying by a constant produces a scientific-looking number with no
validation behind it: there is no calibration against a labelled corpus, the
criteria are not independent, and the result varies with the reviewer. Report the
counts against the thresholds and let the reader conclude. If the user explicitly
asks for the composite number, deliver it, and record in the report that it is
not a calibrated probability.

**It does not paste the manuscript into a third-party service.** Sending
unpublished work to an external API exposes it: it may be retained, cached or
indexed, and under blind review that is a real problem. The scan runs locally,
over the file. If the user wants to use an external detector, that is their
decision, and it is worth warning them before the decision is made.

**It does not audit conduct.** This stage diagnoses **the text**. It does not
infer who wrote it, does not evaluate whether the manuscript's AI-use declaration
is sufficient, and does not cross the text with project history to raise that
question. It is a real question and it belongs to the author, but it is of a
different nature: it moves from "the writing has these defects" to "the declared
conduct has this gap", which the user did not ask for. If the user wants that
analysis, it is requested explicitly and runs separately.
