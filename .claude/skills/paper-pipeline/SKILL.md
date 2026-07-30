---
name: paper-pipeline
description: The manuscript pipeline — stage definitions, gate criteria, and per-stage artifacts for moving papers from idea to accepted. Use when advancing a manuscript, scoping a new paper, deciding whether a draft is ready for the next stage, preparing a submission, choosing a target venue, or answering "what's blocking this paper". Triggers on manuscript, paper, submission, peer review, IMRaD, systematic review, target venue, revision.
---

# Paper pipeline

The goal is five to ten peer-review-level papers out the door. This pipeline exists because the
failure mode is not bad writing — it is manuscripts sitting at a stage for months with no gate
telling anyone they are stuck.

## Stages

```
idea → scoped → lit-complete → irb → data → analysis → drafting
     → internal-review → external-review → submitted → revision → accepted
```

Also `shelved`, which is a legitimate outcome and better than pretending. Skip `irb`, `data`, and
`analysis` for conceptual or practitioner pieces.

## Gates

A stage advances only when its artifact exists and its criteria are met. **Skipping a gate is how
a paper reaches submission and gets rejected for something knowable in week one.**

| Stage | Artifact in `papers/<slug>/` | Criteria |
|---|---|---|
| scoped | `01-scope.md` | Research question stated. Contribution claim in one sentence. Target venue chosen with its word limit. Authorship agreed with everyone named. |
| lit-complete | `02-lit.md` + `source` entities | Gap statement defensible. Key prior work cited. Search strategy recorded if the venue expects one. |
| irb | `03-irb.md` | Submission prepared via `uva-irb-navigator`. Determination recorded. |
| data / analysis | `04-analysis.md` | Data sources named. Analysis plan written **before** results are interpreted. |
| drafting | `05-draft.md` | Full argument end to end. Holes marked explicitly. No placeholder sections. |
| internal-review | `06-internal.md` | Voice pass done. Argument structure checked. Every claim traceable to evidence. |
| external-review | `07-reviewer2.md` | `reviewer-2` run and every fatal finding answered. Cross-model second pass for high-stakes venues. |
| submitted | `08-submission.md` | Venue checklist complete: format, word count, figures, disclosures, cover letter. |

## Scoping well

The contribution claim is the whole game. Write it as one sentence before anything else:

> This paper shows that ___, which matters because ___, and which no one has shown because ___.

If the third clause is hard to fill, the gap may not be real. Find that out at `scoped`, not at
`external-review`.

## Venue fit

Read the `venue` entity before drafting, not after. Word limits, review norms, and response
windows change the artifact, not just its formatting. Two specific traps:

- **Practitioner outlets** want the argument first and no literature-review throat-clearing.
  Academic habits read as evasion there.
- **Response and correspondence formats are perishable.** They have windows that close. If the
  window has passed, the honest options are reframe as standalone or shelve — not "draft it anyway."

## Keeping the graph honest

On every stage change, update the paper entity: `status`, `stage_entered` (today), `next_action`,
`updated`. `stage_entered` is what makes days-in-stage real, and days-in-stage is what makes
`/weekly` able to say "this has not moved in four months."

Never advance two stages in one pass. Run it twice so each gate leaves its artifact.

## When a paper is stuck

Diagnose which it is, because the fixes are unrelated:

- **Blocked on a person** — the action is a message, not writing. Usually the cheapest unblock available.
- **Blocked on a decision** — make it or shelve it. Undecided papers consume attention silently.
- **Blocked on work** — schedule it and stop calling it blocked.
- **Blocked on funding or approval** — check whether the *next* section actually requires it. Often it doesn't.
