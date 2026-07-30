# MDP/HDS Document Components — docx-js Implementation

This file contains reusable docx-js code for every component in the MDP/HDS design system. When building a document, import or inline these patterns. All values match the design system in SKILL.md.

---

## Setup and Constants

```javascript
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, PageBreak,
  HeadingLevel, Header, Footer, PageNumber, NumberFormat
} = require('docx');
const fs = require('fs');

// === COLOR CONSTANTS ===
const C = {
  PRIMARY:    "242424",  // Near Black — headings, emphasis, header block borders
  BODY:       "333333",  // Dark Gray — body copy
  SECONDARY:  "666666",  // Medium Gray — captions, chevrons, metadata
  SUBTLE:     "999999",  // Light Gray — footers
  ACCENT:     "024762",  // Teal — links, step numbers, CTAs (sparingly)
  BG_WARM:    "F5F4F0",  // Warm Off-White — callout backgrounds
  BORDER:     "CCCCCC",  // Silver — section borders, dividers
  WHITE:      "FFFFFF",  // Page background
};

// === TYPOGRAPHY CONSTANTS ===
const FONT = {
  SANS:  "Arial",
  MONO:  "Consolas",  // Fallback for JetBrains Mono in Word
};

// === BORDER HELPERS ===
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };
const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: C.BORDER };
const thinBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const heavyBorder = { style: BorderStyle.SINGLE, size: 12, color: C.PRIMARY }; // 6pt = 12 half-points
const heavyBorders = { top: heavyBorder, bottom: heavyBorder, left: heavyBorder, right: heavyBorder };

// === STANDARD CELL PADDING (for section cards) ===
const cardMargins = { top: 140, bottom: 140, left: 220, right: 220 };
```

---

## Header Block (Page 1)

The centered, heavy-bordered block at the top of page 1. Contains `< mdp >` mark, "Medical Design Program" subtitle, document title (tracked out), and descriptive subtitle.

```javascript
function headerBlock({ title, subtitle }) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: heavyBorders,
            margins: { top: 200, bottom: 200, left: 300, right: 300 },
            children: [
              // < mdp > mark
              new Paragraph({
                alignment: AlignmentType.CENTER,
                spacing: { after: 40 },
                children: [
                  new TextRun({ text: "< ", font: FONT.MONO, size: 28, color: C.SECONDARY }),
                  new TextRun({ text: "mdp", font: FONT.MONO, size: 28, bold: true, color: C.PRIMARY }),
                  new TextRun({ text: " >", font: FONT.MONO, size: 28, color: C.SECONDARY }),
                ],
              }),
              // "Medical Design Program"
              new Paragraph({
                alignment: AlignmentType.CENTER,
                spacing: { after: 120 },
                children: [
                  new TextRun({ text: "Medical Design Program", font: FONT.SANS, size: 22, color: C.SECONDARY }),
                ],
              }),
              // Document title — large, tracked out
              new Paragraph({
                alignment: AlignmentType.CENTER,
                spacing: { after: 80 },
                children: [
                  new TextRun({
                    text: title.toUpperCase(),
                    font: FONT.SANS,
                    size: 36,
                    bold: true,
                    color: C.PRIMARY,
                    characterSpacing: 60,
                  }),
                ],
              }),
              // Descriptive subtitle
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({ text: subtitle, font: FONT.SANS, size: 20, color: C.BODY }),
                ],
              }),
            ],
          }),
        ],
      }),
    ],
  });
}
```

---

## Running Header

Applied automatically to every page after page 1 via the docx section `headers.default`. The `< mdp >` mark sits left, the document title sits right, with a thin rule below achieved via a bottom-bordered table. Page 1 is suppressed with `differentFirstPage: true`.

