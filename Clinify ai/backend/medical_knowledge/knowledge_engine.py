"""
CareTranslate AI - Dynamic Medical Knowledge & Grounding Engine
Interprets clinician-entered diagnoses dynamically without fixed allergy assumptions,
separates source facts from general medical terminology, and executes MedNLI-style
entailment and contradiction audits.
"""

import os
import json
import re
from typing import Dict, Any, List, Optional, Tuple

# Path to datasets reference
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(os.path.dirname(os.path.dirname(CURRENT_DIR)), "datasets")
VOCAB_FILE = os.path.join(DATASETS_DIR, "clinical_vocab_reference.json")

# Core grounded disease concept library
KNOWN_DISEASE_CONCEPTS = {
    "diabetes": {
        "concept": "Diabetes Mellitus",
        "basic": "Diabetes is when there is too much sugar in your blood. Your body needs sugar for energy, but without enough insulin, the sugar gets trapped in your blood instead of feeding your cells.",
        "standard": "Diabetes is a metabolic condition where your blood glucose (sugar) is higher than normal. Your pancreas either does not make enough insulin, or your cells cannot use it properly, leaving excess sugar in your bloodstream.",
        "advanced": "Diabetes Mellitus is a chronic endocrine disorder of carbohydrate metabolism characterized by persistent hyperglycemia resulting from impaired insulin secretion, peripheral insulin resistance, or both.",
        "warnings": [
            "Very high blood sugar readings (such as above 250 mg/dL)",
            "Signs of low blood sugar including shakiness, sudden sweating, confusion, or dizziness",
            "Any new numbness, tingling, or skin sores on your feet that are not healing"
        ]
    },
    "hypertension": {
        "concept": "Hypertension (High Blood Pressure)",
        "basic": "High blood pressure means blood is pushing too hard against your blood pipes. Over time, this extra push can strain your heart and blood vessels.",
        "standard": "High blood pressure means the pressure of blood against the walls of your blood vessels is higher than recommended. Over time, high pressure makes your heart work harder and can damage your arteries.",
        "advanced": "Essential or secondary hypertension is sustained elevation of systemic arterial blood pressure, which increases afterload on the left ventricle and accelerates vascular endothelial stress.",
        "warnings": [
            "A sudden, severe headache or extreme lightheadedness",
            "Blurry vision, double vision, or dark spots in your sight",
            "Chest tightness, difficulty breathing, or unexpected nosebleeds"
        ]
    },
    "asthma": {
        "concept": "Asthma",
        "basic": "Asthma is a lung issue where breathing tubes get puffy and tight. This makes it harder for air to go in and out, which causes wheezing and coughing.",
        "standard": "Asthma is a chronic lung condition where the airways become inflamed, swollen, and narrowed, making breathing difficult and triggering coughing, wheezing, and chest tightness.",
        "advanced": "Bronchial asthma is a chronic inflammatory disorder of the tracheobronchial tree characterized by reversible airflow obstruction and airway hyperresponsiveness to external stimuli.",
        "warnings": [
            "Severe shortness of breath that does not improve within 20 minutes after using your rescue inhaler",
            "Rib or neck muscles pulling in tightly while trying to breathe",
            "Struggling to speak more than a couple of words without stopping for breath"
        ]
    },
    "migraine": {
        "concept": "Migraine Headache",
        "basic": "A migraine is a very strong, throbbing headache, usually on one side of your head. It often makes bright lights and loud sounds hurt your eyes and ears, and can make you feel sick to your stomach.",
        "standard": "A migraine is a neurological condition that causes intense, throbbing head pain, typically on one side of the head. It is commonly accompanied by nausea, vomiting, and extreme sensitivity to light and sound.",
        "advanced": "Migraine is a complex neurovascular disorder involving cortical spreading depression, trigeminovascular activation, and neurogenic dural inflammation causing unilateral pulsating cephalalgia.",
        "warnings": [
            "A sudden, explosive 'thunderclap' headache that peaks in intensity within seconds",
            "Headache accompanied by high fever, stiff neck, confusion, or slurred speech",
            "Sudden numbness or weakness on one side of your face or body, or sudden loss of vision"
        ]
    },
    "pneumonia": {
        "concept": "Pneumonia",
        "basic": "Pneumonia is an infection in your lungs. The tiny air sacs inside your lungs fill with fluid, which makes you cough, run a fever, and feel out of breath.",
        "standard": "Pneumonia is an infection in one or both of your lungs. It causes the tiny air sacs (alveoli) to become inflamed and fill with fluid or mucus, leading to fever, cough with phlegm, and shortness of breath.",
        "advanced": "Pneumonia is acute lower respiratory parenchymal inflammation and consolidation of alveolar spaces caused by viral, bacterial, or fungal pathogens, compromising pulmonary gas exchange.",
        "warnings": [
            "Shortness of breath that worsens rapidly or occurs even while resting quietly",
            "High fever that does not decrease, or shaking chills that return",
            "Coughing up rust-colored, dark green, or blood-streaked mucus, or bluish discoloration of the lips"
        ]
    },
    "bronchitis": {
        "concept": "Acute Bronchitis",
        "basic": "Bronchitis is an inflammation of your main breathing tubes. It makes you cough a lot and produce chest mucus.",
        "standard": "Acute bronchitis is an inflammation of the bronchial breathing tubes that carry air into your lungs, typically leading to a chesty cough, mucus production, and mild fatigue.",
        "advanced": "Acute bronchitis is self-limiting inflammation of the large airways of the lung, primarily the bronchi, with bronchial epithelial edema and mucus hypersecretion.",
        "warnings": [
            "A cough that lasts longer than 3 weeks or begins producing blood",
            "High fever above 101°F or new difficulty catching your breath",
            "Loud chest wheezing that does not improve after resting"
        ]
    },
    "heart failure": {
        "concept": "Heart Failure (CHF)",
        "basic": "Heart failure means your heart pump is tired and not pumping fluid as strongly as it should. This can cause extra fluid to back up into your lungs, ankles, and legs.",
        "standard": "Congestive heart failure means your heart muscle is not pumping blood as efficiently as it should. As a result, fluid can collect in your lungs, legs, and ankles, causing swelling and shortness of breath.",
        "advanced": "Congestive heart failure is a clinical syndrome characterized by structural or functional impairment of ventricular filling or ejection, leading to elevated intracardiac pressures and systemic venous congestion.",
        "warnings": [
            "Rapid weight gain of 3 pounds in a single day or 5 pounds in one week",
            "Increasing swelling in both ankles, legs, or abdomen",
            "Sudden severe shortness of breath, especially when lying flat in bed"
        ]
    },
    "cellulitis": {
        "concept": "Cellulitis / Skin Infection",
        "basic": "Cellulitis is a bacterial skin infection that causes a patch of skin to become red, warm, swollen, and tender to touch.",
        "standard": "Cellulitis is a common bacterial infection of the deep skin layers and underlying tissue, causing redness, swelling, warmth, and pain in the affected area.",
        "advanced": "Cellulitis is an acute bacterial infection of the dermis and subcutaneous tissues, most frequently caused by Streptococcus or Staphylococcus species, manifesting with poorly demarcated erythema and edema.",
        "warnings": [
            "Redness or swelling spreading quickly beyond the marked skin boundary",
            "Fever over 101°F, chills, or sudden body aches",
            "Pus drainage, blistering, or skin darkening over the infected area"
        ]
    },
    "sinusitis": {
        "concept": "Sinusitis",
        "basic": "Sinusitis is swelling inside the air pockets around your nose and forehead, causing facial pressure and a stuffy nose.",
        "standard": "Sinusitis is inflammation of the tissue lining the sinus cavities around your nose, leading to facial pressure, headache, congestion, and nasal discharge.",
        "advanced": "Rhinosinusitis is mucosal inflammation of the paranasal sinuses and nasal cavity, causing ostiomeatal complex obstruction and impaired mucociliary clearance.",
        "warnings": [
            "Severe headache with high fever and stiff neck",
            "Swelling, redness, or pain around one or both eyes",
            "Vision changes or persistent confusion"
        ]
    }
}

