---
name: hip-tier-router
description: Classify and route any Health Intent Partners (HIP) file, note, transcript, task, or new client engagement into HIP's 5-tier confidentiality model, and say exactly where it should live, what may sync, what AI may read, and the git/handling rules. Use this whenever setting up or organizing a HIP engagement or client folder, migrating files toward git, or deciding storage for anything sensitive — and whenever the user asks "what tier is this," "where should this live/go," "is this safe for git/Notion/the cloud," "can I commit/sync/share this," or is about to store transcripts, contracts, cash/cap-table/M&A/investor info, strategy memos, or reusable playbooks. Trigger even if the user never says the word "tier."
---

# HIP tier router

## Why this exists
HIP works across many client engagements. The most sensitive material — call transcripts, cash/M&A signals, cap tables, signed contracts — is often also the most important context for good thinking, which creates a trap: lock it down and you lose it from your working context; expose it and you breach confidentiality. This skill resolves that by classifying every item into a sensitivity tier, routing it to the right home, and separating the **raw artifact** (which stays secured) from its **distilled signal** (which travels). Apply it so storage decisions are consistent, sensitive data never lands in the wrong place, and every new engagement is set up the same way.

## The five tiers (quick reference; full detail in references/tier-model.md)
- **T1 Public** — marketing-safe / already public. Anywhere; any AI.
- **T2 HIP IP** — Matt's frameworks, playbooks, methods, client-agnostic theses. Private HIP-org repo; AI-readable.
- **T3 Client internal** — Matt's work *about* a client: strategy, prep, analysis, dossiers. Private per-client repo; local AI.
- **T4 Client confidential** — the client's info entrusted to Matt: verbatim transcripts, cash/burn, M&A, cap tables, investor lists, PII. Encrypted vault / E2EE; never a plaintext host; AI only when the user decrypts it in-session.
- **T5 Legal/contract** — signed agreements, NDAs. Encrypted archival; no AI; never git.

## How to classify (take the first that matches)
1. Signed legal/contract doc? → **T5**.
2. Contains the client's confidential info entrusted to you — verbatim transcript, cash/burn/runway, fundraise/M&A, cap table, investor names/emails, personal data? → **T4**.
3. Your work product *about* the client — strategy, prep, product/market analysis, dossiers? → **T3**.
4. Your generalizable IP — a framework, playbook, method, or client-agnostic thesis? → **T2**.
5. Marketing-safe / fully public? → **T1**.

Mixed content takes the tier of its **most sensitive element**. To share or sync a lower tier, produce a sanitized derivative (paraphrase/remove the sensitive parts) rather than downgrading the original.

## What to output when classifying
Be decisive and consistent. For each item, return:
- **Tier** + a one-line reason.
- **Storage home** (iCloud archive / private per-client repo / HIP-org repo / encrypted vault).
- **Syncs?** and **AI may read?** (yes / only on decrypt / no).
- **Git rule** (commit OK / gitignore / never; note "git-crypt if it must ride on git").
- **Action flags** — e.g., "scrub verbatim quotes before push," "add to .gitignore," "distill the signal into the engagement brief," "store the contract in the vault, not git."

**Example**
Input: "A Zoom transcript of a client's board call."
Output: **T4** (client confidential, verbatim). Home: encrypted vault / local. Syncs: only encrypted. AI: only when you decrypt it in-session. Git: never — add `*Transcript*.txt` to `.gitignore`. Action: distill the durable signal into the engagement brief so the context still travels.

## The raw-vs-signal rule (do this every time)
When something sensitive (T3/T4/T5) carries context you'll need later, **distill its durable signal** — the facts and implications, not the raw text/numbers — into the engagement's **portable context layer** (the always-loaded Engagement Brief + memory). The raw artifact stays in its secure home; the signal travels across sessions and machines. This is how sensitive context stays usable without the sensitive data leaving its vault.

## Routing & storage homes
- **iCloud (or equivalent) archive** = the full record, all tiers — system of record, especially for raw T4/T5.
- **`~/Projects/<repo>` working copies** → private GitHub repos: **HIP-org repo** (T2) and **per-client repo** (T3). Keep git working copies out of iCloud (sync churn).
- **Encrypted vault / E2EE** = raw T4/T5. A private repo is access-controlled, **not** hidden from the host — for sensitive-on-git, encrypt first (e.g., git-crypt) so the host sees only ciphertext; keep signed contracts (T5) in a dedicated vault, not git.
- **AI boundary:** AI reads the portable context layer + T2 + T3 by default; it reads raw T4/T5 only when the user decrypts and provides it in-session.
- **Action boundary:** never create remotes, change repo visibility/permissions, or push on the user's behalf — prepare the commands and hand them over; the user pushes.

## New-engagement setup mode
When starting or organizing a new HIP client, scaffold consistently:
1. Create the client folder with numbered subfolders for the work; keep raw T4/T5 in clearly separable folders (e.g., `Company Intel/`, `Contracts/`, `Timelog/`, `transcripts/`).
2. Drop in the per-client **`.gitignore`** (references/gitignore-template.txt) excluding all T4/T5 paths + any `evidence-local/` + T2 staging.
3. Create the **Engagement Brief** (references/engagement-brief-template.md) and make it read-me-first (the portable context layer).
4. Map the two repos: `~/Projects/<client>` (T3, private per-client repo) and `~/Projects/hip-infrastructure` (T2, HIP-org repo).
5. Classify existing files into tiers and route them.

## Guardrails
- A **private repo is not encryption** — fine for T2/T3, wrong for raw T4/T5.
- Never put T4/T5 in plaintext on a hosted service or let cloud AI index it.
- When unsure between two tiers, choose the **more** sensitive one.
- Don't let convenience override confidentiality obligations (NDAs, client agreements) — when a confidentiality term is in play, flag it rather than assuming.

## References
- `references/tier-model.md` — full tier table (storage/AI/git) with worked classification examples.
- `references/gitignore-template.txt` — per-client `.gitignore` starter.
- `references/engagement-brief-template.md` — the portable context-layer template.
