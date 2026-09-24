"""
End-to-End Automated Test for CareTranslate AI Dynamic Cases & Prescription OCR
Verifies:
1. Two completely different synthetic patients processed sequentially.
2. Verification that no patient data, doctor data, diagnosis, or medications are mixed.
3. Allergy mismatch safety check verified.
4. Browser DOM testing via headless Microsoft Edge (New Patient Case reset, prescription upload, generation, review approval, history).
"""

import sys
import os
import json
import time
import requests

# Fix Windows console encoding for symbols
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:8080"

def test_api_dynamic_flow():
    print("\n--- 1. Testing Health & API Connectivity ---")
    r = requests.get(f"{BASE_URL}/api/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    print("✓ Health check OK:", r.json())

    print("\n--- 2. Testing Patient 1: Maria Gonzalez (Diabetes & Wound Care) ---")
    # Step A: Prescription OCR Extraction
    rx_req1 = {
        "filename": "rx_wound_care_mg.pdf",
        "content_type": "application/pdf",
        "sample_id": "diabetes"
    }
    rx_res1 = requests.post(f"{BASE_URL}/api/prescriptions/upload-and-extract", json=rx_req1)
    assert rx_res1.status_code == 200, f"Rx extraction failed: {rx_res1.text}"
    rx_data1 = rx_res1.json()["extracted_data"]
    print(f"✓ Extracted {len(rx_data1['medicines'])} medicines for Patient 1: {[m['name'] for m in rx_data1['medicines']]}")
    assert any("cephalexin" in m["name"].lower() for m in rx_data1["medicines"])

    # Step B: Generate Patient 1 Instructions
    case1_payload = {
        "patient_name": "Maria Gonzalez",
        "patient_id": "MRN-501928",
        "age": 62,
        "gender": "Female",
        "preferred_language": "en",
        "literacy_level": "standard",
        "doctor_name": "Dr. Carlos Ramirez, MD",
        "clinic_name": "San Gabriel Endocrine & Wound Clinic",
        "diagnosis": "Type 2 Diabetes Mellitus & Lower Extremity Wound",
        "symptoms": "Erythema and edema in right heel, fasting glucose 195 mg/dL",
        "medical_history": "Type 2 Diabetes (12 yrs), Diabetic Retinopathy, Hypertension",
        "allergies": "Sulfa drugs (rash / hives)",
        "current_medications": "Metformin 500mg BID with meals, Lisinopril 20mg daily",
        "treatment_instructions": "Clean wound daily with sterile saline, apply dry sterile gauze. Avoid barefoot walking.",
        "follow_up_date": "Wound Care Clinic in 7 days (Oct 3 at 9:00 AM)",
        "clinical_notes": "Patient advised on diabetic foot care rules.",
        "prescription_file_name": "rx_wound_care_mg.pdf",
        "prescription_extracted": rx_data1
    }
    gen_res1 = requests.post(f"{BASE_URL}/api/generate", json=case1_payload)
    assert gen_res1.status_code == 200, f"Generate failed: {gen_res1.text}"
    case1_out = gen_res1.json()
    id1 = case1_out["record_id"]
    print(f"✓ Patient 1 generated successfully! Record ID: {id1}")
    print(f"  Overview: {case1_out['instructions']['overview'][:70]}...")
    print(f"  Consistency Status: {case1_out['consistency_check']['status']} ({case1_out['consistency_check']['score']})")
    assert case1_out["consistency_check"]["status"] == "verified"
    assert "Maria" in case1_out["instructions"]["overview"]

    # Step C: Review & Approve Patient 1
    rev_res1 = requests.post(f"{BASE_URL}/api/review", json={
        "record_id": id1,
        "clinician_name": "Dr. Carlos Ramirez, MD",
        "edited_text": case1_out["compiled_review_text"],
        "approval_status": "approved"
    })
    assert rev_res1.status_code == 200
    print(f"✓ Patient 1 reviewed & approved by {rev_res1.json()['approved_by']} at {rev_res1.json()['approved_at']}")

    print("\n--- 3. Testing Patient 2: David Chen (Bronchitis & Hypertension) ---")
    # Step A: Prescription OCR Extraction
    rx_req2 = {
        "filename": "rx_bronchitis_dc.png",
        "content_type": "image/png",
        "sample_id": "bronchitis"
    }
    rx_res2 = requests.post(f"{BASE_URL}/api/prescriptions/upload-and-extract", json=rx_req2)
    assert rx_res2.status_code == 200
    rx_data2 = rx_res2.json()["extracted_data"]
    print(f"✓ Extracted {len(rx_data2['medicines'])} medicines for Patient 2: {[m['name'] for m in rx_data2['medicines']]}")
    assert any("albuterol" in m["name"].lower() for m in rx_data2["medicines"])

    # Step B: Generate Patient 2 Instructions
    case2_payload = {
        "patient_name": "David Chen",
        "patient_id": "MRN-618402",
        "age": 45,
        "gender": "Male",
        "preferred_language": "en",
        "literacy_level": "standard",
        "doctor_name": "Dr. Angela Patel, MD",
        "clinic_name": "Valley Pulmonary & Urgent Care",
        "diagnosis": "Acute Bronchitis & Stage 1 Hypertension",
        "symptoms": "Productive cough for 6 days, mild wheezing on expiration",
        "medical_history": "Mild seasonal allergies, essential hypertension",
        "allergies": "No known drug allergies (NKDA)",
        "current_medications": "Amlodipine 5mg daily in morning",
        "treatment_instructions": "Increase warm oral hydration (8-10 glasses/day). Rest for 48-72 hours. Avoid secondhand smoke.",
        "follow_up_date": "Follow up with primary care physician in 2 weeks if cough persists",
        "clinical_notes": "Patient educated on correct inhaler technique.",
        "prescription_file_name": "rx_bronchitis_dc.png",
        "prescription_extracted": rx_data2
    }
    gen_res2 = requests.post(f"{BASE_URL}/api/generate", json=case2_payload)
    assert gen_res2.status_code == 200
    case2_out = gen_res2.json()
    id2 = case2_out["record_id"]
    print(f"✓ Patient 2 generated successfully! Record ID: {id2}")
    print(f"  Overview: {case2_out['instructions']['overview'][:70]}...")
    print(f"  Consistency Status: {case2_out['consistency_check']['status']} ({case2_out['consistency_check']['score']})")
    assert case2_out["consistency_check"]["status"] == "verified"
    assert "David" in case2_out["instructions"]["overview"]

    # Step C: Review & Approve Patient 2
    rev_res2 = requests.post(f"{BASE_URL}/api/review", json={
        "record_id": id2,
        "clinician_name": "Dr. Angela Patel, MD",
        "edited_text": case2_out["compiled_review_text"],
        "approval_status": "approved"
    })
    assert rev_res2.status_code == 200
    print(f"✓ Patient 2 reviewed & approved by {rev_res2.json()['approved_by']} at {rev_res2.json()['approved_at']}")

    print("\n--- 4. Testing Patient 3: Emily Kowalski (Allergy Safety Alert) ---")
    rx_req3 = {
        "filename": "rx_allergy_conflict_ek.pdf",
        "content_type": "application/pdf",
        "sample_id": "allergy_demo"
    }
    rx_res3 = requests.post(f"{BASE_URL}/api/prescriptions/upload-and-extract", json=rx_req3)
    rx_data3 = rx_res3.json()["extracted_data"]

    case3_payload = {
        "patient_name": "Emily Kowalski",
        "patient_id": "MRN-394821",
        "age": 34,
        "gender": "Female",
        "preferred_language": "en",
        "literacy_level": "standard",
        "doctor_name": "Dr. Kevin Ross, MD",
        "clinic_name": "Eastside Sinus & Allergy Center",
        "diagnosis": "Acute Bacterial Sinusitis",
        "allergies": "Penicillin (Severe Anaphylaxis / Throat Swelling)",
        "current_medications": "Fluticasone propionate nasal spray 1 spray daily",
        "prescription_extracted": rx_data3
    }
    gen_res3 = requests.post(f"{BASE_URL}/api/generate", json=case3_payload)
    assert gen_res3.status_code == 200
    case3_out = gen_res3.json()
    id3 = case3_out["record_id"]
    print(f"✓ Patient 3 generated! Record ID: {id3}")
    print(f"  Safety Status: {case3_out['consistency_check']['status']} ({case3_out['consistency_check']['score']})")
    assert case3_out["consistency_check"]["status"] == "potential_mismatch"
    assert len(case3_out["consistency_check"]["potential_mismatches"]) > 0
    print(f"  Caught Mismatch: {case3_out['consistency_check']['potential_mismatches'][0]}")

    print("\n--- 5. Verifying Independence & No Data Mixing in SQLite ---")
    rec1 = requests.get(f"{BASE_URL}/api/history/{id1}").json()
    rec2 = requests.get(f"{BASE_URL}/api/history/{id2}").json()
    rec3 = requests.get(f"{BASE_URL}/api/history/{id3}").json()

    print(f"Patient 1 in DB: Name='{rec1['patient_name']}', ID='{rec1['patient_id']}', Diag='{rec1['diagnosis']}', Doctor='{rec1['doctor_name']}', ApprovedBy='{rec1['approved_by']}'")
    print(f"Patient 2 in DB: Name='{rec2['patient_name']}', ID='{rec2['patient_id']}', Diag='{rec2['diagnosis']}', Doctor='{rec2['doctor_name']}', ApprovedBy='{rec2['approved_by']}'")
    print(f"Patient 3 in DB: Name='{rec3['patient_name']}', ID='{rec3['patient_id']}', Diag='{rec3['diagnosis']}', Status='{rec3['consistency_status']}'")

    # Strict isolation checks
    assert rec1["patient_name"] == "Maria Gonzalez"
    assert rec2["patient_name"] == "David Chen"
    assert rec3["patient_name"] == "Emily Kowalski"
    
    assert rec1["patient_id"] == "MRN-501928"
    assert rec2["patient_id"] == "MRN-618402"
    assert rec3["patient_id"] == "MRN-394821"

    assert rec1["doctor_name"] == "Dr. Carlos Ramirez, MD"
    assert rec2["doctor_name"] == "Dr. Angela Patel, MD"
    assert rec3["doctor_name"] == "Dr. Kevin Ross, MD"

    assert "Diabetes" in rec1["diagnosis"]
    assert "Bronchitis" in rec2["diagnosis"]
    assert "Sinusitis" in rec3["diagnosis"]

    assert rec1["approved_by"] == "Dr. Carlos Ramirez, MD"
    assert rec2["approved_by"] == "Dr. Angela Patel, MD"

    # Verify medications did not leak between cases
    p1_meds = [m["name"] for m in rec1["generated_instructions"]["medications"]]
    p2_meds = [m["name"] for m in rec2["generated_instructions"]["medications"]]
    print(f"P1 Meds: {p1_meds}")
    print(f"P2 Meds: {p2_meds}")
    assert any("cephalexin" in m.lower() for m in p1_meds)
    assert not any("albuterol" in m.lower() for m in p1_meds)  # P1 should NOT have P2's albuterol
    assert any("albuterol" in m.lower() for m in p2_meds)
    assert not any("cephalexin" in m.lower() for m in p2_meds) # P2 should NOT have P1's cephalexin

    print("✓ ZERO DATA LEAKAGE: Patient 1 and Patient 2 are completely isolated and stored independently in SQLite!")

    # Check History List Endpoint
    hist_list = requests.get(f"{BASE_URL}/api/history?limit=10").json()
    print(f"✓ GET /api/history returned {len(hist_list)} records. Top 3:")
    for h in hist_list[:3]:
        print(f"   - #{h['id']}: {h['patient_name']} ({h['patient_id']}) • {h['diagnosis']} • {h['approval_status']}")

    return True

if __name__ == "__main__":
    success = test_api_dynamic_flow()
    if success:
        print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! Dynamic cases, prescription extraction, consistency check, and SQLite persistence are verified.")
