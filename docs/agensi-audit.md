# Agensi audit — local path dependencies

Scope: every file that ships inside a skill (`skills/paper-reviewer/**`,
`skills/paper-writer/**`) plus the parts of `README.md` that tell a user how to
set a skill up. Line numbers refer to commit `3318eec`.

The question asked of each file: **does this still work if the skill is not
sitting at `.claude/skills/<name>/` on the user's disk?** Agensi's terms say
nothing is saved on the buyer's machine; Agensi support says the buyer's agent
runs the bundled scripts. Until that is settled, the skill has to work in three
situations:

| | Situation | What the agent has |
|---|---|---|
| S1 | Local install (`npx skills add`) | the skill directory on disk, at an agent-specific location |
| S2 | Delivered with files | the skill directory on disk, at an unknown location |
| S3 | Delivered as context only | the text of `SKILL.md`; reference files possibly unreachable by path |

## Summary

| ID | File | Line | Severity | Breaks in |
|---|---|---|---|---|
| W1 | `skills/paper-writer/SKILL.md` | 23 | High | S2, S3 |
| W2 | `skills/paper-writer/references/project-config.template.md` | 3–4 | Medium | S1, S2, S3 |
| W3 | `skills/paper-writer/references/project-config.template.md` | 9 | Low | S1, S2, S3 |
| R1 | `skills/paper-reviewer/SKILL.md` | 188–192 | High | S1, S2, S3 |
| R2 | `skills/paper-reviewer/SKILL.md` | 194 | Medium | S3 |
| D1 | `README.md` | 259–264 | High | S1 (partly), S2, S3 |

Severity is about the user-visible consequence: **High** stops the skill or
silently degrades a result, **Medium** produces a wrong or confusing artifact,
**Low** is a dangling pointer.

No fixed `.claude/skills/...` path appears inside either skill. The only one in
the repository is in the README (D1).

## Findings

### W1 — the writer tells the agent to copy a file out of the skill folder

`skills/paper-writer/SKILL.md:23`

> **Se não existir nenhum, pare e peça.** Copie
> `references/project-config.template.md` (desta skill) para o projeto, peça ao
> usuário para preencher, e só então prossiga.

**Risk.** "Copy" is a filesystem operation on a source the agent may be unable to
locate. In S2 the agent has to guess where "this skill" lives; in S3 there is no
file to copy and the skill stops at its very first step with nothing the user
can do about it.

**Proposed fix.** Replace the copy with a create: the agent reads
`references/project-config.template.md`, resolved against the directory that
holds `SKILL.md`, and **writes** `.claude/paper-writer.md` in the project with
that content. Then it stops and asks the user to fill it in, exactly as today.
The requirement itself does not move: no config, no writing.

For S3, add one fallback sentence: if the template cannot be read, the agent
builds the file from the four blocks already tabulated at `SKILL.md:27–34` and
says that it did so. See decision 1 below.

### W2 — the template's first line is an instruction that becomes false once copied

`skills/paper-writer/references/project-config.template.md:3–4`

> Copie este arquivo para `.claude/paper-writer.md` na raiz do repositório do seu
> manuscrito e preencha. A skill não escreve nada até encontrá-lo.

**Risk.** After W1 is fixed the agent creates the config from this content, so
the user opens `.claude/paper-writer.md` and reads an instruction to copy the
file to where it already is. It also repeats the copy-from-a-folder assumption.

**Proposed fix.** Reword so the sentence is true in both places: this is the
project config for `paper-writer`, it lives at `.claude/paper-writer.md`, fill
in every block, the skill writes nothing until it is filled in.

### W3 — the template points at a sibling file by bare name

`skills/paper-writer/references/project-config.template.md:9`

> Há um exemplo completo e preenchido em `example-config-ptbr-abnt.md`.

**Risk.** Correct inside `references/`, dangling once the content lives in
`.claude/paper-writer.md`: the user has no such file next to it.

**Proposed fix.** Say where the example actually is — it ships with the skill
under `references/` and is in the GitHub repository — and that the agent can
show it on request.

### R1 — the reviewer hands a relative path to a subagent

`skills/paper-reviewer/SKILL.md:188–192`

> lives in `references/stage-3-5-language-signature.md`. The dispatching prompt
> must carry that path, plus the lexicon matching the manuscript's language —
> `references/lexicons-en.md` […] or `references/lexicons-pt.md` […] — and the
> instruction to **read both in full before measuring**.

**Risk.** The paths are relative to the skill directory, which is right. The
problem is who resolves them. The Stage 3.5 reviewer is a subagent whose working
directory is the user's project, so `references/lexicons-en.md` resolves to
`<project>/references/lexicons-en.md`, which does not exist. The subagent then
either fails or, worse, measures from memory — the outcome line 194 forbids.
This affects the current local install too, not only Agensi.

