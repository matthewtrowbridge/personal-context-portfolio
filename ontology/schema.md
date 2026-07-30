# Ontology

The machine-readable definition is `ontology/schema.json`. `scripts/graph.py` reads that file — no rules are hardcoded in Python. **Extending the ontology is a JSON edit, not a code change.** This document explains the why.

## The shape of an entity

One markdown file per entity. YAML frontmatter carries structure; the body carries prose.

```yaml
---
id: paper:mispriced-asset-darden
type: paper
title: "The Mispriced Asset: Why AI Data Centers Need Health Impact Assessment"
status: drafting
domain: hip
sensitivity: T2
owner: person:matt-trowbridge
next_action: "Send Lenox email #1 (Becky drafts)"
updated: 2026-07-30
review_by: 2026-08-15
rel:
  authored_by: [person:matt-trowbridge, person:michael-lenox]
  targets:     [venue:darden-ideas-to-action]
  part_of:     [project:dc-health-impact]
---

Prose goes here. Everything an agent needs that isn't structured.
```

`id`, `type`, `title`, `status`, `domain`, `sensitivity`, and `updated` are required on every entity. Everything else is per-type and optional.

## Node types

Eight, and each has to earn its place. A type that doesn't change how work gets done is a type that just adds filing overhead.

| Type | Directory | Why it exists |
|---|---|---|
| `person` | `graph/people/` | Cadence-driven relationship upkeep; authorship; deference calibration |
| `org` | `graph/orgs/` | Clients, departments, publishers, partners |
| `project` | `graph/projects/` | The primary unit of work |
| `paper` | `graph/papers/` | The goal. First-class, not a project subtype. |
| `venue` | `graph/venues/` | Word limits, formats, review norms and response windows *drive drafting decisions* |
| `engagement` | `graph/engagements/` | Client work has a distinct shape; pairs with the engagement-brief pattern |
| `source` | `graph/sources/` | Evidence for papers; answers "what cites this" |
| `decision` | `graph/decisions/` | Gives a decision a date, a rationale, and a reversal trail |

**Deliberately not types.** `task` — a next action is a *field*, not an entity; one file per todo buries the graph. `artifact` — deliverables are files, tracked in a `deliverables:` list on their project or paper. `meeting` — meetings produce entity updates; they aren't entities.

## Edges

All relations live in a single `rel:` map. Not scattered top-level fields, not inline wikilinks. One place to parse, one place to validate, one place to extend. Wikilinks in prose are fine as reading affordances — the validator ignores them.

Closed vocabulary: `part_of`, `owns`, `authored_by`, `collaborates_on`, `targets`, `blocked_by`, `depends_on`, `cites`, `derived_from`, `supersedes`, `works_at`, `governed_by`, `relevant_to`.

Every target must resolve to an existing `id`. A dangling edge is an error, not a warning — silent broken links are how a graph rots.

## Status enums

Per type, defined in `schema.json`. The one that matters most:

**`paper`** — `idea → scoped → lit-complete → irb → data → analysis → drafting → internal-review → external-review → submitted → revision → accepted`, plus `shelved`. (`irb` is skipped when there's no human-subjects component.) Each transition has a gate artifact in `papers/<slug>/`.

## Sensitivity, and the word "tier"

`sensitivity: T1–T5` comes straight from the `hip-tier-router` skill, which stays the single authority.

**This repo is the T1/T2 spine.** T3 warns. T4 and T5 are hard errors — they belong in their secure homes, referenced here by pointer stub:

```yaml
sensitivity: T2
raw_location: "local:~/Projects/acme"   # a path that does NOT resolve in this repo
raw_sensitivity: T4
```

That's the raw-vs-signal rule: the durable signal travels, the raw artifact stays put.

`data_class` is **additive and orthogonal** — `[phi]`, `[irb]`, `[ferpa]` — not a competing tier system. `phi` is forbidden in the spine outright.

**Naming collision, resolved.** Notion's "Relationship Tier" means contact cadence; `hip-tier-router`'s "tier" means confidentiality. In this graph: `sensitivity:` for confidentiality, `contact_cadence:` for people. The bare word "tier" never appears as a field name.

## Deliverables

`project` and `paper` entities carry the finished outputs. This list is what makes things findable from a phone.

```yaml
deliverables:
  - title: "Data Center HIA — Executive Brief"
    type: pdf
    date: 2026-07-18
    version: v3
    status: final          # draft | final | sent | superseded
    share: link-view       # private | link-view | public — set deliberately at publish
    url: https://drive.google.com/file/d/...
    keywords: [materiality, HIA, siting]
    sent_to: [person:michael-lenox]
    sent_on: 2026-07-19
    mirror: true           # false for UVA-domain work — stays in the UVA tenant
```

`sent_to` / `sent_on` exist so the graph can always answer "which version did I actually send?" — the question that otherwise gets answered by scrolling through sent mail.

## Extending this

Add a node type, an edge, a status value, or a leakage pattern by editing `ontology/schema.json`. Run `python3 scripts/graph.py validate` to confirm nothing broke. No Python changes, ever — that separation is deliberate, because the ontology is durable and the tooling is not.
