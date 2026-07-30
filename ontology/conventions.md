# Conventions

## Identifiers

`id` is `type:slug`, and it must match the file path:

```
graph/papers/mispriced-asset-darden.md   →   id: paper:mispriced-asset-darden
graph/people/andrew-taylor.md            →   id: person:andrew-taylor
```

Slugs are lowercase kebab-case: `^[a-z][a-z0-9-]*$`. Directory names are plural (`people/`, `papers/`); type prefixes are singular (`person:`, `paper:`). The validator enforces the correspondence, so an id can never drift from its filename.

Slugs are permanent. Renaming one breaks every edge pointing at it — if something genuinely must be renamed, create the new entity and link the old one with `supersedes`.

## Dates

ISO 8601, always: `2026-07-30`. Never `07/30/26`.

- `updated` — last meaningful change. Bump it when the content changes, not when a typo is fixed.
- `review_by` — when this must next be looked at. A past date is an **error**, not a warning: the point is that it's impossible to ignore.
- `stage_entered` (papers) — drives the days-in-stage number in `/weekly`.

## What goes in frontmatter vs the body

Frontmatter is for anything that needs to be **queried, filtered, or validated**. The body is for anything that needs to be **read**.

If you find yourself writing prose into a frontmatter field, it belongs in the body. If you find yourself grepping the body for something structured, it belongs in frontmatter.

## Body structure

No fixed template — entities differ. But keep them **one page, not five**. The stock interview protocol in `stock/interview-protocol/` puts it well: a good context file is short enough to load without thinking about it.

Front-load the useful part. An agent reading three entities to answer a question should get what it needs from the first paragraph of each.

## Sensitivity discipline

Before writing anything into this repo, ask what tier it is. When unsure between two, **choose the more sensitive one** — that rule comes from `hip-tier-router` and it holds here.

Never paste into the spine: verbatim transcripts, cash/burn/runway figures, cap tables, investor lists, personal contact details beyond a work email, PHI, or anything from a signed agreement. The validator scans for these, but it catches patterns — it can't catch judgment.

For sensitive context you'll need later, write the **signal**, not the raw: the fact and its implication, not the numbers or the quote.

## House style

The repo has an established voice from the stock scaffold; entities should match it.

- Em-dash asides are fine. Emoji are not — nowhere in the repo.
- Sentence-case headings.
- Second person in guidance docs, third person in entity prose.
- No bold-heavy hype. Bold only where it helps someone scan.
- Prefer a short concrete sentence over a long hedged one.

## Generated files

Everything in `generated/` is derived and committed. **Never hand-edit it.** If a generated file looks wrong, the fix is in the source entity or the generator, and the nightly audit will overwrite your edit anyway.

Committing generated output is deliberate — it means a fresh clone, or an agent on another machine, gets a working index without running anything first.

## Adding an entity

1. Pick the type. If none fits, don't invent one — ask whether it's really a field on an existing type.
2. Create `graph/<type>s/<slug>.md` with the required fields.
3. Link it. An entity with no edges is an orphan, and the validator will say so.
4. Run `python3 scripts/graph.py validate`.
5. Run `python3 scripts/graph.py index` to refresh `generated/`.