```javascript
function runningHeader(shortTitle) {
  return new Header({
    children: [
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        borders: {
          top: noBorder, left: noBorder, right: noBorder,
          bottom: { style: BorderStyle.SINGLE, size: 1, color: C.BORDER },
          insideHorizontal: noBorder, insideVertical: noBorder,
        },
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders: noBorders,
                width: { size: 50, type: WidthType.PERCENTAGE },
                margins: { bottom: 60 },
                children: [
                  new Paragraph({
                    children: [
                      new TextRun({ text: "< ", font: FONT.MONO, size: 20, color: C.SECONDARY }),
                      new TextRun({ text: "mdp", font: FONT.MONO, size: 20, bold: true, color: C.PRIMARY }),
                      new TextRun({ text: " >", font: FONT.MONO, size: 20, color: C.SECONDARY }),
                    ],
                  }),
                ],
              }),
              new TableCell({
                borders: noBorders,
                width: { size: 50, type: WidthType.PERCENTAGE },
                margins: { bottom: 60 },
                children: [
                  new Paragraph({
                    alignment: AlignmentType.RIGHT,
                    children: [
                      new TextRun({ text: shortTitle, font: FONT.SANS, size: 17, color: C.SECONDARY }),
                    ],
                  }),
                ],
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

// Empty first-page header (suppresses running header on page 1)
function emptyFirstPageHeader() {
  return new Header({
    children: [new Paragraph({ children: [] })],
  });
}
```

---

## Running Footer

Applied to every page after page 1. Thin rule above, contact info left, page number right. First-page footer can show a fuller CTA or match the default.

```javascript
function runningFooter() {
  return new Footer({
    children: [
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        borders: {
          top: { style: BorderStyle.SINGLE, size: 1, color: C.BORDER },
          bottom: noBorder, left: noBorder, right: noBorder,
          insideHorizontal: noBorder, insideVertical: noBorder,
        },
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders: noBorders,
                width: { size: 75, type: WidthType.PERCENTAGE },
                margins: { top: 60 },
                children: [
                  new Paragraph({
                    children: [
                      new TextRun({
                        text: "Matthew Trowbridge, MD, MPH",
                        font: FONT.SANS, size: 15, bold: true, color: C.PRIMARY,
                      }),
                      new TextRun({
                        text: " • Director, UVA Medical Design Program",
                        font: FONT.SANS, size: 15, color: C.SECONDARY,
                      }),
                    ],
                  }),
                ],
              }),
              new TableCell({
                borders: noBorders,
                width: { size: 25, type: WidthType.PERCENTAGE },
                margins: { top: 60 },
                children: [
                  new Paragraph({
                    alignment: AlignmentType.RIGHT,
                    children: [
                      new TextRun({ text: "Page ", font: FONT.SANS, size: 15, color: C.SECONDARY }),
                      new TextRun({
                        children: [PageNumber.CURRENT],
                        font: FONT.SANS, size: 15, color: C.SECONDARY,
                      }),
                    ],
                  }),
                ],
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

// First-page footer — full CTA with website + email, no page number
function firstPageFooter() {
  return new Footer({
    children: [
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        borders: {
          top: { style: BorderStyle.SINGLE, size: 1, color: C.BORDER },
          bottom: noBorder, left: noBorder, right: noBorder,
          insideHorizontal: noBorder, insideVertical: noBorder,
        },
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders: noBorders,
                margins: { top: 60 },
                children: [
                  new Paragraph({
                    children: [
                      new TextRun({
                        text: "Matthew Trowbridge, MD, MPH",
                        font: FONT.SANS, size: 15, bold: true, color: C.PRIMARY,
                      }),
                      new TextRun({
                        text: " • Director, UVA Medical Design Program • Assoc. Prof., Emergency Medicine • ",
                        font: FONT.SANS, size: 15, color: C.SECONDARY,
                      }),
                      new TextRun({
                        text: "mtrowbridge@virginia.edu",
                        font: FONT.SANS, size: 15, color: C.ACCENT,
                      }),
                    ],
                  }),
                ],
              }),
            ],
          }),
        ],
      }),
    ],
  });
}
```

---

## Chevron Section Header

Returns a Paragraph with the chevron prefix in mono and the title in bold sans-serif.

```javascript
function chevronHeader(chevron, title) {
  // chevron is one of "<", ">", "<>"
  return new Paragraph({
    spacing: { after: 100 },
    children: [
      new TextRun({ text: chevron + " ", font: FONT.MONO, size: 26, color: C.SECONDARY }),
      new TextRun({ text: title, font: FONT.SANS, size: 26, bold: true, color: C.PRIMARY }),
    ],
  });
}
```

---

## Section Card

