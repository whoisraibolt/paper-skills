# paper-skills

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21982661-1682D4)](https://doi.org/10.5281/zenodo.21982661)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Two Claude Code skills for scientific manuscripts: a deep pre-submission
**reviewer** and a grounded **writer**. Both use the same architecture —
segment the manuscript, give every agent the *whole* text as context but only
*one* segment as its target, run them in parallel, then consolidate.

`paper-reviewer` is written in English and ships lexicons for **English and
Brazilian Portuguese**. `paper-writer` is written in Brazilian Portuguese and
ships an ABNT-oriented voice example, because its value is the Portuguese-language
academic context.

**Stage 3.5 thresholds are empirically calibrated**, not asserted: against 76
full-text human articles published before 2020. The previous asserted values were
wrong by up to a factor of eight, and one criterion had its automation withdrawn
after failing validation. See [Measured, not asserted](#measured-not-asserted).

## Getting it

### Try one without installing

```bash
npx -y skills use whoisraibolt/paper-skills --skill paper-reviewer --agent claude-code
```

Resolves the skill into a temporary directory, hands it to the agent for that
session, and leaves nothing behind — nothing written to `.claude/`, nothing
occupying your system prompt afterwards. Drop `--agent claude-code` to print the
generated prompt to stdout and pipe it wherever you like.

This is the honest default for a reviewer. You know when you are reviewing a
manuscript, so there is nothing to gain from a skill that fires unasked, and an
installed skill's description is paid on every message of every session, whether
or not you are anywhere near a paper.

### Install, if you reach for it often

```bash
npx -y skills add whoisraibolt/paper-skills --skill paper-reviewer --agent claude-code
npx -y skills add whoisraibolt/paper-skills --skill paper-writer   --agent claude-code
```

Installs into `.claude/skills/` of the current project. Add `--global` to install
for all projects.

### By reference, with no installer at all

The repository is a plain skill tree, so an agent that resolves paths can read
either skill straight from GitHub with no package step:

```
@skills:gh:whoisraibolt/paper-skills/skills/paper-reviewer
@skills:gh:whoisraibolt/paper-skills/skills          # both, as a two-line menu
```

That syntax is the `@skills` protocol (Yin et al., 2026, arXiv:2608.12610), a
proposal rather than an adopted standard — Claude Code does not implement it
natively today. It is documented here because it costs this repository nothing:
the tree already answers those paths, and `git clone` plus a file read works with
or without any protocol at all.

---

## What it produces

**→ [See a full review report](examples/revisao-exemplo.md)** — produced by
`paper-reviewer` on [this synthetic manuscript](examples/manuscrito-exemplo.md)
with deliberately planted defects.

A sample of what it catches:

> ### [CRÍTICO] Achado garantido por construção apresentado como descoberta empírica
>
> **Onde:** `manuscrito-exemplo.md:96`, definição em `:76`
> **Texto:** "consultas classificadas como complexas mencionam, em média, 3,4
> entidades técnicas, enquanto consultas simples mencionam 1,6."
> **Defeito:** A Seção 3.3 define complexa como "mais de duas entidades técnicas
> distintas". Que o grupo "mais de duas" tenha média superior ao grupo "até duas"
> é consequência aritmética da definição, não resultado.
> **Confiança:** CONFIRMADO — verificado contra a definição no próprio manuscrito.
> **Eu estaria errado se:** a densidade de entidades tivesse sido medida por um
> instrumento independente da regra de partição.

Every finding carries a literal quote, a confidence level, and **what would have
to be true for the finding to be wrong**. Findings without a quote are discarded
at consolidation, not downgraded.

The report also includes the Stage 3.5 language-signature scan, with the honest
framing the design requires:

> **A1, A2 and A3 do not fire. They are removable by find-and-replace and are
> therefore non-diagnostic when they pass: the low count licenses no inference.**

The example is synthetic on purpose. Publishing a critique of a real paper in a
tool's README would expose named authors to a review they never asked for.

---

## Why segmentation

A single reading pass spends its reasoning budget uniformly and shallowly. It
finds the obvious problems and misses the ones that only surface when you hold a
definition in one hand and a results table in the other.

Splitting the manuscript into semantic segments, giving each reviewer the full
text as context but a single segment to verify, and then deduplicating and
grounding the findings, raises real-error detection substantially. This is the
architecture of Google Research's **Paper Assistant Tool** (PAT); on the Math/CS
subset of the SPOT benchmark it took the same model from 55.2% to 89.7%
detection.

These skills reimplement that architecture on Claude Code subagents.

---

## `paper-reviewer`

Read-only. Never edits the manuscript. Produces objective errors and actionable
improvements — no score, no ranking, no accept/reject recommendation.

- **Segments semantically, not by length.** Segments can be non-contiguous: if
  the abstract quotes a number from Section 7, both belong to the same segment.
- **Adaptive budget.** Metric definitions, proofs, statistics and results tables
  get the expensive model and line-by-line instructions; framing and related work
  do not.
- **Every finding must quote the text.** No literal quote, no finding — it gets
  discarded at consolidation, not downgraded.
- **Every finding states what would have to be true for it to be wrong.** This
  one field is what separates useful criticism from noise.
- **Anti-hallucination guards** against the three failure modes PAT documents:
  claiming something is outdated without checking, inventing references, and
  declaring an argument wrong after failing to understand it.

### Stage 3.5 — automated language signature

This part is **not** from the PAT paper. It scans the whole manuscript for the
markers commonly used to flag AI-generated text, and it splits them by **cost of
evasion**:

- **Band A — scrubbable.** Sentence-opening connectives, lexical absolutism,
  em-dash density. A ten-minute find-and-replace zeroes all of them without
  touching a line of reasoning.
- **Band B — resistant.** Template symmetry, semantic redundancy, definitional
  tautology, inflated hypotaxis, single rhetorical frame, absent authorial voice,
  robotic rhythm. None of these come out without rewriting.

Which yields the rule the stage is built around:

> **A scrubbable criterion only informs you when it fires. When it passes, it
> tells you nothing.**

So the report is required to say so out loud. Reporting "four of six criteria
came back clean" issues a certificate the instrument cannot give — worse than not
measuring, because it reassures.

Three things this stage deliberately refuses to do: emit a single probability
percentage (there is no calibration behind it), paste the manuscript into a
third-party service (unpublished work under blind review), or audit conduct (it
diagnoses the text, not the author).

And the honest framing, which goes in every report: these markers **do not prove
AI authorship**. A rushed human produces all of them; a well-revised assisted
text produces none. What they actually measure is weak writing, meaning
structural predictability, artificial emphasis, and claims without backing. That
is what holds up, and it is also what is actionable.

The instrument itself — both bands, the calibrated thresholds, the measurement
notes and the three refusals — is in
[`references/stage-3-5-language-signature.md`](skills/paper-reviewer/references/stage-3-5-language-signature.md),
loaded by the Stage 3.5 reviewer at dispatch rather than carried in `SKILL.md`.

### Measured, not asserted

Most skills of this kind ship thresholds someone picked by intuition. These were
measured against a corpus of 76 full-text human academic articles published
before 2020, at the 95th percentile of human writing. Three things came out of
it, and all three are in the skill:

**The asserted thresholds were wrong by up to a factor of eight.** A1 alerted
above 4 connectives per paragraph when real academic text, human and machine
alike, runs at 0.2 to 0.4. That threshold never fired. It is now 0.48.

**One criterion had its automation withdrawn.** B6 (absent authorial voice) was
operationalized as a regular-expression proxy. Against an independent blind reader
on a stratified sample of 154 paragraphs, agreement was **49.4%**, which for a
binary judgement is chance. The criterion remains valid for human reading; the
automation is gone.

**The lexical criteria are language-specific, and the failure is silent.** Running
Portuguese lexicons over an English corpus returns an AUC of exactly 0.500: every
text scores zero and all of them tie. The instrument does not measure a little,
it measures nothing. This holds for any detector resting on a word list, and it is
rarely declared. Both lexicons ship with the skill:
[English](skills/paper-reviewer/references/lexicons-en.md) and
[Portuguese](skills/paper-reviewer/references/lexicons-pt.md).

The calibration is specific to that corpus (Brazilian Portuguese, pre-2020,
across the fields the collection returned). Applying it to another language,
genre or field is unmeasured extrapolation, and recalibrating first is worth the
effort.

---

## `paper-writer`

Mirrors the reviewer, on the writing side. **It does not produce publishable
text** — it produces a grounded draft, every numeric claim traceable to a
declared artifact, for a human to approve sentence by sentence.

Because this one writes, its grounding discipline is stricter, not looser: here a
hallucination becomes a false statement *inside* the paper.

Four hard rules, pasted verbatim into every writer subagent:

1. **Only canonical artifacts are sources.** Nothing from a previous draft or a
   superseded data round, ever, without explicit re-verification.
2. **The process narrative does not go in the manuscript.** The text describes the
   artifact *as it stands today*, not the journey of finding and fixing a bug.
   Curation methodology appears aggregated, never as a line-by-line log.
3. **No number without a traceable source.** Missing values become
   `[VERIFICAR: ...]`, never a plausible estimate.
4. **No invented citations.** Unsupported references become
   `[CITAÇÃO NECESSÁRIA: ...]`.

### Configuration is required

`paper-writer` will not write a sentence until it finds a project config at
`.claude/paper-writer.md`. Copy the template and fill it in:

```bash
cp .claude/skills/paper-writer/references/project-config.template.md .claude/paper-writer.md
```

The config declares your canonical artifacts, your **forbidden** superseded
sources, the process narrative to keep out of the text, and your voice guide. See
[`example-config-ptbr-abnt.md`](skills/paper-writer/references/example-config-ptbr-abnt.md)
for a filled-in example.

This is deliberate. Without a declared artifact list, a writer agent under
pressure fills the gap with a plausible number — and a plausible number is
indistinguishable from a correct one until a reviewer checks.

---

## Using them together

Writing and reviewing are separate passes by design: whoever writes does not
approve their own text in the same context.

```
paper-writer  →  merge  →  paper-reviewer  →  fix  →  paper-reviewer again
```

Re-running the reviewer after corrections is cheap and is the intended use. PAT
gave one pass per manuscript; these skills have no such limit.

---

## Attribution

The segmentation + adaptive budget + parallel deep review + grounded
consolidation architecture is from:

> Jayaram, R., Tyler, D., Woodruff, D., Cortes, C., Matias, Y., Mirrokni, V., &
> Cohen-Addad, V. (2026). *Towards Automating Scientific Review with Google's
> Paper Assistant Tool.* arXiv:2606.28277.

This is an independent reimplementation on Claude Code subagents, written from
the paper. No code from PAT was used, and this project is not affiliated with or
endorsed by Google or Anthropic.

Stage 3.5 of `paper-reviewer` and the grounding contract of `paper-writer` are
original to this repository.

## How to cite

If you use these skills in published work, please cite the archived release:

> Raibolt, A. (2026). *paper-skills: deep pre-submission review and grounded
> drafting for scientific manuscripts* (v1.0.0). Zenodo.
> https://doi.org/10.5281/zenodo.21982661

The DOI above is the **concept DOI**: it always resolves to the most recent
version. To cite v1.0.0 specifically, use `10.5281/zenodo.21982662`.

Machine-readable metadata is in [CITATION.cff](CITATION.cff); GitHub's
"Cite this repository" button reads it.

## License

MIT — see [LICENSE](LICENSE).
