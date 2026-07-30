---
name: mdp-hds-brand
description: UVA Medical Design Program and Health Design Sprint brand system for generating professional documents. Use when creating executive briefs, workshop plans, course materials, handouts, syllabi, or any document for the Medical Design Program (MDP), Health Design Sprint (HDS), or MDP-affiliated academic materials. Triggers on requests mentioning MDP, Medical Design Program, Health Design Sprint, HDS, design sprint documents, MDP branding, the mdp chevron mark, or chevron section headers. Also use when Matt asks to create materials for meetings with deans, administrators, or external partners about MDP or HDS. Do NOT use for Health Intent Partners (HIP) consulting materials — use the hip-brand skill instead.
---

# MDP / HDS Document Design System

## Brand Architecture — When To Use What

| Entity | What It Is | When To Use |
|--------|-----------|-------------|
| **Medical Design Program (MDP)** | The UVA academic program (10 years, 200+ students) | Academic context, UVA-affiliated materials, course sites |
| **Health Design Sprint (HDS)** | The methodology (the repeatable system) | Methodology descriptions, executive briefs, workshop materials |
| **Health Intent Partners (HIP)** | Matt's LLC for commercial engagement | **NOT this skill** — use `/mnt/skills/user/hip-brand/SKILL.md` |

MDP and HDS materials use the `< mdp >` mark and position Matt as "Director, UVA Medical Design Program." HIP materials use the HIP logo. The two should never appear on the same document.

---

## Design Philosophy

MDP/HDS materials communicate **clinical creativity meets rigor**. The audience ranges from medical school deans to Microsoft executives to NIH program officers. The design is structured and evidence-forward, but warmer than pure corporate — it's an academic program with a soul.

**Core principles:**
- Card-based layout with bordered sections — structured but not rigid
- Chevron vocabulary (`<`, `>`, `<>`) borrowed from the website's code-meets-care identity
- Narrative-first, then evidence — lead with the thesis, prove it with data
- Mono + sans-serif typographic contrast signals "tech-aware academia"
- Restrained palette — grayscale with teal used sparingly for accent

---

## Color Palette

| Role | Hex | Name | Usage |
|------|-----|------|-------|
| **Primary** | `#242424` | Near Black | Headings, logo mark, emphasis, header block borders |
| **Body** | `#333333` | Dark Gray | Body copy |
| **Secondary** | `#666666` | Medium Gray | Captions, metadata, chevron symbols, dates |
| **Subtle** | `#999999` | Light Gray | Footers, de-emphasized text |
| **Accent** | `#024762` | Teal | Links, loop step numbers, CTAs — used sparingly |
| **Background** | `#F5F4F0` | Warm Off-White | Callout boxes, comparison cells, highlighted sections |
| **Rules/Borders** | `#CCCCCC` | Silver | Section borders, divider lines, stat box separators |
| **Surface** | `#FFFFFF` | White | Page background, card interiors |

**Not used:** UVA Navy `#232D4B`, UVA Orange `#E57200` — reserve for institutional co-branding only.

---

## Typography

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Brand mark `< mdp >` | Consolas | 26-28pt | Bold "mdp", Regular chevrons | Primary / Secondary |
| Document title | Arial | 34-36pt | Bold | Primary |
| Subtitle | Arial | 19-22pt | Regular | Body or Secondary |
| Section headers | Arial + Consolas | 24-28pt | Bold title, Regular chevron | Primary + Secondary |
| Body | Arial | 20-22pt (half-points) | Regular | Body |
| Bold emphasis | Arial | same as body | Bold | Primary |
| Italic emphasis | Arial | same as body | Italic | Primary |
| Table labels | Arial | 20-22pt | Bold | Primary |
| Table descriptions | Arial | 20-22pt | Regular | Body |
| Loop step numbers | Consolas | 21pt | Bold | Accent (teal) |
| Captions/metadata | Arial | 15-17pt | Regular | Secondary |
| Stat numbers | Consolas | 34-38pt | Bold | Primary |
| Stat labels | Arial | 15-17pt | Regular | Secondary |
| Student quotes | Arial | 20pt | Italic | Primary |
| Quote attribution | Arial | 17pt | Regular | Secondary |

Body text uses justified alignment throughout. Consolas is the system-font fallback for JetBrains Mono in Word.

---

## Page Layout (US Letter)