Wraps content (array of Paragraphs, Tables, etc.) in a bordered section card. Pass a chevron and title for the header, plus an array of children for the body.

```javascript
function sectionCard(chevron, title, bodyChildren) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: thinBorders,
            margins: cardMargins,
            children: [
              chevronHeader(chevron, title),
              ...bodyChildren,
            ],
          }),
        ],
      }),
    ],
  });
}
```

---

## Body Paragraph

Standard justified body text.

```javascript
function bodyParagraph(text, options = {}) {
  const { bold = false, italic = false, spacing = { after: 100 } } = options;
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing,
    children: [
      new TextRun({
        text,
        font: FONT.SANS,
        size: 21,  // 10.5pt — half-point units
        color: C.BODY,
        bold,
        italic,
      }),
    ],
  });
}

// For paragraphs with mixed formatting (bold key terms, etc.),
// build the children array manually:
function mixedParagraph(runs, options = {}) {
  const { spacing = { after: 100 } } = options;
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing,
    children: runs.map(r => new TextRun({
      font: r.font || FONT.SANS,
      size: r.size || 21,
      color: r.color || C.BODY,
      bold: r.bold || false,
      italic: r.italic || false,
      text: r.text,
    })),
  });
}
```

---

## Definition Table

Two-column borderless table. Array of `{ label, description }` objects.

```javascript
function definitionTable(items, labelWidth = 2400) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: items.map(item =>
      new TableRow({
        children: [
          new TableCell({
            borders: noBorders,
            width: { size: labelWidth, type: WidthType.DXA },
            margins: { top: 60, bottom: 60, left: 0, right: 120 },
            children: [
              new Paragraph({
                children: [
                  new TextRun({ text: item.label, font: FONT.SANS, size: 21, bold: true, color: C.PRIMARY }),
                ],
              }),
            ],
          }),
          new TableCell({
            borders: noBorders,
            margins: { top: 60, bottom: 60, left: 0, right: 0 },
            children: [
              new Paragraph({
                alignment: AlignmentType.JUSTIFIED,
                children: [
                  new TextRun({ text: item.description, font: FONT.SANS, size: 21, color: C.BODY }),
                ],
              }),
            ],
          }),
        ],
      })
    ),
  });
}
```

---

## Loop Step Table

Three-column borderless table with teal step numbers. Array of `{ number, name, description }`.

```javascript
function loopStepTable(steps) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: steps.map(step =>
      new TableRow({
        children: [
          // Step number (teal, mono)
          new TableCell({
            borders: noBorders,
            width: { size: 380, type: WidthType.DXA },
            margins: { top: 50, bottom: 50, left: 0, right: 40 },
            children: [
              new Paragraph({
                children: [
                  new TextRun({
                    text: String(step.number),
                    font: FONT.MONO,
                    size: 21,
                    bold: true,
                    color: step.number === 0 ? C.SECONDARY : C.ACCENT,
                  }),
                ],
              }),
            ],
          }),
          // Step name (bold)
          new TableCell({
            borders: noBorders,
            width: { size: 2160, type: WidthType.DXA },
            margins: { top: 50, bottom: 50, left: 0, right: 80 },
            children: [
              new Paragraph({
                children: [
                  new TextRun({ text: step.name, font: FONT.SANS, size: 21, bold: true, color: C.PRIMARY }),
                ],
              }),
            ],
          }),
          // Description
          new TableCell({
            borders: noBorders,
            margins: { top: 50, bottom: 50, left: 0, right: 0 },
            children: [
              new Paragraph({
                alignment: AlignmentType.JUSTIFIED,
                children: [
                  new TextRun({ text: step.description, font: FONT.SANS, size: 21, color: C.BODY }),
                ],
              }),
            ],
          }),
        ],
      })
    ),
  });
}
```

---

## Stat Box Row

Three metrics displayed side by side with vertical dividers. Array of `{ value, label }`.

