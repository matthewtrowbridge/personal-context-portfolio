---
description: Validate the context graph, regenerate the index and board, and report on its health
argument-hint: "[--fix]"
allowed-tools: Bash, Read, Edit, Glob, Grep
model: claude-haiku-4-5-20251001
---

Run the graph health check. This is mechanical work — stay on the cheap model and do not
editorialize.

1. `python3 scripts/graph.py audit`
2. If there are errors, fix the mechanical ones directly: malformed frontmatter, id/filename
   mismatches, bad enum values, wrong directory for a type. Re-run until clean.
3. Do **not** silently fix these — report them and stop:
   - a dangling edge (the target may need creating, or the edge may be wrong)
   - any sensitivity or leakage error (that is a judgment call, and the whole point of the check)
4. `python3 scripts/graph.py index` then `python3 scripts/build_board.py`
5. Report in this order: errors fixed, errors needing a decision, warnings worth acting on,
   and the entity counts.

If `$ARGUMENTS` contains `--fix`, also propose (do not apply) frontmatter updates for entities
flagged stale — the fix for staleness is a real content update, never just bumping `updated`.
