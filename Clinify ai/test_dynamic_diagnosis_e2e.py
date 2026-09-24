"""
Comprehensive E2E Test Suite for CareTranslate AI
Validates Dynamic Disease Understanding, Source Grounding, Consistency Checks,
Prescription Analysis, Multilingual Tamil Support, and Regulatory Disclaimers.
"""

import requests
import json
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = "http://127.0.0.1:8080"

def log_test(name, passed, details=""):
    mark = "✅ PASS" if passed else "❌ FAIL"
    print(f"[{mark}] {name}")
    if details:
        print(f"       {details}")
    if not passed:
        sys.exit(1)

def main():
    print("==================================================")
    print("CareTranslate AI - Dynamic Disease & Grounding E2E")
    print("==================================================")

    # 1. Health Check
    r = requests.get(f"{BASE_URL}/api/health", timeout=5)
    log_test("API Health Check", r.status_code == 200, f"Status: {r.status_code}, Res: {r.json()}")

    # 2. TEST 1: Diabetes (Dynamic understanding, no allergy bias, no wound assumption if omitted)
    p_diabetes = {
        "patient_name": "Maria Gonzalez",
        "patient_id": "MRN-101",
        "age": 54,
        "gender": "Female",
        "doctor_name": "Dr. Carlos Ramirez, MD",
        "clinic_name": "Metro Health Endocrinology",
        "diagnosis": "Type 2 Diabetes Mellitus",
        "symptoms": "Increased thirst, frequent urination, mild fatigue",
        "medical_history": "Pre-diabetes diagnosed 2 years ago",
        "allergies": "", # Missing intentionally
        "current_medications": "",
        "treatment_instructions": "Monitor fasting blood glucose daily before breakfast. Maintain a balanced low-sugar diet.",
        "follow_up_date": "Follow up in 4 weeks",
        "prescription_extracted": {
            "medicines": [
                {
                    "name": "Metformin",
                    "dosage": "500 mg",
                    "frequency": "Twice daily with meals",
                    "duration": "30 days",
                    "instructions": "Take with breakfast and dinner to avoid stomach upset"
                }
            ],
            "doctor_instructions": "Check blood sugar twice daily",
            "follow_up": "In 4 weeks"
        }
    }
    r1 = requests.post(f"{BASE_URL}/api/generate", json=p_diabetes, timeout=10)
    log_test("Generate Instructions: Diabetes API response", r1.status_code == 200)
    data1 = r1.json()
    inst1 = data1["instructions"]
    audit1 = data1["consistency_check"]
    review1 = data1["compiled_review_text"]

    overview1 = inst1.get("overview", "")
    print(f"\n[Diabetes Overview Output]:\n{overview1}\n")

    # Check Diabetes specific explanation
    has_diabetes_concept = ("diabetes" in overview1.lower() or "sugar" in overview1.lower() or "glucose" in overview1.lower())
    log_test("TEST 1A: Diabetes diagnosis dynamically understood", has_diabetes_concept, f"Overview mentions diabetes/glucose/sugar: {has_diabetes_concept}")

    # Verify no allergy bias or NKDA assumption
    no_allergy_bias = "allergy" not in overview1.lower() and "penicillin" not in overview1.lower()
    log_test("TEST 1B: No generic allergy response in overview", no_allergy_bias)

    # Verify missing allergies flagged as 'Not provided'
    missing_allergies_flagged = any("allergies" in m.lower() and "not provided" in m.lower() for m in audit1.get("missing_information", []))
    log_test("TEST 1C: Missing allergies flagged as 'Not provided' (NOT 'no allergies')", missing_allergies_flagged, f"Missing info: {audit1.get('missing_information')}")

    # Verify no fake claim of "no allergies"
    no_fake_allergy_claim = "no allergies" not in overview1.lower() and "no known allergies" not in overview1.lower() and "nkda" not in overview1.lower()
    log_test("TEST 1D: Never assumes 'no allergies' when omitted", no_fake_allergy_claim)

    # 3. TEST 2: Hypertension (Medication strictly grounded)
    p_hypertension = {
        "patient_name": "James Wilson",
        "patient_id": "MRN-202",
        "age": 62,
        "gender": "Male",
        "doctor_name": "Dr. Sarah Lin, MD",
        "clinic_name": "Pacific Cardiovascular Center",
        "diagnosis": "Essential Hypertension",
        "symptoms": "Mild morning occipital headache and elevated home blood pressure readings",
        "medical_history": "Hyperlipidemia",
        "allergies": "Sulfa drugs",
        "current_medications": "Atorvastatin 20mg daily",
        "treatment_instructions": "Maintain low-sodium DASH diet. Check blood pressure every morning after waking.",
        "follow_up_date": "Follow up in 2 weeks for blood pressure check",
        "prescription_extracted": {
            "medicines": [
                {
                    "name": "Amlodipine",
                    "dosage": "5 mg",
                    "frequency": "Once daily in the morning",
                    "duration": "30 days",
                    "instructions": "Take with water every morning"
                }
            ],
            "doctor_instructions": "Limit sodium < 2,000 mg daily",
            "follow_up": "Cardiology clinic follow-up in 2 weeks"
        }
    }
    r2 = requests.post(f"{BASE_URL}/api/generate", json=p_hypertension, timeout=10)
    log_test("Generate Instructions: Hypertension API response", r2.status_code == 200)
    data2 = r2.json()
    inst2 = data2["instructions"]
    audit2 = data2["consistency_check"]
    overview2 = inst2.get("overview", "")
    print(f"\n[Hypertension Overview Output]:\n{overview2}\n")

    has_htn_concept = ("hypertension" in overview2.lower() or "blood pressure" in overview2.lower() or "arteries" in overview2.lower())
    log_test("TEST 2A: Hypertension diagnosis dynamically understood", has_htn_concept)

    # Check Amlodipine is included and grounded
    med_names2 = [m.get("name", "") for m in inst2.get("medications", [])]
    has_amlodipine = any("amlodipine" in m.lower() for m in med_names2)
    log_test("TEST 2B: Prescribed Amlodipine 5 mg accurately included", has_amlodipine, f"Medications: {med_names2}")

    # Check daily rules include blood pressure tracking & sodium
    rules2 = " ".join(inst2.get("daily_rules", [])).lower()
    has_bp_rule = "blood pressure" in rules2 or "sodium" in rules2
    log_test("TEST 2C: Grounded daily rules for Hypertension (BP tracking / sodium)", has_bp_rule)

    # 4. TEST 3: Asthma
    p_asthma = {
        "patient_name": "Maya Patel",
        "patient_id": "MRN-303",
        "age": 28,
        "gender": "Female",
        "doctor_name": "Dr. Angela Patel, MD",
        "clinic_name": "Valley Pulmonary Clinic",
        "diagnosis": "Bronchial Asthma Flare-up",
        "symptoms": "Expiratory wheezing, chest tightness, coughing at night",
        "medical_history": "Allergic rhinitis",
        "allergies": "", # omitted
        "current_medications": "",
        "treatment_instructions": "Use rescue inhaler at first sign of wheezing. Avoid cold air and smoke.",
        "follow_up_date": "Follow up in 10 days",
        "prescription_extracted": {
            "medicines": [
                {
                    "name": "Albuterol HFA Inhaler",
                    "dosage": "90 mcg (2 puffs)",
                    "frequency": "Every 4 to 6 hours as needed for wheezing",
                    "duration": "PRN",
                    "instructions": "Inhale 2 puffs for chest tightness"
                }
            ]
        }
    }
    r3 = requests.post(f"{BASE_URL}/api/generate", json=p_asthma, timeout=10)
    data3 = r3.json()
    inst3 = data3["instructions"]
    overview3 = inst3.get("overview", "")
    print(f"\n[Asthma Overview Output]:\n{overview3}\n")

    has_asthma_concept = ("asthma" in overview3.lower() or "airway" in overview3.lower() or "wheez" in overview3.lower())
    log_test("TEST 3A: Asthma diagnosis dynamically understood", has_asthma_concept)

    rules3 = " ".join(inst3.get("daily_rules", [])).lower()
    has_inhaler_rule = "inhaler" in rules3 or "airway" in rules3
    log_test("TEST 3B: Grounded asthma daily rules (inhaler / triggers)", has_inhaler_rule)

    # 5. TEST 4: Migraine
    p_migraine = {
        "patient_name": "Elena Rostova",
        "patient_id": "MRN-404",
        "age": 35,
        "gender": "Female",
        "doctor_name": "Dr. Marcus Vance, MD",
        "clinic_name": "Neurology Associates",
        "diagnosis": "Acute Migraine Headache",
        "symptoms": "Unilateral pulsating headache, photophobia, nausea",
        "medical_history": "None",
        "allergies": "",
        "treatment_instructions": "Rest in dark quiet room. Hydrate well.",
        "follow_up_date": "Follow up in 3 weeks",
        "prescription_extracted": {
            "medicines": [
                {
                    "name": "Sumatriptan",
                    "dosage": "50 mg",
                    "frequency": "At onset of migraine headache",
                    "duration": "PRN",
                    "instructions": "Take at onset of severe head pain"
                }
            ]
        }
    }
    r4 = requests.post(f"{BASE_URL}/api/generate", json=p_migraine, timeout=10)
    data4 = r4.json()
    inst4 = data4["instructions"]
    overview4 = inst4.get("overview", "")
    print(f"\n[Migraine Overview Output]:\n{overview4}\n")

    has_migraine_concept = ("migraine" in overview4.lower() or "head pain" in overview4.lower() or "headache" in overview4.lower())
    log_test("TEST 4A: Migraine diagnosis dynamically understood", has_migraine_concept)

    rules4 = " ".join(inst4.get("daily_rules", [])).lower()
    has_migraine_rules = "quiet" in rules4 or "dark" in rules4 or "trigger" in rules4 or "rest" in rules4
    log_test("TEST 4B: Grounded migraine daily care rules (dark quiet room)", has_migraine_rules)

    warnings4 = " ".join(inst4.get("warning_signs", [])).lower()
    has_thunderclap = "thunderclap" in warnings4 or "stiff neck" in warnings4 or "numbness" in warnings4
    log_test("TEST 4C: Grounded neurological warning signs for Migraine", has_thunderclap)

    # 6. TEST 5: Pneumonia
    p_pneumonia = {
        "patient_name": "Arthur Pendelton",
        "patient_id": "MRN-505",
        "age": 68,
        "gender": "Male",
        "doctor_name": "Dr. Emily Kowalski, MD",
        "clinic_name": "Community Pulmonary Care",
        "diagnosis": "Bacterial Pneumonia",
        "symptoms": "Productive cough with rust-colored sputum, fever of 101.8°F, dyspnea on exertion",
        "medical_history": "Former smoker",
        "allergies": "",
        "treatment_instructions": "Bed rest for 5 days. Drink warm liquids. Complete all antibiotic doses.",
        "follow_up_date": "Chest X-ray and clinic follow-up in 2 weeks",
        "prescription_extracted": {
            "medicines": [
                {
                    "name": "Azithromycin",
                    "dosage": "500 mg day 1, then 250 mg",
                    "frequency": "Once daily for 5 days",
                    "duration": "5 days",
                    "instructions": "Complete entire course"
                }
            ]
        }
    }
    r5 = requests.post(f"{BASE_URL}/api/generate", json=p_pneumonia, timeout=10)
    data5 = r5.json()
    inst5 = data5["instructions"]
    overview5 = inst5.get("overview", "")
    print(f"\n[Pneumonia Overview Output]:\n{overview5}\n")

    has_pneumonia_concept = ("pneumonia" in overview5.lower() or "lung" in overview5.lower() or "air sacs" in overview5.lower())
    log_test("TEST 5A: Pneumonia diagnosis dynamically understood", has_pneumonia_concept)

    rules5 = " ".join(inst5.get("daily_rules", [])).lower()
    has_pna_rules = "warm hydration" in rules5 or "bed rest" in rules5 or "antibiotic" in rules5 or "deep breath" in rules5
    log_test("TEST 5B: Grounded pneumonia daily care rules (bed rest, hydration, antibiotic)", has_pna_rules)

    # 7. TEST 6: POST /api/analyze-diagnosis Endpoint (Requirement 11)
    req_diag = {
        "diagnosis": "Diabetes",
        "symptoms": "polyuria, polydipsia",
        "literacy_level": "standard"
    }
    r_diag = requests.post(f"{BASE_URL}/api/analyze-diagnosis", json=req_diag, timeout=5)
    log_test("POST /api/analyze-diagnosis status code 200", r_diag.status_code == 200)
    diag_data = r_diag.json()
    print(f"\n[POST /api/analyze-diagnosis Output]:\n{json.dumps(diag_data, indent=2)}\n")

    log_test("TEST 6A: analyze-diagnosis returns diagnosis", diag_data.get("diagnosis") == "Diabetes")
    log_test("TEST 6B: analyze-diagnosis returns simple_explanation", len(diag_data.get("simple_explanation", "")) > 15)
    log_test("TEST 6C: analyze-diagnosis returns warnings", len(diag_data.get("warnings", [])) > 0)
    log_test("TEST 6D: analyze-diagnosis returns disclaimer", "AI-generated patient-friendly information must be reviewed" in diag_data.get("disclaimer", ""))

    # 8. TEST 7: POST /api/analyze-diagnosis with unlisted diagnosis (e.g. Acute Otitis Media)
    req_unlisted = {
        "diagnosis": "Acute Otitis Media",
        "symptoms": "ear pain, fever",
        "literacy_level": "basic"
    }
    r_unlisted = requests.post(f"{BASE_URL}/api/analyze-diagnosis", json=req_unlisted, timeout=5)
    log_test("POST /api/analyze-diagnosis unlisted disease status 200", r_unlisted.status_code == 200)
    unlisted_data = r_unlisted.json()
    print(f"\n[Unlisted Diagnosis Analysis]: {unlisted_data.get('simple_explanation')}\n")
    log_test("TEST 7A: Dynamically parses unlisted medical term without allergy template", "otitis" in unlisted_data.get("simple_explanation", "").lower() or "swelling" in unlisted_data.get("simple_explanation", "").lower())

    # 9. TEST 8: POST /api/analyze-prescription Endpoint (Requirement 11)
    req_rx = {
        "filename": "prescription.jpg",
        "sample_id": "cardio"
    }
    r_rx = requests.post(f"{BASE_URL}/api/analyze-prescription", json=req_rx, timeout=5)
    log_test("POST /api/analyze-prescription status 200", r_rx.status_code == 200)
    rx_resp = r_rx.json()
    log_test("TEST 8A: Returns clinician verification notice", "clinician verification" in rx_resp.get("verification_notice", "").lower() or "verify" in rx_resp.get("verification_notice", "").lower())
    log_test("TEST 8B: Extracted medicines present", len(rx_resp["extracted_data"]["medicines"]) >= 1)

    # 10. TEST 9: Tamil Multi-Disease Translation (Requirement 9)
    p_tamil_htn = dict(p_hypertension)
    p_tamil_htn["preferred_language"] = "ta"
    r_ta = requests.post(f"{BASE_URL}/api/generate", json=p_tamil_htn, timeout=10)
    log_test("Generate Instructions in Tamil status 200", r_ta.status_code == 200)
    ta_data = r_ta.json()
    ta_overview = ta_data["instructions"]["overview"]
    print(f"\n[Tamil Hypertension Overview Output]:\n{ta_overview}\n")
    log_test("TEST 9A: Tamil overview contains diagnosis/health guidance in Tamil", "உயர் இரத்த அழுத்தம்" in ta_overview or "இரத்த" in ta_overview)

    # Check medication names preserved in Latin characters
    ta_meds = ta_data["instructions"]["medications"]
    log_test("TEST 9B: Medicine name 'Amlodipine 5 mg' preserved in Latin characters", any("Amlodipine" in m["name"] and "5 mg" in m["name"] for m in ta_meds))

    # 11. TEST 10: Mandatory Regulatory Disclaimer (Requirement 5)
    req_disclaimer = "AI-generated patient-friendly information must be reviewed and approved by a clinician before being provided to the patient."
    log_test("TEST 10A: Disclaimer present in instructions payload", data1["instructions"].get("disclaimer") == req_disclaimer)
    log_test("TEST 10B: Disclaimer present in compiled clinician review text", req_disclaimer in data1["compiled_review_text"])

    # Verify no claims of "100% medically accurate" or "Clinically validated"
    all_compiled = data1["compiled_review_text"] + " " + data2["compiled_review_text"]
    log_test("TEST 10C: No forbidden claim '100% medically accurate'", "100% medically accurate" not in all_compiled)
    log_test("TEST 10D: No forbidden claim 'Clinically validated'", "clinically validated" not in all_compiled.lower())

    print("\n==================================================")
    print("ALL 11 TEST SUITES PASSED FLAWLESSLY! 🚀")
    print("==================================================")

if __name__ == "__main__":
    main()
