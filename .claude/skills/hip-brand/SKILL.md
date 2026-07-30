---
name: hip-brand
description: Health Intent Partners brand assets and logo usage guidelines. Use when creating documents, presentations, or materials for Health Intent Partners (HIP), Matt Trowbridge, or any HIP client engagement. Triggers on requests involving HIP logos, Health Intent Partners branding, or document templates for HIP deliverables.
---

# Health Intent Partners Design System

## Design Philosophy

HIP materials communicate **authority through restraint**. The audience—executives, investors, former government officials—responds to clarity, precision, and substance. Every design element earns its place by supporting comprehension.

**Core principles:**
- Confidence through simplicity
- Typography carries the message
- Strategic white space
- Quantified claims before narrative (lead with metrics)

---

## Logo Files

All logos: 600dpi PNGs with transparent backgrounds in `assets/`.

**Primary (use by default):** `HIP_logo_black.png` (838×481px, 1.74:1 ratio)
**Reversed:** `HIP_logo_white.png` (for dark backgrounds)
**Icons:** `HIP_icon_black.png`, `HIP_icon_white.png` (348×480px, 0.725:1 ratio)

| Context | File | Size |
|---------|------|------|
| Cover page | HIP_logo_black.png | 180×103px |
| Document header | HIP_logo_black.png | 100×57px |
| Small placement | HIP_icon_black.png | 40×55px |

**Critical:** Always maintain aspect ratios. Logo minimum width: 80px.

---

## Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| **Primary** | #000000 | Headings, logo, emphasis |
| **Body text** | #333333 | Body copy |
| **Secondary** | #666666 | Captions, labels, metadata |
| **Subtle** | #999999 | Footer text |
| **Accent** | #024762 | Sparingly—links, key metrics, charts |
| **Background** | #F8F8F8 | Callout boxes only |
| **Rules** | #CCCCCC | Horizontal rules, table borders |

Default to grayscale. Use teal (#024762) only when color adds meaning.

---

## Typography

**Font:** Arial (Helvetica Neue if available)

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Document title | 28-32pt | Bold | Black |
| H1 Section | 18pt | Bold | Black |
| H2 Subsection | 14pt | Bold | Black |
| Body | 11pt | Regular | #333333 |
| Caption | 9pt | Regular | #666666 |
| Footer | 8pt | Regular | #999999 |

**Line height:** 1.4 for body text

---

## Page Layout (US Letter)

| Element | Measurement | DXA |
|---------|-------------|-----|
| Top/Bottom margin | 1.0" | 1440 |
| Left margin | 1.25" | 1800 |
| Right margin | 1.0" | 1440 |

Wider left margin creates visual balance and accommodates binding.

---

## Headers and Footers

**Header (interior pages):**
```
[HIP icon 28×38px]                    [Document title, 9pt #666666]
```
- Icon-only on interior pages (not full lockup)
- Full logo reserved for title page
- Increase top margin to 1.25" for adequate header padding

**Footer (all pages):**
```
───────────────────────────────────────────────────────────────
CONFIDENTIAL              [Client name]              Page X
```
- 0.5pt rule above (#CCCCCC)
- 8pt text, #999999

---

## Logo Usage

| Context | File | Size |
|---------|------|------|
| Title page | HIP_logo_black.png | 180×103px |
| Interior header | HIP_icon_black.png | 28×38px |
| Dark backgrounds | HIP_logo_white.png / HIP_icon_white.png | As needed |

**Rule:** Full logo on title/cover pages only. Icon mark for interior page headers.

---

## Company Information

**Legal name:** Health Intent Partners LLC
**Principal:** Matthew Trowbridge, MD, MPH
**Email:** matthew.trowbridge@healthintent.partners

---

## Graphic Elements

**Section divider:** 1pt black rule below document title
**Subsection divider:** 0.5pt #CCCCCC (optional)
**Footer rule:** 0.5pt #CCCCCC

**Callout boxes** (for key metrics):
- Background: #F8F8F8
- Border: None or 0.5pt #CCCCCC
- Padding: 12pt
- Metric: 24-28pt bold black
- Label: 10pt #666666

**Tables:**
- Border: 0.5pt #CCCCCC
- Header: #F0F0F0 background, bold
- Padding: 8pt vertical, 12pt horizontal

---

## Document Templates

### Executive Brief
1. Document type label: "EXECUTIVE BRIEF" (10pt, #666666, letter-spaced)
2. Title (28pt bold)
3. Horizontal rule (1pt black)
4. Key metrics boxes (2-3 metrics)
5. Executive summary
6. Sections with H1/H2 hierarchy

### Proposal Cover
1. Logo top-left (180×103px)
2. "ENGAGEMENT PROPOSAL" label
3. Title (32pt bold, 2-3 lines)
4. Horizontal rule
5. "Prepared for [Client]"
6. Date

### White Paper Cover
1. "WHITE PAPER" centered (10pt, letter-spaced)
2. Title centered (28pt bold)
3. Subtitle (16pt)
4. Author and affiliation
5. Logo centered near bottom
6. Date

---

## The HIP "Fingerprint"

Documents are recognizably HIP when they exhibit:
1. Clean asymmetric margins (wider left)
2. Confident white space
3. Typography-driven hierarchy
4. Quantified opening (metrics before narrative)
5. Restrained grayscale palette
6. Consistent logo placement
7. Professional footer with thin rule

---

## Implementation (docx-js)

```javascript
// Full logo for title page (180×103px, maintains 1.74:1 ratio)
new ImageRun({
    type: "png",
    data: fs.readFileSync('assets/HIP_logo_black.png'),
    transformation: { width: 180, height: 103 },
    altText: { title: "Health Intent Partners", description: "Logo", name: "HIP" }
})

// Icon for interior page headers (28×38px, maintains 0.725:1 ratio)
new ImageRun({
    type: "png",
    data: fs.readFileSync('assets/HIP_icon_black.png'),
    transformation: { width: 28, height: 38 },
    altText: { title: "Health Intent Partners", description: "Icon", name: "HIP" }
})

// Key metric callout box
new TableCell({
    shading: { fill: "F8F8F8", type: ShadingType.CLEAR },
    margins: { top: 180, bottom: 180, left: 240, right: 240 },
    borders: { /* all BorderStyle.NONE */ },
    children: [
        new Paragraph({ children: [
            new TextRun({ text: "$116B+", size: 52, bold: true, color: "000000" })
        ]}),
        new Paragraph({ children: [
            new TextRun({ text: "Description text", size: 20, color: "666666" })
        ]})
    ]
})
```
