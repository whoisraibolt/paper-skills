---
name: paper-reviewer
description: Deep pre-submission review of a scientific manuscript, modeled on Google's Paper Assistant Tool (PAT). Segments the manuscript, allocates a reasoning budget per segment, dispatches deep reviewers in parallel (each with the full text as context), and consolidates into a single report with severity, quoted evidence, and anti-hallucination checks. Use when asked to review, audit, critique, or validate a paper, thesis, dissertation, chapter, or proposal before submission. Accepts .tex, .md, .pdf, and .docx. Works in English and Brazilian Portuguese.
license: MIT
---

# paper-reviewer — deep pre-submission review

A reimplementation of the **Paper Assistant Tool (PAT)** architecture (Jayaram et
al., Google Research, arXiv:2606.28277) on Claude Code subagents in place of
Gemini Deep Think.

The premise from PAT, which is what makes this skill worth more than "read the
paper and criticize it": a single reading pass spends its reasoning budget
uniformly and shallowly. Segmenting the manuscript, giving each reviewer **the
whole text as context but only one segment to verify**, then consolidating with
deduplication and grounding checks, raises real-error detection substantially. On
the Math/CS subset of the SPOT benchmark, this orchestration took the same model
from 55.2% to 89.7% detection.

It produces no score, no ranking and no accept/reject recommendation. It produces
**objective errors and actionable improvements**.

Writing counterpart: `paper-writer`. Writing and reviewing are separate passes by
design; whoever writes does not approve their own text in the same context.

---

## Stage 0 — Resolve the target

1. If the user named a file, use it. Otherwise look for the most likely
   manuscript in the current directory (a `.tex` with `\documentclass`, or a long
   `.md`) and **confirm with the user before spending agents** if there is more
   than one candidate.
2. **Always prefer source over PDF.** PAT lists PDF parsing failure among its
   three most reported limitations. If a `.tex` or `.md` exists, use it and ignore
   the compiled PDF.
3. Read the **whole** manuscript before segmenting. Without that, the
   segmentation comes out wrong.
4. Locate verification inputs, if they exist:
   - the `.bib` or reference file;
   - data, result tables or experiment outputs in the repository (for example
     `data/outputs/`), which allow checking number by number;
   - previous reviews, audits or referee reports (for example `reviews/`,
     `response_*.md`, `HANDOFF.md`), which serve to **avoid repeating** a point
     already resolved.

---

## Stage 1 — Segmentation

Break the manuscript into **semantic segments**, not into equal-sized chunks. A
segment is a set of sections that share a logical theme and are verified
together. Segments may be **non-contiguous**: if the abstract quotes a number
from Section 7, both belong to the same segment.

Typical segmentation of an empirical paper:

| Segment | Usually gathers |
|---|---|
| Framing | Abstract, Introduction, Conclusion, claimed contributions |
| Related work | State of the art, positioning of the gap |
| Method / architectures | What was built or compared |
| Metric definition | Every metric the authors propose, with its formalization |
| Data | Datasets, provenance, construction, licensing |
| Experimental protocol | What was held fixed, configuration, statistical analysis |
| Results | Tables, figures, numbers in the body text |
| Discussion and limitations | Interpretation, threats to validity, future work |

Adjust to the actual manuscript. A theoretical paper swaps "Results" for
"Proofs"; a bibliometric one swaps "Architectures" for "Search protocol".

---

## Stage 2 — Adaptive budget

Assign each segment an effort tier according to the density of verifiable
claims. This is what PAT calls Light/Medium/High Thinking.

- **HIGH** — wherever an error invalidates the paper. Metric definitions, proofs,
  statistical protocol, results tables, any number appearing in more than one
  place. These segments go to reviewers with `model: opus` and an explicit
  instruction to reason line by line.
- **MEDIUM** — method, data, experimental configuration, discussion.
  `model: opus`, normal verification.
- **LOW** — framing, related work, acknowledgements and declarations.
  `model: sonnet` is enough.

Announce the segmentation and the budget to the user in a short table before
dispatching. It is the last cheap chance to fix the cut.

---

## Stage 3 — Deep review in parallel

Dispatch **one subagent per segment**, all in the same message so they run in
parallel. Use `subagent_type: general-purpose` with the `model` set in Stage 2.

Every reviewer prompt must contain, without exception:

1. **The whole manuscript** (the file path; the agent reads it), with the
   instruction that it is context, not target.
2. **The assigned segment**, by section and line range, as the only verification
   target.
3. **READ ONLY** — Write, Edit and NotebookEdit are forbidden. The reviewer
   reports; it does not fix.
4. The paths to the verification inputs from Stage 0.
5. The finding contract below.

### Finding contract

Every returned finding must have:

- **Severity** — `CRITICAL` (invalidates a conclusion), `HIGH` (requires
  substantive rewriting), `MEDIUM` (weakens the argument or clarity), `LOW`
  (local correction).
