# Matt Trowbridge — context spine

Physician, academic, and consultant working across four domains. The organizing goal
right now is **output**: five to ten peer-review-level papers out the door. Judge work
against that — does this move a manuscript, or not?

## Domains, and which skill governs each

| Domain | What it is | Voice / brand skill |
|---|---|---|
| `hip` | Health Intent Partners consulting | `hip-brand`, handling via `hip-tier-router` |
| `uva-em` | UVA Emergency Medicine, residency research | `uva-em-voice`, IRB via `uva-irb-navigator` |
| `mdp-hds` | Medical Design Program / Health Design Sprint | `mdp-hds-brand` |
| `red-cell` | Red Cell Partners and portfolio companies | `red-cell-style` |

Universal email defaults live in `matt-email-voice`; each domain layers on top of it.
Never mix registers — a HIP document written in the UVA EM voice is wrong, and vice versa.

## Sensitivity — non-negotiable

**This repo is the T1/T2 spine.** T3 warns, T4 and T5 are errors. Never write into it:
verbatim transcripts, cash or runway figures, ownership tables, investor lists, personal
contact details beyond a work email, PHI, or the contents of signed agreements.

For sensitive material, write the **signal** — the fact and its implication — and leave the
raw where it lives, referenced with `raw_location` / `raw_sensitivity`. Full rules in the
`hip-tier-router` skill, which is the single authority. When torn between two tiers, pick
the more sensitive one.

`scripts/graph.py validate` enforces this, but it catches patterns, not judgment.

## The read protocol

**Never read `graph/` in bulk.** It defeats the whole design and the cost stays bounded only
if you don't.

1. Start at `generated/OPEN-LOOPS.md` for "what needs me" questions, or
   `generated/INDEX.md` to locate entities.
2. Read the 3–6 entity files you actually need.
3. Stop.

That keeps a task around 10k tokens whether the library holds 25 entities or 500.

## Where things live

| Path | What |
|---|---|
| `ontology/schema.json` | The machine-readable ontology. **The validator reads this** — extending the graph is a JSON edit, never a code change. |
| `ontology/schema.md`, `conventions.md` | Human docs for the above |
| `graph/<type>s/<slug>.md` | Entities. `id` is `type:slug` and must match the path. |
| `papers/<slug>/` | Per-manuscript stage artifacts (`01-scope.md`, …) |
| `context/` | The ten-file identity core |
| `voice/profiles/`, `voice/samples/` | Voice specs, and real sent artifacts as ground truth |
| `generated/` | Derived and committed. **Never hand-edit.** |
| `stock/` | The upstream scaffold. Reference only — not Matt's content. |

## Commands

`/brief` · `/weekly` · `/paper <id> <stage>` · `/graph-audit` · `/board`

## Model routing

Match the job to the tier; it's the difference between a system that's affordable and one
that isn't.

- **Script, no model** — validate, index, build the board. Graph upkeep must never cost tokens.
- **Haiku** — mechanical volume: capture triage, frontmatter repair, link checks.
- **Sonnet** — throughput: literature screening, section drafts, imports.
- **Opus** — judgment: synthesis, argument structure, voice passes, adversarial review.

Do agentic work in first-party surfaces (Claude Code CLI, claude.ai) so it draws the
subscription rather than per-token billing. **No API keys in this repo, ever.**

## The invariant that makes this durable

**The harness reads the substrate; the substrate never references the harness.**

Substrate — `context/`, `graph/`, `voice/`, `ontology/`, `papers/` — is durable and outlives
any tool. Harness — `CLAUDE.md`, `.claude/`, `scripts/` — is disposable and gets rebuilt
whenever the field moves.

So: no entity file ever mentions a command, a skill, or a model name. Keep that line clean
and a total harness rewrite is a delete-and-regenerate rather than a migration.

## Working habits

- Entities are one page, not five. Front-load the useful part.
- Frontmatter is for what gets queried; the body is for what gets read.
- After editing `graph/`, run `python3 scripts/graph.py validate`, then `index`.
- An entity with no edges is an orphan. Link it or don't create it.
- Slugs are permanent — renaming breaks every edge pointing at it. Use `supersedes` instead.
- Dates are ISO 8601. Always.
