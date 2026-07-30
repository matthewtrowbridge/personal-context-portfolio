---
name: matt-email-voice
description: Matt's universal email defaults — the base register that every domain-specific voice skill layers on top of. Use when drafting any email, message, or short correspondence from Matt, in any context, unless a domain skill fully covers it. Domain skills (uva-em-voice, red-cell-style, hip-brand, mdp-hds-brand) override specific rules but assume these defaults underneath.
---

# Matt's email voice — base layer

> **Status: partial reconstruction.** The original `feedback_matt_email_voice.md` lives in
> claude.ai auto-memory and was not recoverable from disk. What follows is reconstructed from the
> four defaults `uva-em-voice` explicitly names, plus conventions observable in the existing skill
> set. **This needs a pass from Matt before it should be trusted for unedited sends.**
>
> Until then: draft with these defaults, then run a voice check against real samples in
> `voice/samples/`, and expect to correct.

## The four documented defaults

These are named directly in `uva-em-voice` as Matt's universal email behaviour.

1. **Warm opening.** Messages open with genuine acknowledgement of the person, not a cold jump to
   the ask. Warmth is brief — a sentence, not a paragraph.

2. **Perspective markers.** Positions are marked as his own rather than asserted as fact. "My read
   is…", "I may be wrong here, but…", "From where I sit…". This is a deliberate register, not
   hedging: it preserves the reader's ability to disagree without friction.

3. **Autonomy-preserving closes.** The ending leaves the recipient a real choice. "Happy either
   way", "No pressure on timing", "Tell me if you'd rather go another direction." Matt does not
   close by applying pressure.

4. **Transparent AI use.** When AI substantially shaped a document, that is disclosed rather than
   concealed. This is a standing commitment; do not quietly drop it to make a message read more
   smoothly.

## Consistent across all domains

Observable in every existing voice skill, so treat as global:

- **No emoji.** Nowhere, in any register.
- **No casual group address** — not "gang", not "folks". Use "team", "colleagues", "everyone", or
  omit the address entirely.
- **Complete sentences.** No text-speak.
- **Bold sparingly**, only where it genuinely helps a reader scan — a deadline, a decision point, a
  named ask. If it does not aid scanning, do not bold.
- **Never strident.** No ultimatums, no pressure, no manufactured urgency — even when pushing for
  a decision. The ask is framed as a request.
- **Minimal formatting** in correspondence. Let the prose carry it.

## Layering

This is the base. Domain skills override specific rules and add their own:

- `uva-em-voice` — adds the "forwardable" standard and calibrated deference by seniority
- `red-cell-style` — quantified problems, mission framing, no academic hedging
- `hip-brand` / `mdp-hds-brand` — document and brand standards for those audiences

Where a domain skill conflicts with this file, **the domain skill wins**.

## To finish this skill

Matt should supply: greeting and sign-off patterns by relationship type; how he opens a cold email
versus a reply; length preferences by context; specific phrases he uses and specific phrases he
would never use. Then seed `voice/samples/` with ten to fifteen real sent emails across domains, so
voice checks have ground truth rather than a description of ground truth.