| Property | Value | DXA |
|----------|-------|-----|
| Paper | US Letter | 12240 × 15840 |
| Top margin | 0.53" | 760 |
| Bottom margin | 0.40" | 580 |
| Left margin | 0.60" | 864 |
| Right margin | 0.60" | 864 |
| Content width | 7.3" | 10512 |

The narrower margins maximize content area — these are dense, information-rich documents designed for print handoff at meetings.

---

## Component Library

These are the reusable patterns that give MDP/HDS documents their identity. Every document is assembled from these components. For docx-js implementation code, read `references/components.md`.

### Header Block
Centered, heavy-bordered (`#242424`, 6pt) card. Contains:
1. `< mdp >` mark — chevrons in Consolas Regular (Secondary), "mdp" in Consolas Bold (Primary)
2. "Medical Design Program" subtitle — Arial Regular, Secondary
3. Document title — Arial Bold, large, letter-spaced (tracking 60)
4. Descriptive subtitle — Arial Regular

Used once, top of page 1 only.

### Section Card
Full-width table cell with thin `#CCCCCC` 1pt border. Internal padding: 120-160 DXA vertical, 200-240 DXA horizontal. Contains a chevron section header followed by body content (paragraphs, tables, or both). This is the primary content container — almost everything lives inside a section card.

### Chevron Section Header
Pattern: `[chevron] [Title]` where chevron is in Consolas, Secondary color; title is Arial Bold, Primary color.

The chevron vocabulary:
- `<` = foundational / input-focused sections (e.g., "The Three Tools")
- `>` = output / evidence-focused sections (e.g., "Evidence", "The Loop")
- `<>` = synthesis / bidirectional sections (e.g., "Adoption Gap", "Opportunities")

Choose the chevron based on the section's conceptual role, not arbitrarily.

### Definition Table
Two-column borderless table inside a section card. Left column: bold label (2200-2600 DXA). Right column: justified description (remainder). No internal borders. Row margins: 50-80 DXA vertical. Used for key concept definitions (e.g., "The Three Tools").

### Loop Step Table
Three-column borderless table. Column 1: step number in Consolas/teal (380 DXA). Column 2: bold step name (2160 DXA). Column 3: justified description (remainder). Step 0 uses Secondary color instead of Accent.

### Stat Box Row
Three equal-width cells with vertical `#CCCCCC` dividers between them (no outer borders). Large Consolas number centered above small Arial label. Last cell has no right border. Used for quantitative evidence.

### Old → New Comparison
Three-cell row: left cell (warm `#F5F4F0` background, thin border), arrow cell (no borders), right cell (warm background, thin border). Consolas label ("In the OLD ERA" / "In the NEW ERA") above bold contrast statement.

### Quote Block
Italic body text with em-dash attribution line below in Secondary. Inside section cards, not standalone. Format: *"Quote text."* — Role, Specialty

### CTA Line
Sentence text + bold teal link. No rule above. Followed by single-line contact info.

### Running Header (multi-page documents)
Applied automatically to every page after page 1 via the docx section header. Two elements on a single line with a thin `#CCCCCC` rule below:
- **Left:** `< mdp >` mark — Consolas, same styling as the brand mark (chevrons Secondary, "mdp" Primary), 20pt
- **Right:** Document short title — Arial Regular, 17pt, Secondary color

On page 1, the header is suppressed (set `differentFirstPage: true` on the section) so the Header Block in the body isn't competing with a running header above it.

For two-page documents (the Executive Brief), this running header replaces the old "continuity header" table that was manually placed in the body — it's now automatic and consistent.

### Running Footer (multi-page documents)
Applied to every page. Thin `#CCCCCC` 0.5pt rule above, then a single line:
- **Left:** Contact — "Matthew Trowbridge, MD, MPH" (bold, Primary, 15pt) + title (Secondary, 15pt)
- **Right:** Page number — "Page X" in Arial Regular, 15pt, Secondary

On page 1 (when `differentFirstPage` is true), the footer can either be the same running footer or a custom first-page footer with the full CTA line (website + email) instead of the abbreviated contact + page number.

### In-Body Footer (legacy / two-pager)
For the two-page Executive Brief, the contact footer is still placed inline at the bottom of each page's content as well: **Name** (bold, Primary) + bullet-separated title/role (small, Secondary) + email/URL (small, Accent teal). This provides a complete contact line visible even when printed single-sided. For longer documents (3+ pages), omit the in-body footer and rely on the running footer instead.