```javascript
function statBoxRow(stats) {
  const cellWidth = Math.floor(10512 / stats.length);
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      new TableRow({
        children: stats.map((stat, i) => {
          const isLast = i === stats.length - 1;
          return new TableCell({
            borders: {
              top: noBorder,
              bottom: noBorder,
              left: noBorder,
              right: isLast ? noBorder : thinBorder,
            },
            width: { size: cellWidth, type: WidthType.DXA },
            margins: { top: 80, bottom: 80, left: 60, right: 60 },
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                spacing: { after: 40 },
                children: [
                  new TextRun({ text: stat.value, font: FONT.MONO, size: 36, bold: true, color: C.PRIMARY }),
                ],
              }),
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({ text: stat.label, font: FONT.SANS, size: 16, color: C.SECONDARY }),
                ],
              }),
            ],
          });
        }),
      }),
    ],
  });
}
```

---

## Old → New Comparison

Two contrasting cells with warm background, connected by an arrow.

```javascript
function oldNewComparison(oldText, newText) {
  const warmShading = { fill: C.BG_WARM, type: ShadingType.CLEAR };
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      new TableRow({
        children: [
          // Old era cell
          new TableCell({
            borders: thinBorders,
            shading: warmShading,
            width: { size: 45, type: WidthType.PERCENTAGE },
            margins: { top: 120, bottom: 120, left: 200, right: 200 },
            children: [
              new Paragraph({
                spacing: { after: 40 },
                children: [
                  new TextRun({ text: "In the ", font: FONT.MONO, size: 18, color: C.SECONDARY }),
                  new TextRun({ text: "OLD ERA", font: FONT.MONO, size: 18, bold: true, color: C.SECONDARY }),
                ],
              }),
              new Paragraph({
                children: [
                  new TextRun({ text: oldText, font: FONT.SANS, size: 22, bold: true, color: C.PRIMARY }),
                ],
              }),
            ],
          }),
          // Arrow cell
          new TableCell({
            borders: noBorders,
            width: { size: 10, type: WidthType.PERCENTAGE },
            verticalAlign: "center",
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({ text: "→", font: FONT.SANS, size: 28, color: C.SECONDARY }),
                ],
              }),
            ],
          }),
          // New era cell
          new TableCell({
            borders: thinBorders,
            shading: warmShading,
            width: { size: 45, type: WidthType.PERCENTAGE },
            margins: { top: 120, bottom: 120, left: 200, right: 200 },
            children: [
              new Paragraph({
                spacing: { after: 40 },
                children: [
                  new TextRun({ text: "In the ", font: FONT.MONO, size: 18, color: C.SECONDARY }),
                  new TextRun({ text: "NEW ERA", font: FONT.MONO, size: 18, bold: true, color: C.SECONDARY }),
                ],
              }),
              new Paragraph({
                children: [
                  new TextRun({ text: newText, font: FONT.SANS, size: 22, bold: true, color: C.PRIMARY }),
                ],
              }),
            ],
          }),
        ],
      }),
    ],
  });
}
```

---

## Quote Block

Italic quote with em-dash attribution. Used inside section cards.

```javascript
function quoteBlock(quote, attribution) {
  return [
    new Paragraph({
      spacing: { before: 80, after: 40 },
      indent: { left: 120 },
      children: [
        new TextRun({ text: `"${quote}"`, font: FONT.SANS, size: 20, italic: true, color: C.PRIMARY }),
      ],
    }),
    new Paragraph({
      spacing: { after: 100 },
      indent: { left: 120 },
      children: [
        new TextRun({ text: `— ${attribution}`, font: FONT.SANS, size: 17, color: C.SECONDARY }),
      ],
    }),
  ];
}
```

---

## CTA Line

```javascript
function ctaLine(text, url) {
  return new Paragraph({
    spacing: { before: 100, after: 60 },
    children: [
      new TextRun({ text: text + " ", font: FONT.SANS, size: 20, color: C.BODY }),
      new TextRun({ text: url, font: FONT.SANS, size: 20, bold: true, color: C.ACCENT }),
    ],
  });
}
```

---

## In-Body Footer (two-pager legacy)

For the Executive Brief two-pager, this inline footer is placed at the bottom of each page's body content. For longer documents (3+ pages), omit this and rely on the running footer instead.

