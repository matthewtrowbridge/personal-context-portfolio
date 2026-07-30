---
name: context-graph
description: How to read, write, and extend Matt's personal context graph — the typed markdown entity library in graph/. Use whenever creating or editing an entity (person, org, project, paper, venue, engagement, source, decision), adding a relation, deciding what belongs in frontmatter versus prose, extending the ontology, or answering a question that requires looking things up in the graph. Also triggers on "add this to the system", "what do we know about X", dangling edges, validator errors, and progressive-disclosure questions about token cost.
---

# Context graph

The durable substrate: one markdown file per entity, YAML frontmatter for structure, prose for
everything else. Plain files in git, so no tooling change can strand it.

## Reading — the protocol that keeps cost flat

**Never read `graph/` in bulk.** The design only pays off if you don't.

1. `generated/OPEN-LOOPS.md` for "what needs me" questions.
2. `generated/INDEX.md` to locate entities by id, title, type, status, domain.
3. Read the 3–6 entity files you actually need. Stop there.

A task stays around 10k tokens whether the graph holds 25 entities or 500. Bulk-reading breaks
that property immediately and permanently.

## Writing an entity

```yaml
---
id: paper:some-slug          # type:slug, must match the file path
type: paper
title: "Full title"
status: drafting             # enum is per-type, see ontology/schema.json
domain: hip                  # hip | uva-em | mdp-hds | red-cell | personal
sensitivity: T2              # T1/T2 only in this repo
owner: person:matt-trowbridge
next_action: "The one visible next step"
updated: 2026-07-30
rel:
  part_of:     [project:something]
  targets:     [venue:somewhere]
  authored_by: [person:matt-trowbridge]
---

One page of prose. Front-load the useful part.
```

Required on everything: `id`, `type`, `title`, `status`, `domain`, `sensitivity`, `updated`.

Rules that matter:

- **Frontmatter is for what gets queried; the body is for what gets read.** Prose in a frontmatter
  field belongs in the body. Grepping the body for something structured means it belongs in
  frontmatter.
- **All edges go in one `rel:` map.** Never scattered top-level fields. Closed vocabulary — see
  `ontology/schema.json`. Every target must resolve; dangling edges are errors.
- **Slugs are permanent.** Renaming breaks every edge pointing at it. To replace an entity, create
  the new one and link the old with `supersedes`.
- **One page, not five.**
- An entity with no edges is an orphan. Link it or don't create it.

## Sensitivity

`sensitivity: T1–T5` from the `hip-tier-router` skill, which stays the single authority. **This
repo is T1/T2.** T3 warns; T4 and T5 are hard errors.

For anything more sensitive, write the signal and point at the raw:

```yaml
sensitivity: T2
raw_location: "local:~/Projects/acme"     # deliberately does not resolve here
raw_sensitivity: T4
```

`data_class` (`phi`, `irb`, `ferpa`) is additive and orthogonal — not a second tier system. `phi`
is forbidden in this repo outright.

Note the naming collision, already resolved: `sensitivity` means confidentiality;
`contact_cadence` means how often to stay in touch. The bare word "tier" is never a field name.

## Extending the ontology

Add a node type, edge, status value, or leakage pattern by editing **`ontology/schema.json`**.
The validator reads that file — there is no Python to change. That separation is deliberate: the
ontology is durable, the tooling is not.

## After any edit

```
python3 scripts/graph.py validate
python3 scripts/graph.py index
```

The validator is a plain script with no model calls and no network. Graph upkeep must never cost
tokens, or it won't get done.

## References

- `ontology/schema.json` — the machine-readable definition
- `ontology/schema.md` — node types and why each earns its place
- `ontology/conventions.md` — ids, dates, house style, adding an entity
