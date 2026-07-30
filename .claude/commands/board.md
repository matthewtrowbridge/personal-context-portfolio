---
description: Rebuild the deliverables board from the graph
allowed-tools: Bash, Read
model: claude-haiku-4-5-20251001
---

Rebuild the board.

1. `python3 scripts/graph.py validate` — stop if there are errors; a board built from a broken
   graph is worse than no board.
2. `python3 scripts/graph.py index`
3. `python3 scripts/build_board.py`
4. Report: entity count, how many projects and manuscripts rendered, and how many deliverables
   have no `url` (those are invisible on the phone, which is the whole point of the board).

Deploy is not automated yet — Cloudflare Pages setup lands in Phase 1. For now say where the
file is and note that opening it locally works.