```javascript
function inBodyFooter(options = {}) {
  const { fullTitle = false } = options;
  const titleText = fullTitle
    ? "Director, UVA Medical Design Program • Associate Professor, Emergency Medicine"
    : "Director, UVA Medical Design Program • Assoc. Prof., Emergency Medicine";
  return new Paragraph({
    spacing: { before: 60 },
    children: [
      new TextRun({ text: "Matthew Trowbridge, MD, MPH", font: FONT.SANS, size: 17, bold: true, color: C.PRIMARY }),
      new TextRun({ text: ` • ${titleText} • `, font: FONT.SANS, size: 17, color: C.SECONDARY }),
      new TextRun({ text: "mtrowbridge@virginia.edu", font: FONT.SANS, size: 17, color: C.ACCENT }),
    ],
  });
}
```

---

## Spacer Paragraph

Use between components for breathing room.

```javascript
function spacer(points = 80) {
  return new Paragraph({ spacing: { after: points }, children: [] });
}
```

---

## Full Document Skeleton

Assembles a complete document with running headers and footers. Works for any length — two pages or twenty.

```javascript
function createDocument(bodyChildren, shortTitle) {
  return new Document({
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: {
            top: 760,
            bottom: 580,
            left: 864,
            right: 864,
            header: 360,  // Space above header content
            footer: 360,  // Space below footer content
          },
        },
        // Enable different first page for header/footer
        titlePage: true,
      },
      headers: {
        default: runningHeader(shortTitle),
        first: emptyFirstPageHeader(),
      },
      footers: {
        default: runningFooter(),
        first: firstPageFooter(),
      },
      children: bodyChildren,
    }],
  });
}

// For two-pager: pass all content including manual page break
// For longer docs: just pass the full array of body children —
// Word handles page breaks automatically, and the running
// header/footer appears on every page after page 1.

// Generate and save
async function generateDocument(doc, filename) {
  const buffer = await Packer.toBuffer(doc);
  const outputPath = `/mnt/user-data/outputs/${filename}`;
  fs.writeFileSync(outputPath, buffer);
  return outputPath;
}
```

### Two-pager vs. longer documents

For the **Executive Brief (two-pager)**: pass all content as a flat array with a manual `new Paragraph({ children: [new PageBreak()] })` between pages. The running footer on page 1 shows the full CTA; page 2 shows contact + page number. The in-body footer (`inBodyFooter()`) can also be used at the bottom of each page's content for belt-and-suspenders contact visibility.

For **longer documents (3+ pages)**: just pass the body children array. Don't use in-body footers — the running footer handles contact + page number on every page. The running header (`< mdp >` + title + rule) appears automatically on pages 2+. Content flows naturally with Word's automatic page breaks, or insert manual breaks at section boundaries.

---

## Usage Pattern

When building an MDP/HDS document:

```javascript
const page1 = [
  headerBlock({ title: "Health Design Sprint", subtitle: "A Repeatable Methodology for..." }),
  spacer(),
  bodyParagraph("Opening thesis..."),
  bodyParagraph("Context paragraph..."),
  spacer(40),
  sectionCard("<", "The Three Tools", [
    definitionTable([
      { label: "Domain Expertise", description: "Your clinical knowledge..." },
      { label: "Design Thinking", description: "Structured methods..." },
      { label: "AI as Builder", description: "Vibe coding..." },
    ]),
  ]),
  spacer(40),
  bodyParagraph("Bridge paragraph about PRD..."),
  spacer(40),
  sectionCard(">", "The Signal-to-Prototype Loop", [
    // ... loop steps, explanatory paragraphs
  ]),
  spacer(40),
  ctaLine("See what students built at:", "healthdesignsprint.com"),
  documentFooter(),
];

const page2 = [
  continuityHeader("Health Design Sprint"),
  spacer(60),
  oldNewComparison("The hard part was building the app.", "The hard part is knowing what to build."),
  spacer(60),
  sectionCard(">", "Evidence: February 2026 Pilot", [
    bodyParagraph("Eight fourth-year medical students...", { bold: true }),
    bodyParagraph("Description of flagship project..."),
    statBoxRow([
      { value: "4.8 / 5", label: "Career relevance" },
      { value: "~3×", label: "Skill confidence gain" },
      { value: "5 / 6", label: "Would strongly recommend" },
    ]),
    ...quoteBlock("Quote text...", "M4, Internal Medicine"),
  ]),
  // ... remaining sections
];

const doc = createDocument(page1, page2);
generateDocument(doc, "hds-executive-brief.docx");
```
