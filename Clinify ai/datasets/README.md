# Medical NLP Knowledge & Research Datasets

This directory provides architecture, schemas, and adapter references for integrating clinical NLP research datasets into CareTranslate AI's source-grounded explanation pipeline.

## 1. Supported Research Resources

### A. MedDialog (Clinical Dialogue & Language Understanding)
- **Purpose**: Medical dialogue understanding for simplifying clinical consultations into layperson-friendly conversational explanations.
- **Reference**: *MedDialog: Large-scale Medical Dialogue Dataset* (Zeng et al., 2020).
- **Application**: Informs the phrasing and empathetic tone of patient discharge summaries without altering clinical facts.

### B. MedNLI (Clinical Natural Language Inference)
- **Purpose**: Premise-hypothesis entailment and contradiction checking.
- **Reference**: *MedNLI — A dataset for natural language inference in the clinical domain* (Romanov & Shivade, 2018; PhysioNet).
- **Application**: Used in `backend/medical_knowledge/knowledge_engine.py` to compare source clinical notes (premises) against AI discharge instructions (hypotheses) to classify statements as:
  - `Entailed / Supported`
  - `Contradiction / Mismatch`
  - `Neutral / Added Claim / Unsupported`

### C. MIMIC-IV Clinical Language Patterns
- **Purpose**: De-identified clinical discharge summary structures and section semantics (Hospital Course, Discharge Medications, Follow-up Instructions).
- **Reference**: PhysioNet credentialed access (Johnson et al., 2023).
- **Application**: Guides clinical section parsing while respecting privacy and licensing boundaries.

## 2. Data Governance & Ethical Compliance
- **No Automatic Downloads**: Restricted or credentialed datasets are never automatically downloaded without explicit user authorization and credential verification.
- **Zero Protected Health Information (PHI)**: All patient records processed in this application are synthetic or local clinician-entered cases.
- **Local Fallback**: When external research datasets are not locally downloaded, CareTranslate AI uses its internal grounded medical knowledge engine and the configured Generative AI model (Google Gemini or OpenAI).

## 3. Grounded Architecture Pipeline
```
[Medical Knowledge Base / Datasets]
              ↓
  [Clinical Note + Diagnosis Input]
              ↓
    [Generative AI / NLP Engine]
              ↓
[Source-Grounded Patient-Friendly Handout]
   (Separated: A. Note Facts | B. General Disease Explanation | C. Missing Fields)
              ↓
  [MedNLI-Style Consistency Checker]
              ↓
    [Clinician Review & Approval]
```
