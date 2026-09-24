"""
CareTranslate AI - Database Layer (SQLite)
Handles persistence for dynamic patient cases, prescription data,
AI generated discharge instructions, consistency audits, and clinician reviews.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "caretranslate.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create discharge_records table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS discharge_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        patient_id TEXT,
        mrn TEXT,
        age INTEGER,
        gender TEXT,
        doctor_name TEXT,
        clinic_name TEXT,
        diagnosis TEXT,
        symptoms TEXT,
        medical_history TEXT,
        allergies TEXT,
        current_medications TEXT,
        treatment_instructions TEXT,
        follow_up_date TEXT,
        clinical_notes TEXT,
        original_note TEXT,
        prescription_file_name TEXT,
        prescription_file_data TEXT,
        prescription_extracted_data TEXT,
        selected_language TEXT NOT NULL DEFAULT 'en',
        literacy_level TEXT NOT NULL DEFAULT 'standard',
        generated_instructions TEXT NOT NULL,
        consistency_status TEXT NOT NULL DEFAULT 'verified',
        consistency_result TEXT NOT NULL,
        readability_metrics TEXT,
        clinician_edited_text TEXT,
        approval_status TEXT NOT NULL DEFAULT 'draft',
        approved_by TEXT,
        approved_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)
    conn.commit()

    # Migration check: Ensure newly added columns exist in older tables
    cursor.execute("PRAGMA table_info(discharge_records)")
    existing_cols = {row["name"] for row in cursor.fetchall()}
    
    desired_cols = {
        "patient_id": "TEXT",
        "gender": "TEXT",
        "doctor_name": "TEXT",
        "clinic_name": "TEXT",
        "symptoms": "TEXT",
        "medical_history": "TEXT",
        "allergies": "TEXT",
        "current_medications": "TEXT",
        "treatment_instructions": "TEXT",
        "follow_up_date": "TEXT",
        "clinical_notes": "TEXT",
        "prescription_file_name": "TEXT",
        "prescription_file_data": "TEXT",
        "prescription_extracted_data": "TEXT"
    }

    for col, col_type in desired_cols.items():
        if col not in existing_cols:
            try:
                cursor.execute(f"ALTER TABLE discharge_records ADD COLUMN {col} {col_type}")
            except Exception as e:
                pass
    conn.commit()

    # Seed if database is completely empty
    cursor.execute("SELECT COUNT(*) FROM discharge_records")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_initial_records(cursor)
        conn.commit()

    conn.close()

def seed_initial_records(cursor):
    """Seed synthetic patient records demonstrating different patients, doctors, and conditions"""
    now = datetime.now().isoformat()
    
    seeds = [
        {
            "patient_name": "Maria Gonzalez",
            "patient_id": "MRN-501928",
            "mrn": "MRN-501928",
            "age": 62,
            "gender": "Female",
            "doctor_name": "Dr. Carlos Ramirez, MD",
            "clinic_name": "San Gabriel Endocrine & Wound Clinic",
            "diagnosis": "Type 2 Diabetes Mellitus & Lower Extremity Wound",
            "symptoms": "Erythema and edema in right heel, peripheral neuropathy, fasting glucose 195 mg/dL",
            "medical_history": "Type 2 Diabetes (12 yrs), Diabetic Retinopathy, Hypertension",
            "allergies": "Sulfa drugs (rash / hives)",
            "current_medications": "Metformin 500mg BID with meals, Lisinopril 20mg daily",
            "treatment_instructions": "Cephalexin 500mg QID x 10 days for cellulitis. Clean wound with mild saline, apply dry sterile gauze daily. Inspect both feet every evening. Avoid barefoot walking.",
            "follow_up_date": "Wound Care Clinic in 7 days (Oct 3 at 9:00 AM)",
            "clinical_notes": "Patient advised on diabetic foot care rules and signs of systemic infection.",
            "original_note": "PATIENT: Maria Gonzalez | MRN: 501928 | 62F\nDIAGNOSIS: T2D with right lower extremity cellulitis / wound.\nORDERS: Cephalexin 500mg QID x 10d, Metformin 500mg BID.\nDaily saline wound dressing, no barefoot walking. Follow-up 7 days.",
            "prescription_file_name": "rx_wound_care_mg.pdf",
            "prescription_extracted_data": json.dumps({
                "medicines": [
                    {"name": "Cephalexin (Keflex)", "dosage": "500 mg", "frequency": "4 times daily (every 6 hours)", "duration": "10 days", "instructions": "Complete full 10-day course even if wound looks healed"}
                ],
                "doctor_instructions": "Keep wound clean and dry. Check blood sugar before breakfast and dinner.",
                "follow_up": "Return to clinic Oct 3 at 9:00 AM",
                "doctor_name": "Dr. Carlos Ramirez, MD",
                "clinic_name": "San Gabriel Endocrine & Wound Clinic"
            }),
            "selected_language": "en",
            "literacy_level": "standard",
            "generated_instructions": json.dumps({
                "overview": "Maria, you were evaluated for a mild skin infection (cellulitis) on your right heel alongside your diabetes management. Taking your antibiotic on schedule and protecting your feet will help your skin heal completely.",
                "medications": [
                    {"name": "Cephalexin (Keflex) 500 mg", "nickname": "Antibiotic capsule", "timing": "Take 1 capsule 4 times a day (breakfast, lunch, dinner, bedtime)", "purpose": "Fights the bacterial skin infection.", "warning": "Finish all capsules even if you feel better."},
                    {"name": "Metformin 500 mg", "nickname": "Blood sugar pill", "timing": "1 tablet twice daily with morning and evening meals", "purpose": "Helps your body maintain steady blood sugar levels.", "warning": "Take with meals to prevent stomach upset."}
                ],
                "daily_rules": [
                    "Wound Dressing: Clean your heel wound once daily with sterile saline and apply clean dry gauze.",
                    "Foot Checks: Inspect the bottoms of both feet every night with a mirror.",
                    "Footwear: Always wear cushioned socks and comfortable supportive shoes. Never walk barefoot.",
                    "Blood Sugar: Check your blood glucose morning and night; report numbers consistently above 220 mg/dL."
                ],
                "warning_signs": [
                    "Yellow Red Flag: Redness or warmth spreading past the original wound outline",
                    "Red Flag: Fever over 101°F, chills, or foul odor from the wound (call clinic immediately)"
                ],
                "follow_up": [
                    "Wound Care Clinic follow-up with Dr. Carlos Ramirez on Oct 3 at 9:00 AM",
                    "Bring your blood sugar logbook to your visit"
                ]
            }),
            "consistency_status": "verified",
            "consistency_result": json.dumps({
                "status": "verified",
                "score": "100%",
                "summary": "Verified all 2 active medications, exact Cephalexin 500mg QID schedule, daily wound dressing orders, and Sulfa allergy clearance.",
                "verified_information": ["Cephalexin 500mg QID for 10 days", "Metformin 500mg BID with food", "No sulfa antibiotic prescribed (Allergy safe)"],
                "potential_mismatches": [],
                "missing_information": [],
                "unsupported_information": [],
                "detected_issues": [],
                "checks": [
                    {"item": "Medication Dosage Audit", "status": "pass", "detail": "Cephalexin 500mg QID and Metformin 500mg BID match source notes."},
                    {"item": "Allergy Cross-Check", "status": "pass", "detail": "Patient has Sulfa allergy. Prescribed cephalosporin is clinically safe."},
                    {"item": "Follow-up Timing Check", "status": "pass", "detail": "Wound Care Clinic scheduled exactly in 7 days."}
                ]
            }),
            "readability_metrics": json.dumps({
                "clinical_fk_grade": 12.8,
                "translated_fk_grade": 6.5,
                "clinical_reading_ease": 38.2,
                "translated_reading_ease": 74.6,
                "jargon_reduced_count": 9
            }),
            "approval_status": "approved",
            "approved_by": "Dr. Carlos Ramirez, MD",
            "approved_at": "11:20 AM"
        },
        {
            "patient_name": "David Chen",
            "patient_id": "MRN-618402",
            "mrn": "MRN-618402",
            "age": 45,
            "gender": "Male",
            "doctor_name": "Dr. Angela Patel, MD",
            "clinic_name": "Valley Pulmonary & Urgent Care",
            "diagnosis": "Acute Bronchitis & Stage 1 Hypertension",
            "symptoms": "Persistent productive cough for 6 days, mild wheezing, BP 142/88 mmHg, afebrile",
            "medical_history": "Mild seasonal allergies, essential hypertension",
            "allergies": "No known drug allergies (NKDA)",
            "current_medications": "Amlodipine 5mg daily in the morning",
            "treatment_instructions": "Albuterol HFA inhaler 2 puffs every 4 to 6 hours as needed for wheezing or chest tightness. Benzonatate (Tessalon Perles) 100mg TID PRN for cough. Increase warm oral hydration. Rest for 3 days.",
            "follow_up_date": "Follow up with primary care doctor in 2 weeks if cough persists",
            "clinical_notes": "Advised on correct inhaler technique with spacer and avoiding tobacco smoke.",
            "original_note": "PATIENT: David Chen | 45M | MRN: 618402\nDIAGNOSIS: Acute viral bronchitis + hypertension.\nRX: Albuterol 90mcg 2 puffs q4-6h prn wheeze, Tessalon 100mg TID prn cough.\nContinue Amlodipine 5mg daily. Hydration, PCP f/u 2 weeks.",
            "prescription_file_name": "rx_bronchitis_dc.png",
            "prescription_extracted_data": json.dumps({
                "medicines": [
                    {"name": "Albuterol Inhaler (ProAir)", "dosage": "90 mcg (2 puffs)", "frequency": "Every 4 to 6 hours as needed", "duration": "As needed (PRN)", "instructions": "Inhale 2 puffs for wheezing or tightness"},
                    {"name": "Benzonatate (Tessalon Perles)", "dosage": "100 mg", "frequency": "3 times daily as needed", "duration": "5 days", "instructions": "Swallow whole with water; do not chew or crush capsule"}
                ],
                "doctor_instructions": "Drink plenty of water and warm tea. Avoid secondhand smoke and cold dry air.",
                "follow_up": "Check with primary doctor in 2 weeks if cough has not improved",
                "doctor_name": "Dr. Angela Patel, MD",
                "clinic_name": "Valley Pulmonary & Urgent Care"
            }),
            "selected_language": "en",
            "literacy_level": "standard",
            "generated_instructions": json.dumps({
                "overview": "David, you were treated for acute bronchitis, which is temporary inflammation of your breathing airways following a cold. Your lungs need rest and moisture to heal.",
                "medications": [
                    {"name": "Albuterol Inhaler (ProAir)", "nickname": "Rescue breathing inhaler", "timing": "Breathe in 2 puffs every 4 to 6 hours when you feel chest tightness or wheezing", "purpose": "Relaxes airway muscles to make breathing easier.", "warning": "Rinse your mouth with water after using."},
                    {"name": "Benzonatate (Tessalon Perles) 100 mg", "nickname": "Cough relief capsule", "timing": "1 capsule 3 times a day as needed for severe coughing fits", "purpose": "Numbs cough receptors in the throat and lungs.", "warning": "Swallow whole; do not bite or chew the capsule."},
                    {"name": "Amlodipine 5 mg", "nickname": "Blood pressure daily pill", "timing": "1 tablet every morning", "purpose": "Maintains steady blood pressure.", "warning": "Do not skip your blood pressure medication."}
                ],
                "daily_rules": [
                    "Hydration: Drink 8 to 10 glasses of water, herbal tea, or broth daily to thin mucus.",
                    "Rest: Take at least 48 to 72 hours of restful downtime; avoid strenuous cardiovascular workouts.",
                    "Air Quality: Run a cool-mist humidifier in your bedroom at night and avoid all smoke exposure."
                ],
                "warning_signs": [
                    "Warning: Coughing up dark green or blood-tinged phlegm, or new fever above 101°F",
                    "Emergency: Severe shortness of breath or blue lips (call 911 immediately)"
                ],
                "follow_up": [
                    "Schedule a check-up with your primary physician in 14 days if coughing lingers.",
                    "Call Valley Pulmonary if symptoms worsen over the next 48 hours."
                ]
            }),
            "consistency_status": "verified",
            "consistency_result": json.dumps({
                "status": "verified",
                "score": "100%",
                "summary": "All 3 medications (Albuterol PRN, Benzonatate, Amlodipine maintenance), safety warnings on Tessalon Perles chewing, and 2-week follow-up are fully verified.",
                "verified_information": ["Albuterol 2 puffs q4-6h prn", "Tessalon 100mg swallow whole warning", "Amlodipine 5mg ongoing adherence"],
                "potential_mismatches": [],
                "missing_information": [],
                "unsupported_information": [],
                "detected_issues": [],
                "checks": [
                    {"item": "Medication Dosage Audit", "status": "pass", "detail": "Dosages and PRN conditions correctly mapped."},
                    {"item": "Safety Warning Check", "status": "pass", "detail": "Crucial Tessalon Perles 'do not chew' warning included."},
                    {"item": "Follow-up Consistency", "status": "pass", "detail": "PCP 2-week follow up preserved accurately."}
                ]
            }),
            "readability_metrics": json.dumps({
                "clinical_fk_grade": 11.2,
                "translated_fk_grade": 6.8,
                "clinical_reading_ease": 44.1,
                "translated_reading_ease": 76.2,
                "jargon_reduced_count": 7
            }),
            "approval_status": "approved",
            "approved_by": "Dr. Angela Patel, MD",
            "approved_at": "02:45 PM"
        }
    ]
    
    for s in seeds:
        cursor.execute("""
        INSERT INTO discharge_records (
            patient_name, patient_id, mrn, age, gender,
            doctor_name, clinic_name, diagnosis, symptoms,
            medical_history, allergies, current_medications,
            treatment_instructions, follow_up_date, clinical_notes,
            original_note, prescription_file_name, prescription_extracted_data,
            selected_language, literacy_level, generated_instructions,
            consistency_status, consistency_result, readability_metrics,
            approval_status, approved_by, approved_at,
            created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?,
            ?, ?
        )
        """, (
            s["patient_name"], s["patient_id"], s["mrn"], s["age"], s["gender"],
            s["doctor_name"], s["clinic_name"], s["diagnosis"], s["symptoms"],
            s["medical_history"], s["allergies"], s["current_medications"],
            s["treatment_instructions"], s["follow_up_date"], s["clinical_notes"],
            s["original_note"], s["prescription_file_name"], s["prescription_extracted_data"],
            s["selected_language"], s["literacy_level"], s["generated_instructions"],
            s["consistency_status"], s["consistency_result"], s["readability_metrics"],
            s["approval_status"], s["approved_by"], s["approved_at"],
            now, now
        ))

def save_case_record(
    case_data: Dict[str, Any],
    generated_instructions: Dict[str, Any],
    consistency_result: Dict[str, Any],
    readability_metrics: Optional[Dict[str, Any]] = None,
    original_note_compiled: Optional[str] = None
) -> int:
    """
    Saves a dynamic patient case to SQLite as an independent record.
    If record_id is supplied and exists, updates it; otherwise creates a new record.
    """
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    patient_name = (case_data.get("patient_name") or "").strip()
    patient_id = (case_data.get("patient_id") or "").strip()
    mrn = patient_id
    age = case_data.get("age")
    gender = case_data.get("gender") or ""
    doctor_name = case_data.get("doctor_name") or ""
    clinic_name = case_data.get("clinic_name") or ""
    diagnosis = case_data.get("diagnosis") or ""
    symptoms = case_data.get("symptoms") or ""
    med_history = case_data.get("medical_history") or ""
    allergies = case_data.get("allergies") or ""
    current_meds = case_data.get("current_medications") or ""
    treatment = case_data.get("treatment_instructions") or ""
    follow_up = case_data.get("follow_up_date") or ""
    clinical_notes = case_data.get("clinical_notes") or ""
    
    rx_filename = case_data.get("prescription_file_name") or ""
    rx_extracted = case_data.get("prescription_extracted")
    rx_extracted_str = json.dumps(rx_extracted) if rx_extracted else ""
    rx_file_data = case_data.get("prescription_file_data") or ""
    
    lang = case_data.get("preferred_language") or "en"
    lit = case_data.get("literacy_level") or "standard"
    
    original_note = original_note_compiled or f"PATIENT: {patient_name} ({patient_id})\nDIAGNOSIS: {diagnosis}\nALLERGIES: {allergies}\nMEDS: {current_meds}\nTREATMENT: {treatment}\nNOTES: {clinical_notes}"
    
    instructions_json = json.dumps(generated_instructions)
    consistency_status = consistency_result.get("status", "verified")
    consistency_json = json.dumps(consistency_result)
    readability_json = json.dumps(readability_metrics) if readability_metrics else None
    
    existing_id = case_data.get("record_id")
    
    if existing_id:
        cursor.execute("SELECT id FROM discharge_records WHERE id = ?", (existing_id,))
        if cursor.fetchone():
            cursor.execute("""
            UPDATE discharge_records
            SET patient_name = ?, patient_id = ?, mrn = ?, age = ?, gender = ?,
                doctor_name = ?, clinic_name = ?, diagnosis = ?, symptoms = ?,
                medical_history = ?, allergies = ?, current_medications = ?,
                treatment_instructions = ?, follow_up_date = ?, clinical_notes = ?,
                original_note = ?, prescription_file_name = ?, prescription_file_data = ?,
                prescription_extracted_data = ?, selected_language = ?, literacy_level = ?,
                generated_instructions = ?, consistency_status = ?, consistency_result = ?,
                readability_metrics = ?, updated_at = ?
            WHERE id = ?
            """, (
                patient_name, patient_id, mrn, age, gender,
                doctor_name, clinic_name, diagnosis, symptoms,
                med_history, allergies, current_meds,
                treatment, follow_up, clinical_notes,
                original_note, rx_filename, rx_file_data, rx_extracted_str,
                lang, lit, instructions_json, consistency_status, consistency_json,
                readability_json, now, existing_id
            ))
            conn.commit()
            conn.close()
            return existing_id

    # Insert brand new independent case
    cursor.execute("""
    INSERT INTO discharge_records (
        patient_name, patient_id, mrn, age, gender,
        doctor_name, clinic_name, diagnosis, symptoms,
        medical_history, allergies, current_medications,
        treatment_instructions, follow_up_date, clinical_notes,
        original_note, prescription_file_name, prescription_file_data,
        prescription_extracted_data, selected_language, literacy_level,
        generated_instructions, consistency_status, consistency_result,
        readability_metrics, clinician_edited_text, approval_status,
        created_at, updated_at
    ) VALUES (
        ?, ?, ?, ?, ?,
        ?, ?, ?, ?,
        ?, ?, ?,
        ?, ?, ?,
        ?, ?, ?,
        ?, ?, ?,
        ?, ?, ?,
        ?, NULL, 'draft',
        ?, ?
    )
    """, (
        patient_name, patient_id, mrn, age, gender,
        doctor_name, clinic_name, diagnosis, symptoms,
        med_history, allergies, current_meds,
        treatment, follow_up, clinical_notes,
        original_note, rx_filename, rx_file_data,
        rx_extracted_str, lang, lit,
        instructions_json, consistency_status, consistency_json,
        readability_json, now, now
    ))
    
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id

def update_review(record_id: int, clinician_name: str, edited_text: str, approval_status: str = "approved") -> Dict[str, Any]:
    """Updates clinician edits and digital signature timestamp"""
    conn = get_connection()
    cursor = conn.cursor()
    now_dt = datetime.now()
    now_str = now_dt.isoformat()
    approved_at_display = now_dt.strftime("%I:%M %p")
    
    cursor.execute("""
    UPDATE discharge_records
    SET clinician_edited_text = ?,
        approval_status = ?,
        approved_by = ?,
        approved_at = ?,
        updated_at = ?
    WHERE id = ?
    """, (edited_text, approval_status, clinician_name, approved_at_display, now_str, record_id))
    
    conn.commit()
    
    cursor.execute("SELECT * FROM discharge_records WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return {}

def update_consistency(record_id: int, consistency_status: str, consistency_result: dict):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    cursor.execute("""
    UPDATE discharge_records
    SET consistency_status = ?,
        consistency_result = ?,
        updated_at = ?
    WHERE id = ?
    """, (consistency_status, json.dumps(consistency_result), now, record_id))
    
    conn.commit()
    conn.close()

def get_history(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves list of multiple patient cases sorted chronologically"""
    try:
        limit_val = int(limit)
    except Exception:
        limit_val = 50

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, patient_name, patient_id, mrn, age, gender,
           doctor_name, clinic_name, diagnosis,
           selected_language, literacy_level,
           consistency_status, approval_status,
           approved_by, approved_at, created_at, updated_at
    FROM discharge_records
    ORDER BY id DESC
    LIMIT ?
    """, (limit_val,))
    
    rows = cursor.fetchall()
    conn.close()
    
    items = []
    for r in rows:
        d = dict(r)
        # Use patient_id or fallback to mrn
        if not d.get("patient_id") and d.get("mrn"):
            d["patient_id"] = d["mrn"]
        # Format human-friendly timestamp
        try:
            dt = datetime.fromisoformat(d["created_at"])
            d["timestamp_formatted"] = dt.strftime("%b %d, %Y • %I:%M %p")
        except Exception:
            d["timestamp_formatted"] = d["created_at"]
        items.append(d)
        
    return items

def get_record_by_id(record_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves full case details with parsed JSON attributes"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM discharge_records WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
        
    record = dict(row)
    if not record.get("patient_id") and record.get("mrn"):
        record["patient_id"] = record["mrn"]
        
    # Unpack JSON strings
    for json_field in ["generated_instructions", "consistency_result", "readability_metrics", "prescription_extracted_data"]:
        val = record.get(json_field)
        if val and isinstance(val, str):
            try:
                record[json_field] = json.loads(val)
            except Exception:
                pass
                
    return record

def delete_record_by_id(record_id: int) -> bool:
    """Deletes a patient record"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM discharge_records WHERE id = ?", (record_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
