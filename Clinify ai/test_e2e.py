import subprocess
import time
import json
import urllib.request
import asyncio
import websockets
import sys

# Ensure UTF-8 output on Windows console
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding='utf-8')

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
URL = "http://127.0.0.1:8080/"

async def run_e2e_tests():
    print(">>> Starting Edge process for End-to-End Verification of Dynamic Cases & OCR...")
    proc = subprocess.Popen([
        EDGE_PATH,
        "--headless=new",
        "--remote-debugging-port=9222",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        URL
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    await asyncio.sleep(2.5)

    ws_url = None
    try:
        req = urllib.request.urlopen("http://127.0.0.1:9222/json/list")
        tabs = json.loads(req.read().decode('utf-8'))
        for t in tabs:
            if t.get('type') == 'page':
                ws_url = t.get('webSocketDebuggerUrl')
                break
    except Exception as e:
        print("Failed to get tabs:", e)
        proc.terminate()
        return False

    print(">>> Connected to WebSocket:", ws_url)
    console_logs = []
    errors = []

    try:
        async with websockets.connect(ws_url) as ws:
            msg_id = 0

            async def send(method, params=None):
                nonlocal msg_id
                msg_id += 1
                payload = {"id": msg_id, "method": method, "params": params or {}}
                await ws.send(json.dumps(payload))
                while True:
                    resp = await ws.recv()
                    data = json.loads(resp)
                    if data.get("id") == msg_id:
                        return data
                    elif data.get("method") == "Runtime.consoleAPICalled":
                        console_logs.append(data["params"])
                    elif data.get("method") == "Runtime.exceptionThrown":
                        errors.append(data["params"])

            async def eval_js(expression):
                res = await send("Runtime.evaluate", {
                    "expression": expression,
                    "returnByValue": True,
                    "awaitPromise": True
                })
                return res.get("result", {}).get("result", {}).get("value")

            await send("Runtime.enable")
            await send("Page.enable")

            # 1. Checking Page Load & Title
            print(">>> 1. Checking Page Load & Title...")
            for _ in range(25):
                is_ready = await eval_js("typeof window.handleNewPatientCase === 'function'")
                if is_ready:
                    break
                await asyncio.sleep(0.3)

            title = await eval_js("document.title")
            print("    Page Title:", title)
            assert "CareTranslate AI" in title

            # Check Nav Button
            new_btn_exists = await eval_js("Boolean(document.getElementById('btnNewCaseNav'))")
            assert new_btn_exists, "'+ New Patient Case' nav button must exist"
            print("    ✓ '+ New Patient Case' button confirmed in header")

            # 2. Loading Patient 1: Maria Gonzalez
            print(">>> 2. Loading Test Patient 1: Maria Gonzalez (Diabetes & Wound Care)...")
            await eval_js("loadSampleCase('maria_gonzalez')")
            await asyncio.sleep(0.5)

            p1_name = await eval_js("document.getElementById('patientNameInput').value")
            p1_id = await eval_js("document.getElementById('patientIdInput').value")
            p1_doc = await eval_js("document.getElementById('doctorNameInput').value")
            p1_rx_count = await eval_js("document.querySelectorAll('#extractedMedicinesList .medicine-item-row').length")
            
            print(f"    Patient 1 Form: Name='{p1_name}', ID='{p1_id}', Doctor='{p1_doc}', Extracted Rx Count={p1_rx_count}")
            assert p1_name == "Maria Gonzalez"
            assert p1_id == "MRN-501928"
            assert p1_rx_count >= 1

            # Check Verification Alert notice is visible (Requirement 3)
            rx_section_visible = await eval_js("!document.getElementById('extractedPrescriptionSection').classList.contains('hidden')")
            assert rx_section_visible, "Extracted prescription section must be visible"
            print("    ✓ Extracted prescription editable section and verification notice visible")

            # 3. Generating Instructions for Patient 1
            print(">>> 3. Generating Instructions for Patient 1...")
            await eval_js("handleGenerate(false)")
            await asyncio.sleep(1.0)

            ui_state1 = await eval_js("AppState.uiState")
            assert ui_state1 == "success", f"UI State should be success, got {ui_state1}"

            p1_banner = await eval_js("document.getElementById('patientHeaderBanner').innerText")
            p1_audit = await eval_js("document.getElementById('factualAuditCard').innerText")
            p1_handout = await eval_js("document.getElementById('dischargeInstructionsBody').innerText")
            
            print(f"    Banner: {p1_banner[:60]}...")
            print(f"    Audit Status: {p1_audit[:60]}...")
            assert "Maria Gonzalez" in p1_banner
            assert "Verified" in p1_audit
            assert "Cephalexin" in p1_handout or "Keflex" in p1_handout

            # 4. Clinician Review & Digital Sign-off for Patient 1
            print(">>> 4. Clinician Review & Digital Sign-off for Patient 1...")
            await eval_js("document.getElementById('clinicianSignatureInput').value = 'Dr. Carlos Ramirez, MD'")
            await eval_js("handleApproveInstructions()")
            await asyncio.sleep(0.5)

            p1_approved = await eval_js("AppState.isReviewApproved")
            p1_stamp = await eval_js("document.getElementById('patientCardApprovalStamp').innerText")
            assert p1_approved == True
            assert "Carlos Ramirez" in p1_stamp
            print("    ✓ Patient 1 digitally signed & approved stamp rendered")

            # 5. Testing '+ New Patient Case' Form Reset (Requirement 6)
            print(">>> 5. Testing '+ New Patient Case' Form Reset (Requirement 6)...")
            await eval_js("handleNewPatientCase()")
            await asyncio.sleep(0.3)

            reset_name = await eval_js("document.getElementById('patientNameInput').value")
            reset_id = await eval_js("document.getElementById('patientIdInput').value")
            reset_diag = await eval_js("document.getElementById('diagnosisInput').value")
            reset_state = await eval_js("AppState.uiState")
            
            print(f"    After Reset: Name='{reset_name}', ID='{reset_id}', UI State='{reset_state}'")
            assert reset_name == ""
            assert reset_id == ""
            assert reset_state == "empty"
            print("    ✓ Form completely reset for new case!")

            # 6. Entering Patient 2: David Chen (Requirement 11: Different Patient)
            print(">>> 6. Entering Test Patient 2: David Chen (Bronchitis & Hypertension)...")
            await eval_js("loadSampleCase('david_chen')")
            await asyncio.sleep(0.5)

            p2_name = await eval_js("document.getElementById('patientNameInput').value")
            p2_id = await eval_js("document.getElementById('patientIdInput').value")
            p2_doc = await eval_js("document.getElementById('doctorNameInput').value")
            print(f"    Patient 2 Form: Name='{p2_name}', ID='{p2_id}', Doctor='{p2_doc}'")
            assert p2_name == "David Chen"
            assert p2_id == "MRN-618402"

            # 7. Generating Instructions for Patient 2
            print(">>> 7. Generating Instructions for Patient 2...")
            await eval_js("handleGenerate(false)")
            await asyncio.sleep(1.0)

            p2_banner = await eval_js("document.getElementById('patientHeaderBanner').innerText")
            p2_handout = await eval_js("document.getElementById('dischargeInstructionsBody').innerText")

            print(f"    Patient 2 Banner: {p2_banner[:60]}...")
            assert "David Chen" in p2_banner
            assert "Maria Gonzalez" not in p2_banner # Zero leakage!
            assert "Albuterol" in p2_handout or "Tessalon" in p2_handout or "ProAir" in p2_handout
            assert "Cephalexin" not in p2_handout     # No medication mixing!
            print("    ✓ Verified Patient 2 instructions are personalized and completely isolated from Patient 1!")

            # 8. Testing Case History Modal (Requirement 7)
            print(">>> 8. Testing Case History Modal (Requirement 7)...")
            await eval_js("fetchHistoryList()")
            await asyncio.sleep(0.5)
            await eval_js("openModal('historyModal')")
            await asyncio.sleep(0.3)

            hist_count = await eval_js("document.querySelectorAll('#historyListContainer > div').length")
            hist_text = await eval_js("document.getElementById('historyListContainer').innerText")
            print(f"    History cases count: {hist_count}")
            assert hist_count >= 2
            assert "Maria Gonzalez" in hist_text
            assert "David Chen" in hist_text
            print("    ✓ Case History modal lists multiple independent patient cases!")

            # 9. Verify Browser Console Errors
            print(f">>> 9. Checking Browser Console Health...")
            print(f"    Console errors detected: {len(errors)}")
            assert len(errors) == 0, f"Unexpected browser errors: {errors}"
            print("    ✓ Zero (0) JavaScript console errors throughout complete multi-patient workflow!")

            print("\n🎉 ALL END-TO-END BROWSER TESTS PASSED SUCCESSFULLY!")
            return True

    finally:
        proc.terminate()
        proc.wait(timeout=3)
        print(">>> Browser terminated cleanly.")

if __name__ == "__main__":
    ok = asyncio.run(run_e2e_tests())
    sys.exit(0 if ok else 1)