**Proposed fix.** Keep the references relative to the skill directory in the
text, and move the reading to the only agent that knows where the skill is: the
main agent reads the instrument and the matching lexicon in full, resolving both
against the directory that holds `SKILL.md`, and pastes their **content** into
the Stage 3.5 prompt. The subagent receives no skill path at all. Nothing in the
instrument or the thresholds changes.

### R2 — no stated behaviour when the instrument cannot be read

`skills/paper-reviewer/SKILL.md:194`

> This stage does not run from a memory of this file.

**Risk.** In S3 the instrument and the lexicons may be unreachable. The line
forbids running from memory but does not say what to do instead, so the outcome
is left to the agent.

**Proposed fix.** If the instrument or the matching lexicon cannot be read,
Stage 3.5 does not run, and the report states explicitly that it was **not
executed** and why, worded so that it cannot be read as a clean result. This is
consistent with the existing rule that a quiet result must never read as
"checked and clean". See decision 2 below.

### D1 — the README's setup command hard-codes the install location

`README.md:259–264`

```bash
cp .claude/skills/paper-writer/references/project-config.template.md .claude/paper-writer.md
```

**Risk.** The source path only exists for a project-level install with
`--agent claude-code`. It is wrong with `--global` (the skill is under the home
directory), with `skills use` (temporary directory, which the README itself
recommends as the default), with any other agent, and for an Agensi install. It
is also a POSIX command shown to Windows users.

**Proposed fix.** Remove the `cp` block. Say that on first run the skill creates
`.claude/paper-writer.md` from its template and stops until it is filled in,
and that this is the same for a project install, a global install and an Agensi
install. Keep the link to the filled-in example.

## Checked, no change needed

| File | Line | What | Why it is fine |
|---|---|---|---|
| `skills/paper-writer/SKILL.md` | 19–21 | config looked up at `.claude/paper-writer.md`, then `paper-writer.config.md`, then a user-given path | paths in the **user's project**, not in the skill; two alternatives already exist for agents that do not use `.claude/` |
| `skills/paper-writer/SKILL.md` | 23 | pointer to `references/example-config-ptbr-abnt.md` | already relative to the skill directory; only the wording around it changes with W1 |
| `skills/paper-writer/SKILL.md` | 96–108 | subagent dispatch | uses the built-in `general-purpose` type; no agent definition file is expected anywhere. Rules and voice guide are pasted into the prompt, so the subagent needs no skill file. Every path it receives is a project path |
| `skills/paper-reviewer/SKILL.md` | 97–113 | subagent dispatch | same: built-in type, no definition file, project paths only. The single exception is Stage 3.5 (R1) |
| `skills/paper-reviewer/references/stage-3-5-language-signature.md` | 8–9, 92–93 | links to `lexicons-en.md` / `lexicons-pt.md` | sibling-relative; hold as long as `references/` is kept intact. **Constraint for the packaging script:** do not flatten the directory |
| `skills/paper-reviewer/references/lexicons-en.md`, `lexicons-pt.md` | — | — | no path references |
| `skills/paper-writer/references/example-config-ptbr-abnt.md` | 15–40 | paths such as `tese/tese.tex`, `data/outputs/…` | fictional example content, declared as such on line 3 |
| `skills/*/SKILL.md` | writer 108, 128; reviewer 238 | output paths `rascunhos/…`, `reviews/…` | relative to the manuscript, in the user's project |
| `README.md` | 46 | "Installs into `.claude/skills/`" | describes what the command above it does with `--agent claude-code`; accurate |
| `README.md` | 201, 226–227, 268 | links into `skills/…/references/` | repository links for GitHub readers |

Neither skill ships a script, a subagent definition file or a template other
than the writer's project config.

## Decisions taken

Recorded on 2026-10-13, after review of the findings above.

1. **Fallback when the template is unreachable (W1).** A one-sentence fallback
   that rebuilds the config from the four blocks already described in
   `SKILL.md`. The template is not inlined: two copies would drift, and it would
   add about 90 lines to a file loaded on every use.
2. **Stage 3.5 when the instrument is unreachable (R2).** Included. The report
   must say that Stage 3.5 was not executed and why, in terms that cannot be read
   as a clean result.
3. **R1 is fixed by content, not by path.** The main agent reads the instrument
   and the lexicon and passes their content to the subagent.
4. **Language of the writer skill.** The body of `skills/paper-writer/SKILL.md`
   and both of its reference files are in Portuguese; only the frontmatter is in
   English. The fixes for W1-W3 are written in Portuguese to match. The skill is
   not translated.
