# Decision Rationale Document Template

## Purpose

This document accompanies every generated IRB application to provide full transparency on how form navigation decisions were made. It serves as:
1. Documentation for the researcher to understand the logic
2. Audit trail for future modifications
3. Educational resource for understanding IRB requirements

---

## Template Structure

# IRB Application Decision Rationale
## [Study Title]
Generated: [Date]

---

## Study Classification

**Determination:** [Exempt / Expedited / Full Board]

**Rationale:** [Explain why this classification was selected based on study characteristics]

**Key factors:**
- [Factor 1]
- [Factor 2]
- [Factor 3]

---

## Appendix Decisions

### Appendices INCLUDED

#### Appendix [Letter]: [Title]

**Included because:** [Specific reason based on study characteristics]

**Triggering factor:** [The specific answer or characteristic that triggered this]

**How completed:** [Brief description of what was entered and why]

---

#### [Repeat for each included appendix]

---

### Appendices EXCLUDED

#### Appendix [Letter]: [Title]

**Excluded because:** [Specific reason]

**Verification:** [The question/answer that confirmed exclusion]

---

#### [Repeat for each excluded appendix]

---

## Key Form Field Decisions

### Investigator Experience

**Content source:** [How this was populated—user input, inferred from credentials, etc.]

**Key elements included:**
- [Element 1 and why]
- [Element 2 and why]

---

### Brief Summary

**Purpose statement:** [How derived]

**Methods description:** [How derived]

**Data elements listed:** [Source of this information]

**Identifiers determination:** [How identifier status was determined]

---

### Screening Questions

| Question | Answer | Rationale |
|----------|--------|-----------|
| [Question text] | YES/NO | [Why this answer] |
| [Question text] | YES/NO | [Why this answer] |

---

## HIPAA Analysis

**HIPAA identifiers present:** [YES/NO]

**If YES, identifiers identified:**
| Identifier | Present | Justification for inclusion |
|------------|---------|---------------------------|
| Names | YES/NO | [Reason] |
| Dates | YES/NO | [Reason] |
| [etc.] | | |

**Authorization approach:** [Signed / Waiver / Limited Dataset / De-identified]

**Rationale for approach:** [Why this authorization method was selected]

---

## Data Flow Analysis

### Data Sources
| Source | Internal/External | Contains Identifiers | Appendix Triggered |
|--------|-------------------|---------------------|-------------------|
| [Source] | [I/E] | [YES/NO] | [A/none] |

### Data Destinations
| Destination | Internal/External | Contains Identifiers | Appendix Triggered |
|-------------|-------------------|---------------------|-------------------|
| [Dest] | [I/E] | [YES/NO] | [B/none] |

---

## Data Security Plan Decisions

**HIPAA identifiers collected:** [YES/NO]

**If NO:** Document marked as "Sensitive Data" only; no additional sections required.

**If YES, collection methods:**
| Method | Applicable | Appendix |
|--------|------------|----------|
| Individual device | YES/NO | 1B(1) |
| Web/cloud | YES/NO | 1B(2) |
| Non-approved server | YES/NO | 1B(3) |
| Approved UVA server | YES/NO | 1B(4) |

**Storage location selected:** [Server/platform name]

**Rationale:** [Why this storage location]

---

## Assumptions Made

List any assumptions made during form completion:

1. **Assumption:** [Statement]
   **Basis:** [Why this assumption was reasonable]
   **Impact if incorrect:** [What would change]

2. [Repeat as needed]

---

## Recommendations for Researcher Review

Before submission, the researcher should verify:

- [ ] PI contact information is current
- [ ] Co-investigator list is complete
- [ ] Funding information matches grant application
- [ ] Data elements accurately reflect study protocol
- [ ] All team members have completed CITI training
- [ ] [Any study-specific items to verify]

---

## Revision History

| Date | Version | Changes | Reason |
|------|---------|---------|--------|
| [Date] | 1.0 | Initial generation | [Initial submission] |

---

## Example Rationale (NEMSIS Study)

### Study Classification
**Determination:** Exempt

**Rationale:** This study involves secondary analysis of an existing de-identified dataset with no direct subject contact, meeting exempt category 4 (secondary research using identifiable private information when publicly available or de-identified).

### Appendices Included

#### Appendix A: Receiving Information from Outside UVA
**Included because:** Study receives data from NEMSIS TAC at University of Utah.
**Triggering factor:** Answer "YES" to receiving data from outside UVA.
**Content:** NEMSIS research dataset containing de-identified EMS event records and derived area-level covariates.

#### Appendix J: Sponsor/Support Source
**Included because:** Study is funded by Emergency Medicine Foundation.
**Triggering factor:** Answer "YES" to outside support/sponsorship.
**Content:** Foundation grant details and departmental support.

### Appendices Excluded

#### Appendix B: Sending Information Outside UVA
**Excluded because:** No data shared externally before publication; only aggregate results will be disseminated.

#### Appendix C, D: Privacy/HIPAA
**Excluded because:** Data received is de-identified with no direct HIPAA identifiers. Area-level covariates (State/County/ZIP) are linked by NEMSIS TAC and only derived variables returned to UVA.

#### Appendix F: Recruitment
**Excluded because:** No subject recruitment; retrospective data analysis only.

#### Appendix G: Compensation
**Excluded because:** No subject compensation; no direct subject contact.

#### Appendix I: Taping/Photography
**Excluded because:** No recording of subjects; data analysis only.