---

## Document Templates

### Executive Brief (The Two-Pager)
The flagship format — designed for meeting handoff to deans, executives, potential partners. Two pages, front and back of a single sheet.

**Page 1 structure: What It Is**
1. Header Block (full, centered, heavy border)
2. Thesis paragraphs (2-3 paragraphs, justified, establishing the "why")
3. Context paragraph (MDP history → HDS as distilled methodology)
4. Section Card: foundational concepts (`<` chevron) — definition table format
5. Bridge paragraph (the central artifact or connecting idea)
6. Section Card: the process/system (`>` chevron) — loop step table + explanatory paragraphs
7. CTA line + contact footer

**Page 2 structure: Evidence + Opportunity**
1. Continuity header (`< mdp >` + title + rule)
2. Old → New Comparison (framing shift)
3. Section Card: evidence (`>` chevron) — bold proof statement, description, stat boxes, student quotes
4. Section Card: strategic framing (`<>` chevron) — the problem/gap this addresses
5. Section Card: opportunities (`<>` chevron) — definition table of 3-5 opportunity areas
6. Footer

### Workshop Session Plan
For facilitator use during HDS sessions or external workshops. Uses the same components but with a more operational structure.

**Structure:**
1. Header Block (simplified — title + date + location)
2. Section Card: session goals and audience
3. Section Card: agenda/timeline — loop step table format with times
4. Section Card: materials and preparation
5. Section Card: facilitation notes
6. Footer

### Course Materials (Syllabi, Handouts)
For student-facing materials. Same visual system, slightly lighter touch.

**Structure:**
1. Header Block with course title and term
2. Section cards for each major content area
3. Definition tables for key concepts
4. CTA with course website link
5. Footer with instructor contact

---

## Tone and Voice

MDP/HDS documents are **peer-to-peer and exploratory, not a pitch deck**. The voice is:
- Confident but not salesy — "this is what we built and what it showed us"
- Evidence-forward — claims are backed by specific numbers and student outcomes
- Thesis-driven — every document opens with a clear framing of why this matters now
- Technically literate — comfortable naming specific tools (Claude Code, Codex, Lovable, Next.js, Supabase) without over-explaining
- Respectful of the reader's intelligence — senior leaders who think about these problems daily

Key phrases and framings that recur across HDS materials:
- "The bottleneck has shifted" — from engineering capacity to domain expertise
- "The Three Tools" — domain expertise, design thinking, AI as builder
- "Signal-to-Prototype Loop" — the core HDS methodology
- "PRD as the central artifact" — Product Requirements Document bridges vision and implementation
- "Layered design lenses" — the core innovation of progressive deepening
- "Adoption gap" / "last-mile problem" — the strategic framing for why HDS matters beyond UVA

---

## Contact Information

| Field | Value |
|-------|-------|
| Name | Matthew Trowbridge, MD, MPH |
| Title (MDP) | Director, UVA Medical Design Program |
| Academic title | Associate Professor, Emergency Medicine |
| Email | mtrowbridge@virginia.edu |
| Website | healthdesignsprint.com |

---

## Implementation

When generating documents with this skill:

1. **Always read the docx skill first** — read `/mnt/skills/public/docx/SKILL.md` for the base document creation workflow (docx-js setup, npm install, file generation patterns)
2. **Then read the component implementations** — read `references/components.md` in this skill directory for docx-js code for every component (header block, section cards, chevron headers, definition tables, stat boxes, quote blocks, etc.)
3. **Assemble the document** from the template structure above, using the component functions
4. **Always output to `/mnt/user-data/outputs/`** and present the file

The components in `references/components.md` are designed as reusable functions. Build the document by composing them — don't re-implement from scratch each time.

---

## File References

| Resource | Location |
|----------|----------|
| HDS Website | https://uva-medical-design.github.io/health-design-sprint/ |
| HDS Methodology | https://uva-medical-design.github.io/health-design-sprint/methodology |
| HDS Showcase | https://uva-medical-design.github.io/health-design-sprint/showcase |
| MDP Brand Repo | `uva-medical-design/mdp-brand` on GitHub |
| Course Repo | `uva-medical-design/health-design-sprint` on `v2-course-overhaul` |
| HIP Brand Skill | `/mnt/skills/user/hip-brand/SKILL.md` — for HIP materials only |
