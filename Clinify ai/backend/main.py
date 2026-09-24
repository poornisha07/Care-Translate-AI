"""
CareTranslate AI - FastAPI Application Backend
Provides RESTful APIs for dynamic patient cases, prescription OCR & AI extraction,
personalized discharge instructions, 4-part consistency checks, clinician review,
and SQLite persistence.
"""

import os
import json
from fastapi import FastAPI, HTTPException, status, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Dict, Any, Optional, Union

from .database import (
    init_db,
    save_case_record,
    update_review,
    update_consistency,
    get_history,
    get_record_by_id,
    delete_record_by_id
)
from .schemas import (
    PatientCaseRequest,
    GenerateCaseResponse,
    ConsistencyCheckRequest,
    ConsistencyCheckResponse,
    ReviewRequest,
    ReviewResponse,
    HistoryItem,
    PrescriptionUploadRequest,
    PrescriptionUploadResponse,
    PrescriptionExtractedData,
    DiagnosisAnalysisRequest,
    DiagnosisAnalysisResponse,
    PrescriptionAnalysisRequest,
    PrescriptionAnalysisResponse
)
from .medical_knowledge.knowledge_engine import (
    explain_diagnosis,
    separate_source_facts
)
from .ai_service import (
    extract_prescription_from_upload,
    generate_dynamic_patient_instructions,
    check_dynamic_case_consistency,
    calculate_readability_metrics,
    compile_review_text
)

# Initialize Database on startup
init_db()

app = FastAPI(
    title="CareTranslate AI API",
    description="Dynamic clinical patient case management, prescription OCR extraction, plain-language discharge generation, and factual consistency auditing.",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root directory path for static files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_DIR = os.path.join(BASE_DIR, "css")
JS_DIR = os.path.join(BASE_DIR, "js")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

# Mount static asset folders
if os.path.exists(CSS_DIR):
    app.mount("/css", StaticFiles(directory=CSS_DIR), name="css")
if os.path.exists(JS_DIR):
    app.mount("/js", StaticFiles(directory=JS_DIR), name="js")

@app.get("/", include_in_schema=False)
async def serve_index():
    """Serve the single-page frontend application"""
    if os.path.exists(INDEX_PATH):
        return FileResponse(INDEX_PATH)
    return {"message": "CareTranslate AI Backend is running. Please access /docs for API documentation."}

@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CareTranslate AI",
        "version": "2.0.0",
        "database": "connected"
    }

# ================= PRESCRIPTION OCR & EXTRACTION ENDPOINT =================

@app.post("/api/prescriptions/upload-and-extract", response_model=PrescriptionUploadResponse, tags=["Prescription"])
async def upload_and_extract_prescription(request: PrescriptionUploadRequest):
    """
    Process uploaded doctor prescription (JPG, JPEG, PNG, or PDF).
    Extracts medicines, dosages, administration frequency, duration, doctor instructions, and follow-up.
    Always flags output with a verification notice so clinicians must review before generation.
    """
    extracted = extract_prescription_from_upload(
        filename=request.filename,
        content_type=request.content_type or "image/jpeg",
        file_base64=request.file_base64,
        sample_id=request.sample_id,
        raw_text=request.raw_text
    )

    return PrescriptionUploadResponse(
        success=True,
        filename=request.filename,
        extracted_data=PrescriptionExtractedData(**extracted),
        verification_notice="⚠️ Please verify extracted information. OCR output must be clinician-verified before generating patient instructions."
    )

# ================= DIAGNOSIS & PRESCRIPTION ANALYSIS ENDPOINTS =================

@app.post("/api/analyze-diagnosis", response_model=DiagnosisAnalysisResponse, tags=["Diagnosis Analysis"])
async def analyze_diagnosis_endpoint(request: DiagnosisAnalysisRequest):
    """
    Dynamically analyzes clinician-entered diagnosis without fixed allergy templates.
    Returns plain-language explanation, source-supported facts, missing information, and warnings.
    """
    analysis = explain_diagnosis(request.diagnosis, request.literacy_level or "standard")
    source_facts = separate_source_facts(request.dict())
    
    return DiagnosisAnalysisResponse(
        diagnosis=analysis["diagnosis"],
        simple_explanation=analysis["simple_explanation"],
        source_supported_points=source_facts.get("note_facts", []) or analysis.get("source_supported_points", []),
        general_disease_explanation=analysis["simple_explanation"],
        missing_information=source_facts.get("missing_fields", []) or analysis.get("missing_information", []),
        danger_signs=analysis.get("warnings", []),
        warnings=analysis.get("warnings", []),
        disclaimer="AI-generated patient-friendly information must be reviewed and approved by a clinician before being provided to the patient."
    )

@app.post("/api/analyze-prescription", response_model=PrescriptionAnalysisResponse, tags=["Prescription Analysis"])
async def analyze_prescription_endpoint(request: PrescriptionAnalysisRequest):
    """
    Analyze uploaded prescription image or clinical prescription text.
    Extracts medications with clinician verification notice.
    """
    extracted = extract_prescription_from_upload(
        filename=request.filename or "prescription.jpg",
        content_type=request.content_type or "image/jpeg",
        file_base64=request.file_base64,
        sample_id=request.sample_id,
        raw_text=request.raw_text
    )
    return PrescriptionAnalysisResponse(
        success=True,
        filename=request.filename or "prescription.jpg",
        extracted_data=PrescriptionExtractedData(**extracted),
        verification_notice=extracted.get("confidence_notice") or "AI-extracted — Clinician verification required",
        disclaimer="AI-generated patient-friendly information must be reviewed and approved by a clinician before being provided to the patient."
    )

