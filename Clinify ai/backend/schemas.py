"""
CareTranslate AI - Pydantic Request & Response Schemas
Provides data validation for dynamic patient cases, prescription extraction,
discharge generation, factual consistency audits, and clinician reviews.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PrescriptionMedicineItem(BaseModel):
    name: str = Field(..., description="Medication name")
    dosage: Optional[str] = Field(default="", description="e.g. 500 mg, 10 mL")
    frequency: Optional[str] = Field(default="", description="e.g. Twice daily, Every 8 hours")
    duration: Optional[str] = Field(default="", description="e.g. 7 days, 30 days, Ongoing")
    instructions: Optional[str] = Field(default="", description="Directions: with food, before bed, etc.")

class PrescriptionExtractedData(BaseModel):
    medicines: List[PrescriptionMedicineItem] = []
    doctor_instructions: Optional[str] = ""
    follow_up: Optional[str] = ""
    doctor_name: Optional[str] = ""
    clinic_name: Optional[str] = ""
    raw_text: Optional[str] = ""
    confidence_notice: str = "Please verify extracted information before generating instructions."

class PrescriptionUploadRequest(BaseModel):
    filename: str
    content_type: Optional[str] = "image/jpeg"
    file_base64: Optional[str] = None
    sample_id: Optional[str] = None
    raw_text: Optional[str] = None

class PrescriptionUploadResponse(BaseModel):
    success: bool = True
    filename: str
    extracted_data: PrescriptionExtractedData
    verification_notice: str = "⚠️ Please verify extracted information. OCR output must be clinician-verified before generating patient instructions."

class PatientCaseRequest(BaseModel):
    patient_name: Optional[str] = Field(default="", description="Patient Full Name")
    patient_id: Optional[str] = Field(default="", description="Medical Record Number / Patient ID")
    age: Optional[int] = Field(default=None, description="Patient Age")
    gender: Optional[str] = Field(default="", description="Patient Gender")
    preferred_language: str = Field(default="en", description="Target language (en, es, zh, vi, tl, ar, fr, hi)")
    literacy_level: str = Field(default="standard", description="Grade adaptation (basic, standard, advanced)")
    doctor_name: Optional[str] = Field(default="", description="Attending Doctor Name")
    clinic_name: Optional[str] = Field(default="", description="Hospital or Clinic Name")
    diagnosis: Optional[str] = Field(default="", description="Primary Diagnosis / Disease")
    symptoms: Optional[str] = Field(default="", description="Reported or observed symptoms")
    medical_history: Optional[str] = Field(default="", description="Past medical history")
    allergies: Optional[str] = Field(default="", description="Known drug/food allergies")
    current_medications: Optional[str] = Field(default="", description="Active ongoing medications")
    treatment_instructions: Optional[str] = Field(default="", description="Clinician orders & instructions")
    follow_up_date: Optional[str] = Field(default="", description="Follow-up timeframe or date")
    clinical_notes: Optional[str] = Field(default="", description="Additional clinical notes or SOAP notes")
    prescription_file_name: Optional[str] = None
    prescription_file_data: Optional[str] = None
    prescription_extracted: Optional[Dict[str, Any]] = None
    record_id: Optional[int] = Field(default=None, description="Existing record ID if updating")

class AuditCheckItem(BaseModel):
    item: str
    status: str = Field(..., description="pass | warning | fail")
    detail: str

class ConsistencyCheckResponse(BaseModel):
    status: str = Field(..., description="verified | needs_review | potential_mismatch")
    score: str = Field(..., description="Verification percentage score or safety level")
    summary: str
    verified_information: List[str] = []
    potential_mismatches: List[str] = []
    missing_information: List[str] = []
    unsupported_information: List[str] = []
    detected_issues: List[str] = []
    checks: List[AuditCheckItem] = []

class ConsistencyCheckRequest(BaseModel):
    case_data: Dict[str, Any]
    instructions: Dict[str, Any]
    record_id: Optional[int] = None

class GenerateCaseResponse(BaseModel):
    record_id: int
    patient_info: Dict[str, Any]
    case_data: Dict[str, Any]
    instructions: Dict[str, Any]
    consistency_check: ConsistencyCheckResponse
    readability: Dict[str, Any]
    compiled_review_text: str

class ReviewRequest(BaseModel):
    record_id: int
    clinician_name: Optional[str] = Field(default="Attending Clinician")
    edited_text: str
    approval_status: str = Field(default="approved", description="approved | draft")

class ReviewResponse(BaseModel):
    record_id: int
    approval_status: str
    approved_by: str
    approved_at: str
    message: str

class HistoryItem(BaseModel):
    id: int
    patient_name: Optional[str] = None
    patient_id: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    doctor_name: Optional[str] = None
    clinic_name: Optional[str] = None
    diagnosis: Optional[str] = None
    selected_language: str
    literacy_level: str
    consistency_status: str
    approval_status: str
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    created_at: str
    timestamp_formatted: Optional[str] = None

# Backward compatibility schema for legacy generate request
class LegacyGenerateRequest(BaseModel):
    clinical_note: str = Field(..., min_length=10)
    preferred_language: str = Field(default="en")
    literacy_level: str = Field(default="standard")

class DiagnosisAnalysisRequest(BaseModel):
    diagnosis: str = Field(..., description="Diagnosis/Disease to analyze")
    symptoms: Optional[str] = Field(default="", description="Reported symptoms")
    medical_history: Optional[str] = Field(default="", description="Patient medical history")
    allergies: Optional[str] = Field(default="", description="Patient allergies")
    current_medications: Optional[str] = Field(default="", description="Current medications")
    treatment_instructions: Optional[str] = Field(default="", description="Treatment instructions")
    clinical_notes: Optional[str] = Field(default="", description="Additional clinical notes")
    literacy_level: Optional[str] = Field(default="standard", description="basic | standard | advanced")
    preferred_language: Optional[str] = Field(default="en", description="Target language")

class DiagnosisAnalysisResponse(BaseModel):
    diagnosis: str
    simple_explanation: str
    source_supported_points: List[str] = []
    general_disease_explanation: str = ""
    missing_information: List[str] = []
    danger_signs: List[str] = []
    warnings: List[str] = []
    disclaimer: str = "AI-generated patient-friendly information must be reviewed and approved by a clinician before being provided to the patient."

class PrescriptionAnalysisRequest(BaseModel):
    filename: Optional[str] = "prescription.jpg"
    content_type: Optional[str] = "image/jpeg"
    file_base64: Optional[str] = None
    sample_id: Optional[str] = None
    raw_text: Optional[str] = None

class PrescriptionAnalysisResponse(BaseModel):
    success: bool = True
    filename: str
    extracted_data: PrescriptionExtractedData
    verification_notice: str = "AI-extracted — Clinician verification required"
    disclaimer: str = "AI-generated patient-friendly information must be reviewed and approved by a clinician before being provided to the patient."
