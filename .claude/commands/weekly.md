---
description: Weekly review — what moved, what stalled, one next action per project and paper
allowed-tools: Read, Glob, Grep, Bash, Edit
model: claude-sonnet-5
---

Run the weekly review. This is the loop that keeps manuscripts moving; treat it as the most
important recurring job in the system.

**Setup:** run `python3 scripts/graph.py audit` first, then read `generated/OPEN-LOOPS.md`.
Read individual entities only as needed.

Produce:

1. **Manuscripts** — the pipeline, most-advanced first. For each: stage, days in stage, next
   action, and what blocks it. Flag anything that has not changed stage in 30+ days. Getting
   papers out is the goal, so this section leads.
2. **Projects** — status, next action, anything overdue.
3. **Parking lot** — `status: idea` and `parking-lot` entities with their trigger conditions.
   These are not nags; surface them only so a changed world can resurface them.
4. **The one thing** — a single recommendation for the week, argued in two sentences. Prefer
   whatever unblocks the most downstream work over whatever is easiest.
5. **Graph health** — one line: entity count, errors, stale count.

Then offer to update `next_action` and `updated` on anything that has actually moved. Ask before
editing; never bump `updated` without a real content change, because that turns the staleness
check into decoration.

Be direct about what is not moving. A weekly review that reads as reassuring is not doing its job.