# ================= DYNAMIC GENERATION ENDPOINT =================

@app.post("/api/generate", tags=["Translation"])
async def generate_instructions(payload: Dict[str, Any] = Body(...)):
    """
    Generates personalized discharge instructions combining:
    Patient Information + Clinical Notes + Extracted Prescription Data.
    Performs factual consistency check and persists as an independent record in SQLite.
    Supports both dynamic PatientCaseRequest format and legacy clinical_note payloads.
    """
    # Normalize payload
    case_data = payload.copy()
    
    # Handle legacy clinical_note input if submitted
    if "clinical_note" in case_data and not case_data.get("diagnosis"):
        raw_note = case_data["clinical_note"]
        case_data["clinical_notes"] = raw_note
        # Simple extraction for demo
        if "PATIENT:" in raw_note:
            import re
            m = re.search(r"PATIENT:\s*([^\n|]+)", raw_note)
            if m: case_data["patient_name"] = m.group(1).strip()
            d = re.search(r"DIAGNOSIS:\s*([^\n|]+)", raw_note)
            if d: case_data["diagnosis"] = d.group(1).strip()

    lang = case_data.get("preferred_language") or "en"
    literacy = case_data.get("literacy_level") or "standard"

    # 1. Generate personalized instructions
    instructions = generate_dynamic_patient_instructions(
        case_data=case_data,
        language=lang,
        literacy=literacy
    )

    # 2. Perform 4-part clinical safety audit
    consistency_result = check_dynamic_case_consistency(
        case_data=case_data,
        instructions=instructions
    )

    # 3. Compile editable review text & calculate readability
    compiled_text = compile_review_text(instructions)
    readability = calculate_readability_metrics(
        case_text=f"{case_data.get('diagnosis', '')} {case_data.get('treatment_instructions', '')} {case_data.get('clinical_notes', '')}",
        generated_text=compiled_text
    )

    # 4. Save to SQLite database as independent record
    record_id = save_case_record(
        case_data=case_data,
        generated_instructions=instructions,
        consistency_result=consistency_result,
        readability_metrics=readability
    )

    patient_info = {
        "name": case_data.get("patient_name") or "",
        "mrn": case_data.get("patient_id") or "",
        "patient_id": case_data.get("patient_id") or "",
        "age": case_data.get("age"),
        "gender": case_data.get("gender") or "",
        "diagnosis": case_data.get("diagnosis") or "",
        "doctor_name": case_data.get("doctor_name") or "",
        "clinic_name": case_data.get("clinic_name") or ""
    }

    return {
        "record_id": record_id,
        "patient_info": patient_info,
        "case_data": case_data,
        "instructions": instructions,
        "consistency_check": consistency_result,
        "readability": readability,
        "compiled_review_text": compiled_text
    }

# ================= CONSISTENCY CHECK ENDPOINT =================

@app.post("/api/check-consistency", response_model=ConsistencyCheckResponse, tags=["Safety Audit"])
async def audit_consistency(request: ConsistencyCheckRequest):
    """
    Compare generated discharge instructions with the entered clinical information and prescription data.
    Returns verified information, potential mismatches, missing information, and unsupported information.
    """
    audit_result = check_dynamic_case_consistency(
        case_data=request.case_data,
        instructions=request.instructions
    )

    if request.record_id:
        update_consistency(
            record_id=request.record_id,
            consistency_status=audit_result["status"],
            consistency_result=audit_result
        )

    return ConsistencyCheckResponse(**audit_result)

# ================= CLINICIAN REVIEW & APPROVAL ENDPOINT =================

@app.post("/api/review", response_model=ReviewResponse, tags=["Clinician Review"])
async def review_and_approve(request: ReviewRequest):
    """
    Allow clinicians to review, edit, approve, and electronically sign off on discharge instructions.
    Saves the final approved version with digital timestamp.
    """
    existing = get_record_by_id(request.record_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient record with ID {request.record_id} not found."
        )

    updated = update_review(
        record_id=request.record_id,
        clinician_name=request.clinician_name or "Attending Clinician",
        edited_text=request.edited_text,
        approval_status=request.approval_status
    )

    return ReviewResponse(
        record_id=request.record_id,
        approval_status=updated.get("approval_status", "approved"),
        approved_by=updated.get("approved_by", request.clinician_name),
        approved_at=updated.get("approved_at", "Just now"),
        message="Discharge instructions successfully reviewed and electronically signed."
    )

# ================= HISTORY ENDPOINTS =================

@app.get("/api/history", response_model=List[HistoryItem], tags=["History"])
async def get_discharge_history(limit: int = Query(default=50, ge=1, le=100)):
    """
    Fetch history of multiple patient cases stored in SQLite database.
    """
    records = get_history(limit=limit)
    return [HistoryItem(**r) for r in records]

@app.get("/api/history/{record_id}", tags=["History"])
async def get_discharge_record_detail(record_id: int):
    """
    Retrieve full details of a specific historical patient case to load back into workspace.
    """
    record = get_record_by_id(record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient record with ID {record_id} not found."
        )
    return record

@app.delete("/api/history/{record_id}", tags=["History"])
async def delete_discharge_record(record_id: int):
    """
    Delete a specific patient case record.
    """
    success = delete_record_by_id(record_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record {record_id} not found."
        )
    return {"message": f"Patient record {record_id} deleted successfully."}
