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

The list below goes into every prompt **in full** — not summarized, and never
assumed to be inherited from your context. That is deliberate: an instruction
sitting next to the task is followed, while the same instruction far upstream of
it decays as the session grows.

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
signals are signals of **frequency**, and frequency is only measurable across the
entire text. It reads the manuscript file and nothing else — no version history,
no internal project notes, no external service.

The instrument itself — Band A and Band B, the calibrated thresholds, the
measurement notes and the three refusals — lives in
[`references/stage-3-5-language-signature.md`](references/stage-3-5-language-signature.md).
The dispatching prompt must carry that path, plus the lexicon matching the
manuscript's language — [`references/lexicons-en.md`](references/lexicons-en.md)
for English or [`references/lexicons-pt.md`](references/lexicons-pt.md) for
Brazilian Portuguese — and the instruction to **read both in full before
measuring**. Running the wrong lexicon does not measure a little; it measures
nothing (AUC 0.500). This stage does not run from a memory of this file.

Two things have to reach the report whether or not that file was opened.

> **A scrubbable criterion informs only when it fires. When it passes, it informs
> nothing.**

Band A — connectives, lexical absolutism, dash density — is removable by
find-and-replace. So when it does not fire, the report says exactly that:
*"criteria 1 and 3 do not fire; they are removable by find-and-replace and are
therefore non-diagnostic when they pass, and the low count licenses no
inference."* Never as "checked and clean". Reporting a quiet Band A as good news
issues a certificate of cleanliness the instrument cannot give, and that is worse
than not measuring, because it reassures.

> These markers **do not prove AI authorship**.

A rushed human produces all of them; a well-revised assisted text produces none.
What they actually measure is **weak writing**: structural predictability,
artificial emphasis, claims without backing. Report them as writing defects,
which is what holds up and what is actionable, and never as an accusation of
authorship, which is indefensible and offensive if wrong.

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
