---
description: Standing brief — what needs Matt today, across all domains or one
argument-hint: "[domain: hip | uva-em | mdp-hds | red-cell]"
allowed-tools: Read, Glob, Grep, Bash
model: claude-haiku-4-5-20251001
---

Produce the standing brief. Optional domain filter: `$ARGUMENTS`.

**Read protocol — follow it exactly.** Read `generated/OPEN-LOOPS.md`, then only the entity
files you actually need to explain something. Do not read `graph/` in bulk.

Output, in this order and nothing else:

1. **Needs you today** — overdue items and anything due within three days. For each: the entity,
   the next action, and how long it has been sitting. Lead with the one that unblocks the most.
2. **Moving** — items with recent activity, one line each.
3. **Quietly stuck** — active status but no update in 45+ days. Name them plainly. This is the
   section that earns the brief; do not soften it.

Rules:

- One line per item. No preamble, no summary paragraph, no encouragement.
- Never invent a next action. If an entity has none, say "no next action set" — that is itself
  the finding.
- If nothing is overdue, say so in one line and move on.
