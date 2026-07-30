---
description: Advance a manuscript through a pipeline stage and produce that stage's gate artifact
argument-hint: "<paper-id> <stage>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
model: claude-opus-5
---

Advance a manuscript. Arguments: `$ARGUMENTS` — a paper id (with or without the `paper:` prefix)
and a target stage.

**Load the `paper-pipeline` skill first.** It holds the stage definitions, gate criteria, and
venue conventions; this command is only the orchestration.

Steps:

1. Read the paper entity in `graph/papers/`. Read its `targets:` venue entity — word limits and
   review norms change what the artifact should be.
2. Check the gate for the requested stage. **If the current stage's criteria are not met, say so
   and stop.** Skipping a gate is how manuscripts reach submission and get rejected on something
   that was knowable in week one.
3. Produce the stage artifact in `papers/<slug>/` using the numbering in `paper-pipeline`.
4. Update the entity: `status`, `stage_entered` (today), `next_action`, `updated`.
5. Run `python3 scripts/graph.py validate` then `index`.
6. Report what changed and what the next gate requires.

Never advance more than one stage per invocation. If the work for two stages is genuinely done,
run it twice so each gate leaves its own artifact.
