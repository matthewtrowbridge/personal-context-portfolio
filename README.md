# Personal context spine

Matt Trowbridge's context library and agentic harness. A typed markdown entity graph in git,
plus the commands, skills, and subagents that operate on it.

The organizing goal is **output** — five to ten peer-review-level papers out the door. Everything
here is judged against that.

## The idea

The system is split in two, and the boundary never blurs:

| | **Substrate** — durable | **Harness** — disposable |
|---|---|---|
| What | Identity, voice, ontology, entities, manuscripts | `CLAUDE.md`, `.claude/`, `scripts/` |
| Format | Markdown + YAML frontmatter | Whatever the current tool wants |
| Lifetime | Years. Outlives any model or vendor. | Rebuilt whenever the field moves. |

**The invariant: the harness reads the substrate; the substrate never references the harness.**
No entity file mentions a command, a skill, or a model name. That one rule means a total harness
rewrite is a delete-and-regenerate, never a migration — which is the entire answer to "best
practices keep shifting."

## Layout

```
CLAUDE.md              always-on router (capped at 120 lines)
ontology/
  schema.json          the machine-readable ontology -- the validator reads THIS
  schema.md            node types and why each earns its place
  conventions.md       ids, dates, house style
graph/                 entities: people, orgs, projects, papers, venues,
                       engagements, sources, decisions
papers/<slug>/         per-manuscript stage artifacts
context/               the ten-file identity core
voice/                 voice profiles and real sent samples as ground truth
generated/             INDEX.md, OPEN-LOOPS.md, index.json, board.html -- derived, committed
scripts/               graph.py, build_board.py, sync_skills.py -- stdlib only
.claude/               commands, skills, subagents, hooks
stock/                 the upstream scaffold this repo started from. Reference only.
```

## Using it

```bash
python3 scripts/graph.py validate     # is the graph well-formed?
python3 scripts/graph.py index        # regenerate generated/
python3 scripts/graph.py audit        # health report + paper pipeline
python3 scripts/build_board.py        # generated/board.html

bash scripts/install_hooks.sh         # pre-commit validation
python3 scripts/sync_skills.py        # dry run; --apply to write to ~/.claude/skills
```

Commands: `/brief` · `/weekly` · `/paper <id> <stage>` · `/graph-audit` · `/board`

## Two properties worth protecting

**Progressive disclosure.** Agents read `generated/INDEX.md` or `OPEN-LOOPS.md`, then the three to
six entities they need — never `graph/` in bulk. A task stays around 10k tokens whether the graph
holds 25 entities or 500. Bulk-reading breaks this permanently.

**Zero-cost maintenance.** `scripts/` is standard-library Python with no network calls, no API
keys, and no model calls. CI enforces it. Graph upkeep that costs tokens is graph upkeep that
doesn't happen.

## Sensitivity

This repo is the **T1/T2 spine**. T3 warns; T4 and T5 are hard errors, caught by the validator.
Anything more sensitive stays in its secure home and is referenced by pointer:

```yaml
sensitivity: T2
raw_location: "local:~/Projects/acme"
raw_sensitivity: T4
```

The `hip-tier-router` skill is the single authority on tiers. `data_class` (`phi`, `irb`, `ferpa`)
is additive and orthogonal — not a competing model. `phi` is forbidden here outright.

## Extending it

Add a node type, edge, status value, or leakage pattern by editing `ontology/schema.json`. The
validator reads that file; there is no Python to change. That separation is deliberate.

---

Started from Anthropic's [personal context portfolio](https://github.com/anthropics) scaffold,
preserved under `stock/`.
