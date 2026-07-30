---
name: uva-irb-navigator
description: Navigate UVA IRB-HSR submission forms by intelligently determining which appendices and sections are required based on study characteristics. Use when a researcher needs help completing IRB Exempt Applications, Data Security Plans, or other UVA IRB-HSR forms. Triggers on requests involving IRB submissions, exempt reviews, human subjects research applications, HIPAA compliance forms, or UVA research protocol submissions. Generates completed Word documents plus detailed decision rationale explaining all form navigation choices.
---

# UVA IRB Navigator

## Overview

This skill helps researchers navigate UVA IRB-HSR submission forms by:
1. Collecting study characteristics through structured questions
2. Determining which form sections/appendices are required
3. Generating completed Word documents
4. Producing a decision rationale document explaining all choices

## Workflow

### Phase 1: Study Intake

Collect study information using structured questions. See [references/intake-questions.md](references/intake-questions.md) for the complete question set organized by topic.

**Core questions to ask upfront:**
1. Study title and brief description
2. Primary data source (new collection vs. secondary analysis)
3. HIPAA identifiers involved (any of the 18 HIPAA identifiers?)
4. Funding source (federal, foundation, departmental, unfunded)
5. External collaborators or data sharing outside UVA

### Phase 2: Determine Required Components

Based on intake answers, determine which appendices are required using the decision trees in [references/exempt-decision-tree.md](references/exempt-decision-tree.md).

**Key decision points for Exempt Applications:**

| Condition | Required Appendix |
|-----------|-------------------|
| Federally funded OR outside support | Appendix J |
| Receiving data/specimens from outside UVA | Appendix A |
| Sending data/specimens outside UVA | Appendix B |
| Study involves HIPAA identifiers | Appendix C (Privacy Plan) + Appendix D (HIPAA) |
| Need waiver of HIPAA authorization | Appendix E |
| Active recruitment of subjects | Appendix F |
| Compensation/reimbursement provided | Appendix G |
| Data Use Agreement required | Appendix H |
| Recording/photography of subjects | Appendix I |

### Phase 3: Generate Documents

Generate two outputs:

**1. Completed IRB Application (.docx)**
Use the docx skill to create a Word document. Follow the template structure in [references/exempt-template.md](references/exempt-template.md).

**2. Decision Rationale (.md)**
Generate a markdown document explaining:
- Which appendices were included and why
- Which appendices were skipped and why  
- How each form field was populated
- Any assumptions made

### Phase 4: Review and Refine

Present outputs to researcher for review. Common refinements:
- Adjusting narrative descriptions
- Adding investigator experience details
- Clarifying data handling procedures

## Critical Form Logic

### Exempt Eligibility Disqualifiers

A study CANNOT be exempt if ANY of these apply:
- Surveys/interviews with minors
- Observation of minors with investigator participation
- Procedures causing discomfort beyond daily life
- Deception without prospective agreement
- Research involving rare traits that could cause harm if disclosed
- FDA-regulated research
- Targeted enrollment of prisoners
- FERPA-governed data without consent
- Embryos, fetal tissue, stem cells
- New specimen collection specifically for research

### Data Security Plan Logic

The Data Security Plan has its own decision tree. Key branching:

```
HIPAA identifiers collected? 
├── NO → Mark as "Sensitive Data", no further questions needed
└── YES → Continue to collection method questions
    ├── Onto individual device? → Complete Appendix 1B(1)
    ├── Via web/cloud? → Complete Appendix 1B(2)  
    ├── To non-approved server? → Complete Appendix 1B(3)
    └── To approved UVA server? → Complete Appendix 1B(4), list server
```

## Document Generation

When generating the Exempt Application document:

1. **Header section**: PI name, contact, funding status, biospecimen use
2. **Investigator Experience**: Brief paragraph on team qualifications
3. **Brief Summary**: Purpose, methods, data sources, identifiers, external sharing
4. **Investigator Agreement**: Checkbox confirmation (always checked)
5. **Screening questions**: Series of YES/NO based on study characteristics
6. **Required appendices only**: Include ONLY appendices determined in Phase 2

For document creation mechanics, invoke the docx skill.

## Example Study Types

**Secondary data analysis (like the NEMSIS study):**
- Typically requires: Appendix A (receiving external data), possibly Appendix J (if funded)
- Usually skips: Appendix B, F, G, I (no sending, recruitment, compensation, recording)
- HIPAA status depends on whether limited dataset or fully de-identified

**Survey research:**
- Typically requires: Appendix C, F (privacy plan, recruitment)
- If online: Data Security Plan 1B(2) for web-based collection
- If compensated: Appendix G

**Chart review:**
- Typically requires: Appendix C, D (privacy, HIPAA)
- Usually needs waiver of authorization: Appendix E
- Consider: Is data leaving UVA? → Appendix B
