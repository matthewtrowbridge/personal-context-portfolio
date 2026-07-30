# Exempt Application Decision Tree

## Pre-Screening: Exempt Eligibility

Before proceeding, confirm NONE of these apply (any YES = NOT EXEMPT):

| Question | If YES |
|----------|--------|
| Surveys or interviews given to minors? | NOT EXEMPT |
| Observation of minors with investigator participation? | NOT EXEMPT |
| Procedures causing discomfort beyond daily life? | NOT EXEMPT |
| Deception without prospective agreement? | NOT EXEMPT |
| Research involving rare traits that could cause harm if disclosed? | NOT EXEMPT |
| FDA-regulated research (test articles, clinical investigations)? | NOT EXEMPT |
| Targeted enrollment of prisoners? | NOT EXEMPT |
| FERPA-governed data without student consent? | NOT EXEMPT |
| Embryos, fetal tissue, stem cells involved? | NOT EXEMPT |
| New specimen collection specifically for this research? | NOT EXEMPT |

## Main Decision Tree

### Question 1: Federal Funding or Outside Support?

```
Is this study federally funded?
├── YES → Appendix J REQUIRED
└── NO → Continue

Does this study have support or sponsorship from outside UVA?
├── YES → Appendix J REQUIRED
└── NO → Continue
```

### Question 2: Data/Specimen Flow

```
Will you RECEIVE data or specimens from OUTSIDE UVA?
├── YES → Appendix A REQUIRED
│         Also consider: Does received data contain HIPAA identifiers?
│         ├── YES → Appendix D also REQUIRED
│         └── NO → Continue
└── NO → Continue

Will you SEND data or specimens OUTSIDE UVA (before publication)?
├── YES → Appendix B REQUIRED
│         Will identifiers be sent?
│         ├── YES → Appendix D also REQUIRED
│         └── NO → Continue
└── NO → Continue
```

### Question 3: HIPAA Identifiers

```
Will any of the 18 HIPAA identifiers be collected, used, or accessed?
├── YES → Appendix C (Privacy Plan) REQUIRED
│         Appendix D (HIPAA Regulations) REQUIRED
│         
│         How will HIPAA authorization be obtained?
│         ├── Signed authorization from each subject → No additional appendix
│         ├── Waiver of authorization needed → Appendix E REQUIRED
│         └── Data already de-identified/limited dataset → Document in Appendix D
│
└── NO → May still need Appendix C if other sensitive data involved
```

**The 18 HIPAA Identifiers:**
1. Names
2. Geographic data smaller than state
3. Dates (except year) related to individual
4. Phone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and serial numbers
13. Device identifiers and serial numbers
14. Web URLs
15. IP addresses
16. Biometric identifiers
17. Full-face photographs
18. Any other unique identifying number or code

### Question 4: Subject Interaction

```
Will subjects be actively recruited for this study?
├── YES → Appendix F REQUIRED
│         Describe recruitment methods, materials, locations
└── NO → Continue (e.g., retrospective data analysis)

Will subjects receive compensation or reimbursement?
├── YES → Appendix G REQUIRED
│         Document amounts, timing, proration
└── NO → Continue

Will subjects be recorded (audio, video, photography)?
├── YES → Appendix I REQUIRED
│         Document consent process, storage, destruction
└── NO → Continue
```

### Question 5: Data Use Agreements

```
Is a Data Use Agreement required for data being received?
├── YES → Appendix H REQUIRED (or attach external DUA)
└── NO → Continue

Is data being obtained under a Limited Data Set arrangement?
├── YES → Document in Appendix D, ensure DUA in place
└── NO → Continue
```

## Appendix Summary Matrix

| Appendix | Title | Required When |
|----------|-------|---------------|
| A | Receiving from Outside UVA | Data/specimens coming from external source |
| B | Sending Outside UVA | Data/specimens leaving UVA before publication |
| C | Privacy Plan | HIPAA identifiers OR other sensitive data |
| D | HIPAA Regulations | Any HIPAA identifiers involved |
| E | Waiver of HIPAA Authorization | Cannot obtain signed authorization |
| F | Recruitment | Active subject recruitment |
| G | Compensation | Payment, reimbursement, or gifts |
| H | Data Use Agreement | DUA required for data transfer |
| I | Taping/Photography | Any recording of subjects |
| J | Sponsor/Support Source | Federal funding OR outside support |

## Common Study Type Patterns

### Secondary Data Analysis (De-identified)
- **Typical appendices**: A (if external), J (if funded)
- **Usually skip**: B, C, D, E, F, G, H, I

### Secondary Data Analysis (Limited Dataset)
- **Typical appendices**: A, C, D, H, J (if funded)
- **Usually skip**: B, E, F, G, I

### Online Survey (No HIPAA)
- **Typical appendices**: C, F
- **Usually skip**: A, B, D, E, H, I
- **If compensated**: Add G

### Chart Review with Waiver
- **Typical appendices**: C, D, E
- **Usually skip**: A, B, F, G, H, I

### Multi-site with Data Sharing
- **Typical appendices**: A, B, C, D, H, J
- **Consider**: E (if waiver needed), F (if recruiting)
