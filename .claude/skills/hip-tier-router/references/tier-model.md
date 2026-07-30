# HIP 5-Tier Model — full reference

| Tier | What it is | Storage | Cloud AI | Hosted git |
|---|---|---|---|---|
| T1 Public | Marketing-safe, public facts/papers | Any substrate | OK | OK (any) |
| T2 HIP Internal | Frameworks, playbooks, methods, client-agnostic theses | HIP Infrastructure | OK | Private HIP-org repo |
| T3 Client Internal | Work *about* a client: strategy, prep, analysis, dossiers | Per-client folder | Local AI only | Private per-client repo |
| T4 Client Confidential | Client CI entrusted to you: transcripts, cash/burn, M&A, cap table, investor lists, PII | Local / E2EE only | No cloud indexing | Never (or git-crypt ciphertext only) |
| T5 Legal/Contract | Signed agreements, NDAs | Encrypted archival, immutable | No | Never |

## Worked examples
- A markdown strategy memo you wrote analyzing a client's product → **T3**.
- A reusable "deal-structure playbook" with no client specifics → **T2**.
- A CSV of a client's burn rate and runway → **T4** (never git).
- A signed advisory agreement PDF → **T5** (vault, no AI).
- A blog post draft for public release → **T1**.
- A strategy doc that quotes a client transcript verbatim → **T3 doc with a T4 element**: keep local or paraphrase the quotes before any push; the full transcript stays T4.
- An investor-update email listing investor names/emails → **T4** (PII + confidential).

## The raw-vs-signal split
- Raw artifact (transcript, cap table, contract) → secure home, by tier.
- Distilled signal (durable facts + implications) → the portable context layer (Engagement Brief + memory), which is T3 and syncs. Keep the most sensitive specifics out of the signal layer (abstract them).

## Using GitHub securely
- Private repo = access-controlled, not hidden from the host. Fine for T2/T3.
- For sensitive-on-git: encrypt before it touches the host (git-crypt / SOPS / age) so only ciphertext is stored. Manage the key per machine; AI can't read it without the key in-session (by design).
- Signed contracts (T5): dedicated encrypted vault, not git.
