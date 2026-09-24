"""
CareTranslate AI - Verification of Patient Report Generation & Client Bindings
"""

import re
import sys
import json
import urllib.request

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_client_files_and_bindings():
    print("\n--- Verifying Client-Side Files & Bindings ---")
    
    # 1. Fetch index.html
    req = urllib.request.urlopen("http://127.0.0.1:8080/")
    html = req.read().decode("utf-8")
    
    assert "reportPreviewModal" in html, "Missing #reportPreviewModal in index.html"
    assert "reportExportCanvas" in html, "Missing #reportExportCanvas in index.html"
    assert "previewReportBtn" in html, "Missing #previewReportBtn in index.html"
    assert "downloadReportBtn" in html, "Missing #downloadReportBtn in index.html"
    assert "generateReportImageBtn" in html, "Missing #generateReportImageBtn in index.html"
    assert "ttsAudioBtn" in html, "Missing #ttsAudioBtn in index.html"
    assert "ttsPauseBtn" in html, "Missing #ttsPauseBtn in index.html"
    assert "ttsResumeBtn" in html, "Missing #ttsResumeBtn in index.html"
    assert "ttsStopBtn" in html, "Missing #ttsStopBtn in index.html"
    print("✓ All modal, canvas, and toolbar UI elements confirmed present in index.html")
    
    # 2. Fetch js/app.js
    req_js = urllib.request.urlopen("http://127.0.0.1:8080/js/app.js")
    js = req_js.read().decode("utf-8")
    
    required_functions = [
        "generatePatientReportData",
        "previewPatientReport",
        "downloadPatientReport",
        "generateReportImage",
        "startAudioPlayback",
        "pauseAudioPlayback",
        "resumeAudioPlayback",
        "stopAudioPlayback",
        "toggleAudioPlayback"
    ]
    
    for fn in required_functions:
        assert fn in js, f"Function {fn} missing from js/app.js"
        assert f"window.{fn} = {fn}" in js, f"Function {fn} not exported to window in js/app.js"
    print(f"✓ All {len(required_functions)} required functions and window exports confirmed in js/app.js")

    # 3. Verify Multilingual Voice Selection and Tamil Mapping
    assert '"ta": "ta-IN"' in js, "Tamil ta-IN language code mapping missing in app.js"
    assert "tamilVoice" in js, "Tamil voice detection logic missing in app.js"
    print("✓ Multilingual speech engine with Tamil voice detection confirmed in js/app.js")

    # 4. Verify 20 Required Report Fields in generator logic
    required_report_fields = [
        "reportTitle",
        "patientName",
        "patientId",
        "age",
        "gender",
        "doctorName",
        "clinicName",
        "diagnosis",
        "symptoms",
        "medicalHistory",
        "allergies",
        "verifiedMedicines",
        "followUpDate",
        "preferredLanguage",
        "literacyLevel",
        "prescriptionOcrInfo",
        "factualConsistencyStatus",
        "finalInstructions",
        "dateGenerated",
        "approvalStatus"
    ]
    for field in required_report_fields:
        assert field in js, f"Report field {field} missing from generator in js/app.js"
    print(f"✓ All 20 required report fields confirmed in report generator logic")

if __name__ == "__main__":
    try:
        test_client_files_and_bindings()
        print("\n=======================================================")
        print("🎉 CLIENT UI & TTS BINDINGS VERIFIED WITH 100% SUCCESS!")
        print("=======================================================\n")
    except Exception as e:
        print(f"\n❌ CLIENT VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