- **Location** — file and line.
- **A literal quote** of the problematic passage. Without a quote, the finding
  does not exist.
- **The defect**, in one sentence.
- **Confidence** — `CONFIRMED` (verified against the source, the data or the
  `.bib`) or `PLAUSIBLE` (grounded suspicion, not verified).
- **What would have to be true for this finding to be wrong** — one line. This
  field is what separates useful criticism from noise.

### What to hunt

Generic, in any manuscript:

- **Cross-numeric consistency.** Every number in the abstract, the body, the
  tables and the figures must agree. Where raw data exist in the repository,
  check against them. This is the most common error class and the cheapest to
  detect.
- **Claims beyond the evidence.** A causal claim supported by a correlational
  result; "demonstrates" where "suggests" belongs; generalization beyond the
  tested conditions.
- **Claimed versus delivered contributions.** Does each item in the contribution
  list have a corresponding section that fulfils it?
- **Orphan research questions.** Is each RQ answered explicitly? Does each answer
  point to specific evidence?
- **References.** Every `\cite` has an entry in the `.bib`; every entry is cited;
  the cited work supports what the text says it supports. Flag entries that look
  fabricated (missing DOI, vague authorship, generic title).
- **Arithmetically small and logically fatal errors** — flipped sign, inverted
  inequality, unit error, off-by-one, overloaded notation. PAT reports these as
  the most frequent and most underestimated finding.
- **Missing limitation.** An obvious threat to validity the text does not
  acknowledge.
- **Methodological leakage.** Was the evaluation instrument built using the thing
  it evaluates? Circularity between what is measured and what is used to measure.
- **Provenance and licensing** of data and corpora, when the text describes them.

### Anti-hallucination guards

PAT documents three failure modes of its own. Instruct every reviewer against all
three:

1. **Do not claim something is outdated** — a date, a version, "state of the art"
   — without checking. If it could not be checked, the finding is `PLAUSIBLE` and
   is phrased as a question.
2. **Do not invent a reference, theorem or related work.** If external literature
   is cited, it must be something the reviewer can locate.
3. **Do not declare an argument incorrect for having failed to understand it.**
   Before marking a piece of reasoning `CRITICAL`, the reviewer must reconstruct
   the author's argument in their own words and only then point to where it
   breaks. If the reconstruction does not close, the finding becomes `PLAUSIBLE`
   with the doubt made explicit.

No praise. The report has no strengths section.

---

## Stage 3.5 — Automated language signature

One dedicated reviewer, over the **whole manuscript**. This is not a segment: the
signals below are signals of **frequency**, and frequency is only measurable
across the entire text.

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
[`references/lexicons-en.md`](references/lexicons-en.md) and
[`references/lexicons-pt.md`](references/lexicons-pt.md). Use the one that matches
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

---

## Stage 4 — Global synthesis

Done by you, in the main context, after all reviewers return.

1. **Deduplicate.** The same defect seen from two segments becomes one finding,
   with both locations.
2. **Drop the unfounded.** A finding without a literal quote, or whose quote does
   not match the real text, is discarded, not downgraded. Open the file and
   confirm the `CRITICAL` and `HIGH` findings by sampling.
3. **Verify the grounding.** For findings that depend on an external fact (does a
   reference exist? does a number match the data?), confirm it yourself before
   reporting. Use WebSearch for literature and file reading for data. This is
   PAT's `search grounding`.
4. **Reorder by real severity**, not by segment order.
5. **Separate error from improvement.** Two distinct lists: what is wrong and what
   would be better.

### Output

Write to `reviews/review_<manuscript-name>_<YYYY-MM-DD>.md`, next to the
manuscript, and summarize in chat only the `CRITICAL` and `HIGH` findings.

```markdown
# Pre-submission review — <manuscript>
<date> · <N> segments · <N> reviewers · <N> findings after deduplication

## Verdict
<2-4 sentences: what blocks submission today, if anything does.>

## Errors
### [CRITICAL] <short title>
**Where:** file:line
**Text:** "<literal quote>"
**Defect:** <one sentence>
**Confidence:** CONFIRMED — <how it was verified>
**I would be wrong if:** <one line>
**Suggested fix:** <actionable>

## Improvements
<same structure, without severity>

## Checked and clean
<short list of what was checked and showed no problem: numbers verified against
data, citations matched against the .bib. This tells the user what they do NOT
need to re-check by hand.>
```

---

## Operating notes

- A short manuscript (under ~15 pages) can go with 4 or 5 segments. A thesis or a
  long paper asks for 8 to 10.
- If the user asks for focus (`only the statistics`), reduce the segments to the
  requested scope and say explicitly in the report what was left out.
- If there is a previous audit, the report must say which findings are **new** and
  which **recur**.
- Re-running after fixes is cheap and is the intended use. PAT gave one pass per
  manuscript; this skill has no such limit.
