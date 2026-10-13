# Agensi listings — drafts

Draft copy for the two Agensi listing pages. Every figure below comes from
`README.md` or from the example in `examples/`; nothing here is a new claim.

---

## paper-reviewer

**Title:** Paper Reviewer — deep pre-submission review

**One-line description:** Finds the errors a referee would find in your
manuscript before you submit, each one quoted, checked and open to challenge.

**Long description:**

The errors that sink a paper are the ones a single read-through misses: a
number in the abstract that disagrees with the table, or a result the paper's
own definition guarantees. Paper Reviewer splits your manuscript into thematic
segments and gives each one a dedicated reviewer that still sees the whole text,
then merges everything into a single report. Each finding quotes the passage,
says how it was checked, and states what would have to be true for it to be
wrong. It also scans the writing for the patterns that make text read as
machine-made, and reports them as writing problems you can fix, never as an
accusation of authorship. It never edits your manuscript. You get errors and
improvements, not a score or an accept/reject verdict. Works on .tex, .md, .pdf
and .docx, in English and Brazilian Portuguese. Requires an agent that supports
subagents, such as Claude Code.

**Proof of result:** the repository includes a
[full report](../examples/revisao-exemplo.md) produced by the skill on a
[synthetic manuscript](../examples/manuscrito-exemplo.md) with deliberately
planted defects. Five segment reviewers plus the language reviewer returned nine
findings after deduplication. Two block submission: the abstract reports 87.3%
accuracy where Table 1 reports 84.3% for the same condition, and a "finding"
that complex queries mention more entities turns out to be guaranteed by how the
paper defines a complex query. The report also flags a declared research
question that is never answered and a declared contribution that is never
delivered. The example is synthetic so that no real author is exposed to a
review they did not ask for.

**Suggested category:** Research & Analysis

**Suggested tags:** peer review, academic writing, manuscript, pre-submission,
thesis, dissertation, research paper, LaTeX, proofreading, Portuguese

---

## paper-writer

**Title:** Paper Writer — grounded manuscript drafting

**One-line description:** Drafts sections of your paper or thesis in your own
voice, with every number traced to a file you declared and nothing invented.

**Long description:**

Paper Writer drafts sections of your paper, thesis or proposal without
inventing anything. Before it writes a sentence, you declare which files your
numbers may come from and which old drafts and data rounds are off limits. Every
number in the draft then cites the file it came from. A value it cannot find
becomes a visible [VERIFICAR] marker instead of a plausible guess, and a
reference that is not in your .bib becomes [CITAÇÃO NECESSÁRIA]. Drafts follow
the voice guide you set, so new text matches what you already wrote, and they
are saved to a separate file: nothing reaches your manuscript until the markers
are resolved. The result is a grounded draft for you to approve sentence by
sentence, not finished text. Written in Brazilian Portuguese, for
Portuguese-language academic writing, with an ABNT-oriented example. Requires an
agent that supports subagents, such as Claude Code.

**Proof of result:** the repository includes a
[synthetic project](../examples/escrita-exemplo/) and the Results draft the
skill produced from it. The project declares two data files as the only
legitimate sources and marks an older data round as forbidden. The older round
says the best architecture reaches 87.3%; the current one says 84.3%. The draft
uses 84.3% and never opens the forbidden file. The section outline also asks for
latency, which no declared file contains, so the draft carries four
[VERIFICAR] markers there instead of numbers, and for that reason it was not
merged into the manuscript. One comparison with p = 0.041 is reported as not
reaching the corrected threshold of 0.0167 rather than as significant. All data
in the example are synthetic.

**Suggested category:** Writing & Content

**Suggested tags:** academic writing, manuscript, thesis, dissertation, research
paper, drafting, citations, ABNT, Portuguese, LaTeX

---

## Closing paragraph (both listings)

Paper Reviewer and Paper Writer are open source under the MIT license. The
source, the full example report and the calibration notes behind the language
scan are on GitHub: <https://github.com/whoisraibolt/paper-skills>. Issues and
suggestions are welcome there.

---

## Notes for whoever publishes these

- **Paper Writer is in Portuguese.** Only its frontmatter description is in
  English. The long description says so; a buyer who does not read Portuguese
  should know before installing.
- **Figures deliberately left out.** The README quotes 55.2% to 89.7% error
  detection. That is Google's result for the Paper Assistant Tool on the SPOT
  benchmark, not a measurement of this skill, so it is not used as a selling
  point here. The 76-article calibration and the 49.4% agreement figure are
  about the language scan's thresholds, which is architecture rather than
  benefit; they stay in the README.
