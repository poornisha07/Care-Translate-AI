"""
CareTranslate AI - Medical Knowledge & Grounding Engine
Provides dynamic disease terminology understanding, MedNLI-style factual consistency auditing,
and source-grounded patient instruction formatting.
"""

from .knowledge_engine import (
    explain_diagnosis,
    get_danger_signs_for_diagnosis,
    separate_source_facts,
    check_clinical_entailment
)

__all__ = [
    "explain_diagnosis",
    "get_danger_signs_for_diagnosis",
    "separate_source_facts",
    "check_clinical_entailment"
]
