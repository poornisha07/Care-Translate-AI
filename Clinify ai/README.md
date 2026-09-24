# CareTranslate AI 🏥

> **Clinical NLP & Prescription OCR System**: Converts dynamic clinical cases and uploaded doctor prescriptions into simple, patient-friendly discharge instructions with automated 4-part factual consistency auditing, clinician review sign-off, and independent SQLite persistence.

![CareTranslate AI](https://img.shields.io/badge/Status-Complete-emerald)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%2B%20SQLite-009688)
![OCR](https://img.shields.io/badge/Vision%20OCR-Gemini%20%2B%20Clinical%20Heuristic-orange)
![Pydantic](https://img.shields.io/badge/Validation-Pydantic%20v2-e91e63)
![Generative AI](https://img.shields.io/badge/AI%20Engine-Gemini%20%2B%20Clinical%20NLP-4285f4)

---

## 🌟 Key Capabilities & Architecture

1. **Dynamic Patient Information Form**:
   - Clinicians can create a new case for any patient with 16 editable fields:
     `Patient Name`, `Patient ID`, `Age`, `Gender`, `Preferred Language`, `Literacy Level`, `Doctor Name`, `Hospital/Clinic Name`, `Diagnosis/Disease`, `Symptoms`, `Medical History`, `Allergies`, `Current Medications`, `Treatment/Instructions`, `Follow-up Date`, and `Additional Clinical Notes`.
   - No hardcoded doctor or patient data assumed.

2. **Prescription Upload & OCR Extraction**:
   - Supports **JPG, JPEG, PNG, and PDF** files with immediate preview, replace, and remove capabilities.
   - Extracts prescribed medicines (name, strength/dosage, administration frequency, duration, directions), doctor instructions, and follow-up timeline.
   - **Crucial Safety Guardrail**: Extracted details are rendered in an **editable form** with a prominent notice:
     `⚠️ Please verify extracted information. OCR output must be clinician-verified before generating patient instructions.`

3. **Combined Generation Flow**:
   - Synthesizes: **Patient Demographics + Clinical Notes + Clinician-Verified Prescription**.
   - Generates personalized, empathetic, multi-lingual discharge instructions tailored to the specific patient's condition.

4. **4-Part Factual Consistency & Safety Audit**:
   - Compares generated instructions against entered case data and prescription info:
     - ✅ **Verified Information** (confirmed medication schedules, allergy clearance, appointments)
     - ⚠️ **Potential Mismatches** (e.g. Penicillin allergy vs. Augmentin/Amoxicillin cross-reactivity alert)
     - ❓ **Missing Information** (prescribed drugs or instructions omitted)
     - 🔍 **Unsupported Information** (hallucinated or ungrounded directions)

5. **+ New Patient Case Button**:
   - Clearly visible button in the header navigation and form to immediately reset all fields and prepare for a new patient without reloading the application.

6. **Multi-Patient Case History & Independent SQLite Persistence**:
   - Every patient case is stored as an independent record in SQLite (`discharge_records` table).
   - History modal lists all cases with Patient Name, ID, Diagnosis, Doctor, Date, and Status (`Approved` / `Draft`).
   - "View / Edit" loads any previous case directly back into the clinician workspace.

---

## 📡 Backend API Endpoints

Interactive Swagger documentation is available at **`/docs`** and ReDoc at **`/redoc`**.

* **`POST /api/prescriptions/upload-and-extract`**:
  Uploads prescription image/PDF and extracts structured medications, directions, and follow-up.
* **`POST /api/generate`**:
  Accepts full dynamic patient case + verified prescription, generates plain-language instructions, executes 4-part consistency check, and persists to SQLite.
* **`POST /api/check-consistency`**:
  Audits instructions against case data and prescription details.
* **`POST /api/review`**:
  Allows attending clinicians to edit, review, and digitally sign off on the discharge handout.
* **`GET /api/history`**:
  Retrieves list of multiple saved patient cases from SQLite.
* **`GET /api/history/{id}`**:
  Retrieves complete details of any specific patient case to reload into the workspace.
* **`DELETE /api/history/{id}`**:
  Deletes a specific patient case record.

---

## 🚀 How to Run the Application

### 1. Start the Server
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8080
```

### 2. Access in Browser
- **Dashboard:** [http://localhost:8080/](http://localhost:8080/)
- **Swagger API Docs:** [http://localhost:8080/docs](http://localhost:8080/docs)

---

## 🧪 Automated End-to-End Test Suite

Run the automated verification suite to test multiple patients sequentially:

```bash
# 1. API & Data Isolation Verification
python test_dynamic_e2e.py

# 2. Browser CDP Test (Full UI, reset button, and multi-patient DOM check)
python test_e2e.py
```
*(Verifies zero data bleeding between patients, prescription OCR extraction, form reset, approval stamps, and 0 console errors.)*