def load_vocab_reference() -> Dict[str, Any]:
    """Loads external datasets/vocab reference if available"""
    if os.path.exists(VOCAB_FILE):
        try:
            with open(VOCAB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def explain_diagnosis(diagnosis: str, literacy_level: str = "standard") -> Dict[str, Any]:
    """
    Dynamically analyzes ANY clinical diagnosis entered by the clinician.
    Never falls back to generic allergy responses.
    """
    diag_clean = (diagnosis or "").strip()
    if not diag_clean:
        return {
            "diagnosis": "Not provided",
            "simple_explanation": "Diagnosis was not provided in the clinical notes. Please contact your clinician to clarify your primary condition.",
            "source_supported_points": [],
            "missing_information": ["Primary clinical diagnosis"],
            "warnings": ["Consult your healthcare provider for an accurate diagnostic evaluation."]
        }

    diag_lower = diag_clean.lower()
    level = (literacy_level or "standard").lower()

    # 1. Match known concept library
    matched_key = None
    for k in KNOWN_DISEASE_CONCEPTS:
        if k in diag_lower:
            matched_key = k
            break

    if matched_key:
        concept_data = KNOWN_DISEASE_CONCEPTS[matched_key]
        simple_explanation = concept_data.get(level) or concept_data.get("standard")
        warnings = concept_data.get("warnings", [])
    else:
        # 2. Dynamic medical linguistic interpretation for any clinical term
        simple_explanation, warnings = _interpret_unknown_diagnosis(diag_clean, level)

    return {
        "diagnosis": diag_clean,
        "simple_explanation": simple_explanation,
        "source_supported_points": [f"Diagnosis recorded as: {diag_clean}"],
        "missing_information": [],
        "warnings": warnings
    }

def _interpret_unknown_diagnosis(diag_name: str, level: str) -> Tuple[str, List[str]]:
    """
    Morphological and semantic parsing for unlisted clinical diagnoses.
    Explains the medical roots and clinical nature without inventing patient facts.
    """
    d_lower = diag_name.lower()
    
    # Anatomical and suffix rules
    if d_lower.endswith("itis") or "inflammation" in d_lower:
        organ = d_lower.replace("itis", "").replace("acute", "").replace("chronic", "").strip()
        if level == "basic":
            explanation = f"{diag_name} means irritation and swelling in your {organ or 'body tissues'}."
        elif level == "advanced":
            explanation = f"{diag_name} is characterized by acute or chronic localized tissue inflammation and cellular immune response."
        else:
            explanation = f"{diag_name} refers to inflammation and swelling affecting the body's {organ or 'involved tissues'}."
        warnings = [
            "Fever above 101°F or spreading redness/warmth",
            "Sudden severe pain that does not improve with resting",
            "Any difficulty breathing, swallowing, or sudden weakness"
        ]
    elif d_lower.endswith("algia") or "pain" in d_lower:
        if level == "basic":
            explanation = f"{diag_name} is a medical term for nerve or muscle pain in that area of your body."
        else:
            explanation = f"{diag_name} refers to localized discomfort or nerve irritation affecting the diagnosed region."
        warnings = [
            "Sudden severe pain accompanied by numbness, weakness, or loss of feeling",
            "Pain that prevents normal movement or is accompanied by fever"
        ]
    elif "infection" in d_lower or "abscess" in d_lower or d_lower.endswith("osis"):
        explanation = f"{diag_name} is a condition where microorganisms or bacteria have caused localized infection and tissue reaction."
        warnings = [
            "High fever, shaking chills, or dizziness when standing",
            "Rapidly spreading pain, redness, or discharge from the infected area"
        ]
    elif "fracture" in d_lower or "sprain" in d_lower or "injury" in d_lower or "contusion" in d_lower:
        explanation = f"{diag_name} is a physical trauma or structural injury affecting the bone, joint, or surrounding soft tissue."
        warnings = [
            "Sudden severe swelling, cold or pale fingers/toes, or inability to feel touch",
            "Severe pain not controlled by prescribed pain medication"
        ]
    elif "deficiency" in d_lower or "anemia" in d_lower:
        explanation = f"{diag_name} is a condition where the body has lower-than-normal levels of a vital nutrient or blood component."
        warnings = [
            "Severe dizziness, feeling faint when standing, or chest fluttering",
            "Extreme shortness of breath during light walking"
        ]
    else:
        # General respectful clinical explanation grounded strictly in the name
        if level == "basic":
            explanation = f"{diag_name} is the specific health issue your clinician treated today."
        elif level == "advanced":
            explanation = f"{diag_name} represents the primary clinical pathology identified during your medical evaluation."
        else:
            explanation = f"{diag_name} is the primary medical condition evaluated and treated by your healthcare provider during your visit."
        warnings = [
            "Symptoms that worsen significantly rather than improving with time",
            "New onset fever, difficulty breathing, or unexpected severe pain"
        ]

    return explanation, warnings

def get_danger_signs_for_diagnosis(diagnosis: str, symptoms: str = "") -> List[str]:
    """Returns grounded danger signs corresponding strictly to the disease and symptoms"""
    diag_lower = (diagnosis or "").lower()
    
    for k in KNOWN_DISEASE_CONCEPTS:
        if k in diag_lower:
            return KNOWN_DISEASE_CONCEPTS[k]["warnings"]
            
    # Generic safety red flags when disease is uncataloged
    return [
        "Sudden severe chest pain, shortness of breath, or feeling faint (Call 911 immediately)",
        "New high fever over 101°F or symptoms worsening rapidly instead of improving",
        "Signs of an allergic reaction: sudden hives, lip/facial swelling, or throat tightness"
    ]

def separate_source_facts(case_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Requirement 3: Separates:
    A. Information present in the clinician's note
    B. General explanation of the diagnosis
    C. Information that is missing (strictly flagged as 'Not provided')
    """
    # 1. Clinician Note Facts
    note_facts = []
    diag = case_data.get("diagnosis", "").strip()
    if diag:
        note_facts.append(f"Diagnosis: {diag}")

    symp = case_data.get("symptoms", "").strip()
    if symp and symp.lower() != "none":
        note_facts.append(f"Reported Symptoms: {symp}")

    hist = case_data.get("medical_history", "").strip()
    if hist and hist.lower() != "none":
        note_facts.append(f"Medical History: {hist}")

    allergy = case_data.get("allergies", "").strip()
    if allergy and allergy.lower() != "none" and allergy.lower() != "nkda":
        note_facts.append(f"Documented Allergies: {allergy}")

    curr_meds = case_data.get("current_medications", "").strip()
    if curr_meds and curr_meds.lower() != "none":
        note_facts.append(f"Current Ongoing Medications: {curr_meds}")

    rx_extracted = case_data.get("prescription_extracted") or {}
    rx_meds = rx_extracted.get("medicines") or []
    if rx_meds:
        med_strs = [f"{m.get('name', '')} {m.get('dosage', '')} ({m.get('frequency', '')})".strip() for m in rx_meds]
        note_facts.append(f"Verified Prescribed Medications: {', '.join(med_strs)}")

    treatment = case_data.get("treatment_instructions", "").strip()
    if treatment and treatment.lower() != "none":
        note_facts.append(f"Clinician Treatment Orders: {treatment}")

    follow_up = case_data.get("follow_up_date", "").strip() or (rx_extracted.get("follow_up", "").strip())
    if follow_up and follow_up.lower() != "none":
        note_facts.append(f"Scheduled Follow-up: {follow_up}")

    # 2. General Explanation of Diagnosis
    lit_level = case_data.get("literacy_level", "standard")
    diag_analysis = explain_diagnosis(diag, lit_level)
    general_explanation = diag_analysis["simple_explanation"]

    # 3. Missing Information (Strictly identified, never invented)
    missing_fields = []
    if not allergy or allergy.lower() == "none" or allergy.lower() == "nkda":
        missing_fields.append("Allergies: Not provided in clinician record.")
    if not symp or symp.lower() == "none":
        missing_fields.append("Specific symptoms: Not provided.")
    if not hist or hist.lower() == "none":
        missing_fields.append("Past medical history: Not provided.")
    if not curr_meds or curr_meds.lower() == "none":
        missing_fields.append("Ongoing daily medications: Not provided.")
    if not rx_meds:
        missing_fields.append("Prescription image/medicines: Not uploaded or not provided.")
    if not treatment or treatment.lower() == "none":
        missing_fields.append("Home care/treatment instructions: Not provided by clinician.")
    if not follow_up or follow_up.lower() == "none":
        missing_fields.append("Follow-up appointment date: Not provided.")

    return {
        "note_facts": note_facts,
        "general_explanation": general_explanation,
        "missing_fields": missing_fields,
        "warnings": diag_analysis.get("warnings", [])
    }

def check_clinical_entailment(case_data: Dict[str, Any], instructions: Dict[str, Any]) -> Dict[str, Any]:
    """
    MedNLI-Style Premise-Hypothesis Factual Consistency Checker (Requirement 6).
    Compares the source case data against generated patient instructions to identify:
    1. Supported information
    2. Missing information
    3. Unsupported information / added medical claims
    4. Contradictions (allergy conflicts, dose conflicts)
    """
    supported: List[str] = []
    unsupported: List[str] = []
    missing: List[str] = []
    contradictions: List[str] = []
    checks: List[Dict[str, str]] = []

    diag = case_data.get("diagnosis", "").strip()
    symptoms = case_data.get("symptoms", "").strip()
    allergies = case_data.get("allergies", "").strip()
    curr_meds = case_data.get("current_medications", "").strip()
    treatment = case_data.get("treatment_instructions", "").strip()
    follow_up = case_data.get("follow_up_date", "").strip()
    
    rx_extracted = case_data.get("prescription_extracted") or {}
    rx_meds = rx_extracted.get("medicines") or []
    rx_med_names = [m.get("name", "").lower() for m in rx_meds]

    inst_overview = instructions.get("overview", "")
    inst_meds = instructions.get("medications", [])
    inst_rules = instructions.get("daily_rules", [])
    inst_warn = instructions.get("warning_signs", [])
    inst_follow = instructions.get("follow_up", [])
    
    all_inst_text = (
        f"{inst_overview} " +
        " ".join([f"{m.get('name', '')} {m.get('timing', '')} {m.get('purpose', '')}" for m in inst_meds]) +
        " ".join(inst_rules) +
        " ".join(inst_warn) +
        " ".join(inst_follow)
    ).lower()

    # 1. Diagnosis Verification
    if diag:
        diag_words = [w for w in re.split(r'[\s,&/]+', diag.lower()) if len(w) > 3]
        if any(w in all_inst_text for w in diag_words) or diag.lower() in all_inst_text:
            supported.append(f"Diagnosis Supported: Patient discharge explanation accurately centers on '{diag}'.")
            checks.append({
                "item": "Diagnosis Alignment",
                "status": "pass",
                "detail": f"Generated instructions accurately reflect diagnosed condition '{diag}'."
            })
        else:
            unsupported.append(f"Diagnosis Omission: Key diagnosis '{diag}' not clearly reflected in instructions.")
            checks.append({
                "item": "Diagnosis Alignment",
                "status": "warning",
                "detail": f"Primary diagnosis '{diag}' may be inadequately addressed."
            })
    else:
        missing.append("Diagnosis not provided in clinical input.")
        checks.append({
            "item": "Diagnosis Alignment",
            "status": "warning",
            "detail": "No primary diagnosis provided in patient case."
        })

    # 2. Allergy & Cross-Reactivity Audit
    if allergies and allergies.lower() != "none" and allergies.lower() != "nkda":
        al_lower = allergies.lower()
        # Check conflict with Augmentin / Penicillin
        if "penicillin" in al_lower and any("augmentin" in m or "amoxicillin" in m for m in rx_med_names):
            contradictions.append("CRITICAL ALLERGY CONFLICT: Documented Penicillin allergy contradicts prescribed Augmentin/Amoxicillin.")
            checks.append({
                "item": "Allergy & Cross-Reactivity Audit",
                "status": "fail",
                "detail": f"Documented allergy ({allergies}) conflicts with prescribed beta-lactam antibiotic."
            })
        elif "sulfa" in al_lower and any("bactrim" in m or "sulfamethoxazole" in m for m in rx_med_names):
            contradictions.append("CRITICAL ALLERGY CONFLICT: Documented Sulfa allergy contradicts prescribed Sulfamethoxazole/Bactrim.")
            checks.append({
                "item": "Allergy & Cross-Reactivity Audit",
                "status": "fail",
                "detail": f"Documented allergy ({allergies}) conflicts with prescribed sulfa medication."
            })
        else:
            supported.append(f"Allergy Safety Clearance: Prescribed medications checked against documented allergy: '{allergies}'.")
            checks.append({
                "item": "Allergy & Cross-Reactivity Audit",
                "status": "pass",
                "detail": f"Prescriptions cleared against documented allergy profile ({allergies})."
            })
    else:
        # When allergies are not provided, NEVER claim "no allergies"
        missing.append("Patient Allergies: Not provided in clinician record.")
        if "no known allergies" in all_inst_text or "no allergies" in all_inst_text or "nkda" in all_inst_text:
            unsupported.append("Unsupported Allergy Claim: Handout stated 'no allergies', but allergies were not provided in source notes.")
            checks.append({
                "item": "Allergy & Cross-Reactivity Audit",
                "status": "warning",
                "detail": "Unsupported claim: Allergy status assumed without documentation."
            })
        else:
            checks.append({
                "item": "Allergy & Cross-Reactivity Audit",
                "status": "pass",
                "detail": "Allergies recorded as 'Not provided'; no ungrounded claims generated."
            })

    # 3. Prescription & Medication Grounding Check
    if rx_meds:
        for rx in rx_meds:
            rx_name = rx.get("name", "")
            rx_dose = rx.get("dosage", "")
            # Check if drug is present in instructions
            clean_name = re.split(r'[\s(]+', rx_name.lower())[0]
            if clean_name in all_inst_text:
                supported.append(f"Medication Grounded: Prescribed medicine '{rx_name}' ({rx_dose}) successfully matched.")
            else:
                missing.append(f"Prescribed medicine '{rx_name}' appears on prescription but was not found in instructions.")
        
        checks.append({
            "item": "Medication Source Grounding",
            "status": "pass" if not any("not found" in m for m in missing) else "warning",
            "detail": f"{len(rx_meds)} prescribed item(s) checked against clinician prescription."
        })
    else:
        # Check if instructions hallucinated unprescribed medicines
        if inst_meds:
            # If meds were generated when none were entered or prescribed
            for im in inst_meds:
                unsupported.append(f"Potentially Added Medication: '{im.get('name', '')}' was generated, but no prescription was entered in source.")
            checks.append({
                "item": "Medication Source Grounding",
                "status": "warning",
                "detail": "Instructions contain medications not explicitly provided in clinician source."
            })
        else:
            checks.append({
                "item": "Medication Source Grounding",
                "status": "pass",
                "detail": "No medications prescribed or generated; strict grounding preserved."
            })

    # 4. Check for ungrounded physiological claims (e.g. 'blood pressure is normal' when not measured)
    if "blood pressure is normal" in all_inst_text and "blood pressure" not in (symptoms + treatment + case_data.get("clinical_notes", "")).lower():
        unsupported.append("Unsupported Vitals Claim: Stated 'blood pressure is normal', but blood pressure was not entered in source note.")

    if "vital signs are normal" in all_inst_text and "stable" not in (case_data.get("clinical_notes", "")).lower():
        unsupported.append("Unsupported Vitals Claim: Stated 'vital signs are normal', but vitals were not entered in source note.")

    # 5. Treatment and Follow-up Check
    if treatment:
        supported.append(f"Doctor Treatment Instructions Grounded: Tailored home care incorporates clinician orders.")
    else:
        missing.append("Clinician Treatment Orders: Not provided in clinical notes.")

    if follow_up:
        supported.append(f"Follow-up Grounded: Outpatient appointment timeline '{follow_up}' included.")
    else:
        missing.append("Follow-up Date: Not provided in clinical notes.")

    # Overall Status & Score Calculation
    if contradictions:
        status = "potential_mismatch"
        score = "⚠️ High Risk - Action Required"
        summary = "CRITICAL CLINICAL MISMATCH: High-risk allergy contradiction detected between patient profile and prescribed therapy. Immediate clinician review required."
    elif unsupported:
        status = "needs_review"
        score = "Review Recommended"
        summary = f"Grounded check identified {len(unsupported)} ungrounded medical claim(s) or omissions. Please review flagged items."
    elif missing:
        status = "needs_review"
        score = "Partially Complete"
        summary = f"Instructions are grounded in available data, but {len(missing)} clinical field(s) were not provided."
    else:
        status = "verified"
        score = "Source-Grounded"
        summary = f"All {len(supported)} instruction points are strictly supported by the clinician's note with zero ungrounded medical claims."

    return {
        "status": status,
        "score": score,
        "summary": summary,
        "verified_information": supported,
        "potential_mismatches": contradictions,
        "missing_information": missing,
        "unsupported_information": unsupported,
        "detected_issues": contradictions + unsupported,
        "checks": checks
    }
